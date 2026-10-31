from fractions import Fraction as F
from copy import deepcopy
from random import Random
import json
import sympy as sp
from capacity import acquire, certify, sparse_fixture, dense_fixture, sqrt_bounds, Unknown
from verify import receiving_verify

checks=0
def ok(x):
    global checks
    checks+=1
    assert x

def rejects(fun):
    global checks
    checks+=1
    try:
        fun()
    except (Unknown, ValueError, TypeError, KeyError):
        return
    raise AssertionError("admitted deliberate corruption")

rng=Random(761031)
for _ in range(1200):
    a=F(rng.getrandbits(rng.randrange(1,180)),1+rng.getrandbits(rng.randrange(1,180)))
    p=rng.randrange(0,160)
    lo,hi=sqrt_bounds(a,p)
    ok(F(lo*lo,1<<(2*p))<=a<=F(hi*hi,1<<(2*p)))
    ok(hi-lo<=1)
for p in [0,1,8,128]:
    for k in range(8):
        a=F(k*k,1<<(2*p))
        ok(sqrt_bounds(a,p)==(k,k))

# Exact Gaussian continuity identity, not a sampled density check.
y,z1,z2,beta=sp.symbols("y z1 z2 beta", positive=True)
zs=sp.Matrix([z1,z2]); ks=[sp.Rational(1,2),sp.Rational(3,2)]
v=(1-y*y)**2
aa=[1+k*v for k in ks]
vel=sp.Matrix([-sp.diff(a,y)*z/(2*a) for a,z in zip(aa,zs)])
rho_y=sum(sp.diff(a,y)/(2*a)-beta*sp.diff(a,y)*z*z/2 for a,z in zip(aa,zs))
div=sum(sp.diff(vel[i],zs[i])-beta*aa[i]*zs[i]*vel[i] for i in range(2))
ok(sp.simplify(rho_y+div)==0)
K=sum(sp.diff(a,y)**2/(4*beta*a**3) for a in aa)
ok(sp.simplify(K-4*y*y*v/beta*sum(k*k/(1+k*v)**3 for k in ks))==0)

# Pointwise step in the all-dimension integration-by-parts bound.
for _ in range(500):
    yy=F(rng.randrange(0,1001),2000)
    vv=(1-yy*yy)**2
    kappas=[F(rng.randrange(1,10000),rng.randrange(1,1000)) for _ in range(rng.randrange(2,12))]
    s1=sum(k/(1+k*vv) for k in kappas)
    s2=sum(k*k/(1+k*vv)**3 for k in kappas)
    cc=F(4,9)
    ok(s2<=cc*s1)
    kval=4*yy*yy*vv*s2
    minus_logder=2*yy*(1-yy*yy)*s1
    ok(kval<=2*cc*yy*(1-yy*yy)*minus_logder)

base=sparse_fixture(2)
acq=acquire(base); cert=certify(acq)
ok(receiving_verify(base,cert)["status"]=="PASS")
for bad in [True,3.0,"3"]:
    rr=deepcopy(base); rr["n"]=bad
    rejects(lambda rr=rr:acquire(rr))
rr=deepcopy(base); rr["terms"].append(deepcopy(rr["terms"][0])); rejects(lambda:acquire(rr))
rr=deepcopy(base); rr["terms"][0]["coefficient"]="2/2"; rejects(lambda:acquire(rr))
rr=deepcopy(base); rr["terms"][0]["coefficient"]=True; rejects(lambda:acquire(rr))
rr=deepcopy(base); rr["terms"][0]["powers"][0]=False; rejects(lambda:acquire(rr))
rr=deepcopy(base); rr["terms"][0]["coefficient"]="19/13"; rejects(lambda:acquire(rr))
rr=deepcopy(base); rr["terms"].append({"powers":[6,0,0],"coefficient":"1"}); rejects(lambda:acquire(rr))
for field,value in [("m",True),("n",9),("ell",["0","1","0"]),("beta","2"),("b","1/3"),
                    ("direction_rational",["1","1","0"]),("direction_norm_squared","2"),
                    ("observable","mean first-hit time"),("grid_N",True),("grid_N",63),
                    ("precision_bits",0),("cutoff_T","3"),("universal_factor","1"),("tail_upper","0")]:
    cc=deepcopy(cert); cc[field]=value
    rejects(lambda cc=cc:receiving_verify(base,cc))
for name in ["mass_A_unnormalized","resistance","free_energy_rate","full_diffusion_rate"]:
    cc=deepcopy(cert); cc[name]["lower"]="1"
    rejects(lambda cc=cc:receiving_verify(base,cc))
rejects(lambda:receiving_verify(base,cert,beta=F(2)))
rejects(lambda:receiving_verify(base,cert,max_quad_ratio=F(10000001,10000000)))

dense=dense_fixture(3)
got=acquire(dense)
ok(got["route"].startswith("exact_quadratic_nullspace"))
ok(sum(F(a)**2 for a in got["ell"])==1)
ok([F(c) for c in got["determinant_coefficients"]]==[F(1),F(3),F(11,4),F(3,4)])
dc=certify(got)
ok(receiving_verify(dense,dc)["status"]=="PASS")
for i in [0,len(dense["terms"])//2,-1]:
    rr=deepcopy(dense)
    rr["terms"][i]["coefficient"]=str(F(rr["terms"][i]["coefficient"])+F(1,1009))
    rejects(lambda rr=rr:acquire(rr))

# Rational raw model with irrational unit direction AND irrational positive
# fiber eigenvalues. No eigensystem or radical arithmetic is used to integrate.
xs=sp.symbols("r0:3"); x=sp.Matrix(xs)
vv=sp.Matrix([1,1,0]); Pi=vv*vv.T/2; P=sp.eye(3)-Pi
ww=sp.Matrix([1,-1,0]); ee=sp.Matrix([0,0,1])
H=P+(ww*ee.T+ee*ww.T)/4
expr=sp.expand(((x.T*P*x)[0]+(1-(x.T*Pi*x)[0])**2*(x.T*H*x)[0])/2)
from capacity import encode
irr_raw=encode(expr,xs); irr=acquire(irr_raw)
ok(irr["direction_norm_squared"]=="2")
ok(irr["determinant_coefficients"]==["1","2","7/8"])
ok(irr["kappa"] is None)
irr_cert=certify(irr)
ok(receiving_verify(irr_raw,irr_cert)["status"]=="PASS")
with open("irrational_geometry_fixture.json","w") as f:
    json.dump({"raw":irr_raw,"acquisition":irr,"certificate":irr_cert},f,indent=2)

# Re-acquire and verify every saved scaling certificate from raw coefficients.
with open("capacity_results.json") as f:
    all_results=json.load(f)
receipts=[]
for rec in all_results:
    m=rec["acquisition"]["m"]
    receipt=receiving_verify(sparse_fixture(m),rec["certificate"])
    ok(receipt["status"]=="PASS")
    receipts.append(receipt)

report={"status":"PASS","author_assertions":checks,"receiving_receipts":receipts,
        "limits":"author tests, not independent review or proof of physical model validity"}
with open("check_results.json","w") as f:
    json.dump(report,f,indent=2)
print(json.dumps(report,indent=2))
