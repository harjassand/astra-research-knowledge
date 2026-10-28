"""Exact algebraic receipt for the g^-3 calibration cost review.

No Bernoulli samples or trajectories are executed. Trial counts below are
proposed budgets. The checks use exact rational operator calculations.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json


def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def psd2(a):
    return a[0][0]>=0 and a[1][1]>=0 and a[0][0]*a[1][1]-a[0][1]**2>=0


def inv2(a):
    det=a[0][0]*a[1][1]-a[0][1]*a[1][0]
    assert det>0
    return [[a[1][1]/det,-a[0][1]/det],[-a[1][0]/det,a[0][0]/det]]


def ceilq(x):
    return (x.numerator+x.denominator-1)//x.denominator


def norm2(v):
    return sum((x[0]*x[0] for x in v),F(0))


def run():
    upper=[];lower=[]
    for m in [4,8,16,32,64,128]:
        g=F(1,m);a=1-g/2;h=1-a*a
        tail=1/h;depth=ceilq(tail);normalizer=depth+tail
        assert depth==m+1
        assert F(15,16)*g<=h<=g
        matrices=[[[1-g,g],[g,F(1,4)]],[[1-2*g,g],[g,F(1,3)]]]
        for i,A in enumerate(matrices):
            assert psd2(A)
            assert psd2([[a-A[0][0],-A[0][1]],[-A[1][0],a-A[1][1]]])
            assert all(min(row)>=0 and sum(row)<=1 for row in A)
            A2=mm(A,A)
            inv=inv2([[1-A2[0][0],-A2[0][1]],[-A2[1][0],1-A2[1][1]]])
            Q=g*g*inv[1][1]
            assert Q<=2*g*g
            state=[[F(0)],[g]]
            polynomial=F(0)
            for k in range(depth):
                polynomial+=norm2(state)
                state=mm(A,state)
            polynomial+=tail*norm2(state)
            assert Q<=polynomial<=2*Q
            event_probability=polynomial/normalizer
            assert event_probability<=8*g**3
            departure=1-A[0][0]
            expected_ops=1+departure*(depth*depth+tail*(2*depth+1))/normalizer
            expected_bits=1+2*departure-departure/normalizer
            assert expected_ops<=1+departure*(2*depth+1)<=F(13,2)
            assert expected_bits<=1+2*departure
            expected_end_out=F(0)
            # Conditional on first departure, compute the terminal return
            # probability without observing hidden identities.
            endpoint=[[F(0)],[g]]
            # Joint distribution after step 1 and the event of departure.
            for k in range(depth+1):
                if k==0:
                    endpoint=mm(A,endpoint)  # length 2
                else:
                    endpoint=mm(A,mm(A,endpoint))
                weight=tail if k==depth else F(1)
                expected_end_out+=weight*(departure-endpoint[0][0])/normalizer
            assert 0<=expected_end_out<=departure

            n=2560*m**3;L=F(10)
            variance_term=g*g/8
            assert variance_term**2==2*(2*g)*L/n
            radius=variance_term+2*L/(3*n)
            assert radius<=g*g/4
            flag_upper_envelope=4*event_probability+6*L/n
            Q_upper_envelope=normalizer*flag_upper_envelope
            model_Q_envelope=2*Q_upper_envelope+2*radius**2/h
            model_R_lower=1-(A[0][0]+radius)**2
            assert model_R_lower>0
            error_envelope=2*model_Q_envelope/model_R_lower+radius/model_R_lower
            upper.append({
                "g":str(g),"action":i,"source_norm_cap":str(a),
                "depth":depth,"normalizer":str(normalizer),
                "Q_over_g_squared":str(Q/g**2),
                "finite_form_over_Q":float(polynomial/Q),
                "mixture_probability_over_g_cubed":float(event_probability/g**3),
                "expected_primitive_steps_per_trial":str(expected_ops),
                "expected_membership_bits_per_trial":str(expected_bits),
                "expected_actual_preparations_per_trial_upper":str(departure),
                "terminal_outside_probability":float(expected_end_out),
                "proposed_trials_not_executed":n,
                "variance_aware_radius":str(radius),
                "high_probability_error_envelope_over_g":float(error_envelope/g),
                "all_exact_checks_passed":True})

        p0=1-g;p1=1-g+g*g
        assert 0<p0<p1<=a<1
        chi=g**4/(p1*(1-p1))
        assert chi<=F(16,9)*g**3
        H=m;gap=p1**H-p0**H
        assert gap>=g*(1-g)**(H-1)>g/3
        assert gap>2*g/10
        assert F(2,9)/(F(16,9)*g**3)==1/(8*g**3)
        lower.append({"g":str(g),"p0":str(p0),"p1":str(p1),
                      "source_norm_cap":str(a),"horizon":H,
                      "chi_square_over_g_cubed":str(chi/g**3),
                      "target_gap_over_g":float(gap/g),
                      "expected_source_steps_lower":str(1/(8*g**3)),
                      "both_Galerkin_residuals_zero":True,
                      "all_exact_checks_passed":True})

    rescaled=[]
    target_constant=F(4);beta=F(25)
    assert beta>6*target_constant
    for m in [64,128,256]:
        g=F(1,m);p0=1-g;p1=1-g+beta*g*g
        assert g<=1/(2*beta) and p1<=1-g/2
        chi=beta**2*g**4/(p1*(1-p1))
        assert chi<=F(8,3)*beta**2*g**3
        gap=p1**m-p0**m
        assert gap>=beta*g*(1-g)**(m-1)>beta*g/3>2*target_constant*g
        rescaled.append({"g":str(g),"target_accuracy_over_g":str(target_constant),
                         "beta":str(beta),"target_gap_over_g":float(gap/g),
                         "expected_source_steps_lower":str(1/(12*beta**2*g**3)),
                         "all_exact_checks_passed":True})
    assert sum((F(10**k,factorial(k)) for k in range(30)),F(0))>8000
    output={"scope":"Exact algebra, not executed stochastic acquisition.",
            "upper_class_constants":{"c":"1/2","departure_upper_constant":2,
                                     "Q_upper_constant":2,"q":2,
                                     "confidence_log_budget":10},
            "upper_fixtures":upper,"lower_fixtures":lower,
            "rescaled_accuracy_lower_fixtures":rescaled,
            "all_checks_passed":True}
    path=Path(__file__).with_name("CALIBRATION_COST_REVIEW_CHECKS.json")
    path.write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps(output,indent=2))


if __name__=="__main__":
    run()
