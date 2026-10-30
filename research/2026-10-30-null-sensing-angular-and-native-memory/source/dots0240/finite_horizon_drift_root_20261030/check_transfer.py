"""Finite-matrix regression only; does not prove the uniform incidence bound."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
I=np.eye(2); X=np.array([[0,1],[1,0]],complex); Z=np.diag([1,-1]); sm=np.array([[0,1],[0,0]],complex)
def emb(a,j,n=3):
    out=np.array([[1]],complex)
    for k in range(n): out=np.kron(out,a if j==k else I)
    return out
def sop(fun,d):
    out=np.empty((d*d,d*d),complex)
    for j in range(d*d):
        e=np.zeros(d*d,complex); e[j]=1
        out[:,j]=fun(e.reshape(d,d)).reshape(-1)
    return out
def dissip(k,o):
    p=k.conj().T@k
    return k.conj().T@o@k-(p@o+o@p)/2
D=8; id8=np.eye(D); theta=.4
h01=.13*emb(X,0)@emb(Z,1); h12=.11*emb(X,1)@emb(Z,2)
ks=[np.sqrt(.2)*emb(sm,j) for j in range(3)]
L=sop(lambda o:1j*((h01+h12)@o-o@(h01+h12))+sum((dissip(k,o) for k in ks),np.zeros_like(o)),D)
hn=.07*emb(X,1); N=sop(lambda o:1j*(hn@o-o@hn),D)
# All nonempty connected animals on a three-vertex path.
animals=[(0,),(1,),(2,),(0,1),(1,2),(0,1,2)]
a=.1; V=np.zeros((D,D),complex); W=V.copy()
for A in animals:
    f=np.exp(a*len(A))*id8
    for j in A: f=f@emb(np.diag([theta,1]),j)
    V+=f; W+=len(A)*f
# Site incidence: pair Hamiltonian contributions .26+.22, plus onsite jump .4.
J=.88; r=2; q=1; eta=.14; b=k=1
out=[]
for fraction in [.05,.25,.5,.8]:
    t=fraction/(2*J*r*theta**(-k*r))
    E=expm(t*L); Ei=expm(-t*L); M=Ei@N@E
    mv=(M@V.reshape(-1)).reshape(D,D)
    C=b*theta**(-k*q)*(1-fraction)**(-1-q/r)
    upper=C*eta*W
    resid=np.linalg.norm(N@E-E@M,2)
    mineig=np.linalg.eigvalsh((upper-mv+(upper-mv).conj().T)/2).min()
    assert resid<1e-11 and mineig>-1e-10
    out.append(dict(fraction=fraction,t=t,similarity_residual=float(resid),upper_bound_slack=float(mineig)))
# Independent one-qubit damped model: exact averaged observable and noisy drift.
th=.3; kap=.8; T=.2; eps=.01
v=np.diag([th,1.]); f=np.diag([th*T,th*T+(1-th)*(1-np.exp(-kap*T))/kap])
lf=dissip(np.sqrt(kap)*sm,f)
expected=np.diag([0.,-(1-th)*(1-np.exp(-kap*T))])
assert np.linalg.norm(lf-expected)<1e-14
report={'scope':'finite regression, not a native-service theorem','three_site_checks':out,'one_site_exact_average_residual':float(np.linalg.norm(lf-expected))}
Path(__file__).with_name('transfer_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
