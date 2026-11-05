"""Evaluate the available factorial-tail / actual-weight alternative.

This is high-precision resource arithmetic, not experiment execution or a
lower bound. Actual deployment must certify the coefficient rounding as in
the proof. The factor-of-two norm inflation is deliberately conservative.
"""
import json, math
from pathlib import Path
import mpmath as mp
from check_finite_derivative import weights
mp.mp.dps=80
n,M,k=2,15,2
B,r,kappa,eps=map(mp.mpf,["1.37","4","2.46","0.1"])
Lam=2*B+2*n*r
T=mp.log(400*n/eps**2)/kappa
eta=eps/(100*M*T); h=1/(8*Lam); delta=eps/100
rows=[]
for b in [1,2]:
    s=b+1; D=max(s,2)
    while True:
        _,aw=weights(D,s); _,at=weights(D,1)
        # The w=0 column is exactly zero, so it can be omitted.
        A=sum(abs(x) for x in aw[:-1])*sum(abs(x) for x in at)
        A/=2*math.factorial(s)*r**s*h**(s+1)
        A_safe=2*A+eta/16
        R=2*mp.exp(mp.mpf(3)/8)*mp.power(4,-D-1)/mp.factorial(D+1)
        if A_safe*R<=eta/4:
            break
        D+=1
    pmax=(r*h)**s
    N=mp.ceil(32*(A_safe**2*pmax/eta**2+A_safe/eta)*mp.log(2*M/delta))
    rows.append(dict(front_sites=b,degree=D,actual_weight_l1=str(A),
                     inflated_weight_bound=str(A_safe),factorial_tail_bound=str(R),
                     coefficient_bias_bound=str(A_safe*R),
                     log10_total_raw_trials=float(mp.log10(M*N)),
                     minimum_timing_accuracy=str(eta/(48*Lam*A_safe)),
                     note="Same source/capture parameters and eta as the loose schedule; finite dyadic randomized node scheme."))
result=dict(n=n,M=M,k=k,B_H=str(B),r=str(r),margin=str(kappa),epsilon=str(eps),
            capture_time=str(T),coefficient_accuracy=str(eta),h=str(h),rows=rows,
            scope="Numerical resource evaluation of an explicit sufficient upper bound. No raw trials or physical receiver executed. No claim of optimality.")
Path(__file__).with_name("sharper_schedule.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
