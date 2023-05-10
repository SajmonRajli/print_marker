# -*- coding: utf-8 -*-
#Flask api
from flask import Flask, jsonify, redirect, render_template, request, url_for, send_from_directory
import os
from data_base import Database
from tcp import Printer


TCP = Printer()

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

# дополнительная функция для печати, надо бы в отдельный файл вынести, но пока здесь оставил
def print_code(gtin, marker):
	id_marker = marker[0]
	serial = marker[1]
	DATA = f"01{gtin}21{serial}"
	print(DATA)
	# проверяем готов ли принтер
	print('проверяем готов ли принтер')
	response = TCP.status_print()
	if response == 'Ready' or response == 'Printing':
		# ставим метку, что маркер печатается и отправляем на печать и ждем ответа, ответы не реализовал.
		DB.update_status_marker(id_marker, 'print')
		try:
			print('Отправили в печать, ждем ответ')
			response = TCP.print(DATA)
			# после ответа принтера об ошибке или успехе меняю статус у маркера
			if response == "done":
				status = "done"
			else:
				status = "error"
		except Exception as E:
			print(E)
			status = "error"
		finally:
			DB.update_status_marker(id_marker, status)


# печать
@app.route('/print', methods = ['POST'])
def printer():
	print(request)
	DATA = request.get_json(force=True)
	print(DATA)
	id_prod = DATA['id']
	# DB.get_wait_prod_marker(id_prod)
	product = DB.get_product(id_prod)['Response'][0]
	gtin = product[2]

	# в первую очередь печатаем коды с ошибкой
	error_markers = DB.get_error_prod_marker(id_prod)['Response']
	print('error_markers')
	for marker in error_markers:
		print(marker)
		print_code(gtin, marker)


	markers = DB.get_wait_prod_marker(id_prod)['Response']
	print('markers')
	for marker in markers:
		print(marker)
		print_code(gtin, marker)

	return jsonify(result={"response": f'print {DATA}'})


# остановка печати
@app.route('/stop_print', methods = ['POST'])
def stop_print():
	TCP.stop_print()
	return jsonify(result={"response": 'stop_print'})

# получение статуса
@app.route('/status_print', methods = ['POST'])
def status_print():
	r = TCP.status_print()
	return jsonify(result={"response": r})



if __name__ == "__main__": 
	app.run()