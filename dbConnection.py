# CSE 5341: Senior Design at SMU, Spring 2019
# Adam Ashcraft, Chase Goehring, Jeremy Brachle, Matthew Wagner, Nora Potenti
# this program will connect to our database to perform login, register,
# and various other user management operations

# version 1.0.0.0

# import necessary libraries
import flask
from flask import jsonify, request
from flask_cors import CORS
import sqlite3
from sqlite3 import Error

# initialize the app and set up CORS
app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

# api routes
# default
@app.route('/', methods=['GET'])
def home():
    return "Default Route"

# login
@app.route('/login', methods=['POST'])
def login():
    try:
        # test connection to the database
        conn = sqlite3.connect('PlatinumMotors.db')
        cur = conn.cursor()
        # get the post arguments as json
        jsonData = request.get_json()
        # get the username password combo and execute the query
        username = jsonData['username']
        password = jsonData['password']
        cur.execute('select count(*) from User where username = \'' + str(username) + '\' and password = \'' + str(password) + '\'')
        # check the query and see if 1 or 0
        auth = cur.fetchone()
        # if 1, then success
        if (auth[0] == 1):
            return '1'
        else:
            return '0'
    except Error as e:
        print(e)
        return 'connection failed'


# set user
@app.route('/setUser', methods=['POST'])
def setUser():
    try:
        # test connection to the database
        conn = sqlite3.connect('PlatinumMotors.db')
        cur = conn.cursor()
        # get the post arguments as json
        jsonData = request.get_json()
        # get the username password combo
        username = jsonData['username']
        password = jsonData['password']
        cur.execute('select * from User where username = \'' + str(username) + '\' and password = \'' + str(password) + '\'')
        user = cur.fetchone()
        return jsonify(user)
    except Error as e:
        print(e)
        return 'connection failed'


# register
@app.route('/register', methods=['POST'])
def register():
    try:
        # test connection to the database
        conn = sqlite3.connect('PlatinumMotors.db')
        cur = conn.cursor()
        # get the post arguments as json
        jsonData = request.get_json()
        # get the username password combo and execute the query
        username = jsonData['username']
        password = jsonData['password']
        # check and make sure a unique entry for this username
        cur.execute('select count(*) from User where username = \'' + str(username) + '\'')
        # check the query and see if 1 or 0
        reg = cur.fetchone()
        # if 0, then no record exists yet
        if (reg[0] == 0):
            # execute the new query for creating the account, then commit the insert
            cur.execute('insert into User (username, password) values (\'' + str(username) + '\', \'' + str(password) + '\')')
            cur.execute('commit;')
            # return 1 to signify that the new record can be created with this username password combo
            return '1'
        else:
            # otherwise, this username already exists
            return '0'
    except Error as e:
        print(e)
        return 'connection failed'


# run the API
app.run()