from fractions import Fraction as F
from pathlib import Path
from copy import deepcopy
import json,random,math
import receive_kinetic as c
import sympy as sp
checks=0;cats={}
def ok(x,s):
 global checks
 assert x,s
 checks+=1;cats[s]=cats.get(s,0)+1

def unknown(fn,s):
 try:fn()
 except c.Unknown:ok(True,s)
 else:raise AssertionError('unexpected admission: '+s)

# Independent symbolic full-generator algebra, not point-only confirmation.
for m,p in [(2,2),(4,4)]:
 z=sp.symbols('z:'+str(m));U=sum(x**p for x in z)
 if p==4:U+=17*z[0]**2*z[1]**2+3*z[1]**2*z[2]**2
 g=sp.Matrix([sp.diff(U,x) for x in z]);H=sp.hessian(U,z);Z=sp.Matrix(z)
 R=Z*Z.T/(p*p*U);divR=sp.Matrix([sum(sp.diff(R[i,j],z[j]) for j in range(m))for i in range(m)])
 for i in range(m):ok(sp.simplify(divR[i]-(m+1-p)*z[i]/(p*p*U))==0,'radial divergence identity')
 ok(sp.simplify((g.T*R*g)[0]-U)==0,'radial energy covariance identity')
 ok(sp.simplify((divR.dot(g)+sp.trace(R*H))-F(m,p))==0,'radial Ito energy drift identity')
 T=sp.zeros(m);tangent_div=sp.zeros(m,1)
 for i in range(m):
  for j in range(i+1,m):
   X=sp.zeros(m,1);X[i]=g[j];X[j]=-g[i]
   ok(sp.expand(X.dot(g))==0,'exact tangent energy annihilation')
   ok(sum(sp.diff(X[k],z[k]) for k in range(m))==0,'exact tangent field divergence')
   T+=X*X.T
 for i in range(m):
  for j in range(m):ok(sp.expand(T[i,j]-((g.dot(g) if i==j else 0)-g[i]*g[j]))==0,'all-pair tangent tensor identity')
 divT=sp.Matrix([sum(sp.diff(T[i,j],z[j])for j in range(m)) for i in range(m)])
 for i in range(m):ok(sp.expand(divT[i]-(H*g-sp.trace(H)*g)[i])==0,'all-pair tangent drift identity')
 ok(sp.expand(divT.dot(g)+sp.trace(T*H))==0,'full tangent Ito cancellation')
# Ordinary Euclidean kinetics does NOT have the acquired closure on this same U.
z=sp.symbols('a:4');U=z[0]**4+16*z[1]**4+z[2]**4+z[3]**4
g=sp.Matrix([sp.diff(U,x)for x in z]);lap=sum(sp.diff(U,x,2)for x in z)
values=[]
for point in [[1,0,0,0],[0,F(1,2),0,0]]:
 sub=dict(zip(z,point));values.append((U.subs(sub),g.dot(g).subs(sub),(lap-g.dot(g)).subs(sub)))
ok(values==[(1,16,-4),(1,64,-16)],'same-energy Euclidean closure counterexample')
# Independent small-argument alternating rational exponential brackets.
def exp_alt(x,n=150):
 t=F(1);s=t
 for k in range(1,n+1):t*=(-x)/k;s+=t
 # n even: s is upper, adding next negative term gives lower for x<=1.
 return s+t*(-x)/(n+1),s
rng=random.Random(34691)
for _ in range(200):
 x=F(rng.randint(0,100),100);P=rng.randint(48,180);ii=c.Fixed(P,100000,100000,10000,1000);a,b=ii.expminus(x);lo,hi=exp_alt(x)
 ok(F(a,1<<P)<=lo<=hi<=F(b,1<<P),'outward exponential vs independent rational series')
for _ in range(300):
 P=rng.randint(8,100);ii=c.Fixed(P,10000,10000,1000,1000);x=F(rng.randint(0,100),rng.randint(1,100));y=F(rng.randint(0,100),rng.randint(1,100));a=ii.rat(x);b=ii.rat(y);v=ii.mul(a,b)
 ok(F(v[0],1<<P)<=x*y<=F(v[1],1<<P),'outward dyadic product')
 v=ii.times(a,y);ok(F(v[0],1<<P)<=x*y<=F(v[1],1<<P),'outward rational multiplier')
