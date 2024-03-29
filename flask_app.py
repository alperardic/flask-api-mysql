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
        return ({"Success" : "False", "ERROR" : "AUTH ERROR! CHECK YOUR LOG FILE FOR MORE INFO!"})
    elif(e.errno == errorcode.ER_BAD_DB_ERROR):
        logging.error(str(e))
        return ({"Success" : "False", "ERROR" : "DB DOES NOT EXIST! CHECK YOUR LOG FILE FOR MORE INFO!"})
    elif(e.errno == errorcode.ER_BAD_TABLE_ERROR):
        logging.error(str(e))
        return ({"Success" : "False", "ERROR" : "TABLE DOES NOT EXIST! CHECK YOUR LOG FILE FOR MORE INFO!"})
    else:
        logging.error(str(e))
        return ({"Success" : "False", "ERROR" : "UNKNOWN ERROR! CHECK YOUR LOG FILE FOR MORE INFO."})

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
    id = request.args.get("id")
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    email = request.args.get("email")
    try:
        mysqldb = mysql_connect()
        cursor = mysqldb.cursor(buffered=True)
        
        #table_name girilmezse
        if (table_name == None):
            return make_response(jsonify(Success = False , Error = "Tablo ismi girilmedi!"), 403)
        #Butun tablo icin
        elif (table_name != None and id == None and firstname == None and lastname == None and email == None):
            query = f""" SELECT * FROM
            {config['DB']['mysql_database']}.{table_name} """
        #Sadece id verilirse
        elif (table_name != None and id != None and firstname == None and lastname == None and email == None):
            query = f""" SELECT * FROM
            {config['DB']['mysql_database']}.{table_name} 
            WHERE id = '{id}'"""
        #Sadece firstname verilirse
        elif (table_name != None and id == None and firstname != None and lastname == None and email == None):
            query = f""" SELECT * FROM
            {config['DB']['mysql_database']}.{table_name} 
            WHERE firstname = '{firstname}'"""
        #Sadece lastname verilirse
        elif (table_name != None and id == None and firstname == None and lastname != None and email == None):
            query = f""" SELECT * FROM
            {config['DB']['mysql_database']}.{table_name} 
            WHERE lastname = '{lastname}'"""
        #Sadece email verilirse
        elif (table_name != None and id == None and firstname == None and lastname == None and email != None):
            query = f""" SELECT * FROM
            {config['DB']['mysql_database']}.{table_name} 
            WHERE email = '{email}'"""
        #firstname ve lastname verilirse
        elif (table_name != None and id == None and firstname != None and lastname != None and email == None):
            query = f""" SELECT * FROM
            {config['DB']['mysql_database']}.{table_name} 
            WHERE firstname = '{firstname}' AND lastname = '{lastname}'"""
        #firstname ve email verilirse
        elif (table_name != None and id == None and firstname != None and lastname == None and email != None):
            query = f""" SELECT * FROM
            {config['DB']['mysql_database']}.{table_name} 
            WHERE firstname = '{firstname}' AND email = '{email}'"""
        #firstname, lastname ve email verilirse
        elif (table_name != None and id == None and firstname != None and lastname != None and email != None):
            query = f""" SELECT * FROM
            {config['DB']['mysql_database']}.{table_name} 
            WHERE firstname = '{firstname}' AND lastname='{lastname}' AND email = '{email}'"""
        else:
            return make_response(jsonify(Success = False, Error = "İstenilen sorgu yapılamaz!"), 403)
        
        cursor.execute(query)
        row_headers=[x[0] for x in cursor.description]
        response = cursor.fetchall()
        json_data=[]
        for result in response:
            json_data.append(dict(zip(row_headers, result)))
        mysqldb.close()
        if json_data == []:
            return make_response(jsonify(Success=False, Error="Aradığınız veri bulunamadı!"), 404)
        else:
            return make_response(jsonify(json_data), 200)
    except mysql.connector.Error as e:
        return make_response(jsonify(mysql_errors(e)), 404)

@app.route('/insert', methods = ['POST', 'PUT'])
def insert():
    req_methods = request.method

    if req_methods == 'POST': 
        table_name = request.args.get("table_name")
        firstname = request.args.get("firstname")
        lastname = request.args.get("lastname")
        email = request.args.get("email")
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
            return make_response(jsonify(mysql_errors(e)), 404)
    elif req_methods == 'PUT': #json formatında al.
        js_object = request.get_json()
        table_name = js_object["table_name"]
        firstname = js_object["firstname"]
        lastname = js_object["lastname"]
        email = js_object["email"]
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
            return make_response(jsonify(mysql_errors(e)), 404)
    else:
        return make_response(jsonify(ERROR=f"{req_methods} METHOD IS NOT ALLOWED!"), 405)

