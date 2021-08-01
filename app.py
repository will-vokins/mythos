#!/usr/bin/env python
''' Main file, center of operations for Mythos RPG '''

__author__ = "Will D. Vokins"
__credits__ = ["Will D. Vokins"]
__copyright__ = "Copyright 2021, Will Vokins"

__license__ = "GPL"
__version__ = "0.0.1"
__status__ = "Prototype"
__email__ = "will@vokins.net"
__maintainer__ = "Will D. Vokins"
__updated__ = "09:10 2021-08-01 GMT"

from flask.json import jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, url_for, session, flash
from passlib.hash import sha256_crypt

import re
import json
import sqlite3



app = Flask(__name__)
app.secret = "Hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=30)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    _username = db.Column("username", db.String(12), unique=True)
    _password = db.Column("password", db.String(1028))
    _email = db.Column("email", db.String(128), unique=True)
    gender = db.Column("gender", db.String(1))
    hardcore = db.Column("hardcore", db.Boolean, default=False, nullable=False)
    role = db.Column("role", db.String(32))
    
    def __init__(self,
                 _username,
                 _password,
                 _email):
        
        self._username = _username
        self._password = _password
        self._email = _email
        

class user_stats(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer())
    stamina = db.Column("stamina", db.Integer())
    constitution = db.Column("constitution", db.Integer())
    agility = db.Column("agility", db.Integer())
    strength = db.Column("strength", db.Integer())
    perception = db.Column("perception", db.Integer())
    intellect = db.Column("intellect", db.Integer())
    guile = db.Column("guile", db.Integer())
    charisma = db.Column("charisma", db.Integer())
    magicks = db.Column("magicks", db.Integer())
    hit = db.Column("hit", db.Integer())
    spell_power = db.Column("spell_power", db.Integer())
    crit = db.Column("crit", db.Integer())
    spell_crit = db.Column("spell_crit", db.Integer())
    crit_damage = db.Column("crit_damage", db.Integer())
    armour = db.Column("armour", db.Integer())
    magic_resist = db.Column("magic_resist", db.Integer())
    
    def __init__(self,
                 user_id,
                 stamina,
                 constitution,
                 agility,
                 strength,
                 perception,
                 intellect,
                 guile,
                 charisma,
                 magicks,
                 hit,
                 spell_power,
                 crit,
                 spell_crit,
                 crit_damage,
                 armour,
                 magic_resist):
        
        self.user_id = user_id
        self.stamina = stamina
        self.constitution = constitution
        self.agility = agility
        self.strength = strength
        self.perception = perception
        self.intellect = intellect
        self.guile = guile
        self.charisma = charisma
        self.magicks = magicks
        self.hit = hit
        self.spell_power = spell_power
        self.crit = crit
        self.spell_crit = spell_crit
        self.crit_damage = crit_damage
        self.armour = armour
        self.magic_resist = magic_resist
    
commands = ["login\t\tlogin &lt;username&gt; &lt;password&gt;",
            "register\tregister &lt;username&gt; &lt;password&gt; &lt;email&gt;"]

badCommandMessage = "Invalid command! '?' will bring up command list"

def userHelp():
    returnString = "\n<u>Commands:</u>"
    for command in commands:
        returnString = returnString + "\n" + command
    
    return(returnString)
        
    
def create_character(username, password, email):
    if(len(username) > 12):
        return("Username too long. Please use between 1 and 12 characters.")
    if(len(password) > 35):
        return("Password too long. Please use between 8 and 35 characters.")
    if(len(password) < 8):
        return("Password to short. Please use between 8 and 35 characters.")
    
    emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    if(re.match(emailRegex, email)):
        pass
    else:
        return("Please enter a valid email address.")
    
    password = sha256_crypt.hash(password)
    
    found_user = users.query.filter_by(_username=username.lower()).first()
    found_email = users.query.filter_by(_email=email.lower()).first()
    if found_user:
        return("User '" + username + "' taken!")
    elif found_email:
        return("Email '" + email + "' in use!")
    else:
        usr = users(username.lower(), password, email.lower())
        try:
            db.session.add(usr)
            db.session.commit()
            return("Character '" + username + "' created!\nYou may now login using the credentials you provided.")
        except Exception as e:
            return("Error :( " + str(e))
        
def log_in(username, password):
    username = username.lower()
    
    found_user = users.query.filter_by(_username=username).first()
    if found_user:
        correct_password = sha256_crypt.verify(password, found_user._password)
        print(correct_password)
        if correct_password == True:
            return("Logged in")
            # Export user data to session.
        else:
            print(password)
            print(found_user._password)
            return("Incorrect password.")
    else:
        print(password)
        return("No character is associated with that username.")
    

@app.route("/")
def home_page():
    return render_template("home_page.html",
                           author=__author__,
                           version=__version__,
                           updated=__updated__)
    
@app.route("/command", methods=["POST"])
def handle_command():
    
    if request.method == "POST":
        command = request.form["command"]
        if(command != ""):
            command_array = command.split()
            command_length = len(command_array)
            if(command_length > 0):
                if(command[0].lower()=="?"):
                    return(userHelp())
                if(command_array[0].lower()=="login"):
                    if(command_length == 3):
                        return(log_in(command_array[1], command_array[2]))
                    else:
                        return(badCommandMessage)
                elif(command_array[0].lower()=="register"):
                    if(command_length == 4):
                        return create_character(command_array[1], command_array[2], command_array[3])
                    else:
                        return(badCommandMessage)
                else:
                    return(badCommandMessage)
            else:
                return(badCommandMessage)
        else:
            return (badCommandMessage)
    else:
        return("<pre>Invalid request</pre>", 400)
    
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)