#!/usr/bin/env python

from flask import Flask
import read_press

app= Flask(__name__)

@app.route('/')
def hello_world():
	return str(read_press.get_pressure())

@app.route('/api')
def api_hello():
	return '{"message":"thanks!"}'

@app.route('/api/stand')
def stand():
	return True

@app.route('/api/sit')
def sit():
	return True



if __name__ =='__main__':
	app.run(host='0.0.0.0',debug=True)




