"""Independent published-equation kernels; no upstream software executed."""
import sys,json,time,math,hashlib,argparse,resource
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
from scipy.special import expit
from scipy.optimize import brentq
from scipy.stats import t as student_t,beta
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'canonical_qec_circuit_gate_20261105'))
from tilted_pilot import CircuitModel

def acquire():
 G=json.loads((ROOT.parent/'qec_fault_tuple_20261105/d21/input_graph.json').read_text());params=json.loads((ROOT.parent/'qec_fault_tuple_20261105/d21/parameters.json').read_text())
 m=CircuitModel(G);m.q=np.array(params['q_numerators'],dtype=float)/2.**64;m.n=len(m.edges);m.cutarr=np.array(m.cut);m.cutmask=np.zeros(m.n,np.uint8);m.cutmask[m.cut]=1
 rr=[];cc=[]
 for i,x in enumerate(m.edge_checks):rr.extend(x);cc.extend([i]*len(x))
 m.H=csr_matrix((np.ones(len(rr),np.uint8),(rr,cc)),shape=(len(m.checks),m.n));m.cache={};m.calls=0;m.cachehits=0
 return m

def failure(m,e,s=None):
 if s is None:s=np.asarray(m.H@e,dtype=np.uint8)%2
 key=s.tobytes()
 if key in m.cache:v=m.cache[key];m.cachehits+=1
 else:
  c=m.m.decode(s);v=int(c[m.cutarr].sum())%2;m.calls+=1
  if len(m.cache)>=16384:m.cache.clear()
  m.cache[key]=v
 return (int(e[m.cutarr].sum())%2)^v

def ladder(q):
 ts=[math.log(8)];logit=np.log(q/(1-q))
 while ts[-1]>0:
  qq=expit(logit+ts[-1]);ts.append(max(0.,ts[-1]-.8/math.sqrt(float(np.sum(qq*(1-qq))))))
 return ts

