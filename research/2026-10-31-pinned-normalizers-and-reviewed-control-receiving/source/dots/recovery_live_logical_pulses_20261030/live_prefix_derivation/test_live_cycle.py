import itertools, json, math, random
out={}
# Exhaust actual CSS support law for two banks of length 3: per-output
# CSS weight <= input total. This is sharper than multiplying total by 2.
count=0
for bits in itertools.product((0,1), repeat=12):
    xc,zc,xt,zt=[bits[3*j:3*j+3] for j in range(4)]
    yc=xc; vc=tuple(a^b for a,b in zip(zc,zt))
    yt=tuple(a^b for a,b in zip(xt,xc)); vt=zt
    w=sum(bits)
    assert sum(yc)+sum(vc)<=w
    assert sum(yt)+sum(vt)<=w
    count+=1
out['exact_CNOT_CSS_support_cases']=count
# Numerical fixtures check algebra only, not native hardware estimates.
rng=random.Random(20261030)
for _ in range(10000):
    s=rng.uniform(.1,3); sp=s*rng.uniform(.1,.9)
    ec=rng.uniform(.001,.1); r0=rng.uniform(.01,.3)
    h=rng.uniform(.01,2); cu=rng.uniform(.1,20)
    f=rng.randint(1,20); a=rng.randint(1,20); R=rng.uniform(1,100)
    Ae=2*cu/h; Ab=6*cu*f+R; Ap=2*cu*(1+f*a)+R*a
    alpha=min(sp*ec/(4*s),cu*r0/2)
    e=alpha/(3*(Ae+1)); b=alpha/(3*(Ab+1)); p=alpha/(3*(Ap+1))
    d=2*e/h+6*f*b+2*(1+f*a)*p
    bp=b+a*p; Ep=cu*d+R*bp
    assert Ep<alpha and d<r0/2 and s*Ep<sp*ec/4
    g=sp*e/16; qt=sp*e/16
    nu=g+sp*e/8
    w=g+s*Ep; TE=sp*e-qt
    cB=rng.uniform(.1,1); CB=cB+rng.uniform(.1,3)
    delta=rng.uniform(.0001,.1); nuB=cB*delta*b/2
    wB=2*CB*delta*bp; TB=2*cB*delta*b
    rateE=rng.uniform(1e-9,1); rateB=rng.uniform(.01,2)
    tE=math.log(max(1,2*max(0,w-nu)/(TE-nu)))/rateE
    tB=math.log(max(1,2*max(0,wB-nuB)/(TB-nuB)))/rateB
    t=max(tE,tB)
    E_t=nu+(w-nu)*math.exp(-rateE*t)
    B_t=nuB+(wB-nuB)*math.exp(-rateB*t)
    assert E_t<=.5*(TE+nu)*(1+1e-12)
    assert B_t<=.5*(TB+nuB)*(1+1e-12)
    assert max(w,nu)+qt<sp*ec/2
out['strict_budget_algebra_fixtures']=10000
out['not_a_native_numeric_threshold']=True
# Counterexample: mean energy does NOT imply warm exponential-moment bound.
# State has energy N with probability 1/N, else 0: mean=1,
# log E exp(sE)/N -> s, not 0.
N=1000;s=.1
logmoment=math.log1p((math.exp(s*N)-1)/N)
assert logmoment>N*s*.9
out['mean_energy_shortcut_counterexample']={'N':N,'mean_E':1,'log_moment':logmoment}
print(json.dumps(out,indent=2))
