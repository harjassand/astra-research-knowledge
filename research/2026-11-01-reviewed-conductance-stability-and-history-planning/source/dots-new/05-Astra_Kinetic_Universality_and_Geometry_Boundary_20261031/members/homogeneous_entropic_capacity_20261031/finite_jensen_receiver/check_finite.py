"""Exact author checks for the additional finite Jensen operation."""
from fractions import Fraction as F
from pathlib import Path
import copy,json,random
import receive_jensen as j
count=0

def ck(x):
    global count
    assert x;count+=1

def no(fn):
    global count
    try:fn()
    except j.Unknown:count+=1;return
    raise AssertionError('expected UNKNOWN')

rng=random.Random(20261031)
# Extra integrand: ordered, correct outward fourth roots, monotone on the slab.
for m in [2,3,4,8,17]:
    for k in [F(1,10),F(1),F(10)]:
        ii=j.PlusIntegrator(m,k,128,1000,100000)
        previous=None
        for x in range(51):
            y=F(x,100);a=1+k;v=1+k*(1-y*y)**2;r=a*a/(2*a-v)
            ck(r>=v and r<=a)
            lo,hi=ii.point(y)[1]
            ck(F(lo,1<<128)**4<=r**m<=F(hi,1<<128)**4)
            if previous is not None:ck(hi<=previous)
            previous=hi
        lo,hi=ii.integrate(F(0),F(1,2),32,1);ck(0<lo<=hi)
        no(lambda:ii.point(F(3,4)))
# Delta profile exact algebra behind the extra resistance.
for _ in range(100):
    y=F(rng.randrange(0,101),200);k=F(rng.randrange(1,100),rng.randrange(1,100))
    a=1+k;v=1+k*(1-y*y)**2
    ck(a*a-v*(2*a-v)==(a-v)**2)
# Small positive producer/receiver and raw/task substitutions.
raw=j.base.fixture(3);cert=j.certify(raw)
ck(j.verify(raw,cert)['status']=='PASS')
ck(F(cert['structural_ratio']['lower'])>=1)
ck(F(cert['full_ratio_exact'])==F(cert['full_rate']['upper'])/F(cert['full_rate']['lower']))
base=j.base.certify(raw)
ck(F(cert['full_rate']['lower'])>F(base['full_rate']['lower']))
ck(cert['total_scalar_evaluations']==cert['point_evaluations']+cert['N']+1)
for key,val in [('full_ratio_exact','1'),('requested_full_ratio','2'),('scalar_source_sha256','wrong'),
                ('N',True),('schema','homogeneous_parallel_capacity.v1'),('structural_method','radial')]:
    bad=copy.deepcopy(cert);bad[key]=val;no(lambda bad=bad:j.verify(raw,bad))
for name in ['jensen_resistance','structural_ratio','full_rate']:
    for side in ['lower','upper']:
        bad=copy.deepcopy(cert);bad[name][side]='0';no(lambda bad=bad:j.verify(raw,bad))
bad=copy.deepcopy(cert);bad['acquisition']['couplings'][0][0]=True;no(lambda:j.verify(raw,bad))
bad=copy.deepcopy(cert);bad['factor_upper']='1';no(lambda:j.verify(raw,bad))
no(lambda:j.verify(j.base.fixture(3,coupling=F(21)),cert))
no(lambda:j.verify(raw,cert,full_ratio=F(2)))
no(lambda:j.verify(raw,cert,beta=F(2)))
for val in [True,1,1.0,F(1),F(0),F(-1),float('nan')]:no(lambda val=val:j.certify(raw,full_ratio=val))
no(lambda:j.certify(raw,full_ratio=F(100001,100000)))
no(lambda:j.certify(raw,max_points=cert['point_evaluations']))
no(lambda:j.certify(raw,max_points=cert['point_evaluations']+cert['N']))
no(lambda:j.certify(raw,full_ratio=F(2**100),max_coefficient_bits=10))
no(lambda:j.certify(raw,unsupported=1))
bad=copy.deepcopy(cert);bad['seconds']=-1;bad['jensen_resistance']['upper_display']=float('nan');ck(j.verify(raw,bad)['status']=='PASS')
# Input graph/strength/scale are checked but do not enter the final scalar bound.
ref=j.certify(j.base.fixture(4))
for graph,coupling,dmin in [('none',F(20),F(1)),('complete',F(2**1000),F(1,1000000)),('chain',F(1,1000000),F(10000))]:
    c=j.certify(j.base.fixture(4,graph=graph,coupling=coupling,dmin=dmin,axis=2))
    ck(c['full_rate']==ref['full_rate'])
c2=j.certify(j.base.fixture(4),beta=F(2))
for side in ['lower','upper']:ck(F(c2['full_rate'][side])==F(ref['full_rate'][side])/2)
# Every saved result is independently received from recreated raw input, including
# the costly m512 sub-1% requested full bracket. This replay is fully paid.
receipts=[]
for row in json.loads(Path('finite_results.json').read_text()):
    kwargs={'quad_relative':F(row['quad_relative']),
            'full_ratio':None if row['requested_full_ratio']is None else F(row['requested_full_ratio'])}
    rec=j.verify(j.base.fixture(row['m']),row['certificate'],**kwargs);receipts.append(rec);ck(rec['status']=='PASS')
    if row['m']==512:ck(F(row['certificate']['full_ratio_exact'])<F(101,100))
    print('replayed',row['m'],flush=True)
out={'status':'PASS','author_assertions':count,'receipts':receipts,
     'scope':'additional exact finite Jensen tests; inherited arithmetic has separate2550+471 review'}
Path('check_results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'status':'PASS','author_assertions':count},indent=2))
