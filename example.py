import rinocloud as rino

rino.api_key = "e0687a68dd9568120e3db7e98f26f1c99ef54b81"
rino.set_local_path('data/')

r = rino.Object()
r.set_name("file.txt")

r.slope = 2
r.constant = 3

# variables beginning with underscores are not saved, making it handy to attach all related
# data to the one object.
r._x = range(10)
# y = slope * x + constant
r._y = [i * r.slope + r.constant for i in r._x]

with open(r.filepath, 'w') as outfile:
    for (i, j) in zip(r._x, r._y):
        outfile.write("%1.2lf, %1.2lf\n" % (i, j))

r.save_local_metadata()
r.upload()
