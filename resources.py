from flask_restful import Resource, reqparse
from flask import make_response, render_template
import models

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

        #if models.UserModel.find_by_username(data['username']):
        #    return {'message': 'User {} already exists'. format(data['username'])}

        new_user = models.UserModel(
            username = data['username'],
            password = data['password'],
            email = data['email']
        )
        print(data)
        new_user.save_to_db()
        #try:
        #    new_user.save_to_db()
        #    return {'message': 'User {} was created'.format( data['username'])}, 200
        #except:
        #    return {'message': 'Something went wrong'}, 500


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