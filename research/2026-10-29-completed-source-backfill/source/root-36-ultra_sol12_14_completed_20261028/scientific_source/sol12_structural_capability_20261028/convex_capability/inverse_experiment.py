"""Qualified compatible-jet inverse with paid exact candidate conditioning.

The same numerical proposal/data feed both receivers. The14 contact margin
is accepted only by exact LDL; no eigensolver or optimizer accuracy is used.
The original energy/selector and180 Gram are frozen scientific inputs.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import itertools,json,math,time
from fractions import Fraction as Q
from pathlib import Path
MODULE_STARTED=time.monotonic()
import numpy as np
import scipy.linalg as la
import scipy.optimize as opt
import sympy as sp
OUT=Path(__file__).resolve().parent
WORK=OUT.parents[1]
SOURCE=WORK/'sol8_opportunity_selection_20261027/rational_selector/EXACT_RATIONAL_SUPPORT.json'
RAW=json.loads(SOURCE.read_text())
CW=itertools.combinations_with_replacement
A=sp.symbols('a b c d');a,b,c,d=A
u,v,w,q=a*a+c*c,b*b+d*d,a*b+c*d,a*d-b*c
T=u+v;x,y,z=u-v,2*w,2*q
F=sp.expand(sum(sp.Rational(t)*m for t,m in zip(RAW['target_coefficients'],
 [u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w])))
p=sp.expand(sum(sp.Rational(t)*m for t,m in zip(RAW['selector_coefficients'],
 [x**3,x*x*z,x*z*z,z**3,x*y*y,y*y*z])))
k=p/T**2;cof=[d,-c,-b,a]
JET=[sp.diff(F,t)-k*h for t,h in zip(A,cof)]+[k]
JAC=sp.Matrix(JET).jacobian(A)
def rational(t):return Q(int(t.p),int(t.q))
def literal(poly):return{ex:rational(cc)for ex,cc in sp.Poly(poly,*A).terms()}
FC=literal(F);PC=literal(p);GC=[literal(sp.diff(F,t))for t in A]
def serial(t):
 t=Q(t);return str(t.numerator)+'/'+str(t.denominator)
def peval(poly,point):return sum(vv*math.prod(t**n for t,n in zip(point,ex))for ex,vv in poly.items())
def jet(point):
 norm=sum(t*t for t in point)
 if not norm:return[Q(0)]*5
 selector=peval(PC,point)/(norm*norm)
 co=[point[3],-point[2],-point[1],point[0]]
 return[peval(g,point)-selector*h for g,h in zip(GC,co)]+[selector]
def ldl(mat):
 n=len(mat);L=[[Q(0)for _ in range(n)]for _ in range(n)];piv=[]
 for i in range(n):
  t=mat[i][i]-sum(L[i][j]**2*piv[j]for j in range(i))
  if t<=0:return None
  piv.append(t);L[i][i]=1
  for h in range(i+1,n):
   L[h][i]=(mat[h][i]-sum(L[h][j]*L[i][j]*piv[j]for j in range(i)))/t
 return min(piv)

def contact_margin(point):
 begin=time.monotonic();common=math.lcm(*(t.denominator for t in point))
 integer=[int(t*common)for t in point];norm_integer=sum(t*t for t in integer)
 columns=[];weights=[]
 for aa in CW(range(4),3):
  for ii in range(4):columns.append(ii);weights.append(math.prod(integer[i]for i in aa))
 for aa in CW(range(4),2):
  for j,xx in enumerate(CW(range(4),2)):
   columns.append(4+j);weights.append(common*math.prod(integer[i]for i in aa))
 assert len(columns)==180
 gram=[[0 for _ in range(14)]for _ in range(14)]
 for i in range(180):
  if not weights[i]:continue
  for j in range(180):
   if weights[j]:gram[columns[i]][columns[j]]+=weights[i]*weights[j]*RAW['gram_integer_matrix'][i][j]
 denominator=RAW['gram_denominator']*common**2*norm_integer**2
 exact=[[Q(t,denominator)for t in row]for row in gram]
 numeric=np.array(exact,dtype=float)
 schur=numeric[:4,:4]-numeric[:4,4:]@la.solve(numeric[4:,4:],numeric[4:,:4],assume_a='pos')
 suggested=float(la.eigvalsh(schur)[0]);assert suggested>0
 mu=Q(max(1,math.floor(.9*suggested*10**9)),10**9);attempts=0
 while True:
  attempts+=1
  pivot=ldl([[vv-(mu if i==j and i<4 else 0)for j,vv in enumerate(row)]for i,row in enumerate(exact)])
  if pivot is not None:break
  mu/=2
  assert attempts<20
 return mu,{'mu':serial(mu),'Schur_minimum_diagnostic':suggested,
   'minimum_exact_LDL_pivot':serial(pivot),'LDL_attempts':attempts,
   'Gram_denominator':str(denominator),'Gram_numerators':gram,
   'seconds':time.monotonic()-begin,'numeric_accuracy_assumed':False}

def receiver(point,data,noise_bound,mu):
 residual=sum(abs(x-y)for x,y in zip(jet(point),data));rho=residual+noise_bound
 norm=sum(t*t for t in point);C=1+norm/2
 assert C*C>=1+norm
 beta=Q(1,1600000)
 lower,upper=Q(0),Q(1)
 if not rho:upper=Q(0)
 else:
  while upper*(mu+beta*upper*upper)<rho*(C+upper/2):upper*=2
  for _ in range(120):
   middle=(lower+upper)/2
   if middle*(mu+beta*middle*middle)<rho*(C+middle/2):lower=middle
   else:upper=middle
 error=upper
 linear=None
 if rho<2*mu:
  linear=C*rho/(mu-rho/2);error=min(error,linear)
 return{'status':'GLOBAL_COMPATIBLE_STATE_ERROR_BOUND','rho':serial(rho),
  'residual_l1':serial(residual),'known_noise_l1':serial(noise_bound),
  'C':serial(C),'mu':serial(mu),'state_error_upper':serial(error),
  'error_display_only':float(error),'prior_state_radius_assumed':False,
  'global_quartic_margin':serial(beta),'cubic_root_bracket':[serial(lower),serial(upper)],
  'rational_bisections':120,'linear_regime_threshold_met':linear is not None,
  'linear_regime_bound':serial(linear)if linear is not None else None}

def ivadd(a,b):return a[0]+b[0],a[1]+b[1]
def ivmul(a,b):
 values=[x*y for x in a for y in b];return min(values),max(values)
def ivpow(a,n):
 out=(Q(1),Q(1))
 for _ in range(n):out=ivmul(out,a)
 return out
def iveval(poly,box):
 out=(Q(0),Q(0))
 for ex,c in poly.items():
  value=(c,c)
  for xx,n in zip(box,ex):value=ivmul(value,ivpow(xx,n))
  out=ivadd(out,value)
 return out
def cube_interval(interval,bits=110):
 assert interval[0]>0;scale=1<<bits
 lo=int(sp.integer_nthroot(interval[0].numerator*scale**3//interval[0].denominator,3)[0])
 hi=int(sp.integer_nthroot(interval[1].numerator*scale**3//interval[1].denominator,3)[0])+1
 return Q(lo,scale),Q(hi,scale)
def record_interval(xx):return{'lower':serial(xx[0]),'upper':serial(xx[1]),'display_only':list(map(float,xx))}

def stress_ambiguity():
 """Exact ratio polynomial plus rational isolating boxes; no float-root premise."""
 begin=time.monotonic();t=sp.symbols('t')
 subs={a:1,b:0,c:0,d:t}
 P=sp.expand(sp.diff(F,a).subs(subs));R=sp.expand(sp.diff(F,d).subs(subs))
 Sa,Sd=P.subs(t,1),R.subs(t,1)
 ratio=sp.Poly(Sa*R-Sd*P,t)
 quotient,remainder=sp.div(ratio,sp.Poly(t-1,t));assert remainder.is_zero
 quadratic=quotient.clear_denoms()[1].primitive()[1]
 if quadratic.LC()<0:quadratic=-quadratic
 assert quadratic.degree()==2 and sp.discriminant(quadratic)>0
 assert sp.diff(F,b).subs({b:0,c:0})==0
 assert sp.diff(F,c).subs({b:0,c:0})==0
 roots=[]
 for (lo,hi),multiplicity in sp.polys.polytools.intervals(quadratic,eps=sp.Rational(1,10**40)):
  assert multiplicity==1 and quadratic.eval(lo)*quadratic.eval(hi)<0
  roots.append((rational(lo),rational(hi)))
 roots.append((Q(1),Q(1)));roots.sort()
 pcoeff={ (n,):rational(vv)for (n,),vv in sp.Poly(P,t).terms()}
 rows=[];jetboxes=[]
 for tt in roots:
  pi=iveval(pcoeff,[tt]);assert pi[0]>0
  ai=cube_interval((rational(Sa)/pi[1],rational(Sa)/pi[0]));di=ivmul(ai,tt)
  box=[ai,(Q(0),Q(0)),(Q(0),Q(0)),di]
  ti=ivadd(ivpow(ai,2),ivpow(di,2));ti2=ivpow(ti,2)
  ki=ivmul(iveval(PC,box),(1/ti2[1],1/ti2[0]))
  j0=ivadd((rational(Sa),)*2,ivmul((-ki[1],-ki[0]),di))
  j3=ivadd((rational(Sd),)*2,ivmul((-ki[1],-ki[0]),ai))
  jb=[j0,(Q(0),Q(0)),(Q(0),Q(0)),j3,ki];jetboxes.append(jb)
  determinant=ivmul(ai,di)
  rows.append({'ratio_t':record_interval(tt),'a':record_interval(ai),'d':record_interval(di),
               'determinant':record_interval(determinant),'orientation_preserving':determinant[0]>0,
               'jet':[record_interval(h)for h in jb]})
 for i in range(3):
  for j in range(i+1,3):
   assert any(x[1]<y[0]or y[1]<x[0]for x,y in zip(jetboxes[i],jetboxes[j]))
 return {'status':'EXACT_THREE_STATE_STRESS_AMBIGUITY','common_stress':[serial(rational(Sa)),'0/1','0/1',serial(rational(Sd))],
   'ratio_quadratic_coefficients':list(map(str,quadratic.all_coeffs())),
   'identity':'ratio=t=d/a; a^3=Sa/P(t); (Sa R(t)-Sd P(t))=0 proves both diagonal stresses exactly',
   'branches':rows,'orientation_preserving_branches':sum(r['orientation_preserving']for r in rows),
   'all_distinct_jets_proved_by_disjoint_rational_intervals':True,
   'seconds':time.monotonic()-begin}

def verify_contact(point,record):
 exact=[[Q(t,int(record['Gram_denominator']))for t in row]for row in record['Gram_numerators']]
 features=[tuple(int(j==i)for j in range(4))for i in range(4)]
 features+=[tuple(ii.count(i)for i in range(4))for ii in CW(range(4),2)]
 rebuilt={}
 for i,ex in enumerate(features):
  for j in range(i,14):
   ee=tuple(x+y for x,y in zip(ex,features[j]));value=exact[i][j]*(1 if i==j else 2)
   rebuilt[ee]=rebuilt.get(ee,Q(0))+value
 norm=sum(x*x for x in point);selector=peval(PC,point)/norm**2
 shifted=F.subs({t:t+sp.Rational(vv)for t,vv in zip(A,point)},simultaneous=True)
 target=sp.expand(shifted-sp.Rational(peval(FC,point))
  -sum(sp.Rational(peval(g,point))*x for g,x in zip(GC,A))-sp.Rational(selector)*q)
 assert{ex:v for ex,v in rebuilt.items()if v}==literal(target)
 return True

def inverse_gauge_comparison():
 begin=time.monotonic();kappa=Q(1,20000000);eps=Q(1,100);e=eps-kappa
 qs=literal(q);features=[tuple(ii.count(i)for i in range(4))for ii in CW(range(4),2)]
 qv=[qs.get(ex,Q(0))for ex in features]
 g=[[Q(RAW['gram_integer_matrix'][80+i][80+j],RAW['gram_denominator'])
       -kappa*qv[i]*qv[j]for j in range(10)]for i in range(10)]
 pivot=ldl(g);assert pivot is not None
 rebuilt={}
 for i,aa in enumerate(features):
  for j in range(i,10):
   key=tuple(x+y for x,y in zip(aa,features[j]));v=g[i][j]*(1 if i==j else 2)
   rebuilt[key]=rebuilt.get(key,Q(0))+v
 assert{ex:v for ex,v in rebuilt.items()if v}==literal(F-sp.Rational(kappa)*q*q)
 normal=WORK/'sol11_operation_discovery_20261028/parent/normal_strip/RESULT.json'
 source=json.loads(normal.read_text())
 assert source['status']=='LITERAL_NORMAL_STRIP_CERTIFIED'
 assert Q(source['kappa'])==kappa and Q(source['epsilon_original'])==eps
 ss=Q(1,10000);ww=2*kappa*ss
 assert ss<Q(source['normal_halfwidth'])and abs(ww)<2*e
 newvalue=kappa*ss*ss
 return{'same_physical_graph_energy':'F+epsilon*T, epsilon1/100',
  'same_force':['0/1']*4+[serial(ww)],
  'new70_inverse':['0/1']*4+[serial(ss)],'new70_conjugate':serial(newvalue),
  'old_compensated15_inverse':['0/1']*5,'old_compensated15_conjugate':'0/1',
  'old15_H_Gram_exact_LDL_pivot':serial(pivot),
  'old15_H_Gram_literal_identity':True,'quadratic_margin_e_minus_absw_over2':serial(e-abs(ww)/2),
  'new70_frozen_input':str(normal),'new70_input_reacquired':False,
  'seconds':time.monotonic()-begin,
  'interpretation':'Different auxiliary responses for identical physical graph energy. No accuracy ranking or intrinsic physical normal response follows.'}

def main():
 setup_seconds=time.monotonic()-MODULE_STARTED;started=time.monotonic()
 ambiguity=stress_ambiguity();gauge=inverse_gauge_comparison();compile_begin=time.monotonic()
 jfloat=sp.lambdify(A,JET,'numpy',cse=True)
 jjac=sp.lambdify(A,JAC,'numpy',cse=True)
 compile_seconds=time.monotonic()-compile_begin
 truth=[Q(1),Q(0),Q(0),Q(1)]
 noise=[Q(h,10**12)for h in [1,-1,1,-1,1]]
 noise_bound=sum(map(abs,noise));data=[x+y for x,y in zip(jet(truth),noise)]
 target=np.array(data,dtype=float)
 branch=ambiguity['branches'][-1]
 seeds=[('other_exact_stress_branch',
          [sum(branch['a']['display_only'])/2,0,0,sum(branch['d']['display_only'])/2]),
        ('nearby_nondegenerate_state',[.8,0,0,1.2])]
 trials=[]
 for name,seed in seeds:
  begin=time.monotonic()
  solution=opt.least_squares(lambda aa:np.array(jfloat(*aa),dtype=float)-target,
    seed,jac=lambda aa:np.array(jjac(*aa),dtype=float),
    ftol=1e-14,xtol=1e-14,gtol=1e-13,max_nfev=300)
  proposal_seconds=time.monotonic()-begin
  proposal=[Q(round(float(x)*(1<<46)),1<<46)for x in solution.x]
  mu,contact=contact_margin(proposal)
  verify_begin=time.monotonic();identity=verify_contact(proposal,contact)
  identity_seconds=time.monotonic()-verify_begin
  certified=receiver(proposal,data,noise_bound,mu)
  coarse=receiver(proposal,data,noise_bound,sum(x*x for x in proposal)/2400000)
  true_squared_error=sum((x-y)**2 for x,y in zip(proposal,truth))
  if certified['status']=='GLOBAL_COMPATIBLE_STATE_ERROR_BOUND':
   assert true_squared_error<=Q(certified['state_error_upper'])**2
  if coarse['status']=='GLOBAL_COMPATIBLE_STATE_ERROR_BOUND':
   assert true_squared_error<=Q(coarse['state_error_upper'])**2
  row={'seed_name':name,'seed_display':seed,'proposal':[serial(x)for x in proposal],
   'proposal_seconds':proposal_seconds,'function_evaluations':solution.nfev,
   'optimizer_status_diagnostic':int(solution.status),'optimizer_accuracy_trusted':False,
   'contact':contact,'literal_contact_identity':identity,
   'literal_contact_identity_seconds':identity_seconds,
   'new_receiver':certified,'matched_coarse_receiver':coarse,
   'ground_truth_squared_error_for_control_only':serial(true_squared_error)}
  if certified['status']==coarse['status']=='GLOBAL_COMPATIBLE_STATE_ERROR_BOUND':
   row['same_data_bound_improvement']=serial(Q(coarse['state_error_upper'])/Q(certified['state_error_upper']))
  trials.append(row)
  print(name,'nfev',solution.nfev,'mu',float(mu),'status',certified['status'],
        'error',certified.get('error_display_only'),flush=True)
 successes=[r for r in trials if r['new_receiver']['status']=='GLOBAL_COMPATIBLE_STATE_ERROR_BOUND'
            and r['new_receiver']['error_display_only']<1e-5]
 assert successes,'No usable compatible inverse acquired in bounded test'
 zero_fallback=receiver([Q(0)]*4,data,noise_bound,Q(0))
 assert Q(zero_fallback['state_error_upper'])**2>=2
 result={'status':'QUALIFIED_ORIGINAL_ENERGY_COMPATIBLE_INVERSE_ACQUIRED',
  'input_scope':{'energy':'original F; no epsilon quadratic modification',
   'selector':'p6/T^2, k(0)=0','source':str(SOURCE),
   'accepted_source_replay_seconds':RAW['seconds'],
   'source_acquisition_repeated':False,
   'certificate_input':'Global support identity and PSD R180 are accepted prior inputs; new work specializes and verifies14-Grams.'},
  'data_contract':'w is within supplied known l1 noise of j(B) for some compatible B; no prior B radius; this is five minor-conjugate coordinates, not four physical stresses.',
  'data':[serial(x)for x in data],'known_noise_l1':serial(noise_bound),
  'truth_for_control_only':[serial(x)for x in truth],
  'stress_ambiguity':ambiguity,'trials':trials,
  'offgraph_gauge_comparison':gauge,
  'flat_candidate_global_fallback':zero_fallback,
  'source_primitive70_used_for_new_receiver':False,'C2_lift_required_for_new_receiver':False,
  '70_specific_inverse_or_PDE_advantage':'NOT_ESTABLISHED_DEPRIORITIZED',
  'seconds':{'module_setup':setup_seconds,'jet_Jacobian_compile':compile_seconds,
   'experiment_with_controls':time.monotonic()-started,
   'module_elapsed_excluding_Python_startup':time.monotonic()-MODULE_STARTED},
  'scientific_scope':'A global residual receiver and bounded noisy-data execution under explicit compatible-data promise. No universal inverse proposal solver, physical measurement protocol, PDE solver, historical priority or70-specific advantage established.'}
 (OUT/'INVERSE_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'status':result['status'],'seconds':result['seconds'],
   'successes':len(successes),'stress_branch_count':len(ambiguity['branches'])},indent=2))

if __name__=='__main__':main()
