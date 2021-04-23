from flask import Flask
from configparser import ConfigParser
from os import path
import mysql.connector

dir_path = path.dirname(path.realpath(__file__))
config = ConfigParser()
config.read(f'{dir_path}/flask_app.cfg')

def connect():
    return mysql.connector.connect(
        user = config['DB']['mysql_user'],
        password = config['DB']['mysql_pass'],
        host = config['DB']['mysql_host'],
        database = config['DB']['mysql_database'],
        auth_plugin = 'mysql_native_password')

app = Flask(__name__)

@app.route('/connect', methods=['GET'])
def mysql_connect():
    try:
        mysqldb = connect()
        return ("SUCCESS")
    except mysql.connector.Error as e:
        if(e.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR):
            print(str(e))
            return("AUTH ERROR!")
        elif(e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR):
            print(str(e))
            return("DB NOT EXIST!")
        else:
            print(str(e))
            return("UNKNOWN ERROR!")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080',debug=True)