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
obj = Object(tags=['tag1', 'tag2', 'tag3'])
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
### Uploading
### Updating
### Getting metadata
### Downloading a file

#Querying
#Batch operations







