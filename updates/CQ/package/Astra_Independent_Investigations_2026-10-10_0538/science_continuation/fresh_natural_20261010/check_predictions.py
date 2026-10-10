"""Deterministic tests of conditional tensor algebra and extraction sensitivity.

These are mathematics/figure-digitation tests, not experiments or confidence limits.
"""
import csv,json,math
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
rows=list(csv.DictReader((P/'figure2_vector_observations.csv').open()))
stats=json.loads((P/'observed_statistics.json').read_text())

def mul(x,y):
    z=[a*b for a in x for b in y];return min(z),max(z)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def sub(x,y):return x[0]-y[1],x[1]-y[0]
def divide(x,y):
    assert not y[0]<=0<=y[1]
    return mul(x,(1/y[1],1/y[0]))
def slope_interval(rr, db=0.1, dt=0.01):
    num=(0.,0.);den=(0.,0.)
    for r in rr:
        b=float(r['B_T']);t=float(r['theta_per_mille'])
        bi=(b-db,b+db);ti=(t-dt,t+dt)
        num=add(num,mul(bi,ti))
        sq=(0. if bi[0]<=0<=bi[1] else min(x*x for x in bi),max(x*x for x in bi))
        den=add(den,sq)
    return divide(num,den)
out={'digitization_sensitivity_assumptions':{
    'B_each_point_absolute_bound_T':0.1,'theta_each_point_absolute_bound_per_mille':0.01,
    'meaning':'adversarial numerical perturbations of extracted figure points; NOT experimental errors or confidence intervals'}}
ints={}
for s in sorted({r['series'] for r in rows}):
    ints[s]=slope_interval([r for r in rows if r['series']==s])
out['slope_intervals_per_mille_T']=ints
bs=ints['sample3_short_T2_T3'];rs=ints['sample3_short_T1_T4']
bl=ints['sample3_long_T2_T3'];rl=ints['sample3_long_T1_T4']
out['common_factor_null_determinant_interval']=sub(mul(bl,rs),mul(rl,bs))
out['relative_contact_gain_change_needed_interval']=divide(divide(rl,rs),divide(bl,bs))
assert out['common_factor_null_determinant_interval'][1]<0

# Three crystallographic variants. Q=diag(populations).
def K(a,c,p):return a*np.eye(3)+(c-a)*np.diag(p)
u=np.ones(3)/math.sqrt(3)
for a,c in [(1.,2.),(1.,-2.),(-3.,-.01),(.1,10.)]:
    for p in [(1,0,0),(0,0,1),(.2,.3,.5),(1/3,1/3,1/3)]:
        m=K(a,c,p)
        assert np.isclose(np.trace(m),2*a+c)
        assert np.isclose(u@m@u,(2*a+c)/3)
        eig=np.linalg.eigvalsh(m)
        assert min(a,c)-1e-14<=eig.min()<=eig.max()<=max(a,c)+1e-14
assert np.allclose(K(1,-2,(1/3,)*3),0)
for a,c in [(1,2),(.0001,2),(3,.0001)]:
    assert (2*a+c)/3>=max(a,c)/3-1e-14
out['conditional_tensor_tests']='PASS'
out['experimental_uncertainty']='Not supplied by the vector symbols; geometry/contact changes and local fields remain unresolved.'
(P/'sensitivity_and_theory_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
