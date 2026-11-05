"""Independent implementation of published rare-event MH/BAR mathematics.
No upstream mcmc4qec source is executed or imported.
"""
import sys,time,json,math,argparse,hashlib
from pathlib import Path
import numpy as np
from scipy.special import expit
from scipy.optimize import brentq
from scipy.stats import t as student_t, beta
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'canonical_qec_witness_20261105'))
from sampler import Model

class State:
 def __init__(self,m,e):
  self.m=m;self.e=e.copy();self.n=len(e);self.w=int(e.sum())
  self.s=np.zeros(len(m.checks),np.uint8)
  for i in np.flatnonzero(e):
   for c in m.edge_checks[i]:self.s[c]^=1
  self.cutpar=int(e[m.cut].sum())%2
  if not hasattr(m,'_cache'):m._cache={};m._decode_calls=0
 def isfailure(self):
  key=self.s.tobytes();v=self.m._cache.get(key)
  if v is None:
   c=self.m.m.decode(self.s);v=int(c[self.m.cut].sum())%2;self.m._cache[key]=v;self.m._decode_calls+=1
  return self.cutpar ^ v
 def flip(self,inds):
  for i in inds:
   self.w+=1-2*int(self.e[i]);self.e[i]^=1
   if i<self.m.d:self.cutpar^=1
   for c in self.m.edge_checks[i]:self.s[c]^=1

