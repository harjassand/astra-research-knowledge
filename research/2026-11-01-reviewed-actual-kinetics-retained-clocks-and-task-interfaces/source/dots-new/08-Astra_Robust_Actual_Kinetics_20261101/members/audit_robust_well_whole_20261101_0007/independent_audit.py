from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import importlib.util,json,random,time,shutil
H=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('robust_audit',H/'robust_well_kinetics_20261031/receive_robust.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
counts={};refusals=[];start=time.perf_counter();rng=random.Random(611010010)
def ok(x,k):
 assert x,k
 counts[k]=counts.get(k,0)+1
def unknown(fn,k):
 try:fn()
 except c.Unknown as e:ok(True,k);refusals.append({'test':k,'reason':str(e)})
 else:raise AssertionError('unexpected admission '+k)
def reference_exp(x,P):
 # Independently directed alternating series: enclose each exact magnitude
 # dyadically; even partial sum bounds above and next odd partial below.
 if not x:return F(1),F(1)
 shift=0;r=x
 while r>F(1,2):r/=2;shift+=1
 Q=1<<(P+128);tl=th=Q;sl=sh=Q;up=None
 # Degree321 has remainder < 2^-2500 on r<=1/2, sufficient for P<=1792.
 assert P<=1792
 for n in range(1,322):
  den=r.denominator*n;nl=tl*r.numerator;nh=th*r.numerator;tl=nl//den;th=-(-nh//den)
  if n%2:sl-=th;sh-=tl
  else:sl+=tl;sh+=th
  if n==320:up=sh
 lo,hi=sl,up
 for _ in range(shift):lo=lo*lo//Q;hi=-(-hi*hi//Q)
 return F(max(0,lo),Q),F(min(Q,hi),Q)
# New profiles and full monotonicity segments against independent exact rationals.
for _ in range(320):
 a=rng.randrange(4,100);k=F(rng.randrange(1,50),rng.randrange(1,50));e=k*F(rng.randrange(0,100),100);kind=rng.choice(['qb','re']);y=F(rng.randrange(0,1001),2000)if kind=='re'else F(1,2)+F(rng.randrange(0,1000),100)
 x=y*y;v=1+k*(1-x)**2;g=x*(1-x)**2/(1+x);b=v+e*g;exact=(1/b if kind=='qb'else (1+k)**2/(2*(1+k)-b))**a
 ii=c.Scalar(a,k,1024,10000,1000000,100000,defect=e);l,h=ii.point(y,kind);ok(F(l,ii.S)<=exact<=F(h,ii.S),'new robust point exact rational enclosure')
 ok(0<=g<=v/k and b>=v,'global envelope scalar inequality')
 if kind=='re':ok(b<=1+k and 2*(1+k)-b>=1+k,'entire slab positive lower-price denominator')
for a in [4,16,64]:
 for k,e in [(F(1),F(0)),(F(1),F(1,1000)),(F(3,7),F(1,5))]:
  ii=c.Scalar(a,k,1024,10000,1000000,100000,defect=e)
  for left,right,kind in [(F(1,2),F(1),'qb'),(F(1),F(2),'qb'),(F(0),F(1,2),'re')]:
   l,h=ii.integrate(left,right,16,kind);vals=[]
   for j in range(33):
    y=left+(right-left)*j/32;x=y*y;b=1+k*(1-x)**2+e*x*(1-x)**2/(1+x);vals.append((1/b if kind=='qb'else (1+k)**2/(2*(1+k)-b))**a)
   ll=(right-left)/32*sum((min(x,y)for x,y in zip(vals,vals[1:])),F(0));hh=(right-left)/32*sum((max(x,y)for x,y in zip(vals,vals[1:])),F(0));ok(l<=ll<=hh<=h,'robust coarse enclosure contains independent refined Darboux')
for kind,left,right in [('qb',F(1,2),F(2)),('qb',F(0),F(1)),('re',F(0),F(1)),('re',F(-1),F(0))]:unknown(lambda kind=kind,left=left,right=right:c.Scalar(4,F(1),192,100,10000,10000,defect=F(1,1000)).integrate(left,right,32,kind),'unproved scalar segment refused')
ii=c.Scalar(4,F(1),192,2,10000,10000,defect=F(1,1000));ii.point(F(1),'q');ii.point(F(0),'r');unknown(lambda:ii.point(F(1),'qb'),'new lower mass shares full point budget')
for _ in range(350):
 k=F(rng.randrange(1,50),rng.randrange(1,50));e=k*F(rng.randrange(0,100),100);y=F(rng.randrange(-200,201),20);x=y*y;v=1+k*(1-x)**2;g=x*(1-x)**2/(1+x);b=v+e*g;u=v+F(rng.randrange(0,100),10);t=v+F(rng.randrange(0,100),10)
 ok(u+t-b>0 and u+t-b>=(1-e/k)*(u+t-v),'entire-domain cross-density price lower denominator')
 # Correct separate-current inflation is a square-root cross bound, not same source.
 A=F(rng.randrange(1,100));C=F(rng.randrange(1,100));eta=F(rng.randrange(0,100),100)
 ok((1+eta)*(A*A+eta*C*C)-(A+eta*C)**2==eta*(A-C)**2,'exact distinct-source weighted Cauchy identity')
raw=c.fixture(64);task={'defect':F(1,1000),'quad_relative':F(1,20),'full_ratio':F(2),'ks_error':F(3,4),'query_absolute_width':F(1),'times':[F(0),F(1000),F(10000)]};cert=c.certify(raw,**task)
def formula(cc,beta,k,e,mu,dmin,a):
 ml,mh=map(F,[cc['nominal_basin_mass']['lower'],cc['nominal_basin_mass']['upper']]);bl,bh=map(F,[cc['lower_density_basin_mass']['lower'],cc['lower_density_basin_mass']['upper']]);rl,rh=map(F,[cc['nominal_resistance']['lower'],cc['nominal_resistance']['upper']]);el,eh=map(F,[cc['robust_slab_resistance']['lower'],cc['robust_slab_resistance']['upper']]);z=cc['constants'];price=F(z['density_price_factor_upper']);L=1/(1-e/k);su=F(z['S_upper']);eta=su/ml;rho=su/bl;cs=F(z['source_S_nominal_factor_upper']);K=F(z['K_upper']);D=F(z['Dmax_upper']);star=1+k;ab=1+F(9,16)*k;d=F(1,a)
 ok(F(z['L'])==L and price*price>=L**(2*a+1),'full integrated density-price exponent alpha plus half')
 ok(K*K>=F(a*a,64)/(mu*mu*beta*dmin) and D*D>=16*a*a*max(k,F(1))**2/(mu*mu*beta*dmin) and (cs-1)**2>=k*k/(4*mu*mu*beta*dmin*ab**3),'all inherited moment root factors outward')
 rest={x:F(y)for x,y in cc['nominal_rest_components_upper'].items()};gb=star*star/(2*star-ab);g1=star*star/(2*star-1)
 ok(rest['near']>=mh*mh*(F(1,2)+d)*gb**a and rest['middle']>=star*star*g1**a/(128*k*k*(a-1)**2*d*d) and rest['vertical']>=K*k*k*g1**a and rest['far']==(1+D)/(16*k*k*(a-1)**2),'every full nominal non-slab current component')
 BA=beta*(mh*mh*eh+price*sum(rest.values(),F(0)));BS=price*beta*su*su*rh*cs;C=price*beta*mh*mh*rh*cs
 ok(F(cc['source_A_upper'])==BA and F(cc['source_S_upper'])==BS,'actual source domination priced against lower density')
 ok(F(z['eta_v_upper'])==eta and F(z['rho_actual_upper'])==rho and su>=ab**(-a),'distinct nominal source and actual-law mass ratios')
 cross=eta*(BA+C)/2;lo=beta*bl*rl;hi=(BA+cross)/bl
 ok(cross*cross>=BA*BS,'AMGM price dominates ACTUAL separate source cross bound')
 ok(F(cc['mean_hitting_time']['lower'])==lo and F(cc['mean_hitting_time']['upper'])==hi and F(cc['total_mean_ratio'])==hi/lo,'actual member mean lower and full upper with M_b')
 eps=(1+eta)*(BA+eta*C)/(beta*rl*bl*bl)-1;init=F(cc['initial_law_error_upper']);root=init-rho;kl=1/(beta*bh*rh);kh=1/(beta*bl*rl);rate=F(3,16)*(kh/kl-1);err=eps+init+rate
 ok(F(cc['spectral_error_upper'])==eps and root*root>=rho*(1+rho),'actual source spectral defect and initial-law root')
 ok(F(cc['reference_rate_enclosure']['lower'])==kl and F(cc['reference_rate_enclosure']['upper'])==kh and F(cc['reference_exponential_rate'])==(kl+kh)/2,'uniform reference uses lower-density M_b not actual or nominal mass')
 ok(F(cc['finite_rate_error_upper'])==rate and F(cc['uniform_KS_error_upper'])==err,'all uncertainty and rate error components retained')
 for q in cc['queries']:
  t=F(q['time']);l,h=map(F,[q['cdf']['lower'],q['cdf']['upper']]);ok(0<=l<=h<=1,'actual family CDF range')
  if not t:ok(l==h==0,'exact separated-set zero-time CDF');continue
  le,he=reference_exp((kl+kh)*t/2,cc['precision_bits']);ok(l<=max(F(0),1-he-err)and h>=min(F(1),1-le+err),'independently directed alternating actual CDF query enclosure')
formula(cert,F(1),F(1),F(1,1000),F(1),F(1),16);ok(c.verify(raw,cert,**task)['status']=='PASS','cheap literal original task full receiving')
# Known point ranges remain conservative members, not a secretly identified actual V.
rr=deepcopy(raw);rr['uncertainty_program']['ranges']=[['0','0']for _ in rr['energy_terms']];point=c.certify(rr,**task)
ok(point['acquisition']['unidentified_atom_weights']==0 and point['acquisition']['point_atom_weights']==len(rr['energy_terms']),'known-point versus unknown-range acquisition')
ok(point['mean_hitting_time']==cert['mean_hitting_time'] and point['queries']==cert['queries'],'narrower family conservatively retains same envelope not false specialization')
rr=deepcopy(raw);rr['uncertainty_program']['ranges'][-1]=['1/3','2/3'];cc=c.certify(rr,**task);ok(cc['mean_hitting_time']==cert['mean_hitting_time'],'nontrivial interior real-weight interval supported');unknown(lambda:c.verify(rr,cert,**task),'changed family cannot reuse old complete hash')
for mutation in ['missing','generic_envelope','adaptive','prior','extra','last_negative','last_reversed','last_over_one','canonical','bool','float','nested','oversized','range_count','missing_pure','negative_atom','last_mobility']:
 rr=deepcopy(raw);rs=rr['uncertainty_program']['ranges']
 if mutation=='missing':del rr['uncertainty_program']
 elif mutation in ['generic_envelope','adaptive','prior']:rr['uncertainty_program']['kind']=mutation
 elif mutation=='extra':rr['uncertainty_program']['claimed_global_proof']=True
 elif mutation=='last_negative':rs[-1][0]='-1'
 elif mutation=='last_reversed':rs[-1]=['1','0']
 elif mutation=='last_over_one':rs[-1][1]='2'
 elif mutation=='canonical':rs[-1][1]='1/1'
 elif mutation=='bool':rs[-1][0]=False
 elif mutation=='float':rs[-1][0]=0.0
 elif mutation=='nested':rs[-1][0]=['0']
 elif mutation=='oversized':rs[-1][1]='1/'+str(1<<4097)
 elif mutation=='range_count':rs.pop()
 elif mutation=='missing_pure':rr['energy_terms'].pop(63);rs.pop(63)
 elif mutation=='negative_atom':rr['energy_terms'][-1]['coefficient']='-1'
 else:rr['mobility_program']={'kind':'constant_diagonal','entries':['1']*63+['0']}
 unknown(lambda rr=rr:c.certify(rr,**task),'complete family refusal '+mutation)
class FF(F):pass
class II(int):pass
for key in ['defect','beta','kappa','quad_relative','full_ratio','ks_error','query_absolute_width']:
 for bad in [True,1,1.0,None,F(-1),FF(1,1000)]:unknown(lambda key=key,bad=bad:c.certify(raw,**dict(task,**{key:bad})),'strict exact rational task controls')
for key in ['max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_rational_bits','max_grid','max_points','max_cutoff','max_precision','max_operations','max_integer_bits','max_queries','max_exp_terms']:
 for bad in [True,1.0,None,0,-1,II(100)]:unknown(lambda key=key,bad=bad:c.certify(raw,**dict(task,**{key:bad})),'strict finite resource controls')
for times in [(),[True],[1],[1.0],[F(-1)],[F(1<<4097)],[[F(1)]]]:unknown(lambda times=times:c.certify(raw,**dict(task,times=times)),'malformed oversized or negative query times')
for e in [F(-1),F(1),F(2)]:unknown(lambda e=e:c.certify(raw,**dict(task,defect=e)),'exact defect domain gate')
# Shared costs, original lower-density roots and whole widths.
bit_total=sum(cert['acquisition'][k]for k in ['coefficient_bits_read','mobility_coefficient_bits_read','uncertainty_coefficient_bits_read'])
for key,val in [('max_total_coefficient_bits',bit_total),('max_grid',cert['N']),('max_points',cert['work']['scalar_points']),('max_precision',cert['precision_bits']),('max_operations',cert['work']['total_fixed_operations']),('max_integer_bits',max(cert['work'][k]for k in ['largest_scalar_product_bound_bits','largest_query_product_bound_bits','largest_root_integer_bound_bits']))]:
 ok(c.certify(raw,**dict(task,**{key:val}))['mean_hitting_time']==cert['mean_hitting_time'],'exact shared budget equality passes');unknown(lambda key=key,val=val:c.certify(raw,**dict(task,**{key:val-1})),'one-below shared budget refuses')
for ts in [None,[],[F(0),F(0)]]:
 cc=c.certify(raw,**dict(task,times=ts,max_operations=cert['work']['scalar_fixed_operations']));ok(cc['work']['query_fixed_operations']==0 and cc['work']['root_calls']==5,'optional empty zero query retains all-time root costs')
unknown(lambda:c.certify(raw,**dict(task,max_operations=cert['work']['scalar_fixed_operations'])),'query stage cannot reset shared product budget')
for key,value in [('full_ratio',F(cert['total_mean_ratio'])),('ks_error',F(cert['uniform_KS_error_upper'])),('query_absolute_width',max(F(q['cdf']['upper'])-F(q['cdf']['lower'])for q in cert['queries']))]:
 tt=dict(task,max_coefficient_bits=100000,**{key:value});ok(c.certify(raw,**tt)['mean_hitting_time']==cert['mean_hitting_time'],'exact total output tolerance equality passes');unknown(lambda key=key,value=value:c.certify(raw,**dict(task,max_coefficient_bits=100000,**{key:value-F(1,1<<10000)})),'below exact total output tolerance refuses')
for key in [k for k in cert if k not in ['work','seconds','queries']]:
 cc=deepcopy(cert);cc[key]=None;unknown(lambda cc=cc:c.verify(raw,cc,**task),'every outer proof field bound')
for key in ['nominal_basin_mass','lower_density_basin_mass','nominal_resistance','robust_slab_resistance','mean_hitting_time','reference_rate_enclosure']:
 for side in ['lower','upper']:
  cc=deepcopy(cert);cc[key][side]='0';unknown(lambda cc=cc:c.verify(raw,cc,**task),'every exact endpoint bound')
for text in ['nominal Gibbs conditioned on A','fixed angular ray','small TV preparation','adversarial time varying atom weights']:
 cc=deepcopy(cert);cc['observable']=text;unknown(lambda cc=cc:c.verify(raw,cc,**task),'actual member own full Gibbs and fixed family cannot be weakened')
for bad in [None,[],{},True]:unknown(lambda bad=bad:c.verify(raw,bad,**task),'malformed certificate object')
cc=deepcopy(cert);cc['queries']=[cc];unknown(lambda:c.verify(raw,cc,**task),'cyclic malformed query refuses')
cc=deepcopy(cert);cc['task']['times']=[cc];unknown(lambda:c.verify(raw,cc,**task),'cyclic wrong-type task refuses')
cc=deepcopy(cert);cc['queries']*=2000;unknown(lambda:c.verify(raw,cc,**task),'oversized output query list refuses')
cc=deepcopy(cert);cc['new_claim']=True;unknown(lambda:c.verify(raw,cc,**task),'extra unproved claim refuses')
cc=deepcopy(cert);cc['work']=None;cc['seconds']=None;cc['mean_hitting_time']['display']=None;cc['queries'][1]['cdf']['display']=None;ok(c.verify(raw,cc,**task)['status']=='PASS','diagnostics intentionally not proof inputs')
unknown(lambda:c.verify(raw,cert,**dict(task,times=list(reversed(task['times'])))),'literal original query order binds')
# Three full saved-family operations recaptured under literal controls, not record tasks.
saved=[]
for index,row in enumerate(json.loads((H/'robust_well_kinetics_20261031/results.json').read_text())):
 f=row['fixture'];r=c.fixture(512,F(20)if index<2 else F(10**100),index==2);e=F(0)if index==0 else F(1,1000);tt={'defect':e,'times':[F(0),F(10**36),F(4*10**36),F(10**37),F(10**38)]};cc=c.certify(r,**tt);old=row['certificate']
 ok(c.base.same(c.proof_record(cc),c.proof_record(old)),'actual saved family literal task whole recapture');ok(cc['work']==old['work'],'actual all paid work counters recaptured');formula(cc,F(1),F(1),e,F(1),F(1),128)
 N=cc['N'];J=F(cc['T']).numerator.bit_length()-1;points=(2*J+4)*N+4;powers=points+J+4;products=powers*17
 ok(cc['work']['scalar_points']==points and cc['work']['integer_power_calls']==powers and cc['work']['scalar_fixed_operations']==products and cc['work']['root_calls']==5,'independent four-profile scalar power product and root ledger')
 ops=0;terms=0
 for q in cc['queries']:
  t=F(q['time'])
  if not t:continue
  fx=c.base.Fixed(cc['precision_bits'],100000,100000,16384,1);x=F(cc['reference_exponential_rate'])*t;fx.expminus(x);shift=max(0,x.numerator.bit_length()-x.denominator.bit_length()+2);ok(fx.operations==4*fx.exp_terms+1+2*shift,'independent exponential product count');ops+=fx.operations;terms+=fx.exp_terms
 ok(cc['work']['query_fixed_operations']==ops and cc['work']['total_fixed_operations']==products+ops and cc['work']['exp_terms']==terms,'same total paid source and query budget')
 ok(cc['acquisition']['unidentified_atom_weights']==1023 and cc['acquisition']['uncertain_atom_intervals_read']==1023,'all 1023 actual fixed unknown weight slots read')
 saved.append({'defect':str(e),'fixture':f,'mean_display':cc['mean_hitting_time']['display'],'mean_ratio_display':float(F(cc['total_mean_ratio'])),'KS_display':float(F(cc['uniform_KS_error_upper'])),'query_4e36':cc['queries'][2]['cdf']['display'],'work':cc['work']})
rr=json.loads((H/'robust_well_kinetics_20261031/small_raw_fixture.json').read_text());cc=json.loads((H/'robust_well_kinetics_20261031/small_certificate.json').read_text());ok(c.verify(rr,cc,**task)['status']=='PASS','standalone small literal original task replay')
unknown(lambda:c.verify(rr,cc),'omitted original tolerances not adopted from certificate')
unknown(lambda:c.certify(c.fixture(512),defect=F(1,100),times=[]),'larger defect honest TOTAL mean refusal replay')
# Runtime dependency alteration in a deliberately isolated copy only.
d=H/'dependency_tamper';(d/'robust_well_kinetics_20261031').mkdir(parents=True);(d/'well_redistribution_mfpt_20261031').mkdir();shutil.copyfile(H/'robust_well_kinetics_20261031/receive_robust.py',d/'robust_well_kinetics_20261031/receive_robust.py');(d/'well_redistribution_mfpt_20261031/receive_mfpt.py').write_bytes((H/'well_redistribution_mfpt_20261031/receive_mfpt.py').read_bytes()+b'\n# isolated tamper\n');s=importlib.util.spec_from_file_location('bad_robust',d/'robust_well_kinetics_20261031/receive_robust.py');m=importlib.util.module_from_spec(s)
try:s.loader.exec_module(m)
except RuntimeError as e:ok(str(e)=='accepted well-current runtime dependency hash mismatch','dependency altered byte refused before import')
else:raise AssertionError('dependency admitted')
report={'status':'PASS','checks':sum(counts.values()),'categories':counts,'refusals':refusals,'saved_actual_recaptures':saved,'seconds_diagnostic':time.perf_counter()-start,'scope':'Every fixed admitted weight choice, its OWN exact full Gibbs|A; no member reconstruction or generic-envelope parser.'};(H/'independent_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['refusals','saved_actual_recaptures']},indent=2))
