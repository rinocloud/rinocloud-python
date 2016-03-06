from six.moves.urllib.request import Request, urlopen
from six.moves.urllib.error import HTTPError
from six.moves.urllib.parse import urlencode #probably don't need these
import json
import requests

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

API_ROOT = 'http://staging.rinocloud.com/api/1/'
CONNECTION_TIMEOUT = 60


def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

def dictionary_clean_up(dictionary):
    new_dict = dictionary.copy()
    for key in ['created_on', 'created_on_str', 'filepath', 'metadata', 'owner', 'project', 'project_name', 'share_code', 'shared', 'size', 'size_str', 'type', 'updated_on', 'updated_on_str' ]:
        new_dict.pop(key, None)
    return new_dict

class RinoRequests(object):

    @classmethod
    def GET(cls, uri, **kw):
        return cls.execute(uri, 'GET', **kw)

    @classmethod
    def POST(cls, uri, **kw):
        return cls.execute(uri, 'POST', **kw)

    @classmethod
    def execute(cls, uri, http_verb, extra_headers=None, _file=None, _json=None, _data=None, _stream = False, **kw):
        url = API_ROOT + uri
        headers = {
        'Authorization': authenticate(),
        'X-Requested-With': 'XMLHttpRequest'
        }
        if http_verb == 'GET':
            r = requests.get(url, json=_json, headers=headers, stream = _stream)
        elif http_verb == 'POST':
            r = requests.post(url, json=_json, files=_file, data=_data, headers=headers)
        return r


class Object(RinoRequests):
    def __init__(self, metadata = {}, filepath='File path not specified.', parent = None, tags = None, id=None):
        self.filepath = filepath
        self.parent = parent
        self.tags = tags
        self.id = id
        self.__dict__.update(metadata)
   
    def add(self, params):
        self.__dict__.update(metadata)
    
    def upload(self):
        uri = 'files/upload_multipart/'
        file = {'file': open(self.filepath, 'rb')}
        response = self.__class__.POST(uri, _data = {'json': json.dumps(dictionary_clean_up(self.__dict__))}, _file = file)
        self.__dict__.update(json_loads_byteified(response._content))
        # instead of returning something - update dict.
        # include hidden object to check if upload has already been called and throw error if there is no filepath specified

    def get(self):
        uri = 'files/get_metadata/'
        response = self.__class__.POST(uri, _data = {'id': self.id})
        dictionary = json_loads_byteified(response._content)
        metadata_dictionary = dictionary.get('metadata')
        self.__dict__.update(dictionary)
        self.__dict__.update(metadata_dictionary)

    def update(self):
        uri = 'files/update_metadata/'
        response = self.__class__.POST(uri, _data = dictionary_clean_up(self.__dict__))
        dictionary = json_loads_byteified(response._content)
        metadata_dictionary = dictionary.get('metadata')
        self.__dict__.update(dictionary)
        self.__dict__.update(metadata_dictionary)
        
    def download(self, *filename):
        uri = 'files/download/?id=' + str(self.id)
        if filename:
            local_filename = filename
        elif self.name:
            local_filename = self.name
        else:
            self.get()
            local_filename = self.name
        response = self.__class__.GET(uri, _stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return local_filename
        


        # to add: 
        # update: updates metadata
        # download: downloads file 


