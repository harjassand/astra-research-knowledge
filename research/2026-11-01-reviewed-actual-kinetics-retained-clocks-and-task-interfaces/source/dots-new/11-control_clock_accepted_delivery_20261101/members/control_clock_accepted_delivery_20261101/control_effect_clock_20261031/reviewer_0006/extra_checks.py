from pathlib import Path
import sys,json,gzip,hashlib,itertools
from copy import deepcopy
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import clock_response as R
C=R.C
ROOT=Path(__file__).resolve().parents[1]
def run():
 checks=refusals=0
 def check(v):
  nonlocal checks
  assert v;checks+=1
 # Synthetic exact paths ONLY: exercise meeting before/at/after each requested cap.
 for gamma in ('1/100','1/2','99/100'):
  for j in range(4):
   for tau in range(10):
    d=R.design(source_id='synthetic_no_observations',n=2,m=3,gamma=gamma,parts=[[0],[1]],i=1,j=j,delta_total='1/7',root_bits=20)
    end=max(tau,d['K']+1)
    x=[0]*(tau+1);y=[1]*tau+[0]
    trials=[dict(x=x,y=y),dict(x=y,y=x)]
    rows=[dict(state=i,action=a,trials=deepcopy(trials)) for i in range(2) for a in (1,2)]
    calls=16*(tau+1)
    rec=dict(kind='retained_paired_path_bank_v1',design=d,rows=rows,source_calls=calls,attempts=[dict(N=2,K=tau,new_source_calls=calls,cumulative_source_calls=calls)])
    out=R.receive(rec,expected_design=d)
    check(all(S.Matrix(v)==S.zeros(2) for v in out['empirical_scaled_rows']))
    check(all(b['nonmeetings']==2*int(tau>d['K']) for b in out['row_radii']))
    check(out['prefix_terms_replayed']==8*min(tau,d['K']))
    check(out['retained_source_calls']==calls)
 # Prefix confidence is nonzero even every observed trial meets at zero.
 d=R.design(source_id='null_unseen_alternative',n=2,m=2,gamma='99/100',parts=[[0],[1]],i=3,j=3,delta_total='1/100',root_bits=30)
 rows=[dict(state=i,action=1,trials=[dict(x=[i],y=[i]) for _ in range(d['N'])]) for i in range(2)]
 calls=4*d['N'];rec=dict(kind='retained_paired_path_bank_v1',design=d,rows=rows,source_calls=calls,attempts=[dict(N=d['N'],K=d['K'],new_source_calls=calls,cumulative_source_calls=calls)])
 out=R.receive(rec,expected_design=d)
 check(S.Rational(out['eta_U'])>0)
 check(all(S.Rational(b['sample_variance'][0])==0 and S.Rational(b['prefix'])>0 and S.Rational(b['tail'])>0 for b in out['row_radii']))
 # External design/task rejection; aliases and actual censoring, not just checksum.
 saved=json.loads((ROOT/'observed_response_v2.json').read_text());record=json.loads(gzip.decompress((ROOT/'observed_paired_paths.json.gz').read_bytes()));des=saved['design']
 muts=[]
 for field,value in [('i',True),('j',False),('root_bits',True),('parts',[[0,1],[2,3]]),('delta','1/2')]:
  rr=deepcopy(record);rr['design'][field]=value;muts.append(rr)
 rr=deepcopy(record);rr['rows'][0]['trials']=rr['rows'][0]['trials'][:1];muts.append(rr)
 rr=deepcopy(record);rr['rows'][1]['state']=rr['rows'][0]['state'];muts.append(rr)
 rr=deepcopy(record);rr['rows'][0]['trials'][0]['x'][0]=-1;muts.append(rr)
 rr=deepcopy(record);rr['rows'][0]['trials'][0]['x'][0]=0.0;muts.append(rr)
 rr=deepcopy(record);rr['attempts'][0]['new_source_calls']=True;muts.append(rr)
 rr=deepcopy(record);rr['source_calls']=True;muts.append(rr)
 rr=deepcopy(record);old=rr['rows'][0]['trials'][0];rr['source_calls']-=2*(len(old['x'])-1);rr['rows'][0]['trials'][0]={'x':[0],'y':[1]};rr['attempts'][0]['new_source_calls']=rr['source_calls'];rr['attempts'][0]['cumulative_source_calls']=rr['source_calls'];muts.append(rr)
 for rr in muts:
  try:R.receive(rr,expected_design=des)
  except (ValueError,TypeError,KeyError,IndexError):refusals+=1
  else:raise AssertionError('accepted mutation')
 # Lower task values from full Bellman inverse, not copied closed forms.
 for ep in (S.Rational(1,16),S.Rational(1,100)):
  for ga in (S.Rational(1,2),S.Rational(99,100)):
   p=8*ep*(1-ga)/ga
   for h in range(21):
    th=S.Rational(h,20);A=S.Matrix([[1-th*p,th*p],[0,1]]);reward=S.Matrix([2*ep*(1-th),1]);v=(1-ga)*(S.eye(2)-ga*A).inv()*reward
    check(v[0]==(2*ep+6*ep*th)/(1+8*ep*th))
    if th<=S.Rational(1,2):check(8*ep/(1+8*ep)-v[0]>ep)
 # Dyadic budgets and exact diagonal cost upper bound.
 for D in range(1,12):
  mass=sum(S.Rational(1,2)**(i+j+1) for i in range(1,D+1) for j in range(D+1-i))
  check(mass<1)
  check(sum(k*2**k for k in range(1,D+1))==(D-1)*2**(D+1)+2)
 # Frozen artifact/dependency check after replay.
 man=json.loads((ROOT/'REVIEW_FREEZE_MANIFEST_20261031_2348UTC.json').read_text())
 for item in man['files']+man['dependencies']:
  raw=(ROOT.parent/item['path']).read_bytes();check(len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256'])
 return dict(status='PASS',exact_checks=checks,refusals=refusals,new_source_calls=0,synthetic_paths_not_observations=True,scope='Finite receiving and algebra, not iid provenance or extra successful learning.')
if __name__=='__main__':print(json.dumps(run(),indent=2))
