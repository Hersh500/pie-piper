import requests

url = 'http://127.0.0.1:5000'
add_on = '/images/api/v1.0/' 

files = {'file':open('/Users/Hersh/Desktop/burger.jpg', 'rb')}
result = requests.post (url+add_on, files=files)
print (result.text)
