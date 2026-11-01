#!/usr/bin/env python3
"""Exact independent join checks; does not prove the harmonic source theorem."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json
import sympy as s
P=Path(__file__).resolve().parent; ROOT=P.parents[1]
u,v,z=s.symbols('u v z', nonnegative=True)
u0=10**20;v0=10**10;h=4*10**26
checks={};polys={}
def ck(k,b):checks[k]=bool(b);assert b,k
def nonnegative_on(k,expr,var,start,strict=True):
 p=s.Poly(s.expand(expr.subs(var,start+z)),z);co=p.all_coeffs()
 ck(k,all(a>=0 for a in co) and (p.eval(0)>0 if strict else p.eval(0)>=0))
 polys[k]=[str(a) for a in co]
ck('all_start_h_exact',Q(400)/Q(1,10**12)**2==h)
ck('harmonic_m0_range',0<Q(1,10**12)<=Q(1,10**6))
nonnegative_on('all_start_N_ge_32h',u*u-32*h,u,u0)
nonnegative_on('service_fits_4million_sqrtN',4000000*u-h,u,u0,False)
nonnegative_on('prefix_plus_service_lt_44960002_sqrtN',(s.Rational(2)-s.Rational(8,20000))*u-10**12,u,u0)
nonnegative_on('full_clock_strictly_below_original',1+10**8*u-44960002*u,u,u0)
ck('log32h_below_100_using_e_gt_2',32*h<2**100)
ck('log10_below_3_by_exp_series',sum(Q(3)**k/Q(s.factorial(k)) for k in range(4))>10)
ck('logu_le_sqrtu_base_and_derivative_range',60<10**10 and u0>=4)
ck('100_plus_4sqrtu_le_5sqrtu',100<=v0)
nonnegative_on('first_error_half_exponent_reserve',v**4/s.Integer(2*10**15)-v*v/s.Integer(10**6),v,v0)
nonnegative_on('first_error_pays_log_prefactor',v**4/s.Integer(2*10**15)-5*v,v,v0)
ck('second_error_denominator_bound_requirements',10**40>=32*h and 10**40>=7)
nonnegative_on('harmonic_A_error_common_scale',100*u*u-u/s.Integer(10**6),u,u0)
nonnegative_on('harmonic_death_error_common_scale',u*u/2-u/s.Integer(10**6),u,u0)
nonnegative_on('harmonic_immigration_error_common_scale',u*u/96-u/s.Integer(10**6),u,u0)
ck('global_headroom_supplies_harmonic_entry',Q(65,64)<Q(5,4))
ck('post_service_unused_time_allowance',Q(13,16)+Q(1,64)==Q(53,64)<Q(15,16))
ck('old_lower_hit_unused_time_allowance',Q(3,4)+Q(1,64)==Q(49,64)<Q(15,16))
ck('all_start_error_prefactor',Q(101,100)+1+1+8+1+4+1==Q(1701,100)<32)
delta=Q(1,10**100);m0=delta/2;hh=Q(400)/m0**2
ck('induction_h_exact',hh==1600/delta**2)
ck('induction_size_exact',32*hh==51200/delta**2)
ck('induction_m0_range',0<m0<=Q(1,10**6))
ck('new_induction_size_implies_old_base',32*hh>=10**200)
ck('new_induction_size_implies_deltaN_ge4',delta*(32*hh)>=4)
ck('imbalance_M_lower_at_deltaN4',Q(31,32)*4-Q(1,2)>=Q(1,2)*4)
ck('induction_band_in_harmonic_entry',Q(1)-delta>Q(3,4) and Q(1)+delta<Q(5,4))
ck('induction_persistence_exponent_exact',m0/1000==delta/2000)
ck('clearance_endpoint_stronger_than_target',Q(13,16)<Q(15,16))
ck('induction_dyadic_time_below_T',32**2<(10**40)**3)
ck('finite_level_plus_dyadic_below_4T',Q(2)+Q(1,4)+Q(32,10**60)<4)
files={
 'induction_replacement':('return_path_construction_20261101/rate2_induction_clock_20261101/EXPLICIT_CLEARANCE_RECEIVER_ADDENDUM.md','9465869ac18d64f86642fca0e8033c0fee4c9820c035634504c7b9fc3e084805'),
 'all_start_replacement':('return_path_construction_20261101/rate2_uniform_removal_composition/explicit_harmonic_receiver/EXPLICIT_THRESHOLD_REPLACEMENT.md','b8e1e9f1061bacca3dd1bded7b754944452477a71696eb2f36412f9e2035ee81'),
 'harmonic_source':('return_path_construction_20261101/rate2_explicit_macro_removal/EXPLICIT_HARMONIC_PERSISTENCE_AND_REMOVAL.md','4d1ad7a929f7e3c6d81d06222bd8217eb96e06eb183e6f0cfe3f5dbca6ca16ca'),
 'old_all_start':('return_path_construction_20261101/rate2_uniform_removal_composition/UNIFORM_ACTUAL_REMOVAL_BLOCK.md','a0e09b39c50c28365a1ed5a0fe04c71b003b9c5556ffe9b94202441f9ee4cb21'),
 'old_clearance':('return_path_construction_20261101/rate2_induction_clock_20261101/ACTUAL_CLEARANCE_WINDOW_AND_OCCUPATION.md','0eeb311064eaaad654d69ada711e22d26b4e8622b38d15e3a3998bcfbae1bd4d'),
 'finite_level':('return_path_construction_20261101/rate2_induction_clock_20261101/FINITE_LEVEL_CORRECTED_CLOCK.md','e0700bad37717a38976f295049a8d2cb1120aeb155c343783780d6b201f20c9d'),
}
for key,(path,hsh) in files.items():ck('hash_'+key,hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==hsh)
report={'status':'PASS_JOIN_ARITHMETIC_NOT_HARMONIC_SOURCE_REVIEW','exact_checks':len(checks),'checks':checks,
 'translated_polynomial_certificates':polys,
 'source_bindings':{k:{'path':p,'sha256':h} for k,(p,h) in files.items()},
 'scope':'Join identities and literal range inequalities only; harmonic theorem acceptance is a separate prerequisite.'}
(P/'EXACT_JOIN_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'exact_checks':len(checks)},indent=2))
