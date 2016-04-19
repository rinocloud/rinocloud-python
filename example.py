import numpy as np
import rinocloud as rino

rino.api_key = "e0687a68dd9568120e3db7e98f26f1c99ef54b81"
# rino.api_key = "651ae65b9d5106e53106fbb7f525218b7b2e1456"

# o = rino.Object()
# o.set_name("file.txt", path="data/", create_dir=True)
# o.p = 1

# o = rino.Object()
# o.set_name("file2.txt")
# o.p = 2
# o.upload_meta()

# write the data to the file
# x = np.linspace(0, 10, 11)
# y = np.random.random(size=11)
# np.savetxt(o.filepath, np.vstack((x, y)).T)
# o.upload()

o2 = rino.Object()
o2.set_local_path('data/', create_dir=True)
o2.get(id=346, overwrite=True, increment=False, path='data/', create_dir=True)

o2.save_local_metadata()
o2.download()

# for item in rino.Query().filter(p__gt=0).query():
#     print item.name
