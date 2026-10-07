"""Exact rational checks of the noncommuting spectral-loss certificate.
These finite checks are diagnostics, not a proof of the general theorem.
"""
import itertools, json
from pathlib import Path
import sympy as s
R=s.Rational
root=Path(__file__).resolve().parent

def realify(T):
    return T.applyfunc(s.re).row_join(-T.applyfunc(s.im)).col_join(
        T.applyfunc(s.im).row_join(T.applyfunc(s.re)))

def psd_exact(A):
    A=s.simplify((A+A.T)/2)
    ds=[]
    for k in range(1,A.rows+1):
        for inds in itertools.combinations(range(A.rows),k):
            val=s.factor(A.extract(inds,inds).det())
            assert val.is_nonnegative is True, (inds,val)
            ds.append(val)
    return ds

Uin=s.Matrix([[R(3,5),s.I*R(4,5)],[s.I*R(4,5),R(3,5)]])
Uout=s.Matrix([[R(3,5),-R(4,5)],[R(4,5),R(3,5)]])
T=Uout*s.diag(R(1,4),R(1,8))*Uin
assert s.simplify(Uin.H*Uin)==s.eye(2)
L=realify(T); C=L*L.T
n=R(9,16); m=R(15,16)
S=s.diag(1,1,-1,-1)
K0=n*C+m*L*S*L.T
B0=R(16,15)*C
J=s.zeros(4); J[:2,2:]=-s.eye(2); J[2:,:2]=s.eye(2)
assert J*J.T==s.eye(4)
assert C*J==J*C
assert K0*B0!=B0*K0, 'Fixture must be genuinely noncommuting.'
P=[]
for i in range(2):
    pi=s.zeros(4); pi[i,i]=1; pi[i+2,i+2]=1; P.append(pi)

records=[]; check_count=0
for u in [R(0),R(1,4),R(1,2),R(3,4),R(1)]:
    H=K0*(s.eye(4)+u*K0).inv()
    Gamma=-B0+B0*(H+B0).inv()*B0
    Gamma_passive=(Gamma+J*Gamma*J.T)/2
    psd_exact(-Gamma_passive); check_count+=15
    psd_exact(H+B0); check_count+=15
    records.append({'u':str(u),'passive_trace':str(s.factor(s.trace(Gamma_passive)))})

# Test certificate and generator identity after a finite sequence of actual jumps.
v=R(1,2); u=1-v; K=v*K0*(s.eye(4)+u*K0).inv(); B=v*B0
for step in range(3):
    Y=K+B
    psd_exact(Y); check_count+=15
    lambdas=[s.trace(pi*K)/2 for pi in P]
    deltas=[s.simplify(K*pi*K/la) for pi,la in zip(P,lambdas)]
    assert s.simplify(sum((la*dd for la,dd in zip(lambdas,deltas)),s.zeros(4))-K*K)==s.zeros(4)
    check_count+=1
    for la,dd in zip(lambdas,deltas):
        assert la>0
        psd_exact(2*Y-dd); check_count+=15
    phi=s.trace(Y*K*K)
    flow=s.trace((-Y-K*K)*K*K+Y*((-K-K*K)*K+K*(-K-K*K)))
    jump=sum(la*(s.trace((Y+dd)*(K+dd)*(K+dd))-phi) for la,dd in zip(lambdas,deltas))
    remainder=sum(la*(s.trace((Y+2*K)*dd*dd)+s.trace(dd**3)) for la,dd in zip(lambdas,deltas))
    assert s.factor(flow+jump+3*phi-remainder)==0
    assert s.factor(10*s.trace(Y*Y*K*K)-remainder)>=0
    check_count+=2
    records.append({'jump_step':step,'phi':str(s.factor(phi))})
    K=s.simplify(K+deltas[step%2])

S3=s.trace((T.H*T)**3)
assert s.factor(S3)==R(65,262144)
result={'status':'PASS','exact_assertions_or_principal_minors':check_count,
        'fixture':'two-mode rational complex mixing before unequal attenuation and mixing after attenuation',
        'r':'log(2)','n':'9/16','m':'15/16','transmissions':['1/16','1/64'],
        'S3':str(S3),'records':records,
        'scope':'Finite rational checks only; no external validation or formal proof.'}
(root/'exact_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
