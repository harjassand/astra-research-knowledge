"""Exact author regression/adversarial checks; every saved certificate is recomputed."""
from fractions import Fraction as F
from copy import deepcopy
from pathlib import Path
import json,random
import receive_dilation as c
checks=0;categories={}
def ok(v,label):
 global checks
 assert v,label
 checks+=1;categories[label]=categories.get(label,0)+1

def unknown(fn,label):
 try:fn()
 except c.Unknown:ok(True,label)
 else:raise AssertionError('accepted: '+label)

rng=random.Random(1912)
for _ in range(1200):
 x=F(rng.randint(1,100),rng.randint(1,100));n=rng.randint(-19,19);d=rng.choice([1,2,4]);P=rng.randint(1,80)
 ii=c.Integrator(1,F(1),4,P,100,100000);lo,hi=ii.bounds(x,n,d)
 ok(F(lo,1<<P)**d<=x**n<=F(hi,1<<P)**d,'root enclosure');ok(0<=hi-lo<=1,'root width')
for m in range(1,21):
 ii=c.Integrator(m,F(3,2),4,256,100,100000)
 for y in [F(0),F(1,8),F(3,8),F(1,2)]:
  s=ii.profile(y);x=ii.s02p/(2*ii.s0p-s**4);lo,hi=ii.point('rplus',y)
  ok(F(lo,1<<256)**4<=x**m<=F(hi,1<<256)**4,'extra integrand enclosure');ok(x**m>=s**(4*m),'extra dominates free')
for m in range(1,9):
 ii=c.Integrator(m,F(1),4,512,100000,100000)
 lower=sum((ii.integrate(F(j),F(j+1),32,'q')[0] for j in range(2,10)),F(0))
 ok(ii.tail(F(2))>=lower,'physical m tail bound')
for d in [2,4]:
 for j in range(1,101):
  r=F(j,100);ok((2-r**d)**4>=(2-r**4)**d,'radial p4 concavity')
for i in range(-100,101):
 t=F(i,13)**2;U=t-t*t+t**3+t**4
 ok(12*t-16*t*t+12*t**3>=0 and U>=F(3,4)*t+t**4,'broader radial certificate')
for k in [F(1,100),F(1),F(100)]:
 for j in range(-100,101):
  y=F(j,7);s=1+k*(1-y*y)**2;ok(4*k*y*y*(y*y-1)/s>=-k,'global Lyapunov bracket')
c1=F(8065,4096);c2=F(7121,4096);A=(c1*c1-c2*c2)/(c1*c1+c2*c2);tstar=2/(c1*c1+c2*c2)
ok(c1>c2>0 and A>0,'barrier constants');ok(c1*c1*tstar-1==1-c2*c2*tstar==A,'barrier threshold')
ok(2-F(1,6)+F(1,80)==F(443,240),'obstruction exact R0')
for m in [1,2,3,5]:
 for axis in range(m+1):
  for k in [F(1,5),F(1),F(5,2)]:
   raw=c.fixture(m,kappa=k,axis=axis);a=c.acquire(raw)
   ok(a['axis']==axis and a['m']==m and F(a['kappa'])==k,'raw axis/parameter')
   ok(a['degree_cap']==4 and a['energy_is_mixed_degree'] is True,'mixed degree acquired')
   ok(max(sum(t['powers']) for t in raw['terms'])==20,'whole degree 20')
raw=c.fixture(2);a=c.acquire(raw)
for j in range(len(raw['terms'])):
 r=deepcopy(raw);r['terms'][j]['coefficient']=c.fs(F(r['terms'][j]['coefficient'])+F(1,7));unknown(lambda r=r:c.acquire(r),'every coefficient checked')
 r=deepcopy(raw);del r['terms'][j];unknown(lambda r=r:c.acquire(r),'every monomial required')
for bad in [None,[],True,{'n':3,'terms':[]},dict(raw,extra=1),dict(raw,n=True),dict(raw,n=3.0)]:unknown(lambda bad=bad:c.acquire(bad),'raw schema refusal')
for value in [True,1.0,'1.0','01','2/2','nan','0','1/0']:
 r=deepcopy(raw);r['terms'][0]['coefficient']=value;unknown(lambda r=r:c.acquire(r),'strict coefficients')
for value in [True,2.0,-1,21]:
 r=deepcopy(raw);r['terms'][0]['powers'][1]=value;unknown(lambda r=r:c.acquire(r),'strict exponents')
