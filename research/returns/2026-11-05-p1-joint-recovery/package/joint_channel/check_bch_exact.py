"""Exact rational certification of the ordered-triple fourth-order coefficient."""
import sympy as sp
from itertools import product,permutations
from math import factorial
I=sp.I
def swap(n,a,b):
 d=2**n;P=sp.zeros(d)
 for x in range(d):
  y=x if ((x>>(n-1-a))&1)==((x>>(n-1-b))&1) else x^(1<<(n-1-a))^(1<<(n-1-b))
  P[y,x]=1
 return P
P=[swap(4,0,j) for j in range(1,4)]
S=[]
for p in range(5):
 M=sp.zeros(16)
 for a,b,c in product(range(p+1),repeat=3):
  if a+b+c==p:M+=(I**p)*(P[2]**c)*(P[1]**b)*(P[0]**a)/sp.Integer(factorial(a)*factorial(b)*factorial(c))
 S.append(M)
O4=S[4]-(S[1]*S[3]+S[2]**2+S[3]*S[1])/2+(S[1]**2*S[2]+S[1]*S[2]*S[1]+S[2]*S[1]**2)/3-S[1]**4/4
H4=(O4[:8,:8]+O4[8:,8:])/(2*I)
chi=2*I*(swap(3,0,1)*swap(3,1,2)-swap(3,1,2)*swap(3,0,1))
assert H4==chi/8
print('Exact rational identity holds: normalized bus trace of H4 = chi_123 / 8.')
O3=S[3]-(S[1]*S[2]+S[2]*S[1])/2+S[1]**3/3
H3=(O3[:8,:8]+O3[8:,8:])/(2*I)
C=sum((2*swap(3,a,b)-sp.eye(8) for a,b in [(0,1),(0,2),(1,2)]),sp.zeros(8))
assert H3==C/6
print('Exact rational identity holds: normalized bus trace of H3 = sum pair dots / 6.')