@app.route('/delete', methods = ['DELETE'])
def delete():
    table_name = request.args.get('table_name')
    id = request.args.get('id')
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    email = request.args.get('email')
    try:
        mysqldb = mysql_connect()
        cursor = mysqldb.cursor(buffered=True)
        
        # table_name verilmezse
        if (table_name == None):
            return make_response(jsonify(Success = False, Error = "Geçerli tablo ismi girilmedi."), 404)
        # Sadece id ile silme islemi
        elif (id != None and table_name != None and firstname == None and lastname == None and email == None):
            query = f"""DELETE FROM {config['DB']['mysql_database']}.{table_name}
            WHERE id='{id}' """
    
        # Sadece firstname ile silme islemi
        elif (id == None and table_name != None and firstname != None and lastname == None and email == None):
            query = f"""DELETE FROM {config['DB']['mysql_database']}.{table_name}
            WHERE firstname='{firstname}' """
    
        # Sadece lastname ile silme islemi
        elif (id == None and table_name != None and firstname == None and lastname != None and email == None):
            query = f"""DELETE FROM {config['DB']['mysql_database']}.{table_name}
            WHERE lastname='{lastname}' """
    
        # Sadece email ile silme islemi
        elif (id == None and table_name != None and firstname == None and lastname == None and email != None):
            query = f"""DELETE FROM {config['DB']['mysql_database']}.{table_name}
            WHERE email='{email}' """
    
        # firstname ve lastname ile silme islemi
        elif (id == None and table_name != None and firstname != None and lastname != None and email == None):
            query = f"""DELETE FROM {config['DB']['mysql_database']}.{table_name}
            WHERE firstname='{firstname}' AND lastname={lastname} """
    
        # firstname ve email ile silme islemi
        elif (id == None and table_name != None and firstname != None and lastname == None and email != None):
            query = f"""DELETE FROM {config['DB']['mysql_database']}.{table_name}
            WHERE firstname='{firstname}' AND email={email} """

        # lastname ve email ile silme islemi
        elif (id == None and table_name != None and firstname == None and lastname != None and email != None):
            query = f"""DELETE FROM {config['DB']['mysql_database']}.{table_name}
            WHERE lastname='{lastname}' AND email={email} """
        # 
        else:
            return make_response(jsonify(Success = False, Error = "İstenilen silme işlemi yapılamaz!"), 403)
        
        cursor.execute(query)
        mysqldb.commit()
        mysqldb.close()
        return make_response(jsonify(Succces = True, Status = "Delete işlemi başarı ile tamamlandı."), 200)
    except mysql.connector.Error as e:
        return make_response(jsonify(mysql_errors(e)), 404)

@app.route('/update', methods = ['POST'])
def update():
    table_name = request.args.get("table_name")
    id = request.args.get("id")
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    email = request.args.get("email")
    try:
        mysqldb = mysql_connect()
        cursor = mysqldb.cursor(buffered=True)
        #table_name verilmezse
        if (table_name == None):
            return make_response(jsonify(Success = False, Error = "Tablo ismi girilmedi!"), 403)
        #sadece id ile firstname, lastname, email degistirme
        elif (table_name != None and id != None and firstname != None and lastname != None and email != None):
            query = f"""UPDATE {config['DB']['mysql_database']}.{table_name}
            SET firstname = '{firstname}', lastname = '{lastname}', email = '{email}'
            WHERE id = '{id}' """
        #sadece eposta ile firstname, lastname degistirme
        elif (table_name != None and id == None and firstname != None and lastname != None and email != None):
            query = f"""UPDATE {config['DB']['mysql_database']}.{table_name}
            SET firstname = '{firstname}', lastname = '{lastname}'
            WHERE email = '{email}' """
        else:
            return make_response(jsonify(Success = False, Error = "Geçersiz update işlemi!"), 403)
        cursor.execute(query)
        mysqldb.commit()
        mysqldb.close()
        return make_response(jsonify(Success = True, Status = "Update işlemi başarı ile tamamlandı."), 200)
    except mysql.connector.Error as e:
        return make_response(jsonify(mysql_errors(e)), 404)

if __name__ == "__main__":
    app.run(host=config['API']['api_host'], 
            port=config['API']['api_port'],
            debug=config['API']['api_debug_mode'])