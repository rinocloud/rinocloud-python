
import numpy as np
import rinocloud as rino

rino.api_key = "e0687a68dd9568120e3db7e98f26f1c99ef54b81"
# rino.api_key = "651ae65b9d5106e53106fbb7f525218b7b2e1456"

o = rino.Object()
o.set_name("file.txt", overwrite=True, increment=False, path='data/', create_dir=True)

x = np.linspace(0, 10, 11)
y = np.random.random(size=11)

o.param1 = "some parameter"
o.param2 = 1.34324
o.nested_parameter = {
    "nested": True
}

np.savetxt(o.filepath, np.vstack((x, y)).T)
o.save_json()

import json
print json.dumps(o.__dict__, indent=4)

o.upload()

print json.dumps(o.__dict__, indent=4)
