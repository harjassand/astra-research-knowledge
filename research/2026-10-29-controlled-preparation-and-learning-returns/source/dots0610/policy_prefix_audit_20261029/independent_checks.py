import pathlib,sys,json,math,itertools
from fractions import Fraction
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parent
POL=pathlib.Path('producer-workspace/guard_policy_optimization_20261029');PRE=pathlib.Path('producer-workspace/acquisition_prefix_tradeoff_20261029')
sys.path.insert(0,str(POL));from embedded_chain import evaluate_fast
tr=np.array([1.,0,0,1]);rng=np.random.default_rng(202610290456)
def sup(Ks):return sum(np.kron(K,K.conj()) for K in Ks)
def chronological(tp,tf,sv,sigma,s,J,b,N=600):
 state=np.zeros((J,b+1,4),complex);state[0,0]=sigma.reshape(-1);acc=np.zeros(4,complex);abort=np.zeros(4,complex);cost=0.
 for _ in range(N):
  cost+=float(np.einsum('a,jfa->',tr,state).real);new=np.zeros_like(state)
  for j in range(J):
   for f in range(b+1):
    v=state[j,f];new[j,f]+=(1-s)*tp@v
    z=s*sv@v
    if j+1==J:acc+=z
    else:new[j+1,f]+=z
    z=(1-s)*tf@v
    if f==b:abort+=z
    else:new[j,f+1]+=z
  state=new
 return float((tr@acc).real),cost,acc+abort,float(np.einsum('a,jfa->',tr,state).real)
small=[]
for case in range(8):
 lam=rng.uniform(.1,.9,size=2);A=np.diag(np.sqrt(lam));B=np.diag(np.sqrt(1-lam))
 Z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));U,_=np.linalg.qr(Z)
 tp=sup([U@A]);tf=sup([U.conj().T@B]);p=.17
 sv=sup([np.array([[1,0],[0,np.sqrt(1-p)]],complex),np.array([[0,np.sqrt(p)],[0,0]],complex)])
 sigma=np.array([[.6,.12j],[-.12j,.4]]);s=.3+.05*(case%3);J=2+case%4;b=case%3
 A0,C0,end,res=chronological(tp,tf,sv,sigma,s,J,b)
 fast=evaluate_fast(tp,tf,sv,sigma,s,J,b)
 assert res<1e-30 and abs(A0-fast['uncapped_acceptance'])<1e-12 and abs(C0-fast['uncapped_expected_calls'])<1e-11
 small.append({'case':case,'acceptance_residual':abs(A0-fast['uncapped_acceptance']),'cost_residual':abs(C0-fast['uncapped_expected_calls']),'unabsorbed_probability':res})
grid=json.load(open(POL/'policy_grid_v2.json'));rows=grid['all_policies'];exact=0
for r in rows:
 R=Fraction(r['R']);q=1/(1+R);p=R/(1+R);b=r['b'];t=r['t']
 tail=sum(Fraction(math.comb(t+b+1,j))*q**j*p**(t+b+1-j) for j in range(b+1))
 assert tail==Fraction(r['NB_tail_exact'])<=Fraction(1,128)
 if t:
  prev=sum(Fraction(math.comb(t+b,j))*q**j*p**(t+b-j) for j in range(b+1));assert prev>Fraction(1,128)
 sf=Fraction(r['s']);assert R==Fraction(r['C'])*sf/(1-sf)
 assert r['cap_native_calls']==math.ceil(Fraction(2*r['J']+256)/sf)
 assert r['payload_qubits']==r['h']*(r['B']-4*t) and r['J']==r['h']*r['B']
 exact+=1
for name,w in grid['winners_guard_throughput'].items():
 eligible=[r for r in rows if r['test']==name];assert w==max(eligible,key=lambda r:r['finite_guard_payload_per_call_lower'])
maps=np.load(PRE/'prefix_maps.npz');saved=np.load(PRE/'terminal_memory_maps.npz');terminal={};prefix_checks=[]
for m in (100,1000,10000,100000,1000000):
 for method,C in [('six',1.5),('matching',2.)]:
  s=1/(1+C);tp=maps[f'{method}_pass_{m}'];tf=maps[f'{method}_fail_{m}'];sv=maps[f'good_{m}']+maps[f'bad_{m}']
  G=np.linalg.solve(np.eye(4)-(1-s)*tp,np.eye(4));S=s*sv@G;F=(1-s)*tf@G
  # Independent backward recurrence, composing a terminal future with one epoch.
  acc=np.eye(4,dtype=complex);end=np.eye(4,dtype=complex);cost=np.zeros(4,complex)
  for _ in range(155):
   acc=acc@S;end=F+end@S;cost=tr@G+cost@S
  assert np.linalg.norm(tr@end-tr)<1e-10
  errs={k:float(np.linalg.norm(v-saved[f'{method}_{k}_{m}'])) for k,v in [('acc',acc),('end',end),('cost',cost)]}
  assert max(errs.values())<1e-9
  terminal[m,method]=(acc,end,cost)
  prefix_checks.append({'prefix':m,'test':method,'recurrence_residuals':errs})
stats={m:[maps[f'sigma_{m}'].reshape(-1),0.,0.] for m in (100000,1000000)};cross=None;snap={}
for count in range(1,10001):
 rates={}
 for m,st in stats.items():
  acc,end,cost=terminal[m,'six'];v=st[0];st[1]+=float((tr@acc@v).real);st[2]+=float((cost@v).real);st[0]=end@v;rates[m]=35*st[1]/(m+st[2])
 if rates[1000000]>=rates[100000] and cross is None:cross=count
 if count in (1,1000,2031,2032,10000):snap[count]=rates
assert cross==2032
frozen=json.load(open(POL/'frozen_policy_prefixes.json'));large=[]
for r in frozen['rows']:
 m=r['learning_calls'];method='six' if r['test']=='six_state' else 'matching';p=r['frozen_policy'];s=float(Fraction(p['s']))
 ev=evaluate_fast(maps[f'{method}_pass_{m}'],maps[f'{method}_fail_{m}'],maps[f'good_{m}']+maps[f'bad_{m}'],maps[f'sigma_{m}'],s,p['J'],p['b'])
 assert abs(ev['uncapped_acceptance']-r['uncapped_acceptance'])<1e-12 and abs(ev['uncapped_expected_calls']-r['uncapped_expected_calls'])<1e-7
 if m in (100000,1000000):large.append({'prefix':m,'test':r['test'],**ev})
out={'all_checks_passed':True,'independent_native_step_recursions':small,'exact_grid_rows':exact,'prefix_backward_recurrences':prefix_checks,'retained_bath_crossover':cross,'rate_snapshots':snap,'frozen_large_workload_replay':large,'scope':'Floating diagnostics, no interval-certified probabilities; training source not rerun.'}
(ROOT/'independent_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'all_checks_passed':True,'exact_grid_rows':exact,'retained_bath_crossover':cross,'large':large},indent=2))
