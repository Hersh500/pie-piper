#Hersh Sanghvi
#ALSO TODO: CHECK HOW TO SET ENV VARIABLES 

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

@app.route('/images/api/v1.0/', methods=['POST']) #Same thing as above, except this is what Flask should do when a POST request is made to this URL
def get_tags():
	#TODO: Error checking
	os.environ['CLARIFAI_APP_ID'] = '3QUAmRKkKsqo6RExP-oARAeezvTlOWqseo3LyCUe' #TODO: Make secret
	os.environ['CLARIFAI_APP_SECRET'] = 'S4eGqB-Ym1Qu3vmfZRpT9WKHfVIcHb8CQ7hrR_lj' #TODO: Make secret
	blob_service = BlobService('calhacks','mm7EmY+T+MGahePBDSDU5LHpZR5tRXuh4MSco4jFrzHovOPEf06e18c89pxtPIo4NDVhhjSeaQY/FQmKNxjjyA==') #TODO: hide this 
	clarifai_api = ClarifaiApi()

	blob_name = request.data
	blob_name = blob_name.decode('utf-8')
	#print(blob_service.list_blobs('imagestore', marker=None))
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
	return ingredients

if __name__ == "__main__":
	app.run(debug=True)

