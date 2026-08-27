#!/bin/bash
# Launch the Focusa workforce extension browser and open its start page.
# Robust: mounts parent so /extroot/dist is always fresh; CDP discovers ID.
PDIR=/config/.config/chromium-uiai
EXT=/extroot/dist
# wait for X display (best-effort)
for i in $(seq 1 40); do
  if su -s /bin/bash abc -c "DISPLAY=:1 xset q >/dev/null 2>&1"; then break; fi
  sleep 1
done
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
fi
