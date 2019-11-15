from flask import Flask, render_template, make_response

app = Flask(__name__)

users = {
    'admin': 'password',
}

session = dict()

@app.route('/') # main page
def index():
    pass

@app.route('/login')
def login():
    return make_response(render_template('login.html'))

@app.route('/auth') # authenticate users
def auth():
    pass

@app.route('/register')
def register():
    return make_response(render_template('register.html'))

@app.route('/validate') # validate new users
def validate():
    pass

@app.route('/check/<username>') # check is username is available
def check(username):
    pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')