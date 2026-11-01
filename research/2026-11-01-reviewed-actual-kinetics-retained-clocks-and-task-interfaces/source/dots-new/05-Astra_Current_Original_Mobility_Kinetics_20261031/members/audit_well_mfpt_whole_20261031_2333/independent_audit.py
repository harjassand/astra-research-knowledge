from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
from math import comb
import importlib.util,json,random,time,shutil
H=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('well_audit',H/'well_redistribution_mfpt_20261031/receive_mfpt.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
counts={};refusals=[];start=time.perf_counter();rng=random.Random(2334)
def ok(x,k):
 assert x,k
 counts[k]=counts.get(k,0)+1
def unknown(fn,k):
 try:fn()
 except c.Unknown as e:ok(True,k);refusals.append({'test':k,'reason':str(e)})
 else:raise AssertionError('admitted '+k)
# New scalar profile tested against exact rational values, not its own primitives.
for _ in range(400):
 alpha=rng.randrange(4,80);kap=F(rng.randrange(1,100),rng.randrange(1,100));y=F(rng.randrange(0,1001),2000);ii=c.Scalar(alpha,kap,512,1000,100000,100000)
 v=1+kap*(1-y*y)**2;vs=1+kap;q=(vs*vs/(2*vs-v))**alpha;lo,hi=ii.point(y,'rplus')
 ok(F(lo,ii.S)<=q<=F(hi,ii.S),'Rplus points contain independent exact rational powers')
 ok(vs*vs/(2*vs-v)>=v and 2*vs-v>=vs,'parallel profile positivity and Rplus dominates R')
for alpha in [4,11,32,128]:
 for kap in [F(1,7),F(1),F(19,3)]:
  ii=c.Scalar(alpha,kap,1024,10000,1000000,100000);lo,hi=ii.integrate(F(0),F(1,2),32,'rplus');vals=[]
  for j in range(65):
   y=F(j,128);v=1+kap*(1-y*y)**2;vs=1+kap;vals.append((vs*vs/(2*vs-v))**alpha)
  rlo=sum(vals[1:],F(0))/128;rhi=sum(vals[:-1],F(0))/128
  ok(lo<=rlo<=rhi<=hi,'Rplus exact finer Darboux contained in coarse outward enclosure');ok(all(x>=y for x,y in zip(vals,vals[1:])),'full slab profile monotonicity on rational fixtures')
ii=c.Scalar(4,F(1),192,2,10000,10000);ii.point(F(1),'q');ii.point(F(0),'r');unknown(lambda:ii.point(F(0),'rplus'),'Rplus shares previous cache point budget')
for y in [F(-1),F(1),F(1,2)+F(1,2**100)]:unknown(lambda y=y:c.Scalar(4,F(1),192,100,10000,10000).point(y,'rplus'),'outside-slab Rplus refused')
for n in [True,0,-1,1.0]:unknown(lambda n=n:c.Scalar(4,F(1),192,100,10000,10000).integrate(F(0),F(1,2),n,'rplus'),'strict Rplus integration count')
# Independent rigorous integrated Taylor enclosure for actual kappa=1 Rplus.
# (2/(1+x))^alpha, x=y²-y⁴/2 >=0. Derivatives alternate globally, so
# Taylor degree 160 is an upper bound and degree 161 a lower bound.
I=[]
for n in range(162):
 q=sum((F(comb(n,j)*(-1)**j,8**j*(2*n+2*j+1))for j in range(n+1)),F(0))/4**n
 ok(q>0,'exact integrated nonnegative parallel-profile power');I.append(q)
def exact_parallel(alpha):
 total=F(0);up=None
 for n,integral in enumerate(I):
  total+=(-1)**n*comb(alpha+n-1,n)*integral
  if n==160:up=total*2**alpha
 return total*2**alpha,up

def exact_R(alpha):
 coeff=[1]
 for _ in range(alpha):
  nxt=[0]*(len(coeff)+2)
  for j,a in enumerate(coeff):
   for k,b in enumerate([2,-2,1]):nxt[j+k]+=a*b
  coeff=nxt
 return sum((F(a,2**(2*j)*(2*j+1))for j,a in enumerate(coeff)),F(0))

def formula(cc,beta,kappa,mu,dmin,alpha):
 ml,mh=map(F,[cc['basin_mass']['lower'],cc['basin_mass']['upper']]);rl,rh=map(F,[cc['slab_resistance']['lower'],cc['slab_resistance']['upper']]);pl,ph=map(F,[cc['parallel_slab_resistance']['lower'],cc['parallel_slab_resistance']['upper']]);d=F(1,alpha);vs=1+kappa;ab=1+F(9,16)*kappa;gb=vs*vs/(2*vs-ab);g1=vs*vs/(2*vs-1);z=cc['constants'];K=F(z['K_upper']);D=F(z['global_transport_correction_upper']);gbp=F(z['G_b_power_upper']);g1p=F(z['G_1_power_upper']);cs=F(cc['source_S_slab_factor_upper'])-1;r=F(cc['slab_to_basin_mass_ratio_upper'])
 ok(F(z['a_b'])==ab and F(z['delta'])==d and F(z['vstar'])==vs and F(z['G_b'])==gb and F(z['G_1'])==g1,'all new exact well constants')
 ok(gbp>=gb**alpha and g1p>=g1**alpha and r*ml>=ab**(-alpha),'outward explicit powers and slab mass ratio')
 ok(K*K>=F(alpha*alpha,64)/(mu*mu*beta*dmin) and D*D>=16*alpha*alpha*max(kappa,F(1))**2/(mu*mu*beta*dmin) and cs*cs>=kappa*kappa/(4*mu*mu*beta*dmin*ab**3),'all three current-root factors have outward squared bounds')
 terms={'parallel_slab':beta*mh*ph,'near_well_longitudinal':beta*mh*(1+d-F(1,2))*gbp,'middle_well_longitudinal':beta*vs*vs*g1p/(128*kappa*kappa*(alpha-1)**2*d*d*ml),'well_vertical_redistribution':beta*K*kappa*kappa*g1p/ml,'far_conditional_tail':beta*(1+D)/(16*kappa*kappa*(alpha-1)**2*ml)}
 ok(all(F(cc['upper_source_A_components'][k])==v for k,v in terms.items()),'independent all five source-A corrections')
 UA=sum(terms.values(),F(0));US=r*r*beta*mh*rh*(1+cs);cross=r*(UA+beta*mh*rh*(1+cs))/2
 ok(F(cc['source_A_inverse_per_mass_upper'])==UA and F(cc['source_S_inverse_per_mass_upper'])==US,'independent separate source-A and source-S bounds')
 ok(F(cc['source_cross_AMGM_upper'])==cross and cross*cross>=UA*US,'exact cross-source AMGM dominates Cauchy')
 ok(F(cc['mean_hitting_time']['upper'])==UA+cross and F(cc['mean_hitting_time']['lower'])==beta*ml*rl,'complete actual MFPT lower and upper join')
 ok(F(cc['total_ratio_exact'])==(UA+cross)/(beta*ml*rl),'total ratio includes every structural term')
raw=c.fixture(16);task={'quad_relative':F(1,50),'full_ratio':F(1000000)};cert=c.certify(raw,**task);formula(cert,F(1),F(1),F(1),F(1),4)
ok(c.verify(raw,cert,**task)['status']=='PASS','small literal task actual receiver roundtrip')
# Last-axis minima and nonsquare physical parameter/root cases.
rr=c.fixture(16,diagonal=True);rr['energy_terms'][15]['coefficient']='1/7';rr['mobility_program']['entries'][-1]='2/11';cc=c.certify(rr,beta=F(2,3),kappa=F(3,7),**task)
ok(cc['acquisition']['pure_coefficient_min']=='1/7' and cc['acquisition']['mobility_floor']=='2/11','complete nonfirst-axis minima acquisition');formula(cc,F(2,3),F(3,7),F(2,11),F(1,7),4)
for key in ['beta','kappa','quad_relative','full_ratio']:
 for bad in [True,1,1.0,None,F(0),F(-1)]:unknown(lambda key=key,bad=bad:c.certify(raw,**dict(task,**{key:bad})),'strict exact task type refusal')
for key in ['max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_rational_bits','max_grid','max_points','max_cutoff','max_precision','max_operations','max_integer_bits']:
 for bad in [True,1.0,None,0,-1]:unknown(lambda key=key,bad=bad:c.certify(raw,**dict(task,**{key:bad})),'strict resource type refusal')
for mutation in ['last_coefficient','last_odd','missing_pure','duplicate','last_diagonal','oversized','unknown','booldim','dense','radial']:
 rr=deepcopy(raw)
 if mutation=='last_coefficient':rr['energy_terms'][-1]['coefficient']='0'
 elif mutation=='last_odd':rr['energy_terms'][-1]['powers'][-1]=1
 elif mutation=='missing_pure':rr['energy_terms'].pop(15)
 elif mutation=='duplicate':rr['energy_terms'].append(deepcopy(rr['energy_terms'][0]))
 elif mutation=='last_diagonal':rr['mobility_program']={'kind':'constant_diagonal','entries':['1']*15+['-1']}
 elif mutation=='oversized':rr['energy_terms'][-1]['coefficient']=str(1<<4097)
 elif mutation=='unknown':rr['claimed_full_gibbs']=True
 elif mutation=='booldim':rr['dimension']=True
 elif mutation=='dense':rr['mobility_program']={'kind':'constant_dense','entries':[]}
 else:rr['mobility_program']['kind']='radial_lift'
 unknown(lambda rr=rr:c.certify(rr,**task),'full raw refusal '+mutation)
for key,val in [('max_grid',cert['N']),('max_points',cert['work']['scalar_points']),('max_precision',cert['precision_bits']),('max_operations',cert['work']['fixed_operations']),('max_integer_bits',max(cert['work']['largest_guarded_product_bits'],cert['work']['largest_root_integer_bound_bits']))]:
 ok(c.certify(raw,**dict(task,**{key:val}))['mean_hitting_time']==cert['mean_hitting_time'],'exact paid numerical boundary passes')
 unknown(lambda key=key,val=val:c.certify(raw,**dict(task,**{key:val-1})),'one-below paid numerical boundary refuses')
ratio=F(cert['total_ratio_exact']);ok(c.certify(raw,**dict(task,full_ratio=ratio))['total_ratio_exact']==str(ratio),'exact total width threshold passes');unknown(lambda:c.certify(raw,**dict(task,full_ratio=ratio-F(1,1<<300))),'below exact total width threshold refuses')
fields=['schema','dependency_sha256','task','acquisition','observable','actual_full_generator','initialization','proof_method','not_claimed','total_ratio_exact','source_S_slab_factor_upper','slab_to_basin_mass_ratio_upper','source_A_inverse_per_mass_upper','source_S_inverse_per_mass_upper','upper_source_A_components','source_cross_AMGM_upper','constants','N','T','tail_upper','precision_bits']
for key in fields:
 cc=deepcopy(cert);cc[key]=None;unknown(lambda cc=cc:c.verify(raw,cc,**task),'all proof-bearing top fields bind')
for key in ['basin_mass','slab_resistance','parallel_slab_resistance','mean_hitting_time']:
 for side in ['lower','upper']:
  cc=deepcopy(cert);cc[key][side]='0';unknown(lambda cc=cc:c.verify(raw,cc,**task),'all exact new and inherited endpoints bind')
cc=deepcopy(cert);cc['work']=None;cc['seconds']=None;cc['mean_hitting_time']['display']=None;cc['unrecognized_annotation']='not authenticated';ok(c.verify(raw,cc,**task)['status']=='PASS','diagnostics and extra annotations excluded from core proof')
# Physical time scaling preserves correction factors but not the clock.
scaled=c.certify(c.fixture(16,mobility=F(1,3)),beta=F(9),**task)
ok(all(F(scaled['mean_hitting_time'][side])==9*F(cert['mean_hitting_time'][side])for side in ['lower','upper']),'beta and mobility scaling gives absolute mean time factor nine')
# Four actual saved raw programs under literal original requests.
saved=[]
for row in json.loads((H/'well_redistribution_mfpt_20261031/results.json').read_text()):
 f=row['fixture'];r=c.fixture(f['m'],F(f['coupling']),F(f['mobility']),f['diagonal']);target=F(11,10)if f['m']==128 else F(103,100)if f['m']==256 else F(101,100);cc=c.certify(r,beta=F(1),kappa=F(1),quad_relative=F(1,1000),full_ratio=target);old=row['certificate']
 for key in fields+['basin_mass','slab_resistance','parallel_slab_resistance','mean_hitting_time','work']:ok(c.base.same(cc[key],old[key]),'actual saved proof and work recapture')
 alpha=f['m']//4;formula(cc,F(1),F(1),F(1),F(1),alpha);rlo,rhi=exact_parallel(alpha);pl,ph=map(F,[cc['parallel_slab_resistance']['lower'],cc['parallel_slab_resistance']['upper']])
 ok(pl<=rlo<=rhi<=ph,'actual Rplus contains independent integrated Taylor proof interval');er=exact_R(alpha);ok(F(cc['slab_resistance']['lower'])<=er<=F(cc['slab_resistance']['upper']),'actual R independently exactly polynomial-integrated')
 N=cc['N'];J=F(cc['T']).numerator.bit_length()-1;points=(J+3)*N+3;powers=points+J+3;ops=powers*(1+2*(alpha.bit_count()+alpha.bit_length()-1))
 ok(cc['work']['scalar_points']==points and cc['work']['integer_power_calls']==powers and cc['work']['fixed_operations']==ops and cc['work']['root_calls']==3,'independent complete new scalar cache power product and root ledger')
 ok(F(cc['total_ratio_exact'])<=target,'actual external total MFPT ratio');saved.append({'fixture':f,'mean_display':cc['mean_hitting_time']['display'],'total_ratio_display':float(F(cc['total_ratio_exact'])),'parallel_reference_relative_width':float((rhi-rlo)/rlo),'work':cc['work']})
r=json.loads((H/'well_redistribution_mfpt_20261031/small_raw_fixture.json').read_text());cc=json.loads((H/'well_redistribution_mfpt_20261031/small_certificate.json').read_text());ok(c.verify(r,cc,full_ratio=F(11,10))['status']=='PASS','standalone literal original task replay')
unknown(lambda:c.certify(c.fixture(256),full_ratio=F(101,100)),'m256 honest one-percent sufficient-bound refusal')
unknown(lambda:c.certify(c.fixture(16,mobility=F(1,10**9)),**task),'tiny actual mobility retains paid current penalty')
d=H/'dependency_tamper';(d/'well_redistribution_mfpt_20261031').mkdir(parents=True);(d/'constant_spd_mfpt_20261031').mkdir();shutil.copyfile(H/'well_redistribution_mfpt_20261031/receive_mfpt.py',d/'well_redistribution_mfpt_20261031/receive_mfpt.py');(d/'constant_spd_mfpt_20261031/receive_mfpt.py').write_bytes((H/'constant_spd_mfpt_20261031/receive_mfpt.py').read_bytes()+b'\n# isolated tamper\n')
s=importlib.util.spec_from_file_location('bad_well',d/'well_redistribution_mfpt_20261031/receive_mfpt.py');m=importlib.util.module_from_spec(s)
try:s.loader.exec_module(m)
except RuntimeError as e:ok(str(e)=='accepted constant-SPD acquisition dependency hash mismatch','dependency tamper refused before import')
else:raise AssertionError('dependency admitted')
report={'status':'PASS','checks':sum(counts.values()),'categories':counts,'refusals':refusals,'actual_saved_recaptures':saved,'seconds_diagnostic':time.perf_counter()-start,'scope':'Exact full Gibbs|A actual ordinary unit-mobility-capable MFPT; new dual witness only.'};(H/'independent_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['refusals','actual_saved_recaptures']},indent=2))
