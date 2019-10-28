# app.py - a minimal flask api using flask_restful

from flask import Flask, render_template, make_response
from flask_restful import Resource, Api

import views, models, resources

app = Flask(__name__)
api = Api(app)

api.add_resource(resources.Index, '/')
api.add_resource(resources.Login, '/login')
api.add_resource(resources.Register, '/register')
api.add_resource(resources.CheckLogin, '/user/<username>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')