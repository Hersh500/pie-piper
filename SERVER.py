#Hersh Sanghvi
#ALSO TODO: CHECK HOW TO SET ENV VARIABLES 

from flask import Flask, request #Imports necessary flask libs
from clarifai.client import ClarifaiApi #Imports the clarifai api
import requests
import json
import base64

app = Flask(__name__) #don't worry about this part

@app.route('/') #This part essentially marks that the following function is what Flask should do when the client wants to go to "/"
def index():
	return "Hello, World! This is the server for our calhacks team's project"

@app.route('/images/api/v1.0/', methods=['POST']) #Same thing as above, except this is what Flask should do when a POST request is made to this URL
def get_tags():
	#TODO: Error checking
	common_terms = ['food', 'nobody', 'still life', 'meal', 'dish', 'plate', 'delicious', 'isolated', 'cutout', 'unhealthy', 'one', 'background'] 
	clarifai_api = ClarifaiApi()
	#img = request.files['file'] #assumes that this data is raw image data
	img = request.data
	i = open ('s.jpg', 'wb')
	i.write(base64.b64decode(img))
	i.close()
	img = open ('s.jpg', 'rb')

	result = clarifai_api.tag_images(img)
	#print (str(result))
	st = result['results'][0]['result']['tag']['classes'][0:6]
	for i in common_terms:
		while i in st:
			st.remove(i)

	return search_terms(st)

def search_terms(term_list):

	search_terms = {'key': 'bd8bd23310a5b8837ade81d9dc094a6b', 'q': str(term_list)}
	r = requests.get('http://food2fork.com/api/search', params= search_terms)
	i = 0
	recipe = []
	while i < 3 or i < len(r.json()['recipes']):
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

