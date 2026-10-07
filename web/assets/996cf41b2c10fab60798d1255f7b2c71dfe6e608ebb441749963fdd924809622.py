"""Independent exact tensor generator checks; not an SDE sampler."""
from pathlib import Path
import time,json
import sympy as s

start=time.perf_counter()
OUT=Path(__file__).with_suffix('.json')

def basis(d):
    f=[]
    for i in range(d):
        for j in range(i+1,d):
            z=s.zeros(d);z[i,j]=z[j,i]=1;f.append((z,s.Rational(1,4)))
            z=s.zeros(d);z[i,j]=-s.I;z[j,i]=s.I;f.append((z,s.Rational(1,4)))
    for l in range(1,d):
        z=s.zeros(d)
        for i in range(l):z[i,i]=1
        z[l,l]=-l;f.append((z,s.Rational(1,2*l*(l+1))))
    return f

def tensor(seq):
    a=s.ones(1,1)
    for b in seq:a=s.kronecker_product(a,b)
    return a

def exactzero(a):return all(s.expand(x)==0 for x in a)

def dk(rho,n,v):
    a=s.zeros(rho.rows**n)
    for i in range(n):
        seq=[rho]*n;seq[i]=v;a+=tensor(seq)
    return a

def ddk(rho,n,v,w):
    a=s.zeros(rho.rows**n)
    for i in range(n):
        for j in range(n):
            if i!=j:
                seq=[rho]*n;seq[i]=v;seq[j]=w;a+=tensor(seq)
    return a

fixtures=[]
for d,n in [(2,1),(2,2),(3,1),(3,2),(4,1)]:
    fs=basis(d);I=s.eye(d);k=len(fs)
    # Rational full-rank state with off-diagonal imaginary component.
    rho=s.diag(*[s.Rational(i+1,d*(d+1)//2) for i in range(d)])
    rho[0,1]=s.I/s.Integer(100*d);rho[1,0]=-s.I/s.Integer(100*d)
    eps=s.Rational(2,7);eta=s.Rational(1,5)
    B=fs[0][0]/3+fs[-1][0]/5
    weights=[(s.Rational(i+2,i+1))*q for i,(_,q) in enumerate(fs)]
    # Add an axis not belonging to the orthogonal basis; tests cross terms.
    axes=[(f,w) for (f,_),w in zip(fs,weights)]+[(fs[0][0]+fs[-1][0],s.Rational(1,9))]
    def collective(F):return dk(I,n,F)
    Js=[(collective(f),c) for f,c in axes]
    H=eps*sum((c*J*J for J,c in Js),s.zeros(d**n))+eta*collective(B)
    ker=tensor([rho]*n);a=s.zeros(d);V=0;G=s.zeros(d**n)
    Z=s.zeros(d)
    for F,c in axes:
        x=s.trace(rho*F);y=s.trace(rho*F*F)
        v=F*rho+rho*F-2*x*rho;r=-s.I*(F*rho-rho*F)
        a+=eps*c*(n-1)*x*v;Z+=c*F*F
        V+=eps*c*(n*(n-1)*x*x+n*y)
        G+=eps*c*(ddk(rho,n,v,v)-ddk(rho,n,r,r))/4
        assert exactzero(dk(rho,n,v)+2*n*x*ker-(collective(F)*ker+ker*collective(F)))
        assert exactzero(s.I*dk(rho,n,r)-(collective(F)*ker-ker*collective(F)))
    vZ=Z*rho+rho*Z-2*s.trace(rho*Z)*rho
    vB=B*rho+rho*B-2*s.trace(rho*B)*rho
    a+=eps*vZ/2+eta*vB/2;V+=eta*n*s.trace(rho*B)
    G+=dk(rho,n,a)+V*ker
    target=(H*ker+ker*H)/2
    assert exactzero(G-target)
    assert s.expand(V-s.trace(H*ker))==0
    # Exact logdet-generator and quadratic-variation identities.
    inv=rho.inv();linear=s.trace(inv*a);quadratic=0;qv=0
    for F,c in axes:
        x=s.trace(rho*F);v=F*rho+rho*F-2*x*rho;r=-s.I*(F*rho-rho*F)
        quadratic-=eps*c*s.trace(inv*v*inv*v-inv*r*inv*r)/4
        qv+=eps*c*((s.trace(inv*v))**2-(s.trace(inv*r))**2)/2
    xCx=sum((c*s.trace(rho*F)**2 for F,c in axes),s.Integer(0))
    ell_formula=-eps*d*((2*n-1)*xCx+s.trace(rho*Z))-eta*d*s.trace(rho*B)
    assert s.simplify(linear+quadratic-ell_formula)==0
    assert s.simplify(qv-2*eps*d*d*xCx)==0
    # Isotropic principal form via completeness in this normalization.
    for Y,_ in fs:
        Y=Y+fs[-1][0]/7;y=s.trace(rho*Y)
        D=sum((q*((s.trace(Y*(F*rho+rho*F-2*s.trace(rho*F)*rho)))**2-
                  (s.trace(Y*(-s.I*(F*rho-rho*F))))**2) for F,q in fs),s.Integer(0))
        centered=Y-y*I
        assert s.expand(D-2*s.trace(rho*centered*rho*centered))==0
    fixtures.append({'d':d,'N':n,'matrix_dimension':d**n,'cross_axis':True,
        'kernel_generator_exact':True,'potential_exact':True,
        'logdet_drift_exact':True,'logdet_qv_exact':True,
        'isotropic_principal_form_exact':True})

# Check global positive factor square on a rational-square diagonal spectrum.
for d,p in [(2,[s.Rational(9,25),s.Rational(16,25)]),(3,[s.Rational(1,9),s.Rational(4,9),s.Rational(4,9)])]:
    rho=s.diag(*p);root=s.diag(*[s.sqrt(x) for x in p]);I=s.eye(d)
    for Y,_ in basis(d):
        lhs=0
        for F,q in basis(d):
            w=2*(root*F*root-s.trace(rho*F)*rho)
            lhs+=q*s.trace(Y*w)**2
        z=Y-s.trace(rho*Y)*I
        assert s.expand(lhs-2*s.trace(rho*z*rho*z))==0

OUT.write_text(json.dumps({'origin':'c04_s02','fixtures':fixtures,
    'global_factor_checks_d':[2,3],'elapsed_seconds':time.perf_counter()-start,
    'scope':'Exact small tensor identities, not an SDE simulation, sampler, asymptotic test or theorem proof.'},indent=2)+'\n')
print(OUT)
print('seconds',time.perf_counter()-start)
