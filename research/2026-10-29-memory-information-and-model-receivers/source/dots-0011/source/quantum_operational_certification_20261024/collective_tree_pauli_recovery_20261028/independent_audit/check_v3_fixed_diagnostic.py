import numpy as np,math,itertools,json,hashlib,time
from fractions import Fraction as F
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parent;start=time.time()
C=np.array([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]],dtype=np.int64)
N=2**22;n=8;rng=np.random.default_rng(202610282259)
S=np.zeros((n,3),np.int64);SS=np.zeros((n-1,3,3),np.int64);prefix=None
rootlabels=np.array([0]*7+[1,2,3]);steps=np.array([0]*397+[1,2,3])
for offset in range(0,N,16384):
 m=min(16384,N-offset);e=np.zeros((m,n),np.int64);e[:,0]=rootlabels[rng.integers(0,10,size=m)]
 for j in range(1,n):e[:,j]=(e[:,j-1]+steps[rng.integers(0,400,size=m)])%4
 axes=rng.integers(1,4,size=(m,n));sign=rng.integers(0,2,size=(m,n))*2-1
 out=sign*C[axes,e];y=sign*out
 z=np.stack([(axes==a)*y for a in (1,2,3)],axis=2)
 S+=z.sum(axis=0)
 for j in range(n-1):SS[j]+=z[:,j,:].T@z[:,j+1,:]
 if offset+m==2**20:prefix=(S.copy(),SS.copy())
def counts(N,S,SS):
 A=S@C[1:];one=N+3*A;two=np.empty((n-1,4,4),np.int64)
 for j in range(n-1):two[j]=N+3*A[j,:,None]+3*A[j+1,None,:]+9*C[1:].T@SS[j]@C[1:]
 return one,two
one,two=counts(N,S,SS);saved=np.load(R/'sufficient_counts_v3.npz')
assert np.array_equal(one,saved['one']) and np.array_equal(two,saved['two'])
pone,ptwo=counts(2**20,*prefix);old=np.load(R/'sufficient_counts_v2.npz')
assert np.array_equal(pone,old['one']) and np.array_equal(ptwo,old['two'])
delta=F(1,400);clip=lambda a:max(F(0),min(F(1),a))
L=[[clip(F(int(v),4*N)-delta) for v in row] for row in one];U=[[clip(F(int(v),4*N)+delta) for v in row] for row in one]
EL=[[[clip(F(int(v),16*N)-delta) for v in row] for row in edge] for edge in two]
EU=[[[clip(F(int(v),16*N)+delta) for v in row] for row in edge] for edge in two]
def factors(nodes,edges,poly):
 return [[[edges[j][a][b]*math.prod(nodes[j][c] for c in range(4) if c!=a) if poly else edges[j][a][b]/nodes[j][a] for b in range(4)] for a in range(4)] for j in range(n-1)]
def candidate_score(root,trans,candidate):return root[candidate[0]]*math.prod(trans[j][candidate[j]][candidate[j+1]] for j in range(n-1))
# Backward suffix maximum; competitor is classified by FIRST differing position.
def other_best(root,trans,candidate):
 suffix=[[F(1)]*4 for _ in range(n)]
 for j in reversed(range(n-1)):
  for a in range(4):suffix[j][a]=max(trans[j][a][b]*suffix[j+1][b] for b in range(4))
 choices=[];prefix=F(1)
 for j in range(n):
  for b in range(4):
   if b==candidate[j]:continue
   score=(root[b] if j==0 else prefix*trans[j-1][candidate[j-1]][b])*suffix[j][b]
   choices.append(score)
  prefix=root[candidate[0]] if j==0 else prefix*trans[j-1][candidate[j-1]][candidate[j]]
 return max(choices)
