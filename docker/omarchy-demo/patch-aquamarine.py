"""Build-time patches for Aquamarine 0.15.0 (Hyprland's backend).

Aquamarine is GPL-3.0; these patches are applied in-image at build time and are
kept in this repository to satisfy source provision. Two independent fixes:

1. **Registry version clamp** (always applied)
   Aquamarine binds Wayland protocol globals with hardcoded versions
   (wl_compositor 6, wl_seat 9, ...) and crashes against capture compositors
   advertising older globals. Clamp every bind to the advertised version —
   same 0.15.0 ABI, one-line behavioral fix.

2. **wl_shm output presentation** (opt-in via `AQ_PRESENT_SHM=1` at runtime)
   Aquamarine's `CWaylandBuffer` presents every output frame as a
   zwp_linux_dmabuf_v1 buffer. Capture compositors without GPU import (e.g.
   pixelflux/smithay on a virtual-GPU host) fail to import those dmabufs and
   never send `wl_buffer.release`, which deadlocks the swapchain and prevents
   every nested client from mapping its first frame. With the env set, output
   frames are instead presented as plain wl_shm buffers — the same CPU path
   ordinary software clients use — at the cost of one memcpy per frame.

   Design notes (verified against v0.15.0 source):
   - The swapchain stays GBM-allocated (Hyprland's renderer needs it); only
     *presentation* changes. Pixels are copied with the existing public
     `IBuffer::beginDataPtr()/endDataPtr()` API (same API the cursor path
     uses), so no manual dmabuf mmap/DMA_BUF sync ioctls are needed.
   - One memfd-backed wl_shm pool per swapchain buffer slot, mirroring how
     normal shm clients keep N buffers in flight. The pool object is reset
     right after `sendCreateBuffer` (the wl_buffer outlives the pool resource
     — the same pattern the cursor path already relies on), while the mmap
     stays valid for repeated copies.
   - Assumes a linear, CPU-mappable bo (true for software-rendered virtual
     GPUs). A stride/size mismatch is logged and skips the copy rather than
     corrupting the frame.
   - When the env is unset, zero behavior change (original dmabuf path).
"""
import pathlib

SRC = pathlib.Path('/tmp/aq-src/src/backend/Wayland.cpp')
HDR = pathlib.Path('/tmp/aq-src/include/aquamarine/backend/Wayland.hpp')


def patch_version_clamps(src: str) -> str:
    # getenv must be visible in Wayland.cpp; be explicit rather than relying on
    # transitive includes.
    if '#include <cstdlib>' not in src:
        src = src.replace('#include <cstring>', '#include <cstring>\n#include <cstdlib>', 1)
    pairs = [
        ('&wl_seat_interface, 9)', '&wl_seat_interface, std::min(9u, version))'),
        ('&xdg_wm_base_interface, 6)', '&xdg_wm_base_interface, std::min(6u, version))'),
        ('&wl_compositor_interface, 6)', '&wl_compositor_interface, std::min(6u, version))'),
        ('&wl_shm_interface, 1)', '&wl_shm_interface, std::min(1u, version))'),
        ('&zwp_linux_dmabuf_v1_interface, 4)', '&zwp_linux_dmabuf_v1_interface, std::min(4u, version))'),
    ]
    count = 0
    for old, new in pairs:
        if old in src:
            src = src.replace(old, new)
            count += 1
    assert count == 5, f'expected 5 bind sites, patched {count}'
    return src


BUFFER_OLD = '''Aquamarine::CWaylandBuffer::CWaylandBuffer(SP<IBuffer> buffer_, Hyprutils::Memory::CWeakPointer<CWaylandBackend> backend_) : buffer(buffer_), backend(backend_) {
    auto params = makeShared<CCZwpLinuxBufferParamsV1>(backend->waylandState.dmabuf->sendCreateParams());'''

BUFFER_NEW = '''// VERAGENSIA PATCH (shm-presentation): with AQ_PRESENT_SHM=1 in the environment,
// present output frames as wl_shm buffers instead of zwp_linux_dmabuf_v1 buffers.
// See the module docstring in the deployment repo for the rationale and the
// runtime-cost tradeoff. Without the env this constructor is byte-for-byte the
// upstream dmabuf path.
Aquamarine::CWaylandBuffer::CWaylandBuffer(SP<IBuffer> buffer_, Hyprutils::Memory::CWeakPointer<CWaylandBackend> backend_) : buffer(buffer_), backend(backend_) {
    if (getenv("AQ_PRESENT_SHM") && initShmPresentation())
        return;

    auto params = makeShared<CCZwpLinuxBufferParamsV1>(backend->waylandState.dmabuf->sendCreateParams());'''

