import sympy as s
n,h=s.symbols('n h', real=True);I=s.I
# Frequencies represented by (a,b) for a*n+b; identities hold away from accidental collisions.
def add(*ds):
 out={}
 for d in ds:
  for k,v in d.items():out[k]=s.expand(out.get(k,0)+v)
 return {k:v for k,v in out.items() if v!=0}
def scale(d,c):return {k:s.expand(c*v) for k,v in d.items()}
def mul(a,b):
 out={}
 for (i,j),v in a.items():
  for (k,l),w in b.items():out[i+k,j+l]=s.expand(out.get((i+k,j+l),0)+v*w)
 return {k:v for k,v in out.items() if v!=0}
def der(d):return {k:s.expand(I*(k[0]*n+k[1])*v) for k,v in d.items()}
def cos(k):return {k:s.Rational(1,2),(-k[0],-k[1]):s.Rational(1,2)}
def sin(k):return {k:1/(2*I),(-k[0],-k[1]):-1/(2*I)}
def dot(a,b):return add(mul(a[0],b[0]),mul(a[1],b[1]))
def det(a,b):return add(mul(a[0],b[1]),scale(mul(a[1],b[0]),-1))
def values(u):
 v=[der(x) for x in u];w=[der(x) for x in v]
 return [s.factor(d.get((0,0),0)) for d in [mul(dot(u,v),dot(v,v)),mul(det(u,v),dot(v,v)),mul(dot(u,u),det(v,w))]]
cases={
 'scalar_resonance':[add(sin((0,1)),scale(cos((1,0)),h),scale(cos((2,1)),h)),{}],
 'det_resonance':[add(sin((0,1)),scale(cos((1,0)),h)),scale(cos((2,1)),h)],
 'circle_highcircle':[add(cos((0,1)),scale(cos((1,0)),h)),add(sin((0,1)),scale(sin((1,0)),h))]
}
for label,u in cases.items():print(label,values(u))

expected={
 'scalar_resonance':[3*h**3*n*(n+1)**2/4,0,0],
 'det_resonance':[0,h**3*n*(n**2+4*n+1)/4,-h**3*(2*n+1)*(3*n**2+2*n+1)/4],
 'circle_highcircle':[0,h**4*n**3+2*h**2*n**2+2*h**2*n+1,h**4*n**3+h**2*(n**3+n**2+n+1)+1]
}
for label,u in cases.items():
 assert all(s.expand(a-b)==0 for a,b in zip(values(u),expected[label]))
 # Every monomial has four input frequencies, each with |b| <= 1.
 assert all(abs(k[1])<=1 for component in u for k in component)
 for N in range(5,13):
  # Collapse modes before multiplying, independently checking ordinary frequencies.
  un=[{(0,a*N+b):v for (a,b),v in component.items()} for component in u]
  assert all(s.expand(a-b.subs(n,N) if hasattr(b,'subs') else a-b)==0
             for a,b in zip(values(un),expected[label]))

# Exact jet-algebra checks of total-derivative identities.
x=s.symbols('x0:4');y=s.symbols('y0:4')
A=s.Matrix([x[0],y[0]]);B=s.Matrix([x[1],y[1]])
C=s.Matrix([x[2],y[2]]);D=s.Matrix([x[3],y[3]])
def determinant(v,w):return v[0]*w[1]-v[1]*w[0]
def Dt(p):return s.expand(sum(s.diff(p,x[j])*x[j+1]+s.diff(p,y[j])*y[j+1] for j in range(3)))
q=A.dot(B)*B.dot(B);r=determinant(A,B)*B.dot(B);t=A.dot(A)*determinant(B,C)
e1=A.dot(A)*B.dot(C);e2=A.dot(B)*A.dot(C)
f2=A.dot(B)*determinant(A,C);f3=A.dot(C)*determinant(A,B)
identities=[
 e1+q-Dt(A.dot(A)*B.dot(B))/2,
 e2+q-Dt(A.dot(B)**2)/2,
 A.dot(A)*A.dot(D)-3*q-Dt(A.dot(A)*A.dot(C)-A.dot(B)**2-A.dot(A)*B.dot(B)/2),
 t-f2+f3,
 f2-(t-r)/2-Dt(A.dot(B)*determinant(A,B))/2,
 f3+(t+r)/2-Dt(A.dot(B)*determinant(A,B))/2,
 A.dot(A)*determinant(A,D)-r+2*t-Dt(A.dot(A)*determinant(A,C)-A.dot(B)*determinant(A,B))
]
assert all(s.expand(v)==0 for v in identities)
print('PASS: exact Fourier tests, integer-frequency cross-checks n=5,...,12, and seven jet identities.')
