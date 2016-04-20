# Rinocloud python

Rinocloud python is an easy way to organise scientific datasets in python.
The library is open source (MIT License), so you are free to modify it to suit your needs.

Typically when doing simulations/experiments/modelling you have a bunch of parameters, which we call metadata, and an actual dataset, which is big list of numbers. This library aims to make taking care of the metadata and dataset easy.

- [Installation](#installation)
- [Examples](#examples)
- [Documentation](#documentation)
- [Development](#development)

## Installation

```pip install rinocloud ```

## Getting started

### Importing the library and authentication

```python
import rinocloud as rino

rino.api_key = '<Your API Token Here>'
```

## Examples

### Saving data and parameters from numpy

With numpy

```python
import numpy as np

import rinocloud as rino

rino.api_key = "<your api key>"
rino.set_local_path('data/', create_dir=True)

r = rino.Object()
r.set_name("file.txt")

r.slope = 2
r.constant = 3

# we will write x and y to a file and upload it, so we dont want it being uploaded as metadata
# so we mark it with an underscore
r._x = np.linspace(0, 10, 11)
r._y = r._x * r.slope + r.constant

np.savetxt(r.filepath, np.vstack((r._x, r._y)).T)

r.save_local_metadata()
r.upload()
```

### Saving data from pure python (no numpy)

Pure python, without numpy

```python
import rinocloud as rino

rino.api_key = "<your api key>"
rino.set_local_path('data/', create_dir=True)

r = rino.Object()
r.set_name("file.txt")

r.slope = 2
r.constant = 3

r._x = range(10)
# y = slope * x + constant
r._y = [i * r.slope + r.constant for i in r._x]

with open(r.filepath, 'w') as outfile:
    for (i, j) in zip(r._x, r._y):
        outfile.write("%1.2lf, %1.2lf\n" % (i, j))

r.save_local_metadata()
r.upload()
```

### Querying Rinocloud

```python
q = rinocloud.Query()

# searches data where x is "A22" and y is greater than 2.2
q.filter(x="A22", y__gt=2.2)
list_of_objects = q.query()
```

There are a lot of query types have a look at the [documentation](#querying) for more

## Documentation

### Creating an object

The Rinocloud library works uses objects to store the metadata associated with a file. To create an object called 'obj', enter:

```python
obj = rinocloud.Object()
```

### Associating a file with an object

You can set the path that rinocloud will look in, and save files too with

```python
rinocloud.set_local_path('data/'[, create_dir=False])
```

If `create_dir=True` then it will create the directory if it doesn't exist, `create_dir` defaults to False.

You can set the name of the object with

```python
obj.set_name("file.txt")

print obj.filepath
>>> file.txt

rinocloud.set_local_path('data/', create_dir=True)
obj.set_name("file.txt")
print obj.filepath
>>> data/file.txt
```

### Adding metadata

You can input metadata as keyword arguments on creation:

```python
obj = rino.Object(key1=value1, key2=value2)
```

or to set the values after creation:

```python
obj.key1 = value1
obj.key2 = value2
```

### Saving data and metadata locally

You can use the `obj.filepath` to save whatever you want locally, and `obj.save_local_metadata()` to save the metadata to a json file

```python
np.savetxt(obj.filepath, [1,2,3,4,5])
obj.save_local_metadata()
```

If we were saving into a folder called `data/` (set by using rinocloud.set_local_path('data/')) we would then have a folder structure of

```
data/
    file.txt # raw data
    file.txt.json # holds metadata
```

### Importing a locally saved objects

```
obj = rino.Object()
obj.set_name("file.txt", overwrite=True)
obj.import_local_metadata()
```

We need to pass `overwrite=True` since rinocloud will refuse to edit existing files otherwise.

### Setting a parent

To upload an object to a specific folder, you must set the 'parent' variable to be the object ID of the folder. So

```python
obj.parent = 10
```

Would save the object to a folder with id 10 inside Rinocloud, if you chose to upload the data to Rinocloud.

### Uploading

You can upload the file and associated metadata to Rinocloud, where you can later share it with your team, and discuss.
To do this you simply call the upload method:

```python
obj.upload()

>>> [====================       ] 456/500 -- 00:12:32
```

This also updates the object metadata to include the data returned from Rinocloud, such as the creation time and object ID.

### Updating

Metadata can be added to an object after it has been uploaded. e.g.

```python
obj.upload()
obj.new_key = 'value4'
obj.update()
```

It will be updated on Rinocloud.

### Downloading a file

Provided that tho object ID is specified, you can download the file from Rinocloud. This is done using the download method:
```python
obj.download()
```
The downloaded file can be renamed by passing a new file name to the download method:
```python
r = rino.Object(id=3397)
r.get()
r.download()

>>> [====================       ] 544/785 -- 00:32:45
```

It will download as whatever the filename is in Rinocloud, or it will increment the filename if a local file already exists.

## Querying

Rinocloud also contains tools for querying. You can query any and multiple metadata fields of all objects saved to Rinocloud.

## Creating a query object

To make a query, you must create a query object:
```python
qobj = rinocloud.Query()
```

## Making a query

trigger the query by adding filters and calling `.query()`
```python
list_of_objects = rinocloud.Query().filter(x=3).query()
```

## Adding filters

You can add filters to the query object. Rinocloud allows you to filter using the following operators:

```
'eq' - equal to,
'neq' - not equal to,
'lt' - less than,
'lte' - less than or equal to,
'gt' - greater than,
'gte' - greater than or equal to,
'ne' - not equal to,
'in' - in array,
'nin' - not in array,
'exists' - whether the metadata field exists,
'string_contains' - checks if the name or notes field contains a certain substring.
'or' - allows multiple possibilities to be specified
```

Filters are specified by adding a double underscore followed by the operator to the metadata key. For example, to show only objects with 'key1' having a value greater than 21, you would enter:

```python
rinocloud.Query().filter(key1__gt=21)
```

It is possible to add multiple filters, so to see only results where 'key2' is not a number in the array [1,2,3] and where a variable called 'key3' exists, as well as using the filter that has already been applied, you would enter:

```python
rinocloud.Query().filter(key2__nin=[1,2,3], key3__exists=True)
```

To use the 'or' filter, add '\__or' to the end of the key. For example:

```python
rinocloud.Query().filter(key1__or=6, key2__or=True)
```

Would return results where 'key1' was '6' or 'key2' was 'True'.

You can also access sub-objects. Suppose the metadata of some file looked like this:

```
{
  "x": {
    "y": 3
  }
}
```

you could search for this by using

```python
rinocloud.Query().filter(x__y__eq=3)
```

## Making the query

Once the filters are specified, the query is made by entering:

```python
rinocloud.Query().query()
```

more filters can be added and the query can be made again if needed.

Making a query returns a list of Rinocloud objects.

# Batch operations
Batch operations are designed to streamline working with multiple objects. You can perform the download, upload, add, get and update methods on a list of objects using:

```python
rino.batch.download(<list of objects>)
rino.batch.upload(<list of objects>)
rino.batch.get(<list of objects>)
rino.batch.update(<list of objects>)
```

## Development

Clone the repo and type:

`python setup.py develop`

This will install the package into a directory for development.
