import requests
import json

def api():
    return 'http://staging.rinocloud.com/api/1/'

def authenticate(*args):
    if len(args)>1:
        raise Exception('authenticate takes only 0 or 1 input arguments.') 
  
    global rinocloud_auth_token
    if len(args) == 1:
        if isinstance(args[0], str):
            rinocloud_auth_token = args[0]
        else:
            raise Exception('Your API token should be entered as a string.') 
    try:
        return 'Token ' + rinocloud_auth_token
    except:
        raise Exception('Set your API token using the authenticate function.') 

def upload(fname, **kwargs):
    headers = {
    'Authorization': authenticate(),
    'X-Requested-With': 'XMLHttpRequest'
    }
    file = {'file': open(fname, 'rb')}
    r = requests.post(api() + 'files/upload_multipart/', files = file, headers = headers)
    return json.dumps(r.json(), indent=4)