def starting(m,chain):
 e=np.zeros(len(m.edges),np.uint8);y=chain%m.d
 e[[x*m.d+y for x in range((m.d+1)//2 if chain%2 else m.d)]]=1
 return e

def simulate(m,p,kind,steps,burn,chain,seed,initial=None,terminal=None):
 rng=np.random.default_rng(seed);st=State(m,starting(m,chain) if initial is None else initial);calls_start=m._decode_calls;assert st.isfailure()
 alpha=math.sqrt((1-p)/p);beta0=1/alpha
 out=np.empty(steps,np.uint16);stats=dict(proposals=0,decoder_calls=0,failure_gate_queries=0,accepted=0,mh_rejected=0,nonfailure=0,cluster_proposed=0)
 for step in range(steps+burn):
  stats['proposals']+=1
  cluster=kind=='mix' and rng.random()<.3
  if cluster:
   stats['cluster_proposed']+=1
   occ=np.flatnonzero(st.e);emp=np.flatnonzero(st.e==0)
   if min(len(occ),len(emp))<2:
    if step>=burn:out[step-burn]=st.w
    continue
   inds=np.r_[rng.choice(occ,2,replace=False),rng.choice(emp,2,replace=False)]
   accept=1.
  elif kind=='obf':
   i=int(rng.integers(st.n));inds=[i];accept=1. if st.e[i] else p/(1-p)
  else:
   lam=st.w*alpha+(st.n-st.w)*beta0
   downward=rng.random()<st.w*alpha/lam
   choices=np.flatnonzero(st.e if downward else st.e==0)
   i=int(choices[rng.integers(len(choices))]);inds=[i]
   wnew=st.w-1 if downward else st.w+1
   accept=min(1.,lam/(wnew*alpha+(st.n-wnew)*beta0))
  if rng.random()<accept:
   st.flip(inds);stats['failure_gate_queries']+=1
   if st.isfailure():stats['accepted']+=1
   else:st.flip(inds);stats['nonfailure']+=1
  else:stats['mh_rejected']+=1
  if step>=burn:out[step-burn]=st.w
 assert st.isfailure();stats['decoder_calls']=m._decode_calls-calls_start
 if terminal is not None:terminal.append(st.e.copy())
 return out,stats

def ladder(n,d):
 ps=[.15]
 while ps[-1]>.001:
  p=ps[-1];ps.append(max(.001,p*math.exp(-.8/math.sqrt(max(n*p,(d+1)//2)))))
 return ps

def anchor(m,N=50000,seed=2026110501):
 rng=np.random.default_rng(seed);fail=0;start=time.perf_counter();batch=2048
 # Sparse multiplication preserves the exact code/check matrix and decoder.
 for begin in range(0,N,batch):
  e=(rng.random((min(batch,N-begin),len(m.edges)))<.15).astype(np.uint8)
  H=m.H
  s=np.asarray((H@e.T).T,dtype=np.uint8)%2
  c=m.m.decode_batch(s)
  fail+=int(np.count_nonzero((e[:,m.cut].sum(1)+c[:,m.cut].sum(1))%2))
 dt=time.perf_counter()-start
 a=dict(trials=N,failures=fail,estimate=fail/N,p=.15,seed=seed,seconds=dt,
  exact_binomial_CP_999=[float(beta.ppf(.0005,fail,N-fail+1)),float(beta.ppf(.9995,fail+1,N-fail))],
  interval_note='Numeric evaluation of exact CP definition; not outward integer-certified.')
 (ROOT/'anchor.json').write_text(json.dumps(a,indent=2));return a

def bar(hist1,hist2,p1,p2,n):
 w=np.arange(n+1);ell=w*math.log(p2/p1)+(n-w)*math.log((1-p2)/(1-p1))
 offset=math.log(hist2.sum()/hist1.sum())
 def score(r):return float(hist1@expit(ell-r+offset)-hist2@expit(-ell+r-offset))
 active=(hist1+hist2)>0
 r=brentq(score,float(ell[active].min()-50),float(ell[active].max()+50),xtol=2e-13)
 return r

def iat(x):
 x=np.asarray(x,float);x-=x.mean();n=len(x)
 if not np.any(x):return 1.
 v=np.fft.rfft(x,n=2*n);c=np.fft.irfft(v*v.conj())[:n];c/=c[0]
 z=1.
 for j in range(1,min(n//2,2000),2):
  pair=float(c[j]+c[j+1])
  if pair<=0:break
  z+=2*pair
 return max(1.,z)

def run(kind,chains=8,steps=8000,burn=1000):
 allstart=time.perf_counter();m=Model(13);ps=ladder(len(m.edges),m.d)
 a=json.loads((ROOT/'anchor.json').read_text())
 traces=np.empty((len(ps),chains,steps),np.uint16);records=[]
 start=time.perf_counter()
 for j,p in enumerate(ps):
  stats=[];m._cache={};m._decode_calls=0
  for k in range(chains):
   seed=202611050000+100000*['obf','zanella','mix'].index(kind)+100*j+k
   traces[j,k],st=simulate(m,p,kind,steps,burn,k,seed);stats.append(st)
  row=dict(rung=j,p=p,cache_entries=len(m._cache),mean_weight=float(traces[j].mean()),stats=stats,
   initial_logical_mean=float(traces[j,::2].mean()),initial_minfail_mean=float(traces[j,1::2].mean()))
  records.append(row);print(json.dumps(dict(kernel=kind,**{k:row[k] for k in ['rung','p','mean_weight']})),flush=True)
 sampletime=time.perf_counter()-start
 np.savez_compressed(ROOT/(kind+'_traces.npz'),traces=traces,ladder=np.array(ps))
 analyse=time.perf_counter();n=len(m.edges)
 h=np.array([[np.bincount(x,minlength=n+1) for x in rung] for rung in traces])
 pooled=[bar(h[j].sum(0),h[j+1].sum(0),ps[j],ps[j+1],n) for j in range(len(ps)-1)]
 perchain=np.array([[bar(h[j,k],h[j+1,k],ps[j],ps[j+1],n) for j in range(len(ps)-1)] for k in range(chains)])
 tot=perchain.sum(1);point=math.exp(math.log(a['estimate'])+sum(pooled))
 se_chain=float(tot.std(ddof=1)/math.sqrt(chains));se_anchor=math.sqrt((1-a['estimate'])/(a['trials']*a['estimate']))
 se=math.hypot(se_chain,se_anchor);crit=float(student_t.ppf(.9995,chains-1));err=crit*se
 for j,row in enumerate(records):
  row['weight_iat_diagnostics']=[iat(x) for x in traces[j]]
  row['chain_means']=[float(x.mean()) for x in traces[j]]
 result=dict(implementation='Independent published-equation implementation; not upstream mcmc4qec execution',kernel=kind,
  model='same public d13 Model and PyMatching tie convention as canonical witness',n=n,p=.001,
  ladder=ps,chains=chains,steps=steps,burn_in=burn,anchor=a,point_estimate=point,
  nominal_999_student_interval=[point*math.exp(-err),point*math.exp(err)],
  interval_status='Diagnostic asymptotic interval, not a finite-time coverage guarantee. Unverified mixing/systematic bias excluded.',
  log_standard_error=se,chain_log_standard_error=se_chain,anchor_log_standard_error=se_anchor,
  per_chain_log_ratio_sum=tot.tolist(),pooled_log_ratios=pooled,rungs=records,
  total_proposals=sum(z['proposals'] for r in records for z in r['stats']),
  total_decoder_calls=sum(z['decoder_calls'] for r in records for z in r['stats']),
  timing_seconds=dict(sampling=sampletime,analysis=time.perf_counter()-analyse,
   total_excluding_anchor=time.perf_counter()-allstart,total_including_anchor=time.perf_counter()-allstart+a['seconds']))
 (ROOT/(kind+'_result.json')).write_text(json.dumps(result,indent=2));print(json.dumps({k:result[k] for k in ['kernel','point_estimate','nominal_999_student_interval','timing_seconds']}),flush=True)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('kind',choices=['anchor','obf','zanella','mix']);v=ap.parse_args()
 if v.kind=='anchor':print(json.dumps(anchor(Model(13)),indent=2))
 else:run(v.kind)
