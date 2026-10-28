#!/usr/bin/env python3
"""Exact small-class modulus certificates. Not generic QE or source acquisition."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
from math import comb
import hashlib,json
import sympy as sp
root=Path(__file__).resolve().parent
# FULL d=1, one action, two outcomes: rho=1, J=(p,1-p).
# L=1. Midpoint gives exact physical pair-distance² g=(p-q)²,
# F=2(p-q)²; n=1,C=1 valid globally, including endpoints.
p,q=sp.symbols('p q',real=True);mid=(p+q)/2
physical_sq=2*(p-mid)**2+2*(q-mid)**2
assert sp.expand(physical_sq-(p-q)**2)==0
full_checks=0;max_tv=Q(0)
for pp,qq in product([Q(i,20) for i in range(21)],repeat=2):
    F=2*(pp-qq)**2;g=(pp-qq)**2
    assert g<=F
    for H in range(1,8):
        TV=sum(Q(comb(H,k))*abs(pp**k*(1-pp)**(H-k)-qq**k*(1-qq)**(H-k)) for k in range(H+1))/2
        assert TV<=H*abs(pp-qq)
        assert TV**2 <= (1+2*H)**2 * F
        full_checks+=1;max_tv=max(max_tv,TV)
# Restricted physical d=3 reset-to-sink family:
# rho(a)=diag(a,1-a,0); E_1=b|A><A|, E_0=I-E_1;
# Phi_o(X)=Tr(E_o X)|sink><sink|. Only first output can be1.
# Native short-vector F=2L(ab-a'b')² for every L>=1.
# Parameter Frobenius metric is 2(da²+db²) for each model.
a,b,c,d,e=sp.symbols('a b c d e',real=True)
# Exact restricted relation-distance lower certificate on the singular ray.
# On ab=cd: Euclidean_sq - e² = (a+b-e)²+(c-d)².
D=(a-e)**2+(b-e)**2+c*c+d*d
assert sp.expand(D-e*e-((a+b-e)**2+(c-d)**2)+2*(a*b-c*d))==0
# Certificate upper repair: reduce one coordinate of the larger product.
L=17;restricted_checks=0;nonzero_repairs=0;clock_checks=0
for aa,bb,cc,dd in product([Q(i,4) for i in range(5)],repeat=4):
    A,B,C,D=aa,bb,cc,dd
    Delta=aa*bb-cc*dd
    if Delta>0:
        if aa>=bb: B=cc*dd/aa
        else: A=cc*dd/bb
    elif Delta<0:
        if cc>=dd: D=aa*bb/cc
        else: C=aa*bb/dd
    assert all(0<=v<=1 for v in [A,B,C,D]) and A*B==C*D
    dist_sq=2*((aa-A)**2+(bb-B)**2+(cc-C)**2+(dd-D)**2)
    assert dist_sq<=2*abs(Delta)
    F=2*L*Delta**2
    assert dist_sq**2<=2*F # global n=2,C=2 on this RESTRICTED family
    if Delta:nonzero_repairs+=1
    for H in [1,2,7,50]:
        TV=abs(Delta);M=3*(1+2*H)
        assert TV**4<=M**4*2*F
    gamma=Q(3,4);delta=1-gamma;Mclock=3*(1+2*gamma/delta)
    TVclock=gamma*abs(Delta)
    assert TVclock**4<=Mclock**4*2*F
    restricted_checks+=1;clock_checks+=1
# Sharp failure of exponent1 for distance to the RESTRICTED relation only.
# The full unconstrained d=3 physical relation can contain additional repairs.
ray=[]
for k in range(1,8):
    eps=Q(1,2**k);g=2*eps**2;F=2*L*eps**4
    ray.append({'epsilon':str(eps),'restricted_distance_squared':str(g),'F':str(F),'g_over_F':str(g/F)})
# An observationally equivalent pair need not be the same physical model.
# (a,b)=(1,0), (a',b')=(0,1) both emit all zeros, but physical pairwise
# model-distance squared is 2[(1-0)²+(0-1)²]=4.
assert Q(1)*Q(0)==Q(0)*Q(1)
report={
 'status':'PASS: exact small-class evidence; not a generic modulus computation or independent receipt',
 'source_calls':0,'episode_starts':0,'rng_calls':0,'generic_QE_executed':False,
 'source_sha256':hashlib.sha256((root/'SHORT_WORD_SEMIALGEBRAIC_PHYSICAL_PREDICTION.md').read_bytes()).hexdigest(),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'full_d1_binary_class':{'L':1,'n':1,'C':1,'exact_relation_distance_squared':'(p-q)^2','F':'2(p-q)^2','finite_horizon_exact_checks':full_checks},
 'restricted_d3_one_shot_family':{'L':L,'n':2,'C':2,'exact_physical_repair_checks':restricted_checks,'nonzero_repairs':nonzero_repairs,'clocked_checks':clock_checks,'rank_drop':'observable rank2 when ab>0, rank1 at ab=0','all_native_Chois_on_boundary':True,'restricted_singular_ray':ray,'warning':'Exponent1 failure applies only to this constrained family metric; no lower bound for the full d=3 HQMM relation is asserted'},
 'equivalence_relation_not_diagonal':{'pair':[[1,0],[0,1]],'all_observed_word_laws_equal':True,'physical_model_distance_squared':4,'distance_of_pair_to_equivalence_relation':0}
}
(root/'short_word_modulus_exact_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['source_sha256','script_sha256','restricted_d3_one_shot_family']},indent=2))
print('restricted repairs',restricted_checks,'clock checks',clock_checks)
