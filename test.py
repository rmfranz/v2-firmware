import tornado
import json
from tornado import httpclient
from tornado.ioloop import PeriodicCallback


state = "ready"
waits = 1
send_print = False

def on_chunk(chunk):
    with open("cosa.gcode", "ab") as f:
        f.write(chunk) 

def on_done(response):
    print("No moriiiiiii")

def call():
    global state
    global waits
    global send_print
    token = 'o1aZp3lEnFBCfBwUpnSeQktig7jA9kyuZux9V2GJDuAFf2oq76PBkNF7BtGjl3jjVVgB5JdVeLBevBquVmftsAOmcEsHQvDQi9ObXv1wEw45kEPxO64TeSMj4b4jucrp'
    url= "https://cloud.3dprinteros.com/apiprinter/v1/kodak/printer/command"
    req = {
        "report": {
          "state": state,
          "percent": "0",
          "temps": ["24", "24", "24", "c24", "r24"],
          "target_temps": ["24", "24", "24"],
          "fan_speeds": ["0", "0"]
        },
        "auth_token": token
    }
    print(req)
    headers = {'Content-Type': 'application/json'}
    http_client = httpclient.HTTPClient()
    print("mando para el auth")
    resp_reg = http_client.fetch(url, method='POST', raise_error=False, headers=headers, body=json.dumps(req))
    resp_dict = json.loads(resp_reg.body.decode('utf-8'))
    print(resp_dict)
    if "command" in resp_dict and 'gcodes' in resp_dict["command"]:
        state = "downloading"
        waits = 0
        send_print = True
        print("me pongo a bajar el archivo")
        request = httpclient.HTTPRequest(url=resp_dict["payload"], streaming_callback=on_chunk, request_timeout=3600)
        async_http_client = httpclient.AsyncHTTPClient()
        async_http_client.fetch(request, on_done)
        print("paso de largo como colectivo lleno")        
    elif "command" in resp_dict and "pause" in resp_dict["command"]:
        state = "paused"
        waits = 0
        send_print = False
    elif "command" in resp_dict and "unpause" in resp_dict["command"]:
        state = "printing"
        send_print = True
    elif waits > 10 and send_print:
        state = "printing"
    waits = waits + 1
    

pc = PeriodicCallback(call, 2000)
pc.start()
tornado.ioloop.IOLoop.current().start()