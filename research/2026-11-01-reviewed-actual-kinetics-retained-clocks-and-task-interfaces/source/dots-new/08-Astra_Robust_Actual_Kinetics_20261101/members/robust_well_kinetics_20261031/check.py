from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import json,random
import sympy as s
import receive_robust as c
counts={}
def ok(x,label):
 assert x,label
 counts[label]=counts.get(label,0)+1
def unknown(fn,label):
 try:fn()
 except c.Unknown:ok(True,label)
 else:raise AssertionError('unexpected admission: '+label)
r=random.Random(2352)
y,k,e=s.symbols('y k e',real=True);x=s.symbols('x',nonnegative=True)
v=1+k*(1-y*y)**2;g=y*y*(1-y*y)**2/(1+y*y);b=v+e*g
rr=(2*x*x+3*x-1)/(1+x)**2
ok(s.simplify(s.diff(b,y)-2*y*(y*y-1)*(2*k+e*rr.subs(x,y*y)))==0,'exact global perturbed profile derivative')
ok(s.simplify(rr+1-x*(3*x+5)/(1+x)**2)==0,'global derivative bracket lower certificate')
ok(s.simplify(rr-1-(x+2)*(x-1)/(1+x)**2)==0,'well derivative bracket upper certificate')
ok(s.simplify(s.diff(g,y)*y-2*y*y*(y*y-1)*rr.subs(x,y*y))==0,'actual Lyapunov derivative identity')
ok(s.simplify(s.diff(b,y,2).subs(y,0)/2-(e-2*k))==0,'barrier local curvature')
ok(s.simplify(s.diff(b,y,2).subs(y,1)/2-(4*k+2*e))==0,'basin local curvature')
star=1+k;a=1+s.Rational(9,16)*k;Gb=star**2/(2*star-a)
ok(s.simplify(a*(star+1)-2*star-k*(2+9*k)/16)==0,'near-current condition dominates slab-mass condition')
ok(s.simplify((k*(1-Gb/star)).subs(k,1)-s.Rational(7,39))==0,'explicit sufficient asymptotic defect budget')
for _ in range(600):
 K=F(r.randrange(1,30),r.randrange(1,30));E=K*F(r.randrange(0,100),100);Y=F(r.randrange(-100,101),20);X=Y*Y
 V=1+K*(1-X)**2;G=X*(1-X)**2/(1+X);B=V+E*G;L=1/(1-E/K)
 sig=V+F(r.randrange(0,100),20);tau=V+F(r.randrange(0,100),20)
 ok(0<=G<=V/K and V<=B,'global energy/density envelope algebra')
 ok(sig+tau-B>0 and sig+tau-B>=(1-E/K)*(sig+tau-V),'positive squared-current density denominator')
 ok((sig+tau-V)/(sig+tau-B)<=L,'exact uniform integrated density-price inflation')
 if abs(Y)<=F(1,2):ok(B<=1+K,'robust slab denominator remains positive')
 # Source cross AM-GM and the separately named spectral join.
 A=F(r.randrange(1,100));C=F(r.randrange(1,100));eta=F(r.randrange(0,100),100)
 ok((1+eta)*(A*A+eta*C*C)-(A+eta*C)**2==eta*(A-C)**2,'separate-source weighted Cauchy identity')
# Exact directed scalar endpoints and independent rational Darboux sums.
for _ in range(120):
 alpha=r.randrange(4,15);K=F(r.randrange(1,8),r.randrange(1,8));E=K*F(r.randrange(0,100),100)
 ii=c.Scalar(alpha,K,192,10000,1000000,10000,defect=E)
 kind=r.choice(['qb','re']);aa,bb=(F(0),F(1,2))if kind=='re'else r.choice([(F(1,2),F(1)),(F(1),F(2))]);N=8
 def exact(Y):
  X=Y*Y;B=1+K*(1-X)**2+E*X*(1-X)**2/(1+X)
  return (1/B if kind=='qb'else (1+K)**2/(2*(1+K)-B))**alpha
 vals=[]
 for j in range(N+1):
  Y=aa+j*(bb-aa)/N;z=exact(Y);l,h=ii.point(Y,kind)
  ok(F(l,ii.S)<=z<=F(h,ii.S),'directed robust point contains exact rational power');vals.append(z)
 lower=(bb-aa)/N*sum(min(x,y)for x,y in zip(vals,vals[1:]));upper=(bb-aa)/N*sum(max(x,y)for x,y in zip(vals,vals[1:]))
 lo,hi=ii.integrate(aa,bb,N,kind);ok(lo<=lower<=upper<=hi,'independent exact monotone Darboux enclosure')
