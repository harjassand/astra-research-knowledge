"""Actual memory-source simulation with record-only certified compressed updates."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import numpy as np,json,time,sys
from fractions import Fraction as F
from certified_projection_v1 import *
HERE=Path(__file__).parent;OLD=HERE.parent/'compact_prequential_flag_recovery_20261028'
# Import only the unchanged source/preparation/readout functions, without executing
# or rewriting the old uncertified diagnostic.
src=(OLD/'quantum_memory_fixture_v1.py').read_text().split('max_grad=0;')[0]
src=src.replace('from check_compressed_projection_v1 import project','')
ns={};exec(compile(src,str(OLD/'quantum_memory_fixture_v1.py'),'exec'),ns)
emit=ns['emit'];memory_after=ns['memory_after'];pa=ns['pa'];resource=ns['resource'];phi=ns['phi']
N=int(sys.argv[1]) if len(sys.argv)>1 else 64
assert isqrt(N)**2==N
xi=F(1,256*N*N);step=F(1,isqrt(N));A=16
certs=[];runs=[];records=[];start=time.time()
for seed in [7301,7302,7303]:
 rng=np.random.default_rng(seed);mem=np.array([[.5,.5],[.5,.5]],complex)
 known=[];E=[[F(1),F(0),F(0),F(0)]];K=A
 total=0.;identity=0.;term=int(rng.integers(1,N+1));terminal=None
 for t in range(1,N+1):
  rho,rdg,blocks,sig=emit(mem)
  M=np.zeros((A,2,2),complex)
  for j,k in enumerate(known):M[k]=matrix(E[j])
  if K:
   for k in set(range(A))-set(known):M[k]=matrix(scale(F(1,K),E[-1]))
  score=float(np.einsum('xij,xji->',M,sig).real);total+=score;identity+=float(np.trace(sig[0]).real)
  if t==term:terminal=float(np.vdot(phi,resource(rdg,M)@phi).real);assert abs(terminal-score)<1e-12
  probs=np.trace(sig,axis1=1,axis2=2).real;probs=np.maximum(probs,0);probs/=sum(probs)
  x=int(rng.choice(A,p=probs));wi=int(rng.integers(4));W=pa[wi]
  if wi==0:b=1
  else:
   plus=float(np.trace(memory_after(blocks[x],W,1)).real)/probs[x]
   b=1 if rng.random()<min(1,max(0,plus)) else -1
  memnew=memory_after(blocks[x],W,b);mem=memnew/np.trace(memnew).real
  records.append([seed,t,x,wi,b])
  # The entire learner input consists ONLY of (x,wi,b), N and known A.
  if x not in known:
   default=E.pop();new=scale(F(1,K),default);K-=1
   E.append(new);known.append(x)
   if K:E.append(scale(F(K,K+1),default))
  Y=[e[:] for e in E];Y[known.index(x)][wi]+=step*b
  mult=[1]*len(known)+([K] if K else [])
  E,certificate=project_certified(Y,mult,xi)
  certificate.update(seed=seed,t=t);certs.append(certificate)
 runs.append({'seed':seed,'N':N,'private_terminal_T':term,'terminal_resource_score':terminal,'average_learned_score':total/N,'average_identity_score':identity/N,'distinct_labels_seen':len(known)})
 print('run',seed,'done',time.time()-start,flush=True)
old=np.load(OLD/'quantum_memory_records_v1.npy')
out={'status':'ALL_STEPS_EXACT_RATIONAL_FEASIBLE_AND_GAP_CERTIFIED','N':N,'xi':str(xi),'source_calls_simulated':3*N,'certified_projection_steps':len(certs),'max_certified_gap':max(c['gap_float'] for c in certs),'maximum_dykstra_iterations':max(c['iterations'] for c in certs),'elapsed_seconds':time.time()-start,'runs':runs,'same_records_as_old_N64':bool(np.array_equal(old,np.array(records))) if N==64 else None,'scope':'Floating physical-source simulation; learner feasibility and objective gaps exact rational. No hardware acquisition, nonvacuous regret, expected occupation optimum or arbitrary flag-dimension solver claimed.'}
(HERE/f'memory_summary_N{N}_v1.json').write_text(json.dumps(out,indent=2)+'\n')
(HERE/f'memory_certificates_N{N}_v1.json').write_text(json.dumps(certs,separators=(',',':'))+'\n')
np.save(HERE/f'memory_records_N{N}_v1.npy',np.array(records,dtype=np.int64))
print(json.dumps(out,indent=2))
