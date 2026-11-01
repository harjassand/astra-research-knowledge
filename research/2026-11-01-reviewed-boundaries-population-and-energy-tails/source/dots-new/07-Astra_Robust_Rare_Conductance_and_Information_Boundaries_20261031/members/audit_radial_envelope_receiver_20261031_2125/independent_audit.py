"""Independent exact algebra, numerical, grammar and proof-field attack audit.
Runs against the copied, hash-matched frozen source. No source edits.
"""
from fractions import Fraction as F
from pathlib import Path
from copy import deepcopy
from math import comb, gcd
import hashlib, importlib.util, json, random, sys, time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'robustness_dilation_capacity_20261031'))
import receive_robustness as c
counts={}; events=[]; start=time.perf_counter()
def ok(b,cat):
    if not b: raise AssertionError(cat)
    counts[cat]=counts.get(cat,0)+1

def reject(fn,cat):
    try: fn()
    except c.Unknown as e:
        ok(True,cat); events.append({'category':cat,'reason':str(e)})
    else: raise AssertionError('false admission: '+cat)

def polyval(a,t):
    v=F(0)
    for x in reversed(a):v=v*t+x
    return v

def pmul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

def powpoly(a,n):
    out=[F(1)]
    for _ in range(n):out=pmul(out,a)
    return out

