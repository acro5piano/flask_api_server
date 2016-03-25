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
	cursor.execute(query)
	conn.commit()
	return cursor

# api to browser
@app.route('/api/is_music_play')
def is_music_play():
	# total of recent 12 of stand
	recent_stand_time = execute('select count(*) from (select * from chair_log order by inserted_at desc limit 12) as L where L.action = 0').fetchone()[0] ;	
	# if you stand up at least once , return 0
	res = 0 if recent_stand_time > 0 else 1
	return jsonify({"music_play":res})

@app.route('/api/continous_sit_time')
def continous_sit_time():
	row = execute('select count(*) from chair_log as C , (select MAX(inserted_at) as M from chair_log where action = 0) as MAX where MAX.M < C.inserted_at;') ;	
	res = row.fetchone()[0] * 5

	return jsonify({"continuous_sit_time":res})

@app.route('/api/daytotal_sit_time')
def daytotal_sit_time():
	row = execute('select count(*) from chair_log where action = 1 and DATE_SUB(now(),INTERVAL 1 DAY) < inserted_at;') ;	
	res = row.fetchone()[0] * 5
	return jsonify({"daytotal_sit_time":res})

    
if __name__ =='__main__':
	execute('create table if not exists chair_log(id int primary key auto_increment, action tinyint(1), inserted_at datetime)')
	app.run(host='127.0.0.1',debug=True,port=config.SERVER_PORT)
	#app.run(host='0.0.0.0',debug=True,port=config.SERVER_PORT)




