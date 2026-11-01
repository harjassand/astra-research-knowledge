from fractions import Fraction as F
from pathlib import Path
from copy import deepcopy
import json,random
import sympy as sp
import receive_survival as c
checks=0;categories={}
def ok(x,label):
 global checks
 assert x,label
 checks+=1;categories[label]=categories.get(label,0)+1
def unknown(fn,label):
 try:fn()
 except c.Unknown:ok(True,label)
 else:raise AssertionError('unexpected admission: '+label)
rng=random.Random(2259)
# Analytic identities used by the all-time bound, not a sampled time grid proof.
x,t,s=sp.symbols('x t s',positive=True)
ok(sp.simplify(sp.diff(sp.log(x)-1+1/x,x)-(x-1)/x**2)==0,'global logarithm comparison derivative')
ok(sp.simplify((x-1)**2/x-(x-1-sp.log(x))-(sp.log(x)-1+1/x))==0,'Taylor to harmonic-moment comparison')
ok(sp.simplify(sp.integrate((x-t)/t**2,(t,1,x))-(x-1-sp.log(x)))==0,'right Taylor remainder integral')
ok(sp.simplify(sp.integrate((t-x)/t**2,(t,x,1))-(-sp.log(x)-1+x))==0,'left Taylor remainder integral')
ok(sp.simplify(sp.diff(s*s*sp.exp(-s*t),s)-s*sp.exp(-s*t)*(2-s*t))==0,'global second-derivative supremum calculus')
ok(sum((F(1),F(1),F(1,2),F(1,6),F(1,24)))>F(8,3),'exact Taylor lower bound on Euler number')
ok(F(3,8)+F(9,16)==F(15,16)<1,'uniform spectral constant strictly below one')
# Spectral arithmetic/harmonic moments require no spectral support gap.
for _ in range(600):
 n=rng.randrange(2,9);weights=[F(rng.randrange(1,30))for i in range(n)];z=sum(weights);weights=[w/z for w in weights]
 vals=[F(rng.randrange(1,100),rng.randrange(1,100))for i in range(n)];mean=sum((w*x for w,x in zip(weights,vals)),F(0));vals=[x/mean for x in vals]
 ex=sum((w*x for w,x in zip(weights,vals)),F(0));inv=sum((w/x for w,x in zip(weights,vals)),F(0));eps=inv-1
 ok(ex==1 and eps>=0,'positive normalized spectral moments')
 ok(sum((w*(x-1)**2/x for w,x in zip(weights,vals)),F(0))==eps,'exact spectral defect identity')
# Exact initialization comparison for positive self-adjoint L2 contractions.
for _ in range(500):
 n=rng.randrange(2,15);a=rng.randrange(1,n);h=[F(1)]*a+[F(rng.randrange(0,11),10)for i in range(n-a)]
 kill=F(rng.randrange(1,10),10);mix=F(rng.randrange(0,11),10)
 def P(v):return [kill*(mix*x+(1-mix)*sum(v)/n)for x in v]
 av=[F(1)]*a+[F(0)]*(n-a);dv=[F(1)]*n;gv=[h[i]-av[i]for i in range(n)];rv=[1-hh for hh in h]
 dot=lambda x,y:sum((u*v for u,v in zip(x,y)),F(0))
 left=dot(av,P(dv))-dot(h,P(h));term1=dot(av,P(rv));term2=dot(gv,P(h));N=dot(h,h);M=F(a);S=F(n-a)
 ok(left==term1-term2 and term1>=0 and term2>=0,'exact positive A-versus-committor numerator decomposition')
 ok(left*left<=N*S,'max not sum initialization norm bound')
 ok(M<=N<=M+S and 0<=dot(h,P(h))/N<=1,'normalization and contraction bounds')
# Rational interval rate midpoint comparison, all terms exact.
for _ in range(800):
 kl=F(rng.randrange(1,100),rng.randrange(1,100));kh=kl+F(rng.randrange(1,100),rng.randrange(1,100));km=(kl+kh)/2
 k0=kl+(kh-kl)*F(rng.randrange(0,101),100)
 ok(abs(km-k0)/min(km,k0)<=(kh/kl-1)/2,'single reference midpoint rate uncertainty')
