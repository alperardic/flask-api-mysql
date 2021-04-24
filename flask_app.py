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

def mysql_connect():
    return mysql.connector.connect(
        user = config['DB']['mysql_user'],
        password = config['DB']['mysql_pass'],
        host = config['DB']['mysql_host'],
        database = config['DB']['mysql_database'],
        auth_plugin = 'mysql_native_password')

def mysql_errors(e):
    if(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
        logging.error(str(e))
        return make_response(jsonify(Success = False, ERROR = 'AUTH ERROR! CHECK YOUR LOG FILE FOR MORE INFO!'), 401)
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
        mysqldb = mysql_connect()
        cursor = mysqldb.cursor(buffered=True)
        query = f""" INSERT INTO 
        {config['DB']['mysql_database']}.{table_name}
        ( firstname, lastname, email ) VALUES 
        ( '{firstname}', '{lastname}', '{email}') """
        cursor.execute(query)
        mysqldb.commit()
        mysqldb.close()
        return make_response(jsonify(Success=True, Status=f"NEW VALUES ADDED TO {table_name}"), 201)
    except mysql.connector.Error as e:
        return(mysql_errors(e))

def mysql_select(table_name, id_obj, firstname, lastname, email):
    # Sadece table_name verilirse.
    if (firstname == None and lastname == None and email == None and id_obj == None):
        try:
            mysqldb = mysql_connect()
            cursor = mysqldb.cursor(buffered=True)
            query = f""" SELECT * FROM
            {config['DB']['mysql_database']}.{table_name} """
            cursor.execute(query)
            row_headers=[x[0] for x in cursor.description]
            response = cursor.fetchall()
            json_data=[]
            for result in response:
                json_data.append(dict(zip(row_headers, result)))
            mysqldb.close()
            if json_data == []:
                return make_response(jsonify(Success=False, Status="Aradığınız veri bulunamadı!"), 204)
            else:
                return make_response(jsonify(json_data), 200)
        except mysql.connector.Error as e:
            return(mysql_errors(e))
    
    # table_name ve email verilirse.
    elif (firstname == None and lastname == None and id_obj == None):
        try:
            mysqldb = mysql_connect()
            cursor = mysqldb.cursor(buffered=True)
            query = f""" SELECT * FROM
            {config['DB']['mysql_database']}.{table_name} 
            WHERE email = '{email}'"""
            cursor.execute(query)
            row_headers=[x[0] for x in cursor.description]
            response = cursor.fetchall()
            json_data=[]
            for result in response:
                json_data.append(dict(zip(row_headers, result)))
            mysqldb.close()
            if json_data == []:
                return make_response(jsonify(Success=False, Status="Aradığınız veri bulunamadı!"), 204)
            else:
                return make_response(jsonify(json_data), 200)
        except mysql.connector.Error as e:
            return(mysql_errors(e))
    
    # table_name ve id verilirse
    elif (firstname == None and lastname == None and email == None):
        try:
            mysqldb = mysql_connect()
            cursor = mysqldb.cursor(buffered=True)
            query = f""" SELECT * FROM
            {config['DB']['mysql_database']}.{table_name} 
            WHERE id = '{id_obj}'"""
            cursor.execute(query)
            row_headers=[x[0] for x in cursor.description]
            response = cursor.fetchall()
            json_data=[]
            for result in response:
                json_data.append(dict(zip(row_headers, result)))
            mysqldb.close()
            if json_data == []:
                return make_response(jsonify(Success=False, Status="Aradığınız veri bulunamadı!"), 204)
            else:
                return make_response(jsonify(json_data), 200)
        except mysql.connector.Error as e:
            return(mysql_errors(e))
    
    # table_name ve firstname verilirse
    elif (lastname == None and email == None and id_obj == None):
        try:
            mysqldb = mysql_connect()
            cursor = mysqldb.cursor(buffered=True)
            query = f""" SELECT * FROM
            {config['DB']['mysql_database']}.{table_name} 
            WHERE firstname = '{firstname}'"""
            cursor.execute(query)
            row_headers=[x[0] for x in cursor.description]
            response = cursor.fetchall()
            json_data=[]
            for result in response:
                json_data.append(dict(zip(row_headers, result)))
            mysqldb.close()
            if json_data == []:
                return make_response(jsonify(Success=False, Status="Aradığınız veri bulunamadı!"), 204)
            else:
                return make_response(jsonify(json_data), 200)
        except mysql.connector.Error as e:
            return(mysql_errors(e))

    # table_name ve lastname verilirse
    elif (firstname == None and email == None and id_obj == None):
        try:
            mysqldb = mysql_connect()
            cursor = mysqldb.cursor(buffered=True)
            query = f""" SELECT * FROM
            {config['DB']['mysql_database']}.{table_name} 
            WHERE lastname = '{lastname}'"""
            cursor.execute(query)
            row_headers=[x[0] for x in cursor.description]
            response = cursor.fetchall()
            json_data=[]
            for result in response:
                json_data.append(dict(zip(row_headers, result)))
            mysqldb.close()
            if json_data == []:
                return make_response(jsonify(Success=False, Status="Aradığınız veri bulunamadı!"), 204)
            else:
                return make_response(jsonify(json_data), 200)
        except mysql.connector.Error as e:
            return(mysql_errors(e))
    
    # table_name, firstname ve lastname verilirse
    elif (email == None and id_obj == None):
        try:
            mysqldb = mysql_connect()
            cursor = mysqldb.cursor(buffered=True)
            query = f""" SELECT * FROM
            {config['DB']['mysql_database']}.{table_name} 
            WHERE firstname = '{firstname}' AND lastname = '{lastname}'"""
            cursor.execute(query)
            row_headers=[x[0] for x in cursor.description]
            response = cursor.fetchall()
            json_data=[]
            for result in response:
                json_data.append(dict(zip(row_headers, result)))
            mysqldb.close()
            if json_data == []:
                return make_response(jsonify(Success=False, Status="Aradığınız veri bulunamadı!"), 204)
            else:
                return make_response(jsonify(json_data), 200)
        except mysql.connector.Error as e:
            return(mysql_errors(e))
    else:
        return make_response(jsonify(Success=False, Status="Aradığınız veri bulunamadı."), 204)    
@app.route('/connect', methods = ['GET'])
def connect():
    try:
        mysqldb = mysql_connect()
        mysqldb.close()
        return make_response(jsonify(Success = True), 200)
    except mysql.connector.Error as e:
        return(mysql_errors(e))

@app.route('/select', methods = ['GET'])
def select():
    table_name = request.args.get("table_name")
    id_obj = request.args.get("id")
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    email = request.args.get("email")
    response = mysql_select(table_name, id_obj, firstname, lastname, email)
    return response

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