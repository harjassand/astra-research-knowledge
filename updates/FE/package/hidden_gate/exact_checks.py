"""Exact rational tests of the one-edge minimax endpoint lemma and interval coverage."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
from fractions import Fraction as F
import sympy as sp
import random, json, time, itertools

def run():
    rng=random.Random(731091); cases=0; asserts=0; completions=0
    st=time.perf_counter()
    for n in range(2,6):
        for case in range(8):
            # Sink star guarantees SPD at every positive completion.
            edges=[(i,-1) for i in range(n)]
            for i in range(n):
                for j in range(i+1,n):
                    if rng.random()<.45:edges.append((i,j))
            vecs=[]
            for i,j in edges:
                d=sp.zeros(n,1);d[i]=1
                if j>=0:d[j]=-1
                vecs.append(d)
            m=sp.Matrix([sp.Rational(rng.randint(1,5),rng.randint(1,4)) for _ in range(n)])
            lo=[sp.Rational(rng.randint(1,3),rng.randint(1,5)) for _ in edges]
            hi=[x+sp.Rational(rng.randint(1,6),rng.randint(1,4)) for x in lo]
            def mat(c):
                return sum((x*d*d.T for x,d in zip(c,vecs)),sp.zeros(n))
            Al=mat(lo);Ah=mat(hi);Kl=Al.inv();Kh=Ah.inv();ul=Kl*m;uh=Kh*m
            fl=(m.T*ul)[0];fh=(m.T*uh)[0];G=fl-fh
            assert G>=0;asserts+=1
            for e,d in enumerate(vecs):
                delta=hi[e]-lo[e]
                r=(d.T*Kl*d)[0];s=(d.T*Kh*d)[0]
                a2=(d.T*ul)[0]**2;b2=(d.T*uh)[0]**2
                assert 1-delta*s>0;asserts+=1
                assert r*(1-delta*s)>=s;asserts+=1
                endpoint_high=delta*a2/(1+delta*r)
                endpoint_low=delta*b2/(1-delta*s)
                score=min(endpoint_high,endpoint_low)
                for t in [sp.Rational(k,8) for k in range(9)]:
                    p=t*delta
                    gain=p*a2/(1+p*r)+(delta-p)*b2/(1-(delta-p)*s)
                    assert gain>=score;asserts+=1
                    ll=lo.copy();hh=hi.copy();ll[e]=hh[e]=lo[e]+p
                    newmax=(m.T*mat(ll).inv()*m)[0]
                    newmin=(m.T*mat(hh).inv()*m)[0]
                    newgap=newmax-newmin
                    worst_ratio=max(fl/(fh+endpoint_low),(fl-endpoint_high)/fh)
                    assert newmax/newmin<=worst_ratio;asserts+=1
                    assert sp.cancel(newgap-(G-gain))==0;asserts+=1
            for _ in range(8):
                cc=[l+(h-l)*sp.Rational(rng.randint(0,8),8) for l,h in zip(lo,hi)]
                ff=(m.T*mat(cc).inv()*m)[0]
                assert fh<=ff<=fl;asserts+=1;completions+=1
            cases+=1
    result={'cases':cases,'exact_assertions':asserts,'sampled_rational_completions':completions,
            'seconds':time.perf_counter()-st,'status':'PASS',
            'scope':'Finite exact checks supplement the proof, not an exhaustive proof or external review.'}
    print(result)
    with open(str(ROOT / 'exact_checks.json'),'w') as f:json.dump(result,f,indent=2)

if __name__=='__main__':run()
