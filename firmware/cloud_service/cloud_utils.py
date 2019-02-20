import json
from tornado import httpclient

def get_auth(registration_code, mac_address, url, controller):
    headers = {'Content-Type': 'application/json'}
    body_with_registration = {"VID": "0KDK", "PID": "0001", "SNR": "00000000000000", "mac": mac_address, "type": "K_PORTRAIT", 
        "version": "", "registration_code_ttl": 20,  "registration_code": registration_code}
    http_client = httpclient.HTTPClient()
    print("mando para el auth")
    resp_reg = http_client.fetch(url, method='POST', raise_error=False, headers=headers, body=json.dumps(body_with_registration))
    resp_dict = json.loads(resp_reg.body.decode('utf-8'))
    if resp_reg.code == 200 and "auth_token" in resp_dict:
        #guardar en algun lado
        auth_token = resp_dict["auth_token"]
        print("tengo el token: {}",format(auth_token))
        controller.auth_token_caller.stop()
    else:
        print("no tengo un choto: {}".format(resp_dict))

def cloud_service_resp(response):
    # TODO: Capturar error
    print(response)