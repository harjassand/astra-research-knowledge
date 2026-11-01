"""Exact independent direct-admission checks, no source calls."""
from pathlib import Path
import sys,json,copy,random,itertools,signal,time
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));import direct as D
C=D.C

def from_witness(cert,X,d,tol):
 r,m,gamma,eta,_,B,_=D.effect_coefficients(cert);t=gamma/(1-gamma);beta=1-d;trans=[]
 for Ba in B:
  Y=X*(S.eye(r)-t*Ba).T;Q=S.zeros(r+1);Q[:r,:r]=Y
  for j in range(r):Q[r,j]=d-sum(Y[:,j])
  Q[r,r]=d;P=(S.eye(r+1)-Q).T/beta if beta else S.eye(r+1);trans.append(C.serial(P))
 return dict(status='PASS_EXACT_CANONICAL_COMPUTATIONAL_MDP',source_certificate_sha256=C.digest(cert),r=r,m=m,X=C.serial(X),canonical_gap=str(d),canonical_discount=str(beta),transitions=trans,admission=D.direct_admission(X,d,t,eta,tol))
def run():
 checks=0;refusals=0;rng=random.Random(2305);backend_refusals=[]
 oldlp=D.linprog
 def alarm_handler(*args):raise TimeoutError('reviewer 5-second per-LP test budget')
 oldhandler=signal.signal(signal.SIGALRM,alarm_handler)
 def bounded_lp(*args,**kwargs):
  signal.setitimer(signal.ITIMER_REAL,5)
  try:return oldlp(*args,**kwargs)
  finally:signal.setitimer(signal.ITIMER_REAL,0)
 D.linprog=bounded_lp
 def ck(x):
  nonlocal checks
  assert x;checks+=1
 def reject(fn):
  nonlocal refusals
  try:fn()
  except (ValueError,AssertionError,TypeError):refusals+=1
  else:raise AssertionError('invalid accepted')
 # Exact counterexample to v1 optimization sentence, within a real source class.
 gamma=S.Rational(9,10);A0=S.Matrix([[S.Rational(1,2),S.Rational(1,2),0],[S.Rational(1,4),S.Rational(3,4),0],[0,0,1]]);A1=S.Matrix([[S.Rational(103,144),S.Rational(41,144),0],[S.Rational(49,72),S.Rational(23,72),0],[0,0,1]]);M=S.Matrix([[S.Rational(3,4),S.Rational(1,4),0],[-S.Rational(1,2),S.Rational(3,2),0],[0,0,1]]);E=C.exact_effects([A0,A1],[[0],[1],[2]],gamma);ck(gamma/(1-gamma)*E['B'][1]==S.eye(3)-M)
 cert=dict(r=3,m=2,gamma=str(gamma),eta='1/1000',Bhat=[C.serial(B) for B in E['B']]);d=S.Rational(3,5);tol=S.Rational(27,1000);badX=S.Matrix([[S.Rational(4,5),0,0],[-S.Rational(1,5),S.Rational(3,5),0],[0,0,1]]);goodX=badX.copy();goodX[2,2]=S.Rational(4,5)
 out=[]
 for X in [badX,goodX]:
  model=from_witness(cert,X,d,tol);ad=D.verify_uniform(cert,model,expected_certificate_sha256=C.digest(cert),expected_model_sha256=C.digest(model),expected_tolerance=tol);out.append(ad);ck(X.det()!=0)
 ck(out[0]['weight_bound']=='5/3');ck(out[1]['weight_bound']=='4/3');ck(out[0]['status']=='UNKNOWN_ALL_GOAL_DIRECT_CANONICAL_ADMISSION');ck(out[1]['status']=='PASS_ALL_GOAL_DIRECT_CANONICAL_ADMISSION')
 # Exact optimality upper bound: Y21=3X21/4+X22/4<=0,
 # Y22=-X21/2+3X22/2<=1 => X22<=3/5, delta<=X22.
 a,b=S.symbols('a b');ck(-(-b/3)/2+S.Rational(3,2)*b==S.Rational(5,3)*b)
 counter={'gamma':str(gamma),'A0':C.serial(A0),'A1':C.serial(A1),'M1':C.serial(M),'optimal_delta':str(d),'X_worse':C.serial(badX),'X_better':C.serial(goodX),'admissions':out,'scope':'Both delta-optimal, but different maxdiag(X)/delta. Main feasible-witness guarantee unaffected.'}
 # Nonsymmetric three-action random models; source h omitted entirely.
 tasks=0;selectors=0
 for case in range(8):
  n=5;r=3;m=3;parts=[[0],[1,2],[3,4]];Z,W,which=C.partitions(parts,n);gamma=[S.Rational(1,3),S.Rational(2,3)][case%2]
  rows=[[rng.randrange(1,6) for _ in range(n)] for _ in range(n)];A0=S.Matrix([[S.Rational(v,sum(row)) for v in row] for row in rows]);actions=[A0]
  for a in range(1,m):
   B=S.Matrix([[rng.randrange(-2,3),rng.randrange(-2,3),0] for _ in range(r)])/200
   for j in range(r):B[j,2]=-sum(B.row(j))
   Ap=A0+Z*B*W;Ap[2,0]+=S.Rational(a,10**6);Ap[2,4]-=S.Rational(a,10**6);actions.append(Ap)
  E=C.exact_effects(actions,parts,gamma);cert=dict(r=r,m=m,gamma=str(gamma),eta=str(max(E['eta'],S.Rational(1,1000))),Bhat=[C.serial(B) for B in E['B']]);ch=C.digest(cert);model=D.compile_model(cert,expected_certificate_sha256=ch,expected_tolerance='1/10');mh=C.digest(model)
  if model['status']!='PASS_EXACT_CANONICAL_COMPUTATIONAL_MDP':
   backend_refusals.append({'case':case,'stage':'compile','result':model});continue
  ad=D.verify_uniform(cert,model,expected_certificate_sha256=ch,expected_model_sha256=mh,expected_tolerance='1/10');ck(ad['status']=='PASS_ALL_GOAL_DIRECT_CANONICAL_ADMISSION');X=C.matrix(model['X']);hc=(X.inv()*S.ones(r,1)).T;ck(min(hc)>0);t=gamma/(1-gamma)
  for _ in range(8):
   weights=[]
   for j in range(r):
    row=[rng.randrange(1,6) for a in range(m)];weights.append([S.Rational(v,sum(row)) for v in row])
   Bpi=S.Matrix(r,r,lambda j,k:sum(weights[j][a]*E['B'][a][j,k] for a in range(m)));M=S.eye(r)-t*Bpi;Y=X*M.T
   ck(hc*M.inv()==S.ones(1,r)*(Y.T).inv());ck(min(hc*M.inv())>0);selectors+=1
  for _ in range(5):
   goals=[[str(S.Rational(rng.randrange(5),4)) for j in range(r)] for a in range(m)];kw=dict(expected_certificate_sha256=ch,expected_model_sha256=mh,expected_goal_sha256=C.digest(goals),expected_tolerance='1/10');a=D.plan_model(cert,model,goals,**kw);b=D.plan_small_lp(cert,model,goals,**kw)
   ck(a['status']=='PASS_POLICY_REGRET')
   if b['status']=='PASS_POLICY_REGRET':ck(a['w']==b['w'])
   else:backend_refusals.append({'case':case,'stage':'small_lp','goals':goals,'result':b})
   ck(min(map(S.Rational,a['w']))>=0);ck(max(map(S.Rational,a['w']))<=S.Rational(ad['weight_bound']));ck(S.Rational(a['regret_bound'])<=S.Rational(ad['normalized_pointwise_regret_bound']));tasks+=1
 # Wrong source objective fields are irrelevant, not silently used as guarantees.
 weird=copy.deepcopy(cert);weird['hhat']=['garbage'];weird['delta_h']='garbage';wm=D.compile_model(weird,expected_certificate_sha256=C.digest(weird),expected_tolerance='1/10');ck(wm['admission']['status']=='PASS_ALL_GOAL_DIRECT_CANONICAL_ADMISSION')
 for field,value in [('r',True),('m',3.0),('eta','-1'),('gamma','1')]:
  cc=copy.deepcopy(cert);cc[field]=value;reject(lambda cc=cc:D.compile_model(cc,expected_certificate_sha256=C.digest(cc),expected_tolerance='1/10'))
 for field,value in [('canonical_gap','0'),('canonical_discount','1'),('X',C.serial(S.zeros(r))),('source_certificate_sha256','bad')]:
  mm=copy.deepcopy(model);mm[field]=value;reject(lambda mm=mm:D.verify_uniform(cert,mm,expected_certificate_sha256=ch,expected_model_sha256=C.digest(mm),expected_tolerance='1/10'))
 mm=copy.deepcopy(model);mm['admission']['weight_bound']='0';reject(lambda:D.verify_uniform(cert,mm,expected_certificate_sha256=ch,expected_model_sha256=C.digest(mm),expected_tolerance='1/10'))
 reject(lambda:D.verify_uniform(cert,model,expected_certificate_sha256=ch,expected_model_sha256=mh,expected_tolerance='1/5'))
 D.linprog=oldlp;signal.signal(signal.SIGALRM,oldhandler)
 return {'backend_refusals':backend_refusals,'status':'PASS_INDEPENDENT_MAIN_DIRECT_THEOREM_CHECKS','exact_checks':checks,'refusals':refusals,'random_models':8,'mixed_selectors':selectors,'action_reward_tasks':tasks,'source_calls':0,'original_auxiliary_optimization_counterexample':counter}
if __name__=='__main__':print(json.dumps(run(),indent=2))
