from flask import Flask
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
        return("AUTH ERROR! CHECK YOUR LOG FILE FOR MORE INFO.")
    elif(e.errno == errorcode.ER_BAD_DB_ERROR):
        logging.error(str(e))
        return("DB NOT EXIST! CHECK YOUR LOG FILE FOR MORE INFO.")
    else:
        logging.error(str(e))
        return("UNKNOWN ERROR! CHECK YOUR LOG FILE FOR MORE INFO.")

@app.route('/connect', methods=['GET'])
def mysql_connect():
    try:
        mysqldb = connect()
        return("SUCCESS")
    except mysql.connector.Error as e:
        return(mysql_errors(e))

if __name__ == "__main__":
    app.run(host=config['API']['api_host'], 
            port=config['API']['api_port'],
            debug=config['API']['api_debug_mode'])