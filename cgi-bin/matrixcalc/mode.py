from matrix import *
from fractions import *

'''
TODO: factor this into matrix class (?)
'''
def parseNum(n):
    parts = n.split("/")
    if len(parts) > 1:
        return Fraction(parts[0])/Fraction(parts[1])
    else:
        return Fraction(n)

'''
TODO: factor this into matrix class
'''
def parseTextToMatrix(m):
    if not m:
        raise ValueError('Input matrix must not be None')

    # Do validate
    lines = list(filter(lambda x: len(x) > 0, m.splitlines()))
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
                matrix = Matrix(len(list(filter(lambda r: len(r.split()) > 0, lines))), len(colVals))
        elif cols != len(colVals):
            raise ValueError('All columns must have the same amount of elements')

        # Parse row
        matrix[row] = [parseNum(val) for val in colVals]

    return matrix

'''
Each mode implements one calculation mode
'''
class Mode:
    def __init__(self):
        pass

    def getShortDesc(self):
        pass

    def handle(self, ma, mb=None):
        pass

class ModeMult(Mode):
    def __init__(self):
        pass

    def getShortDesc(self):
        return "multiply"

    def handle(self, a, b=None):
        try:
            ma = parseTextToMatrix(a)
        except ValueError as e:
            print("""<script> swal({
                title: "Could not parse left Matrix",
                text: "{0}",
                type: "error",
                confirmButtonText: "Ok"});</script>""".format(e))
            return
        try:
            mb = parseTextToMatrix(b)
        except ValueError as e:
            print("""<script> swal({
                title: "Could not parse right Matrix",
                text: "{0}",
                type: "error",
                confirmButtonText: "Ok"});</script>""".format(e))
            return
        try:
            mc = ma * mb
        except ValueError as e:
            print("""<script> swal({
                title: "Could not multiply Matrices",
                text: "{0}",
                type: "error",
                confirmButtonText: "Ok"});</script>""".format(e))
            return

        print("<div class='center'><h3>Result:</h3><math style='display: inline-block;'>" + str(ma) + "<mo>&middot;</mo>" + str(mb) + "<mo>=</mo>" + str(mc) + "</math></div>")

class ModeTran(Mode):
    def __init__(self):
        pass

    def getShortDesc(self):
        return "transpose"

    def handle(self, a, b=None):
        try:
            ma = parseTextToMatrix(a)
        except ValueError as e:
            print("""<script> swal({
                title: "Could not parse Matrix",
                text: "{0}",
                type: "error",
                confirmButtonText: "Ok"});</script>""".format(e))
            return

        print("<div class='center'><h3>Result:</h3><math style='display: inline-block;'><msup>" + str(ma) + "<mi>T</mi></msup><mo>=</mo>" + str(ma.getTransposed()) + "</math></div>")

class ModeSymm(Mode):
    def __init__(self):
        pass

    def getShortDesc(self):
        return "symmetry"

    def handle(self, a, b=None):
        try:
            ma = parseTextToMatrix(a)
        except ValueError as e:
            print("""<script> swal({
                title: "Could not parse Matrix",
                text: "{0}",
                type: "error",
                confirmButtonText: "Ok"});</script>""".format(e))
            return

        print("<div class='center'><h3>Result:</h3><p>")
        if ma.isSymmetrical():
            print("The matrix is symmetric, meaning <math style='display: inline-block;'><msup><mi>A</mi><mi>T</mi></msup> <mo>=</mo> <mi>A</mi></math>")
        else:
            print("The matrix is not symmetric, meaning <math style='display: inline-block;'><msup><mi>A</mi><mi>T</mi></msup> <mo>&ne;</mo> <mi>A</mi></math>")
        print("</p></div>")

class ModeLRZE(Mode):
    def __init__(self):
        pass

    def getShortDesc(self):
        return "LR"

    def handle(self, a, b=None):
        try:
            ma = parseTextToMatrix(a)
        except ValueError as e:
            print("""<script> swal({
                title: "Could not parse Matrix",
                text: "{0}",
                type: "error",
                confirmButtonText: "Ok"});</script>""".format(e))
            return

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
            return

def getModes():
    return {"mult" : ModeMult(), "tran" : ModeTran(), "symm" : ModeSymm(), "lrze" : ModeLRZE()}
