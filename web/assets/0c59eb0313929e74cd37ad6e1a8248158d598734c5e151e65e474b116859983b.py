"""Exact rational checks for C07_S02's optimal endpoint analytic N>=200 tail.

No libm, float sign, or finite matrix diagnostic proves an infinite quantifier.
The saved mathematical reconstruction supplies that proof; this checks its
load-bearing endpoint arithmetic and records immutable source hashes.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib,json,time

started=time.perf_counter();checks={}
def test(name,v):
    assert v,name
    checks[name]=True
def expsum(x,n):return sum(x**j/F(factorial(j)) for j in range(n))
def cos_sum(x,last):return sum((-1)**j*x**(2*j)/F(factorial(2*j)) for j in range(last+1))
def sin_sum(x,last):return sum((-1)**j*x**(2*j+1)/F(factorial(2*j+1)) for j in range(last+1))

dlo=F(138629,100000);dhi=F(13863,10000);dbar=F(138629437,100000000)
log2lo=2*sum(F(1,3)**(2*j+1)/F(2*j+1) for j in range(25))
log2hi=log2lo+2*F(1,3)**51/(51*(1-F(1,9)))
test('delta_lower_and_upper',dlo<2*log2lo<2*log2hi<dhi)
test('prefix_rational_delta_strictly_above_endpoint',2*log2hi<dbar)
lam=F(101,100);a=F(241,100);za=a/2
test('saddle_contraction',dhi*lam/2<F(71,100))
cos_a_upper=cos_sum(za,4);cos_a_lower=cos_sum(za,5)
test('strip_cos_squared',0<cos_a_lower<cos_a_upper and cos_a_upper**2<F(13,100))
vhi=F(25703,25000)
test('strip_logsec_endpoint',cos_a_lower*expsum(vhi,13)>1)
z=F(1,2);cos_core_lower=cos_sum(z,3);sin_core_upper=sin_sum(z,2)
test('core_tangent_endpoint',sin_core_upper/cos_core_lower<(F(11,10)*z))
test('core_logsec_endpoint',cos_core_lower*expsum(F(2,15),6)>1)
z=F(11,10);sin_outer_lower=sin_sum(z,3);cos_outer_upper=cos_sum(z,4)
test('outer_tangent_lower',sin_outer_lower/cos_outer_upper>F(49,25))
test('outer_logsec_endpoint',cos_sum(z,3)*expsum(F(121,150),5)>1)
test('pi_delta_lower',3*dlo>4)
blo=1/(4*dhi);bhi=1/(4*dlo)
test('b_lower_exact',blo==F(2500,13863))
test('b_upper181_over1000',bhi<F(181,1000))
glo=blo-2*lam/15
test('core_g_margin',glo>F(91,2000)>F(9,200))
test('core_phase_cubic',F(2,5)*F(11,10)**2/24==F(121,6000))
test('sqrt_delta_bound',dlo>F(8,7)**2)
test('sqrt_g_bound',F(9,200)>F(21,100)**2)
phase=(F(15,32)*F(121,6000)**2*F(10201,2000000)
       /(F(8,7)*F(9,200)**3*F(21,100)))
test('phase_loss_less_one_twentieth',phase<F(1,20))
test('core_tail_prefactor',4*dhi/(3*200)<1)
test('core_tail_exponent',200*blo>8)
test('exp2_lower7',expsum(F(2),6)>7)
test('outer_first_endpoint1',blo-2*lam/15>F(91,2000))
test('outer_first_endpoint11_over5',blo*F(121,25)-lam*F(121,150)>F(91,2000))
test('sqrt200_lt99_over7',200<F(99,7)**2)
test('exp3_lower20',expsum(F(3),9)>20)
test('outer_first_error',F(297,35*8800)<F(1,1000))
test('outer_second_derivative',F(22,5)*F(181,1000)-F(49,50)<-F(9,50))
test('outer_second_concavity',2*F(181,1000)-(1+F(49,25)**2)/4<0)
end_a=blo*a*a
test('outer_final_ba_squared',end_a==F(58081,55452))
fa200lo=end_a-lam*vhi
test('outer_final_barrier',fa200lo>F(9,1000))
test('N_times_final_barrier_increasing',end_a-vhi>0)
test('sqrt200_gt14',200>14**2)
test('exp_nine_fifths_lower',expsum(F(9,5),6)>F(11,2))
test('outer_second_error',F(25,693)<F(1,25))
kappalo=1-dhi*lam/2-F(13,87)
test('vertical_kappa_margin',kappalo>F(3,20))
test('vertical_delta_lambda',dhi*lam<F(141,100))
test('vertical_prefactor',F(141,100)/(3*F(8,3)*F(3,20))<F(11,10)**2)
test('vertical_loss_bound',F(11,10)*F(2,11)==F(1,5))
test('combined_density_margin',1-F(1,1000)-F(1,20)-F(1,1000)-F(1,25)-F(1,5)==F(177,250)>F(2,3))
r0=end_a-F(3,4)*dhi
test('correction_rate_positive',r0>0)
correction_exponent=-200*r0+dhi+dhi/200
test('correction_exponent_at200',correction_exponent<0)
test('correction_prefactor_at200',2304*dhi<a*a*3*200)

paths=[Path('work/cycle6/c07_s02/phase2')/f for f in
       ['OPTIMAL_ANALYTIC_TAIL.txt','QUANTITATIVE_VERTICAL_GAP.txt','CORRELATED_VERTICAL_LEMMA.txt']]
out={'status':'EXACT_OPTIMAL_ENDPOINT_ANALYTIC_CONSTANTS_PASS',
     'scope':'Analytic symmetric N>=200 tail only; finite prefix has not been assumed certified.',
     'endpoint_exact':'2 log 2','finite_prefix_admission_delta':str(dbar),
     'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
     'checks':checks,'check_count':len(checks),'phase_upper_bound':str(phase),
     'kappa_lower_bound':str(kappalo),'f_a_N200_lower_bound':str(fa200lo),
     'correction_exponent_upper_at200':str(correction_exponent),
     'log2_interval':{'lower':str(log2lo),'upper':str(log2hi)},
     'wall_seconds':time.perf_counter()-started}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='log2_interval'},indent=2))
