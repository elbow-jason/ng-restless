#import flask
from flask import Flask

#import flask extensions
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless   import APIManager

#standard lib
import subprocess

#config values
SQLALCHEMY_DATABASE_URI ='sqlite:///some_database.db'
DEBUG = False
SECRET_KEY = 'development key'

#create app
app = Flask(__name__)

#config app
app.config.from_object(__name__)

#init extensitions
db = SQLAlchemy(app)
api_manager = APIManager(app, flask_sqlalchemy_db=db)

#many-to-many persons_to_hobbies
persons_hobbies = db.Table('persons_hobbies',
    db.Column('person_id', db.Integer, db.ForeignKey('person.id')),
    db.Column('hobby_id',  db.Integer, db.ForeignKey('hobby.id'))
    )

#base object class
class BaseSQLModel(object):
    id              = db.Column(db.Integer(), primary_key=True)
    name            = db.Column(db.String)


#Person Declarative DB object with mulitple inheritance
class Person(db.Model, BaseSQLModel):
    __tablename__   = 'person'
    profession      = db.Column(db.String)
    project         = db.Column(db.String)
    url             = db.Column(db.String)
    age             = db.Column(db.Integer)
    hobbies         = db.relationship('Hobby', secondary=persons_hobbies,
        backref=db.backref('persons', lazy='dynamic'))


#Person Declarative DB object with mulitple inheritance
class Hobby(db.Model, BaseSQLModel):
    __tablename__   = 'hobby'
    description     = db.Column(db.String)



# Create API endpoints, which will be available at /api/<tablename> by default.
# Allowed HTTP methods can be specified as well.
crud = ['POST', 'GET', 'PUT', 'DELETE' ]
api_manager.create_api(Person, methods=crud)
api_manager.create_api(Hobby,  methods=crud)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    subprocess.Popen(['python','seeder.py'])
    app.run()