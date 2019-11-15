from flask import Flask, render_template, make_response

app = Flask(__name__)

@app.route('/') # main page
def index():
    pass

@app.route('/login')
def login():
    pass

@app.route('/auth') # authenticate users
def auth():
    pass

@app.route('/register')
def register():
    pass

@app.route('/validate') # validate new users
def validate():
    pass

@app.route('/check/<username>') # check is username is available
def check(username):
    pass