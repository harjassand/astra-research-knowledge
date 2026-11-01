"""Independent exact numerical/model/receiver audit of frozen kinetic consumer."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
from math import factorial
import json,sys,random,time,hashlib
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'clean_replay'))
import receive_kinetic as c
counts={};refusals=[];start=time.perf_counter()
def ok(v,label):
 if not v:raise AssertionError(label)
 counts[label]=counts.get(label,0)+1

def unknown(fn,label):
 try:fn()
 except c.Unknown as e:ok(True,label);refusals.append({'case':label,'reason':str(e)})
 else:raise AssertionError('false admission: '+label)

# Independent exact exponential: unscaled positive rational Taylor sum and
# geometric bound on its entire remaining tail, then reciprocal. No Fixed code.
def expref(x,N=260):
 assert 0<=x<=40
 if not x:return F(1),F(1)
 t=s=F(1)
 for k in range(1,N+1):t=t*x/k;s+=t
 nxt=t*x/(N+1);tail=nxt/(1-x/(N+2))
 return 1/(s+tail),1/s

def mul(a,b):return a[0]*b[0],a[1]*b[1]
def add(a,b):return a[0]+b[0],a[1]+b[1]
def times(a,q):return a[0]*q,a[1]*q

def cdfref(alpha,lam,x,N=120):
 el=expref(lam);ex=expref(x);lo=hi=masslo=F(0)
 # Direct rational factorial formulas, not candidate fixed-point recurrences.
 for n in range(N):
  a=lam**n/F(factorial(n));w=times(el,a);masslo+=w[0]
  pref=sum((x**k/F(factorial(k)) for k in range(alpha+n)),F(0))
  gl=max(F(0),1-ex[1]*pref);gh=min(F(1),max(F(0),1-ex[0]*pref))
  lo+=w[0]*gl;hi+=w[1]*gh
 return lo,min(F(1),hi+max(F(0),1-masslo))

rng=random.Random(202610312153)
for i in range(160):
 x=F(rng.randrange(0,4001),100);P=rng.randrange(20,161);ii=c.Fixed(P,100000,100000,1000,1000)
 a,b=ii.expminus(x);l,u=expref(x)
 ok(F(a,ii.S)<=l<=u<=F(b,ii.S),'unscaled rational exponential reference')
for x in [F(0),F(1,2**300),F(1,2),F(1),F(2),F(16),F(40)]:
 ii=c.Fixed(256,100000,100000,1000,1000);a,b=ii.expminus(x);l,u=expref(x)
 ok(F(a,ii.S)<=l<=u<=F(b,ii.S),'exponential zero tiny and scaling boundaries')
for i in range(250):
 P=rng.randrange(8,160);ii=c.Fixed(P,100000,100000,1000,1000)
 x=F(rng.randrange(0,10000),rng.randrange(1,1000));y=F(rng.randrange(0,10000),rng.randrange(1,1000))
 a=ii.rat(x);b=ii.rat(y);z=ii.mul(a,b);zz=ii.times(a,y)
 ok(F(a[0],ii.S)<=x<=F(a[1],ii.S),'independent rational conversion')
 ok(F(z[0],ii.S)<=x*y<=F(z[1],ii.S),'independent fixed multiplication')
 ok(F(zz[0],ii.S)<=x*y<=F(zz[1],ii.S),'independent rational scaling')
# Noncentral (not just central) CDF references have full rational remainder bounds.
for alpha,lam,x in [(1,F(0),F(1,2)),(2,F(1,10),F(1)),(1,F(1),F(2)),(3,F(3,2),F(4)),(8,F(5),F(10)),(2,F(4),F(1,5))]:
 ii=c.Fixed(192,1000000,100000,1000,10000);a,b=ii.cdf_point(alpha,lam,x,F(1,10**18));l,u=cdfref(alpha,lam,x)
 ok(F(a,ii.S)<=l<=u<=F(b,ii.S),'noncentral Gamma independent rational series and full tail')
# Fixed-point extreme domains must soundly refuse or provide [0,1] absolute bounds.
for P,lam,x in [(16,F(1000),F(1)),(16,F(100),F(100))]:
 ii=c.Fixed(P,100000,100000,1000,1000)
 unknown(lambda:ii.cdf_point(1,lam,x,F(1,10**6)),'underresolved noncentral seed refusal')

raw=c.fixture(4,coupling=F(7,3),tangent=F(5,7))
z=[F(-2),F(1,2),F(0),F(-1,3)]
aq,u0,alpha=c.acquire(raw,z)
expected=sum(F(t['coefficient'])*__import__('functools').reduce(lambda x,y:x*y,[z[i]**n for i,n in enumerate(t['powers'])],F(1)) for t in raw['energy_terms'])
ok(u0==expected and alpha==1 and F(aq['coercivity_lower'])==F(1,4),'raw initial energy and norm coercivity independently reconstructed')
ok(aq['initial_energy_rational_operations']==5*len(raw['energy_terms']),'initial energy operation ledger all p factors plus sum')
# Nonzero tangent implies full SPD by kernel/Euler argument, not diagonal assumption.
for tangent in [F(0),F(1,10**100),F(10**100)]:
 a,u,al=c.acquire(c.fixture(4,tangent=tangent),[F(1),F(0),F(0),F(0)])
 ok(a['transverse_SPD_away_origin']==(tangent>0),'rank-one versus full-SPD declaration bound')
# Complete input ordering is part of this declared program hash (unlike prior canonical polynomial hash).
r=deepcopy(raw);r['energy_terms'].reverse();a,u,al=c.acquire(r,z)
ok(u==u0 and a['raw_sha256']!=aq['raw_sha256'],'reordered identical polynomial is different bound raw program')
# Last-record corruption cannot hide behind early degree recognition or homogeneity.
for mode in ['negative','zero','alias','odd','duplicate','missing_pure','unknown_extra','huge','nonhomogeneous','malformed']:
 r=deepcopy(raw)
 if mode=='negative':r['energy_terms'][-1]['coefficient']='-1'
 elif mode=='zero':r['energy_terms'][-1]['coefficient']='0'
 elif mode=='alias':r['energy_terms'][-1]['powers'][0]=False
 elif mode=='odd':r['energy_terms'][-1]['powers']=[0,0,1,3]
 elif mode=='duplicate':r['energy_terms'].append(deepcopy(r['energy_terms'][0]))
 elif mode=='missing_pure':r['energy_terms'].pop(0)
 elif mode=='unknown_extra':r['energy_terms'][-1]['extra']=0
 elif mode=='huge':r['energy_terms'][-1]['coefficient']='9'*9000
 elif mode=='nonhomogeneous':r['energy_terms'][-1]['powers']=[0,0,0,2]
 else:r['energy_terms'][-1]['powers']=None
 unknown(lambda r=r:c.acquire(r,z),'complete raw corruption refusal')
for value in [None,True,False,1,1.0,'+1','01','1/1','-0','1/0','1e0','NaN','Infinity',' 1','1 ','١']:
 r=deepcopy(raw);r['tangent_program']['weight']=value
 unknown(lambda r=r:c.acquire(r,z),'strict canonical tangent weight')
for value in [True,1.0,{},[],None,'identity','complete_pair_gradient ']:
 r=deepcopy(raw);r['tangent_program']['kind']=value
 unknown(lambda r=r:c.acquire(r,z),'actual tangent generator syntax refusal')
for name,v in [('max_dimension',4),('max_terms',aq['raw_terms']),('max_exponent_entries',aq['exponent_entries_read']),('max_total_coefficient_bits',aq['coefficient_bits_read'])]:
 ok(c.acquire(raw,z,**{name:v})[0]['raw_sha256']==aq['raw_sha256'],'exact raw resource boundary accepted')
 unknown(lambda name=name,v=v:c.acquire(raw,z,**{name:v-1}),'one-below raw resource boundary refuses')
for val in [True,1.0,0,-1]:
 for name in ['max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_rational_bits']:
  unknown(lambda name=name,val=val:c.acquire(raw,z,**{name:val}),'strict acquisition budget types')
unknown(lambda:c.acquire(raw,z,max_rational_bits=10),'initial energy rational precheck refusal')
# Independent protocol composition: direct sum over all future segment factors.
task={'initial_state':[F(1),F(0),F(0),F(0)],'protocol':[{'y':F(-1),'duration':F(1,3)},{'y':F(0),'duration':F(1,2)},{'y':F(1,2),'duration':F(2,3)}],'threshold':F(1),'beta':F(7,3),'kappa':F(5,4),'cdf_absolute_error':F(1,10**12)}
cert=c.certify(raw,**task);es=[];bs=[]
for j,seg in enumerate(task['protocol']):
 v=1+task['kappa']*(1-seg['y']**2)**2;e=expref(v*seg['duration']);b=((1-e[1])/(task['beta']*v),(1-e[0])/(task['beta']*v));es.append(e);bs.append(b)
 E=(F(1),F(1));B=(F(0),F(0))
 for q in es:E=mul(E,q)
 for k in range(j+1):
  q=bs[k]
  for ef in es[k+1:]:q=mul(q,ef)
  B=add(B,q)
 par=cert['parameters'][j]
 for key,ref in [('E',E),('B',B)]:ok(F(par[key]['lower'])<=ref[0]<=ref[1]<=F(par[key]['upper']),'independent protocol product-sum enclosure')
mean=add(E,times(B,F(1)));var=add(times(mul(E,B),F(2)),mul(B,B))
for key,ref in [('terminal_mean',mean),('terminal_variance',var)]:ok(F(cert[key]['lower'])<=ref[0]<=ref[1]<=F(cert[key]['upper']),'independent terminal moments')
ok(c.verify(raw,cert,**task)['status']=='PASS','independent chosen protocol full receiving')
# Clamping composition identity: splitting a constant segment preserves exact law;
# both outward boxes contain a common high-accuracy reference above, not identical rounding.
single=dict(task,protocol=[{'y':F(0),'duration':F(1)}]);split=dict(task,protocol=[{'y':F(0),'duration':F(1,3)},{'y':F(0),'duration':F(2,3)}])
a=c.certify(raw,**single);b=c.certify(raw,**split)
for key in ['terminal_CDF','terminal_mean','terminal_variance']:
 ok(max(F(a[key]['lower']),F(b[key]['lower']))<=min(F(a[key]['upper']),F(b[key]['upper'])),'constant-clamp subdivision consistency')
# Absolute width, not relative rare-probability accuracy.
tiny=c.certify(raw,**dict(task,threshold=F(1,10**100)))
l,h=F(tiny['terminal_CDF']['lower']),F(tiny['terminal_CDF']['upper'])
ok(l==0 and 0<=h-l<=task['cdf_absolute_error'],'rare CDF may have zero lower absolute enclosure')
# Every task/model/acquisition/endpoint binding is tested beyond author selections.
for key in ['schema','task','acquisition','operation','not_claimed','law','total_protocol_duration']:
 for val in [None,True]:
  cc=deepcopy(cert);cc[key]=val;unknown(lambda cc=cc:c.verify(raw,cc,**task),'all top proof fields typed binding')
for key in cert['acquisition']:
 cc=deepcopy(cert);cc['acquisition'][key]=None;unknown(lambda cc=cc:c.verify(raw,cc,**task),'all acquired proof fields bound')
for key in cert['task']:
 cc=deepcopy(cert);cc['task'][key]=True;unknown(lambda cc=cc:c.verify(raw,cc,**task),'all external task fields bound')
for key in ['terminal_CDF','terminal_mean','terminal_variance']:
 for side in ['lower','upper']:
  for val in [None,True,1.0,'0']:
   cc=deepcopy(cert);cc[key][side]=val;unknown(lambda cc=cc:c.verify(raw,cc,**task),'terminal exact endpoint corruption')
for i in range(len(cert['parameters'])):
 for key in ['v','duration']:
  cc=deepcopy(cert);cc['parameters'][i][key]='0';unknown(lambda cc=cc:c.verify(raw,cc,**task),'every protocol scalar parameter bound')
 for key in ['E','B']:
  for side in ['lower','upper']:
   cc=deepcopy(cert);cc['parameters'][i][key][side]='0';unknown(lambda cc=cc:c.verify(raw,cc,**task),'every protocol interval parameter bound')
changed=deepcopy(raw);changed['tangent_program']['weight']='0'
unknown(lambda:c.verify(changed,cert,**task),'changed tangent generator cannot reuse certificate')
changed=deepcopy(raw);changed['energy_terms'][-1]['coefficient']='99'
unknown(lambda:c.verify(changed,cert,**task),'changed energy input cannot reuse certificate')
cc=deepcopy(cert);cc['work']={'anything':False};cc['seconds']=None;cc['terminal_CDF']['display']=-1;cc['extra_field']='ignored'
ok(c.verify(raw,cc,**task)['status']=='PASS','diagnostics and extra fields explicitly unauthenticated')
# Finite precision, series, operations and total width are separate refusal domains.
for key in ['max_operations','max_integer_bits']:
 v=cert['work']['fixed_operations'] if key=='max_operations' else cert['work']['largest_guarded_product_bits']
 out=c.certify(raw,**task,**{key:v});ok(out['terminal_CDF']==cert['terminal_CDF'],'exact fixed budget boundary accepted')
 unknown(lambda key=key,v=v:c.certify(raw,**task,**{key:v-1}),'one-below fixed budget refuses')
unknown(lambda:c.certify(raw,**dict(task,precision_bits=16,cdf_absolute_error=F(1,10**30)),max_series_terms=100),'fixed precision cannot guarantee arbitrary accuracy')
for protocol in [None,[],[{'y':F(0)}],[{'y':F(0),'duration':F(0)}],[{'y':True,'duration':F(1)}],[{'y':F(0),'duration':F(1),'feedback':'energy'}]]:
 unknown(lambda protocol=protocol:c.certify(raw,**dict(task,protocol=protocol)),'fixed declared protocol schema and no implicit feedback')
# Saved standalone input/certificate not exercised by author's four-row loop.
rr=json.loads((H/'clean_replay/small_raw_fixture.json').read_text());cc=json.loads((H/'clean_replay/small_certificate.json').read_text())
ok(c.verify(rr,cc,**c.external_from_record(cc))['status']=='PASS','standalone saved raw certificate replay')
# Recompute saved cases directly and capture diagnostic work; verifier does not bind it.
saved=[]
for row in json.loads((H/'clean_replay/results.json').read_text()):
 fi=row['fixture'];rr=c.fixture(fi['m'],fi['p'],F(fi['coupling']),F(fi['tangent']));old=row['certificate']
 # Literal reconstruction of the source's ORIGINAL external task, not certificate-selected tasks.
 original={'initial_state':[F(1)]+[F(0)]*(fi['m']-1),'protocol':[{'y':F(-1),'duration':F(1,3)},{'y':F(0),'duration':F(1,2)},{'y':F(1,2),'duration':F(2,3)}],'threshold':F(fi['m'],8),'cdf_absolute_error':F(1,10**10)}
 new=c.certify(rr,**original)
 ok(c.verify(rr,old,**original)['status']=='PASS','saved replay with literal original external task')
 for key in ['task','acquisition','parameters','terminal_CDF','terminal_mean','terminal_variance','work']:ok(new[key]==old[key],'independently recaptured saved exact fields and work')
 l,h=F(new['terminal_CDF']['lower']),F(new['terminal_CDF']['upper']);tol=F(new['task']['cdf_absolute_error'])
 ok(0<=l<=h<=1 and h-l<=tol,'saved total absolute width exact')
 saved.append({'fixture':fi,'CDF':new['terminal_CDF'],'width_exact':str(h-l),'work':new['work'],'raw_exponent_entries':new['acquisition']['exponent_entries_read']})
ok(saved[-1]['CDF']==saved[-2]['CDF'],'paired 512D outputs exact equal')
# Ordinary Gaussian and quartic classes get the same scalar backend when alpha,u match.
common={'protocol':task['protocol'],'threshold':F(2),'cdf_absolute_error':F(1,10**12)}
ga=c.certify(c.fixture(4,p=2),initial_state=[F(1)]+[F(0)]*3,**common)
qu=c.certify(c.fixture(8,p=4),initial_state=[F(1)]+[F(0)]*7,**common)
ok(ga['terminal_CDF']==qu['terminal_CDF'],'ordinary Gaussian comparator retained without handicap')
report={'status':'PASS','checks':sum(counts.values()),'categories':counts,'refusals':refusals,'saved_recaptured':saved,'seconds_diagnostic':time.perf_counter()-start,'scope':'Declared homogeneous engineered generator, fixed clamp terminal energy CDF, absolute errors only.'}
(H/'independent_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['refusals','saved_recaptured']},indent=2))
