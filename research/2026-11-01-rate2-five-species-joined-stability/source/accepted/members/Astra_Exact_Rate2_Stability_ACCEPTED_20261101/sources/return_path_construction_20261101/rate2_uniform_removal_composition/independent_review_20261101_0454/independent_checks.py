#!/usr/bin/env python3
"""Independent exact support; infinite-state claims are proved in the review."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib,json,itertools
import sympy as sp
P=Path(__file__).resolve().parent
ROOT=P.parents[2]
u,w=sp.symbols('u w',nonnegative=True)
u0=10**20
checks={}
certs={}
def ck(name,value):
    checks[name]=bool(value)
    assert value,name
def positive_after_u0(name,poly):
    pp=sp.Poly(sp.expand(poly.subs(u,u0+w)),w)
    co=pp.all_coeffs()
    ck(name,all(t>=0 for t in co) and pp.eval(0)>0)
    certs[name]=[str(z) for z in co]
positive_after_u0('floor_m_lower',u/sp.Integer(40000)-1)
positive_after_u0('parameter_N_ge_1e8_mplus1_squared',u*u-10**8*(u/sp.Integer(20000)+1)**2)
positive_after_u0('core_B_ge_Nhalf',u*u/4-sp.Rational(49,20000)*u-48)
positive_after_u0('k_ge_8_from_floor_bound',u/sp.Integer(160000)-8)
positive_after_u0('k_le_deltaN',u*u/sp.Integer(10**12)-u/sp.Integer(40000))
positive_after_u0('clock_budget',1+10**8*u-(sp.Rational(8,20000)*u+10**12+40960000*u+6))
positive_after_u0('whole_block_immigration_mean_cap',u*u/256-1-10**8*u)
positive_after_u0('linear_macro_resource_error_dominates_target',u*u/100000-u/10**6)
positive_after_u0('linear_immigration_error_dominates_target',u*u/256-u/10**6)
ck('activated_R_entry_margin',(Q(3,4)-Q(1,10**12))/101>=Q(4,1000))
ck('chernoff_immigration_exponent',Q(1,256)-Q(1,64)*Q(2,3)<=-Q(1,256))
ck('final_lower_hit_mass',Q(3,4)+Q(1,64)==Q(49,64)<Q(15,16))
ck('final_interior_service_mass',Q(7,8)*Q(65,64)+Q(1,64)==Q(463,512)<Q(15,16))
ck('mesoscopic_failure_exponents',Q(1,480000)>Q(1,10**6) and Q(1,160000)>Q(1,10**6))
ck('failure_prefactor_sum',Q(101,100)+1+1+8+1+10+1+1<32)
ck('consumer_theta_exact_margin',4*100000001*Q(1,10**16)<Q(1,10**6))
ck('consumer_exponential_linearization_range',2*Q(1,10**16)<=1)
# Reconstruct every actual source/vector, with coefficient two only on CD->AE.
C={'0':(0,0,0,0,0),'A':(1,0,0,0,0),'AA':(2,0,0,0,0),
   'AB':(1,1,0,0,0),'AC':(1,0,1,0,0),'AD':(1,0,0,1,0),
   'AE':(1,0,0,0,1),'CD':(0,0,1,1,0)}
rs=[('0','A',1),('A','0',1),('AA','AC',1),('AC','AA',1),
    ('AA','AD',1),('AD','AA',1),('AA','AE',1),('AE','AA',1),
    ('AE','CD',1),('CD','AE',2),('CD','AB',1),('AB','CD',1)]
reactions={(a,b):(C[a],C[b],k) for a,b,k in rs}
def apply(x,a,b):
    src,dst,k=reactions[a,b]
    assert all(z>=y for z,y in zip(x,src)),(x,a,b)
    return tuple(z-y+t for z,y,t in zip(x,src,dst))
def propensity(x,source,k):
    value=k
    for z,y in zip(x,source):
        for j in range(y): value*=z-j
    return value

def G(x,N):
    a,b,c,d,e=x;M=a+min(c,d);R=c+d+e
    phi=min(Q(1),max(Q(0),Q(96)-Q(R,M+1))/48)
    return Q(1,2**M)*(1+Q(16,N)*phi*a*a)
def driftG(x,N):
    gx=G(x,N);v=Q(0)
    for src,dst,k in reactions.values():
        rate=propensity(x,src,k)
        if rate:
            y=tuple(z-a+b for z,a,b in zip(x,src,dst))
            v+=rate*(G(y,N)-gx)
    return v
N=10**40;m=10**20//20000
states=set()
for a,l,gap in itertools.product(range(4),range(4),(0,1,9)):
    c,d=l,l+gap;M=a+l
    for R in (c+d,48*(M+1),48*(M+1)+1,96*(M+1)-1,96*(M+1),96*(M+1)+1,98*(M+1),N):
        if R<c+d: continue
        for b in (0,N//4,N//2,N):
            x=(a,b,c,d,R-c-d)
            if sum(x)>3*N//4:states.add(x)
    states.add((a,0,l,N,0));states.add((a,0,N,l,0))
for x in states:
    assert x[0]+min(x[2],x[3])<m and sum(x)>3*N//4
    assert driftG(x,N)<=-G(x,N)/4,x
ck('sampled_exact_global_seed_extension',True)
# Constructive communication: these loops are exact tests of the general paths
# proved in CONSUMER_APPLICATION.md, not a finite-state proof of irreducibility.
path_moves=0
for target in itertools.product(range(5),repeat=5):
    if sum(target)>4:continue
    x=target
    if x[0]==0 and sum(x)>0:x=apply(x,'0','A');path_moves+=1
    for idx,label in ((2,'AC'),(3,'AD'),(4,'AE')):
        while x[idx]:x=apply(x,label,'AA');path_moves+=1
    while x[1]:
        for a,b in (('AB','CD'),('CD','AE'),('AE','AA')):
            x=apply(x,a,b);path_moves+=1
    while x[0]:x=apply(x,'A','0');path_moves+=1
    assert x==(0,0,0,0,0)
    x=(0,0,0,0,0)
    for j in range(sum(target)+1):x=apply(x,'0','A');path_moves+=1
    for idx,label in ((2,'AC'),(3,'AD'),(4,'AE')):
        for j in range(target[idx]):x=apply(x,'AA',label);path_moves+=1
    for j in range(target[1]):
        for a,b in (('AA','AE'),('AE','CD'),('CD','AB')):
            x=apply(x,a,b);path_moves+=1
    x=apply(x,'A','0');path_moves+=1
    assert x==target
ck('constructive_irreducibility_paths_on_finite_fixtures',True)
files={
 'composition':('return_path_construction_20261101/rate2_uniform_removal_composition/UNIFORM_ACTUAL_REMOVAL_BLOCK.md','a0e09b39c50c28365a1ed5a0fe04c71b003b9c5556ffe9b94202441f9ee4cb21'),
 'growth':('return_path_construction_20261101/rate2_uniform_initial_growth/UNIFORM_FULL_GENERATOR_INITIAL_GROWTH.md','90a80f12bfc045350b5254a4c8d731f506da5520ee161ccd9e7cbb11df82329e'),
 'growth_receipt':('return_path_construction_20261101/rate2_uniform_initial_growth/audit_uniform_growth_20261101_0435/SOURCE_BOUND_ACCEPTANCE.md','a1eb22f7376fb8cfd138908629f7242edc164dc721476be0999dde4716de67e8'),
 'activation':('return_path_construction_20261101/rate2_uniform_activation/UNIFORM_ACTIVATION_OR_REMOVAL.md','c1d2ed0820d4f92ea236dcb27eab1cd29e27665f9b1a2e826617cc34e3c3fda8'),
 'activation_receipt':('return_path_construction_20261101/rate2_uniform_activation/audit_uniform_activation_20261101_0444/SOURCE_BOUND_ACCEPTANCE.md','1d26eae541ea6784b9f41965a19c27244fc39147f0872cfc1243ba869f0bb8e1'),
 'macro':('return_path_construction_20261101/rate2_activated_macro_interface/ACTIVATED_TO_MACRO_AND_POSITIVE_FRACTIONS.md','e527fafdfe790fa753b4584fca338bf9e4aa37179643a1f1596e39b140cb99a0'),
 'macro_receipt':('return_path_construction_20261101/rate2_activated_macro_interface/audit_activated_macro_20261101_0450/SOURCE_BOUND_REVIEW.md','bf220ba3d2b5ec36687dae26ecf4f7fbb207664b5e784a4fa4f7f1995bea7ae7'),
 'macro_receiving_addendum':('return_path_construction_20261101/rate2_activated_macro_interface/receiving_qualifications_20261101/EXACT_RECEIVING_ADDENDUM.md','4f98b41a63e4a80a9d07353605b8579e02532ccd2406c35e4286c14ff5703635'),
 'interior':('return_path_construction_20261101/rate2_paid_interior_removal/PAID_INTERIOR_REMOVAL.md','a8e0bd383b053021f72e8197986581c87878046cdeaa7570536e44f5cf71a1cf'),
 'interior_receipt':('return_path_construction_20261101/rate2_paid_interior_removal_independent_review_20261101/INDEPENDENT_REVIEW.md','25513463673a7b7146fe8e573c3937bdc9612ee7d55620d280404a91c5d8f24a'),
 'consumer':('sampled_return_consumer_root_20261101/PAID_ACTIVATION_TO_STATIONARY_MOMENT.md','a4d41076e1c5cfaa9448d276a71fe0e3055de89560405334760598c83ce0dff4'),
}
for key,(path,h) in files.items():ck('hash_'+key,hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h)
report={'status':'PASS','assertions':len(checks),'checks':checks,
 'translated_polynomial_nonnegative_coefficients':certs,
 'global_seed_exact_fixture_states':len(states),'constructive_path_fixture_moves':path_moves,
 'dependencies':{k:{'path':p,'sha256':h} for k,(p,h) in files.items()},
 'scope':'Exact/rational supporting checks only. Ordinary infinite-state proof and receipt consumption are in the accompanying audit.'}
(P/'EXACT_CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('status','assertions','global_seed_exact_fixture_states','constructive_path_fixture_moves')},indent=2))
