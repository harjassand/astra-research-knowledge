"""Exact commutator/circuit diagnostic for the 12-state clean shared-lock fixture."""
from pathlib import Path
import numpy as np,json
p=Path(__file__).parent
ns={};exec((p/'check_guarded_data_blocks_analytic.py').read_text().split('out=[]')[0],ns)
for name in ['n','d','states','ix','P','Ks','killed_gram','hubjump','cp_h','dissip']:
 globals()[name]=ns[name]

def apparatus(eps):
    Hs=[];Jss=[]
    for h in range(2):
        v=hubjump(h,0,1);H=eps*(v+v.conj().T)
        v=hubjump(h,1,2,0,h+1);H+=v+v.conj().T
        js=[np.kron(hubjump(h,1,0),np.eye(d)),np.kron(hubjump(h,3,0,h+1,0),np.eye(d))]
        jt=hubjump(h,2,3);js.extend(np.kron(jt,k) for k in Ks[h])
        for phase in range(4):
            q=np.diag([int(s[h]==phase) for s in states]);js.append(np.sqrt(.7)*np.kron(q,np.eye(d)))
        Hs.append(np.kron(H,np.eye(d)));Jss.append(js)
    def Lh(o,h):
        H=Hs[h];return 1j*(H@o-o@H)+sum(dissip(j,o) for j in Jss[h])
    def L(o):return Lh(o,0)+Lh(o,1)
    return L,Lh

results=[]
for eps in [.2,.1,.05,.025]:
    S,beta,R=killed_gram(eps);L,Lh=apparatus(eps)
    V=np.kron(np.eye(n),P);LV=L(V);first=LV.copy();max_id=0.
    for h in range(2):
        Q=lambda o:cp_h(o,S,h,1.,analytic=True)
        own=Lh(Q(V),h)-Q(Lh(V,h))
        dh=P-sum(k.T@P@k for k in Ks[h])
        guard=np.diag([int(s[1-h]==0) for s in states])
        A=np.diag([int(s[h]==2) for s in states])
        # Isolated terminal C has R_C=1 exactly in this fixture.
        expected=np.kron(guard@(-beta*np.eye(n)+beta*A),dh)
        max_id=max(max_id,float(np.linalg.norm(own-expected,2)))
        first+=.02*eps**2*(L(Q(V)-V)-(Q(LV)-LV))
    t=.02*eps**2
    T=lambda o:cp_h(cp_h(o,S,1,t,analytic=True),S,0,t,analytic=True)
    y=L(T(V));x=y.copy()
    for _ in range(30):x=y-(T(x)-x)
    fixed_res=np.linalg.norm(T(x)-y,2)
    rem=float(np.linalg.norm(x-first,2)/(t*t))
    results.append(dict(epsilon=eps,t=t,own_commutator_identity_error=max_id,effective_remainder_over_t2=rem,inverse_fixed_point_residual=float(fixed_res)))
assert max(r['own_commutator_identity_error'] for r in results)<1e-10
assert max(r['inverse_fixed_point_residual'] for r in results)<1e-10
print(json.dumps({'scope':'Exact finite shared-lock diagnostic only; terminal C is one-dimensional, not full Tanner circuit','all_own_commutator_checks_pass':True,'cases':results},indent=2))
