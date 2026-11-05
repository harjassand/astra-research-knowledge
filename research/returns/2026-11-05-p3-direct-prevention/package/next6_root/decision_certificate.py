"""Decision certificates; no weights, absolute rarity or lifetime are inputs."""
from fractions import Fraction
from decimal import Decimal, localcontext

def display(x, digits=30):
    if not isinstance(x,Fraction): return str(x)
    with localcontext() as c:
        c.prec=digits
        return str(Decimal(x.numerator)/Decimal(x.denominator))

def ceil_fraction(x):
    return -(-x.numerator//x.denominator)

def exp_minus_lower_small(z):
    assert 0<=z<=1
    # Alternating Taylor series; the last (odd) term gives a lower bound.
    total=Fraction(1); term=Fraction(1)
    for j in range(1,8):
        term*=(-z)/j; total+=term
    return total

def phi_lower_small(z):
    assert 0<=z<=1
    total=Fraction(1); term=Fraction(1)
    for j in range(1,8):
        term*=(-z)/(j+1); total+=term
    return total

def bernoulli_envelope(successes, trials, alpha=Fraction(1, 1000), bits=36):
    """Exact-integer, two one-sided martingale Chernoff inversions.

    If all conditional success means lie in [p_lo,p_hi], the lower endpoint
    is <=p_hi and the upper endpoint >=p_lo except with probability alpha each.
    """
    s,n=int(successes),int(trials)
    assert 0<=s<=n and n>0 and 0<alpha<1
    D=1<<bits
    fixed=(D**n)*(s**s)*((n-s)**(n-s))*alpha.numerator
    n_power=n**n
    def outside(a):
        return (a**s)*((D-a)**(n-s))*n_power*alpha.denominator<=fixed
    if s==0: lower=0
    else:
        lo,hi=0,(s*D+n-1)//n
        while hi-lo>1:
            mid=(lo+hi)//2
            if outside(mid): lo=mid
            else: hi=mid
        lower=lo
    if s==n: upper=D
    else:
        lo,hi=(s*D)//n,D
        while hi-lo>1:
            mid=(lo+hi)//2
            if outside(mid): hi=mid
            else: lo=mid
        upper=hi
    return Fraction(lower,D),Fraction(upper,D)

def structural(N, eta='0.01', rlo='0.20', rhi='1', qbar='0.25', gamma='0.14'):
    """Exact-rational true-Q bound. Exp tail <=2^-C, sqrt(a^k)<=a^floor(k/2)."""
    eta,rl,rh,q,gam=map(Fraction,[eta,rlo,rhi,qbar,gamma])
    pbar=q**N; a=q/(1-q); g=gam/(N*rh); s0=(1-pbar)**2
    c=0
    while Fraction(1,1<<c)/g>eta*s0/3: c+=1
    L=max(1,ceil_fraction(c/g))
    k=1
    while L*a**k>eta*s0/3: k+=1
    assert k<N
    dmin=rl/rh
    nu=(1-Fraction(k,N))*dmin*(1-q)-Fraction(k,N)*q
    contrast=q/(dmin*(1-q)); rho=contrast*k/(N-k)
    assert nu>0 and rho<1
    zeta=contrast/(N-1)/(1-rho)
    assert zeta<1
    rem=L*a**k+a**(k//2)*Fraction(1,1<<c)/g
    lo=(1-pbar)**2; hi=1/(1-zeta)+rem
    err=pbar*(L+k/nu)+rem
    exact={'p_upper':pbar,'g':g,'nu':nu,'C':contrast,'rho':rho,'return_bound':zeta,
           'remainder':rem,'q0S_lower':lo,'q0S_upper':hi,'sparse_score_error':err,'s0':s0}
    return {'N':N,'L_analysis_only':L,'k':k,'binary_tail_exponent':c,
            **{key:display(value) for key,value in exact.items()},
            'structural_arithmetic':'Exact Fraction throughout; displayed decimals rounded.'}, exact

def mean_ratio_interval(N, observed, h=Fraction(1,4), omega=Fraction(1,100),
                        bias=Fraction(1,1000), alpha=Fraction(1,1200),
                        timing_contract='exogenous'):
    """Exogenous timer may depend on prior history; optional path-adaptive bound."""
    cert,exact=structural(N)
    lower_fun=phi_lower_small if timing_contract=='exogenous' else exp_minus_lower_small
    km=(1-omega)*lower_fun(h*(1+omega)); kp=1+omega
    env={}; theta={}
    for action,(s,n) in observed.items():
        l,u=bernoulli_envelope(s,n,alpha)
        theta[action]=(max(Fraction(0),(l-bias)/kp),(u+bias)/km)
        env[action]={'successes':s,'trials':n,'mean_lower_fraction':str(l),
            'mean_upper_fraction':str(u),'theta_lower':display(theta[action][0]),
            'theta_upper':display(theta[action][1])}
    chosen=min(env,key=lambda u: theta[u][1])
    factor=exact['q0S_lower']/exact['q0S_upper']
    ratios={other:factor*theta[other][0]/theta[chosen][1] for other in env if other!=chosen}
    return {'structural':cert,'kminus':str(km),'kplus':str(kp),
            'timing_contract':timing_contract,
            'conditional_bias_budget':str(bias),'per_tail_confidence':str(alpha),
            'envelopes':env,'chosen':chosen,
            'relative_mean_lower_vs_others':{u:display(r) for u,r in ratios.items()},
            'certifies_best':all(x>1 for x in ratios.values()),
            'arithmetic_note':'All issuing comparisons exact rational/integer; displayed decimal ratios are rounded.'}
