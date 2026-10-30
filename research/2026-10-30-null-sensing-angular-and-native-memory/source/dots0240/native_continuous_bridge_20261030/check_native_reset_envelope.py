import itertools,json,numpy as np
rng=np.random.default_rng(20261030)
R,k,n=3,2,8
theta=1e-4;c=.9;a=c*np.log(1/theta)
D=set(range(R+k));edges={tuple(sorted((i,j))) for i in D for j in D if i<j}
edges|={(4,5),(5,6),(6,7)}
adj=[set() for _ in range(n)]
for i,j in edges:adj[i].add(j);adj[j].add(i)
animals=[]
for mask in range(1,1<<n):
 s={i for i in range(n) if mask>>i&1};seen={next(iter(s))};front=list(seen)
 while front:
  x=front.pop()
  for y in adj[x]&s-seen:seen.add(y);front.append(y)
 if seen==s:animals.append(s)
def VW(data,flag,remote):
 occ=set(i for i in range(R) if flag)
 occ|={R+j for j in range(k) if data>>j&1}
 occ|={R+k+j for j in range(n-R-k) if remote>>j&1}
 vals=np.array([np.exp(a*len(A))*theta**(len(A)-len(A&occ)) for A in animals])
 return np.array([vals.sum(),sum(len(A)*v for A,v in zip(animals,vals))])
def charge(data,remote,weighted):
 occ=set(range(R))|{R+j for j in range(k) if data>>j&1}|{R+k+j for j in range(n-R-k) if remote>>j&1}
 return (1-theta)/2*theta**k*sum((len(A) if weighted else 1)*np.exp(a*len(A))*theta**(len(A)-len(A&occ)) for A in animals if D<=A)
# Intended clean channel clears syndrome bit0, recording its previous value.
# Dirty completion is a random unitary on all remaining input/output dimensions.
dim=16;good_cols=[4*d for d in range(4)];good_rows=[4*(d&2)+(d&1) for d in range(4)]
bad_cols=[i for i in range(dim) if i not in good_cols];bad_rows=[i for i in range(dim) if i not in good_rows]
U=np.zeros((dim,dim),complex)
for col,row in zip(good_cols,good_rows):U[row,col]=1
Q,_=np.linalg.qr(rng.normal(size=(12,12))+1j*rng.normal(size=(12,12)))
U[np.ix_(bad_rows,bad_cols)]=Q
A,_=np.linalg.qr(rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim)))
result={'animals':len(animals),'unitary_error':float(np.linalg.norm(U.conj().T@U-np.eye(dim))), 'terminal_cross_relative_max':0., 'bad_terminal_margin_relative_min':1., 'arbitrary_abort_margin_relative_min':1.,'envelope_charge_ratio_min':float('inf'),'tested_remote_blocks':8,'native_clock_service_claimed':False}
for rem in range(8):
 for weighted in (0,1):
  vals=np.array([VW(d,f,rem)[weighted] for f in (0,1) for d in range(4)])
  dest=np.diag([vals[d] for d in range(4) for w in range(4)])
  src=np.diag([vals[d+(4 if w else 0)] for d in range(4) for w in range(4)])
  eff=U.conj().T@dest@U
  scale=max(vals)
  result['terminal_cross_relative_max']=max(result['terminal_cross_relative_max'],float(np.linalg.norm(eff[np.ix_(good_cols,bad_cols)])/scale))
  loss=src-eff
  charge_diag=np.diag([charge(d,rem,weighted) for d in range(4) for w in range(4)])
  mb=np.linalg.eigvalsh((loss-charge_diag)[np.ix_(bad_cols,bad_cols)])[0]/scale
  result['bad_terminal_margin_relative_min']=min(result['bad_terminal_margin_relative_min'],float(mb))
  src_abort=np.diag([vals[d+4] for d in range(4) for w in range(4)])
  ma=np.linalg.eigvalsh(src_abort-A.conj().T@dest@A-charge_diag)[0]/scale
  result['arbitrary_abort_margin_relative_min']=min(result['arbitrary_abort_margin_relative_min'],float(ma))
  envelope=vals[4]-vals[3]
  for d in range(4):result['envelope_charge_ratio_min']=min(result['envelope_charge_ratio_min'],float(envelope/charge(d,rem,weighted)))
assert result['unitary_error']<1e-12
assert result['terminal_cross_relative_max']<1e-12
assert result['bad_terminal_margin_relative_min']>=-1e-12
assert result['arbitrary_abort_margin_relative_min']>=-1e-12
assert result['envelope_charge_ratio_min']>=1
print(json.dumps(result,indent=2))
