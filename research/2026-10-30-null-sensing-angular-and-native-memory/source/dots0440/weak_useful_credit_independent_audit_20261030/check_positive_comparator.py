"""New coherent positive-comparator test on the author's preserved 12-clock fixture.
The fixture uses direct dephasing and is NOT the actual native monitor apparatus.
Only the comparator algebra is checked here; see the separate actual-monitor test.
"""
from pathlib import Path
source=(Path(__file__).parent/'reviewed_sources/check_guarded_data_blocks_analytic.py').read_text()
exec(source.split('out=[]')[0])
records=[]
for eps in [.1,.05,.025,.0125,.00625]:
 S,beta,R=killed_gram(eps);H=np.zeros((n,n),complex);jumps=[]
 for h in range(2):
  v=hubjump(h,0,1);H+=eps*(v+v.conj().T)
  v=hubjump(h,1,2,0,h+1);H+=v+v.conj().T
  jumps += [np.kron(hubjump(h,1,0),np.eye(d)),np.kron(hubjump(h,3,0,h+1,0),np.eye(d))]
  jt=hubjump(h,2,3);jumps.extend(np.kron(jt,k) for k in Ks[h])
  for phase in range(4):jumps.append(np.sqrt(.7)*np.kron(np.diag([int(s[h]==phase) for s in states]),np.eye(d)))
 HH=np.kron(H,np.eye(d));V=np.kron(np.eye(n),P);t=.1
 T=lambda O:cp_h(cp_h(O,S,1,t,analytic=True),S,0,t,analytic=True)
 F=T(V);LF=1j*(HH@F-F@HH)+sum(dissip(j,F) for j in jumps)
 NN=np.zeros_like(V,dtype=complex)
 for h in range(2):
  other=1-h;guard=np.diag([int(s[other]==0) for s in states]);AT=hubjump(h,2,3).conj().T@hubjump(h,2,3)
  dh=P-sum(k.conj().T@P@k for k in Ks[h])
  charge=np.kron(guard@((1-t*.5)*AT+t*beta*np.eye(n)),dh)
  NN+=cp_h(charge,S,other,t,analytic=True)
 U=[i*d+j for i,s in enumerate(states) if (s[0]!=0)+(s[1]!=0)==1 for j in range(d)]
 RR=(LF+NN)[np.ix_(U,U)];Rherm=(RR+RR.conj().T)/2
 pe=np.kron(np.diag([int(s[0]!=0 and s[1]!=0) for s in states]),np.eye(d))
 records.append({'epsilon':eps,'positive_comparator_min_eig':float(np.linalg.eigvalsh((NN+NN.conj().T)/2)[0]),'U_remainder_norm_over_eps2':float(np.linalg.norm(Rherm,2)/eps**2),'exact_pair_fixed_error':float(np.linalg.norm(T(pe)-pe))})
 assert records[-1]['positive_comparator_min_eig']>-1e-10
 assert records[-1]['exact_pair_fixed_error']<1e-10
print(json.dumps({'scope':'New comparator tested on preserved abstract 12-clock fixture, not native monitor proof','records':records},indent=2))
