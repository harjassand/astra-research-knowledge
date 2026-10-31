from fractions import Fraction as F
from pathlib import Path
import copy,json
import receive_parallel as r
count=0

def ck(x):
    global count
    assert x;count+=1

def no(fn):
    global count
    try:fn()
    except r.Unknown:count+=1;return
    raise AssertionError('expected UNKNOWN')

receipts=[]
for m in [2,3,4,16,64,128,256]:
    raw=r.base.fixture(m);c=r.certify(raw);receipts.append(r.verify(raw,c))
    factor=F(c['factor_upper']);ck(factor**2>=F(39,28));ck(factor<F(119,100))
    ck(F(c['full_rate']['upper'])/F(c['full_rate']['lower'])<=F(119,100)*F(101,100))
    old=r.base.certify(raw);ck(F(c['full_rate']['lower'])>F(old['full_rate']['lower']))
    ck(c['free_rate']==old['free_rate'])
# beta/d_min change the old radial factor but not this structural factor.
for k in [F(1,10),F(1),F(10)]:
    factors=[]
    for beta,dmin in [(F(1),F(1)),(F(2),F(1,1000000)),(F(1,10000),F(10000))]:
        raw=r.base.fixture(3,kappa=k,dmin=dmin);c=r.certify(raw,beta=beta)
        factors.append(c['factor_upper']);ck(F(c['factor_upper'])<F(13,10));ck(r.verify(raw,c,beta=beta)['status']=='PASS')
    ck(len(set(factors))==1)
# Couplings, graph and d_i can vary, but q and the complete received bracket agree
# when m,kappa,beta are fixed. This is not equality of the unknown true capacities.
ref=r.certify(r.base.fixture(4))
for graph,coupling,dmin in [('none',F(20),F(1)),('complete',F(2**1000),F(1,1000000)),('chain',F(1,1000000),F(10000))]:
    raw=r.base.fixture(4,graph=graph,coupling=coupling,dmin=dmin,axis=2);c=r.certify(raw)
    ck(c['full_rate']==ref['full_rate']);ck(r.verify(raw,c)['status']=='PASS')
raw=r.base.fixture(3);cert=r.certify(raw)
for path,val in [(('factor_squared_exact',),'1'),(('factor_upper',),'1'),(('scalar_source_sha256',),'wrong'),
                 (('structural_method',),'conditional radial'),(('schema',),'homogeneous_quartic_capacity.v1'),
                 (('full_rate','lower'),'0'),(('acquisition','axis'),False),(('task','max_points'),1000000.0)]:
    c=copy.deepcopy(cert);d=c
    for key in path[:-1]:d=d[key]
    d[path[-1]]=val;no(lambda c=c:r.verify(raw,c))
no(lambda:r.verify(r.base.fixture(3,coupling=F(21)),cert))
no(lambda:r.verify(raw,cert,beta=F(2)))
no(lambda:r.certify(raw,beta=float('nan')))
no(lambda:r.certify(raw,max_power_bits=10))
no(lambda:r.certify(raw,unrecognized=1))
no(lambda:r.verify(raw,r.base.certify(raw)))
c=copy.deepcopy(cert);c['seconds']=-100;c['full_rate']['lower_display']=float('nan');ck(r.verify(raw,c)['status']=='PASS')
out={'status':'PASS','wrapper_author_assertions':count,'receipts':receipts,
     'scope':'additional receiver tests; frozen scalar2550 checks and theorem proof are separate dependencies'}
Path('receiver_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