# A cheap complete family task exercises receiving without replacing actual law.
raw=c.fixture(64);task={'defect':F(1,1000),'quad_relative':F(1,20),'full_ratio':F(2),'ks_error':F(3,4),'query_absolute_width':F(1),'times':[F(0),F(1000),F(10000)]}
cert=c.certify(raw,**task);ok(c.verify(raw,cert,**task)['status']=='PASS','literal complete family receiving replay')
for key in ['defect','beta','kappa','quad_relative','full_ratio','ks_error','query_absolute_width']:
 for bad in [True,1,1.0,float('nan'),None,F(-1)]:
  q=dict(task);q[key]=bad;unknown(lambda q=q:c.certify(raw,**q),'strict external exact rational controls')
for key in ['max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_rational_bits','max_grid','max_points','max_cutoff','max_precision','max_operations','max_integer_bits','max_queries','max_exp_terms']:
 for bad in [True,1.0,None,0,-1]:
  q=dict(task);q[key]=bad;unknown(lambda q=q:c.certify(raw,**q),'strict finite resource controls')
for key,value in [('defect',F(1)),('quad_relative',F(1)),('full_ratio',F(1)),('ks_error',F(1)),('query_absolute_width',F(2)),('max_grid',1),('max_points',1),('max_cutoff',1),('max_precision',16),('max_operations',1),('max_exp_terms',1),('max_queries',1),('max_integer_bits',32),('full_ratio',F(1001,1000)),('ks_error',F(1,10000)),('query_absolute_width',F(1,10000))]:
 q=dict(task);q[key]=value;unknown(lambda q=q:c.certify(raw,**q),'honest total tolerance or finite-budget refusal')
for bad in [(),[True],[1],[1.0],[F(-1)],[[F(1)]]]:
 q=dict(task);q['times']=bad;unknown(lambda q=q:c.certify(raw,**q),'strict optional exact query interface')
for mutation in ['missing','extra','kind','range_count','bool','float','negative','over_one','reversed','nested','bad_canonical','false_global_certificate','missing_pure','negative_energy','actual_mobility']:
 rr=deepcopy(raw)
 if mutation=='missing':rr.pop('uncertainty_program')
 elif mutation=='extra':rr['unknown_external_term']='0'
 elif mutation=='kind':rr['uncertainty_program']['kind']='measured_local_samples'
 elif mutation=='range_count':rr['uncertainty_program']['ranges'].pop()
 elif mutation=='bool':rr['uncertainty_program']['ranges'][0][0]=False
 elif mutation=='float':rr['uncertainty_program']['ranges'][0][0]=0.0
 elif mutation=='negative':rr['uncertainty_program']['ranges'][0][0]='-1'
 elif mutation=='over_one':rr['uncertainty_program']['ranges'][0][1]='2'
 elif mutation=='reversed':rr['uncertainty_program']['ranges'][0]=['1','0']
 elif mutation=='nested':rr['uncertainty_program']['ranges'][0]=[['0'],'1']
 elif mutation=='bad_canonical':rr['uncertainty_program']['ranges'][0][0]='00'
 elif mutation=='false_global_certificate':rr['uncertainty_program']['certificate']='trust me'
 elif mutation=='missing_pure':rr['energy_terms'].pop(0);rr['uncertainty_program']['ranges'].pop(0)
 elif mutation=='negative_energy':rr['energy_terms'][0]['coefficient']='-1'
 else:rr['mobility_program']['value']='0'
 unknown(lambda rr=rr:c.certify(rr,**task),'global family acquisition refusal: '+mutation)
