# app.py - a minimal flask api using flask_restful

from flask import Flask, render_template, make_response
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'

db = SQLAlchemy(app)

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(120), nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
        

@app.before_first_request
def create_tables():
    print('Tworzenie bazy danych.')
    db.create_all()
    print(db.engine.table_names())

import views, models, resources

api.add_resource(resources.Index, '/')
api.add_resource(resources.Login, '/login')
api.add_resource(resources.Register, '/register')
api.add_resource(resources.CheckLogin, '/user/<username>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')