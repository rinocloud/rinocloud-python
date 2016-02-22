import requests
import json

def api():
    return 'http://staging.rinocloud.com/api/1/'

def authenticate(*args):
    if len(args)>1:
        raise Exception('authenticate takes only 0 or 1 input arguments.') 
    # Save API token if given
    global rinocloud_auth_token
    if len(args) == 1:
        if isinstance(args[0], str):
            rinocloud_auth_token = args[0]
        else:
            raise Exception('Your API token should be entered as a string.') 
    # Return API token if not given an input argument        
    try:
        return 'Token ' + rinocloud_auth_token
    except:
        raise Exception('Set your API token using the authenticate function.') 

def upload(fname, metadata = {}, newname = None, tags = [], parent = None):
    # Check inputs
    if type(fname) is not str:
        raise Exception('The file name should be entered as a string.') 
    if type(metadata) is not dict:
        raise Exception('Metadata should be entered as a dictionary.') 
    if type(tags) is not list:
        raise Exception('Tags should be entered as a list, even for single tags.') 

    # Update metadata if optional arguments are specified
    if len(tags) > 0:
        metadata['tags'] = tags
    if newname is not None:
        if type(newname) is not str:
            raise Exception('The new name should be entered as a string.')
        metadata['name'] = newname
    if parent is not None:
        if type(parent) is not int:
            raise Exception('The parent should be given as an integer.')
        metadata['parent'] = parent

    # Set HTTP request headers
    headers = {
    'Authorization': authenticate(),
    'X-Requested-With': 'XMLHttpRequest'
    }

    # Open file and send request
    file = {'file': open(fname, 'rb')}
    r = requests.post(api() + 'files/upload_multipart/', files = file, data = {'json': json.dumps(metadata)}, headers = headers)
    return json.dumps(r.json(), indent=4)
