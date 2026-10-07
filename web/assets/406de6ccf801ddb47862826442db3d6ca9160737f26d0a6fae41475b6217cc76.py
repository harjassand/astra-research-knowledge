from math import comb, prod, log, lgamma
from fractions import Fraction
from decimal import Decimal, localcontext
import json
from pathlib import Path

def fall(j,m): return prod(range(j-m+1,j+1)) if j>=m else 0

def weights(v,m,rho_num=1,rho_den=4):
    lo,n=m-1,v-m+1
    return {j:rho_num**(j-lo)*rho_den**(n-j)*prod(comb(v-2*r,j-r) for r in range(m)) for j in range(lo,n+1)}

def numerical(x):
    with localcontext() as c:
        c.prec=60
        return str(Decimal(x.numerator)/Decimal(x.denominator))

checks=0
for m in range(1,5):
    for v in range(max(2*m,8),33):
        w=weights(v,m)
        for j in range(m-1,v-m+1):
            assert w[j]*fall(v-j,m)==4*w[j+1]*fall(j+1,m)
            checks+=1
        for j in w:
            flux=0
            if j-1 in w:flux+=w[j-1]*fall(v-j+1,m)
            if j+1 in w:flux+=4*w[j+1]*fall(j+1,m)
            flux-=w[j]*(fall(v-j,m)+4*fall(j,m))
            assert flux==0
            checks+=1
        L=max(m,v//4)
        if L<=v//2:
            h={L-1:Fraction(0)}
            tail=0
            tails={}
            for j in reversed(w):
                tail+=w[j];tails[j]=tail
            for j in range(L,v-m+2):
                h[j]=h[j-1]+Fraction(tails[j]*v**(m-1),4*fall(j,m)*w[j])
            for j in range(L,v-m+2):
                b=Fraction(fall(v-j,m),v**(m-1));d=Fraction(4*fall(j,m),v**(m-1))
                generator=d*(h[j-1]-h[j])
                if j+1 in h:generator+=b*(h[j+1]-h[j])
                assert generator==-1
                checks+=1

q,p=Fraction(1,4),Fraction(1,3)
delta=2*(float(q)*log(float(q/p))+float(1-q)*log(float((1-q)/(1-p))))
report={"status":"exact finite algebra checks plus numerical asymptotic evaluations, no trajectory simulation", "exact_checks":checks,"m":2,"kappa":1,"K":4,"q":"1/4","p":"1/3","delta":delta,"volumes":[]}
for v in (100,200,500,1000,1200,1240,1280,1400,3000):
    w=weights(v,2);L=v//4;mid=v//2;n=v-1
    R=Fraction(sum(w[j] for j in range(1,L+1)),sum(w[j] for j in range(1,mid+1)))
    T=6_000_000_000
    dL=Fraction(4*fall(L,2),v)
    exit_bound=2*dL*T*R
    # Exact stationary comparison bound; Decimal evaluation is descriptive.
    row={"V":v,"stationary_tail_ratio":numerical(R),"uniform_marginal_bound":numerical(2*R),"exit_bound_T_6e9":numerical(exit_bound),"negative_log_ratio_per_V":-(log(R.numerator)-log(R.denominator))/v}
    with localcontext() as c:
        c.prec=70
        running=0;mean=Decimal(0)
        tails={}
        for j in range(n,0,-1): running+=w[j];tails[j]=running
        for j in range(L,mid+1):
            mean+=Decimal(tails[j]*v)/Decimal(4*fall(j,2)*w[j])
        row["left_hitting_mean_numerical"]=str(mean)
        row["log_mean_per_V"]=float(mean.ln()/Decimal(v))
    if v==3000:
        row["rigorous_exit_bound_lt_1e_minus_30"]=exit_bound<Fraction(1,10**30)
        row["rigorous_exit_bound_lt_1e_minus_29"]=exit_bound<Fraction(1,10**29)
    if v==1240:
        row["rigorous_exit_bound_lt_1e_minus_6"]=exit_bound<Fraction(1,10**6)
    report["volumes"].append(row)
Path('work/cycle1/reaction_robust_birth_death_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
