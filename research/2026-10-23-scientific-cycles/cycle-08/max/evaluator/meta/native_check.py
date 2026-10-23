"""Independent exact native-word check of the anisotropic receiving problem.

No owner or receiver implementation is imported. Fractions are exact; this
finite check corroborates the all-length proof but does not replace it.
"""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from math import comb
from pathlib import Path
import argparse, hashlib, json, resource, time

def waterfill(p):
    order=sorted(range(len(p)),key=lambda i:p[i],reverse=True)
    for s in range(2,len(p)+1):
        active=order[:s]
        c=F(s-1)/sum((1/p[i] for i in active),F(0))
        if c<=min(p[i] for i in active) and all(p[i]<=c for i in order[s:]):
            z=[max(F(0),1-c/x) for x in p]
            assert sum(z)==1
            f=sum(x*(1-y)**2 for x,y in zip(p,z))
            return c,z,f
    raise AssertionError('active set not found')

def formula(p,k):
    a=2*(1-sum(x*x for x in p))
    c,z,b=waterfill(p)
    C=sum((F((k-1-n)*comb(n,n//2),2**n) for n in range(0,k-1,2)),F(0))
    N=F(k*(k-1),2)
    return a*(N-C)/4+b*C/2,c,z,b,C

def toggle(a,b,i):
    a=list(a); b=list(b)
    for j in list(range(i+1))+list(range(i-1,-1,-1)):
        if a[j]==0:
            a[j]=b.pop(0)
        else:
            b.insert(0,a[j]); a[j]=0
    return tuple(a),tuple(b)

def native_g1(d,k):
    inputs=list(product(range(d+1),repeat=k))
    baths=list(product(range(1,d+1),repeat=k))
    ai={a:i for i,a in enumerate(inputs)}
    bi={b:i for i,b in enumerate(baths)}
    terms=defaultdict(int)
    # Additional bath colors avoid any reflecting cutoff/root boundary.
    # Every retained charge-preserving term must restore this entire buffer.
    tail=(1,)*(4*k+2)
    for x,a in enumerate(inputs):
        for u,b in enumerate(baths):
            initial=b+tail
            for j in range(k):
                ap,bp=toggle(a,initial,j)
                plus=(a[j]==0)
                for i in range(k):
                    # C_- C_+ - C_+ C_- in actual chronological order.
                    if (ap[i]!=0) != plus: continue
                    ao,bo=toggle(ap,bp,i)
                    assert len(bo)==len(initial) and bo[k:]==tail
                    terms[(ai[ao],bi[bo[:k]],x,u)]+=1 if plus else -1
    terms={key:v for key,v in terms.items() if v}
    for (y,v,x,u),n in terms.items():
        assert terms.get((x,u,y,v),0)==n
        assert sum(t!=0 for t in inputs[x])==sum(t!=0 for t in inputs[y])
    return inputs,baths,terms

def contract(inputs,terms,zeta):
    h=defaultdict(F)
    for (y,v,x,u),n in terms.items():
        h[y,x]+=n*zeta.get((u,v),F(0))
    k=len(inputs[0])
    for x,a in enumerate(inputs):
        h[x,x]+=2*sum(t!=0 for t in a)-k
    h={key:v for key,v in h.items() if v}
    for (y,x),v in h.items(): assert h.get((x,y),F(0))==v
    return h

def weights(inputs,p):
    result=[]
    for a in inputs:
        w=F(1)
        for v in a: w*=F(1,2) if v==0 else p[v-1]/2
        result.append(w)
    assert sum(result)==1
    return result

def objective(h,w):
    return sum((w[x]*v*h[x,y] for (y,x),v in h.items()),F(0))

def check(p,k):
    d=len(p); inputs,baths,g=native_g1(d,k); w=weights(inputs,p)
    value,c,z,b,C=formula(p,k)
    zeta={}
    for j,bath in enumerate(baths):
        if len(set(bath))==1 and z[bath[0]-1]: zeta[j,j]=z[bath[0]-1]
    h=contract(inputs,g,zeta)
    assert objective(h,w)==value
    assert all(w[x]==w[y] for y,x in h)
    t=defaultdict(F)
    for (y,v,x,u),n in g.items():
        t[v,u]+=w[x]*h.get((x,y),F(0))*n
    t={key:v for key,v in t.items() if v}
    assert all(v==u for v,u in t)
    gaps=[t.get((u,u),F(0))-value for u in range(len(baths))]
    assert min(gaps)>=0
    assert all(gaps[u]==0 for u,v in zeta)
    # Three exact competing states: maximally mixed, coherent product,
    # and nonproduct GHZ with real amplitudes. Full complex scope is analytic.
    n=len(baths)
    uniform={(u,u):F(1,n) for u in range(n)}
    coherent={(u,v):F(1,n) for u in range(n) for v in range(n)}
    pure_indices=[u for u,bath in enumerate(baths) if len(set(bath))==1]
    ghz={(u,v):F(1,d) for u in pure_indices for v in pure_indices}
    scores={}
    noncommuting=False
    for name,zz in [('mixed',uniform),('coherent_product',coherent),('ghz',ghz)]:
        hh=contract(inputs,g,zz); vv=objective(hh,w)
        assert vv>=value
        scores[name]=str(vv)
        noncommuting |= any(w[y]!=w[x] for y,x in hh)
    return {'d':d,'k':k,'p':list(map(str,p)),'c':str(c),'z':list(map(str,z)),
            'v':str(value),'collision':str(C),'one_color_minimum':str(b),
            'dual_min_gap':str(min(gaps)),'dual_max_gap':str(max(gaps)),
            'dual_is_scalar':max(gaps)==0,'coherent_noncommutation_seen':noncommuting,
            'competitor_scores':scores,'port_dimension':len(inputs),
            'prefix_dimension':len(baths),'g1_nonzeros':len(g)}

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    args=parser.parse_args(); start=time.perf_counter(); cpu=time.process_time()
    psets=[(F(4,5),F(3,20),F(1,20)),(F(1,2),F(1,3),F(1,6)),
           (F(9,10),F(1,10)),(F(3,5),F(1,5),F(1,5)),(F(1,2),F(1,2))]
    records=[check(p,k) for p in psets for k in (2,3)]
    out={'status':'PASS','method':'independent exact native toggle commutator, no source imports',
         'records':records,'wall_seconds':time.perf_counter()-start,
         'cpu_seconds':time.process_time()-cpu,
         'peak_rss_native_units':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'scope':'finite exact corroboration; not all-length proof or discovery-speed evidence',
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','wall_seconds','cpu_seconds','peak_rss_native_units']}))

if __name__=='__main__':main()
