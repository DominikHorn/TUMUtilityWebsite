#!/usr/bin/env python
# coding=utf-8

# Import modules for CGI Handling
import cgi, cgitb
from mode import *

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
a = form.getvalue('matrix-a')
b = form.getvalue('matrix-b')
mode = form.getvalue('mode')

# Initialize other globals
modes = getModes()

if a == None:
    a = "1"
if b == None:
    b = "1"
if mode == None:
    mode = "mult"

# Start printing out html
# Print header: REQUIRED FOR CLIENT
print("Content-Type: text/html\r\n\r\n")

# Actual html page
print("""
<html>
  <head>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta content='initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=0' name='viewport'/>

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
                document.getElementById("matrix2").style.display = 'block';
            } else if (selected == 'tran') {
                document.getElementById("matrix2").style.display = 'none';
            } else if (selected == 'symm') {
                document.getElementById("matrix2").style.display = 'none';
            } else if (selected == 'lrze') {
                document.getElementById("matrix2").style.display = 'none';
            } else if (selected == 'dete') {
                document.getElementById("matrix2").style.display = 'none';
            } else if (selected == 'solv') {
                document.getElementById("matrix2").style.display = 'block';
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
""")

for key in modes:
    print("<option value='{0}' {1}>{2}</option>".format(key, "selected" if key == mode else "", modes[key].getShortDesc()))

print("""
            </select>
        </div>
        <h4 class="center">Input Matrices:</h4>
        <div id="container">
            <div style="display: block;" class="box" id="matrix1">
                <textarea name="matrix-a" cols="20" rows="10" style='resize: none;'>{0}</textarea>
            </div>
            <div style="display: block;" class="box" id="matrix2">
                <textarea name="matrix-b" cols="20" rows="10" style='resize: none;'>{1}</textarea>
            </div>
        </div>
        <div class="center">
            <input type="submit" value="calculate"/>
        </div>
    </form>
""".format(a, b))

# Let mode impl handle the actual wörk
m = modes[mode]
m.handle(a, b)

print("""
  <footer>
  </footer>
  </body>
</html>
""")
