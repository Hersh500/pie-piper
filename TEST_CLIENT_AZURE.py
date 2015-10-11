import requests
import base64
import json

remote_url = 'https://nameless-cliffs-9474.herokuapp.com'
local_url = 'http://127.0.0.1:5000'

url = local_url
post_add_on = '/images/api/v1.0/' 
get_status_add_on = '/images/api/v1.0/status'
get_dict_add_on = '/images/api/v1.0/getd'

o = open ('/Users/Hersh/Desktop/burger.jpg', 'rb')
#s = 'YAI3XrSWJAWs8wpD'
s = "zsHukJLJilFkKjsj"
#files = {'file':open('/Users/Hersh/Desktop/burger.jpg', 'rb')}
requests.post (url+post_add_on, data=s)

while (json.loads(requests.get(url+get_status_add_on, data=s).text)["0"] == "NO"):
	print (json.loads(requests.get(url+get_status_add_on, data=s).text)["0"])
result = requests.get(url+get_dict_add_on)
print (result.text)