author=json.loads((R/'results_v3.json').read_text());cand=author['candidate']
PL=factors(L,EL,True);PU=factors(U,EU,True)
low=candidate_score(L[0],PL,cand);high=other_best(U[0],PU,cand)
assert low==F(author['division_free_candidate_lower']) and high==F(author['division_free_competitor_upper']) and low>high
# Direct rational probability guard has reversed denominator endpoints and clipping.
TL=[[[EL[j][a][b]/U[j][a] for b in range(4)] for a in range(4)] for j in range(n-1)]
TU=[[[min(F(1),EU[j][a][b]/L[j][a]) for b in range(4)] for a in range(4)] for j in range(n-1)]
assert candidate_score(L[0],TL,cand)==F(author['candidate_probability_lower'])
assert other_best(U[0],TU,cand)==F(author['competitor_upper'])
# Independent exact source probabilities/marginals; strongest actual competitor.
pi=[F(7,10),F(1,10),F(1,10),F(1,10)];T=[[F(397 if a==b else 1,400) for b in range(4)] for a in range(4)]
truth=candidate_score(pi,[T]*7,cand);trueother=other_best(pi,[T]*7,cand);assert truth>trueother
# Estimator identities checked for EVERY true Pauli label and independent axes.
for err in range(4):
 for target in range(4):
  vals=[F(1+3*C[a,target]*C[a,err],4) for a in (1,2,3)]
  assert sum(vals)/3==int(target==err) and set(vals)<=set([F(1),F(-1,2)])
# CPTP decoder global optimum via Kraus Parseval: random channels plus exact sum rule.
P=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
PB=[np.kron(a,b) for a in P for b in P];rng2=np.random.default_rng(619)
max_norm_err=0.;worst_gap=1.
for _ in range(100):
 V=rng2.normal(size=(20,4))+1j*rng2.normal(size=(20,4));V=np.linalg.qr(V)[0];ks=V.reshape(5,4,4)
 q=np.array([sum(abs(np.trace(K@p))**2 for K in ks)/16 for p in PB]);max_norm_err=max(max_norm_err,abs(sum(q)-1))
 prob=rng2.random(16);prob/=sum(prob);score=prob@q;assert score<=max(prob)+1e-14;worst_gap=min(worst_gap,max(prob)-score)
# Exact finite tree identity on a three-leaf star, no division in S(x).
parents=[None,0,0,1];marg=[pi,None,None,None];trans=[None,T,T,T]
for j in range(1,4):marg[j]=[sum(marg[parents[j]][a]*T[a][b] for a in range(4)) for b in range(4)]
edges={j:[[marg[parents[j]][a]*T[a][b] for b in range(4)] for a in range(4)] for j in range(1,4)}
children=[sum(p==j for p in parents[1:]) for j in range(4)];den=math.prod(math.prod(marg[j])**children[j] for j in range(4))
for x in itertools.product(range(4),repeat=4):
 prob=marg[0][x[0]]*math.prod(T[x[parents[j]]][x[j]] for j in range(1,4))
 score=marg[0][x[0]]*math.prod(edges[j][x[parents[j]]][x[j]] for j in range(1,4))*math.prod(math.prod(marg[j][a] for a in range(4) if a!=x[j])**children[j] for j in range(4))
 assert score==den*prob
# Zero-marginal limitation: deterministic root makes all cleared scores vanish.
assert math.prod([F(1),F(0),F(0),F(0)])==0
# Non-tree counterexample: all 1/2-site marginals identical, global mode sets disjoint.
dists=[]
for shift in (0,1):
 d={x:F(int(x[2]==(x[0]+x[1]+shift)%4),16) for x in itertools.product(range(4),repeat=3)};dists.append(d)
for inds in [(0,),(1,),(2,),(0,1),(0,2),(1,2)]:
 for val in itertools.product(range(4),repeat=len(inds)):
  sums=[sum(p for x,p in d.items() if tuple(x[i] for i in inds)==val) for d in dists];assert sums[0]==sums[1]
assert dists[0][(0,0,0)]==F(1,16) and dists[1][(0,0,0)]==0
# Hoeffding bound independently evaluated with finite positive exponential series.
x=F(2*N)*delta**2/F(9,4);series=sum(x**k/math.factorial(k) for k in range(81));failure=F(2*(4*n+16*(n-1)))/series
assert failure==F(author['rigorous_failure_bound'])
out={'status':'independent exact guard, source replay, global-oracle and support checks','records_replayed':N,'native_qubit_exposures_replayed':n*N,'all_one_and_edge_counts_match':True,'v2_is_v3_prefix':True,'division_free_guard_lower':str(low),'division_free_guard_upper':str(high),'true_mode_probability':str(truth),'true_best_other_probability':str(trueother),'fixed_N_failure_bound':str(failure),'Kraus_Parseval_max_error':float(max_norm_err),'zero_support_requires_abstention':True,'non_tree_same_marginal_counterexample':True,'elapsed_seconds':time.time()-start,'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'test_tree_v3.py',R/'sufficient_counts_v3.npz',R/'results_v3.json']}}
(D/'results_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
