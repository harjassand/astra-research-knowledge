"""Independent whole constant-SPD MFPT arithmetic/model/receiving audit."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
from math import isqrt
import json,sys,random,time,hashlib,importlib.util,shutil
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'constant_spd_mfpt_20261031'))
import receive_mfpt as c
counts={};refusals=[];start=time.perf_counter()
def ok(b,k):
 if not b:raise AssertionError(k)
 counts[k]=counts.get(k,0)+1

def unknown(fn,k):
 try:fn()
 except c.Unknown as e:ok(True,k);refusals.append({'case':k,'reason':str(e)})
 else:raise AssertionError('false admission '+k)

# Root obligations can be checked exactly by squaring, without a float oracle.
rng=random.Random(202610312250)
for _ in range(700):
 q=F(rng.randrange(1,2**180),rng.randrange(1,2**180));P=rng.randrange(1,257);rt=c.Roots(P,100000);h=rt.upper(q);ulp=F(1,1<<P)
 ok(h*h>=q,'independent exact upper-root square inequality')
 ok(h<ulp or (h-ulp)**2<=q,'independent root one-ulp or exact enclosure')
for root in [F(1,2**500),F(1,3),F(7,11),F(1),F(10**100),F(2**400,3)]:
 for P in [1,16,192]:
  rt=c.Roots(P,10000);ok(rt.upper(root*root)==root,'exact rational root bypass without rounding')
for P in [1,8,32,192]:
 for j in [1,2,7,100]:
  # Strictly below/above a dyadic square; no lost denominator remainder.
  a=F(j,1<<P);eps=F(1,1<<(4*P+20))
  for q in [a*a-eps,a*a+eps]:
   h=c.Roots(P,100000).upper(q);ok(h*h>=q and (h<F(1,1<<P)or(h-F(1,1<<P))**2<=q),'root neighbors of dyadic square')
q=F(2,3);P=192;limit=q.numerator.bit_length()+2*P
ok(c.Roots(P,limit).upper(q)**2>=q,'exact scaled-root operand boundary pass')
unknown(lambda:c.Roots(P,limit-1).upper(q),'one-below scaled-root operand budget')
for q in [F(0),F(-1)]:unknown(lambda q=q:c.Roots(192,10000).upper(q),'nonpositive internal root refusal')
# Check inherited powers/monotone quadrature against direct rational endpoint sums.
for _ in range(150):
 aa=rng.randrange(4,129);ii=c.Scalar(aa,F(1),192,10000,100000,1000000);q=F(rng.randrange(1,100),rng.randrange(1,100));n=rng.randrange(0,130)
 l,u=ii.power(q,n);ok(F(l,ii.S)<=q**n<=F(u,ii.S),'source-pinned powers independent rational reference')
for aa in [4,7,16]:
 for k in [F(1,7),F(1),F(11,3)]:
  ii=c.Scalar(aa,k,256,10000,1000000,1000000)
  for a,b,kind in [(F(1,2),F(1),'q'),(F(1),F(2),'q'),(F(2),F(4),'q'),(F(0),F(1,2),'r')]:
   N=29;vs=[]
   for j in range(N+1):
    y=a+(b-a)*j/N;v=1+k*(1-y*y)**2;vs.append(v**(-aa if kind=='q'else aa))
   low=(b-a)/N*sum(min(x,y)for x,y in zip(vs,vs[1:]));high=(b-a)/N*sum(max(x,y)for x,y in zip(vs,vs[1:]));l,u=ii.integrate(a,b,N,kind)
   ok(l<=low<=high<=u,'independent exact all-region Darboux enclosure')
  for T in [F(3,2),F(2),F(4)]:ok(ii.tail(T)>=T/F(4*aa-1)/(k*(T*T-1)**2)**aa,'independent full tail formula')

budgets={'max_dimension':1024,'max_terms':100000,'max_coefficient_bits':4096,'max_exponent_entries':64000000,'max_total_coefficient_bits':32000000,'max_rational_bits':1000000}
raw=c.fixture(16,diagonal=True)
# The least diagonal and least pure coefficient are deliberately LAST, not probes/firsts.
raw['mobility_program']['entries']=['17']*15+['7/11']
for rec in raw['energy_terms']:
 if sum(n!=0 for n in rec['powers'])==1:rec['coefficient']='2' if rec['powers'][15]==0 else '1/7'
aq,alpha,mu,dmin=c.acquire(raw,**budgets)
ok(mu==F(7,11)and dmin==F(1,7)and F(aq['coercivity_lower'])==F(1,112),'actual last-axis minima acquired exactly')
ok(aq['energy_probe_at_e1']=='2'and'tangent_weight'not in aq and'transverse_SPD_away_origin'not in aq and'initial_energy'not in aq,'synthetic tangent and witness not physical claims')
ok(aq['transverse_SPD_everywhere'] is True and aq['mobility_entries_read']==16,'constant SPD everywhere and complete diagonal scan')
mobbits=sum(F(x).numerator.bit_length()+F(x).denominator.bit_length()for x in raw['mobility_program']['entries'])
energybits=sum(F(t['coefficient']).numerator.bit_length()+F(t['coefficient']).denominator.bit_length()for t in raw['energy_terms'])
ok(aq['mobility_coefficient_bits_read']==mobbits and aq['coefficient_bits_read']==energybits,'independent full energy and mobility bit ledger')
for key,value in [('max_dimension',16),('max_terms',aq['raw_terms']),('max_exponent_entries',aq['exponent_entries_read']),('max_total_coefficient_bits',energybits+mobbits)]:
 b=dict(budgets);b[key]=value;ok(c.acquire(raw,**b)[0]['raw_sha256']==aq['raw_sha256'],'exact complete input budget boundary')
 b[key]=value-1;unknown(lambda b=b:c.acquire(raw,**b),'one-below full energy mobility resource budget')
# Reject late invalid entries, absent/rotated/dense/gain programs, and pathological types.
for value in [None,True,1,1.0,'0','-1','1/1','01','1/0','9'*9000]:
 r=deepcopy(raw);r['mobility_program']['entries'][-1]=value;unknown(lambda r=r:c.certify(r),'last mobility entry fully parsed')
for program in [None,{}, {'kind':'constant_isotropic','value':'1','floor':'64'}, {'kind':'constant_diagonal','entries':['1']*15}, {'kind':'dense_spd','matrix':[[1]]}, {'kind':'radial_gain','value':'512'}, {'kind':'constant_isotropic','value':'64','entries':['64']*16}]:
 r=deepcopy(raw);r['mobility_program']=program;unknown(lambda r=r:c.certify(r),'unsupported or ambiguous actual mobility program')
for mode in ['negative','zero','odd','mixeddegree','missingpure','duplicate','extra','bool','huge']:
 r=deepcopy(raw)
 if mode=='negative':r['energy_terms'][-1]['coefficient']='-1'
 elif mode=='zero':r['energy_terms'][-1]['coefficient']='0'
 elif mode=='odd':r['energy_terms'][-1]['powers'][-1]=1
 elif mode=='mixeddegree':r['energy_terms'][0]['powers'][0]=2
 elif mode=='missingpure':r['energy_terms'].pop(0)
 elif mode=='duplicate':r['energy_terms'].append(deepcopy(r['energy_terms'][0]))
 elif mode=='extra':r['radial_gain']='512'
 elif mode=='bool':r['dimension']=True
 else:r['dimension']=10**50
 unknown(lambda r=r:c.certify(r),'complete energy and no radial-model conflation')
# Independent formula12 root inequalities and exact outward corner assembly.
task={'beta':F(2,3),'kappa':F(3,7),'quad_relative':F(1,50),'full_ratio':F(10**9)}
cert=c.certify(raw,**task)
def formula_check(cc,beta,kappa,mu,dmin,alpha):
 ml,mh=F(cc['basin_mass']['lower']),F(cc['basin_mass']['upper']);rl,rh=F(cc['slab_resistance']['lower']),F(cc['slab_resistance']['upper']);a=1+F(9,16)*kappa;d=F(1,alpha);c1=1+kappa*(1-(1+d)**2)**2
 cs=F(cc['transport_factor_upper'])-1;D=F(cc['constants']['global_transport_correction_upper']);S0=F(1,2)*a**alpha+d*c1**alpha;W=1/(64*kappa*kappa*(alpha-1)**2*d)
 ok(cs>0 and cs*cs>=kappa*kappa/(4*mu*mu*beta*dmin*a**3),'slab root factor exact squared proof')
 ok(D>0 and D*D>=16*alpha*alpha*max(kappa,F(1))**2/(mu*mu*beta*dmin),'global basin root factor exact squared proof')
 vals={'slab_with_transport':beta*mh*rh*(1+cs),'basin_near_with_global_transport':beta*(1+D)*mh*S0,'basin_far_with_global_transport':beta*(1+D)*W/ml}
 for k,x in vals.items():ok(F(cc['upper_components'][k])>=x,'all formula12 components outward propagated')
 low=beta*ml*rl;high=(1+a**(-alpha)/ml)*sum(vals.values(),F(0));got=F(cc['mean_hitting_time']['upper'])
 ok(F(cc['mean_hitting_time']['lower'])==low and got>=high,'absolute-time endpoints independently reconstructed')
 ok(got==(1+F(cc['slab_to_basin_mass_ratio_upper']))*sum(map(F,cc['upper_components'].values()),F(0)),'source cross factor retained exactly')
 ok(F(cc['total_ratio_exact'])==got/low and mh*rh<=(1+F(cc['task']['quad_relative']))*ml*rl,'numeric integral width separate from total mean ratio')
formula_check(cert,task['beta'],task['kappa'],mu,dmin,alpha)
ok(c.verify(raw,cert,**task)['status']=='PASS','nonunit beta dmin kappa diagonal original-task replay')
# Same outer bound is not equality of actual means; raw program remains bound.
riso=c.fixture(16);base_task={'quad_relative':F(1,50),'full_ratio':F(10**6)};basecert=c.certify(riso,**base_task)
rdiag=c.fixture(16,diagonal=True);diagcert=c.certify(rdiag,**base_task)
ok(basecert['mean_hitting_time']==diagcert['mean_hitting_time']and basecert['acquisition']['raw_sha256']!=diagcert['acquisition']['raw_sha256'],'common-floor outer interval with distinct actual models')
# Exact coordinate/time scaling checks expose wrong mu,beta,dmin factors.
scaled=deepcopy(riso)
for rec in scaled['energy_terms']:rec['coefficient']=str(9*F(rec['coefficient']))
scaled['mobility_program']['value']='64/3';sc=c.certify(scaled,**base_task)
ok(sc['mean_hitting_time']==basecert['mean_hitting_time'],'quartic energy nine mobility one-third compensating scaling')
time_scaled=deepcopy(riso);time_scaled['mobility_program']['value']='64/3';tc=c.certify(time_scaled,beta=F(9),**base_task)
for side in ['lower','upper']:ok(F(tc['mean_hitting_time'][side])==9*F(basecert['mean_hitting_time'][side]),'absolute time beta mobility scaling')
# Every proof-bearing top/nested field and output endpoint is authenticated.
keys=['schema','dependency_sha256','task','acquisition','observable','actual_full_generator','initialization','proof_method','not_claimed','total_ratio_exact','transport_factor_upper','slab_to_basin_mass_ratio_upper','upper_components','source_cross_multiplier_upper','constants','N','T','tail_upper','precision_bits']
for key in keys:
 for val in [None,True]:
  cc=deepcopy(basecert);cc[key]=val;unknown(lambda cc=cc:c.verify(riso,cc,**base_task),'all top proof fields type bound')
for field in ['acquisition','task','upper_components','constants']:
 for key in basecert[field]:
  cc=deepcopy(basecert);cc[field][key]=None;unknown(lambda cc=cc:c.verify(riso,cc,**base_task),'every nested model task correction bound')
for field in ['basin_mass','slab_resistance','mean_hitting_time']:
 for side in ['lower','upper']:
  for val in [None,True,1.0,'0']:
   cc=deepcopy(basecert);cc[field][side]=val;unknown(lambda cc=cc:c.verify(riso,cc,**base_task),'all exact numerical endpoints typed bound')
for text in ['fixed-ray same energy law','Gibbs energy marginal only','small total variation approximation','arbitrary point initialization']:
 cc=deepcopy(basecert);cc['initialization']=text;unknown(lambda cc=cc:c.verify(riso,cc,**base_task),'full Gibbs initialization cannot be weakened')
rr=deepcopy(riso);rr['mobility_program']['value']='65';unknown(lambda:c.verify(rr,basecert,**base_task),'actual mobility cannot be changed under certificate')
cc=deepcopy(basecert);cc['work']=None;cc['seconds']='ignored';cc['mean_hitting_time']['display']=-1;cc['extra_field']=True
ok(c.verify(riso,cc,**base_task)['status']=='PASS','diagnostics and extra fields not authenticated')
for key,v in [('max_grid',basecert['N']),('max_points',basecert['work']['scalar_points']),('max_precision',basecert['precision_bits']),('max_operations',basecert['work']['fixed_operations']),('max_integer_bits',basecert['work']['largest_guarded_product_bits'])]:
 out=c.certify(riso,**base_task,**{key:v});ok(out['mean_hitting_time']==basecert['mean_hitting_time'],'exact finite numerical budget pass')
 unknown(lambda key=key,v=v:c.certify(riso,**base_task,**{key:v-1}),'one-below finite numerical budget refusal')
ratio=F(basecert['total_ratio_exact']);ok(c.certify(riso,**dict(base_task,full_ratio=ratio))['total_ratio_exact']==str(ratio),'exact total mean ratio boundary passes')
unknown(lambda:c.certify(riso,**dict(base_task,full_ratio=(1+ratio)/2)),'numerical tolerance not total physical mean ratio')
unknown(lambda:c.certify(c.fixture(512,mobility=F(1)),full_ratio=F(101,100)),'ordinary unit mobility honestly refuses one percent')
# Six literal-original-task replays, actual work recapture, exact finite resistance.
def convolution(a,b):
 z=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):z[i+j]+=x*y
 return z

def R_exact(alpha):
 p=[F(1)]
 for _ in range(alpha):p=convolution(p,[F(2),F(-2),F(1)])
 return sum((2*x*F(1,2)**(2*j+1)/(2*j+1)for j,x in enumerate(p)),F(0))
saved=[]
for row in json.loads((H/'constant_spd_mfpt_20261031/results.json').read_text()):
 f=row['fixture'];rr=c.fixture(f['m'],F(f['coupling']),F(f['mobility']),f['diagonal']);old=row['certificate'];target=F(13,10)if F(f['mobility'])==1 else F(11,10)if f['m']==64 else F(101,100)
 original={'beta':F(1),'kappa':F(1),'quad_relative':F(1,1000),'full_ratio':target};new=c.certify(rr,**original)
 for key in ['task','acquisition','basin_mass','slab_resistance','mean_hitting_time','upper_components','constants','work']:ok(new[key]==old[key],'saved original-task exact fields and work recapture')
 formula_check(new,F(1),F(1),F(f['mobility']),F(1),f['m']//4)
 rex=R_exact(f['m']//4);ok(F(new['slab_resistance']['lower'])<=rex<=F(new['slab_resistance']['upper']),'saved resistance independently exactly integrated')
 low,high=F(new['mean_hitting_time']['lower']),F(new['mean_hitting_time']['upper']);ok(high/low<=target,'each original requested total ratio achieved')
 N=new['N'];J=F(new['T']).numerator.bit_length()-1;alpha=f['m']//4;points=(J+2)*N+2;calls=points+J+3;ops=calls*(1+2*(alpha.bit_count()+alpha.bit_length()-1))
 ok(new['work']['scalar_points']==points and new['work']['integer_power_calls']==calls and new['work']['fixed_operations']==ops and new['work']['root_calls']==2,'independent complete scalar power product root ledger')
 saved.append({'fixture':f,'mean_display':[float(low),float(high)],'ratio_display':float(high/low),'work':new['work'],'energy_entries':new['acquisition']['exponent_entries_read'],'mobility_entries':new['acquisition']['mobility_entries_read']})
rr=json.loads((H/'constant_spd_mfpt_20261031/small_raw_fixture.json').read_text());cc=json.loads((H/'constant_spd_mfpt_20261031/small_certificate.json').read_text())
ok(c.verify(rr,cc,beta=F(1),kappa=F(1),quad_relative=F(1,1000),full_ratio=F(11,10))['status']=='PASS','standalone small original-task replay')
# Isolated dependency tamper: no frozen or clean source modifications.
scratch=H/'dependency_tamper';(scratch/'constant_spd_mfpt_20261031').mkdir(parents=True,exist_ok=True);(scratch/'autonomous_radial_mfpt_20261031').mkdir(exist_ok=True)
shutil.copy2(H/'constant_spd_mfpt_20261031/receive_mfpt.py',scratch/'constant_spd_mfpt_20261031/receive_mfpt.py')
(scratch/'autonomous_radial_mfpt_20261031/receive_mfpt.py').write_bytes((H/'autonomous_radial_mfpt_20261031/receive_mfpt.py').read_bytes()+b'\n# deliberate isolated byte-tamper test\n')
spec=importlib.util.spec_from_file_location('tampered_mfpt_for_test',scratch/'constant_spd_mfpt_20261031/receive_mfpt.py');mod=importlib.util.module_from_spec(spec)
try:spec.loader.exec_module(mod)
except RuntimeError as e:ok(str(e)=='scalar acquisition dependency hash mismatch','dependency hash fails before import')
else:raise AssertionError('dependency modification admitted')
report={'status':'PASS','checks':sum(counts.values()),'categories':counts,'refusals':refusals,'saved_recaptured':saved,'seconds_diagnostic':time.perf_counter()-start,'scope':'Actual ordinary constant-SPD full Gibbs|A MFPT. No closure, fixed-ray, physical preparation or future survival-lemma claim.'}
(H/'independent_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['refusals','saved_recaptured']},indent=2))
