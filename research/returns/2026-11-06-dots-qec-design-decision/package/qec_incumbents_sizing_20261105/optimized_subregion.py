"""Independent implementation of published subregion MCMC + BAR.
Target distribution is pinned graph product law, not a new model fit.
No imported upstream rare-event package. Diagnostics do not certify mixing.
"""
import sys,json,time,math,argparse,hashlib,resource
from pathlib import Path
import numpy as np,pymatching
from scipy.sparse import csr_matrix
from scipy.special import expit
from scipy.optimize import brentq
from scipy.stats import t as student_t,beta
BASE=Path(__file__).resolve().parent.parent; OUT=Path(__file__).resolve().parent

def model(graph,parameters):
 G=json.loads(Path(graph).read_text()); P=json.loads(Path(parameters).read_text()); n=len(G['edges']); nd=G['internal_vertices'];left=set(G['left']);cut=[];ends=[];match=pymatching.Matching();rr=[];cc=[]
 for i,(u,v) in enumerate(G['edges']):
  ep=[z for z in (u,v) if z<nd];ends.append(ep);rr.extend(ep);cc.extend([i]*len(ep));iscut=u in left or v in left
  if iscut:cut.append(i)
  kw=dict(fault_ids={0} if iscut else set(),weight=G['costs'][i])
  if len(ep)==2:match.add_edge(*ep,**kw)
  else:match.add_boundary_edge(ep[0],**kw)
 H=csr_matrix((np.ones(len(rr),np.uint8),(rr,cc)),shape=(nd,n));q=np.array(P['q_numerators'],float)/2.**64
 ei=np.full((n,2),-1,int)
 for i,ep in enumerate(ends):ei[i,:len(ep)]=ep
 cm=np.zeros(n,np.uint8);cm[cut]=1
 return dict(q=q,n=n,nd=nd,H=H,match=match,cut=np.array(cut),cm=cm,ei=ei)

def synd(m,E):return np.packbits(np.asarray((m['H']@E.T).T,np.uint8)%2,axis=1,bitorder='little')
def fail(m,E,S=None):
 if S is None:S=synd(m,E)
 p=m['match'].decode_batch(S,bit_packed_shots=True,bit_packed_predictions=True)[:,0]&1
 return p^(E[:,m['cut']].sum(1).astype(np.uint8)&1)

def sparse_bernoulli(rng,p):
 # Independent envelope Bernoulli sites via geometric spacings, then thinning.
 n=len(p);v=float(p.max());out=[];offset=-1
 if v==0:return np.empty(0,int)
 while True:
  count=max(32,int((n-offset)*v*1.5)+16)
  x=offset+np.cumsum(rng.geometric(v,size=count));valid=x[x<n]
  out.extend(valid.tolist())
  if len(valid)<len(x):break
  offset=int(x[-1])
 inds=np.array(out,int)
 return inds[rng.random(len(inds))<p[inds]/v]

def ladder(q,scale=8.):
 ts=[math.log(scale)];logit=np.log(q/(1-q))
 while ts[-1]>0:
  qq=expit(logit+ts[-1]);ts.append(max(0.,ts[-1]-.8/math.sqrt(float(np.sum(qq*(1-qq))))))
 return np.array(ts)

def bar(a,b,t1,t2,q):
 w=np.arange(len(a));A=lambda t:float(np.log1p(q*np.expm1(t)).sum());ell=w*(t2-t1)-(A(t2)-A(t1));use=(a+b)>0;offset=math.log(b.sum()/a.sum())
 return float(brentq(lambda r:float(a@expit(ell-r+offset)-b@expit(-ell+r-offset)),float(ell[use].min()-50),float(ell[use].max()+50),xtol=1e-12))

