from flask import Flask
from models import db
from decouple import config
from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

def configure_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')
    db.init_app(app)