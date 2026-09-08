#!/usr/bin/env bash
# Veragensia Omarchy public demo — Waybar Work presenter renderer.
# Reads the dated, curated public Work snapshot packaged with the Chrome
# extension (/extroot/dist/public-work.json). Public-safe: no Focusa daemon
# connection, no private state, no credentials.
set -euo pipefail

PUBLIC_SNAPSHOT=/extroot/dist/public-work.json
mode="${1:-work}"

if [[ ! -r "${PUBLIC_SNAPSHOT}" ]]; then
    echo "veragens  snapshot unavailable"
    exit 0
fi

read_field() {
    # Minimal JSON extraction without external deps.
    python3 - "$1" <<'PY'
import json, sys
data = json.load(open('/extroot/dist/public-work.json'))
def walk(obj, key):
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for v in obj.values():
            r = walk(v, key)
            if r is not None:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = walk(v, key)
            if r is not None:
                return r
    return None
val = walk(data, sys.argv[1])
print("" if val is None else val)
PY
}

published=$(read_field published_at || true)
agent=$(read_field agent || true)
work_count=$(read_field work_count || true)

case "${mode}" in
    work)
        echo "veragens  Work view  ${published:+— published ${published}}  ${work_count:+${work_count} items}"
        ;;
    published)
        echo "${published:+veragens public snapshot ${published}}  ${agent:+agent ${agent}}"
        ;;
    *)
        echo "veragens"
        ;;
esac
