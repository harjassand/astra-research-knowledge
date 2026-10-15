"""Exact sharp-floor acoustic geometry; no optimizer or source mutation."""
import sympy as s
from itertools import combinations, combinations_with_replacement as cwr

r,t,p,q=s.symbols('r t p q', real=True)
x=s.Matrix(s.symbols('a b c d',real=True));a,b,c,d=x
z=s.Matrix(s.symbols('z0:6',real=True))
u=a*a+c*c;v=b*b+d*d;j=a*d-b*c
H=(u+v-2*j)**2
alpha_star=3*r/(8*(r+2))
F=alpha_star*H+r*(r-1)*u*u/6+j*j+r*u*j
B1=s.Matrix([z[0],z[1],z[3],z[4]])
B2=s.Matrix([z[1],z[2],z[4],z[5]])
Z=s.kronecker_product(x,z)
R=s.Matrix([[p,-q],[q,p]])

def rankone_jet(target,xi):
    n,m=xi
    return s.Matrix([target[0]*n*n,target[0]*n*m,target[0]*m*m,
                     target[1]*n*n,target[1]*n*m,target[1]*m*m])

def kernel_curve(A,xi):
    AA=R*A
    zz=rankone_jet(R[:,0],xi)
    ZZ=s.kronecker_product(s.Matrix(list(AA)),zz)
    out=[]
    for order in [0,1]:
        vv=ZZ.diff(t,order).subs(t,0)
        for mon in [p*p,p*q,q*q]:
            out.append(s.Matrix([s.Poly(vi,p,q).coeff_monomial(mon) for vi in vv]))
    return out

old_A=s.Matrix([[1,-(r+1)*t],[(r+1)*t,1]])
new_A=s.Matrix([[-3*(r+1)*t/(2*r+1),(2*r+1)/3],[1,(r+1)*t]])
Kold=s.Matrix.hstack(*kernel_curve(old_A,(t,1)))
Knew=s.Matrix.hstack(*kernel_curve(new_A,(1,t)))
K=Kold.row_join(Knew)

def acoustic(A,xi):
    rr=s.Matrix([xi[0],xi[1],0,0])
    pol=(rr.T*s.hessian(F,x)*rr)[0]
    return s.factor(pol.subs(dict(zip(x,list(A)))))

def verify():
    assert acoustic(old_A,(t,1)) == s.Rational(2,3)*r*(r+1)**2*(r+2)*t**4
    assert acoustic(new_A,(1,t)) == 6*r*(r+1)**2*(r+2)*t**4/(2*r+1)**2
    n,m=s.symbols('n m',real=True)
    rr=s.Matrix([n,m,0,0]);pol=(rr.T*s.hessian(F,x)*rr)[0]
    MM=s.simplify(s.hessian(pol,x)/2)
    assert s.factor(MM.det())==9*m**4*n**4*r**4
    print('old rank',Kold.rank(),'new rank',Knew.rank(),'combined rank',K.rank(),flush=True)
    print('combined pivot rows',K.T.rref()[1],flush=True)
    return MM

if __name__=='__main__':
    verify()
