from flask import Flask, request, make_response
from auth_app import redirect
from uuid import uuid4
from jwt import decode, InvalidTokenError

app = Flask(__name__)
JWT_SECRET = 'secret'

@app.route('/download/<fid>')
def download(fid):
    pass

@app.route('/upload', methods=['POST'])
def upload():
    pass