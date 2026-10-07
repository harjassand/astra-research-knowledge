#!/usr/bin/env python3
"""Exact rational checks supplementing, not replacing, the analytic proof."""
from pathlib import Path
from fractions import Fraction as F
import datetime,hashlib,json,math
OWN=Path(__file__).parent
checks=[]
def check(name,slack):
    slack=F(slack);assert slack>0,(name,slack)
    checks.append({'name':name,'strict_positive_slack':str(slack)})
def exp_lower(x,terms):return sum((F(x)**j/F(math.factorial(j)) for j in range(terms)),F(0))
def cos_taylor(x,last):return sum(((-1)**j*F(x)**(2*j)/F(math.factorial(2*j)) for j in range(last+1)),F(0))
def sin_taylor(x,last):return sum(((-1)**j*F(x)**(2*j+1)/F(math.factorial(2*j+1)) for j in range(last+1)),F(0))
def main():
    dl=F(138629,100000);dh=F(13863,10000);db=F(138629437,100000000)
    a=F(241,100);lam=F(101,100);U=F(25703,25000);b=F(2500,13863)
    log2_lo=2*sum((F(1,3)**(2*j+1)/F(2*j+1) for j in range(25)),F(0))
    log2_hi=log2_lo+2*F(1,3)**51/(51*(1-F(1,9)))
    check('delta_lower',2*log2_lo-dl);check('delta_upper',dh-2*log2_hi)
    check('finite_rational_upper_delta',db-2*log2_hi)
    z=a/2;cu=cos_taylor(z,4);cl=cos_taylor(z,5)
    check('cos_positive',cl);check('cos_squared_upper',F(13,100)-cu**2)
    check('logsec_a_endpoint',cl*exp_lower(U,13)-1)
    z=F(1,2);sl=sin_taylor(z,2);cl=cos_taylor(z,3)
    check('core_tan_over_z',F(11,10)*z*cl-sl)
    check('core_logsec',cl*exp_lower(F(2,15),6)-1)
    z=F(11,10);sl=sin_taylor(z,3);cu=cos_taylor(z,4)
    check('outer_tan_lower',sl-F(49,25)*cu)
    cl=cos_taylor(z,5)
    check('outer_logsec_endpoint',cl*exp_lower(F(121,150),12)-1)
    check('pi_delta_lower_from_pi3',3*dl-4)
    check('b_upper',F(181,1000)-1/(4*dl))
    g=b-2*lam/15
    check('core_g_lower',g-F(91,2000))
    check('sqrt_delta_lower',dl-F(64,49))
    check('sqrt_g_lower',F(9,200)-F(441,10000))
    phase=F(15,32)*F(121,6000)**2*F(10201,2000000)/(F(8,7)*F(9,200)**3*F(21,100))
    check('phase_loss',F(1,20)-phase)
    check('gaussian_tail_exponent8',200*b-8)
    check('exp2_above7',exp_lower(2,7)-7)
    check('gaussian_tail_exp8_above1000',F(7**4)-1000)
    check('outer_first_endpoint',b-2*lam/15-F(91,2000))
    check('outer_middle_endpoint',b*F(121,25)-lam*F(121,150)-F(91,2000))
    check('sqrt200_upper',F(99,7)**2-200)
    check('exp3_above20',exp_lower(3,9)-20)
    check('outer_middle_loss',F(1,1000)-F(297,35*8800))
    check('outer_endpoint_slope',-F(9,50)-(F(22,5)*F(181,1000)-F(49,50)))
    check('outer_slope_decreasing',(1+F(49,25)**2)/4-2*F(181,1000))
    fend=b*a*a-lam*U
    check('outer_a_rate',fend-F(9,1000))
    check('outer_a_Nrate_increases',b*a*a-U)
    check('exp1p8_above5p5',exp_lower(F(9,5),6)-F(11,2))
    check('outer_edge_loss',F(1,25)-F(25,693))
    kappa=1-dh*lam/2-F(13,87)
    check('vertical_kappa',kappa-F(3,20))
    check('vertical_delta_lambda',F(141,100)-dh*lam)
    check('vertical_prefactor_squared',F(121,100)-F(141,100)/(3*F(8,3)*F(3,20)))
    check('positive_contour_margin',F(177,250)-F(2,3))
    r=b*a*a-F(3,4)*dh
    check('completion_exponent_rate',r)
    check('completion_exponent_at200',200*r-dh-dh/200)
    check('completion_prefactor_at200',a*a*3*200-2304*dh)
    out={'status':'PASS exact rational strict inequalities','checks':checks,
         'delta_star_enclosure':[str(2*log2_lo),str(2*log2_hi)],
         'rational_prefix_delta':str(db),'scope':'Analytic constant checks only; contour, exact moment and congruence proofs remain separate.',
         'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'proof_sha256':hashlib.sha256((OWN/'OPTIMAL_ANALYTIC_TAIL.txt').read_bytes()).hexdigest()}
    path=OWN/'evidence'/'optimal_analytic_exact_checks.json'
    if path.exists():raise SystemExit('preserving existing check evidence')
    path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'checks':len(checks),'path':str(path)}))
if __name__=='__main__':main()
