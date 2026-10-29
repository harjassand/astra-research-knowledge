import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import sys,json
from pathlib import Path
import numpy as np
BASE=Path(__file__).parent;Q=BASE.parent/'compact_prequential_flag_recovery_20261028'
sys.path.insert(0,str(Q))
exec((Q/'quantum_memory_fixture_v1.py').read_text().split('max_grad=0;')[0],globals())
N=64;out=[];records=[]
for seed in [7301,7302,7303]:
 rng=np.random.default_rng(seed);T=int(rng.integers(1,N+1));mem=np.array([[.5,.5],[.5,.5]],complex)
 M=np.zeros((16,2,2),complex);M[0]=I;lw=np.log([.9,.1]);score=np.zeros(3);ns=ne=0
 for t in range(1,N+1):
  rho,rdg,blocks,sig=emit(mem);pr=np.trace(sig,axis1=1,axis2=2).real;pr/=sum(pr)
  w=np.exp(lw-max(lw));w/=sum(w);p=(1-1/8)*w+np.ones(2)/16
  baseline=float(np.trace(sig[0]).real);learn=float(np.einsum('xij,xji->',M,sig).real);meta=p[0]*baseline+p[1]*learn;score+=[baseline,learn,meta]
  x=int(rng.choice(16,p=pr))
  if rng.random()<.25:
   ns+=1;wi=int(rng.integers(4));W=pa[wi]
   if wi==0:b=1;E=I
   else:
    plus=float(np.trace(memory_after(blocks[x],W,1)).real)/pr[x];b=1 if rng.random()<np.clip(plus,0,1) else -1;E=(I+b*W)/2
   new=memory_after(blocks[x],W,b)
   center=M.copy();center[x]+=8*b*W/(2*2*np.sqrt(N));M,it=project(center,np.ones(16))
   records.append([seed,t,0,x,wi,b,-1,-1])
  else:
   ne+=1;i=int(rng.choice(2,p=p))
   if i==0:z=0;E=I
   else:
    probs=np.array([np.trace(e@sig[x]).real for e in M]);probs=np.maximum(probs,0);probs/=sum(probs);z=int(rng.choice(16,p=probs));E=M[z]
   new=np.einsum('mgnh,hg->mn',blocks[x].reshape(2,2,2,2),E);loss=int(z!=x);lw[i]-=loss/(4*np.sqrt(N)*.75*p[i]);lw-=max(lw)
   records.append([seed,t,1,x,-1,-1,i,z])
  mem=(new+new.conj().T)/2;mem/=np.trace(mem).real
 out.append({'seed':seed,'shadow_calls':ns,'evaluation_calls':ne,'private_terminal_T':T,'path_average_baseline_score':score[0]/N,'path_average_learner_score':score[1]/N,'path_average_meta_score':score[2]/N,'final_meta_weights':(np.exp(lw)/sum(np.exp(lw))).tolist()})
result={'source_calls_simulated':192,'runs':out,'scope':'unchanged negative source but new actual mixed-role occupation; reused seeds not independent evidence; floating diagnostics, no confidence, exact solver or hardware'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');np.save(BASE/'negative_source_meta_records_v1.npy',np.array(records,dtype=np.int64));print(json.dumps(result))
