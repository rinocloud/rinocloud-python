
import rinocloud

rinocloud.api_key = "<your api key>"

# Saving objects
o = rinocloud.Object()
o.set_name("test")
o.x = 4

with open(o.filepath, 'w') as outfile:
    outfile.write('some information')

o.save_local_metadata()  # saves everything locally
o.upload()  # backs up to Rinocloud, allows querying

# Querying
print rinocloud.Query().filter(x__eq=4).query()