SHM_METHODS = '''
// VERAGENSIA PATCH (shm-presentation): allocate a memfd-backed wl_shm pool and
// wrap it in a wl_buffer. The pool resource is dropped after buffer creation
// (same pattern as the cursor path); the mmap is kept for repeated copies.
bool Aquamarine::CWaylandBuffer::initShmPresentation() {
    auto attrs = buffer->dmabuf();
    if (!attrs.success || attrs.planes != 1) {
        backend->backend->log(AQ_LOG_ERROR, "WaylandBuffer: AQ_PRESENT_SHM needs a single-plane dmabuf buffer");
        return false;
    }

    shmStride = attrs.strides.at(0);
    shmLen    = (size_t)shmStride * attrs.size.y;

    int fd = allocateSHMFile(shmLen);
    if (fd < 0) {
        backend->backend->log(AQ_LOG_ERROR, "WaylandBuffer: AQ_PRESENT_SHM failed to allocate a shm file");
        return false;
    }

    shmMap = mmap(nullptr, shmLen, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (shmMap == MAP_FAILED) {
        backend->backend->log(AQ_LOG_ERROR, "WaylandBuffer: AQ_PRESENT_SHM failed to mmap the pool file");
        shmMap = nullptr;
        close(fd);
        return false;
    }

    auto pool = makeShared<CCWlShmPool>(backend->waylandState.shm->sendCreatePool(fd, shmLen));
    close(fd); // the mapping stays valid after close; the server holds its own fd
    if (!pool) {
        backend->backend->log(AQ_LOG_ERROR, "WaylandBuffer: AQ_PRESENT_SHM failed to create a wl_shm pool");
        munmap(shmMap, shmLen);
        shmMap = nullptr;
        return false;
    }

    waylandState.buffer =
        makeShared<CCWlBuffer>(pool->sendCreateBuffer(0, attrs.size.x, attrs.size.y, shmStride, shmFormatFromDRM(attrs.format)));
    if (!waylandState.buffer || !waylandState.buffer->resource()) {
        backend->backend->log(AQ_LOG_ERROR, "WaylandBuffer: AQ_PRESENT_SHM failed to create a wl_shm buffer");
        munmap(shmMap, shmLen);
        shmMap = nullptr;
        return false;
    }

    waylandState.buffer->setRelease([this](CCWlBuffer* r) { pendingRelease = false; });
    shmMode = true;
    backend->backend->log(AQ_LOG_WARNING, "WaylandBuffer: AQ_PRESENT_SHM active — presenting frames through wl_shm");
    return true;
}

// Copy the just-rendered frame into the shm pool before the compositor reads
// it. Uses the public beginDataPtr()/endDataPtr() CPU-mapping API (the cursor
// path already relies on it), so CPU access sync is handled by GBM.
void Aquamarine::CWaylandBuffer::syncShmPixels() {
    if (!shmMode || !shmMap)
        return;

    auto [pixelData, fmt, bufLen] = buffer->beginDataPtr(0);
    if (bufLen != shmLen) {
        backend->backend->log(AQ_LOG_ERROR, "WaylandBuffer: AQ_PRESENT_SHM stride/size mismatch, skipping copy");
        buffer->endDataPtr();
        return;
    }
    memcpy(shmMap, pixelData, shmLen);
    buffer->endDataPtr();
}

bool Aquamarine::CWaylandBuffer::good() {'''

GOOD_OLD = '''bool Aquamarine::CWaylandBuffer::good() {'''

HEADER_OLD = '''      private:
        struct {
            Hyprutils::Memory::CSharedPointer<CCWlBuffer> buffer;
        } waylandState;'''

HEADER_NEW = '''      private:
        struct {
            Hyprutils::Memory::CSharedPointer<CCWlBuffer> buffer;
        } waylandState;

        // VERAGENSIA PATCH (shm-presentation): optional wl_shm output presentation
        // for capture compositors that cannot import dmabufs (GPU-less hosts).
        // Opt-in via AQ_PRESENT_SHM=1; see docker/omarchy-demo/README.md.
        bool                            shmMode   = false;
        void*                           shmMap    = nullptr;
        size_t                          shmLen    = 0;
        uint32_t                        shmStride = 0;
        bool                            initShmPresentation();
        void                            syncShmPixels();'''

SYNC_OLD = '''    wlBuffer->pendingRelease = true;

    waylandState.surface->sendAttach(wlBuffer->waylandState.buffer.get(), 0, 0);'''

SYNC_NEW = '''    wlBuffer->pendingRelease = true;

    // VERAGENSIA PATCH (shm-presentation): copy the just-rendered frame into the
    // shm pool before the attach so the compositor reads fresh pixels. The
    // zero-copy dmabuf path needs no copy, which is why this is guarded by
    // shmMode and only exists in the opt-in presentation mode.
    wlBuffer->syncShmPixels();

    waylandState.surface->sendAttach(wlBuffer->waylandState.buffer.get(), 0, 0);'''


def main() -> None:
    src = SRC.read_text()
    src = patch_version_clamps(src)
    assert BUFFER_OLD in src, 'buffer ctor anchor not found'
    src = src.replace(BUFFER_OLD, BUFFER_NEW)
    assert GOOD_OLD in src, 'good() anchor not found'
    src = src.replace(GOOD_OLD, SHM_METHODS, 1)
    assert SYNC_OLD in src, 'commit sync anchor not found'
    src = src.replace(SYNC_OLD, SYNC_NEW)
    SRC.write_text(src)

    hdr = HDR.read_text()
    assert HEADER_OLD in hdr, 'header anchor not found'
    hdr = hdr.replace(HEADER_OLD, HEADER_NEW)
    HDR.write_text(hdr)

    print('patched: 5 registry version clamps + AQ_PRESENT_SHM wl_shm presentation path')


if __name__ == '__main__':
    main()