q=dict(task);q['max_total_coefficient_bits']=cert['acquisition']['coefficient_bits_read']+cert['acquisition']['mobility_coefficient_bits_read']
unknown(lambda:c.certify(raw,**q),'shared actual uncertainty coefficient budget is paid')
q=dict(task);q['max_operations']=cert['work']['scalar_fixed_operations']
unknown(lambda:c.certify(raw,**q),'scalar and exponential products share one budget')
q['times']=[];z=c.certify(raw,**q);ok(z['work']['total_fixed_operations']==z['work']['scalar_fixed_operations'],'no-query all-time law consumes no hidden exponential products')
for mutation in ['mean_lower','mean_upper','KS','sourceA','sourceS','density_factor','actual_family','task','uncertainty_count','query','proof','rate','rho','slab_integral','extra']:
 z=deepcopy(cert)
 if mutation=='mean_lower':z['mean_hitting_time']['lower']='1'
 elif mutation=='mean_upper':z['mean_hitting_time']['upper']='1'
 elif mutation=='KS':z['uniform_KS_error_upper']='0'
 elif mutation=='sourceA':z['source_A_upper']='0'
 elif mutation=='sourceS':z['source_S_upper']='0'
 elif mutation=='density_factor':z['constants']['density_price_factor_upper']='1'
 elif mutation=='actual_family':z['actual_generator_family']='nominal model'
 elif mutation=='task':z['task']['defect']='0'
 elif mutation=='uncertainty_count':z['acquisition']['unidentified_atom_weights']=True
 elif mutation=='query':z['queries'][1]['time']='1'
 elif mutation=='proof':z['proof_sha256']='0'*64
 elif mutation=='rate':z['reference_exponential_rate']='1'
 elif mutation=='rho':z['constants']['rho_actual_upper']='0'
 elif mutation=='slab_integral':z['robust_slab_resistance']['upper']='1'
 else:z['new_unproved_claim']=True
 unknown(lambda z=z:c.verify(raw,z,**task),'complete strict proof/task/model conjunction: '+mutation)
z=deepcopy(cert);z['work']={};z['seconds']=None;z['mean_hitting_time']['display']=[];z['queries'][1]['cdf']['display']=[]
ok(c.verify(raw,z,**task)['status']=='PASS','diagnostic displays and work cannot set proof or recomputation budget')
rr=deepcopy(raw);rr['uncertainty_program']['ranges'][0]=['0','0'];unknown(lambda:c.verify(rr,cert,**task),'different admitted family cannot reuse old acquisition binding')
# Saved production families: all actual operations are repeated, not trusted.
rows=json.loads(Path('results.json').read_text());reports=[]
for row in rows:
 f=row['fixture'];rr=c.fixture(f['m'],F(f['coupling']),f['diagonal']);tt={'defect':F(row['original_defect']),'times':[F(0),F(10**36),F(4*10**36),F(10**37),F(10**38)]}
 cc=row['certificate'];ok(c.verify(rr,cc,**tt)['status']=='PASS','full saved actual-family case replay')
 ok(F(cc['total_mean_ratio'])<=F(101,100)and F(cc['uniform_KS_error_upper'])<=F(1,100),'original mean and all-time uncertainty budget conjunction')
 for qq,t in zip(cc['queries'],tt['times']):
  lo,hi=F(qq['cdf']['lower']),F(qq['cdf']['upper']);ok(F(qq['time'])==t and 0<=lo<=hi<=1 and hi-lo<=F(1,50),'actual finite family CDF query times and probability widths')
 ok(cc['acquisition']['unidentified_atom_weights']==1023,'all actual microscopic shape weights remain unidentified')
 reports.append({'defect':row['original_defect'],'mean_ratio_display':float(F(cc['total_mean_ratio'])),'KS_display':float(F(cc['uniform_KS_error_upper'])),'total_products':cc['work']['total_fixed_operations']})
ok(rows[1]['certificate']['mean_hitting_time']==rows[2]['certificate']['mean_hitting_time']and rows[1]['certificate']['queries']==rows[2]['certificate']['queries'],'same outer bounds across two different admitted angular families, not same actual laws')
# Meaningful larger perturbation must not inherit the small-error certificate.
unknown(lambda:c.certify(c.fixture(512),defect=F(1,100),times=[]),'one-percent global profile defect does not meet one-percent total mean with this witness')
report={'status':'AUTHOR CHECKS PASS; independent theorem and whole receiving pending','checks':sum(counts.values()),'categories':counts,'actual_saved_families_recomputed':len(rows),'reports':reports}
Path('check_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
