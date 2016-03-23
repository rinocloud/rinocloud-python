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
    def __init__(self, metadata = {}, file=None, parent = None, tags = None, id=None, **kwargs):
        self.file = file
        self.parent = parent
        self.tags = tags
        self.id = id
        self.metadata = metadata
        self.__dict__.update(metadata)
        self.metadata.update({'parent' : self.parent, 'tags' : self.tags, 'id' : self.id})
        self.__dict__.update(kwargs.pop('Obj_from_dict', ''))
        
    def metadata_dict_update(self):
        self.metadata.update({'parent' : self.parent, 'tags' : self.tags, 'id' : self.id})
   
    def add(self, params):
        self.metadata.update(params)
        self.__dict__.update(params)
    
    def upload(self):
        self.metadata_dict_update()
        uri = 'files/upload_multipart/'
        response = self.__class__.POST(uri, _data = {'json': json.dumps(self.metadata)}, _file = {'file': self.file})
        self.__dict__.update(json_loads_byteified(response._content))

    def get(self):
        uri = 'files/get_metadata/'
        response = self.__class__.POST(uri, _data = {'id': self.id})
        dictionary = json_loads_byteified(response._content)
        self.metadata = dictionary.get('metadata')
        self.__dict__.update(dictionary)
        self.__dict__.update(self.metadata)

    def update(self):
        self.metadata_dict_update()
        uri = 'files/update_metadata/'
        response = self.__class__.POST(uri, _data = self.metadata_dict)
        dictionary = json_loads_byteified(response._content)
        print dictionary
        print dictionary.get('metadata')
        self.metadata = dictionary.get('metadata')
        self.__dict__.update(dictionary)
        self.__dict__.update(self.metadata)
        
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
    
class Queryset(RinoRequests):

    def __init__(self, dictionary = {}, results = {'results' : 'The query method has not yet been called.'}):
        self.dictionary = dictionary
        self.results = results

    OPERATORS = [
        'lt', 'lte', 'gt', 'gte', 'ne', 'in', 'nin', 'exists', 'or' 
    ]

    @classmethod
    def extract_filter_operator(cls, parameter):
        for op in cls.OPERATORS:
            underscored = '__%s' % op
            if parameter.endswith(underscored):
                return parameter[:-len(underscored)], op
        return parameter, None

    def filter(self, **kw):
        #q = copy.deepcopy(self)
        for name, value in kw.items():
            attr, operator = Queryset.extract_filter_operator(name)
            if operator is None:
                self.dictionary[attr] = value
            elif operator is 'or':
                option_list = []
                for option in value:
                    option_list.append({attr : option})
                self.dictionary['$' + operator] = option_list
            else:
                if attr in self.dictionary:
                    self.dictionary[attr]['$'+ operator] = value
                else:
                    self.dictionary[attr] = {'$'+ operator : value}      
        return self

    def query(self):
         uri = 'files/query/'
         response = self.__class__.POST(uri, _json = {'query' : self.dictionary})        
         reply = json_loads_byteified(response._content)
         self.results = []
         for obj in reply['result']:
            self.results.append(Object(Obj_from_dict=obj)) 
         return self.results