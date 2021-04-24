from flask import Flask, jsonify, make_response, request
from configparser import ConfigParser
from os import path
from mysql.connector import errorcode
import mysql.connector
import logging

dir_path = path.dirname(path.realpath(__file__))
config = ConfigParser()
config.read(f'{dir_path}/flask_app.cfg')
logging.basicConfig(filename = config['LOGGING']['log_file'], level = config['LOGGING']['log_level'])

app = Flask(__name__)

def connect():
    return mysql.connector.connect(
        user = config['DB']['mysql_user'],
        password = config['DB']['mysql_pass'],
        host = config['DB']['mysql_host'],
        database = config['DB']['mysql_database'],
        auth_plugin = 'mysql_native_password')

def mysql_errors(e):
    if(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
        logging.error(str(e))
        return make_response(jsonify(Success = False, ERROR = 'AUTH ERROR! CHECK YOUR LOG FILE FOR MORE INFO!'), 404)
    elif(e.errno == errorcode.ER_BAD_DB_ERROR):
        logging.error(str(e))
        return make_response(jsonify(Success = False, ERROR = 'DB DOES NOT EXIST! CHECK YOUR LOG FILE FOR MORE INFO!'), 404)
    elif(e.errno == errorcode.ER_BAD_TABLE_ERROR):
        logging.error(str(e))
        return make_response(jsonify(Success = False, ERROR = 'TABLE DOES NOT EXIST! CHECK YOUR LOG FILE FOR MORE INFO!'), 404)
    else:
        logging.error(str(e))
        return make_response(jsonify(Success = False, ERROR = "UNKNOWN ERROR! CHECK YOUR LOG FILE FOR MORE INFO."), 404)

def mysql_insert(table_name, firstname, lastname, email):
    try:
        mysqldb = connect()
        cursor = mysqldb.cursor(buffered=True)
        query = f""" INSERT INTO 
        {config['DB']['mysql_database']}.{table_name}
        ( firstname, lastname, email ) VALUES 
        ( '{firstname}', '{lastname}', '{email}') """
        cursor.execute(query)
        mysqldb.commit()
        mysqldb.close()
        return make_response(jsonify(Success=True, Status=f"NEW VALUES ADDED TO {table_name}"), 200)
    except mysql.connector.Error as e:
        return(mysql_errors(e))

@app.route('/connect', methods = ['GET'])
def mysql_connect():
    try:
        mysqldb = connect()
        mysqldb.close()
        return make_response(jsonify(Success = True), 200)
    except mysql.connector.Error as e:
        return(mysql_errors(e))

@app.route('/insert', methods = ['POST', 'PUT'])
def insert():
    req_methods = request.method

    if req_methods == 'POST': 
        table_name = request.args.get("table_name")
        firstname = request.args.get("firstname")
        lastname = request.args.get("lastname")
        email = request.args.get("email")
        return(mysql_insert(table_name,firstname,lastname,email))
    elif req_methods == 'PUT': #json formatında al.
        js_object = request.get_json()
        table_name = js_object["table_name"]
        firstname = js_object["firstname"]
        lastname = js_object["lastname"]
        email = js_object["email"]
        return(mysql_insert(table_name,firstname,lastname,email))
    else:
        return make_response(jsonify(ERROR=f"{req_methods} METHOD IS NOT ALLOWED!"), 405)

if __name__ == "__main__":
    app.run(host=config['API']['api_host'], 
            port=config['API']['api_port'],
            debug=config['API']['api_debug_mode'])