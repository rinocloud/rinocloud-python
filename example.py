
import rinocloud as rino

rino.set_domain('http://localhost:8000')
rino.api_key = "651ae65b9d5106e53106fbb7f525218b7b2e1456"

# r = rino.Object()
# r.set_name("query_test")
# r.x = {'y': 2}
# r.upload_meta()

q = rino.Query()

q.filter(x=4)
q.print_filter()
print q.query()
