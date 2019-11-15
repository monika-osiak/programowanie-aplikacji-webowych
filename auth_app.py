from flask import Flask, render_template, make_response, request
from uuid import uuid4

app = Flask(__name__)

users = {
    'admin': 'password',
}

session = dict()
SESSION_TIME = 180
INVALIDATE = -1

@app.route('/') # main page
def index():
    session_id = request.cookies.get('session_id')
    user = request.cookies.get('username')
    return make_response(render_template('index.html', user=user))

@app.route('/login')
def login():
    return make_response(render_template('login.html'))

@app.route('/logout')
def logout():
    response = redirect('/')
    response.set_cookie('session_id', 'INVALIDATE', max_age=INVALIDATE)
    response.set_cookie('username', 'INVALIDATE', max_age=INVALIDATE)
    return response

@app.route('/auth', methods=['POST']) # authenticate users
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    response = make_response('', 303)

    if username in users and users[username] == password:
        session_id = str(uuid4())
        response.set_cookie('session_id', session_id, max_age=SESSION_TIME)
        response.headers['Location'] = '/'
        response.set_cookie('username', username, max_age=SESSION_TIME)
    else:
        response.set_cookie('session_id', 'INVALIDATE', max_age=INVALIDATE)
        response.headers['Location'] = '/login'

    return response

@app.route('/register')
def register():
    return make_response(render_template('register.html'))

@app.route('/validate', methods=['POST']) # validate new users
def validate():
    username = request.form.get('username')
    password = request.form.get('password')

    if username not in users:
        users[username] = password
        response = redirect('/login')
    else:
        response = redirect('/register')

    return response

@app.route('/check/<username>') # check is username is available
def check(username):
    if username in users:
        status = 404
    else:
        status = 200
    return make_response('', status)

@app.route('/all')
def all():
    return users

def redirect(location):
    response = make_response('', 303)
    response.headers['Location'] = location
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')