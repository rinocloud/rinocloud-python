import json
import requests
import copy
import glob
import os

API_ROOT = 'http://staging.rinocloud.com/api/1/'
URI = {'upload' : 'files/upload_multipart/', 'get' : 'files/get_metadata/' ,'update' : 'files/update_metadata/',
           'download' : 'files/download/?id=', 'query' : 'files/query/'}

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

class batch():
    @staticmethod
    def download(obj_list):
        for obj in obj_list:
            obj.download()
    
    @staticmethod
    def upload(obj_list):
        for obj in obj_list:
            obj.upload()

    @staticmethod        
    def add(obj_list, params):
        for obj in obj_list:
            obj.add(params)

    @staticmethod       
    def get(obj_list):
        for obj in obj_list:
            obj.get()

    @staticmethod        
    def update(obj_list):
        for obj in obj_list:
            obj.update()
    
    @staticmethod
    def objects_from_filename_list(file_list, json_from_file=True):
        #test if it works for single files
        obj_list = []
        for filename in file_list:
            obj_list.append(Object(file=open(filename, "rb")))
        if json_from_file == True:
            for obj in obj_list:
                try:
                    obj.get_from_json_local(obj.file.name + '.json')
                except:
                    pass
        return obj_list
    
    @staticmethod
    def objects_from_folder(folder_path, file_type=None, json_from_file=True):
        if file_type == None:
            file_list = glob.glob(folder_path + '/*')
            for filename in file_list:
                if '.json' == os.path.splitext(filename)[1]:
                    aList.remove(filename);
        else:
            file_list = glob.glob(folder_path + '/*' + file_type)
        

        return objects_from_filename_list(file_list, json_from_file=json_from_file)
        
    #include if needed
    #@staticmethod
    #def objects_from_file_pointer_list(file_pointer_list):
    #    pass
        # move stuff from objects_from_filename_list here and point that function here.
    

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
    # set so that kwargs can be used to set variables.
    def __init__(self, metadata = {}, file=None, parent = None, tags = [], id=None, __recieved_metadata__ = {}, use_local_metadata=False,  **kwargs):
        self.file = file
        self.parent = parent
        self.tags = tags
        self.id = id
        self.metadata = metadata
        self.__recieved_metadata__ = __recieved_metadata__
        self.__dict__.update(metadata)
        self.__dict__.update(kwargs.pop('Obj_from_dict', ''))
        for name, value in kwargs.items():
            self.__dict__[name] = value
        if use_local_metadata==True:
            try:
                self.get_from_json_local(self.file.name + '.json')
            except:
                pass
        self.__dict__.pop('use_local_metadata', '')

    def add(self, params):
        self.metadata.update(params)
        self.__dict__.update(metadata)
    
    def upload(self):
        self._prep_metadata_for_sending()
        response = self.__class__.POST(URI['upload'], _data = {'json': json.dumps(self.metadata)}, _file = {'file': self.file})
        self._process_returned_metadata(response)
               
    def get(self):
        response = self.__class__.POST(URI['get'], _data = {'id': self.id})
        self._process_returned_metadata(response)

    def update(self):
        self._prep_metadata_for_sending()
        uri = 'files/update_metadata/'
        response = self.__class__.POST(URI['update'], _data = self.metadata)
        self._process_returned_metadata(response)
 
    def download(self, newname = None):
        local_filename = self._extract_name(newname)
        response = self.__class__.GET(URI['download'] + str(self.id), _stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return local_filename
    
    # Local saving and loading
    def save_local(self, newname = None):
        contents = self.file.read()
        localfile = open(self._extract_name(newname), "wb")
        localfile.write(contents)
        localfile.close()
        
    def save_json_local(self, newname = None):
        self._prep_metadata_for_sending()
        _local_saving_dict = copy.deepcopy(self.__dict__)
        _local_saving_dict.pop('file')
        jsonfile = open(self._extract_name(newname) + '.json', 'w')
        jsonfile.write(json.dumps(_local_saving_dict))
        jsonfile.close()
        
    def get_from_json_local(self, jsonfile):
        jf = open(jsonfile, 'r')
        jsondata=jf.read()
        self.__recieved_metadata__.update(json_loads_byteified(jsondata))
        self.__dict__.update(self.__recieved_metadata__)
        jf.close()
    
    # -----------------------------------------------------
    def _prep_metadata_for_sending(self):
        self.metadata.update(self.__dict__)
        self.metadata.pop('metadata')
        for key in self.__recieved_metadata__:
            try:
                self.metadata.pop(key)
            except:
                pass
        try:
            self.metadata.pop('file')
        except:
            pass
        try:
            self.metadata.pop('__recieved_metadata__')
        except:
            pass
        
    def _process_returned_metadata(self, response):
        self.__recieved_metadata__.update(json_loads_byteified(response._content))
        self.__dict__.update(self.__recieved_metadata__)
        
    def _extract_name(self, newname = None):
        try:
            if newname is not None:
                local_file_name = newname
            elif 'name' in vars():
                local_file_name = self.name
            else:
                local_file_name = self.file.name
            return local_file_name 
        except:
            self.get()
            return self.name

class Query(RinoRequests):

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
    
    def print_filter(self):
        print self.dictionary
        
    def return_filter(self):
        return self.dictionary
        
    def remove_filter(self, key=None):
        if key == None:
            self.dictionary = {}
        else:
            self.dictionary.pop(key)
    
    def query(self):
         response = self.__class__.POST(URI['query'], _json = {'query' : self.dictionary})        
         reply = json_loads_byteified(response._content)
         self.results = []
         for obj in reply['result']:
            self.results.append(Object(Obj_from_dict=obj)) 
         return self.results