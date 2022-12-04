from flask import Flask
import os
from Models import db

def create_app():
    flask_app = Flask(__name__)
    #connect to database with database emergente_db.bd
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emergente_db.db'
    #flask_app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.abspath(os.getcwd())+"/emergente_db.db"
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.app_context().push()
    db.init_app(flask_app)
    db.create_all()
    return flask_app


