#Hersh Sanghvi

from flask import Flask, request #Imports necessary flask libs
from clarifai.client import ClarifaiApi #Imports the clarifai api
from azure.storage.blob import BlobService
import requests
import json
import base64
import os

app = Flask(__name__) #don't worry about this part

@app.route('/') #This part essentially marks that the following function is what Flask should do when the client wants to go to "/"
def index():
	return "Hello, World! This is the server for our calhacks team's project"

#d = {}
@app.route('/images/api/v1.0/', methods=['POST']) #Same thing as above, except this is what Flask should do when a POST request is made to this URL
def get_tags():
	#TODO: Error checking
#	global d 
#	d = {}
	return json.dumps({'0':'OK'})

	clarifai_api = ClarifaiApi()
	blob_service = BlobService('calhacks', 'mm7EmY+T+MGahePBDSDU5LHpZR5tRXuh4MSco4jFrzHovOPEf06e18c89pxtPIo4NDVhhjSeaQY/FQmKNxjjyA==')	

	blob_name = request.form['blob_id']
	blob_name = blob_name.decode('utf-8')
	blob_service.get_blob_to_path('imagestore', blob_name, 'out.png')	
	print("checkpoint 1")
	i = open ('out.png', 'r')
	strd = ""
	for line in i:
		strd += line.strip()
	fname = 'img.png'
	with open (fname, 'wb') as f:
		f.write (base64.b64decode(strd))
		f.close()

	f = open (fname, 'rb')
	result = clarifai_api.tag_images(f)
	print(result)
	st = result['results'][0]['result']['tag']['classes'][0:6]

	for i in ['food', 'nobody', 'still life', 'meal', 'dish', 'plate', 'delicious', 'isolated', 'cutout', 'unhealthy', 'one', 'background']: 
		while i in st:
			st.remove(i)
	return json.dumps(search_terms(st))

#	return "success!"
'''
@app.route('/images/api/v1.0/status', methods=['GET'])
def get_status():
	blob_name = request.data.decode('utf-8')
	if blob_name in d.keys():
		return json.dumps({"0":"OK"})		
	else:
		return json.dumps({"0":"NO"})

@app.route('/images/api/v1.0/getd', methods=['GET'])
def get_dict():
	return json.dumps(d)
'''
def search_terms(term_list):

	search_terms = {'key': 'bd8bd23310a5b8837ade81d9dc094a6b', 'q': str(term_list)}
	r = requests.get('http://food2fork.com/api/search', params= search_terms)
	i = 0
	recipe = []
	while i < 3 and i < len(r.json()['recipes']):
		current_rid = r.json()['recipes'][i]['recipe_id']
		recipe.append(current_rid)
		i += 1
	return get_recipes(recipe)

def get_recipes(lst):
	ingredients = {}
	for i in range(0,len(lst)):
		search_params = {'key': 'bd8bd23310a5b8837ade81d9dc094a6b', 'rId': lst[i]}
		test = requests.get('http://food2fork.com/api/get', params= search_params)
		ingredients[i] = (test.json()['recipe']['ingredients'][0:])
	return json.dumps(ingredients)

if __name__ == "__main__":
	app.run(debug=True)

