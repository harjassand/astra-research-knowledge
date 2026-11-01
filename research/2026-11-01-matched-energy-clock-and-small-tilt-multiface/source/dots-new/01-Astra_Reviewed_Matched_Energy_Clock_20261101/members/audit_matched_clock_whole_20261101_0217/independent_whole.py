from pathlib import Path
from fractions import Fraction as F
from math import isqrt,comb
from copy import deepcopy
import sys,json,hashlib,random,time
A=Path(__file__).resolve().parent;S=A/'replay/matched_energy_clock_constructor_20261101';sys.path.insert(0,str(S));import receive_matched_clock as r
checks=0;cats={};refusals=[];start=time.perf_counter();rng=random.Random(11010217)
def ok(v,k):
 global checks
 assert v,k
 checks+=1;cats[k]=cats.get(k,0)+1

def no(fn,k):
 try:fn()
 except r.Unknown as e:refusals.append({'test':k,'reason':str(e)});ok(True,k)
 else:raise AssertionError('false admission '+k)

def root(q,P):
 n=isqrt(q.numerator);d=isqrt(q.denominator)
 if n*n==q.numerator and d*d==q.denominator:return F(n,d)
 return F(isqrt((q.numerator<<(2*P))//q.denominator)+1,1<<P)

def ex(x):
 P=1536;S=1<<P;s=0
 while x>F(1,2):x/=2;s+=1
 tl=th=lo=hi=S
 for j in range(1,257):
  den=x.denominator*j;tl=tl*x.numerator//den;th=(th*x.numerator+den-1)//den
  if j%2:lo-=th;hi-=tl
  else:lo+=tl;hi+=th
  if j==255:lower=max(0,lo)
 upper=hi
 for _ in range(s):lower=lower*lower//S;upper=(upper*upper+S-1)//S
 return F(lower,S),F(upper,S)

full=json.loads((A/'actual_full_recapture.json').read_text());saved=json.loads((S/'matched_certificate.json').read_text());old=json.loads((S.parent/'retained_state_renewal_clock_20261101/results.json').read_text())[0]['certificate'];literal=json.loads((S/'original_physical_task.json').read_text());raw=r.p.old.fixture()
ok(r.base.same(r.p.old.proof_record(full),r.p.old.proof_record(saved)),'actual once-replayed full certificate every proof endpoint equals frozen')
ok(r.base.canonical_hash(raw)==literal['raw_sha256']==full['raw_derivative_acquisition']['actual_raw_sha256']=='e693d5c1ccf5fe43336f3e845d78fdad3a308d0fe88094cc8c4688a5caca76ff','identical original actual raw SHA not favorable replacement')
ok(hashlib.sha256((S.parent/'retained_state_renewal_clock_20261101/results.json').read_bytes()).hexdigest()==literal['source_file_sha256'],'literal physical query original source file hash')
for k in ['actual_full_generator','initialization']:ok(full[k]==old[k],'same generator and exact FULL GibbsA initial law '+k)
ok(full['actual_physical_spacing']==literal['physical_spacing']==old['physical_grid_spacing'],'literal EXACT old physical spacing no retiming')
ok(full['actual_physical_horizon']==old['physical_horizon'] and full['task']['n']==old['task']['n']==10,'same exact physical horizon and observation count')
ok(full['event']['lower_count']==old['event']['lower_count']==4 and full['event']['upper_count']==old['event']['upper_count']==6,'same actual finite record count event')
# Exact independent full normalization/current/energy join.
T=r.external_from_record(full);P=T['precision_bits'];a=full['raw_derivative_acquisition']['alpha'];beta=T['beta'];kap=T['kappa'];V=(1+kap)**a;vs=1+kap;vb=1+9*kap/16;abar=vs*(1-F(1,2*a));mean=full['inherited_source_certificate'];ml,mh=(F(mean['basin_mass'][k])for k in ['lower','upper']);rl,rh=(F(mean['slab_resistance'][k])for k in ['lower','upper']);pp=full['primal_scalar_price'];Pu=F(pp['P_total_upper']);d=F(1,a);const=mean['constants']
ok(vb<=abar<=vs and 2*abar-vs>=1+kap/8 and F(full['shifted_current_parameter'])==abar,'shifted current full matching admission not denominator only')
E=mh**2*(F(1,2)+d)*F(const['G_b_power_upper'])+(vs**2/(128*kap**2*(a-1)**2*d**2)+F(const['K_upper'])*kap**2)*F(const['G_1_power_upper'])+(1+F(const['global_transport_correction_upper']))/(16*kap**2*(a-1)**2)
ok(E==F(full['well_remainder_upper_without_beta']),'all four well regions including newly conditional band retained')
bf=(mh/ml)**2*F(full['scaled_shifted_resistance']['upper'])+2*E/(ml**2*V);br=1/(4*ml**2*(vs*(1+kap/8))**a)
ok(bf==F(full['normalized_odd_basin_source_inverse_upper']) and br==F(full['normalized_odd_slab_residual_inverse_upper']),'one slab twice wells and NEW odd residual complete beta normalization')
Cu=Pu/(beta*V);eps=Cu*beta*V*(root(bf,P)+root(br,P))**2-1;rate=Cu/ml
ok(Cu==F(full['full_trial_energy_upper']) and eps==F(full['global_moment_error_upper']) and eps>0,'full energy-inverse-energy product not old MFPT error')
ok(rate==F(full['reference_flip_rate']) and 2*rate==F(full['reference_correlation_decay_rate']) and 1/rate==F(full['reference_mean_time']),'Cu over Ml same spectral/count flip rate with factor2 only for correlation')
x=rate*T['physical_spacing'];eta=F(mean['slab_to_basin_mass_ratio_upper']);C=2+eta;s=eta/C;G=root(eps*(1+eps),P)/2+3*eps/8;delta=G+2*root(s,P)
ok(x==F(full['reference_dimensionless_step']) and x!=1,'new reference chain allowed but literal time unchanged')
ok(G==F(full['sharp_trial_vector_error_upper']) and delta==F(full['sign_vector_error_upper']),'whole vector and actual initialization/slab errors joined')
lo4,hi4=ex(4*x);tv=F(full['record_TV_error_upper']);ok((tv-T['n']*eta)**2>=C*T['n']*delta**2/(2*(1-hi4)),'independent rational exponential whole-record denominator bound')
jitter=tv+(C+1)*T['n']*x*x/2+C*T['n']*eps/4+F(3,2)*T['n']*eta
ok(F(full['continuous_jitter_failure_unclipped_upper'])==jitter and F(full['continuous_jitter_failure_upper'])==min(F(1),jitter),'full new-rate count/cluster/slab formula no borrowed midpoint term')
lo2,hi2=ex(2*x);ql,qh=(1-hi2)/2,(1-lo2)/2;cp=full['comparison_flip_probability'];ok(F(cp['lower'])<=ql<=qh<=F(cp['upper']),'reference kernel independent alternating exponential enclosure')
L,U=4,6;n=10;pl=sum((comb(n,j)*ql**j*(1-qh)**(n-j)for j in range(L,U+1)),F(0));ph=sum((comb(n,j)*qh**j*(1-ql)**(n-j)for j in range(L,U+1)),F(0));ev=full['event'];ok(F(ev['comparison_probability']['lower'])<=pl<=ph<=F(ev['comparison_probability']['upper']),'original count event independently integrated binomial enclosure')
ok(F(ev['actual_probability']['lower'])==max(F(0),F(ev['comparison_probability']['lower'])-tv) and F(ev['actual_probability']['upper'])==min(F(1),F(ev['comparison_probability']['upper'])+tv),'actual event endpoints include whole path uncertainty')
ok(tv<=F(1,10) and F(ev['actual_probability']['upper'])-F(ev['actual_probability']['lower'])<=F(1,5),'literal original ten-percent and total width gates both met')
# Cheap full query recomputation only: never a second full model production.
fx=r.base.Fixed(P,T['max_operations'],T['max_integer_bits'],T['max_exp_terms'],1);r4=fx.expminus(4*x);den=1-F(r4[1],fx.S);tv2=root(C*n*delta*delta/(2*den),P)+n*eta;r2=fx.expminus(2*x);qi=((fx.S-r2[1])//2,(fx.S-r2[0]+1)//2);(cl,ch),updates=r.p.old.count_event(fx,qi,n,L,U)
ok(tv2==tv and F(cl,fx.S)==F(ev['comparison_probability']['lower']) and F(ch,fx.S)==F(ev['comparison_probability']['upper']),'exact query recapture from already earned primitive and current record')
ok(fx.operations==full['work']['query_fixed_operations']==804 and updates==52,'query complete actual work counter independent recapture')
ok(sum(full['work'][k]for k in ['inherited_fixed_operations','shifted_fixed_operations','new_primal_fixed_operations','query_fixed_operations'])==full['work']['total_fixed_operations']==20131904,'single shared inherited shifted primal query product ledger')
(A/'independent_query_ledger.json').write_text(json.dumps({'fixed_operations':fx.operations,'exponential_calls':fx.exp_calls,'exponential_Taylor_terms':fx.exp_terms,'largest_guarded_product_bits':fx.max_guarded_bits,'dp_updates':updates,'proof_nodes':r.p.old.guard_certificate_tree(full)},indent=2)+'\n')
# Actual small scientific receiver mutations: no producer stubbing here.
small=json.loads((S/'small_certificate.json').read_text());sr=r.p.old.fixture(64,F(1));st=r.external_from_record(small);ok(r.verify(sr,small,**st)['status']=='PASS','independent small literal whole scientific receiving')
def leaves(o,path=()):
 if type(o)is dict:
  for k,v in o.items():
   if k not in ['work','seconds','display']:yield from leaves(v,path+(k,))
 elif type(o)is list:
  for k,v in enumerate(o):yield from leaves(v,path+(k,))
 else:yield path,o
for path,value in list(leaves(small)):
 b=deepcopy(small);obj=b
 for k in path[:-1]:obj=obj[k]
 obj[path[-1]]=value+'__forged' if type(value)is str else int(value) if type(value)is bool else bool(value) if type(value)is int else 'forged_null'
 no(lambda b=b:r.verify(sr,b,**st),'every typed whole proof leaf actual recomputation rejects mutation')
for k,v in st.items():
 t=st.copy();t[k]=F(99,100) if v is None else v+1 if type(v)is int else v+F(1,100000)
 no(lambda t=t:r.verify(sr,small,**t),'every literal external task value actually bound')
for k,v in st.items():
 if type(v)is int:
  for alias in [True,1.0,None,-1]:
   t=st.copy();t[k]=alias;no(lambda t=t:r.certify(sr,**t),'whole integer preflight refuses aliases')
for k in r.RATKEYS+['jitter_error']:
 for alias in [True,1,1.0,'1/2',F(-1),F(1,1<<5000)]:
  t=st.copy();t[k]=alias;no(lambda t=t:r.certify(sr,**t),'whole exact fraction preflight malformed or oversized')
# L=0 is valid only on its specific lower-window interface, not any positive field.
for k in [z for z in r.RATKEYS if z!='L']:
 t=st.copy();t[k]=F(0);no(lambda t=t:r.certify(sr,**t),'positive external task zero refused')
for k,v in [('max_operations',small['work']['total_fixed_operations']),('max_points',small['work']['inherited_and_shifted_points']),('max_integral_nodes',small['work']['new_tensor_nodes']),('max_dp_updates',st['n']*(st['event_upper']+2)),('max_energy_bins',st['Nt']),('max_y_cells',st['Ny'])]:
 t=st.copy();t[k]=v;z=r.certify(sr,**t);ok(z['record_TV_error_upper']==small['record_TV_error_upper'],'exact complete pipeline budget admits')
 t[k]=v-1;no(lambda t=t:r.certify(sr,**t),'one below full shared or allocation budget refuses')
for t0 in [dict(kappa=F(1,100000)),dict(path_error=F(1,1000)),dict(jitter_error=F(1,1000)),dict(query_absolute_width=F(1,1000)),dict(full_ratio=F(101,100)),dict(max_integer_bits=st['precision_bits']*2-1),dict(max_precision=st['precision_bits']-1),dict(max_exp_terms=1)]:
 t=st.copy();t.update(t0);no(lambda t=t:r.certify(sr,**t),'actual failed current range full error or work conjunction')
# Full binding rejects semantically equal but different literal input without
# falsely treating normalization as identical raw bytes.
b=deepcopy(sr);q=deepcopy(b['energy_terms'][0]);b['energy_terms'][0]['coefficient']='1/2';q['coefficient']='1/2';b['energy_terms'].append(q)
no(lambda:r.verify(b,small,**st),'equal normalized model still binds all actual literal input bytes')
z=r.certify(b,**st);ok(z['record_TV_error_upper']==small['record_TV_error_upper'] and z['raw_derivative_acquisition']['actual_raw_sha256']!=small['raw_derivative_acquisition']['actual_raw_sha256'],'literal duplicate sum independently earns same model with paid different read')
# Guard must reject malformed inputs before all expensive source work.
real=r.certify;called=[]
def forbidden(*a,**kw):called.append(1);raise AssertionError('guard reached expensive source')
r.certify=forbidden
bad={};q=bad
for _ in range(1100):q['deep']={};q=q['deep']
cyc={};cyc['cycle']=cyc;shared=[]
for z in [bad,cyc,{'a':shared,'b':shared},{'big':[0]*100001},{1:0},None,[]]:no(lambda z=z:r.verify({},z),'inherited repaired tree preflight remains active')
ok(not called,'no malformed tree reran scientific computation');r.certify=real
# Non-unit and odd-alpha root branches, actual last-axis mobility/coercivity.
nr=r.p.old.fixture(68,F(1),F(2,3),diagonal=False);nr['mobility_program']={'kind':'constant_diagonal','entries':['2/3']*67+['1/3']};nr['energy_terms'][67]['coefficient']='1/7';nt=st.copy();nt.update(beta=F(2,3),kappa=F(7,3),physical_spacing=F(10**12),path_error=F(99,100),full_ratio=F(10),Nt=128,Ny=64,T=F(150),quad_relative=F(1,100),max_grid=16384)
try:
 nz=r.certify(nr,**nt);ok(r.verify(nr,nz,**nt)['status']=='PASS','nonunit odd-alpha last-axis model actually received');ok(nz['raw_derivative_acquisition']['alpha']==17 and nz['raw_derivative_acquisition']['pure_coefficient_min']=='1/7' and nz['raw_derivative_acquisition']['actual_mobility_floor']=='1/3','actual odd shape and minima completely acquired');extra={'status':'PASS','raw':nr,'certificate':nz}
except r.Unknown as e:extra={'status':'UNKNOWN','reason':str(e),'task':{k:r.fs(v)if type(v)is F else v for k,v in nt.items()}};ok(True,'nonunit exploratory original request honestly refused and retained')
(A/'nonunit_odd_alpha_case.json').write_text(json.dumps(extra,indent=2)+'\n')
report={'status':'PASS','checks':checks,'categories':cats,'UNKNOWN_refusals':len(refusals),'refusals':refusals,'seconds':time.perf_counter()-start,'scope':'whole source/task/current/path/budget checks; actual full producer recapture reused transparently, small mutation receiving is NOT stubbed'};(A/'independent_whole_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='refusals'},indent=2))
