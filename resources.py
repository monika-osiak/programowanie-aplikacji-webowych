from flask_restful import Resource, reqparse
from flask import make_response, render_template

users = [
    'osiakm',
    'admin'
]

parser = reqparse.RequestParser().add_argument(
    'username', help='This field cannot be blank', required=True
).add_argument(
    'email', help='This field cannot be blank', required=True
).add_argument(
    'password', help='This field cannot be blank', required=True
)

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

    def post(self):
        headers = {'Content-Type': 'text/html'}
        data = parser.parse_args()
        print(data)
        return make_response(data, 200, headers)


class CheckLogin(Resource):
    def get(self, username):
        headers = {'Content-Type': 'text/html'}
        if username in users:
            status = 404
            message = "User exists."
        else:
            status = 200
            message = "There is no user with this username."
        return make_response(message, status, headers)