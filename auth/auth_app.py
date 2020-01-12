from flask import Flask, render_template, make_response, request
from uuid import uuid4
from jwt import encode
from os import getenv
from dotenv import load_dotenv
from pprint import pprint
from copy import deepcopy

load_dotenv(verbose=True)

import datetime
import redis

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip

users = {
    'admin': 'password',
}

files = {
    'admin': [
        ['e1d54e90-61e2-417d-ac92-48202763460b', 'application/pdf'],
    ]
}

session = dict()
sessions = redis.Redis(host='0.0.0.0', port=6379, decode_responses=True)

JWT_SECRET = getenv('JWT_SECRET')
JWT_SESSION_TIME = int(getenv('JWT_SESSION_TIME'))
SESSION_TIME = int(getenv('SESSION_TIME'))
HOST = getenv('HOST')
AUTH_PORT = getenv('AUTH_PORT')
FILE_PORT = getenv('FILE_PORT')
INVALIDATE = -1

@app.route('/') # main page
def index():
    user = request.cookies.get('username')
    return make_response(render_template('index.html', user=user))

@app.route('/login')
def login():
    return make_response(render_template('login.html'))

@app.route('/logout')
def logout():
    # remove session_id from database
    username = request.cookies.get('username')
    sessions.delete(username)

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
        sessions.set(session_id, username)
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

@app.route('/upload')
def upload():
    session_id = request.cookies.get('session_id')
    username = request.cookies.get('username')

    if session_id:
        pprint(files)
        print()
        if sessions.exists(session_id) and username in files:
            files_data = deepcopy(files[username])
            
        else:
            files_data = [
                ['', 'text/plain']
            ]

        for elem in files_data:
            elem.append(create_token(elem[0]).decode('ascii'))
        pprint(files_data)
        # download_tokens = [create_token(fid).decode('ascii') for fid in fids]
        upload_token = create_token().decode('ascii')
        # action = f'http://{HOST}:{FILE_PORT}/upload'
        return make_response(render_template(
            'upload.html', 
            upload_token=upload_token, 
            user=username,
            files=files_data), 200)
    return redirect("/login")

@app.route('/remove/<fid>')
def remove(fid):
    session_id = request.cookies.get('session_id')
    username = request.cookies.get('username')

    if session_id:
        pprint(files)
        print()
        if sessions.exists(session_id) and username in files:
            files_data = deepcopy(files[username])
            
        else:
            files_data = [
                ['', 'text/plain']
            ]

        for i, elem in enumerate(files_data):
            if elem[0] == fid:
                files_data = files_data[0:i] + files_data[i+1:]
                files[username] = files_data
        # download_tokens = [create_token(fid).decode('ascii') for fid in fids]
        upload_token = create_token().decode('ascii')
        # action = f'http://{HOST}:{FILE_PORT}/upload'
        return make_response(render_template(
            'upload.html', 
            upload_token=upload_token, 
            user=username,
            files=files_data), 200)
    return redirect("/login")

@app.route('/callback')
def callback(): # when uploaded
    session_id = request.cookies.get('session_id')
    username = request.cookies.get('username')
    fid = request.args.get('fid')
    err = request.args.get('err')

    if not session_id:
        return redirect('/login')

    if err:
        return make_response(f'<h1>AUTH APP</h1> Upload failed: {err}', 400)
    
    if not fid:
        return make_response('<h1>AUTH APP</h1> Upload failed: successfull but no fid returned.', 400)

    download_token = create_token(fid).decode('ascii')
    content_type = request.args.get('content_type', 'text_plain')
    session[session_id] = (fid, content_type)
    if username not in files:
        files[username] = [
            [fid, content_type]
        ]
    else:
        files[username].append([fid, content_type])
    return redirect('/upload')

def create_token(fid=None):
    exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_SESSION_TIME)
    return encode({'iss': 'mendeley.io', 'exp': exp}, JWT_SECRET, 'HS256')

def redirect(location):
    response = make_response('', 303)
    response.headers['Location'] = location
    return response

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=AUTH_PORT)