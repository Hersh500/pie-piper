import requests

remote_url = 'https://nameless-cliffs-9474.herokuapp.com'
local_url = 'http://127.0.0.1:5000'

add_on = '/images/api/v1.0/' 

files = {'file':open('/Users/Hersh/Desktop/burger.jpg', 'rb')}
result = requests.post (remote_url+add_on, files=files)
print (result.text)