r=deepcopy(raw);r['terms'].append(deepcopy(r['terms'][0]));unknown(lambda:c.acquire(r),'duplicate refusal')
for kw in [dict(quadratic=F(-1)),dict(quadratic=F(0)),dict(quartic=F(-1)),dict(coupling=F(-1))]:unknown(lambda kw=kw:c.acquire(c.fixture(2,**kw)),'component/coercivity refusal')
r=deepcopy(raw);r['terms'].append({'powers':[1,3,0],'coefficient':'1'});unknown(lambda:c.acquire(r),'full identity not Hessian only')
ok((2+12+40)-80<0,'genuine nonconvex admitted U')
rq=c.fixture(2,quartic=F(0),coupling=F(0));cq=c.certify(rq)
ok(cq['acquisition']['degree_cap']==2 and not cq['acquisition']['energy_is_mixed_degree'],'strong quadratic comparator');ok(c.verify(rq,cq)['status']=='PASS','quadratic replay')
r=deepcopy(raw);r['terms'].reverse();ar=c.acquire(r)
ok({k:v for k,v in ar.items() if k!='seconds'}=={k:v for k,v in a.items() if k!='seconds'},'raw order invariance')
base=c.certify(c.fixture(3));alt=c.certify(c.fixture(3,quadratic=F(3,7),quartic=F(999),coupling=F(1024),graph='complete'))
for key in ['mass','resistance','jensen_resistance','free_rate','uniform_rate_enclosure']:ok(base[key]==alt[key],'unknown U outer bound independence')
slow=c.certify(c.fixture(3),beta=F(1,7))
for side in ['lower','upper']:ok(F(slow['uniform_rate_enclosure'][side])==7*F(base['uniform_rate_enclosure'][side]),'beta scaling')
kwargs=[dict(beta=1),dict(beta=True),dict(beta=float('nan')),dict(beta=F(0)),dict(quad_relative=float('nan')),dict(quad_relative=F(0)),dict(full_ratio=1.01),dict(full_ratio=F(1)),dict(full_ratio=True)]
for key in ['max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_grid','max_evaluations','max_cutoff','max_precision','max_power_bits']:
 for value in [True,1.0,0,-1]:kwargs.append({key:value})
for kw in kwargs:unknown(lambda kw=kw:c.certify(raw,**kw),'strict external task refusal')
for kw in [dict(max_dimension=2),dict(max_terms=2),dict(max_coefficient_bits=2),dict(max_exponent_entries=4),dict(max_total_coefficient_bits=5),dict(max_grid=63),dict(max_grid=64),dict(max_evaluations=5),dict(max_cutoff=1),dict(max_cutoff=2),dict(max_precision=100),dict(max_power_bits=100),dict(quad_relative=F(1,10**8),max_grid=64),dict(full_ratio=F(1000001,1000000))]:unknown(lambda kw=kw:c.certify(raw,**kw),'budgeted UNKNOWN')
ii=c.Integrator(2,F(2**1000),4,192,1000,100000);ok(ii.integrate(F(1),F(5,4),32,'q')[0]==0,'zero seed diagnosed')
tiny=c.certify(c.fixture(1),beta=F(1,2**2000));ok(tiny['uniform_rate_enclosure']['lower_display'] is None,'optional overflow display')
r=c.fixture(1);cert=c.certify(r)
for key,value in [('schema','wrong'),('method','wrong'),('observable','MFPT'),('basins','partial fibers'),('b',0.5),('marginal','approximation'),('full_ratio_exact','1'),('N',float(cert['N'])),('T',2),('precision_bits',True),('tail_upper','0')]:
 cc=deepcopy(cert);cc[key]=value;unknown(lambda cc=cc:c.verify(r,cc),'original model binding')
for key,value in [('axis',False),('m',True),('energy_is_mixed_degree',1),('kappa',1.0),('quadratic_diagonals',[[True,'1']]),('active_energy_degrees',[2.0,4]),('raw_polynomial_sha256','0'*64)]:
 cc=deepcopy(cert);cc['acquisition'][key]=value;unknown(lambda cc=cc:c.verify(r,cc),'typed nested acquisition')
for key in cert['mobility_family']:
 cc=deepcopy(cert);cc['mobility_family'][key]='different';unknown(lambda cc=cc:c.verify(r,cc),'kinetic family binding')
for key in ['mass','resistance','jensen_resistance','free_rate','uniform_rate_enclosure','structural_ratio']:
 for side in ['lower','upper']:
  cc=deepcopy(cert);cc[key][side]=c.fs(F(cc[key][side])+F(1,99));unknown(lambda cc=cc:c.verify(r,cc),'exact endpoint binding')
cc=deepcopy(cert);cc['task']['beta']='2';unknown(lambda:c.verify(r,cc),'external beta task binding');unknown(lambda:c.verify(r,cert,beta=F(2)),'external changed task')
cc=deepcopy(cert);cc['seconds']='untrusted';cc['scalar_evaluations']=False;cc['mass']['lower_display']='untrusted';ok(c.verify(r,cc)['status']=='PASS','diagnostics outside proof binding')
replays=[]
for row in json.loads(Path('results.json').read_text()):
 target=row['requested_full_ratio'];target=None if target is None else F(target)
 out=c.verify(c.fixture(row['m']),row['certificate'],quad_relative=F(row['quad_relative']),full_ratio=target)
 ok(out['status']=='PASS','saved full replay')
 if target is not None:ok(F(out['full_ratio_exact'])<=target,'requested total ratio received')
 replays.append({'m':row['m'],'status':out['status']})
ok(c.verify(json.loads(Path('small_raw_fixture.json').read_text()),json.loads(Path('small_certificate.json').read_text()))['status']=='PASS','saved nonfirst axis replay')
report={'status':'PASS','checks':checks,'categories':categories,'saved_replays':replays,'scope':'Exact arithmetic and receiving tests supplement the ordinary proof; no physical or MFPT upgrade.'}
Path('check_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
