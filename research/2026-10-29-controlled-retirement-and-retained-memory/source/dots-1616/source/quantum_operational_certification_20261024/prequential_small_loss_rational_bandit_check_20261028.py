"""Deterministic physical-bandit/certified-prox fixture; ZERO source samples.

Floating Newton iterates are proposals only. Every reported action, estimator
identity, PSD/TP condition and prox certificate is checked in exact rationals.
This is not an execution or timing test of the theorem's bounded weak solver.
"""
import hashlib,itertools,json
from pathlib import Path
import numpy as np
import sympy as s

I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]])
Z=s.diag(1,-1); S=s.diag(1,s.I); P=[I,X,Y,Z]; axes=[X,Y,Z]
kron=s.kronecker_product; d=2;k=4;D=12
E=[kron(a,b) for a in axes for b in P]
C0=s.eye(k)/k
theta=s.zeros(D,1); theta[0]=s.Rational(1,128)
theta[7]=s.Rational(1,160);theta[9]=s.Rational(1,192)
def matrix(t):
    c=C0.copy()
    for x,e in zip(t,E): c+=x*e
    return c
def pos(c):
    assert c==c.H
    assert all(c[:j,:j].det()>0 for j in range(1,c.rows+1))
def tp(c):
    assert c[:2,:2]+c[2:,2:]==I/2
def grad(c):
    inv=c.inv()
    return s.Matrix([-s.simplify(s.trace(inv*e)) for e in E])
def hess(c):
    inv=c.inv();return s.Matrix(D,D,lambda a,b:s.simplify(s.trace(inv*E[a]*inv*E[b])))
C=matrix(theta);pos(C);tp(C);H=hess(C)
V=s.eye(D)/10
for a in range(D-1): V[a,a+1]=s.Rational(1,1000)
B=V.T*H*V
pos(B-s.eye(D)/2);pos(s.eye(D)-B)
U=V.inv().T;Hinv=H.inv()
assert U*V.T==s.eye(D)

def decoder(c,r):
    t=d*c*kron(I,r.T)
    return s.Matrix(2,2,lambda a,b:sum(t[2*a+x,2*b+x] for x in range(2)))
K0=s.diag(1,s.Rational(3,5));K1=s.Matrix([[0,s.Rational(4,5)],[0,0]])
channels=[lambda r:r,lambda r:S*(K0*r*K0.H+K1*r*K1.H)*S.H]
gradient_checks=0;variance_checks=0;bit_laws=0
for channel in channels:
    T=s.zeros(4)
    for axis in axes:
      for sign in (-1,1):
        r=channel((I+sign*axis)/2)
        T+=kron((I-sign*axis)/2,r.T)/6
    truegrad=s.Matrix([d*s.trace(e*T) for e in E])
    qcenter=s.simplify(d*s.trace(C*T))
    estimator=s.zeros(D,1);second=0;meanloss=0
    for i in range(D):
      for z in (-1,1):
        played=matrix(theta+z*V[:,i]/2)
        pos(played);tp(played)
        q=s.simplify(d*s.trace(played*T)); assert 0<=q<=1
        actual=0
        for axis in axes:
          for sign in (-1,1):
            r=channel((I+sign*axis)/2)
            actual+=s.trace((I-sign*axis)*decoder(played,r))/12
        assert s.simplify(actual-q)==0
        # Explicitly average the two physical return counts y=0,1.
        for y,prob in ((0,1-q),(1,q)):
            g=2*D*y*z*U[:,i]
            estimator+=prob*g/(2*D)
            norm=(g.T*Hinv*g)[0]
            assert norm<=8*D*D*y
            second+=prob*norm/(2*D)
            meanloss+=prob*y/(2*D)
            bit_laws+=1
    assert s.simplify(estimator-truegrad)==s.zeros(D,1)
    assert s.simplify(meanloss-qcenter)==0
    assert second<=8*D*D*qcenter
    gradient_checks+=1;variance_checks+=1

# Known-matrix Newton proposals; accepted only by exact rational certificates.
en=np.array([np.array(e.tolist(),dtype=complex) for e in E])
cn=np.eye(k)/k
base=np.array(theta,dtype=float).reshape(-1)
gamma=s.Rational(1,2);epsilon=s.Rational(1,8)
eta=gamma/(64*D*D);delta=eta*epsilon/64
basegrad=np.array(grad(C),dtype=complex).real.reshape(-1)
certificates=[]
for i,z in ((0,-1),(0,1),(3,-1),(3,1),(11,-1),(11,1)):
    g=2*D*z*U[:,i]
    gnp=np.array(g,dtype=float).reshape(-1)
    point=base.copy()
    for iteration in range(8):
        c=cn+np.einsum('a,aij->ij',point,en)
        inv=np.linalg.inv(c)
        gg=-np.einsum('ij,aji->a',inv,en).real
        hh=np.array([[np.trace(inv@a@inv@b).real for b in en] for a in en])
        residual=float(eta)*gnp+gg-basegrad
        point-=np.linalg.solve(hh,residual)
    den=2**48
    rational=s.Matrix([s.Rational(int(round(x*den)),den) for x in point])
    result=matrix(rational);pos(result);tp(result)
    step=rational-theta
    radius=(step.T*H*step)[0]
    rr=eta*g+grad(result)-grad(C)
    residual=(rr.T*rr)[0]
    assert radius<=s.Rational(1,4)
    assert residual<=delta**2
    certificates.append({'direction':i,'sign':z,'newton_proposal_steps':8,
      'exact_radius_squared_below_1_4':True,
      'exact_tangent_residual_squared_below_delta_squared':True,
      'dyadic_denominator_bits':48})

caps=[]
for dd,ee,gg in itertools.product((2,4,8),(s.Rational(1,2),s.Rational(1,8)),(s.Rational(1,2),s.Rational(1,8))):
    DD=3*dd*dd;kk=2*dd
    L0=next(l for l in range(1,100) if 2**l>=16/ee)
    target=512*DD*DD*kk*L0/(gg*ee)
    NN=1
    while NN<target:NN*=2
    assert NN<1024*DD*DD*kk*L0/(gg*ee)
    eta0=gg/(64*DD*DD)
    assert kk*L0/(eta0*NN)<=ee/8
    assert 1/(1-gg/8)<=1+gg/7
    assert (ee/16+ee/8+ee/64)/(1-gg/8)*s.Rational(3,2)<=39*ee/112
    caps.append({'d':dd,'epsilon':str(ee),'gamma':str(gg),'N':NN})

path=Path(__file__)
result={'status':'PASS_EXACT_CERTIFICATES_WITH_FLOATING_PROPOSALS_ONLY',
 'source_calls':0,'rng_draws':0,'hardware_executions':0,
 'physical_output_dimension':d,'affine_choi_dimension':D,
 'rational_nonorthogonal_whitening':'exact half-I and I Loewner certificates',
 'exact_action_return_bit_laws':bit_laws,
 'exact_unbiased_gradient_checks':gradient_checks,
 'exact_loss_dependent_variance_checks':variance_checks,
 'exact_rational_prox_certificates':certificates,
 'finite_cap_checks':caps,
 'not_claimed':['sampled learner','production convex solver runtime','all-process proof from finite fixtures'],
 'script_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
path.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
