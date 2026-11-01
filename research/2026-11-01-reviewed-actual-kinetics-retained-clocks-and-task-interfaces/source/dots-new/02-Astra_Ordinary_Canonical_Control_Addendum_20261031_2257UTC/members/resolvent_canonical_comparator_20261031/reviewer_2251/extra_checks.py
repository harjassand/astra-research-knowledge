"""Independent exact comparison/receiving checks; zero observations."""
from pathlib import Path
import sys,json,copy,random
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import canonical as K
C=K.C
from check_control import cert_from_exact

def true_value(actions,rew,gamma):
 n=actions[0].rows;m=len(actions);pi=[0]*n;seen=set()
 while True:
  assert tuple(pi) not in seen;seen.add(tuple(pi));A=S.Matrix(n,n,lambda i,j:actions[pi[i]][i,j]);r=S.Matrix([rew[pi[i]][i] for i in range(n)]);v=(S.eye(n)-gamma*A).inv()*r
  scores=[rew[a]+gamma*actions[a]*v for a in range(m)];best=S.Matrix([max(w[i] for w in scores) for i in range(n)])
  if v==best:return v
  pi=[pi[i] if best[i]==v[i] else max(range(m),key=lambda a:scores[a][i]) for i in range(n)]

def run():
 checks=0;refusals=0;rng=random.Random(2252);models=[]
 def ck(x):
  nonlocal checks
  assert x;checks+=1
 def reject(fn):
  nonlocal refusals
  try:fn()
  except (AssertionError,ValueError,TypeError):refusals+=1
  else:raise AssertionError('invalid accepted')
 for case in range(12):
  n=5;parts=[[0],[1,2],[3,4]];Z,W,which=C.partitions(parts,n);r=3;m=3;gamma=[S.Rational(1,4),S.Rational(1,2),S.Rational(3,4)][case%3]
  rows=[[rng.randrange(1,6) for _ in range(n)] for i in range(n)];A0=S.Matrix([[S.Rational(x,sum(row)) for x in row] for row in rows]);Ds=[S.zeros(r),S.Matrix([[1,-1,0],[0,1,-1],[-1,0,1]])/200,S.Matrix([[-1,0,1],[1,-1,0],[0,1,-1]])/150];raw=[A0+Z*D*W for D in Ds];actions=[A.copy() for A in raw]
  if case%2:
   actions[1][1,0]+=S.Rational(1,10**7);actions[1][1,4]-=S.Rational(1,10**7)
  E=C.exact_effects(actions,parts,gamma);cert=cert_from_exact(E,gamma,E['eta']);ch=C.digest(cert);model=K.compile_model(cert,expected_certificate_sha256=ch,expected_tolerance='1/100');ck(model['status']=='PASS_EXACT_CANONICAL_COMPUTATIONAL_MDP');mh=C.digest(model);X=C.matrix(model['X']);d=S.Rational(model['canonical_gap']);beta=S.Rational(model['canonical_discount']);ck(all(-1<=x<=1 for x in X));ck(d>0 and beta==1-d)
  for a,Pstr in enumerate(model['transitions']):
   P=C.matrix(Pstr);ck(P*S.ones(r+1,1)==S.ones(r+1,1));ck(min(P)>=0);ck(P[r,r]==1)
  for task in range(5):
   g=S.Matrix(m,r,lambda a,j:S.Rational(rng.randrange(5),4));goals=C.serial(g);out=K.plan_model(cert,model,goals,expected_certificate_sha256=ch,expected_model_sha256=mh,expected_goal_sha256=C.digest(goals),expected_tolerance='1/100');ck(out['status']=='PASS_POLICY_REGRET');w=S.Matrix(list(map(S.Rational,out['w'])));ck(out['rho']=='0')
   rew=[(1-gamma)*Z*g.row(a).T for a in range(m)];vo=true_value(actions,rew,gamma);pi=out['policy'];A=S.Matrix(n,n,lambda i,j:actions[pi[which[i]]][i,j]);rr=S.Matrix([rew[pi[which[i]]][i] for i in range(n)]);vp=(S.eye(n)-gamma*A).inv()*rr;ck(min(vo-vp)>=0);ck(max(vo-vp)<=S.Rational(out['regret_bound']))
  # Separately check exact raw common-reset model, using common state rewards only.
  Dmin=S.Matrix(r,r,lambda j,k:min(D[j,k] for D in Ds));bg=A0+Z*Dmin*W;s=-Dmin*S.ones(r,1);SS=S.diag(*s);DD=S.diag(*list(S.ones(n,1)-Z*s));G=(S.eye(n)-gamma*bg).inv();Rs=[D-Dmin for D in Ds]
  ck(min(s)>0);ck(min(bg)>=0);ck(max(bg*S.ones(n,1))<=1)
  T=[gamma*SS.inv()*R*W*G*Z*SS for R in Rs]
  for a in range(m):ck(raw[a]==bg+Z*Rs[a]*W);ck(min(T[a])>=0);ck(max(T[a]*S.ones(r,1))<=gamma)
  g=S.Matrix([S.Rational(1,4),1,S.Rational(1,2)]);f=(1-gamma)*Z*g;b=[(1-gamma)*g+gamma*SS.inv()*R*W*G*DD*f for R in Rs]
  # T has row sums <=gamma; add cemetery to independently invoke stochastic PI.
  trans=[];rewards=[]
  for a in range(m):
   P=S.zeros(r+1);P[:r,:r]=T[a]/gamma
   for j in range(r):P[j,r]=1-sum(P.row(j))
   P[r,r]=1;trans.append(P);rewards.append(S.Matrix(list(b[a])+[0]))
  u=true_value(trans,rewards,gamma)[:r,0];v=G*(Z*SS*u+DD*f);ck(v==true_value(raw,[f]*m,gamma));models.append({'case':case,'gamma':str(gamma),'canonical_discount':str(beta),'eta':str(E['eta'])})
 # Raw reset zero-mass rows: restrict decision indices; no inverse of zero s.
 n=3;A0=S.ones(n)/3;D=S.Matrix([[0,0,0],[S.Rational(1,10),-S.Rational(1,10),0],[-S.Rational(1,10),0,S.Rational(1,10)]]);raw=[A0,A0+D];Dm=S.Matrix(n,n,lambda i,j:min(0,D[i,j]));bg=A0+Dm;s=-Dm*S.ones(n,1);idx=[i for i in range(n) if s[i]>0];Zp=S.eye(n)[:,idx];SS=S.diag(*[s[i] for i in idx]);gamma=S.Rational(2,3);G=(S.eye(n)-gamma*bg).inv();DD=S.diag(*list(S.ones(n,1)-s));Rs=[(Da-Dm)[idx,:] for Da in [S.zeros(n),D]];f=(1-gamma)*S.Matrix([1,S.Rational(1,4),0]);T=[gamma*SS.inv()*R*G*Zp*SS for R in Rs];b=[f[idx,0]+gamma*SS.inv()*R*G*DD*f for R in Rs];trans=[];rewards=[]
 for a in range(2):
  P=S.zeros(3);P[:2,:2]=T[a]/gamma
  for j in range(2):P[j,2]=1-sum(P.row(j))
  P[2,2]=1;trans.append(P);rewards.append(S.Matrix(list(b[a])+[0]))
 u=true_value(trans,rewards,gamma)[:2,0];v=G*(Zp*SS*u+DD*f);ck(s[0]==0);ck(v==true_value(raw,[f]*2,gamma))
 # Immediate-decision beta=0 branch, arbitrary action rewards.
 E=C.exact_effects([S.ones(1)]*3,[[0]],S.Rational(9,10));cert=cert_from_exact(E,S.Rational(9,10));ch=C.digest(cert);model=K.compile_model(cert,expected_certificate_sha256=ch,expected_tolerance='0');ck(model['canonical_discount']=='0');goals=[['0'],['1/3'],['1']];mh=C.digest(model)
 out=K.plan_model(cert,model,goals,expected_certificate_sha256=ch,expected_model_sha256=mh,expected_goal_sha256=C.digest(goals),expected_tolerance='0');ck(out['policy']==[2]);ck(out['w']==['1'])
 def plan(mod=model,goal=goals,core=cert,cht=ch,mht=None,ght=None,tol='0'):
  return K.plan_model(core,mod,goal,expected_certificate_sha256=cht,expected_model_sha256=C.digest(mod) if mht is None else mht,expected_goal_sha256=C.digest(goal) if ght is None else ght,expected_tolerance=tol)
 reject(lambda:plan(cht='wrong'));reject(lambda:plan(mht='wrong'));reject(lambda:plan(ght='wrong'));reject(lambda:plan(tol='-1'))
 for key,value in [('canonical_discount','1'),('canonical_gap','1/2'),('X',[['0']]),('source_certificate_sha256','wrong')]:
  bad=copy.deepcopy(model);bad[key]=value;reject(lambda bad=bad:plan(mod=bad))
 for goal in [[['2'],['0'],['0']],[['-1'],['0'],['0']],[['0']],[['0.0'],['0'],[True]]]:reject(lambda goal=goal:plan(goal=goal))
 bad=copy.deepcopy(model);bad['transitions'][0][0][0]='2';reject(lambda:plan(mod=bad))
 # Backend status/objective is not trusted: zero-gap and infeasible proposals refuse.
 old=K.linprog
 try:
  K.linprog=lambda *args,**kwargs:(S.Integer(0),[S.Integer(1),S.Integer(0)])
  ck(K.compile_model(cert,expected_certificate_sha256=ch,expected_tolerance='0')['status']=='UNKNOWN_NO_POSITIVE_TRANSFORM')
  K.linprog=lambda *args,**kwargs:(S.Integer(-999),[S.Integer(3),S.Integer(1)])
  ck(K.compile_model(cert,expected_certificate_sha256=ch,expected_tolerance='0')['status']=='UNKNOWN_INFEASIBLE_BACKEND_PROPOSAL')
  # A suboptimal positive feasible half-scale transform is sufficient.
  K.linprog=lambda *args,**kwargs:(S.Integer(777),[S.Rational(3,2),S.Rational(1,2)])
  half=K.compile_model(cert,expected_certificate_sha256=ch,expected_tolerance='0');ck(half['status']=='PASS_EXACT_CANONICAL_COMPUTATIONAL_MDP');ck(half['canonical_gap']=='1/2');ck(plan(mod=half)['w']==['1'])
 finally:K.linprog=old
 return {'status':'PASS_INDEPENDENT_CANONICAL_CHECKS','exact_checks':checks,'refusals':refusals,'random_models':12,'action_reward_tasks':60,'raw_common_reset_tasks':12,'source_calls':0,'models':models}
if __name__=='__main__':print(json.dumps(run(),indent=2))
