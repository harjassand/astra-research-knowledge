import numpy as np, json
from pathlib import Path
I=np.eye(2); X=np.array([[0,1],[1,0]],complex); Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1,-1])
def tensor(mats):
    out=np.array([[1.]])
    for a in mats: out=np.kron(out,a)
    return out
def local(n,i,a): return tensor([a if j==i else I for j in range(n)])
fixtures=[]
for n in (4,6):
    phases=[]
    for b in range(2**n):
        bits=[(b>>(n-1-i))&1 for i in range(n)]
        phases.append((-1)**sum(bits[i]*bits[(i+1)%n] for i in range(n)))
    U=np.diag(phases)
    for theta in (0.,.2,.8):
        r=.65
        tau=(I+r*(np.cos(theta)*X+np.sin(theta)*Y))/2
        rho0=tensor([tau]*n); rho=U@rho0@U
        qs=[local(n,i,np.cos(theta)*X+np.sin(theta)*Y) for i in range(n)]
        terms=[U@q@U for q in qs]
        marg=max(abs(np.trace(rho@local(n,i,p))) for i in range(n) for p in (X,Y,Z))
        comm=max(np.linalg.norm(a@b-b@a) for a in terms for b in terms)
        h=-sum(terms); vals,vec=np.linalg.eigh(-np.arctanh(r)*h)
        ex=(vec*np.exp(vals))@vec.conj().T; ex/=np.trace(ex)
        err=np.linalg.norm(ex-rho)
        assert marg<1e-12 and comm<1e-12 and err<1e-12
        fixtures.append(dict(N=n,theta=theta,max_one_site_pauli=float(marg),max_term_commutator=float(comm),gibbs_factorization_error=float(err)))
Path(__file__).with_name('cluster_diagnostics.json').write_text(json.dumps(fixtures,indent=2)+'\n')
print(json.dumps(fixtures,indent=2))
