#!/usr/bin/env python

from flask import Flask, jsonify, render_template, request
from flask.ext.mysql import MySQL
import random

# config file 
import config

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

# api for rapberry pi
@app.route('/api/chair_log',methods=['POST'])
def chair_log():
	value = int(request.form['value'])
	query = 'insert into chair_log( action, inserted_at ) values( %d , NOW() )' % ( value )
	execute(query)
	return jsonify({"message":"ok","action":"stand_up"})

def execute(query):
	conn = mysql.connect()
	cursor = conn.cursor()
	res = cursor.execute(query)
	conn.commit()
	return res

# api to browser
@app.route('/api/is_music_play')
def is_music_play():
	res = execute('select * from (select * from chair_log order by inserted_at desc limit 12) as L where L.action = 0') ;	
	res = 0 if res > 0 else 1
	return jsonify({"music_play":res})

@app.route('/api/is_music_play/random')
def is_music_play_random():
	rand = random.randint(0,1)
	return jsonify({"music_play":rand})

    
if __name__ =='__main__':
	execute('create table if not exists chair_log(id int primary key auto_increment, action tinyint(1), inserted_at datetime)')
	app.run(host='0.0.0.0',debug=True,port=config.SERVER_PORT)




