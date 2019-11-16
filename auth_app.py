from flask import Flask, render_template, make_response, request
from uuid import uuid4
from jwt import encode

import datetime

app = Flask(__name__)

users = {
    'admin': 'password',
}

session = dict()
JWT_SECRET = 'secret'
JWT_SESSION_TIME = 30
SESSION_TIME = 180
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

@app.route('/upload')
def upload():
    session_id = request.cookies.get('session_id')
    username = request.cookies.get('username')

    if session_id:
        if session_id in session:
            fid, content_type = session[session_id]
        else:
            fid, content_type = '', 'text/plain'

        download_token = create_token(fid).decode('ascii')
        upload_token = create_token().decode('ascii')
        return make_response(render_template('upload.html', upload_token=upload_token, user=username), 200)
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

    content_type = request.args.get('content_type', 'text_plain')
    session[session_id] = (fid, content_type)
    return make_response(f'<h1>AUTH APP</h1> User {username} uploaded {fid} ({content_type}).', 200)

def create_token(fid=None):
    exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_SESSION_TIME)
    return encode({'iss': 'mendeley.io', 'exp': exp}, JWT_SECRET, 'HS256')

def redirect(location):
    response = make_response('', 303)
    response.headers['Location'] = location
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')