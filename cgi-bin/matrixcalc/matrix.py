from fractions import *
from collections import Iterable
import copy

'''
Matrix class can be used to do matrix operations
'''
class Matrix:
    def __init__(self, rows, columns):
        if columns < 1 or rows < 1:
            raise ValueError("Matrix dimensions must be greater than zero")

        self._data = [[Fraction(0) for x in range(columns)] for y in range(rows)]

    def __str__(self):
        if self.rowCount() == self.columnCount() and self.rowCount() == 1:
            if self[0][0] == 0:
                return "<mn>0</mn>"
            return "<mn>{0}</mn>".format(self[0][0])

        string="<mfenced><mtable>"

        # i = Zeile, j = spalte
        for i in range(self.rowCount()):
            string += "<mtr>"
            for j in range(self.columnCount()):
                if self[i][j] == 0:
                    string += "<mtd><mn>0</mn></mtd>"
                else:
                    string += "<mtd><mn>{0}</mn></mtd>".format(self[i][j])
            string += "</mtr>"

        string += "</mtable></mfenced>"
        return string

    def __repr__(self):
        return self.__str__()

    '''
    Returns a new matrix C.
    self * other = C
    '''
    def __mul__(self, other):
        # Matrix multiplication
        if isinstance(other, Matrix):
            if self.columnCount() != other.rowCount():
                if self.rowCount() == self.columnCount() and self.rowCount() == 1:
                    return other * self[0][0]
                elif other.rowCount() == other.columnCount() and other.rowCount() == 1:
                    return self * other[0][0]
                else:
                    raise ValueError("Cannot multiply those matrices since dimensions are incompatible")

            c = Matrix(self.rowCount(), other.columnCount())
            for i in range(c.rowCount()):
                for j in range(c.columnCount()):
                    # Calculate sum from line and column
                    value = 0
                    row = self[i]
                    column = other.columnAt(j)
                    for k in range(len(row)):
                        value += row[k] * column[k]

                    c[i][j] = value

            return c
        elif isinstance(other, Iterable):
            if self.columnCount() != len(other):
                raise ValueError("len(vector) must be equal to the length of each row of the matrix")

            data = []
            for row in range(self.rowCount()):
                summed = 0
                for column in range(len(other)):
                    summed += self[row][column] * other[column]
                data.append(summed)
            return data
        else:
            other = Fraction(other)
            c = Matrix(self.rowCount(), self.columnCount())
            for row in range(c.rowCount()):
                for column in range(c.columnCount()):
                    c[row][column] = self[row][column] * other

            return c

    def __pow__(self, pot):
        if pot == 0:
            identity = Matrix(self.columnCount(), self.columnCount())
            for i in range(identity.rowCount()):
                identity[i][i] = 1

            return identity

        # Use binary exponentiation to enhance speed
        bits = ("{0:b}".format(pot))[1:]
        result = self
        for bit in bits:
            if bit == "0":
                result = result * result
            else:
                result = result * result
                result = result * self

        return result

    def __getitem__(self, indices):
        return self._data[indices]

    def __setitem__(self, indices, value):
        if isinstance(value, Iterable):
            if not len(value) == self.columnCount():
                raise ValueError("Can not change matrix length")
            value = [Fraction(v) for v in value]
        else:
            value = [Fraction(value) for i in range(self.columnCount())]

        self._data[indices] = value

    def __eq__(self, other):
        if other.rowCount() != self.rowCount() or other.columnCount() != self.columnCount():
            return False

        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                if other[i][j] != self[i][j]:
                    return False

        return True

    def __ne__(self, other):
        return not (other == self)

    def isSymmetrical(self):
        return self.getTransposed() == self

    def rowAt(self, index):
        return self[index]

    def columnAt(self, index):
        return [row[index] for row in self]

    def getTransposed(self):
        transposed = Matrix(self.columnCount(), self.rowCount())
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                transposed[j][i] = self[i][j]

        return transposed

    '''
    Returns determinant of this matrix
    '''
    def getDeterminant(self):
        if self.rowCount() != self.columnCount():
            raise ValueError("Determinant only defined for quadratic matrices")

        # Abuse LR to obtain Determinant
        (c, l, r, p, sc) = self.getLR()

        # Obtain Determinant
        var = Fraction(1)
        for i in range(r.rowCount()):
            var *= r[i][i]

        # Fix sign based on swaps happened in Pivot
        if sc % 2 != 0:
            var = -var

        return var

    '''
    Calculates and returns the L/R components so that L * R = A
    @return c: combined L/R
    @return l: l Matrix
    @return r: r Matrix
    @return p: p Pivot
    @return sc: swap count
    '''
    def getLR(self):
        t = self.getCopy()
        (p, sc) = t.__lr()
        l = Matrix(self.rowCount(), self.columnCount())
        r = Matrix(self.rowCount(), self.columnCount())
        for i in range(self.rowCount()):
            for j in range(i):
                l[i][j] = t[i][j]
                r[i][j] = Fraction(0)
            l[i][i] = Fraction(1)
            r[i][i] = t[i][i]
            for j in range(i+1,self.columnCount()):
                l[i][j] = Fraction(0)
                r[i][j] = t[i][j]

        return (t, l, r, p, sc)

    '''
    Mutating method for retrieving LR
    @return pivot matrix P
    '''
    def __lr(self):
        if self.rowCount() == self.columnCount() and self.rowCount() <= 1:
            return

        pivot = []
        swapcount = 0
        for o in range(0, self.rowCount()-1):
            # Create Identity matrix
            m = Matrix(self.rowCount(), self.columnCount())
            for i in range(self.rowCount()):
                m[i][i] = 1

            # Find bigest alpha
            maxvalue = self[o][o]
            index = o
            for row in range(o+1, self.rowCount()):
                # Check for absolute value
                if self[row][o]*self[row][o] > maxvalue*maxvalue:
                    index = row
                    maxvalue = self[row][o]

            # Swap values around
            tmp = m[o]
            m[o] = m[index]
            m[index] = tmp
            tmp = self[o]
            self[o] = self[index]
            self[index] = tmp

            if index != o:
                swapcount += 1

            # Append pivot matrix
            pivot.append(m)

            for row in range(o+1, self.rowCount()):
                # Calculate v / alpha
                self[row][o] = self[row][o] / self[o][o]

                # Calculate inner matrix thingy
                for column in range(o+1, self.columnCount()):
                    self[row][column] = self[row][column] - self[row][o] * self[o][column]

        result = None
        for elem in reversed(pivot):
            if not result:
                result = elem
            else:
                result = result * elem

        return (result, swapcount)

    '''
    Returns a deep copy of this object
    '''
    def getCopy(self):
        return copy.deepcopy(self)

    def rowCount(self):
        return len(self._data)

    def columnCount(self):
        return len(self[0])