def anchor():
 begin=time.perf_counter();m=acquire();setup=time.perf_counter()-begin;rng=np.random.default_rng(202611054401);q=expit(np.log(m.q/(1-m.q))+math.log(8));N=10000;count=0;starts=[];ts=time.perf_counter()
 for z in range(0,N,128):
  es=(rng.random((min(128,N-z),m.n))<q).astype(np.uint8);ss=np.asarray((m.H@es.T).T,dtype=np.uint8)%2;cs=m.m.decode_batch(ss);fs=(es[:,m.cutarr].sum(1)+cs[:,m.cutarr].sum(1))%2
  count+=int(fs.sum())
  for e in es[fs.astype(bool)]:
   if len(starts)<16:starts.append(e.copy())
 extra=0
 while len(starts)<16:
  e=(rng.random(m.n)<q).astype(np.uint8);extra+=1
  if failure(m,e):starts.append(e.copy())
 a=dict(trials=N,failures=count,estimate=count/N,additional_start_trials=extra,initialization_seconds=0.,setup_seconds=setup,sampling_seconds=time.perf_counter()-ts,total_seconds=time.perf_counter()-begin,nominal_999_CP=[float(beta.ppf(.0005,count,N-count+1)),float(beta.ppf(.9995,count+1,N-count))],peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,seed=202611054401)
 np.save(ROOT/'anchor_starts.npy',starts);(ROOT/'anchor.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps(a),flush=True)

class State:
 def __init__(self,m,e):
  self.m=m;self.e=e.copy();self.w=int(e.sum());self.s=np.asarray(m.H@e,dtype=np.uint8)%2
 def flip(self,inds):
  for i in inds:
   self.w+=1-2*int(self.e[i]);self.e[i]^=1
   for c in self.m.edge_checks[i]:self.s[c]^=1
 def fail(self):return failure(self.m,self.e,self.s)

def simulate(m,q,kind,e,seed,steps=2000,burn=2000):
 rng=np.random.default_rng(seed);st=State(m,e);assert st.fail();out=np.empty(steps,np.uint16);calls=m.calls;hits=m.cachehits;stats=dict(proposals=steps+burn,accepted=0,nonfailure=0,mh_rejected=0,unchanged=0)
 sq=np.sqrt(q/(1-q));inv=1/sq;rho=1/11
 # Group equal probabilities without approximation. Random selection within
 # a group is uniform, so the square-root proposal is exact up to float RNG.
 vals,gid=np.unique(q,return_inverse=True);groups=[np.flatnonzero(gid==j) for j in range(len(vals))];sqg=np.sqrt(vals/(1-vals));invg=1/sqg
 for z in range(steps+burn):
  if kind=='zanella':
   occ=np.flatnonzero(st.e);wg=np.bincount(gid[occ],minlength=len(vals));ng=np.array([len(g) for g in groups]);weights=np.r_[wg*invg,(ng-wg)*sqg];lam=float(weights.sum());u=rng.random()*lam;ind=int(np.searchsorted(np.cumsum(weights),u));down=ind<len(vals);j=ind%len(vals)
   if down:choices=occ[gid[occ]==j];i=int(choices[int(rng.integers(len(choices)))])
   else:
    g=groups[j]
    while True:
     i=int(g[int(rng.integers(len(g)))])
     if not st.e[i]:break
   delta=(sq[i]-inv[i]) if down else (inv[i]-sq[i]);accept=min(1.,lam/(lam+delta));inds=[i]
   if rng.random()>=accept:
    stats['mh_rejected']+=1
    if z>=burn:out[z-burn]=st.w
    continue
  else:
   # Marginalizing the resampling-region coin gives these independent flips.
   occ=np.flatnonzero(st.e);delete=occ[rng.random(len(occ))<rho*(1-q[occ])]
   add=np.flatnonzero(rng.random(m.n)<rho*q);add=add[st.e[add]==0];inds=np.r_[delete,add]
   if not len(inds):
    stats['unchanged']+=1
    if z>=burn:out[z-burn]=st.w
    continue
  st.flip(inds)
  if st.fail():stats['accepted']+=1
  else:st.flip(inds);stats['nonfailure']+=1
  if z>=burn:out[z-burn]=st.w
 assert st.fail();stats['decoder_calls']=m.calls-calls;stats['cache_hits']=m.cachehits-hits
 return out,st.e.copy(),stats

def bar(a,b,t1,t2,q):
 n=len(q);w=np.arange(n+1);A=lambda t:float(np.log1p(q*np.expm1(t)).sum());ell=w*(t2-t1)-(A(t2)-A(t1));active=(a+b)>0;offset=math.log(b.sum()/a.sum())
 return float(brentq(lambda r:float(a@expit(ell-r+offset)-b@expit(-ell+r-offset)),float(ell[active].min()-50),float(ell[active].max()+50),xtol=1e-12))

def iat(x):
 y=np.array(x,float);y-=y.mean();n=len(y)
 if not np.any(y):return 1.
 v=np.fft.rfft(y,n=2*n);c=np.fft.irfft(v*v.conj())[:n];c/=c[0];z=1.
 for i in range(1,min(n//2,2000),2):
  v=float(c[i]+c[i+1])
  if v<=0:break
  z+=2*v
 return max(1.,z)

def analyse(kind,traces,ts,m,a,records,timing):
 n=m.n;chains=traces.shape[1];h=np.array([[np.bincount(x,minlength=n+1) for x in rung] for rung in traces]);pooled=[bar(h[j].sum(0),h[j+1].sum(0),ts[j],ts[j+1],m.q) for j in range(len(ts)-1)];pc=np.array([[bar(h[j,k],h[j+1,k],ts[j],ts[j+1],m.q) for j in range(len(ts)-1)] for k in range(chains)]);sums=pc.sum(1);point=math.exp(math.log(a['estimate'])+sum(pooled));sechain=float(sums.std(ddof=1)/math.sqrt(chains));sea=math.sqrt((1-a['estimate'])/(a['trials']*a['estimate']));se=math.hypot(sechain,sea);err=float(student_t.ppf(.9995,chains-1))*se
 for j,r in enumerate(records):
  x=traces[j].astype(float);W=float(x.var(1,ddof=1).mean());B=float(x.shape[1]*x.mean(1).var(ddof=1));r['Rhat']=math.sqrt(((x.shape[1]-1)*W+B)/(x.shape[1]*W));r['IAT']=[iat(z) for z in x];r['50maxIAT_pass']=x.shape[1]>=50*max(r['IAT'])
 out=dict(kernel=kind,implementation='Independent published equations, not upstream software',target='fixed d21 weighted graph rounded q law; unchanged CircuitModel decoder',n=n,chains=chains,burn=2000,retained=2000,rungs=records,ladder=ts,anchor=a,point=point,nominal_999_interval=[point*math.exp(-err),point*math.exp(err)],interval_status='Student-t/delta cross-chain diagnostic; unverified mixing and finite-time bias excluded; not guaranteed coverage',log_SE=se,per_chain_log_ratios=sums.tolist(),pooled_log_ratios=pooled,total_proposals=sum(z['proposals'] for r in records for z in r['stats']),decoder_calls=sum(z['decoder_calls'] for r in records for z in r['stats']),timing=timing,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 return out

def run(kind):
 begin=time.perf_counter();m=acquire();setup=time.perf_counter()-begin;ts=ladder(m.q);a=json.loads((ROOT/'anchor.json').read_text());states=np.load(ROOT/'anchor_starts.npy');traces=np.empty((len(ts),16,2000),np.uint16);records=[];samplebegin=time.perf_counter()
 for j,t in enumerate(ts):
  qq=expit(np.log(m.q/(1-m.q))+t);stats=[];m.cache={}
  for k in range(16):
   seed=(202611054500 if kind=='zanella' else 20261105460000)+100*j+k;traces[j,k],states[k],s=simulate(m,qq,kind,states[k],seed);stats.append(s)
  row=dict(rung=j,t=t,mean_weight=float(traces[j].mean()),stats=stats);records.append(row);print(json.dumps({k:row[k] for k in ['rung','t','mean_weight']}),flush=True);np.savez_compressed(ROOT/(kind+'_partial.npz'),traces=traces[:j+1],ladder=np.array(ts[:j+1]))
 sampling=time.perf_counter()-samplebegin;an=time.perf_counter();out=analyse(kind,traces,ts,m,a,records,dict(setup=setup,sampling=sampling));out['timing'].update(analysis=time.perf_counter()-an,total_excluding_anchor=time.perf_counter()-begin,total_including_anchor=time.perf_counter()-begin+a['total_seconds']);(ROOT/(kind+'_result.json')).write_text(json.dumps(out,indent=2)+'\n');np.savez_compressed(ROOT/(kind+'_traces.npz'),traces=traces,ladder=np.array(ts));print(json.dumps({k:out[k] for k in ['kernel','point','nominal_999_interval','timing','peak_rss_kib']}),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('kind',choices=['anchor','zanella','subregion']);a=p.parse_args();anchor() if a.kind=='anchor' else run(a.kind)
