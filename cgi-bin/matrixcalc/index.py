#!/usr/bin/env python
# coding=utf-8

# Import modules for CGI Handling
import cgi, cgitb
from matrix import Matrix
from fractions import *

def parseNum(n):
    parts = n.split("/")
    if len(parts) > 1:
        return Fraction(parts[0])/Fraction(parts[1])
    else:
        return Fraction(n)

def parseTextToMatrix(m):
    if not m:
        raise ValueError('Input matrix must not be None')

    # Do validate
    lines = filter(lambda x: len(x) > 0, m.splitlines())
    rows = len(lines)
    cols = None
    matrix = None
    for row in range(rows):
        # Fetch matrix elements on each line
        colVals = lines[row].split()

        # Empty line
        if len(colVals) == 0:
            continue

        # initialize (meh but it works)
        if not cols:
            cols = len(colVals)
            if not matrix:
                matrix = Matrix(len(filter(lambda r: len(r.split()) > 0, lines)), len(colVals))
        elif cols != len(colVals):
            raise ValueError('All columns must have the same amount of elements')

        # Parse row
        matrix[row] = [parseNum(val) for val in colVals]

    return matrix

def end():
    print"""
      </body>
    </html>
    """
    exit()

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
a = form.getvalue('matrix-a')
b = form.getvalue('matrix-b')
mode = form.getvalue('mode')

if a == None:
    a = "1"
if b == None:
    b = "1"

# Start printing out html
# Print header: REQUIRED FOR CLIENT
print "Content-Type: text/html\r\n\r\n"

# Actual html page
print """
<html>
  <head>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="apple-touch-icon" sizes="57x57" href="/~horndo/favicon/apple-icon-57x57.png">
    <link rel="apple-touch-icon" sizes="60x60" href="/~horndo/favicon/apple-icon-60x60.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/~horndo/favicon/apple-icon-72x72.png">
    <link rel="apple-touch-icon" sizes="76x76" href="/~horndo/favicon/apple-icon-76x76.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/~horndo/favicon/apple-icon-114x114.png">
    <link rel="apple-touch-icon" sizes="120x120" href="/~horndo/favicon/apple-icon-120x120.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/~horndo/favicon/apple-icon-144x144.png">
    <link rel="apple-touch-icon" sizes="152x152" href="/~horndo/favicon/apple-icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/~horndo/favicon/apple-icon-180x180.png">
    <link rel="icon" type="image/png" sizes="192x192"  href="/~horndo/favicon/android-icon-192x192.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/~horndo/favicon/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="96x96" href="/~horndo/favicon/favicon-96x96.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/~horndo/favicon/favicon-16x16.png">
    <link rel="manifest" href="/~horndo/favicon/manifest.json">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="msapplication-TileImage" content="/~horndo/favicon/ms-icon-144x144.png">
    <meta name="theme-color" content="#ffffff">

    <title>MatrixCalc</title>
    <link rel="stylesheet" type="text/css" href="/~horndo/matrixcalc/index.css">
    <link href='http://fonts.googleapis.com/css?family=Cookie' rel='stylesheet' type='text/css'>

    <!-- JQuery sources -->
    <script language="JavaScript" type="text/javascript" src="/~horndo/js/jquery_cookie.js"></script>
    <script language="JavaScript" type="text/javascript" src="/~horndo/js/jquery.min.js"></script>

    <!-- Enable sweet alerts -->
    <script src="/~horndo/swal/sweetalert.min.js"></script>
    <link rel="stylesheet" type="text/css" href="/~horndo/swal/sweetalert.css">

    <script type="text/javascript">
        function setup() {
            enableChromeSupport();
            selectBoxChanged();
        }

        function enableChromeSupport() {
            if(!!window.chrome && !!window.chrome.webstore) {
                jQuery.getScript("https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=MML_HTMLorMML");
                if (Cookies.get('chrome') != 'exists') {
                    swal({
                        title: "Chrome support experimental",
                        text: "Chrome web browser does not natively support MathML and therefore this application will need to download some external javascripts.",
                        type: "error",
                        confirmButtonText: "Who cares..."});

                    Cookies.set('chrome', 'exists', { expires: 1 });
                }
            }
        }

        function selectBoxChanged() {
            var selectBox = document.getElementById("matrixselect");
            var selected = selectBox.options[selectBox.selectedIndex].value;

            // TODO: Debate whether splitting into every single available case is actually desirable
            if (selected == 'mult') {
                document.getElementById("matrix2").style.display = 'inline-block';
            } else if (selected == 'tran') {
                document.getElementById("matrix2").style.display = 'none';
            } else if (selected == 'symm') {
                document.getElementById("matrix2").style.display = 'none';
            } else if (selected == 'lrze') {
                document.getElementById("matrix2").style.display = 'none';
            }
        }

        window.onload = setup;
    </script>

    <style>
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }

        th, td {
          padding: 20px;
        }
    </style>
  </head>
  <body>
    <header class="header">
        <div class="header-limiter">
            <h1><a href="#">Matrix<span>Calc</span></a></h1>
            <!--<nav>
                <a href="#" class="selected">Home</a>
                <a href="#">About</a>
                <a href="#">Contribute</a>
                <a href="#">Faq</a>
            </nav>-->
        </div>
    </header>

    <form action="index.py" method="GET" class="center">
        <div style="display: block;">
            <p style="display: inline-block;">Calculation to be performed:</p>
            <select name="mode" onchange="selectBoxChanged()" id="matrixselect">
"""

