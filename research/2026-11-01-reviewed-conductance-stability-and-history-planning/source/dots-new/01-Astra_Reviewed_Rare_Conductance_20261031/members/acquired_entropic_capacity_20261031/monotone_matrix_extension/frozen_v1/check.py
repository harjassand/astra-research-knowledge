from fractions import Fraction as F
from copy import deepcopy
from itertools import combinations
from random import Random
from pathlib import Path
import json
import sympy as sp
from compile import acquire,certify,verify,fixture,psd,norm_upper,encode_terms,aligned_terms,new_integrator,Unknown

count=0
def ok(x):
    global count
    count+=1;assert x
def rejects(f):
    global count
    count+=1
    try:f()
    except Unknown:return
    raise AssertionError("admitted corruption")

rng=Random(861031)
for _ in range(300):
    A=sp.zeros(3)
    for i in range(3):
        for j in range(i,3):A[i,j]=A[j,i]=sp.Rational(rng.randrange(-3,4),rng.randrange(1,5))
    allmin=True
    for r in range(1,4):
        for inds in combinations(range(3),r):allmin &= A.extract(inds,inds).det()>=0
    ok(psd(A)==allmin)
ok(psd(sp.zeros(3)))
ok(not psd(sp.zeros(3),True))
ok(not psd(sp.Matrix([[0,1],[1,0]])))

raw=fixture(2);acq=acquire(raw);cert=certify(raw)
ok(acq["m"]==2 and acq["determinant_degree"]==4)
ok(acq["tail_exponent_physical_m"]==2)
ok(F(acq["commutator_squared_frobenius"])>0)
ok(cert["factor"]=="7")
ok(verify(raw,cert)["status"]=="PASS")
H1=sp.Matrix(acq["H1"]);H2=sp.Matrix(acq["H2"])
H1=H1.applyfunc(sp.Rational);H2=H2.applyfunc(sp.Rational)
for j in range(51):
    y=sp.Rational(j,100);v=(1-y*y)**2;vp=-4*y*(1-y*y)
    A=sp.eye(3)+v*H1+v*v*H2;Ap=vp*(H1+2*v*H2);Ai=A.inv()
    S=sp.Matrix((sp.kronecker_product(A,sp.eye(3))+sp.kronecker_product(sp.eye(3),A)).inv()*(-Ap).reshape(9,1)).reshape(3,3)
    ok(S==S.T and A*S+S*A==-Ap)
    C=Ai;Cp=-Ai*Ap*Ai
    ok(S*C+C*S==Cp)
    K=sp.trace(S*C*S);bb=sp.trace(Ai*Ap*Ai*Ap)
    ok(K<=bb/4)
    ok(K<=-12*y*sp.trace(Ai*Ap)/4)
    ok(psd(-Ap))
    if j not in [0,50]:ok(H1*H2-H2*H1!=sp.zeros(3))

# Rank-deficient H2: determinant degree3 is not physical dimension2.
H2r=sp.diag(0,sp.Rational(1,2),0)
rankraw=encode_terms(3,aligned_terms(H1,H2r));ra=acquire(rankraw)
ok(ra["m"]==2 and ra["determinant_degree"]==3)
ri=new_integrator(ra,192,10000,200000)
ok(ri.m==2 and ri.leading==F(ra["tail_det_H1"]))
rc=certify(rankraw);ok(verify(rankraw,rc)["status"]=="PASS")

# Rational projector with irrational unit direction and noncommuting matrices.
xs=sp.symbols("r0:3");x=sp.Matrix(xs);u=sp.Matrix([1,1,0]);Pi=u*u.T/2;P=sp.eye(3)-Pi
w=sp.Matrix([1,-1,0]);e=sp.Matrix([0,0,1])
J1=P+(w*e.T+e*w.T)/4;J2=e*e.T/2;s=(x.T*Pi*x)[0]
expr=sp.expand(((x.T*P*x)[0]+(1-s)**2*(x.T*J1*x)[0]+(1-s)**4*(x.T*J2*x)[0])/2)
irr=encode_terms(3,dict(sp.Poly(expr,*xs).terms()));ic=certify(irr)
ok(ic["acquisition"]["direction_norm_squared"]=="2")
ok(F(ic["acquisition"]["commutator_squared_frobenius"])>0)
ok(verify(irr,ic)["status"]=="PASS")
Path("rank_and_irrational_fixtures.json").write_text(json.dumps({"rank_deficient":{"raw":rankraw,"certificate":rc},"irrational":{"raw":irr,"certificate":ic}},indent=2))

for bad in [True,3.,"3"]:
    r=deepcopy(raw);r["n"]=bad;rejects(lambda r=r:acquire(r))
r=deepcopy(raw);r["terms"].append(deepcopy(r["terms"][0]));rejects(lambda:acquire(r))
for c in [True,0,"0","2/2","nan","1/0"]:
    r=deepcopy(raw);r["terms"][0]["coefficient"]=c;rejects(lambda r=r:acquire(r))
for degree in [1,3,5,7,9]:
    r=deepcopy(raw);r["terms"].append({"powers":[degree,0,0],"coefficient":"1"});rejects(lambda r=r:acquire(r))
for field,value in [("beta","2"),("b","1/3"),("observable","first passage"),("factor","1"),("N",True),("T","3"),("precision_bits",0)]:
    c=deepcopy(cert);c[field]=value;rejects(lambda c=c:verify(raw,c))
c=deepcopy(cert);c["acquisition"]["m"]=4;rejects(lambda:verify(raw,c))
c=deepcopy(cert);c["acquisition"]["tail_det_H1"]="1";rejects(lambda:verify(raw,c))
c=deepcopy(cert);c["full_rate"]["lower"]="1";rejects(lambda:verify(raw,c))
for key in ["max_grid","max_points","max_cutoff","max_precision","max_product_bits"]:
    for val in [True,0,float("nan"),1.5]:rejects(lambda key=key,val=val:certify(raw,**{key:val}))
for val in [True,float("nan"),float("inf"),1.01,F(0)]:rejects(lambda val=val:certify(raw,quad_relative=val))
for kw in [{"max_grid":1},{"max_points":16},{"max_cutoff":2},{"max_precision":8},{"max_product_bits":8}]:rejects(lambda kw=kw:certify(raw,**kw))

receipts=[]
for out in json.loads(Path("results.json").read_text()):
    r=verify(fixture(out["acquisition"]["m"]),out);ok(r["status"]=="PASS");receipts.append(r)
rot=json.loads(Path("rotated_fixture.json").read_text());r=verify(rot["raw"],rot["certificate"]);ok(r["status"]=="PASS");receipts.append(r)
Path("check_results.json").write_text(json.dumps({"status":"PASS","author_assertions":count,"receipts":receipts},indent=2))
print(json.dumps({"status":"PASS","author_assertions":count,"receipts":receipts},indent=2))
