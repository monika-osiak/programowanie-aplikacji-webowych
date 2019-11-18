from flask import Flask, request, make_response
from auth_app import redirect, JWT_SECRET
from uuid import uuid4
from jwt import decode, InvalidTokenError

import os

app = Flask(__name__)
#JWT_SECRET = 'secret'

@app.route('/download/<fid>')
def download(fid):
    token = request.headers.get('token') or request.args.get('token')
    
    if len(fid) == 0:
        return make_response('<h1>FILE APP</h1> Missing fid.', 404)
    
    if token is None:
        return make_response('<h1>FILE APP</h1> No token.', 401)

    if not valid(token):
        return make_response('<h1>FILE APP</h1> Invalid token.', 401)

    payload = decode(token, JWT_SECRET)
    if payload.get('fid', fid) != fid:
        return make_response('<h1>FILE APP</h1> Incorrect token payload.', 401)
    
    content_type = request.headers.get('Accept') or request.args.get('content_type')
    with open('tmp/' + fid, 'rb') as file:
        content = file.read()
        response = make_response(content, 200)
        response.headers['Content-Type'] = content_type
        return response

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('file')
    token = request.form.get('token')
    callback = 'http://0.0.0.0:5000' + request.form.get('callback')
    print(callback)

    if f is None:
        return make_response('<h1>FILE APP</h1> No file provided.', 400)
    
    if token is None:
        return make_response('<h1>FILE APP</h1> No token provided.', 401)

    if not valid(token):
        return make_response('<h1>FILE APP</h1> Invalid token.', 401)

    try:
        os.makedirs("tmp/")
    except FileExistsError:
        # directory already exists
        pass

    fid, content_type = str(uuid4()), f.content_type
    f.save('tmp/' + fid)
    f.close()

    #return make_response(f'<h1>FILE APP</h1> Uploaded {fid}', 200)
    return redirect(f"{callback}?fid={fid}&content_type={content_type}") if callback \
    else (f'<h1>CDN</h1> Uploaded {fid}', 200)

def valid(token):
    try:
        decode(token, JWT_SECRET)
    except InvalidTokenError as err:
        print(str(err))
        return False
    return True

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)