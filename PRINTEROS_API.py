from tornado import httpclient
import json

body = {"VID": "0KDK", "PID": "0001", "SNR": "00000000000000", "mac": "b8:27:eb:86:58:b2", "type": "K_PORTRAIT", "version": "", "registration_code_ttl": 20}

staging:
url = "https://acorn.3dprinteros.com/apiprinter/v1/kodak/printer/register"

posta:
url = "https://cloud.3dprinteros.com/apiprinter/v1/kodak/printer/register"

headers = {'Content-Type': 'application/json'}

resp = http_client.fetch(url, method='POST', raise_error=False, headers=headers, body=json.dumps(body))
if resp.code == 200:
    resp_dict = json.loads(resp.body.decode('utf-8'))
    registration_code = resp_dict["registration_code"]
    
#Una vez que el usuario ingreso el registration_code que debería mostrar en pantalla, enviar:
body_with_registration = {"VID": "0KDK", "PID": "0001", "SNR": "00000000000000", "mac": "b8:27:eb:86:58:b2", "type": "K_PORTRAIT", 
        "version": "", "registration_code_ttl": 20, 
        "registration_code": registration_code}
        
resp_reg = http_client.fetch(url, method='POST', raise_error=False, headers=headers, body=json.dumps(body_with_registration))

if resp_reg.code == 200:
    resp_dict = json.loads(resp_reg.body.decode('utf-8'))
    auth_token = resp_dict["auth_token"]
#b'{"auth_token":"CQ4595JnAgiDcSSdWrqlFLKyXAFCTT3t1CAJxZM2YrZfvjG5ZWauAS35drqPqNJnriDV6sBN4V2BApGbYNoPyTxxWeOaksGOkdlgWKCVIi93XfBSBMe061AFToU4djHm","email":"cloud@smart3d.tech"}'