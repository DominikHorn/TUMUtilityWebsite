#!/usr/bin/env python
# coding=utf-8

# Import modules for CGI Handling
import cgi, cgitb
import os

# Adds a user to the database
def addUser(name, password):
    salt = os.urandom(16)


# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
email = form.getvalue('email')
username = form.getvalue('username')
password  = form.getvalue('password')

# Print header: REQUIRED FOR CLIENT
print "Content-Type: text/html\r\n\r\n"

# Actual html page
print """
<html>
    <head>
        <title>Login</title>
    </head>
    <body>
        <p>Please login using your username and password</p>
        <form action="hook-migrator.py" method="POST">
        Email <input onClick="this.setSelectionRange(0, this.value.length)" type="text" name="email" value="max.musterman@musterman.de">  <br />
        Username <input onClick="this.setSelectionRange(0, this.value.length)" type="text" name="username" value="Gustav die Gans">  <br />
        Password <input onClick="this.setSelectionRange(0, this.value.length)" type="password" name="password" /> <br />
        <input type="submit" value="Login"/>
        </form>
    </body>
</html>
"""
