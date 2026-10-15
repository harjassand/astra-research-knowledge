"""Exact rational model, fixed-bit approximate sampler with certified bias budget.
Only stdlib. Float inverse-CDF proposals are untrusted and checked with integers.
"""
import sys, json, math, random, time, hashlib, zipfile
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'conditional_precision'))
from audit import read_npy, down, up, fmt, exact
BASE=Path(__file__).parent
FIX=Path(__file__).resolve().parent.parent/'fixture.npz'
B=256; S=1<<B; COIN=64; T=F(1,200); DELTA=T/F(10**12)

def ceildiv(a,b): return -(-a//b)
def expneg(x):
    """Outward fixed-point alternating Taylor enclosure; 0<=x<=1."""
    assert 0<=x<=1
    a,d=x.numerator,x.denominator
    tl=tu=S; sl=su=S
    for j in range(1,41):
        tl=tl*a//(d*j);tu=ceildiv(tu*a,d*j)
        if j%2: sl-=tu;su-=tl
        else: sl+=tl;su+=tu
    remainder=ceildiv(tu*a,d*41)
    return max(0,sl-remainder),min(S,su)

def mul(a,b):return (a[0]*b[0]//S,ceildiv(a[1]*b[1],S))
def prepare():
    if not __debug__: raise RuntimeError("Run without -O: certificate assertions must remain enabled")
    pin=json.loads((Path(__file__).resolve().parent.parent/'conditional_precision'/'model_pin.json').read_text())
    assert hashlib.sha256(FIX.read_bytes()).hexdigest()==pin['fixture_sha256']
    with zipfile.ZipFile(FIX) as z:
        raw={name:read_npy(z.read(name+'.npy')) for name in ['lam','W','k']}
    assert pin['lam_decimal']==[repr(v) for v in raw['lam']]
    lam=list(map(F,pin['lam_decimal']));w=[F(repr(v)) for v in raw['W']]
    n=len(lam);k=raw['k'][0]
    assert max(lam)*T<=F(1,2)
    assert F(2*(k-1),n)*sum(lam)*T<=1
    # Stronger fixture-specific bounds certify the fixed Taylor precision.
    assert max(lam)*T<F(3,400)
    assert F(2*(k-1),n)*sum(lam)*T<F(3,10)
    assert n==400 and k==20 and all(0<=v<=F(2,n) for v in w)
    assert all(w[i*n+i]==0 for i in range(n))
    ld=math.lcm(*(x.denominator for x in lam));wd=math.lcm(*(x.denominator for x in w))
    li=[int(x*ld) for x in lam];wi=[int(x*wd) for x in w]
    columns=[sum(li[j]*wi[j*n+i] for j in range(n)) for i in range(n)]
    ps=[]
    for rate in lam:
        lo,hi=expneg(rate*T);ps.append((S-hi,S-lo))
    tails=[[(0,0)]*(k+1) for _ in range(n+1)]
    for row in tails:row[0]=(S,S)
    for i in range(n-1,-1,-1):
        p=ps[i];pc=(S-p[1],S-p[0])
        for r in range(1,min(k,n-i)+1):
            a=mul(pc,tails[i+1][r]);b=mul(p,tails[i+1][r-1])
            tails[i][r]=(a[0]+b[0],min(S,a[1]+b[1]))
    qs={};widths=[]
    for i in range(n):
        widths.append(0)
        for r in range(max(0,k-i),min(k,n-i)+1):
            if r==0:q=ps[i]
            elif r==n-i:q=(S,S)
            else:
                d=tails[i][r];assert d[0]>0
                a=mul(ps[i],tails[i+1][r-1]);q=(a[0]*S//d[1],min(S,ceildiv(a[1]*S,d[0])))
            qs[i,r]=q[0] # lower endpoint; exactly a B-bit probability
            widths[-1]=max(widths[-1],q[1]-q[0])
    C=math.prod(1+F(2*j,n) for j in range(k))
    tv=F(sum(widths),S)
    return dict(lam=lam,n=n,k=k,li=li,wi=wi,ld=ld,wd=wd,columns=columns,ps=ps,qs=qs,h=tails[0][k],C=C,tv=tv)

def inverse_time(rate,p,u):
    # Float candidate only proposes an exact dyadic rational. Never trusted.
    cand=F.from_float(-math.log1p(-float(u)*(-math.expm1(-float(rate*T))))/float(rate))
    def cert(c):
        lo=max(F(0),c-DELTA);hi=min(T,c+DELTA)
        elo=expneg(rate*lo);ehi=expneg(rate*hi)
        return (S-elo[0])*u.denominator <= u.numerator*p[0] and (S-ehi[1])*u.denominator >= u.numerator*p[1]
    if 0<=cand<=T and cert(cand):return cand,False
    # Guaranteed finite fallback: monotone interval bisection. If intervals
    # overlap, all inverse roots are within a tiny certified neighborhood.
    lo=F(0);hi=T
    for _ in range(64):
        c=(lo+hi)/2
        if cert(c):return c,True
        e=expneg(rate*c)
        if (S-e[1])*u.denominator > u.numerator*p[1]:hi=c
        elif (S-e[0])*u.denominator < u.numerator*p[0]:lo=c
        else:
            # An overlap at precision B implies distance far below DELTA;
            # checked rather than assumed, so kernel bugs cannot pass silently.
            assert cert(c),'insufficient exponential precision'
            return c,True
    raise AssertionError('inverse-time bound failed')

def sample(m,rng):
    need=m['k'];selected=[]
    for i in range(m['n']):
        if rng.getrandbits(B)<m['qs'][i,need]:
            selected.append(i);need=max(0,need-1)
    assert need==0
    times=[];fallback=0
    for i in selected:
        u=F(2*rng.getrandbits(COIN)+1,1<<(COIN+1))
        t,f=inverse_time(m['lam'][i],m['ps'][i],u);fallback+=f
        times.append((t,i))
    times.sort();history=[];excess=0;H=F(0);J=F(1);last=F(0)
    n=m['n'];wi=m['wi'];li=m['li'];wd=m['wd'];ld=m['ld']
    for t,i in times[:m['k']]:
        H+=F(excess,ld*wd)*(t-last)
        load=sum(wi[i*n+j] for j in history)
        J*=F(wd+load,wd)
        excess+=m['columns'][i]-sum(li[j]*wi[j*n+i] for j in history)-li[i]*load
        assert excess>=0
        history.append(i);last=t
    assert 0<=H<=1
    el,eu=expneg(H)
    # Output is a fixed rational midpoint; clip to the exact likelihood bound.
    lower=max(F(0),J*F(el,S));upper=min(m['C'],J*F(eu,S))
    assert lower<=upper and upper-lower<=F(1,1<<200)
    return (lower+upper)/2, fallback,len(selected)

def run(N,seed):
    start=time.monotonic();m=prepare();prep=time.monotonic()-start
    rng=random.Random(seed);ys=[];fallback=0;maxselected=0
    for _ in range(N):
        y,f,s=sample(m,rng);ys.append(y);fallback+=f;maxselected=max(s,maxselected)
    # Probability/expectation certificates are exact rationals.
    eps=DELTA+T/F(1<<COIN) # inverse Lipschitz <=2T; half-cell <=2^(-b-1)
    order=min(F(1),4*m['n']*(m['n']-1)*eps/T)
    M=F(2*(m['k']-1),m['n'])*sum(m['lam'])
    bias=F(1,1<<200)+m['C']*(m['tv']+order+2*m['k']*M*eps)
    mean=sum(ys)/N
    variance=sum((y-mean)**2 for y in ys)/(N-1) if N>1 else F(0)
    # log(80)< 4.383 certified by positive Taylor partial sum exp(4.383)>80.
    logupper=F(4383,1000)
    term=total=F(1)
    for j in range(1,40):term*=logupper/j;total+=term
    assert total>80
    radicand=2*variance*logupper/N
    scale=1<<128
    root=math.isqrt(ceildiv(radicand.numerator*scale*scale,radicand.denominator))+1
    R=F(root,scale)+7*m['C']*logupper/(3*(N-1)) if N>1 else m['C']
    plo=F(m['h'][0],S)*max(F(1),mean-R-bias)
    phi=F(m['h'][1],S)*min(m['C'],mean+R+bias)
    out=dict(run_role='Confirmatory fixed-N demonstration with fresh seed distinct from the seed-721 runtime pilot' if seed==722 else 'Exploratory reproducibility demonstration',scope='Certified numerical bias contract for pinned synthetic model. Confidence theorem is conditional on iid unbiased random bits. Seeded PRNG demonstration is not proof of that premise.',N_fixed=N,seed=seed,bits=B,time_coin_bits=COIN,prepare_seconds=prep,total_seconds=time.monotonic()-start,mean=fmt(mean),sample_variance=fmt(variance),C=fmt(m['C']),h0_interval=[fmt(F(m['h'][0],S),False),fmt(F(m['h'][1],S))],label_tv=fmt(m['tv']),order_mismatch_probability_upper=fmt(order),normalized_bias_upper=fmt(bias),normalized_bias_exact=exact(bias),empirical_bernstein_radius_upper=fmt(R),conditional_95pct_probability_interval=[fmt(plo,False),fmt(phi)],relative_halfwidth_vs_lower_upper=fmt((phi-plo)/(2*plo)),inverse_fallbacks=fallback,max_selected=maxselected)
    (BASE/f'results_{N}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 10,int(sys.argv[2]) if len(sys.argv)>2 else 721)
