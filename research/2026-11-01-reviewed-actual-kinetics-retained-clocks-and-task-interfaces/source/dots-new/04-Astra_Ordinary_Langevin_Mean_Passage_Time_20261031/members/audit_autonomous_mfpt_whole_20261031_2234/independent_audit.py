"""Independent exact core MFPT arithmetic, source formula and receiving audit."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import json,sys,random,time,math,hashlib,importlib.util,shutil
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'autonomous_radial_mfpt_20261031'))
import receive_mfpt as c
start=time.perf_counter();counts={};refusals=[]
def ok(b,k):
 if not b:raise AssertionError(k)
 counts[k]=counts.get(k,0)+1

def unknown(fn,k):
 try:fn()
 except c.Unknown as e:ok(True,k);refusals.append({'case':k,'reason':str(e)})
 else:raise AssertionError('false admission '+k)

def conv(a,b):
 out=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]+=x*y
 return out

def polynomial_resistance(alpha,kappa):
 # Direct coefficient integration of v(y)^alpha, not numerical quadrature.
 coeff=[F(1)];v=[1+kappa,0,-2*kappa,0,kappa]
 for _ in range(alpha):coeff=conv(coeff,v)
 return 2*sum((v*F(1,2)**(j+1)/(j+1)for j,v in enumerate(coeff)),F(0))

rng=random.Random(202610312234)
for _ in range(600):
 aa=rng.randrange(4,160);kap=F(rng.randrange(1,100),rng.randrange(1,100));P=rng.randrange(8,256)
 ii=c.Scalar(aa,kap,P,10000,100000,1000000);q=F(rng.randrange(1,1000),rng.randrange(1,1000));n=rng.randrange(0,200)
 l,u=ii.power(q,n);ok(F(l,ii.S)<=q**n<=F(u,ii.S),'independent exact integer-power enclosure')
for q in [F(1),F(2),F(1,2),F(1,2**300),F(2**300+1,2**300)]:
 for n in [0,1,2,3,127,128,129]:
  ii=c.Scalar(128,F(1),256,10000,100000,1000000);l,u=ii.power(q,n)
  ok(F(l,ii.S)<=q**n<=F(u,ii.S),'dyadic near-one underflow and exponent edge cases')
for aa in [4,5,16,32]:
 for kap in [F(1,20),F(1),F(9,2)]:
  ii=c.Scalar(aa,kap,384,100000,1000000,1000000)
  for a,b,kind in [(F(1,2),F(1),'q'),(F(1),F(2),'q'),(F(2),F(4),'q'),(F(0),F(1,2),'r')]:
   N=23;vals=[]
   for j in range(N+1):
    y=a+(b-a)*j/N;v=1+kap*(1-y*y)**2;vals.append(v**(-aa if kind=='q'else aa))
   lo=(b-a)/N*sum(min(x,y)for x,y in zip(vals,vals[1:]));hi=(b-a)/N*sum(max(x,y)for x,y in zip(vals,vals[1:]))
   l,u=ii.integrate(a,b,N,kind);ok(l<=lo<=hi<=u,'independent exact Darboux reference every region')
  exact=polynomial_resistance(aa,kap);l,u=ii.integrate(F(0),F(1,2),127,'r')
  ok(2*l<=exact<=2*u,'analytic full resistance integral')
  for T in [F(3,2),F(2),F(4),F(16)]:
   exact=T/F(4*aa-1)/(kap*(T*T-1)**2)**aa
   ok(ii.tail(T)>=exact,'full infinite mass tail independent formula')
# Scalar domains must enforce the proven monotonicity joins, not silently sample across them.
ii=c.Scalar(4,F(1),192,10000,100000,1000000)
for a,b,kind in [(F(1,2),F(2),'q'),(F(0),F(1),'q'),(F(0),F(1),'r'),(F(-1),F(0),'r')]:
 unknown(lambda a=a,b=b,kind=kind:ii.integrate(a,b,64,kind),'invalid monotonicity interval refusal')
# Full analytic estimates for every tail and slab point sampled rationally here;
# general all-point proof is reviewed separately, not inferred from these samples.
for aa in [4,7,16,128]:
 for kap in [F(1,10),F(1),F(7)]:
  d=F(1,aa);a=1+F(9,16)*kap;c1=1+kap*(1-(1+d)**2)**2
  ok(c1<=a and d<=F(1,4),'near-well alpha gate constants')
  for j in range(41):
   x=F(1,2)+(F(1,2)+d)*j/40;v=1+kap*(1-x*x)**2;vp=4*kap*x*(x*x-1)
   ok(v<=a and abs(vp)<=4*kap,'near-basin global profile bounds')
   t=F(j,5);x=1+d+t;v=1+kap*(1-x*x)**2;vp=4*kap*x*(x*x-1)
   ok(vp>=8*kap*(x-1) and 4*kap*(3*x*x-1)>0,'far-basin convex derivative bounds')
# Raw acquisition: witness e1 explicitly is NOT the observable initial state.
budgets={'max_dimension':1024,'max_terms':100000,'max_coefficient_bits':4096,'max_exponent_entries':64000000,'max_total_coefficient_bits':32000000,'max_rational_bits':1000000}
raw=c.fixture(16);aq,alpha,gamma=c.acquire(raw,**budgets)
ok(alpha==4 and gamma==512 and 'energy_probe_at_e1'in aq and 'initial_energy'not in aq,'algebraic witness not physical initialization')
for field,value in [('dimension',10**50),('dimension',True),('radial_gain','1/1'),('radial_gain',None),('radial_gain','9'*9000),('radial_gain','-1')]:
 r=deepcopy(raw);r[field]=value;unknown(lambda r=r:c.certify(r),'raw gamma dimension or oversized grammar refusal')
for mode in ['negative','zero','odd','duplicate','missing_pure','tail_extra','bad_tangent','extra_init']:
 r=deepcopy(raw)
 if mode=='negative':r['energy_terms'][-1]['coefficient']='-1'
 elif mode=='zero':r['energy_terms'][-1]['coefficient']='0'
 elif mode=='odd':r['energy_terms'][-1]['powers'][-1]=1
 elif mode=='duplicate':r['energy_terms'].append(deepcopy(r['energy_terms'][0]))
 elif mode=='missing_pure':r['energy_terms'].pop(0)
 elif mode=='tail_extra':r['energy_terms'][-1]['extra']=0
 elif mode=='bad_tangent':r['tangent_program']['kind']='constant_identity'
 else:r['initial_law']='point source'
 unknown(lambda r=r:c.certify(r),'complete actual-model raw refusal')
for key,v in [('max_dimension',16),('max_terms',aq['raw_terms']),('max_exponent_entries',aq['exponent_entries_read']),('max_total_coefficient_bits',aq['coefficient_bits_read'])]:
 bb=dict(budgets);bb[key]=v;ok(c.acquire(raw,**bb)[0]['raw_sha256']==aq['raw_sha256'],'exact raw resource boundary pass')
 bb[key]=v-1;unknown(lambda bb=bb:c.acquire(raw,**bb),'one-below raw resource boundary')
# Independent outward propagation of every source formula (9) component.
task={'beta':F(7,3),'kappa':F(3,2),'quad_relative':F(1,50),'full_ratio':F(10**9)}
cert=c.certify(raw,**task)
def check_formula(cc,beta,kappa,gamma,alpha):
 ml,mh=F(cc['basin_mass']['lower']),F(cc['basin_mass']['upper']);rl,rh=F(cc['slab_resistance']['lower']),F(cc['slab_resistance']['upper'])
 a=1+F(9,16)*kappa;d=F(1,alpha);c1=1+kappa*(1-(1+d)**2)**2
 S0=F(1,2)*a**alpha+d*c1**alpha;S1=(F(1,2)+d)*16*kappa*kappa*a**(alpha-3);W=1/(64*kappa*kappa*(alpha-1)**2*d);tf=1+4*kappa/(beta*gamma*a*a)
 values={'slab_with_transport':beta*mh*rh*tf,'basin_near_longitudinal':beta*mh*S0,'basin_far_longitudinal':beta*W/ml,'basin_near_radial':F(alpha)*mh*S1/gamma,'basin_far_radial':F(alpha)/(gamma*(alpha-1)**2)}
 for key,v in values.items():ok(F(cc['upper_components'][key])>=v,'each formula9 term independently outward')
 lower=beta*ml*rl;upper=(1+a**(-alpha)/ml)*sum(values.values(),F(0))
 ok(F(cc['mean_hitting_time']['lower'])==lower and F(cc['mean_hitting_time']['upper'])>=upper,'formula9 low exact and high outward')
 gotupper=(1+F(cc['slab_to_basin_mass_ratio_upper']))*sum(map(F,cc['upper_components'].values()),F(0))
 ok(gotupper==F(cc['mean_hitting_time']['upper']),'cross-source multiplier not omitted')
 ok(F(cc['total_ratio_exact'])==gotupper/lower,'full ratio exact reconstruction')
 ok(mh*rh<=(1+F(cc['task']['quad_relative']))*ml*rl,'numeric product distinct from source structural ratio')
 ok(0<F(cc['upper_components']['basin_far_radial']) and 0<F(cc['upper_components']['basin_far_longitudinal']),'basin tails remain positive paid corrections')
check_formula(cert,task['beta'],task['kappa'],gamma,alpha)
ok(c.verify(raw,cert,**task)['status']=='PASS','nonunit beta kappa original-task replay')
# Every proof-bearing field bound, notably source cross, true law and actual gain.
keys=['schema','dependency_sha256','task','acquisition','observable','actual_projected_generator','initialization','proof_method','not_claimed','total_ratio_exact','transport_factor_upper','slab_to_basin_mass_ratio_upper','upper_components','source_cross_multiplier_upper','constants','N','T','tail_upper','precision_bits']
for key in keys:
 for val in [None,True]:
  cc=deepcopy(cert);cc[key]=val;unknown(lambda cc=cc:c.verify(raw,cc,**task),'all proof fields null bool attacks')
for key in cert['acquisition']:
 cc=deepcopy(cert);cc['acquisition'][key]=None;unknown(lambda cc=cc:c.verify(raw,cc,**task),'all acquired model fields bound')
for key in cert['task']:
 cc=deepcopy(cert);cc['task'][key]=True;unknown(lambda cc=cc:c.verify(raw,cc,**task),'all original task fields bound')
for key in cert['upper_components']:
 cc=deepcopy(cert);cc['upper_components'][key]='0';unknown(lambda cc=cc:c.verify(raw,cc,**task),'every separate correction term bound')
for key in cert['constants']:
 cc=deepcopy(cert);cc['constants'][key]='0';unknown(lambda cc=cc:c.verify(raw,cc,**task),'every global tail and near constant bound')
for key in ['basin_mass','slab_resistance','mean_hitting_time']:
 for side in ['lower','upper']:
  for val in [None,True,1.0,'0']:
   cc=deepcopy(cert);cc[key][side]=val;unknown(lambda cc=cc:c.verify(raw,cc,**task),'all exact integral and mean endpoints bound')
r=deepcopy(raw);r['radial_gain']='1024';unknown(lambda:c.verify(r,cert,**task),'changed valid actual gain cannot reuse certificate')
cc=deepcopy(cert);cc['work']='untrusted';cc['seconds']=False;cc['mean_hitting_time']['display']=-1;cc['extra_field']='ignored'
ok(c.verify(raw,cc,**task)['status']=='PASS','diagnostics not falsely authenticated')
# Budget boundaries and TOTAL width remain independently enforced.
for key,v in [('max_grid',cert['N']),('max_points',cert['work']['scalar_points']),('max_precision',cert['precision_bits']),('max_operations',cert['work']['fixed_operations']),('max_integer_bits',cert['work']['largest_guarded_product_bits'])]:
 out=c.certify(raw,**task,**{key:v});ok(out['mean_hitting_time']==cert['mean_hitting_time'],'exact numerical budget boundary pass')
 unknown(lambda key=key,v=v:c.certify(raw,**task,**{key:v-1}),'one-below numerical resource boundary')
ratio=F(cert['total_ratio_exact']);t=dict(task,full_ratio=ratio)
ok(c.certify(raw,**t)['total_ratio_exact']==str(ratio),'exact total-ratio boundary passes')
unknown(lambda:c.certify(raw,**dict(task,full_ratio=(ratio+1)/2)),'numeric tolerance does not override full mean width')
# Scalar utility errors and finite fixed precision refusal domains.
for key,value in [('max_grid',True),('max_points',1.0),('max_cutoff',None),('quad_relative',F(1)),('full_ratio',F(1))]:
 tt=dict(task);tt[key]=value;unknown(lambda tt=tt:c.certify(raw,**tt),'malformed or unsupported external limits')
# A witness perturbation that changes only angular coefficient is still full-raw-bound.
r=deepcopy(raw);r['energy_terms'][-1]['coefficient']='21';unknown(lambda:c.verify(r,cert,**task),'changed angular raw input bound despite same scalar theorem')
# All saved cases repeated against LITERAL original external tasks and work recaptured.
saved=[]
for row in json.loads((H/'autonomous_radial_mfpt_20261031/results.json').read_text()):
 f=row['fixture'];rr=c.fixture(f['m'],F(f['coupling']),F(f['tangent']),F(f['radial_gain']));old=row['certificate'];target=F(11,10)if f['m']==64 else F(101,100)
 original={'beta':F(1),'kappa':F(1),'quad_relative':F(1,1000),'full_ratio':target};cc=c.certify(rr,**original)
 # Receiving is already replayed by full author suite; direct equality captures all proof and work fields.
 for key in ['task','acquisition','basin_mass','slab_resistance','mean_hitting_time','upper_components','constants','work']:
  ok(cc[key]==old[key],'saved original-task exact fields and actual work recaptured')
 check_formula(cc,F(1),F(1),F(f['radial_gain']),f['m']//4)
 exact=polynomial_resistance(f['m']//4,F(1));ok(F(cc['slab_resistance']['lower'])<=exact<=F(cc['slab_resistance']['upper']),'all saved resistance exact polynomial independent')
 lo,hi=F(cc['mean_hitting_time']['lower']),F(cc['mean_hitting_time']['upper']);ok(hi/lo<=target,'all saved requested mean ratios exact')
 # Derived exact ledger, including tails and separately powered constants.
 N=cc['N'];T=F(cc['T']);J=T.numerator.bit_length()-1;aa=f['m']//4
 expected_points=(J+2)*N+2;ok(expected_points==cc['work']['scalar_points'],'exact all-cached scalar-point ledger')
 def cost(n):return 1+2*(n.bit_count()+n.bit_length()-1) if n else 1
 expected_powers=expected_points+J+4
 expected_ops=(expected_points+J+3)*cost(aa)+cost(aa-3)
 ok(expected_powers==cc['work']['integer_power_calls'] and expected_ops==cc['work']['fixed_operations'],'exact power and guarded-product ledger')
 saved.append({'m':f['m'],'gamma':f['radial_gain'],'ratio_display':float(hi/lo),'mean_display':[float(lo),float(hi)],'work':cc['work'],'raw_entries':cc['acquisition']['exponent_entries_read']})
rr=json.loads((H/'autonomous_radial_mfpt_20261031/small_raw_fixture.json').read_text());cc=json.loads((H/'autonomous_radial_mfpt_20261031/small_certificate.json').read_text())
ok(c.verify(rr,cc,**c.external_from_record(cc))['status']=='PASS','saved standalone raw certificate actually replayed')
# The two huge angular/tangent inputs have same interval but separately hashed models.
rows=json.loads((H/'autonomous_radial_mfpt_20261031/results.json').read_text());x,y=rows[-2]['certificate'],rows[-1]['certificate']
ok(x['mean_hitting_time']==y['mean_hitting_time'] and x['acquisition']['raw_sha256']!=y['acquisition']['raw_sha256'],'paired 513D law independence with distinct raw hashes')
# Strong ordinary Gaussian comparator, matched alpha and actual projected gain.
ga=c.certify(c.fixture(8,p=2),**task);ok(ga['mean_hitting_time']==cert['mean_hitting_time'],'Gaussian comparator identical scalar method')
report={'status':'PASS','checks':sum(counts.values()),'categories':counts,'refusals':refusals,'saved_recaptured':saved,'seconds_diagnostic':time.perf_counter()-start,'scope':'Actual autonomous engineered radial-gain mean from exact Gibbs|A observable pushforward, not original constant-SPD model or arbitrary initialization.'}
(H/'independent_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['refusals','saved_recaptured']},indent=2))
