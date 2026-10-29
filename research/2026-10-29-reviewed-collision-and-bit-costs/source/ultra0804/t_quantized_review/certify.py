"""Independent rational stage and finite-kernel comparator checks.

No producer module imported; no sample generation or parameter search.
"""
from fractions import Fraction as F
from pathlib import Path
import json,math,time
import sympy as s

def main():
    started=time.perf_counter()
    b=F(11,10);cap=F(161,250)
    assert b**3>F(23,20)**2
    x=cap/2
    lower=F(529,100)*(x-x*x/2)
    other=F(23,5)*(F(1,2)-cap/8)
    assert other>lower
    exp_lower=sum((lower**j)/math.factorial(j) for j in range(13))
    assert exp_lower>F(25,6)
    rho=F(6,25)
    assert 4*rho==F(24,25)<1
    assert sum((F(23,5)**j)/math.factorial(j) for j in range(8))>16
    assert F(33,5)*F(16,15)<8
    assert F(104,5)*F(16,15)<24
    assert cap<F(2,3)
    rr=s.symbols('r');sums={}
    for power in range(5):
        value=1/(1-rr)
        for _ in range(power):
            value=s.factor(value+rr*s.diff(value,rr))
        sums[str(power)]=str(s.factor(value.subs(rr,s.Rational(24,25))))
    alpha=1/b-F(1,2)
    assert alpha==F(9,22)>0
    assert F(6)*(1/(1-F(1,4)))**2==F(32,3)
    rs=[s.Matrix([[1,0,0],[0,0,-1],[0,1,0]]),
        s.Matrix([[1,0,0],[0,0,1],[0,-1,0]]),
        s.Matrix([[0,0,1],[0,1,0],[-1,0,0]]),
        s.Matrix([[0,0,-1],[0,1,0],[1,0,0]])]
    basis=[s.diag(1,0,0),s.diag(0,1,0),s.diag(0,0,1)]
    for i,j in ((0,1),(0,2),(1,2)):
        matrix=s.zeros(3);matrix[i,j]=matrix[j,i]=1;basis.append(matrix)
    vector=lambda m:s.Matrix([m[0,0],m[1,1],m[2,2],m[0,1],m[0,2],m[1,2]])
    generator=s.Matrix.hstack(*[vector((sum((r*m*r.T for r in rs),s.zeros(3))/4-m)/2)
                                for m in basis])
    metric=s.diag(1,1,1,2,2,2)
    assert generator.T*metric==metric*generator
    assert generator.eigenvals()=={s.Rational(0):1,s.Rational(-1,4):1,
                                   s.Rational(-1,2):1,s.Rational(-3,4):3}
    xx=s.symbols('x0:6');matrix=sum((x*m for x,m in zip(xx,basis)),s.zeros(3));energy=0
    for rotation in rs:
        aa=(s.eye(3)+rotation)/2;bb=(s.eye(3)-rotation)/2
        pp=aa.T*aa;qq=bb.T*bb
        energy+=s.trace(matrix*pp*matrix*pp+matrix*qq*matrix*qq)/4
    remainder=s.factor(s.Rational(3,4)*s.trace(matrix*matrix)-energy)
    assert s.expand(remainder-(xx[2]**2/4+(xx[3]**2+xx[4]**2+xx[5]**2)/2))==0
    sigma1=s.diag(1,s.Rational(21,20),s.Rational(11,10))
    sigma2=s.Matrix([[s.Rational(26,25),s.Rational(1,25),0],
                      [s.Rational(1,25),s.Rational(26,25),0],[0,0,s.Rational(21,20)]])
    mean=s.trace((sigma1+sigma2)/2)/3
    dispersion=sum(s.trace((m-mean*s.eye(3))**2) for m in (sigma1,sigma2))/2
    assert mean==s.Rational(157,150) and dispersion==s.Rational(1,240)
    result={"status":"PASS_independent_exact_algebra",
        "continuation_exponent_lower":str(lower),"rational_exp_lower":str(exp_lower),
        "rho":str(rho),"stage_ratio":str(4*rho),"D_lower":"15/16",
        "first_stage_mean_constant_upper":8,"later_stage_mean_constant_upper":24,
        "sums_(1+level)^p_(24/25)^level":sums,"weighted_radial_alpha":str(alpha),
        "normal_all_grid_height_tail_constant":"32/3",
        "mean_generator_eigenvalues":{str(k):v for k,v in generator.eigenvals().items()},
        "within_copy_energy_remainder":str(remainder),"mu":str(mean),"V0":str(dispersion),
        "no_finite_sampling_or_producer_import":True,"elapsed_seconds":time.perf_counter()-started}
    (Path(__file__).parent/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