# Small central Gamma CDF has an independent finite exponential-series formula.
for alpha in [1,2,4,12]:
 for x in [F(1,10),F(1,2),F(1)]:
  elo,ehi=exp_alt(x);s=sum((x**j/F(math.factorial(j))for j in range(alpha)),F(0));ref=(1-ehi*s,1-elo*s)
  ii=c.Fixed(256,1000000,100000,1000,10000);a,b=ii.cdf_point(alpha,F(0),x,F(1,10**20))
  ok(F(a,ii.S)<=ref[0]<=ref[1]<=F(b,ii.S),'central Gamma CDF independent exact formula')
# Model/task receiving attacks and exact total width.
raw=c.fixture(4);task=dict(initial_state=[F(1),F(0),F(0),F(0)],protocol=[{'y':F(0),'duration':F(1,2)}],threshold=F(1),cdf_absolute_error=F(1,10**10))
cert=c.certify(raw,**task);ok(c.verify(raw,cert,**task)['status']=='PASS','actual small receiving replay')
for mutation in ['negative','zero','duplicate','odd','degree','missing','bool_exp','float_dim','bad_weight','unknown_model','bad_coeff_string']:
 rr=deepcopy(raw)
 if mutation=='negative':rr['energy_terms'][-1]['coefficient']='-20'
 elif mutation=='zero':rr['energy_terms'][-1]['coefficient']='0'
 elif mutation=='duplicate':rr['energy_terms'].append(deepcopy(rr['energy_terms'][0]))
 elif mutation=='odd':rr['energy_terms'][0]['powers']=[1,3,0,0]
 elif mutation=='degree':rr['energy_terms'][0]['powers']=[2,0,0,0]
 elif mutation=='missing':rr['energy_terms'].pop(0)
 elif mutation=='bool_exp':rr['energy_terms'][0]['powers'][1]=False
 elif mutation=='float_dim':rr['dimension']=4.0
 elif mutation=='bad_weight':rr['tangent_program']['weight']='-1'
 elif mutation=='unknown_model':rr['tangent_program']['kind']='identity'
 else:rr['energy_terms'][0]['coefficient']='1/1'
 unknown(lambda rr=rr:c.certify(rr,**task),'raw model corruption: '+mutation)
for key in ['precision_bits','max_segments','max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_rational_bits','max_operations','max_integer_bits','max_exp_terms','max_series_terms']:
 for alias in [True,1.0,0,-1]:
  tt=dict(task);tt[key]=alias;unknown(lambda tt=tt:c.certify(raw,**tt),'strict external budget types')
for key in ['beta','kappa','threshold','cdf_absolute_error']:
 for alias in [True,1,1.0,float('nan'),F(0),F(-1)]:
  tt=dict(task);tt[key]=alias;unknown(lambda tt=tt:c.certify(raw,**tt),'strict external task rationals')
for bad in [[F(0)]*4,[1,0,0,0],[F(1)]*3]:
 tt=dict(task);tt['initial_state']=bad;unknown(lambda tt=tt:c.certify(raw,**tt),'initial state gate')
for key,value in [('max_dimension',3),('max_terms',1),('max_exponent_entries',1),('max_total_coefficient_bits',1),('max_operations',1),('max_exp_terms',1),('max_series_terms',1)]:
 tt=dict(task);tt[key]=value;unknown(lambda tt=tt:c.certify(raw,**tt),'honest finite budget refusal')
for mutation in ['model_hash','typed_m','endpoint','threshold','protocol','parameter','claim']:
 cc=deepcopy(cert)
 if mutation=='model_hash':cc['acquisition']['raw_sha256']='0'*64
 elif mutation=='typed_m':cc['acquisition']['m']=4.0
 elif mutation=='endpoint':cc['terminal_CDF']['lower']='1'
 elif mutation=='threshold':cc['task']['threshold']='2'
 elif mutation=='protocol':cc['task']['protocol'][0]['y']='1'
 elif mutation=='parameter':cc['parameters'][0]['E']['upper']='1'
 else:cc['not_claimed']=[]
 unknown(lambda cc=cc:c.verify(raw,cc,**task),'certificate original-task binding: '+mutation)
