"""New n=4 random matching survival comparison, same acquired candidate and bath.
Replays the independently reviewed comparator then constructs actual test CP maps.
"""
import runpy,contextlib,io,json,numpy as np
from pathlib import Path
p=Path(__file__).parent
if not (p/'reviewed_fixture_arrays.npz').exists():
 with contextlib.redirect_stdout(io.StringIO()):runpy.run_path(str(p/'independent_review.py'))
a=np.load(p/'reviewed_fixture_arrays.npz');V=a['Vhat'];U=a['Ugood'];E=a['E'];D=16
matchings=[[(0,1),(2,3)],[(0,2),(1,3)],[(0,3),(1,2)]]
states=[]
for M in matchings:
 v=np.zeros(D)
 for x in range(D):
  bits=[(x>>(3-j))&1 for j in range(4)]
  if all(bits[i]!=bits[j] for i,j in M):v[x]=np.prod([1 if bits[i]==0 else -1 for i,j in M])/2
 states.append(V@v)
assert np.linalg.norm(sum(np.outer(v,v.conj()) for v in states)/3-E@E.conj().T/2)<1e-12
def superof(fun):
 return np.stack([fun(z.reshape(2,2)).reshape(-1) for z in np.eye(4)],axis=1)
def ptr(r):return np.einsum('abad->bd',r.reshape(D,2,D,2))
S=[]
for fail in [False,True]:
 def fun(sig):
  out=np.zeros((2,2),complex)
  for v in states:
   P=np.outer(v,v.conj());F=np.eye(D)-P if fail else P;Y=np.kron(F,np.eye(2));out+=ptr(Y@U@np.kron(P,sig)@U.conj().T@Y)/3
  return out
 S.append(superof(fun))
effect=lambda T:(T.conj().T@np.eye(2).reshape(-1)).reshape(2,2)
assert np.linalg.norm(effect(S[0]+S[1])-np.eye(2))<1e-12
slack=float(np.linalg.eigvalsh(2*effect(S[1])-effect(a['bad'])).min());assert slack>-1e-12
# Explicit memory/count recursion, aggregate t+1 bucket preserves accepted bad tail.
def dp(testpass,testfail,s,cap):
 live=np.zeros((155,8,4),complex);live[0,0]=a['sigma'].reshape(-1);acc=np.zeros((8,4),complex);abort=0.;calls=0.
 tr=lambda r:float(r[...,[0,3]].sum().real)
 for r in range(cap):
  calls+=tr(live);gp=s*(live@a['good'].T);bp=s*(live@a['bad'].T);nxt=(1-s)*(live@testpass.T);abort+=(1-s)*tr(live@testfail.T)
  nxt[1:]+=gp[:-1];nxt[1:,1:]+=bp[:-1,:-1];nxt[1:,-1]+=bp[:-1,-1];acc+=gp[-1];acc[1:]+=bp[-1,:-1];acc[-1]+=bp[-1,-1];live=nxt
 return {'accept_probability':tr(acc),'accepted_more_than_6_fault_weight':tr(acc[-1]),'expected_source_calls':calls,'cap_abort':tr(live),'total_mass':tr(acc)+abort+tr(live)}
rows=[]
for name,C,pa,fa,cap in [('matching',2,S[0],S[1],650),('two_design',1.5,a['two_pass'],a['two_fail'],500),('weighted_exact',3,a['weighted_pass'],a['weighted_fail'],800)]:
 rows.append({'test':name,'C':C,'s':1/(C+1),'cap':cap,'result':dp(pa,fa,1/(C+1),cap)})
print(json.dumps({'n':4,'K':2,'same_source':'U0 after the same million-call learned history; no bath reset','R':1,'required_services':155,'t':6,'b':0,'accepted_subnormalized_sound_bound':1/128,'matching_hazard_slack':slack,'results':rows,'scope':'Model-generated float DP, no hardware claim. Matching coefficient general proof independently pending; n4 source effects checked here. Control calibration, routing, encoder/decoder cost excluded from scalar calls.'},indent=2))
np.savez(p/'matching_memory_maps.npz',pass_map=S[0],fail_map=S[1])
