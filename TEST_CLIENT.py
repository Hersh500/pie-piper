import requests

remote_url = 'https://immense-taiga-6433.herokuapp.com'
local_url = '0.0.0.0:5000'
add_on = '/images/api/v1.0/' 

files = {'file':open('/Users/Hersh/Desktop/burger.jpg', 'rb')}
result = requests.post (remote_url+add_on, files=files)
print (result.text)
