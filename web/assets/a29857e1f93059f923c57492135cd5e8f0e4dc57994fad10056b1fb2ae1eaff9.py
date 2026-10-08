"""Exact general-n algebra for the analytic escalation; no numerical scan."""
from pathlib import Path
import json
import sympy as s
from sympy.physics.wigner import clebsch_gordan


def direct_clebsch_gordan_replay():
    """Fixed exact spin-3/2 reconstruction of the equality vector and tangent."""
    j=s.Rational(3,2)
    n=3
    d=4
    magnetic=[j-q for q in range(d)]
    e=s.zeros(d**3,1)
    for a,ma in enumerate(magnetic):
        for b,mb in enumerate(magnetic):
            for c,mc in enumerate(magnetic):
                ms=mb+mc
                if ma+ms==j:
                    e[(a*d+b)*d+c,0]=(
                        clebsch_gordan(j,j,n,mb,mc,ms)
                        *clebsch_gordan(j,n,j,ma,ms,j))
    raising=s.zeros(d,d)
    for q in range(1,d):
        raising[q-1,q]=s.sqrt(q*(n-q+1))
    generators=[(raising+raising.T)/2,
                (raising-raising.T)/(2*s.I),s.Matrix.diag(*magnetic)]
    identity=s.eye(d)
    h=[-s.Rational(1,2),-s.Rational(1,2),1]
    star=s.zeros(d**3,d**3)
    star_prime=s.zeros(d**3,d**3)
    local_prime=s.zeros(d,d)
    for t in range(3):
        pair=(s.kronecker_product(generators[t],generators[t],identity)
              +s.kronecker_product(generators[t],identity,generators[t]))
        star-=pair
        star_prime-=h[t]*pair
        local_prime+=h[t]*generators[t]*generators[t]
    expectation=lambda operator:s.simplify((e.T.conjugate()*operator*e)[0])
    assert expectation(s.eye(d**3))==1
    assert all(s.simplify(x)==0 for x in star*e-6*e)
    local_a=s.kronecker_product(local_prime,identity,identity)
    local_b=s.kronecker_product(identity,local_prime,identity)
    local_c=s.kronecker_product(identity,identity,local_prime)
    assert expectation(local_a)==s.Rational(3,10)
    assert expectation(local_b)==expectation(local_c)==s.Rational(18,25)
    assert expectation(star_prime)==s.Rational(6,5)
    allocation_prime=s.Rational(5,2)*(
        s.Rational(3,5)*local_a+s.Rational(1,5)*(local_b+local_c))-star_prime
    assert expectation(allocation_prime)==-s.Rational(3,100)
    return {'dimension':d**3,'spin':'3/2','vector_norm_squared':'1',
            'exact_equality_star_eigenvalue':'6','Lprime_A':'3/10',
            'Lprime_B':'18/25','Lprime_C':'18/25','Wprime':'6/5',
            'three_fifths_allocation_derivative':'-3/100',
            'all_assertions':'passed'}


def main():
    n=s.symbols('n',positive=True)
    j=n/2
    first=n/(n+2)
    factorial_second=2*n*(n-1)/((n+2)*(n+3))
    second=s.factor(first+factorial_second)
    ra=s.factor(second-n*first+n*n/4)
    rs=s.factor(n*n-2*n*first+second)
    rb=s.factor(((2*n-2)*rs+n*n)/(4*(2*n-1)))
    la=s.factor(s.Rational(3,2)*ra-s.Rational(1,2)*j*(j+1))
    lb=s.factor(s.Rational(3,2)*rb-s.Rational(1,2)*j*(j+1))
    star=s.factor(s.Rational(3,2)*(j**3/(j+1)+ra)-s.Rational(1,2)*j*(2*j+1))
    kappa=(2*n-1)/(n-1)
    forced=s.factor((star/kappa-lb)/(la-lb))
    assert s.factor(forced-(n+1)/(2*n+1))==0
    alpha=s.symbols('alpha')
    tangent=s.factor(kappa*(alpha*la+(1-alpha)*lb)-star)
    qtotal=n*(n-1)/4
    compressed=s.factor(tangent/qtotal)
    assert s.factor(compressed+3*(2*n+1)/((n+2)*(n+3))*(alpha-forced))==0
    fixed_tangent=s.factor(tangent.subs(alpha,s.Rational(3,5)))
    assert s.factor(fixed_tangent+3*n*(n-1)*(n-2)/(20*(n+2)*(n+3)))==0
    lower=(j-1)/(2*j-1)
    upper=j/(2*j-1)
    lower_margin=s.factor(forced-lower)
    upper_margin=s.factor(upper-forced)
    separate_rhs=(2*n-1)*(n+1)/(2*n+1)
    assert s.factor(separate_rhs-(n-1/(2*n+1)))==0
    nonaffine=s.factor(separate_rhs.subs(n,n+1)-2*separate_rhs+separate_rhs.subs(n,n-1))
    assert nonaffine!=0

    eps=s.Rational(1,63000)
    jsmall=s.Rational(3,2)
    gprime_norm=s.Rational(9,4)
    feasible_quadratic=s.factor(2*gprime_norm**2/jsmall)
    cmin=s.factor(s.factorial(3)*s.factorial(4)/(s.factorial(0)*s.factorial(7)))
    remainder_constant=s.factor(4*feasible_quadratic/cmin)
    assert remainder_constant==945
    exact_margin=s.factor(-s.Rational(3,100)*eps+remainder_constant*eps**2)
    assert exact_margin==-s.Rational(1,4200000)
    product=[s.Rational(5,2),-s.Rational(7,2),-s.Rational(7,2)]
    a,b,c=product
    alpha_fixed=s.Rational(3,5)
    product_star=-a*(b+c)
    product_allocation=2*alpha_fixed*a*a+(1-alpha_fixed)*(b*b+c*c)
    product_margin=s.factor(product_allocation-product_star)
    assert product_margin==-s.Rational(1,5)
    output={
        'scope':'Exact symbolic algebra replay; analytic assumptions and all-j proof are in REPORT.txt. No solver, random scan, or floating eigenvalues.',
        'general_n':{key:str(value) for key,value in {
            'E_r':first,'E_r2':second,'R_A':ra,'R_B':rb,'R_BC':rs,
            'Lprime_A':la,'Lprime_B':lb,'Wprime':star,
            'alpha_forced':forced,'compressed_derivative':compressed,
            'fixed_three_fifths_tangent':fixed_tangent,
            'single_control_lower_margin':lower_margin,
            'single_control_upper_margin':upper_margin,
            'separate_L_G_allocation_rhs':separate_rhs,
            'separate_allocation_nonaffine_second_difference':nonaffine}.items()},
        'spin_three_halves_explicit_failure':{
            'epsilon':str(eps),'weights':[str(1-eps/2),str(1-eps/2),str(1+eps)],
            'Gprime_operator_norm':str(gprime_norm),
            'feasible_dual_quadratic_constant':str(feasible_quadratic),
            'coherent_min_eigenvalue':str(cmin),
            'optimal_envelope_remainder_constant':str(remainder_constant),
            'expectation_upper_bound':str(exact_margin)},
        'spin_seven_halves_single_control_failure':{
            'physical_product_magnetic_labels':[str(x) for x in product],
            'star':str(product_star),'allocation':str(product_allocation),
            'deficit':str(product_margin)},
        'direct_clebsch_gordan_replay':direct_clebsch_gordan_replay()}
    Path(__file__).with_name('exact_algebra_replay.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':
    main()
