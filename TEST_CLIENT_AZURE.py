import requests
import base64

remote_url = 'https://nameless-cliffs-9474.herokuapp.com'
local_url = 'http://127.0.0.1:5000'

add_on = '/images/api/v1.0/' 

o = open ('/Users/Hersh/Desktop/burger.jpg', 'rb')
s = 'YAI3XrSWJAWs8wpD'
#files = {'file':open('/Users/Hersh/Desktop/burger.jpg', 'rb')}
result = requests.post (local_url+add_on, data=s)
print (result.text)
