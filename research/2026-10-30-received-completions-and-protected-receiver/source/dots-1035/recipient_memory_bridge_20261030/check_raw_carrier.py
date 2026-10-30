import json, itertools
import numpy as np
from scipy.linalg import expm
from scipy.sparse import csr_matrix, kron, eye

# All finite waiting patterns, including stale carrier values abstracted only by WAIT.
rows=[]
for L in range(1,7):
    kappa,nu=1.3,0.7
    b=2.**np.arange(L-1,-1,-1)
    a=2*nu*b[0]/kappa
    weights=np.r_[a,a,b]
    states=list(itertools.product([0,1],repeat=L+2))
    index={x:i for i,x in enumerate(states)}
    Q=np.zeros((len(states),len(states)))
    R=np.array([np.dot(weights,x) for x in states])
    for ix,x in enumerate(states):
        for p in [0,1]:
            if x[p]:
                y=list(x); y[p]=0
                Q[ix,index[tuple(y)]]+=kappa; Q[ix,ix]-=kappa
        for j in range(L):
            value=(x[0] or x[1]) if j==0 else x[1+j]
            if x[2+j]!=value:
                y=list(x); y[2+j]=int(value)
                Q[ix,index[tuple(y)]]+=nu; Q[ix,ix]-=nu
    r=min(kappa,nu)/2
    defect=Q@R+r*R
    worst=float(np.max(defect))
    active=np.flatnonzero(R>0)
    exact=np.linalg.solve(-Q[np.ix_(active,active)],np.ones(len(active)))
    assert worst<1e-10 and min(exact)>0
    rows.append(dict(L=L,states=len(states),max_drift_violation=worst,
                     linear_Rmax=float(max(R)),exact_lifetime_max=float(max(exact)),
                     a0=float(min(weights)/sum(weights))))

# Full quantum pointer/copy algebra, two noncommuting DATA observables on Q,A,
# and actual five-symbol carrier. Dimension 4*3*3*5=180. No pinching of input.
dims=[2,2,3,3,5]
def embed(ops):
    z=csr_matrix([[1.]])
    for i,d in enumerate(dims): z=kron(z,csr_matrix(ops.get(i,np.eye(d))),format='csr')
    return z

def unit(d,a,b):
    q=np.zeros((d,d),complex); q[a,b]=1; return q
X=np.array([[0,1],[1,0]],complex); Z=np.diag([1.,-1.])
Iq=eye(180,format='csr',dtype=complex)
kappa=1.3;nu=.7; a=2*nu/kappa
WQ=embed({2:unit(3,0,0)}); WA=embed({3:unit(3,0,0)})
WC=embed({4:unit(5,0,0)})
R=a*(WQ+WA)+WC
LR=csr_matrix((180,180),dtype=complex)
for data,pointer,O in [(0,2,X),(1,3,Z)]:
    for bit in [0,1]:
        J=np.sqrt(kappa)*embed({data:(np.eye(2)+(-1)**bit*O)/2,
                              pointer:unit(3,bit+1,0)})
        JJ=J.getH()@J
        LR+=J.getH()@R@J-(JJ@R+R@JJ)/2
# Classical copy: pointer source is explicitly measured in its basis.
for q,a_lab in itertools.product(range(3),repeat=2):
    dest=0 if q==0 or a_lab==0 else 1+2*(q-1)+(a_lab-1)
    for old in range(5):
        K=np.sqrt(nu)*embed({2:unit(3,q,q),3:unit(3,a_lab,a_lab),
                            4:unit(5,dest,old)})
        KK=K.getH()@K
        LR+=K.getH()@R@K-(KK@R+R@KK)/2
expected=-kappa*a*(WQ+WA)+nu*(WQ+WA-WQ@WA-WC)
res=float(np.max(np.abs((LR-expected).toarray())))
eig=float(np.linalg.eigvalsh((LR+min(kappa,nu)/2*R).toarray()).max())
assert res<1e-12 and eig<1e-12
out={'waiting_chain':rows,'full_quantum_dimension':180,
     'exact_waiting_algebra_residual':res,'full_operator_drift_maxeig':eig}
print(json.dumps(out,indent=2))
