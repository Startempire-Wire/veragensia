#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"

bash -n scripts/uiai-lab-live scripts/uiai-lab-push scripts/lab-ext.sh scripts/uiai-lab-remote-control

grep -q 'EXT_PARENT_HOST=/home/wirebot/uiai-lab/workforce-extension' scripts/uiai-lab-live
! grep -q '/build/focusa/source/apps/workforce-extension' scripts/uiai-lab-live scripts/uiai-lab-push
grep -q 'repair_extension_mount' scripts/uiai-lab-live
grep -q 'owner_drift:' scripts/uiai-lab-live
grep -q 'ensure_demo_daemon' scripts/uiai-lab-live
grep -q 'demo_daemon:' scripts/uiai-lab-live
grep -q 'pgrep -u abc -x plasmashell' scripts/lab-ext.sh
grep -q 'DBUS_SESSION_BUS_ADDRESS=' scripts/lab-ext.sh
grep -q 'EXT_ID=NOTFOUND' scripts/lab-ext.sh
grep -A4 'EXT_ID=NOTFOUND' scripts/lab-ext.sh | grep -q 'exit 1'
grep -q 'dist.stage' scripts/uiai-lab-push
grep -q 'manifest checksum mismatch' scripts/uiai-lab-push
grep -q 'dist.rollback' scripts/uiai-lab-push
grep -q 'sudo -n /usr/local/sbin/uiai-lab-remote-control sync-activate' scripts/uiai-lab-push
grep -q 'wirebot ALL=(root) NOPASSWD: /usr/local/sbin/uiai-lab-remote-control' ops/sudoers/uiai-lab-remote-control
! grep -R -q 'gui.focusa.dev' scripts

echo 'veragensia lab lifecycle static test: PASS'
