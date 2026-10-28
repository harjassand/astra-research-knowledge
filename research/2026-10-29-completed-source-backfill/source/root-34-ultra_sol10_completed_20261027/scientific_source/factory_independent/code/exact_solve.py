"""Ordinary fraction-free Gaussian elimination with exact RHS verification."""
from fractions import Fraction as F
from math import lcm

class ExactFactor:
    def __init__(self,A):
        self.n=len(A);self.scales=[];work=[]
        for row in A:
            d=lcm(*(x.denominator for x in row));self.scales.append(d);work.append([int(x*d)for x in row])
        self.steps=[];previous=1
        for k in range(self.n-1):
            pivot=work[k][k];assert pivot
            coefficients=[work[i][k]for i in range(k+1,self.n)]
            self.steps.append((pivot,previous,coefficients))
            for i in range(k+1,self.n):
                a=work[i][k]
                for j in range(k+1,self.n):
                    numerator=work[i][j]*pivot-a*work[k][j]
                    quotient,remainder=divmod(numerator,previous);assert remainder==0
                    work[i][j]=quotient
                work[i][k]=0
            previous=pivot
        assert work[-1][-1];self.U=work
    def solve(self,B):
        cols=len(B[0]);b=[[F(v)*self.scales[i]for v in row]for i,row in enumerate(B)]
        for k,(pivot,previous,coefficients)in enumerate(self.steps):
            for i,a in zip(range(k+1,self.n),coefficients):
                b[i]=[(pivot*x-a*y)/previous for x,y in zip(b[i],b[k])]
        ans=[[F(0)]*cols for _ in range(self.n)]
        for i in range(self.n-1,-1,-1):
            for col in range(cols):ans[i][col]=(b[i][col]-sum(self.U[i][j]*ans[j][col]for j in range(i+1,self.n)))/self.U[i][i]
        return ans

def verify_system(A,X,B):
    for i,row in enumerate(A):
        for k in range(len(B[0])):assert sum(a*X[j][k]for j,a in enumerate(row))==B[i][k]
