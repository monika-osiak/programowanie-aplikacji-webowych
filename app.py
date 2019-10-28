# app.py - a minimal flask api using flask_restful

from flask import Flask, render_template, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

import views, models, resources

api.add_resource(resources.Index, '/')
api.add_resource(resources.Login, '/login')
api.add_resource(resources.Register, '/register')
api.add_resource(resources.CheckLogin, '/user/<username>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')