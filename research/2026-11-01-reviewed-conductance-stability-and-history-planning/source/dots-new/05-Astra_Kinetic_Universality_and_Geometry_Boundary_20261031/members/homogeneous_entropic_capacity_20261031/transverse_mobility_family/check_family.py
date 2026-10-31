"""Exact author family receiving and finite-matrix algebra checks.
The infinite-dimensional range proof is not replaced by these finite tests.
"""
from fractions import Fraction as F
from pathlib import Path
import copy,json,random
import receive_family as f
count=0

def ck(x):
    global count
    assert x;count+=1

def no(fn):
    global count
    try:fn()
    except f.Unknown:count+=1;return
    raise AssertionError('expected UNKNOWN')

rng=random.Random(20261031)
# Exact 2D SPD shape algebra: the weighted Lyapunov drift and diffusion trace
# cancel M, including off-diagonal and ill-conditioned rational examples.
for _ in range(100):
    l1=F(rng.randrange(1,100),rng.randrange(1,100));l2=F(rng.randrange(1,100),rng.randrange(1,100));u=F(rng.randrange(-100,101),rng.randrange(1,100))
    M=[[l1*l1,l1*u],[l1*u,u*u+l2*l2]];det=M[0][0]*M[1][1]-M[0][1]**2
    ck(det>0 and M[0][0]>0)
    inv=[[M[1][1]/det,-M[0][1]/det],[-M[1][0]/det,M[0][0]/det]]
    for i in range(2):
        for j in range(2):ck(sum(M[i][k]*inv[k][j] for k in range(2))==int(i==j))
    z=[F(rng.randrange(-5,6),7),F(rng.randrange(-5,6),9)]
    U=z[0]**4+z[1]**4+20*z[0]**2*z[1]**2
    grad=[4*z[0]**3+40*z[0]*z[1]**2,4*z[1]**3+40*z[1]*z[0]**2]
    iz=[sum(inv[i][j]*z[j] for j in range(2)) for i in range(2)]
    mg=[sum(M[i][j]*grad[j] for j in range(2)) for i in range(2)]
    ck(sum(iz[i]*mg[i] for i in range(2))==4*U)
    ck(sum(M[i][j]*inv[j][i] for i in range(2) for j in range(2))==2)
    y=F(rng.randrange(-20,21),10);k=F(7,3);v=1+k*(1-y*y)**2;vp=-4*k*y*(1-y*y);K=1+k/4
    ck(y*vp+4*K*v>=4)
eps=F(1,100);D=[[F(1),F(1)],[F(1),1+eps]];g=[1,-1]
ck(D[0][0]*D[1][1]-D[0][1]**2==eps)
ck(sum(g[i]*D[i][j]*g[j] for i in range(2) for j in range(2))==eps<1)

raw=f.base.fixture(3);cert=f.certify(raw,full_ratio=F(2));ck(f.verify(raw,cert,full_ratio=F(2))['status']=='PASS')
for val in [None,True,'single_unknown_M','all_SPD_including_cross_mobility','variable_SPD']:
    no(lambda val=val:f.certify(raw,family=val))
no(lambda:f.certify(raw,M=[[1,0],[0,1]]))
# Corrupt every model-family statement separately; no implicit contract widening.
for key in cert['kinetic_family']:
    bad=copy.deepcopy(cert);bad['kinetic_family'][key]='unverified alternative';no(lambda bad=bad:f.verify(raw,bad,full_ratio=F(2)))
for key in cert['exact_attainable_set']:
    bad=copy.deepcopy(cert);bad['exact_attainable_set'][key]='wrong';no(lambda bad=bad:f.verify(raw,bad,full_ratio=F(2)))
for path,val in [(('kinetic_family','matrix_entries_required'),0),(('exact_attainable_set','endpoints_attained'),0),
                 (('range_proof_sha256',),'wrong'),(('finite_source_sha256',),'wrong'),
                 (('observable',),'MFPT'),(('numerical_scope',),'exact actual rate'),
                 (('uniform_rate_enclosure','lower'),'0'),(('uniform_rate_enclosure','upper'),'1')]:
    bad=copy.deepcopy(cert);d=bad
    for key in path[:-1]:d=d[key]
    d[path[-1]]=val;no(lambda bad=bad:f.verify(raw,bad,full_ratio=F(2)))
# Changing a returned descriptor must not mutate future expected proof data.
bad=f.certify(raw);bad['kinetic_family']['excluded'].clear()
ck(len(f.certify(raw)['kinetic_family']['excluded'])==6);no(lambda:f.verify(raw,bad))
no(lambda:f.verify(raw,f.engine.certify(raw)))
no(lambda:f.engine.verify(raw,cert,full_ratio=F(2)))
no(lambda:f.verify(raw,cert,full_ratio=F(3)))
no(lambda:f.verify(f.base.fixture(3,coupling=F(21)),cert,full_ratio=F(2)))
bad=copy.deepcopy(cert);bad['uniform_rate_enclosure']['lower_display']=float('nan');ck(f.verify(raw,bad,full_ratio=F(2))['status']=='PASS')
# The 513D family claim gets an ACTUAL full recomputation, not a scope label
# merely affixed to an old saved numerical artifact.
large=json.loads(Path('family_513D_certificate.json').read_text())
receipt=f.verify(f.base.fixture(512),large,full_ratio=F(101,100),quad_relative=F(1,1000))
ck(receipt['status']=='PASS');ck(F(large['full_ratio_exact'])<F(101,100))
ck(large['exact_attainable_set']['lower_endpoint_numerically_evaluated']is False)
out={'status':'PASS','author_assertions':count,'family_513D_receipt':receipt,
     'scope':'new model-family receiving and finite algebra checks; exact range proof remains a separate mathematical review'}
Path('check_results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'status':'PASS','author_assertions':count},indent=2))