# TODO replace with proper code
if mode == "mult":
    print("<option value='mult' selected>multiply</option><option value='tran'>transpose</option><option value='symm'>symmetry</option><option value='lrze'>LR</option>")
elif mode == "tran":
    print("<option value='mult'>multiply</option><option value='tran' selected>transpose</option><option value='symm'>symmetry</option><option value='lrze'>LR</option>")
elif mode == "symm":
    print("<option value='mult'>multiply</option><option value='tran'>transpose</option><option value='symm' selected>symmetry</option><option value='lrze'>LR</option>")
elif mode == "lrze":
    print("<option value='mult'>multiply</option><option value='tran'>transpose</option><option value='symm'>symmetry</option><option value='lrze' selected>LR</option>")
else:
    print("<option value='mult'>multiply</option><option value='tran'>transpose</option><option value='symm'>symmetry</option><option value='lrze'>LR</option>")

print"""
            </select>
        </div>
        <h4 class="center">Input Matrices:</h4>
        <div id="container">
            <div style="display: inline-block;" class="box" id="matrix1">
                <textarea name="matrix-a" cols="20" rows="10" style='resize: none;'>{0}</textarea>
            </div>
            <div style="display: inline-block;" class="box" id="matrix2">
                <textarea name="matrix-b" cols="20" rows="10" style='resize: none;'>{1}</textarea>
            </div>
        </div>
        <div class="center">
            <input type="submit" value="calculate"/>
        </div>
    </form>
""".format(a, b)

# Actual script
if mode == "mult":
    try:
        ma = parseTextToMatrix(a)
    except ValueError as e:
        print"""<script> swal({
            title: "Could not parse left Matrix",
            text: "{0}",
            type: "error",
            confirmButtonText: "Ok"});</script>""".format(e)
        end()
    try:
        mb = parseTextToMatrix(b)
    except ValueError as e:
        print"""<script> swal({
            title: "Could not parse right Matrix",
            text: "{0}",
            type: "error",
            confirmButtonText: "Ok"});</script>""".format(e)
        end()
    try:
        mc = ma * mb
    except ValueError as e:
        print"""<script> swal({
            title: "Could not multiply Matrices",
            text: "{0}",
            type: "error",
            confirmButtonText: "Ok"});</script>""".format(e)
        end()

    print("<div class='center'><h3>Result:</h3><math style='display: inline-block;'>" + str(ma) + "<mo>&middot;</mo>" + str(mb) + "<mo>=</mo>" + str(mc) + "</math></div>")
elif mode == "tran":
    try:
        ma = parseTextToMatrix(a)
    except ValueError as e:
        print"""<script> swal({
            title: "Could not parse Matrix",
            text: "{0}",
            type: "error",
            confirmButtonText: "Ok"});</script>""".format(e)
        end()

    print("<div class='center'><h3>Result:</h3><math style='display: inline-block;'><msup>" + str(ma) + "<mi>T</mi></msup><mo>=</mo>" + str(ma.getTransposed()) + "</math></div>")
elif mode == "symm":
    try:
        ma = parseTextToMatrix(a)
    except ValueError as e:
        print"""<script> swal({
            title: "Could not parse Matrix",
            text: "{0}",
            type: "error",
            confirmButtonText: "Ok"});</script>""".format(e)
        end()

    print("<div class='center'><h3>Result:</h3><p>")
    if ma.isSymmetrical():
        print("The matrix is symmetric, meaning <math style='display: inline-block;'><msup><mi>A</mi><mi>T</mi></msup> <mo>=</mo> <mi>A</mi></math>")
    else:
        print("The matrix is not symmetric, meaning <math style='display: inline-block;'><msup><mi>A</mi><mi>T</mi></msup> <mo>&ne;</mo> <mi>A</mi></math>")
    print("</p></div>")
elif mode == "lrze":
    try:
        ma = parseTextToMatrix(a)
    except ValueError as e:
        print"""<script> swal({
            title: "Could not parse Matrix",
            text: "{0}",
            type: "error",
            confirmButtonText: "Ok"});</script>""".format(e)
        end()

    print("<div class='center'><h3>Result:</h3>")
    try:
        (c, l, r, p) = ma.getLR()
        print("<math style='display: inline-block;'><mi>C</mi> <mo>=</mo>{0}</math>".format(c))
        print("<math style='display: inline-block;'><mi>L</mi> <mo>=</mo>{0}</math>".format(l))
        print("<math style='display: inline-block;'><mi>R</mi> <mo>=</mo>{0}</math>".format(r))
        print("<math style='display: inline-block;'><mi>P</mi> <mo>=</mo>{0}</math>".format(p))
        print("</div>")
    except Exception as e:
        print("An error occured during lr execution: {0}</div>".format(repr(e)))
        end()

end()