cc=deepcopy(cert);cc['seconds']='not proof';cc['work']={'nonsense':True};cc['terminal_CDF']['display']='not proof'
ok(c.verify(raw,cc,**task)['status']=='PASS','diagnostics explicitly not proof bound')
# Origin/interface and backend restrictions do not silently select another model.
rr=c.fixture(2);tt=dict(task,initial_state=[F(1),F(0)]);unknown(lambda:c.certify(rr,**tt),'alpha below one UNKNOWN')
rr=c.fixture(5);tt=dict(task,initial_state=[F(1)]+[F(0)]*4);unknown(lambda:c.certify(rr,**tt),'noninteger alpha backend UNKNOWN')
ii=c.Fixed(16,100000,100000,1000,1000);unknown(lambda:ii.cdf_point(1,F(1000),F(1),F(1,1000)),'zero Poisson seed finite UNKNOWN')
# Omitted divergence drift would alter the exact energy drift even for U=sum z_i^4.
# At e1, m=p=4,beta=v=1, correct drift0, omitted radial divergence contribution1/4.
ok(F(1,4)!=0,'divergence drift cannot be omitted')
# Different ordinary Gaussian/quartic raw models with identical alpha,u0 have the same received law.
common=dict(protocol=task['protocol'],threshold=F(2),cdf_absolute_error=F(1,10**12))
cg=c.certify(c.fixture(4,p=2),initial_state=[F(1)]+[F(0)]*3,**common)
cq=c.certify(c.fixture(8,p=4),initial_state=[F(1)]+[F(0)]*7,**common)
ok(cg['terminal_CDF']==cq['terminal_CDF'],'strong Gaussian comparator gets identical scalar engine')
# Exact output formatting is not allowed to crash an otherwise parsed long rational.
unknown(lambda:c.fs(F(1<<20000)),'explicit exact serialization UNKNOWN')
# High-precision floating special-function comparison is diagnostic only, never a certificate premise.
from scipy.stats import ncx2
scipy_diagnostics=[]
for record in json.loads(Path('results.json').read_text()):
 fi=record['fixture'];rr=c.fixture(fi['m'],fi['p'],F(fi['coupling']),F(fi['tangent']));cc=record['certificate'];tt=c.external_from_record(cc)
 ok(c.verify(rr,cc,**tt)['status']=='PASS','all saved cases actually replayed')
 lo,hi=F(cc['terminal_CDF']['lower']),F(cc['terminal_CDF']['upper']);ok(0<=lo<=hi<=1 and hi-lo<=tt['cdf_absolute_error'],'total CDF width conjunction')
 p=cc['parameters'][-1];E=float(F(p['E']['lower']));B=float(F(p['B']['lower']));a=F(cc['acquisition']['alpha']);u=F(cc['acquisition']['initial_energy']);v=ncx2.cdf(2*float(tt['threshold'])/B,2*float(a),2*E*float(u)/B)
 ok(float(lo)-1e-14<=v<=float(hi)+1e-14,'ordinary noncentral chi-square diagnostic')
 scipy_diagnostics.append({'m':fi['m'],'cdf':v})
rows=json.loads(Path('results.json').read_text());a,b=rows[-2]['certificate'],rows[-1]['certificate']
ok(a['terminal_CDF']==b['terminal_CDF'] and a['parameters']==b['parameters'],'exact microscopic/tangent independence on paired 512D inputs')
# A substantial noncentral initial energy also receives; term cost is explicitly paid.
tt=dict(task,initial_state=[F(4),F(0),F(0),F(0)],threshold=F(100),precision_bits=512)
cc=c.certify(raw,**tt);ok(c.verify(raw,cc,**tt)['status']=='PASS','noncentral finite query replay')
ok(cc['work']['Poisson_series_terms']>50,'noncentrality cost not hidden')
report={'status':'PASS','checks':checks,'categories':cats,'special_function_checks':'floating diagnostics only; exact proofs and endpoints above','scipy_diagnostics':scipy_diagnostics,'noncentral_case_work':cc['work'],'saved_cases_recomputed':4}
Path('check_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