def iat(x):
 y=np.array(x,float);y-=y.mean();n=len(y)
 if not np.any(y):return 1.
 v=np.fft.rfft(y,n=2*n);c=np.fft.irfft(v*v.conj())[:n];c/=c[0];z=1.
 for i in range(1,min(n//2,4000),2):
  s=float(c[i]+c[i+1])
  if s<=0:break
  z+=2*s
 return max(1.,z)

def main():
 p=argparse.ArgumentParser();p.add_argument('--distance',type=int,default=21);p.add_argument('--graph',default=str(BASE/'qec_fault_tuple_20261105/d21/input_graph.json'));p.add_argument('--parameters',default=str(BASE/'qec_fault_tuple_20261105/d21/parameters.json'));p.add_argument('--chains',type=int,default=16);p.add_argument('--burn',type=int,default=2000);p.add_argument('--keep',type=int,default=4000);p.add_argument('--max-seconds',type=float,default=1200);a=p.parse_args()
 start=time.perf_counter();m=model(a.graph,a.parameters);setup=time.perf_counter()-start;q=m['q'];ts=ladder(q);C=a.chains;rho=1/math.ceil(a.distance/2);seed=202611051762+a.distance;rng=np.random.default_rng(seed)
 # Fixed 20k anchor, fresh independent starts separate from anchor count.
 anchstart=time.perf_counter();qq=expit(np.log(q/(1-q))+ts[0]);N=20000;k=0
 for z in range(0,N,128):
  E=(rng.random((min(128,N-z),m['n']))<qq).astype(np.uint8);k+=int(fail(m,E).sum())
 starts=[];ns=0
 while len(starts)<C:
  E=(rng.random((128,m['n']))<qq).astype(np.uint8);fs=fail(m,E);ns+=len(E)
  for e in E[fs.astype(bool)]:
   if len(starts)<C:starts.append(e.copy())
 anchor=dict(shots=N,failures=k,estimate=k/N,nominal_999_CP=[float(beta.ppf(.0005,k,N-k+1)),float(beta.ppf(.9995,k+1,N-k))],separate_start_trials=ns,seconds=time.perf_counter()-anchstart)
 E=np.array(starts);S=synd(m,E);weights=E.sum(1).astype(int);parity=(E[:,m['cut']].sum(1)%2).astype(np.uint8);traces=[];records=[];totaldec=N+ns;totalproposals=0;allseconds=0
 print(json.dumps(dict(anchor=anchor,setup_seconds=setup,rungs=len(ts))),flush=True)
 for j,t0 in enumerate(ts):
  rungstart=time.perf_counter();qq=expit(np.log(q/(1-q))+t0);A=np.empty((C,a.keep),np.uint16);ar=0;changed=0;calls=0
  for it in range(a.burn+a.keep):
   cand=S.copy();diffs=[];pnext=parity.copy();wnext=weights.copy();active=[]
   for c in range(C):
    occ=np.flatnonzero(E[c]);dele=occ[rng.random(len(occ))<rho*(1-qq[occ])];add=sparse_bernoulli(rng,rho*qq);add=add[E[c,add]==0];inds=np.r_[dele,add];diffs.append(inds)
    if len(inds):
     active.append(c);vn=m['ei'][inds].ravel();vn=vn[vn>=0];np.bitwise_xor.at(cand[c],vn//8,(1 << (vn%8)).astype(np.uint8));pnext[c]^=np.bitwise_xor.reduce(m['cm'][inds]);wnext[c]+=len(add)-len(dele)
   if active:
    active=np.array(active);pred=m['match'].decode_batch(cand[active],bit_packed_shots=True,bit_packed_predictions=True)[:,0]&1;accepted=active[(pred^pnext[active]).astype(bool)];calls+=len(active);changed+=len(active);ar+=len(accepted)
    for c in accepted:E[c,diffs[c]]^=1
    S[accepted]=cand[accepted];weights[accepted]=wnext[accepted];parity[accepted]=pnext[accepted]
   if it>=a.burn:A[:,it-a.burn]=weights
  elapsed=time.perf_counter()-rungstart;traces.append(A);allseconds+=elapsed;totaldec+=calls;totalproposals+=C*(a.burn+a.keep)
  W=float(A.astype(float).var(1,ddof=1).mean());B=float(a.keep*A.mean(1).var(ddof=1));R=math.sqrt(((a.keep-1)*W+B)/(a.keep*W));ia=[iat(x) for x in A]
  r=dict(rung=j,tilt=float(t0),mean_weight=float(A.mean()),seconds=elapsed,decoder_calls=calls,acceptance=ar/max(changed,1),Rhat=R,max_IAT=max(ia),maxIAT50_pass=a.keep>=50*max(ia));records.append(r);print(json.dumps(r),flush=True)
  np.savez_compressed(OUT/f'd{a.distance}_optimized_partial.npz',traces=np.array(traces),ladder=ts[:j+1],terminal_states=E)
  (OUT/f'd{a.distance}_optimized_progress.json').write_text(json.dumps(dict(anchor=anchor,rungs=records,elapsed=time.perf_counter()-start),indent=2))
  if time.perf_counter()-start>a.max_seconds:break
 completed=len(traces)==len(ts);out=dict(spec=vars(a),seed=seed,scope='Independent published subregion/BAR equations, not upstream timing. Nominal intervals exclude mixing bias.',graph_sha256=hashlib.sha256(Path(a.graph).read_bytes()).hexdigest(),parameters_sha256=hashlib.sha256(Path(a.parameters).read_bytes()).hexdigest(),anchor=anchor,rungs=records,complete=completed,total_seconds=time.perf_counter()-start,setup_seconds=setup,total_proposals=totalproposals,total_decoder_calls=totaldec,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 if completed:
  H=np.array([[np.bincount(x,minlength=m['n']+1) for x in rung] for rung in traces]);pooled=[bar(H[j].sum(0),H[j+1].sum(0),ts[j],ts[j+1],q) for j in range(len(ts)-1)];logs=np.array([[bar(H[j,c],H[j+1,c],ts[j],ts[j+1],q) for j in range(len(ts)-1)] for c in range(C)]).sum(1);point=math.exp(math.log(k/N)+sum(pooled));se=math.hypot(float(logs.std(ddof=1)/math.sqrt(C)),math.sqrt((1-k/N)/k));delta=float(student_t.ppf(.9995,C-1))*se
  out.update(point=point,nominal_999_interval=[point*math.exp(-delta),point*math.exp(delta)],log_standard_error=se,per_chain_log_ratios=logs.tolist(),log_ratios=pooled)
 (OUT/f'd{a.distance}_optimized_result.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k not in ['rungs','per_chain_log_ratios','log_ratios']}),flush=True)
if __name__=='__main__':main()