def exact_values(m,k,p,delta,shape,y):
    t=y*y;s=1+k*(1-t)**2
    e=t/(1+t)**2 if shape=='well_sensitive' else t*(t-1)**2/(1+t)**4
    l=s*(1-delta*e);u=s*(1+delta*e)
    return {'ql':l**(-m),'qu':u**(-m),'r0':l**m,'rp':((1+k)**(2*p)/(2*(1+k)**p-u**p))**(m//p)}

# Integer/rational truth checked without floating-point references or candidate power.
rng=random.Random(202610312125)
for j in range(800):
    x=F(rng.randrange(1,1000),rng.randrange(1,1000));n=rng.randrange(-150,151)
    d=rng.choice([1,2,4]);P=rng.randrange(2,160)
    ii=c.Integrator(1,F(1),4,F(1,500),'critical_flat',P,100,1000000)
    lo,hi=ii.bounds(x,n,d);S=1<<P
    ok(0<=lo<=hi,'directed power ordering')
    ok(F(lo,S)**d<=x**n<=F(hi,S)**d,'direct rational power/root enclosure')
# Exact powers of two, near-one rationals, tiny underflow, and large physical exponents.
for x in [F(1),F(2),F(1,2),F(2**200+1,2**200),F(1,2**200),F(2**100)]:
    for n in [-513,-512,-1,0,1,511,512,513]:
        for d in [1,2,4]:
            ii=c.Integrator(1,F(1),4,F(0),'critical_flat',192,100,2000000)
            lo,hi=ii.bounds(x,n,d)
            ok(F(lo,2**192)**d<=x**n<=F(hi,2**192)**d,'extreme exponent and dyadic boundaries')
# Independently generated exact endpoint Darboux references for all FOUR integrals.
for shape in ['critical_flat','well_sensitive']:
  for k in [F(1,16),F(1),F(7,3)]:
    delta=k/(4*(1+k))
    for p,m in [(2,2),(2,6),(4,4),(4,12)]:
      ii=c.Integrator(m,k,p,delta,shape,128,100000,1000000)
      for kind,a,b in [('ql',F(1,2),F(1)),('ql',F(1),F(2)),('ql',F(2),F(4)),('qu',F(1,2),F(1)),('qu',F(1),F(2)),('r0',F(0),F(1,2)),('rp',F(0),F(1,2))]:
        N=17;ys=[a+(b-a)*j/N for j in range(N+1)]
        vals=[exact_values(m,k,p,delta,shape,y)[kind] for y in ys]
        h=(b-a)/N;rl=h*sum(min(v,w) for v,w in zip(vals,vals[1:]));ru=h*sum(max(v,w) for v,w in zip(vals,vals[1:]))
        lo,hi=ii.integrate(a,b,N,kind)
        ok(lo<=rl<=ru<=hi,'independent four-integral Darboux enclosure')
# For delta zero r0 is a polynomial; directly integrate its coefficients.
for m in [1,2,3,4,8]:
  for k in [F(1,10),F(1),F(9,2)]:
    a=powpoly([1+k,0,-2*k,0,k],m)
    exact=sum(q*F(1,2)**(j+1)/(j+1) for j,q in enumerate(a))
    ii=c.Integrator(m,k,4,F(0),'critical_flat',192,10000,1000000)
    lo,hi=ii.integrate(F(0),F(1,2),73,'r0')
    ok(lo<=exact<=hi,'analytic polynomial resistance integral')
# Tail is computed independently from its analytic statement, all physical m.
for m in [1,3,4,7,64]:
  for shape,emax in [('critical_flat',F(1,16)),('well_sensitive',F(1,4))]:
    k=F(7,3);de=F(1,200);ii=c.Integrator(m,k,4,de,shape,256,100,1000000)
    for T in [F(3,2),F(2),F(7),F(16)]:
      for kind in ['ql','qu']:
        exact=(k*(1-T**-2)**2)**(-m)*T**(1-4*m)/F(4*m-1)
        if kind=='ql':exact/=(1-de*emax)**m
        got=ii.tail(T,kind)
        ok(exact<=got<exact+F(1,2**256),'independent physical-dimension tail and rounding')
# Projective polynomial certificate must not admit any exact negative witness.
for j in range(100):
    q=F(rng.randrange(1,100),rng.randrange(1,100));eps=F(1,rng.randrange(2,1000))
    # (t-q)^2-eps is negative at exact t=q, including remote/narrow regions.
    reject(lambda q=q,eps=eps:c.Bernstein(10000,18,100000).positive([q*q-eps,-2*q,F(1)]),'negative quadratic no false Bernstein acceptance')
for q in [F(1,2),F(1),F(2),F(99,7),F(1000000)]:
    p=[q*q,-2*q,F(1)]
    try:c.Bernstein(10000,12,100000).positive(p)
    except c.Unknown:ok(True,'nonnegative non-dyadic zero may refuse')
    else:ok(True,'nonnegative square admitted soundly')

# Complete raw read and order invariance; support every physical axis, scales, grammar.
raw=c.fixture(2,kappa=F(3,2),axis=2);de=F(1,500);ac=c.acquire(raw,de,'critical_flat')
rr=deepcopy(raw);rng.shuffle(rr['terms']);ar=c.acquire(rr,de,'critical_flat')
ok({k:v for k,v in ac.items() if k!='seconds'}=={k:v for k,v in ar.items() if k!='seconds'},'full raw canonical ordering invariant')
for axis in [0,1,2]:
    r=c.fixture(2,kappa=F(7,3),axis=axis,angular_scale=F(3,7));a=c.acquire(r,de,'critical_flat')
    ok(a['axis']==axis and F(a['kappa'])==F(7,3) and F(a['anchor_q_min'])==F(3,7),'independent axis parameter and anchor acquisition')
for shape in ['critical_flat','well_sensitive']:
    # Distinct heterogeneous profiles really defeat a single scalar dilation:
    r=c.fixture(2,shape=shape);a=c.acquire(r,de,shape);profs={}
    for rec in r['terms']:
        if rec['powers'][1:]==[2,0] or rec['powers'][1:]==[0,2]:
            key=tuple(rec['powers'][1:]);profs.setdefault(key,{})[rec['powers'][0]//2]=F(rec['coefficient'])
    ps=[ [d.get(j,F(0)) for j in range(21)] for d in profs.values()]
    ok(len(ps)==2 and polyval(ps[0],F(1,3))/ps[0][0]!=polyval(ps[1],F(1,3))/ps[1][0],'actual raw is not common geometric dilation')
# Invalid last entries cannot hide behind valid early recognition/cache reuse.
for change in ['coefficient','exponent','zero','malformed','odd_axis','remote_degree','duplicate']:
    r=deepcopy(raw)
    if change=='coefficient':r['terms'][-1]['coefficient']='1/0'
    elif change=='exponent':r['terms'][-1]['powers'][-1]=True
    elif change=='zero':r['terms'][-1]['coefficient']='0'
    elif change=='malformed':r['terms'][-1]['extra']=0
    elif change=='odd_axis':r['terms'][-1]['powers'][2]+=1
    elif change=='remote_degree':r['terms'].append({'powers':[2,0,50],'coefficient':'1'})
    else:r['terms'].append(deepcopy(r['terms'][0]))
    reject(lambda r=r:c.acquire(r,de,'critical_flat'),'last raw record fully scanned')
# Preserve anchor and degree but inject a compact-scale global envelope violation.
r=c.fixture(1,delta=F(0));terms={tuple(x['powers']):F(x['coefficient']) for x in r['terms']}
terms[(2,2)]=terms.get((2,2),F(0))-1000000
r['terms']=[{'powers':list(v),'coefficient':str(q)} for v,q in terms.items() if q]
reject(lambda:c.acquire(r,de,'critical_flat'),'nominal anchors do not bypass global inequality')
# Strict runtime parsing including oversized objects; no JSON decoder is claimed.
for v in [None,True,False,1.0,{},[],(),object(),'NaN','Infinity','-0','+1','1/01',' 1','1 ','1e0','0/1','1/'+'9'*140000]:
    r=deepcopy(raw);r['terms'][-1]['coefficient']=v
    reject(lambda r=r:c.acquire(r,de,'critical_flat'),'malformed oversized rational refusal')
for key in ['n','denominator','terms']:
    r=deepcopy(raw);del r[key]
    reject(lambda r=r:c.acquire(r,de,'critical_flat'),'missing raw schema field')
# Full exact cap saturation, with one-below refusals, includes exponent/bit scan costs.
for name,v in [('max_terms',ac['raw_terms']),('max_exponent_entries',ac['raw_exponent_entries']),('max_total_coefficient_bits',ac['total_input_coefficient_bits']),('max_bernstein_nodes',ac['bernstein_nodes']),('max_bernstein_bits',ac['bernstein_peak_stored_bits'])]:
    ok(c.acquire(raw,de,'critical_flat',**{name:v})['raw_potential_sha256']==ac['raw_potential_sha256'],'exact acquisition budget boundary passes')
    reject(lambda name=name,v=v:c.acquire(raw,de,'critical_flat',**{name:v-1}),'one-below acquisition budget refuses')

# Small independent consumer executions, exact reconstruction and budget coverage.
small=c.fixture(1);task={'delta':de,'quad_relative':F(1,20)}
cert=c.certify(small,**task)
fields=['mass_lower_profile','mass_upper_profile','resistance_lower_profile','jensen_upper_profile','uniform_rate_enclosure']
lo=1/(F(cert['task']['beta'])*F(cert[fields[0]]['upper'])*F(cert[fields[3]]['upper']))
hi=1/(F(cert['task']['beta'])*F(cert[fields[1]]['lower'])*F(cert[fields[2]]['lower']))
ok(lo==F(cert[fields[4]]['lower']) and hi==F(cert[fields[4]]['upper']) and hi/lo==F(cert['full_ratio_exact']),'consumer endpoints exact reconstruction')
product=F(1)
for key in fields[:4]:product*=F(cert[key]['upper'])/F(cert[key]['lower'])
ok(product<=1+task['quad_relative'],'all four numerical widths paid')
for key,v in [('max_grid',cert['N']),('max_evaluations',cert['scalar_evaluations']),('max_precision',cert['precision_bits']),('max_power_bits',cert['max_guarded_integer_bits'])]:
    cc=c.certify(small,**task,**{key:v});ok(cc['uniform_rate_enclosure']==cert['uniform_rate_enclosure'],'exact numerical budget boundary passes')
    reject(lambda key=key,v=v:c.certify(small,**task,**{key:v-1}),'one-below numerical budget refuses')
ratio=F(cert['full_ratio_exact'])
ok(c.certify(small,**task,full_ratio=ratio)['full_ratio_exact']==str(ratio),'exact total width boundary passes')
reject(lambda:c.certify(small,**task,full_ratio=(ratio+1)/2),'numerical tolerance is not total width')
# All proof-bearing fields protected independently, diagnostics deliberately excluded.
for k in ['schema','dependency_sha256','method','task','mobility_family','observable','basins','full_ratio_exact','N','T','precision_bits','tail_lower_profile','tail_upper_profile','acquisition']:
    for replacement in [None,False]:
        cc=deepcopy(cert);cc[k]=replacement
        reject(lambda cc=cc:c.verify(small,cc,**task),'proof field null or bool substitution')
for key in fields:
    for side in ['lower','upper']:
      for replacement in [None,True,1.0,'0']:
        cc=deepcopy(cert);cc[key][side]=replacement
        reject(lambda cc=cc:c.verify(small,cc,**task),'exact interval endpoint attack')
for k,v in cert['task'].items():
    cc=deepcopy(cert);cc['task'][k]=True
    reject(lambda cc=cc:c.verify(small,cc,**task),'all external task fields protected')
for k,v in cert['acquisition'].items():
    if k=='seconds':continue
    cc=deepcopy(cert);cc['acquisition'][k]=False
    reject(lambda cc=cc:c.verify(small,cc,**task),'all acquired proof fields protected')
for k in cert['mobility_family']:
    cc=deepcopy(cert);del cc['mobility_family'][k]
    reject(lambda cc=cc:c.verify(small,cc,**task),'all kinetic interface fields protected')
cc=deepcopy(cert);cc['seconds']=False;cc['scalar_evaluations']='untrusted';cc['uniform_rate_enclosure']['upper_display']=-1;cc['arbitrary_extra']='ignored'
ok(c.verify(small,cc,**task)['status']=='PASS','unbound diagnostics and extra fields not claimed authenticated')
# Saved exact endpoints and requested total widths checked without diagnostic floats.
saved=[]
for row in json.loads((HERE/'robustness_dilation_capacity_20261031/results.json').read_text()):
    s=row['certificate'];e=s['uniform_rate_enclosure'];L=F(e['lower']);H=F(e['upper']);R=H/L
    ok(R==F(s['full_ratio_exact']),'all saved exact total widths reconstructed')
    ok(L>0 and H>=L,'all saved positive exact endpoints')
    if s['task']['full_ratio'] is not None:ok(R<=F(s['task']['full_ratio']),'all saved requested total widths exact')
    saved.append({'m':row['m'],'shape':s['task']['shape'],'ratio_display':float(R),'low_display':float(L),'high_display':float(H),'raw_terms':s['acquisition']['raw_terms'],'raw_exponent_entries':s['acquisition']['raw_exponent_entries']})
ok(F(16000,15999)**1024>F(1066,1000),'strong reanchored global comparator exact bound')
report={'status':'PASS','assertions':sum(counts.values()),'categories':counts,'refusals':events,'saved_exact_extraction':saved,'seconds_diagnostic':time.perf_counter()-start,'scope':'Exact independent tests supplement mathematical whole audit; no physical membership or arbitrary-start latency.'}
(HERE/'independent_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='refusals'},indent=2))
