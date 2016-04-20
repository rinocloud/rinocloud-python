
import rinocloud as rino

rino.set_domain('http://localhost:8000')
rino.api_key = "651ae65b9d5106e53106fbb7f525218b7b2e1456"

q = rino.Query()

print q.query()
