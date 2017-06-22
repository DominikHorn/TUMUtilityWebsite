#!/usr/bin/env python
# coding=utf-8

# Import modules for CGI Handling
import cgi, cgitb
import library

# Print header: REQUIRED FOR CLIENT
print "Content-Type: text/html\r\n\r\n"
print """
<html>
    <head>
        <title>GIT -> SVN</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Hier könnte Ihre Werbung stehen</h1>
        <p>zum <a href="login.py"> login</p>
    </body>
</html>
"""