# Directed exponential primitive compared to independent rigorous alternating sums.
for _ in range(100):
 xx=F(rng.randrange(1,1000),1000);fx=c.base.Fixed(128,100000,10000,1000,1);lo,hi=fx.expminus(xx)
 term=F(1);s=F(1);upper=None
 for j in range(1,162):
  term=-term*xx/j;s+=term
  if j==160:upper=s
 lower=s
 ok(F(lo,fx.S)<=lower<=upper<=F(hi,fx.S),'outward exp contains rigorous rational alternating enclosure')
# Use a cheap valid small task; altered inputs never inherit old model semantics.
raw=c.fixture(64);task={'times':[F(0),F(1000),F(10000)],'ks_error':F(3,10),'query_absolute_width':F(3,5),'quad_relative':F(1,20),'full_ratio':F(6,5)}
cert=c.certify(raw,**task);ok(c.verify(raw,cert,**task)['status']=='PASS','literal small original-task complete replay')
for key in ['ks_error','query_absolute_width','beta','kappa','quad_relative','full_ratio']:
 for bad in [True,1,1.0,float('nan'),None,F(0),F(-1)]:
  tt=dict(task);tt[key]=bad;unknown(lambda tt=tt:c.certify(raw,**tt),'strict external exact rational type')
for key in ['precision_bits','max_queries','max_exp_terms','max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_rational_bits','max_grid','max_points','max_cutoff','max_precision','max_operations','max_integer_bits']:
 for bad in [True,1.0,None,0,-1]:
  tt=dict(task);tt[key]=bad;unknown(lambda tt=tt:c.certify(raw,**tt),'strict external resource type')
for bad in [None,(),[True],[1],[1.0],[float('nan')],[F(-1)]]:
 tt=dict(task);tt['times']=bad;unknown(lambda tt=tt:c.certify(raw,**tt),'strict complete finite time-query interface')
for key,value in [('max_queries',1),('max_exp_terms',1),('precision_bits',1),('max_precision',32),('max_integer_bits',32),('max_operations',1)]:
 tt=dict(task);tt[key]=value;unknown(lambda tt=tt:c.certify(raw,**tt),'finite extra/base budget UNKNOWN')
for key,value in [('ks_error',F(1)),('query_absolute_width',F(2)),('ks_error',F(1,100000)),('query_absolute_width',F(1,100000))]:
 tt=dict(task);tt[key]=value;unknown(lambda tt=tt:c.certify(raw,**tt),'honest total KS/query-width failure')
# The outer operation budget is SHARED, not reset for query execution.
base_work=cert['mean_certificate']['work']['fixed_operations'];tt=dict(task);tt['max_operations']=base_work
unknown(lambda:c.certify(raw,**tt),'extra exponential products cannot exceed shared total budget')
tt0=dict(tt);tt0['times']=[];law=c.certify(raw,**tt0)
ok(law['work']['total_fixed_operations']==base_work,'no-query law needs no hidden exp operation budget')
for mutation in ['delta','reference','rate_enclosure','rho','spectral','rate_error','root_error','init','generator','observable','uniform_statement','query_time','query_lower','query_upper','root_proof','corollary_proof','model','nested_endpoint','nested_task','nested_bool','task','extra_field']:
 cc=deepcopy(cert)
 if mutation=='delta':cc['uniform_KS_error_upper']='0'
 elif mutation=='reference':cc['reference_exponential_rate']='1'
 elif mutation=='rate_enclosure':cc['exact_rate_enclosure']['lower']='1'
 elif mutation=='rho':cc['slab_mass_ratio_upper']='0'
 elif mutation=='spectral':cc['spectral_error_upper']='0'
 elif mutation=='rate_error':cc['finite_rate_error_upper']='0'
 elif mutation=='root_error':cc['initial_law_comparison_error_upper']='0'
 elif mutation=='init':cc['initialization']='fixed ray'
 elif mutation=='generator':cc['actual_full_generator']='CIR'
 elif mutation=='observable':cc['observable']='capacity'
 elif mutation=='uniform_statement':cc['uniform_statement']='relative tail error'
 elif mutation=='query_time':cc['queries'][1]['time']='1'
 elif mutation=='query_lower':cc['queries'][1]['cdf']['lower']='1'
 elif mutation=='query_upper':cc['queries'][1]['cdf']['upper']='0'
 elif mutation=='root_proof':cc['root_theorem_sha256']='0'*64
 elif mutation=='corollary_proof':cc['finite_rate_corollary_sha256']='0'*64
 elif mutation=='model':cc['mean_certificate']['acquisition']['mobility_floor']='1'
 elif mutation=='nested_endpoint':cc['mean_certificate']['mean_hitting_time']['upper']='1'
 elif mutation=='nested_task':cc['mean_certificate']['task']['beta']='2'
 elif mutation=='nested_bool':cc['mean_certificate']['acquisition']['transverse_SPD_everywhere']=1
 elif mutation=='task':cc['task']['ks_error']='1/2'
 else:cc['unproved_claim']=True
 unknown(lambda cc=cc:c.verify(raw,cc,**task),'strict all-time model/task/proof receiving: '+mutation)
