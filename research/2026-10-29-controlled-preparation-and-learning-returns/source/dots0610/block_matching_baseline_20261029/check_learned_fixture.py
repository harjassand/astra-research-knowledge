import numpy as np,json
from pathlib import Path
from check_tensor_baseline import six,product_states,matching_state
P=Path(__file__).parent;a=np.load(P/'received_fixture.npz');E=a['E'];m=2
rows=[]
for source in ['Ugood','Uburst']:
 Ls=[np.kron(D,np.eye(m))@a[source]@np.kron(E,np.eye(m)) for D in a['Ds']]
 for h in [1,2]:
  d=2**h
  if h==1:Ks=Ls
  else:
   first=[];second=[]
   for L in Ls:
    A=np.zeros((8,8),complex);B=A.copy()
    for i,j,k,l,u,v in np.ndindex(2,2,2,2,2,2):
     if j==l:A[(i*2+j)*2+u,(k*2+l)*2+v]=L[i*2+u,k*2+v]
     if i==k:B[(i*2+j)*2+u,(k*2+l)*2+v]=L[j*2+u,l*2+v]
    first.append(A);second.append(B)
   Ks=[B@A for A in first for B in second]
  Bs=[sum(K.reshape(d,m,d,m)[i,:,i,:] for i in range(d))/d for K in Ks]
  H=np.eye(m)-sum(B.conj().T@B for B in Bs)
  states=product_states(six,h);F=np.zeros((m,m),complex)
  for v in states:
   prep=np.kron(v[:,None],np.eye(m));read=np.kron(v.conj()[None,:],np.eye(m))
   mats=[read@K@prep for K in Ks];F+=(np.eye(m)-sum(M.conj().T@M for M in mats))/len(states)
  slack=np.linalg.eigvalsh(1.5*F-H).min();assert slack>-1e-11
  raw_vectors=[a['Vhat']@matching_state(p) for p in [[(0,1),(2,3)],[(0,2),(1,3)],[(0,3),(1,2)]]]
  mats=[np.kron(v.conj()[None,:],np.eye(m))@a[source]@np.kron(v[:,None],np.eye(m)) for v in raw_vectors]
  if h==2:mats=[B@A for A in mats for B in mats]
  Fmatch=np.eye(m)-sum(M.conj().T@M for M in mats)/len(mats)
  matchslack=float(np.linalg.eigvalsh(2*Fmatch-H).min());assert matchslack>-1e-11
  rows.append({'matching_completed_hazard_min_eigenvalue':matchslack,'actual_carried_bath_matching_q':float(np.trace(Fmatch@a['sigma']).real),'source':source,'h':h,'completed_channel_Kraus':len(Ks),'TP_residual':float(np.linalg.norm(sum(K.conj().T@K for K in Ks)-np.eye(d*m))),'product_six_hazard_min_eigenvalue':float(slack),'actual_carried_bath_q':float(np.trace(F@a['sigma']).real),'actual_carried_bath_bad_mass':float(np.trace(H@a['sigma']).real)})
(P/'learned_fixture_results.json').write_text(json.dumps({'scope':'Same frozen learned E, full decoder Ds, Ugood/Uburst and carried bath. h2 applies same joint source successively to two blocks sharing bath, no reset; completed logical channel, not raw physical orbit.','rows':rows},indent=2)+'\n');print(rows)
