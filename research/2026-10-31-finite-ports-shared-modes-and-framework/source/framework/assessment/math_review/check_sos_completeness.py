"""Independent coefficient elimination for the masked result_7535b35 SOS barrier.

Only local SymPy; no imports from author artifacts and no file writes.
Run with python3 -B.  Output is captured beside this file by the reviewer.
"""
import sympy as s
from itertools import combinations, combinations_with_replacement

a,b,c,d = s.symbols('a b c d', real=True)
A=s.Matrix([a,b,c,d]); hv=s.symbols('h0:6', real=True)
h=s.Matrix(hv)
B1=s.Matrix([h[0],h[1],h[3],h[4]])
B2=s.Matrix([h[1],h[2],h[4],h[5]])
T=A.dot(A);D=a*d-b*c
F=3*T*T-4*T*D-4*D*D
X=a+d+s.I*(c-b);Y=a-d+s.I*(c+b)
P=(h[0]-h[2]+2*h[4]+s.I*(h[3]-h[5]-2*h[1]))/4
Q=(h[0]+h[2]+s.I*(h[3]+h[5]))/4
R=(h[0]-h[2]-2*h[4]+s.I*(h[3]-h[5]+2*h[1]))/4
cc=s.conjugate
real=lambda z:s.expand((z+cc(z))/2)
norm=lambda z:s.expand(z*cc(z))
L7=X*Q+2*Y*P
L5=X*R+2*Y*Q
L3=X*cc(R)+2*cc(Y)*P
V=s.Matrix([cc(X)*P+2*cc(Y)*Q,
             Y*cc(R)+X*cc(Q)+cc(Y)*Q,
             X*cc(Q)+2*cc(Y)*Q])
pairs=list(combinations(range(4),2))

def form(degree, name):
    mon=[s.prod(v) for v in combinations_with_replacement(A,degree)]
    coeff=s.symbols(name+':'+str(6*len(mon)), real=True)
    Om=s.zeros(4)
    for row,(i,j) in enumerate(pairs):
        Om[i,j]=sum(coeff[row*len(mon)+k]*m for k,m in enumerate(mon))
        Om[j,i]=-Om[i,j]
    closed=[]
    for i,j,k in combinations(range(4),3):
        expr=s.diff(Om[j,k],A[i])-s.diff(Om[i,k],A[j])+s.diff(Om[i,j],A[k])
        closed.extend(s.Poly(s.expand(expr),*A).coeffs())
    return Om,list(coeff),closed

def density(poly, Om):
    H=s.hessian(poly,A)
    return s.expand(((B1.T*H*B1)[0]+(B2.T*H*B2)[0]+(B1.T*Om*B2)[0])/16)

# All 60 homogeneous quadratic two-form coefficients are free initially.
Om,w,closed=form(2,'w')
l7,l5,l3,g11,g12,g13,g22,g23,g33=s.symbols('l7 l5 l3 g11 g12 g13 g22 g23 g33',real=True)
gg=[l7,l5,l3,g11,g12,g13,g22,g23,g33]
G=s.Matrix([[g11,g12,g13],[g12,g22,g23],[g13,g23,g33]])
rhs=l7*norm(L7)+l5*norm(L5)+l3*norm(L3)+(cc(V).T*G*V)[0]
eqs=s.Poly(s.expand(density(F,Om)-rhs),*A,*h).coeffs()+closed
mat,bb=s.linear_eq_to_matrix(eqs,w+gg)
sol=list(s.linsolve((mat,bb),w+gg))
assert len(sol)==1
derived=sol[0][-len(gg):]
t=1-g22/2;z=g23;r=g33-1+t/2+z
expected=[t/4-z/2,r,t-r,1+s.Rational(5,4)*t-z/2-r,t-z,z-t,2*(1-t),z,1-t/2-z+r]
assert all(s.simplify(u-v)==0 for u,v in zip(derived,expected))
print('PASS: eliminating every closed quadratic two-form gives exactly the reported 3-parameter invariant leading SOS Gram family.')
print('Coefficient-system shape:',mat.shape,'; free Gram parameters:',g22,g23,g33)

# All 24 linear two-form coefficients are free in the cubic matching.
OC,wc,closedc=form(1,'wc')
C=real(cc(X)*Y**2)
e,f,k1,k2,k3=s.symbols('e f k1 k2 k3',real=True)
coupling=2*e*real(L5*cc(P))+2*f*real(L3*cc(Q))+2*real((cc(V).T*s.Matrix([k1,k2,k3]))[0]*R)
eqc=s.Poly(s.expand(density(C,OC)-coupling),*A,*h).coeffs()+closedc
mc,bc=s.linear_eq_to_matrix(eqc,wc+[e,f,k1,k2,k3])
sc=list(s.linsolve((mc,bc),wc+[e,f,k1,k2,k3]))
assert len(sc)==1
assert all(s.simplify(u-v)==0 for u,v in zip(sc[0][-5:],[-k1,1-k3,k1,0,k3]))
print('PASS: complete closed linear cubic matching forces e+k1=0, k2=0, f+k3=1.')

# The dual argument is checked independently as a scalar identity.
t,z,r=s.symbols('t z r',real=True)
G=s.Matrix([[1+s.Rational(5,4)*t-z/2-r,t-z,z-t],
            [t-z,2*(1-t),z],[z-t,z,1-t/2-z+r]])
v=s.Matrix([1-1/s.sqrt(3),(1-1/s.sqrt(3))/2,1])
expr=s.simplify((v.T*(G+s.diag(r,0,t-r))*v)[0])
assert s.simplify(expr-(3-s.sqrt(3)+(s.Rational(5,6)-s.sqrt(3)/2)*t))==0
assert s.Rational(5,6)-s.sqrt(3)/2<0
print('PASS: independent dual scalar identity and strictly negative t coefficient.')
print('For t>=0 this yields nu >= 1/[4(3-sqrt(3))] = (3+sqrt(3))/24 under the SOS Schur/range constraints.')
