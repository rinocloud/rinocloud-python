import json
import os
import rinocloud


class Object():

    def __init__(self, **kw):
        """
        Initialise a bunch of variables
        """
        # these are some rinocloud variables we dont mind showing to the users
        self.id = None
        self.created_on = None
        self.updated_on = None
        self.name = None

        # these are some variables we will keep hidden, marked with underscore
        self._size = None
        self._parent = None

        # this needs to be set by the user in order to save locally
        # they just call self.set_local_path
        self._path = ''
        self.filepath = ''

        # lets set all the passed kwargs to this object
        for key, value in kw.iteritems():
            setattr(self, key, value)

    def increment_name(self, name, i):
        """
        takes something like
            test.txt
        and returns
            test1.txt
        """
        if i == 0:
            return name
        split = name.split('.')
        split[-2] = split[-2] + str(i)
        return '.'.join(split)

    def set_name(self, name, overwrite=False, increment=True, path=None, create_dir=False):
        """
        Sets the name of the file to be saved.

        @params
            name - the name to the file
            increment - whether or not to increment the filename if there is an existing file ie test.txt => test1.txt
            overwrite - whether or not to overwrite existing local file, renders increment redundant
            path - folder path to save the file too
            create_dir - whether to create the directory if it doesnt exist.
        """
        if path is not None:
            self.set_local_path(path, create_dir)

        # check if the file exists
        exists = os.path.exists(os.path.join(self._path, self.increment_name(name, 0)))

        # make sure that we dont overwrite if overwrite and increment are both false
        warning = "Filename and path already exists, refusing to set filename without overwrite=True or increment=True"
        assert not (exists and not overwrite and not increment), warning

        if overwrite is True:
            increment = False

        # otherwise overwrite the file
        if increment is False:
            self.filepath = os.path.join(self._path, self.increment_name(name, 0))
            self.name = self.increment_name(name, 0)
            return self.name

        # or increment the filename
        i = 0
        while os.path.exists(os.path.join(self._path, self.increment_name(name, i))):
            i += 1
        self.name = self.increment_name(name, i)
        self.filepath = os.path.join(self._path, self.increment_name(name, i))
        return self.name

    def _prep_metadata(self):
        # copy the self.__dict__ and delete all that start with _
        obj = self.__dict__.copy()
        [obj.pop(item) for item in obj.keys() if item.startswith('_')]
        obj.pop('filepath')
        return obj

    def save_json(self):
        """
            save all the exposed variables to a json file
        """
        # save to the set local path and add .json
        with open(self.filepath + '.json', 'w+') as outfile:
            json.dump(self._prep_metadata(), outfile, indent=4)

    def set_local_path(self, directory, create_dir=False):
        """
            sets path for local saving of information
            if create is true we will create the folder even if it doesnt exist
        """
        if not os.path.exists(directory) and create_dir is True:
            os.makedirs(directory)

        if os.path.isdir(directory):
            self._path = directory

    def upload(self):
        meta = self._prep_metadata()
        r = rinocloud.http.upload(self.filepath, meta)
        assert r.status_code == 201, "Upload failed:\n%s" % r.text
        self._process_returned_metadata(r.json())

    def _process_returned_metadata(self, response_metadata):
        self.__dict__.update(response_metadata["metadata"])

        self.id = response_metadata["id"]
        self.created_on = response_metadata["created_on"]
        self.updated_on = response_metadata["updated_on"]
        self.name = response_metadata["name"]

        # these are some variables we will keep hidden, marked with underscore
        self._size = response_metadata["size"]
        self._parent = response_metadata["parent"]
