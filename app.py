import datetime
import hashlib
import json
from flask import Flask, jsonify, render_template,request,redirect
import pymongo
from bson import json_util
from utils import create_block, hash, print_previous_block,proof_of_work,chain_valid

client = pymongo.MongoClient("mongodb+srv://admin:blockchain@cluster0.a5ccxw5.mongodb.net/test")
db = client.get_database('patientdata')
records=db.blocks


app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def homepage():
	return redirect('/all')

@app.route('/login', methods=['GET','POST'])
def login():
	return render_template('login.html')

@app.route('/add', methods=['GET','POST'])
def mine_block():
	previous_block = print_previous_block(records)
	previous_proof = previous_block['proof']
	proof =proof_of_work(previous_proof)
	previous_hash =hash(previous_block)
	if request.method =='POST':
		diagnosis=request.form.get("diagnosis")
		prescribed_medicine=request.form.get("prescribed_medicine")
		symptoms=request.form.get("symptoms")
		message=request.form.get("message")
		data={'diagnosis':diagnosis,
				'prescribed_medicine':prescribed_medicine,
				'symptoms':symptoms,
				'message':message}
		block = create_block(proof, previous_hash,data, records)
		return redirect("/all")
	return render_template('adddata.html')



@app.route('/all', methods=['GET','POST'])
def display_chain():
	chain=[]
	r=db.blocks.find()
	for record in r:
			chain.append(record['diagnosis'])
	response = chain
	return render_template('home.html', message=response)


@app.route('/valid', methods=['GET'])
def valid():
	chain=[]
	r=db.blocks.find()
	for record in r:
			chain.append(record)
	valid = chain_valid(chain)
	
	if valid:
		response = {'message': 'The Blockchain is valid.'}
	else:
		response = {'message': 'The Blockchain is not valid.'}
	return render_template('home.html', message=response)



app.run(host='127.0.0.1', port=5000)
