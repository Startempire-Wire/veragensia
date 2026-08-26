import json,sys,base64,time,urllib.request
import websocket
targets=json.load(urllib.request.urlopen("http://127.0.0.1:9333/json",timeout=5))
sp=[t for t in targets if t.get("type")=="page" and "startpage.html" in t.get("url","")]
if not sp: sys.exit("NO_STARTPAGE")
ws_url=sp[0]["webSocketDebuggerUrl"]
print("WS_URL",ws_url,file=sys.stderr)
ws=websocket.create_connection(ws_url,timeout=10,suppress_origin=True)
_id=[0]
def cmd(method,params=None):
    _id[0]+=1
    ws.send(json.dumps({"id":_id[0],"method":method,"params":params or {}}))
    while True:
        m=json.loads(ws.recv())
        if m.get("id")==_id[0]: return m
cmd("Page.enable")
time.sleep(1.2)
t=cmd("Runtime.evaluate",{"expression":"document.title+' | '+document.body.innerText.length","returnByValue":True})
print("PAGE_STATE",t.get("result",{}).get("result",{}).get("value","?"))
r=cmd("Page.captureScreenshot",{"format":"png"})
data=r.get("result",{}).get("data","")
open("/tmp/ext-shot.png","wb").write(base64.b64decode(data))
print("SHOT_BYTES",len(data))
ws.close()
