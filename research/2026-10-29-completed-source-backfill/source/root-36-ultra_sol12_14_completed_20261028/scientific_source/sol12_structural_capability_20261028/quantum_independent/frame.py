"""Exact qutrit frame over Q[sqrt(-3)], independent of omega-pair code."""
from fractions import Fraction as Q
import itertools
def z(a=0,b=0):return Q(a),Q(b)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[0],-a[1]
def sub(a,b):return add(a,neg(b))
def mul(a,b):return a[0]*b[0]-3*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def conj(a):return a[0],-a[1]
def scale(a,q):return a[0]*q,a[1]*q
def omega(n):return[z(1),z(Q(-1,2),Q(1,2)),z(Q(-1,2),Q(-1,2))][n%3]
def total(xs):
 a=z()
 for b in xs:a=add(a,b)
 return a
def zeros(n):return[[z()for _ in range(n)]for _ in range(n)]
def eye(n):return[[z(int(i==j))for j in range(n)]for i in range(n)]
def mm(a,b):return[[total(mul(x,y)for x,y in zip(row,col))for col in zip(*b)]for row in a]
def trace(a):return total(a[i][i]for i in range(len(a)))
def linear_combination(weights,matrices):
 n=len(matrices[0]);return[[total(scale(m[i][j],w)for w,m in zip(weights,matrices))for j in range(n)]for i in range(n)]
def sic(a,b):
 v=[z()for _ in range(3)];v[(a+1)%3]=z(1);v[(a+2)%3]=neg(omega(-b))
 return[[scale(mul(x,conj(y)),Q(1,2))for y in v]for x in v]
def bell(a,b):
 ans=zeros(9)
 for i in range(3):
  for j in range(3):ans[3*i+(i+a)%3][3*j+(j+a)%3]=scale(omega(b*(i-j)),Q(1,3))
 return ans
SICS=[sic(a,b)for a in range(3)for b in range(3)]
BELLS=[bell(a,b)for a in range(3)for b in range(3)]
def determinant3(a):
 value=z()
 for perm in itertools.permutations(range(3)):
  sign=(-1)**sum(perm[i]>perm[j]for i in range(3)for j in range(i+1,3))
  product=z(1)
  for i,j in enumerate(perm):product=mul(product,a[i][j])
  value=add(value,scale(product,sign))
 return value
