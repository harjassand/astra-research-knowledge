"""Author checks: exact algebra/arithmetic, receiver corruption and budgets.
No sampling/PDE approximation is a proof premise. Standard library only.
"""
import copy,json,random
from pathlib import Path
from fractions import Fraction as F
import compile as c

count=0

def check(test):
    global count
    assert test
    count+=1

def unknown(fn):
    global count
    try:fn()
    except c.Unknown:count+=1;return
    raise AssertionError('expected UNKNOWN')

rng=random.Random(20261031)
for degree in [2,4]:
    for _ in range(500):
        a=F(rng.randrange(0,10**10),rng.randrange(1,10**8));p=rng.randrange(0,100)
        lo,hi=c.root_bounds(a,p,degree)
        check(F(lo,1<<p)**degree<=a<=F(hi,1<<p)**degree)
        check(hi-lo in (0,1))
        if hi==lo:check(F(lo,1<<p)**degree==a)
for degree in [2,4]:
    for a in [F(0),F(1),F(16),F(81,16),F(1,256)]:
        lo,hi=c.root_bounds(a,20,degree)
        check(F(lo,1<<20)**degree<=a<=F(hi,1<<20)**degree)

# Exact acquired coercivity, Euler identity and normalized continuity identity.
for m in [2,3,4,7]:
    raw=c.fixture(m,graph='complete',coupling=F(20),axis=m//2);acq=c.acquire(raw)
    check(acq['axis']==m//2 and acq['m']==m and acq['kappa']=='1')
    for _ in range(20):
        z=[F(rng.randrange(-5,6),rng.randrange(1,7)) for j in range(m)]
        U=sum(x**4 for x in z)+20*sum(z[i]**2*z[j]**2 for i in range(m) for j in range(i+1,m))
        grad=[4*z[i]**3+40*z[i]*sum(z[j]**2 for j in range(m) if j!=i) for i in range(m)]
        check(sum(z[i]*grad[i] for i in range(m))==4*U)
        check(m*sum(x**4 for x in z)-sum(x*x for x in z)**2==sum((z[i]**2-z[j]**2)**2 for i in range(m) for j in range(i+1,m)))
        check(U>=sum(x*x for x in z)**2/m)
        y=F(rng.randrange(0,50),100);v=1+(1-y*y)**2;vp=-4*y*(1-y*y)
        log_rho_y=F(m,4)*vp/v-vp*U
        div_w=-F(m,4)*vp/v
        grad_log_dot_w=vp*sum(z[i]*grad[i] for i in range(m))/4
        check(log_rho_y+div_w+grad_log_dot_w==0)
        check(-vp <= 4*y)  # exact numerator comparison underlying f bound
# Concrete nonconvex admitted U: Hessian eigenvector (1,-1) at(1,1).
check(12-2*20<0)

# Direct monomial input corruption, including complete cross-degree identity.
raw=c.fixture(3,axis=2);base=c.acquire(raw)
for index in range(len(raw['terms'])):
    bad=copy.deepcopy(raw);bad['terms'][index]['coefficient']=str(F(bad['terms'][index]['coefficient'])+F(1,17))
    unknown(lambda bad=bad:c.acquire(bad))
for value in [True,1.0,'02','1/1','nan','1/0',None]:
    bad=copy.deepcopy(raw);bad['terms'][0]['coefficient']=value
    unknown(lambda bad=bad:c.acquire(bad))
for value in [True,1.0,-1,9]:
    bad=copy.deepcopy(raw);bad['terms'][0]['powers'][0]=value
    unknown(lambda bad=bad:c.acquire(bad))
bad=copy.deepcopy(raw);bad['terms'].append(copy.deepcopy(bad['terms'][0]));unknown(lambda:c.acquire(bad))
bad=copy.deepcopy(raw);bad['terms'].pop();unknown(lambda:c.acquire(bad))
unknown(lambda:c.acquire(c.fixture(1)))
unknown(lambda:c.acquire(c.fixture(2,coupling=F(-1))))
unknown(lambda:c.acquire(raw,max_dimension=3))
unknown(lambda:c.acquire(raw,max_terms=2))
unknown(lambda:c.acquire(raw,max_coefficient_bits=2))
# A physical rotation of y,z makes both present in F4: raw finder must UNKNOWN.
rot={'n':3,'terms':[{'powers':[4,0,0],'coefficient':'1'},{'powers':[0,4,0],'coefficient':'1'},{'powers':[0,0,4],'coefficient':'1'}]}
unknown(lambda:c.acquire(rot))

# All fixed-budget exits and strict task types occur before uncontrolled loops.
for name in ['max_dimension','max_terms','max_coefficient_bits','max_grid','max_points','max_cutoff','max_precision','max_power_bits']:
    for val in [True,1.0,0,-1,float('nan')]:
        unknown(lambda name=name,val=val:c.certify(raw,**{name:val}))
for name in ['beta','quad_relative']:
    for val in [True,1,1.0,float('nan'),F(0),F(-1)]:
        unknown(lambda name=name,val=val:c.certify(raw,**{name:val}))
for kw in [{'max_grid':1},{'max_points':1},{'max_cutoff':1},{'max_cutoff':2},{'max_precision':1},{'max_power_bits':10}]:
    unknown(lambda kw=kw:c.certify(c.fixture(2),**kw))
unknown(lambda:c.certify(c.fixture(2,kappa=F(2**1000)),max_precision=192))
unknown(lambda:c.certify(c.fixture(2,kappa=F(1,2**100)),max_cutoff=64))
unknown(lambda:c.acquire({'n':3,'terms':[{'powers':[0,4,0],'coefficient':2**20000}]}))
check(c.show(F(2**2000)) is None and c.show(F(1,2**2000)) is None)

# Positive runs, partition-free invariance of the certified bound under coupling
# graph changes (NOT an assertion of identical true full capacities).
receipts=[];reference={}
for m in [2,3,4,16,64,128,256]:
    raw=c.fixture(m);cert=c.certify(raw);receipts.append(c.verify(raw,cert))
    check(cert['factor_upper']=='157/125')
    check(F(cert['full_rate']['upper'])/F(cert['full_rate']['lower'])<=F(157,125)*F(101,100))
    reference[m]=cert
for graph,coupling in [('none',F(20)),('chain',F(2000000)),('complete',F(1,1000))]:
    raw=c.fixture(4,graph=graph,coupling=coupling,axis=3);cert=c.certify(raw)
    check(cert['full_rate']==reference[4]['full_rate'])
    check(c.verify(raw,cert)['status']=='PASS')
raw=c.fixture(3,axis=2);cert=c.certify(raw)
# Reorder exact raw terms: polynomial identity remains the same.
rev=copy.deepcopy(raw);rev['terms'].reverse();check(c.verify(rev,cert)['status']=='PASS')
for path,val in [(('acquisition','axis'),True),(('acquisition','m'),3.0),(('task','max_dimension'),1024.0),
                 (('N',),True),(('factor_upper',),'1'),(('mass','lower'),'0'),(('full_rate','upper'),'1'),
                 (('observable',),'MFPT'),(('basins',),'arbitrary basins')]:
    bad=copy.deepcopy(cert);d=bad
    for k in path[:-1]:d=d[k]
    d[path[-1]]=val;unknown(lambda bad=bad:c.verify(raw,bad))
for val in [True,0.0]:
    bad=copy.deepcopy(cert);bad['acquisition']['couplings'][0][0]=val
    unknown(lambda bad=bad:c.verify(raw,bad))
unknown(lambda:c.verify(c.fixture(3,axis=2,coupling=F(21)),cert))
unknown(lambda:c.verify(raw,cert,beta=F(2)))
# Non-proof diagnostics may differ or be absent, never influence admission.
bad=copy.deepcopy(cert);bad['full_rate']['lower_display']=float('nan');bad['seconds']=-1
check(c.verify(raw,bad)['status']=='PASS')
# Non-square parameter factor remains an exact outward rational upper bound.
raw=c.fixture(3,kappa=F(2,3),dmin=F(3,7));cert=c.certify(raw,beta=F(5,11))
k=F(2,3);vmin=1+F(9,16)*k;d=F(3,7);beta=F(5,11);fac=F(cert['factor_upper'])
check((fac-1)**2>=k*k/(4*beta*d*vmin**3));check(c.verify(raw,cert,beta=beta)['status']=='PASS')
# Extreme beta doesn't poison valid exact outputs via optional float display.
cert=c.certify(c.fixture(2),beta=F(1,2**2000));check(cert['full_rate']['upper_display']is None)
check(c.verify(c.fixture(2),cert,beta=F(1,2**2000))['status']=='PASS')

out={'status':'PASS','author_assertions':count,'receipts':receipts,'scope':'exact author tests, not independent audit'}
Path('check_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
