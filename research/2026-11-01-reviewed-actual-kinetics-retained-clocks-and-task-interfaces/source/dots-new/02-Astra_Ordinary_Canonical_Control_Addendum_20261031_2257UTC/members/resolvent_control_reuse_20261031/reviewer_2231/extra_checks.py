"""Independent exact algebra/receiving checks. No source calls or file mutation on run()."""
from pathlib import Path
import sys,random,itertools,copy,json,gzip
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import control as C
from check_control import cert_from_exact
from sympy.solvers.simplex import linprog
ROOT=Path(__file__).resolve().parents[1]
def run():
 checks=0;refusals=0;backend_failures=[];rng=random.Random(223134)
 def ck(x):
  nonlocal checks
  assert x;checks+=1
 def reject(f):
  nonlocal refusals
  try:f()
  except (TypeError,ValueError,AssertionError):refusals+=1
  else:raise AssertionError('invalid accepted')
 for case in range(12):
  n=5;parts=[[0],[1,2],[3,4]];Z,W,which=C.partitions(parts,n);r=3;m=3
  gamma=[S.Rational(1,4),S.Rational(1,2),S.Rational(3,4)][case%3]
  A0=S.Matrix([[S.Rational(v,sum(row)) for v in row] for row in [[rng.randrange(1,8) for _ in range(n)] for i in range(n)]])
  actions=[A0]
  for aa in range(1,m):
   D=S.Matrix([[rng.randrange(-2,3) for _ in range(r-1)]+[0] for j in range(r)])/500
   for j in range(r):D[j,r-1]=-sum(D.row(j))
   Ap=A0+Z*D*W
   # A nonzero within-block defect: no exact closure promise.
   Ap[1,0]+=S.Rational(aa,10**7);Ap[1,4]-=S.Rational(aa,10**7)
   ck(min(Ap)>0);actions.append(Ap)
  E=C.exact_effects(actions,parts,gamma);Bn=[B.copy() for B in E['B']]
  Bn[1][0,0]+=S.Rational(1,10**8);Bn[1][0,1]-=S.Rational(1,10**8)
  h=E['h']+S.Matrix([[S.Rational(1,10**8),-S.Rational(1,10**8),0]])
  eta=max(C.row_l1(Ea-Z*Ba) for Ea,Ba in zip(E['C'],Bn));dh=sum(abs(x) for x in h-E['h'])
  cert=cert_from_exact(E,gamma,eta,dh,Bn,h)
  ad=C.uniform_admission(cert,expected_certificate_sha256=C.digest(cert),expected_tolerance='1/100')
  ck(ad['status']=='PASS_ALL_GOAL_LP_ADMISSION');t=gamma/(1-gamma);d=S.Rational(ad['d']);z=S.Rational(ad['objective_margin']);mu=S.ones(1,r)*W/r
  for trial in range(10):
   rows=[]
   for j in range(r):
    vals=[rng.randrange(1,5) for a in range(m)];rows.append([S.Rational(v,sum(vals)) for v in vals])
   Ap=S.Matrix(n,n,lambda i,k:sum(rows[which[i]][a]*actions[a][i,k] for a in range(m)))
   Bp=S.Matrix(r,r,lambda j,k:sum(rows[j][a]*Bn[a][j,k] for a in range(m)))
   M=S.eye(r)-t*Bp;Mi=M.inv();G=(S.eye(n)-gamma*Ap).inv();err=(Ap-A0)*E['H']-Z*Bp
   ck(C.row_l1(err)<=eta)
   ck(E['H']*Mi==(1-gamma)*G*Z-gamma*G*err*Mi)
   ck(C.row_l1(Mi)<=1/d);ck(min(h*Mi)>=z)
  for trial in range(4):
   goals=S.Matrix(m,r,lambda a,j:S.Rational(rng.randrange(6),5));table=C.serial(goals)
   out=C.margin_plan_action_rewards(cert,table,expected_certificate_sha256=C.digest(cert),expected_goal_sha256=C.digest(table),expected_tolerance='1/100')
   ck(out['status']=='PASS_POLICY_REGRET');ck(S.Rational(out['rho'])==0);ck(min(S.Rational(v) for v in out['dual_group_weights'])>=z)
   constraints=S.Matrix.vstack(*[gamma*A-S.eye(n) for A in actions]);rhs=S.Matrix.vstack(*[-(1-gamma)*Z*goals.row(a).T for a in range(m)])
   _,v=linprog(S.ones(1,n),constraints,rhs,bounds=(None,None));v=S.Matrix(v)
   truth=(1-gamma)*S.Matrix([max(goals[a,which[i]]+gamma/(1-gamma)*(actions[a]*v)[i] for a in range(m)) for i in range(n)])
   if v!=truth:
    backend_failures.append({'case':case,'trial':trial,'actions':[C.serial(A) for A in actions],'goals':table,'gamma':str(gamma),'bad_v':C.serial(v),'bad_Bellman':C.serial(truth)})
   # Independent exact policy iteration: never trust the full-state simplex.
   choices=[0]*n
   for _ in range(m**n+1):
    chosenA=S.Matrix(n,n,lambda i,k:actions[choices[i]][i,k]);chosenR=S.Matrix([goals[choices[i],which[i]] for i in range(n)])
    v=(1-gamma)*(S.eye(n)-gamma*chosenA).inv()*chosenR
    scores=[(1-gamma)*Z*goals.row(a).T+gamma*actions[a]*v for a in range(m)]
    new=[choices[i] if scores[choices[i]][i]==max(sc[i] for sc in scores) else max(range(m),key=lambda a:scores[a][i]) for i in range(n)]
    if new==choices:break
    choices=new
   else:raise AssertionError('policy iteration failed')
   ck(v==S.Matrix([max(sc[i] for sc in scores) for i in range(n)]))
   pi=out['policy'];actualA=S.Matrix(n,n,lambda i,k:actions[pi[which[i]]][i,k]);reward=S.Matrix([goals[pi[which[i]],which[i]] for i in range(n)])
   vp=(1-gamma)*(S.eye(n)-gamma*actualA).inv()*reward
   ck(min(v-vp)>=0);ck(max(v-vp)<=S.Rational(out['normalized_pointwise_regret_bound']));ck(S.Rational(out['normalized_pointwise_regret_bound'])<=S.Rational(ad['normalized_pointwise_regret_bound']))
 # Degenerate one-state, baseline-only, multiple rewards and zero goal.
 E=C.exact_effects([S.ones(1)],[[0]],S.Rational(1,2));cert=cert_from_exact(E,S.Rational(1,2))
 for g in [['0'],['1/3'],['1']]:
  o=C.margin_plan(cert,g,expected_certificate_sha256=C.digest(cert),expected_goal_sha256=C.digest(g),expected_tolerance='0');ck(o['status']=='PASS_POLICY_REGRET')
 saved=json.loads((ROOT/'episode_protocol_checks.json').read_text());rec=saved['record'];design=rec['design']
 paths=json.loads(gzip.decompress((ROOT/'episode_micro_paths.json.gz').read_bytes()));ck(C.digest(paths)==saved['micro_path_sha256']);ck(len(paths)==4096)
 counts=[[[0,0] for _ in range(4)] for _ in range(2)];seen=set();calls=0
 for p in paths:
  key=(p['action'],p['source_row'],p['episode']);ck(key not in seen);seen.add(key);q=p['micro_path'];ck(q[0]==p['source_row'] and all(type(i)is int and 0<=i<4 for i in q));ck(2<=len(q)<=34);calls+=len(q)-1;counts[p['action']][p['source_row']][q[-1]//2]+=1
 ck(counts==rec['counts']);ck(calls==38626)
 for key,value in [('n',True),('m',2.0),('N',True),('cap',-1),('root_bits',0),('gamma','0'),('gamma','1'),('delta','0'),('source_id','')]:
  dd=copy.deepcopy(design);dd[key]=value;rr=copy.deepcopy(rec);rr['design']=dd;reject(lambda rr=rr,dd=dd:C.receive_counts(rr,expected_design=dd))
 for key,value in [('N',513),('source_id','OTHER'),('parts',[[0,2],[1,3]]),('delta','1/10')]:
  dd=copy.deepcopy(design);dd[key]=value;reject(lambda dd=dd:C.receive_counts(rec,expected_design=dd))
 for value in [True,-1,379.0]:
  rr=copy.deepcopy(rec);rr['counts'][0][0][0]=value;reject(lambda rr=rr:C.receive_counts(rr,expected_design=design))
 for parts in [[[0,1],[1,3]],[[0,1],[2]],[[0,1],[]]]:
  dd=copy.deepcopy(design);dd['parts']=parts;rr=copy.deepcopy(rec);rr['design']=dd;reject(lambda rr=rr,dd=dd:C.receive_counts(rr,expected_design=dd))
 # Genuine zero-cap endpoint law and geometric cap bias independently exact.
 A=S.Matrix([[S.Rational(3,4),S.Rational(1,4)],[S.Rational(1,3),S.Rational(2,3)]]);gam=S.Rational(2,3);H=(1-gam)*(S.eye(2)-gam*A).inv()
 for cap in range(8):
  truncated=sum(((1-gam)*gam**j*A**j for j in range(cap)),S.zeros(2))+gam**cap*A**cap
  ck(C.row_l1(A*H-A*truncated)<=2*gam**(cap+1));ck(truncated*S.ones(2,1)==S.ones(2,1))
 return {'status':'PASS_INDEPENDENT_RESOLVENT_REVIEW_CHECKS','exact_checks':checks,'refusals':refusals,'random_models':12,'three_action_reward_tasks':48,'mixed_selectors':120,'saved_paths_replayed':4096,'new_source_calls':0,'caught_full_state_simplex_failures':backend_failures}
if __name__=='__main__':print(json.dumps(run(),indent=2))