cc=deepcopy(cert);cc['work']={};cc['seconds']='diagnostic';cc['mean_certificate']['work']={'fixed_operations':0};cc['mean_certificate']['seconds']=None;cc['queries'][1]['cdf']['display']=[]
ok(c.verify(raw,cc,**task)['status']=='PASS','diagnostic counters cannot control proof or budget recomputation')
rr=deepcopy(raw);rr['mobility_program']['value']='65';unknown(lambda:c.verify(rr,cert,**task),'actual raw mobility change cannot reuse certificate')
cc=deepcopy(cert);cc['mean_certificate']=cc;unknown(lambda:c.verify(raw,cc,**task),'malformed cyclic nested certificate refuses finitely')
# Actual saved all-time certificates and finite query endpoints fully recomputed.
rows=json.loads(Path('results.json').read_text());reports=[]
for row in rows:
 fi=row['fixture'];rr=c.fixture(fi['m'],F(fi['coupling']),F(fi['mobility']),fi['diagonal']);tt=c.original_task(fi['m']);cc=row['certificate']
 ok(c.verify(rr,cc,**tt)['status']=='PASS','all saved actual cases fully recomputed')
 err=F(cc['uniform_KS_error_upper']);target=tt.get('ks_error',F(1,200));width=tt.get('query_absolute_width',F(1,100))
 ok(err<=target,'external all-time KS conjunction')
 mean=cc['mean_certificate'];rho=F(mean['slab_to_basin_mass_ratio_upper']);eps=(1+rho)*F(mean['total_ratio_exact'])-1
 ok(eps==F(cc['spectral_error_upper']),'independent source mean to spectral defect arithmetic')
 ok(F(cc['exact_rate_enclosure']['lower'])<=F(cc['reference_exponential_rate'])<=F(cc['exact_rate_enclosure']['upper']),'actual acquired midpoint reference rate')
 for q,t in zip(cc['queries'],tt['times']):
  lo,hi=F(q['cdf']['lower']),F(q['cdf']['upper']);ok(F(q['time'])==t and 0<=lo<=hi<=1 and hi-lo<=width,'actual finite probability query original time and width')
 ok(cc['queries'][0]['cdf']['lower']==cc['queries'][0]['cdf']['upper']=='0','exact zero-time CDF identity')
 reports.append({'m':fi['m'],'KS_display':float(err),'queries':len(cc['queries']),'total_fixed_operations':cc['work']['total_fixed_operations']})
ok(rows[-1]['certificate']['queries']==rows[-2]['certificate']['queries']and rows[-1]['certificate']['uniform_KS_error_upper']==rows[-2]['certificate']['uniform_KS_error_upper'],'same outer law envelope for distinct raw angular/mobility models, not identical actual distributions')
report={'status':'PASS','checks':checks,'categories':categories,'saved_cases_recomputed':len(rows),'scope':'Author executable evidence only; root spectral theorem and whole wrapper independently pending','reports':reports}
Path('check_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
