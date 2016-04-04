# Using Rinocloud with python

Rinocloudpy is the python integration for Rinocloud. It let you save, upload and query all of your data and metadata. The integration is open source, so you are free to modify it to suit your needs.

## Installation
Need to sort this so people can just ```pip install rinocloudpy ```.

## Getting started
### Importing the library and authenication 
In any script or notebook that uses the rinocloudpy library you need to import the library in enter your API token:
```python
import rinocloudpy as rino
rino.authenticate('<Your API Token Here>')
```
## Rinocloudpy Objects
### Creating an object
The Rinocloudpy library works uses objects to store the metadata associated with a file. To create an object called 'obj', enter:
```python
obj = rino.Object()
```
### Associating a file with an object
You can associate file with an object by passing the object a file pointer on creation:
```
obj = rino.Object(file=open('<file name>', 'rb'))
```
or it can be added after the creation of the object:
```
obj.file = open('<file name>', 'rb')
```

### Adding metadata
The are several ways of adding metadata to an object. Metadata can be passed to an object using a dictionary on creation.
```
obj = rino.Object(metadata=<dictionary>)
```
Metadata can bee added or modified after creation by using the add method:
```
obj.add(<dictionary>)
```
Note that the dictionary keys should not contain spaces.

It is also possible to input metadata as keyword arguments on creation:
```
obj = rino.Object(key1=value1, key2=value2)
```
or to set the values after creation:
```
obj.key1 = value1
obj.key2 = value2
```

### Setting tags
Setting tags is similar to setting metadata. Tags can be set on creation:
```
obj = rino.Object(tags=['tag1', 'tag2', 'tag3'])
```
or after creation:
'''
obj.tags = ['tag1', 'tag2', 'tag3']
'''
Tags can also be appended to the list:
```
obj.tags.append('tag4')
```

### Setting a parent
To upload an object to a specific folder, you must set the 'parent' variable to be the object ID of the folder. Again, this can be done on creation:
```python
obj = rino.Object(parent=<parent object ID>)
```
or after creation:
```python
obj.parent = <parent object ID>
```
### Creating a subclass of object
If you want to create multiple objects with the same variables, e.g. if you want to create several objects with the same parent, you can create a subclass of Object. E.g.
```python
class subobj(rino.Object):
    def __init__(self):
        super(subobj, self).__init__()
        self.parent = 333
    pass
```
You can also create add tags and metadata to multiple objects using the batch operations (see below).

### Uploading
Once you have specified a file pointer, you can upload the file and associated metadata to Rinocloud. To do this you simply call the upload method:
```python
obj.upload()
```
This also updates the object metadata to include the data returned from Rinocloud, such as the creation time and object ID.
### Updating
Metadata can be added to an object after it has been uploaded. e.g.
```python
obj.upload()
obj.key4 = 'value4'
```
As long as the objects ID is specified, it is possible to update the metadata on the Rinocloud server using:
```python
obj.update()
```
### Getting metadata
To get an objects metadata from Rinocloud, you need to specify the object's ID:
```python
obj = rino.Object(id=<object id>)
```
You can then get the metadata from Rinocloud using:
```python
obj.get()
```
### Downloading a file
Provided that tho object ID is specified, you can download the file from Rinocloud. This is done using the download method:
```python
obj.download()
```
The downloaded file can be renamed by passing a new file name to the download method:
```python
obj.download('<new file name>')
```

#Local operation
Rinocloudpy objects can also save data and metadata locally. To save a file locally (provided that the file pointer has been specified), enter:
```python
obj.save_local()
```
Optionally, you can specify a new filename:
```python
obj.save_local('<new filename>')
```

Similarly, metadata can be saved locally (as a .json file) by entering:
```python
obj.save_json_local('<optional new filename>')
```

It is also possible to load metadata saved in a local file to an object using:
```python
obj.get_from_json_local(<'json filename'>)
```

# Querying
Rinocloudpy also contains tools for querying. You can query any and multiple metadata fields of all objects saved to Rinocloud.
## Creating a query object
To make a query, you must create a query object:
```python
qobj = rino.Query()
```
## Adding filters
Next, you can add filters to the query object. Rinocloudpy allows you to filter using the following operators:
```
'lt' - less than,
'lte' - less than or equal to, 
'gt' - greater than, 
'gte' - greater than or equal to, 
'ne' - not equal to, 
'in' - in array, 
'nin' - not in array, 
'exists' - whether the metadata field exists, 
'or' - allows multiple posibilities to be specified
```

Filters are specified by adding a double underscore followed by the operator to the metadata key. For example, to show only objects with 'key1' having a value greater than 21, you would enter:
```python
qobj.filter(key1__gt=21)
```
It is possible to add multiple filters, so to see only results where 'key2' is not a number in the array [1,2,3] and where a variable called 'key3' exists, as well as using the filter that has alread been applied, you would enter:
```python
qobj.filter(key2__nin=[1,2,3], key3__exists=True)
```

To use the 'or' filter, add '__or' to the end of the key. For example:
```python
qobj.filter(key1__or=6, key2__or=True)
```
Would return results where 'key1' was '6' or 'key2' was 'True'.

Entering ```qobj.return_filter()``` or ```qobj.print_filter()``` returns or prints the filters used, and it is possible to remove filters by entering:
```python
qobj.remove_filter('<key name>')
```
to remove the filter for one key or:
```python
qobj.remove_filter()
```
to remove all filters

## Making the query
Once the filters are specified, the query is made by entering:
```python
qobj.query()
```
more filters can be added and the query can be made again if needed.
Making a query returns a list of Rinocloudpy objects. The objects contain all the metadata associated with the file from Rinocloud and can be intereacted with individually or by using the batch operations.
# Batch operations
Batch operations are designed to streamline working with multiple objects. You can perform the download, upload, add, get and update methods on a list of objects using:
```python
rino.batch.download(<list of objects>)
rino.batch.upload(<list of objects>)
rino.batch.add(<list of objects>, <parameters as dictionary>)
rino.batch.get(<list of objects>)
rino.batch.update(<list of objects>)
```

Batch operationas are also useful for generating lots of objects from files.
```python
rino.batch.objects_from_filename_list(<list of filenames>)
```
will return a list of objects with file pointers for each file. It will also include metadata if it has been saved locally.

Similarly entering:
```python
rino.batch.objects_from_folder(<folder path>)
```
will return an object for file in the folder. You can optionally specify that only a certain type of file is included, for example, to include only txt files, you would enter:
```python
rino.batch.objects_from_folder(<folder path>, file_type='.txt')
```





