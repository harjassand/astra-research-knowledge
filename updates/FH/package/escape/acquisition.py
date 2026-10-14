"""Energy interrogation with an explicit global pairwise model-class premise.
The graph/interaction coefficient is not supplied to the learner. Point probes
cannot themselves establish absence of higher-order terms; that is a premise.
"""
from fractions import Fraction as F
from itertools import combinations
import random,time,json,math
from collective_sector import CollectiveRing

class WeightOracle:
    def __init__(self,n,t,r=F(1),seed=17):
        order=list(range(n));random.Random(seed).shuffle(order)
        self.n=n;self._edges=[(order[i],order[(i+1)%n]) for i in range(n)]
        self._t=F(t);self._r=F(r);self.queries=[]
    def __call__(self,mask):
        # An exact Boltzmann-weight API is used to keep the synthetic algebra rational.
        # A physical energy oracle returns -log(weight) with finite error instead.
        matches=sum(((mask>>i)&1)==((mask>>j)&1) for i,j in self._edges)
        ans=self._r**mask.bit_count()*self._t**matches
        self.queries.append({'mask':str(mask),'weight':str(ans)})
        return ans

def acquire(n,oracle):
    w0=oracle(0); singles=[oracle(1<<i) for i in range(n)]
    adj=[[] for _ in range(n)];edge_square=[]
    for i,j in combinations(range(n),2):
        ratio=oracle((1<<i)|(1<<j))*w0/(singles[i]*singles[j])
        if ratio!=1:
            if ratio<1:raise ValueError('not a ferromagnetic interaction')
            adj[i].append(j);adj[j].append(i);edge_square.append(ratio)
    if not edge_square or len(set(edge_square))!=1 or any(len(a)!=2 for a in adj):
        raise ValueError('outside uniform cycle class')
    sq=edge_square[0];a=math.isqrt(sq.numerator);b=math.isqrt(sq.denominator)
    if a*a!=sq.numerator or b*b!=sq.denominator:raise ValueError('nonrational coupling: interval implementation required')
    t=F(a,b); rset={w*t*t/w0 for w in singles}
    if len(rset)!=1:raise ValueError('nonuniform site field')
    r=rset.pop()
    order=[0,adj[0][0]]
    while len(order)<n:
        new=next(x for x in adj[order[-1]] if x!=order[-2])
        if new in order:raise ValueError('disconnected cycles')
        order.append(new)
    if 0 not in adj[order[-1]]:raise ValueError('not a cycle')
    return {'n':n,'t':t,'r':r,'order':order,'edges':sum(len(a) for a in adj)//2}

def run_acquired(n,t,r=F(1),nu=F(1),kappa=F(1),seed=17):
    start=time.perf_counter();O=WeightOracle(n,F(t),F(r),seed);law=acquire(n,O);acq=time.perf_counter()
    if law['r']!=1:raise ValueError('hard-trap spectral certificate requires spin-reversal symmetry')
    R=CollectiveRing(n,law['t'],nu,kappa);out=R.run();end=time.perf_counter()
    out['energy_queries']=len(O.queries);out['energy_query_seconds']=acq-start
    out['end_to_end_seconds']=end-start;out['inferred_order']=law['order'];out['query_transcript']=O.queries
    out['model_class_premise']='globally pairwise, uniform ferromagnetic cycle with uniform field; heat-bath microscopic generator'
    return out
if __name__=='__main__':
    import sys
    out=run_acquired(int(sys.argv[1]),F(sys.argv[2]));json.dump(out,open(sys.argv[3],'w'))
    print(json.dumps({k:v for k,v in out.items() if k not in ['query_transcript','witness','lower_exact','upper_exact','inferred_order']}))
