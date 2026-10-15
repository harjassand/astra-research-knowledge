if not __debug__:
    raise RuntimeError("Run without -O / PYTHONOPTIMIZE")
"""Stdlib-only certified audit; no floating-point arithmetic in certificates.
Float decoding is used ONLY to pin each stored fixture scalar to Fraction(repr(x)).
"""
import ast, hashlib, json, struct, zipfile, time
from fractions import Fraction as F
from decimal import Decimal, localcontext, ROUND_CEILING, ROUND_FLOOR
from pathlib import Path
BASE=Path(__file__).resolve().parent
FIX=Path(__file__).resolve().parent.parent/'fixture.npz'

def read_npy(raw):
    assert raw[:6] == b'\x93NUMPY'
    major=raw[6]
    fmt, off=('<H',10) if major==1 else ('<I',12)
    length=struct.unpack_from(fmt,raw,8)[0]
    meta=ast.literal_eval(raw[off:off+length].decode('latin1'))
    assert not meta['fortran_order']
    dtype=meta['descr']; assert dtype in ('<f8','<i8')
    data=raw[off+length:]
    return [x[0] for x in struct.iter_unpack('<d' if dtype=='<f8' else '<q',data)]

def down(x,S): return x.numerator*S//x.denominator

def up(x,S): return -((-x.numerator*S)//x.denominator)

def fmt(x,upper=True):
    with localcontext() as c:
        c.prec=30; c.rounding=ROUND_CEILING if upper else ROUND_FLOOR
        return str(Decimal(x.numerator)/Decimal(x.denominator))

def exact(x): return {'numerator':str(x.numerator),'denominator':str(x.denominator)}

def exp_bracket(x,b):
    # For 0<x<1, odd/even alternating partial sums bound exp(-x).
    assert 0<x<1
    total=F(1); term=F(1); lo=F(0); hi=F(1); j=0
    while hi-lo>F(1,1<<(b+16)):
        j+=1;term*=(-x)/j;total+=term
        if j%2: lo=total
        else: hi=total
    return lo,hi,j

def audit(lam,T,k,b):
    S=1<<b;n=len(lam)
    ps=[];terms=[]
    for rate in lam:
        lo,hi,j=exp_bracket(rate*T,b)
        ps.append((down(1-hi,S),up(1-lo,S)));terms.append(j)
    def mul(a,b): return (a[0]*b[0]//S,(a[1]*b[1]+S-1)//S)
    tails=[[(0,0) for _ in range(k+1)] for _ in range(n+1)]
    for row in tails: row[0]=(S,S)
    for i in range(n-1,-1,-1):
        p=ps[i];pc=(S-p[1],S-p[0])
        for r in range(1,min(k,n-i)+1):
            a=mul(pc,tails[i+1][r]);d=mul(p,tails[i+1][r-1])
            tails[i][r]=(a[0]+d[0],min(S,a[1]+d[1]))
    h=tails[0][k];assert h[0]>0
    perstep=[];worst=(0,None);count=0;min_den=S
    for i in range(n):
        maxw=0
        # r=0 means the threshold was already attained; positive needs r=k-j.
        for r in range(max(0,k-i),min(k,n-i)+1):
            if r==0: q=ps[i]
            elif r==n-i: q=(S,S)
            else:
                d=tails[i][r];assert d[0]>0,(b,i,r)
                min_den=min(min_den,d[0])
                a=mul(ps[i],tails[i+1][r-1])
                q=(a[0]*S//d[1],min(S,(a[1]*S+d[0]-1)//d[0]))
            assert 0<=q[0]<=q[1]<=S
            w=q[1]-q[0];count+=1;maxw=max(maxw,w)
            if w>worst[0]:worst=(w,[i,r])
        perstep.append(maxw)
    # A b-bit integer U is compared to any dyadic threshold selected in q's
    # bracket. Width + 2^-b also covers floor-rounding a chosen real threshold.
    tv=F(sum(perstep)+n,S)
    C=F(1)
    for j in range(k): C*=1+F(2*j,n)
    return dict(bits=b,tail_lower=fmt(F(h[0],S),False),tail_upper=fmt(F(h[1],S)),
        tail_integer_endpoints=list(map(str,h)),tail_grid_denominator=str(S),
        tail_relative_width_upper=fmt(F(h[1]-h[0],h[0])),
        exponential_taylor_terms_max=max(terms),reachable_coin_count=count,
        max_coin_width_upper=fmt(F(worst[0],S)),worst_coin_i_r=worst[1],
        smallest_nondeterministic_tail_lower=fmt(F(min_den,S),False),
        label_total_variation_upper=fmt(tv),label_total_variation_exact_bound=exact(tv),
        normalized_expectation_error_upper=fmt(C*tv),
        label_induced_relative_probability_error_upper=fmt(C*tv),
        C_upper=fmt(C),C_exact=exact(C))

def main():
    started=time.monotonic()
    with zipfile.ZipFile(FIX) as z:
        arr={name:read_npy(z.read(name+'.npy')) for name in ['lam','W','T','k','beta']}
    lam=[F(repr(x)) for x in arr['lam']];T=F('0.005'); k=arr['k'][0]
    assert repr(arr['T'][0])=='0.005' and arr['beta']==[2.0]
    assert len(lam)==400 and k==20 and len(arr['W'])==400**2
    W=[F(repr(x)) for x in arr['W']]
    assert all(0<=w<=F(1,200) for w in W)
    assert all(W[i*400+i]==0 for i in range(400))
    pin={'model':'Each lam and W scalar equals the exact rational denoted by Python repr of its stored binary64 fixture scalar; T=1/200; beta=2. This is an explicitly new exact-model pin, not the original floating-point simulation law.',
         'fixture_sha256':hashlib.sha256(FIX.read_bytes()).hexdigest(),
         'lam_decimal':[repr(x) for x in arr['lam']], 'T':'0.005','n':400,'k':20,
         'W_pin':'repr of each row-major binary64 scalar in the SHA256-pinned fixture',
         'W_bounds_verified':'0 <= W_ij <= 1/200; W_ii=0'}
    (BASE/'model_pin.json').write_text(json.dumps(pin,indent=2)+'\n')
    out={'scope':'Reference event probability and event-conditioned Bernoulli labels only; NOT an end-to-end certificate for floating failure times or likelihoods.',
         'model_pin':'model_pin.json','audits':[audit(lam,T,k,b) for b in (256,512)],
         'runtime_seconds':time.monotonic()-started}
    (BASE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
