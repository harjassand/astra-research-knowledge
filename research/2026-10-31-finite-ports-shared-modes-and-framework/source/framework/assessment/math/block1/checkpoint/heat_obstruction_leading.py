"""Exact impossibility of a polynomial closed-form heat correction for P0.

The symmetry-reduced primitive classes are exhaustive modulo exact 1-forms.
This is an obstruction to this certificate method, NOT to quasiconvexity.
"""
import sympy as S
from itertools import combinations
x,y,u,v=S.symbols('x y u v',real=True);z=S.Matrix([x,y,u,v]);r=x*x+y*y;t=u*u+v*v
F=t*t+2*r*t;C=x*(u*u-v*v)+2*y*u*v;Q=S.Rational(3,16)*(r+t)
h=S.Matrix(S.symbols('h0:6',real=True))
Jx=S.Matrix([h[0]+h[4],h[3]-h[1],h[0]-h[4],h[3]+h[1]]).jacobian(h)
Jy=S.Matrix([h[1]+h[5],h[4]-h[2],h[1]-h[5],h[4]+h[2]]).jacobian(h)
def correction(P):
    W=P.jacobian(z).T-P.jacobian(z);temp=Jx.T*W*Jy
    return S.expand((temp+temp.T)/2)
def heat(f):
    H=S.hessian(f,z);return S.expand(Jx.T*H*Jx+Jy.T*H*Jy)
q0,q1,q2,q3,q4,f,g,j,k=S.symbols('q0 q1 q2 q3 q4 f g j k',real=True)
az=S.Matrix([-y,x,0,0]);aw=S.Matrix([0,0,-v,u]);rw=S.Matrix([0,0,u,v])
PF=q0*r*az+q1*t*az+q2*r*aw+q3*t*aw+q4*r*rw
PC=f*S.Matrix([0,0,x*u+y*v,y*u-x*v])+g*S.Matrix([0,0,x*v-y*u,x*u+y*v])
PQ=S.Matrix([-j*y/2,j*x/2,-k*v/2,k*u/2])
BF=heat(F)+correction(PF);eq=[]
# PSD at all leading acoustic zeros requires annihilation, not merely zero score.
for ox,oy in [(1,0),(0,1),(1,1),(1,-1)]:
    for nx,ny in [(1,0),(0,1),(1,1),(1,-1)]:
        U=S.Matrix([[ox,-oy],[oy,ox]]);V=S.Matrix([[nx,-ny],[ny,nx]]);K=U*S.diag(S.Rational(1,3),1)*V.T
        ac={x:K[0,0]+K[1,1],y:K[1,0]-K[0,1],u:K[0,0]-K[1,1],v:K[1,0]+K[0,1]}
        hh=S.Matrix([ox*nx*nx,ox*nx*ny,ox*ny*ny,oy*nx*nx,oy*nx*ny,oy*ny*ny])
        eq.extend(BF.subs(ac)*hh)
leading=S.solve(eq,[q0,q1,q2,q3,q4],dict=True)[0]
assert leading=={q0:q1/8+S.Rational(3,2),q2:6-q3,q4:0}
B=BF.subs(leading)+heat(C)+correction(PC)+heat(Q)+correction(PQ)
tau=S.symbols('tau',real=True);Astar={x:-S.Rational(1,4),y:tau,u:-tau/2,v:-S.Rational(1,4)}
hstar=S.Matrix([1,-1,1,1,-1,1]);eq=[]
for item in B.subs(Astar)*hstar:eq.extend(S.Poly(S.expand(item),tau).all_coeffs())
necessary=S.solve(eq,[q1,q3,f,g,j,k],dict=True)[0]
assert necessary=={f:0,g:16*j/3+8*k/3+8,q1:-32*j/9+32*k/9+4,q3:64*j/9+8*k/9+12}
B=S.expand(B.subs(necessary))
raw=[((0,0,1,0),[0,5,0,3,0,-2]),((0,0,0,0),[0,-1,0,1,0,-1]),((0,0,1,0),[-3,0,2,0,-5,0])]
constraints=[]
for aa,hh in raw:
    mat=B if aa==(0,0,0,0) else BF.subs(leading).subs(necessary)
    hv=S.Matrix(hh);expression=S.factor((hv.T*mat.subs(dict(zip(z,aa)))*hv)[0]);pp=S.Poly(expression,j,k)
    row=[pp.coeff_monomial(j),pp.coeff_monomial(k),pp.coeff_monomial(1)]
    den=S.ilcm(*(p.q for p in row));row=[S.Integer(p*den) for p in row];gg=S.igcd(*row);row=[p/gg for p in row]
    constraints.append(row)
print('All necessary halfplanes a*j+b*k+c >=0:')
for i,row in enumerate(constraints):print(i,row)
certificate=None
for ids in combinations(range(len(constraints)),3):
    mat=S.Matrix([[constraints[i][0] for i in ids],[constraints[i][1] for i in ids]])
    null=mat.nullspace()
    if len(null)!=1:continue
    weights=null[0]
    if all(a<=0 for a in weights):weights=-weights
    if not all(a>=0 for a in weights):continue
    den=S.ilcm(*(p.q for p in weights));weights=[S.Integer(p*den) for p in weights];gg=S.igcd(*weights);weights=[p/gg for p in weights]
    constant=sum(w*constraints[i][2] for w,i in zip(weights,ids))
    if constant<0:certificate=(ids,weights,constant);break
assert certificate is not None
ids,weights,constant=certificate
assert sum(w*constraints[i][0] for w,i in zip(weights,ids))==0
assert sum(w*constraints[i][1] for w,i in zip(weights,ids))==0
print('Exact Farkas contradiction:',ids,'weights',weights,'weighted constant',constant)
print('No polynomial differential-form heat certificate exists for P0.')
print('This proves no failure of the compatible QC inequality.')
print('leading block',S.simplify(BF.subs(leading).subs(necessary).subs({x:0,y:0,u:1,v:0}).extract([0,2,4],[0,2,4])))
