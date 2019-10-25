# app.py - a minimal flask api using flask_restful

from flask import Flask, render_template, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

users = [
    'osiakm',
    'admin'
]

class Index(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)

class Login(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'), 200, headers)

class Register(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('register.html'), 200, headers)

class CheckLogin(Resource):
    def get(self, username):
        headers = {'Content-Type': 'text/html'}
        if username in users:
            status = 404
        else:
            status = 200
        return make_response(render_template('user.html'), status, headers)

api.add_resource(Index, '/')
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(CheckLogin, '/user/<username>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')