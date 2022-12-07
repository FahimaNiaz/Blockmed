import datetime
import hashlib
import json
from flask import Flask, jsonify, render_template,request,redirect
import pymongo
from bson import json_util


client = pymongo.MongoClient("mongodb+srv://admin:blockchain@cluster0.a5ccxw5.mongodb.net/test")
db = client.get_database('patientdata')
records=db.blocks

def create_block(proof, previous_hash,data,collection):
	chain = collection.find()
	i=0
	for c in chain:
		i+=1
	block = {'index': i + 1,
				'timestamp': str(datetime.datetime.now()),
				'proof': proof,
				'diagnosis':data['diagnosis'],
				'prescribed_medicine':data['prescribed_medicine'],
				'symptoms':data['symptoms'],
				'message':data['message'],
				'previous_hash': previous_hash}
		
	records.insert_one(block)
	return block


def print_previous_block(collection):
		chain=[]
		r=collection.find()
		for record in r:
			chain.append(record)

		return chain[-1]

	
def proof_of_work(previous_proof):
		new_proof = 1
		check_proof = False
		
		while check_proof is False:
			hash_operation = hashlib.sha256(
				str(new_proof**2 - previous_proof**2).encode()).hexdigest()
			if hash_operation[:5] == '00000':
				check_proof = True
			else:
				new_proof += 1
				
		return new_proof

def hash(block):
		encoded_block = str(json.loads(json_util.dumps(block))).encode()
		return hashlib.sha256(encoded_block).hexdigest()

def chain_valid(chain):
		previous_block = chain[0]
		block_index = 1
		
		while block_index < len(chain):
			block = chain[block_index]
			if block['previous_hash'] !=hash(previous_block):
				return False
			
			previous_proof = previous_block['proof']
			proof = block['proof']
			hash_operation = hashlib.sha256(
				str(proof**2 - previous_proof**2).encode()).hexdigest()
			
			if hash_operation[:5] != '00000':
				return False
			previous_block = block
			block_index += 1
		
		return True

def create_collection(username):
	coll=db.createCollection(username)
	return coll

