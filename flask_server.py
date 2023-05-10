# -*- coding: utf-8 -*-
#Flask api
from flask import Flask, jsonify, redirect, render_template, request, url_for, send_from_directory
import os
from data_base import Database


name_db = 'tcpbd'
DB = Database(name_db)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.debug = True
MYDIR = os.path.dirname(__file__)

@app.route('/')   
def hello_world():
	return 'Hello World!'
 
@app.route('/main')  
def web_app():  
	return render_template('main.html') 

@app.route('/get_list_product')	
def get_list_product():	
	results = DB.get_list_product()
	print('get_list_product', results)
	for row in results:
		print(row)
	return jsonify(result=results)


if __name__ == "__main__": 
	app.run()