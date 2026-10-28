"""Small standard-library exact matrix helpers for mathematical fixtures."""
from fractions import Fraction as Q
from itertools import combinations

class Mat:
    def __init__(self, data):
        if not isinstance(data[0], (list, tuple)):
            data = [[x] for x in data]
        self.a = [[Q(x) for x in row] for row in data]
        self.rows, self.cols = len(self.a), len(self.a[0])
    def __getitem__(self, index):
        return self.a[index[0]][index[1]] if isinstance(index, tuple) else self.a[index][0]
    def __eq__(self, other):
        return self.a == other.a
    @property
    def T(self):
        return Mat(list(zip(*self.a)))
    def __add__(self, other):
        return Mat([[x+y for x,y in zip(ar,br)] for ar,br in zip(self.a,other.a)])
    def __sub__(self, other):
        return self + (-1)*other
    def __mul__(self, other):
        if isinstance(other, Mat):
            return Mat([[sum((x*y for x,y in zip(row,col)),Q(0))
                         for col in zip(*other.a)] for row in self.a])
        return Mat([[other*x for x in row] for row in self.a])
    __rmul__ = __mul__
    def __truediv__(self, other):
        return self * (Q(1)/other)
    def extract(self, rows, cols):
        return Mat([[self.a[j][k] for k in cols] for j in rows])
    def det(self):
        if self.rows == 1:
            return self.a[0][0]
        return sum(((-1)**k*self.a[0][k]*self.extract(range(1,self.rows),
                    [j for j in range(self.cols) if j != k]).det()
                    for k in range(self.cols)),Q(0))

def diag(*entries):
    return Mat([[entries[j] if j == k else 0 for k in range(len(entries))]
                for j in range(len(entries))])

def zeros(rows, cols=1):
    return Mat([[0]*cols for _ in range(rows)])

def norm2(v):
    return (v.T*v)[0]

def psd(a):
    assert a == a.T
    return all(a.extract(subset, subset).det() >= 0
               for size in range(1, a.rows+1)
               for subset in combinations(range(a.rows), size))

def block(a,b,c,d):
    return Mat([ar+br for ar,br in zip(a.a,b.a)]
               +[cr+dr for cr,dr in zip(c.a,d.a)])
