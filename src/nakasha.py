# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
    Nakasha
    =======
    Simple service and web application to locate rooms in campuses.
    
    :copyright: (c) 2010 by Mithun Shitole, Shrikant Shinde.
    :license: MIT, See LICENSE file
"""
from flask import Flask, render_template, g, request, jsonify
import sqlite3

app = Flask(__name__)

# Setup initial config
app.config.update(dict(
    DATABASE = '/tmp/nakasha.db',
    DEBUG = True
))

#### Database functions ####

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    """ creates the database tables """
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def insert_data(query, params):
    with app.app_context():
        db = get_db()
        db.cursor().executemany(query, params)
        db.commit()
    
def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

# Write the database interactions
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def get_rooms(filter=None):
    """returns the list of rooms"""
    rooms = query_db("SELECT * FROM room")
    return rooms

def get_room(name):
    room  = query_db("SELECT * FROM room where name=?", [name], True)
    return room

##### Before/after request hooks ####

@app.before_request
def before_request():
    get_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

##### Routes ####

@app.route("/")
def index():
    """ Single page client application"""
    return render_template("index.html")

# REST API
@app.route("/api/rooms")
def rooms():
    rooms  = get_rooms()
    return jsonify(rooms=rooms, total=len(rooms))

@app.route("/api/rooms/<name>")
def room(name):
    room  = get_room(name)
    return  jsonify(room)

if __name__=="__main__":
    init_db()
    app.run()
