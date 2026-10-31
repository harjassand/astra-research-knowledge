"""Independent exact checks; never rewrites author fixtures."""
import copy, hashlib, json, random
from pathlib import Path
import sympy as S
import acquire_operator_certificate as a
import test_operator_certificate as t
checks=[]
def ck(name,value):
    assert value,name
    checks.append(name)
s=t.qutrit(); r=a.acquire(s)
# Every integer scientific/metadata leaf rejects bool and float substitution.
def leaves(v,p=()):
    if type(v) is dict:
        for k,x in v.items(): yield from leaves(x,p+(k,))
    elif type(v) is list:
        for k,x in enumerate(v): yield from leaves(x,p+(k,))
    elif type(v) is int: yield p,v
for p,x in leaves(r):
    for replacement in (bool(x),float(x)):
        z=copy.deepcopy(r); cur=z
        for k in p[:-1]:cur=cur[k]
        cur[p[-1]]=replacement
        ck('record alias '+str(p)+' '+str(type(replacement)),not a.verify_certificate(s,z))
# Valid PSD certificate outside DD cone, no LP invocation needed.
s2=t.base([3]); v=S.Matrix([1,2,2])/3; P=v*v.T; Q=S.eye(3)-P
s2['couplings']=[t.coupling('rank2 charge',0,Q)]
s2['generator_terms']=[t.term('zero',[0],S.zeros(3))]
s2['activation_cap']=t.q(1)
dims,Bs,terms,gap,cap,norms=a.parse(s2); Ps,Qs=a.charges(dims,Bs)
r2=a.base_record(s2,dims,Ps,Qs,norms)
r2.update(status='CERTIFIED',reason='EXACT_LOCAL_PSD_AND_GLOBAL_MARGIN',allocations=[{'M':[[t.q(-1)]],'activation':[t.q(1)]}])
ck('exact independent PSD acceptance beyond DD',a.verify_certificate(s2,r2))
co=a.local_coefficients(dims,Qs,terms[0],S.Matrix([[-1]]),[S.Integer(1)])
ck('nonDD coefficient genuinely present',any(any(A[i,i]<sum(abs(S.re(A[i,j]))+abs(S.im(A[i,j])) for j in range(A.cols) if j!=i) for i in range(A.rows)) for A in co.values()))
# Both margins matter even when local weight is identically I.
s3=t.base([2,2]);s3['generator_terms']=[t.term('zero',[0,1],S.zeros(4))]
dims,Bs,terms,gap,cap,norms=a.parse(s3); Ps,Qs=a.charges(dims,Bs)
r3=a.base_record(s3,dims,Ps,Qs,norms);r3.update(status='CERTIFIED',reason='EXACT_LOCAL_PSD_AND_GLOBAL_MARGIN')
for name,M,want in [('both',S.diag(-1,-1),True),('only row',S.Matrix([[-3,2],[0,-1]]),False),('only column',S.Matrix([[-3,0],[2,-1]]),False)]:
    r3['allocations']=[{'M':[[t.q(x) for x in row] for row in M.tolist()],'activation':[t.q(0),t.q(0)]}]
    ck(name+' margin',a.verify_certificate(s3,r3)==want)
# Exact raw complex common-kernel acquisition.
B=S.Matrix([[9,9+9*S.I,-6*S.I],[9-9*S.I,18,-6-6*S.I],[6*S.I,-6+6*S.I,4]])
PP,QQ=a.charges([3],[[B]])
ck("complex raw common kernel",PP[0].trace()==2 and (B*PP[0]).applyfunc(S.simplify)==S.zeros(3))
# Actual known-model acquisition on a complex rotated transparent sector.
v=S.Matrix([-3,-3+3*S.I,2*S.I]); Q=(v*v.H/31).applyfunc(S.expand); P=S.eye(3)-Q
sc=t.base([3]); sc['couplings']=[t.coupling('complex charge',0,Q)]
js=[(S.Rational(1,62),(P[:,j]*v.H).applyfunc(S.expand)) for j in range(3)]
sc['generator_terms']=[t.term('complex loss',[0],S.zeros(3),js)]
rc=a.acquire(sc)
ck('complex actual acquisition',rc['status']=='CERTIFIED' and a.verify_certificate(sc,rc))
# Exact PSD oracle with complex rank deficient Gram matrices.
rng=random.Random(7321)
for k in range(30):
    d=1+k%5; rank=1+k%3
    X=S.Matrix(d,rank,lambda i,j:S.Rational(rng.randrange(-3,4),3)+S.I*S.Rational(rng.randrange(-3,4),5))
    A=(X*X.H).applyfunc(S.expand)
    ck('complex Gram '+str(k),a.psd(A))
    ck('negative diagonal '+str(k),not a.psd(A-S.diag(A[0,0]+1,*([0]*(d-1)))))
# Exact Bernstein reconstruction for mixed degree matrix entries.
u,v=S.symbols('u v',real=True)
F=S.Matrix([[1+u*v+u*u*v*v,S.I*(u-v)**2],[-S.I*(u-v)**2,2+v*v]])
cs=a.bernstein(F,[u,v]); rec=S.zeros(2)
for (i,j),C in cs.items():rec+=S.binomial(2,i)*u**i*(1-u)**(2-i)*S.binomial(2,j)*v**j*(1-v)**(2-j)*C
ck('Bernstein exact matrix reconstruction',(rec-F).applyfunc(S.expand)==S.zeros(2))
# Changed external models cannot be authorized by editing digest alone.
z=copy.deepcopy(s);z['activation_cap']=t.q(0);rr=copy.deepcopy(r);rr['input_sha256']=a.digest(z)
ck('rehashed zero activation does not pass',not a.verify_certificate(z,rr))
for text in ['{"a":1.0}','{"a":NaN}','{"a":1,"a":2}']:
    try:a.load(text)
    except a.InputError: ok=True
    else:ok=False
    ck('JSON rejection '+text,ok)
print(json.dumps({'count':len(checks),'checks':checks,'scope':'exact local checks, no author artifact mutation'},indent=2))
