from flask import Flask
from configparser import ConfigParser
from os import path

dir_path = path.dirname(path.realpath(__file__))
config = ConfigParser()
config.read(f'{dir_path}/flask_app.cfg')

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080',debug=True)