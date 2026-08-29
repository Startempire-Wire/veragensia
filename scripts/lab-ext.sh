#!/bin/bash
# Launch the Focusa workforce extension browser and open its start page.
# Robust: mounts parent so /extroot/dist is always fresh; CDP discovers ID.
PDIR=/config/.config/chromium-uiai
EXT=/extroot/dist
# Bind to the current desktop session after container restart. su(1) alone
# does not recover the per-session DBus/XDG environment, causing Chromium to
# exit before CDP becomes available.
DESKTOP_PID=$(pgrep -u abc -x plasmashell | head -1)
if [ -z "$DESKTOP_PID" ]; then echo "plasmashell session unavailable" >&2; exit 1; fi
DBUS_SESSION_BUS_ADDRESS=$(su -s /bin/bash abc -c "tr '\0' '\n' </proc/$DESKTOP_PID/environ | sed -n 's/^DBUS_SESSION_BUS_ADDRESS=//p'")
export DBUS_SESSION_BUS_ADDRESS
export XDG_RUNTIME_DIR=/config/.XDG
[ -f "$EXT/manifest.json" ] || { echo "extension manifest missing: $EXT/manifest.json" >&2; exit 1; }
# wait for X display (best-effort)
for i in $(seq 1 40); do
  if su -s /bin/bash abc -c "DISPLAY=:1 xset q >/dev/null 2>&1"; then break; fi
  sleep 1
done
# apply Veragensia overlay branding (git-backed repo at /veragensia)
[ -f /veragensia/overlay/install.sh ] && bash /veragensia/overlay/install.sh >/tmp/overlay.log 2>&1 || true
# kill default autostarted chromium + any prior instance
pkill -f "chromium" 2>/dev/null
sleep 2
rm -f "$PDIR/SingletonLock" "$PDIR/SingletonCookie" "$PDIR/SingletonSocket" 2>/dev/null
su -s /bin/bash abc -c "DISPLAY=:1 nohup chromium --no-sandbox --user-data-dir=$PDIR --load-extension=$EXT --disable-extensions-except=$EXT --remote-debugging-port=9333 --remote-debugging-address=127.0.0.1 --no-first-run --no-default-browser-check --window-size=1280,760 --window-position=150,90 about:blank > /tmp/chrome.err 2>&1 &"
sleep 9
EXT_ID=$(curl -s http://127.0.0.1:9333/json 2>/dev/null | python3 -c 'import sys,json
try:
  for t in json.load(sys.stdin):
    if t.get("type")=="service_worker" and t.get("url","").startswith("chrome-extension://"):
      print(t["url"].split("/")[2]); break
except Exception: pass')
if [ -n "$EXT_ID" ]; then
  curl -s -X PUT "http://127.0.0.1:9333/json/new?chrome-extension://$EXT_ID/startpage.html" >/dev/null 2>&1 || \
    curl -s "http://127.0.0.1:9333/json/new?chrome-extension://$EXT_ID/startpage.html" >/dev/null 2>&1
  echo "$EXT_ID" > /tmp/uiai-ext-id
  echo "EXT_ID=$EXT_ID"
else
  echo "EXT_ID=NOTFOUND"
  tail -3 /tmp/chrome.err 2>/dev/null
  exit 1
fi
