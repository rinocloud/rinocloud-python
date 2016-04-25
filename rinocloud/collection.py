
import os
import json
import rinocloud


class Collection(rinocloud.Object):

    def __init__(self, objs=None):
        super(self.__class__, self).__init__()
        self.objects = objs or []
        self.id = None

    def set_name(self, name, create_dir=False):
        """
        Sets the name of the file to be saved.

        @params
            name - the name to the file
            increment - whether or not to increment the filename if there is an existing file ie test.txt => test1.txt
            overwrite - whether or not to overwrite existing local file, renders increment redundant
        """

        # check if the file exists
        exists = os.path.exists(os.path.join(self._path, name))

        self.filepath = os.path.join(self._path, name)
        if exists is False and create_dir is True:
            os.makedirs(self.filepath)

        self.name = name
        return self.name

    def _prep_metadata(self):
        # copy the self.__dict__ and delete all that start with _
        obj = self.__dict__.copy()
        [obj.pop(item) for item in list(obj.keys()) if item.startswith('_')]
        obj.pop('objects')
        return obj

    def _process_response_metadata(self, response_metadata, **kw):
        super(Collection, self)._process_response_metadata(response_metadata, **kw)
        for o in self.objects:
            o._parent = self.id

    def add(self, obj):
        if isinstance(obj, list):
            for item in obj:
                item.set_local_path(self.filepath)
                item.set_name(item.name)
            self.objects.extend(obj)

        elif isinstance(obj, rinocloud.Object):
            obj.set_local_path(self.filepath)
            obj.set_name(obj.name)
            self.objects.extend([obj])

    def remove(self, obj):
        obj._path = rinocloud.path
        obj.set_name(obj.name)
        self.objects.remove(obj)

    def view(self):
        view_dict = self._prep_metadata()
        view_dict["objects"] = [o._prep_metadata() for o in self.objects]
        return json.dumps(view_dict, indent=4)

    def __iter__(self):
        return iter(self.objects)

    def next(self):
        if self.current > len(self.objects):
            raise StopIteration
        else:
            self.current += 1
            return self.objects[self.current - 1]

    def upload(self):
        meta = self._prep_metadata()
        meta["parent"] = self._parent
        r = rinocloud.http.create_folder(meta)

        assert r.status_code == 201, "Upload failed:\n%s" % r.text
        self._process_response_metadata(r.json())

        for obj in self.objects:
            obj.upload()
