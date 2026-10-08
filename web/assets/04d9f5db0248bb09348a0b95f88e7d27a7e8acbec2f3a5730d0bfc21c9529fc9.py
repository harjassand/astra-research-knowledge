"""Bounded exact checks of identities in the independent all-d proof."""
from pathlib import Path
import hashlib
import json
import sympy as s

d=s.symbols('d',positive=True,integer=True)
a,b,u=s.symbols('a b u',real=True)
mA=d*(d-1)/2;mS=(d-1)*(d+2)/2
r0=(2+d*(d-1)*a+(d-1)*(d+2)*b)/(2*d**2)
rA=(2+d*a-(d+2)*b)/(2*d**2)
rS=(2-d*a+(d-2)*b)/(2*d**2)
assert s.simplify(r0+mA*rA+mS*rS-1)==0
assert s.simplify(a-(r0+mA*rA/(d-1)-mS*rS/(d-1)))==0
assert s.simplify(b-(r0-mA*rA/(d-1)+mS*rS*(d-2)/((d-1)*(d+2))))==0

G=s.Matrix([[1,1/d,1/d],[1/d,1,1/d],[1/d,1/d,1]])
T=s.Matrix([[d-1,1,0],[1,d-1,0],[-1,-1,0]])
assert (G*T-T.T*G).applyfunc(s.simplify)==s.zeros(3)
for vector,value in [(s.Matrix([1,1,-2/d]),d),
                     (s.Matrix([1,-1,0]),d-2),(s.Matrix([0,0,1]),0)]:
    assert (T*vector-value*vector).applyfunc(s.simplify)==s.zeros(3,1)
t=s.symbols('t')
assert s.expand(T.charpoly(t).as_expr()-t*(t-d)*(t-d+2))==0

alpha=4*u*(1-u)/(d-1)
beta=(2-d*alpha)/(d+2)
assert s.simplify(1+mA*alpha+mS*beta-d)==0
assert s.simplify(d*(2*u*(1-u))/mA-alpha)==0
beta_low=2/(d+2)
beta_high=(2-d*(2*a-1))/(d+2)
assert s.simplify(beta_low-(2*b-1)
                  -(2*(2+d*a-(d+2)*b)+d*(1-2*a))/(d+2))==0
assert s.simplify(beta_high-(2*b-1)
                  -2*((d+2)-d*a-(d+2)*b)/(d+2))==0
N=d**2-1
assert s.simplify(1+N*(N+3)/2-d**2*(d**2+1)/2)==0
lam=(d+2)/(2*(d+1))
assert s.simplify((d**2-d)/(d**2-1-(d**2-1)*lam)-2)==0

# Two exact finite matrix instances audit the indexed star identity,
# including the O(4) antisymmetric-representation edge case. No sweep.
instances=[]
for dim in [3,4]:
    I=s.eye(dim);size=dim**3
    omega_vec=s.Matrix([int(i==j) for i in range(dim) for j in range(dim)])/s.sqrt(dim)
    omega=omega_vec*omega_vec.T
    P=s.kronecker_product(omega,I)
    Q=s.zeros(size)
    vecs=[]
    for k in range(dim):
        ui=s.zeros(size,1);vi=s.zeros(size,1);wi=s.zeros(size,1)
        for i in range(dim):
            ui[dim**2*i+dim*i+k]=1/s.sqrt(dim)
            vi[dim**2*i+dim*k+i]=1/s.sqrt(dim)
            wi[dim**2*k+dim*i+i]=1/s.sqrt(dim)
        Q+=vi*vi.T
        vecs.append((ui,vi,wi))
    F_ab=s.Matrix(size,size,lambda ijk,lmn:
        int(ijk//dim**2==(lmn//dim)%dim
            and (ijk//dim)%dim==lmn//dim**2 and ijk%dim==lmn%dim))
    F_ac=s.Matrix(size,size,lambda ijk,lmn:
        int(ijk//dim**2==lmn%dim and (ijk//dim)%dim==(lmn//dim)%dim
            and ijk%dim==lmn//dim**2))
    W=s.zeros(size)
    for i in range(dim):
        for j in range(i+1,dim):
            ji=s.zeros(dim);ji[i,j]=-s.I;ji[j,i]=s.I
            W+=s.kronecker_product(ji.T,ji,I)+s.kronecker_product(ji.T,I,ji)
    assert W==dim*(P+Q)-F_ab-F_ac
    for ui,vi,wi in vecs:
        assert W*ui==(dim-1)*ui+vi-wi
        assert W*vi==ui+(dim-1)*vi-wi
        assert W*wi==s.zeros(size,1)
    instances.append({'dimension':dim,'full_matrix_size':size,'status':'PASS'})

out={'status':'PASS','scope':'exact identity audits, not quantified theorem certification',
     'symbolic_star_block_polynomial':str(s.factor(T.charpoly(t).as_expr())),
     'finite_star_instances':instances,'finite_support_bound':'d^2(d^2+1)/2',
     'd2_naive_formula_failure':{'a':-1,'b':0,'naive_alpha':0,'required_alpha':1},
     'proof_sha256':hashlib.sha256(Path(__file__).with_name('ALL_D_THEOREM_FIRST_BASELINE.txt').read_bytes()).hexdigest()}
Path(__file__).with_name('ALL_D_EXACT_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
