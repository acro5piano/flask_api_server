#!/usr/bin/env python

from flask import Flask, jsonify, render_template, request
from flask.ext.mysql import MySQL

import config
import random

app = Flask(__name__)

# MySQL configurations
mysql = MySQL()
app.config['MYSQL_DATABASE_USER']     = config.DB_USER
app.config['MYSQL_DATABASE_PASSWORD'] = config.DB_PASS
app.config['MYSQL_DATABASE_DB']       = config.DB_NAME
app.config['MYSQL_DATABASE_HOST']     = config.DB_HOST
mysql.init_app(app)

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/api')
def hello_api():
	result = { "message":"welcome to Flask Api Server!" }
	return jsonify(result)

@app.route('/api/chair_log',methods=['POST'])
def chair_log():
	value = int(request.form['value'])
	print(value)
	query = 'insert into chair_log( action, inserted_at ) values( %d , NOW() )' % ( value )
	execute(query)
	return jsonify({"message":"ok","action":"stand_up"})

def execute(query):
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(query)
	conn.commit()

@app.route('/api/is_music_play/random')
def is_music_play():
	rand = random.randint(0,1)
	return jsonify({"music_play":rand})

    
if __name__ =='__main__':
	execute('create table if not exists chair_log(id int primary key auto_increment, action tinyint(1), inserted_at datetime)')
	app.run(host='0.0.0.0',debug=True,port=config.SERVER_PORT)




