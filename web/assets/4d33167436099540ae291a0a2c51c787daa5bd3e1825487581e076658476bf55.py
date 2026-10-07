"""Exact determinant-squared parity contraction on an acquired support ordering.

No external packages. Complex rationals are represented by Fraction pairs;
the DP runs over Gaussian integers after common-denominator clearing.
This is an exact exponential-frontier algorithm, not a general parity FPRAS.
"""
from fractions import Fraction
from itertools import combinations
from collections import defaultdict
from math import lcm
import random

ZERO=(0,0)
ONE=(1,0)

def ga(a,b): return (a[0]+b[0],a[1]+b[1])
def gm(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def gc(a): return (a[0],-a[1])
def gs(a,t): return (a[0]*t,a[1]*t)

def qr(v):
    if isinstance(v,tuple): return (Fraction(v[0]),Fraction(v[1]))
    return (Fraction(v),Fraction(0))

def qdiv(a,b):
    den=b[0]*b[0]+b[1]*b[1]
    return ((a[0]*b[0]+a[1]*b[1])/den,(a[1]*b[0]-a[0]*b[1])/den)

def determinant(M):
    a=[[qr(x) for x in row] for row in M]
    n=len(a); ans=qr(1)
    for p in range(n):
        j=next((j for j in range(p,n) if a[j][p] != (0,0)),None)
        if j is None: return qr(0)
        if j!=p:
            a[p],a[j]=a[j],a[p]; ans=gs(ans,-1)
        pivot=a[p][p]; ans=gm(ans,pivot)
        for j in range(p+1,n):
            fac=qdiv(a[j][p],pivot)
            for h in range(p+1,n): a[j][h]=ga(a[j][h],gs(gm(fac,a[p][h]),-1))
    return ans

class FrontierParity:
    def __init__(self,F,activities=None,order=None):
        self.n=len(F)
        if any(len(row)!=self.n for row in F): raise ValueError('square F required')
        self.order=list(range(self.n)) if order is None else list(order)
        if sorted(self.order)!=list(range(self.n)): raise ValueError('order must be permutation')
        raw=[[qr(F[i][j]) for j in self.order] for i in self.order]
        den=1
        for row in raw:
            for x in row:
                den=lcm(den,x[0].denominator,x[1].denominator)
        self.Fden=den
        self.G=[[(int(x[0]*den),int(x[1]*den)) for x in row] for row in raw]
        aa=[Fraction(1) for _ in range(self.n)] if activities is None else [Fraction(activities[i]) for i in self.order]
        if len(aa)!=self.n or any(x<0 for x in aa): raise ValueError('nonnegative activities required')
        aden=1
        for x in aa: aden=lcm(aden,x.denominator)
        self.Aden=aden; self.A=[int(x*aden) for x in aa]
        self.neighbors=[[] for _ in range(self.n)]
        for i in range(self.n):
            for j in range(i+1,self.n):
                if self.G[i][j]!=ZERO or self.G[j][i]!=ZERO: self.neighbors[i].append(j)
        self.boundaries=[]
        for i in range(self.n):
            self.boundaries.append({v for u in range(i+1) for v in self.neighbors[u] if v>i})
        self.width=max(map(len,self.boundaries),default=0)
        self.stats={}

    def _open(self,v,label,layer_mask,other_mask,row_mask):
        # Pending endpoints all lie to the right of v. Insert one future
        # endpoint. Crossings with older edges are exactly old ends < new end.
        for j in self.neighbors[v]:
            bit=1<<j
            if layer_mask&bit: continue
            want_row=(label==-1)
            union=layer_mask|other_mask
            if union&bit and bool(row_mask&bit)!=want_row: continue
            z=self.G[v][j] if label==1 else gs(self.G[j][v],-1)
            if z==ZERO: continue
            crossings=(layer_mask&((1<<j)-1)).bit_count()
            z=gs(z,-1 if crossings%2 else 1)
            rr=(row_mask|bit) if want_row else (row_mask&~bit)
            yield layer_mask|bit,rr,z

    def integer_partition(self,k,allowed=None):
        if k<0 or 2*k>self.n: return 0
        allowed={} if allowed is None else allowed
        allowed={v:tuple(vals) for v,vals in allowed.items()}
        if any(v<0 or v>=self.n or any(a not in (-1,0,1) for a in vals) for v,vals in allowed.items()):
            raise ValueError('bad allowed labels')
        # a,b are pending endpoint masks for the two matchings. r encodes
        # row type on their union; all other pending sites have column type.
        current={(0,0,0,0):ONE}
        peak=1; transitions=0
        for v in range(self.n):
            nxt=defaultdict(lambda:ZERO); bit=1<<v
            for (a,b,r,q),weight in current.items():
                ia=bool(a&bit); ib=bool(b&bit)
                labels=(1 if r&bit else -1,) if ia or ib else (0,1,-1)
                labels=tuple(x for x in labels if x in allowed.get(v,(-1,0,1)))
                aa=a&~bit; bb=b&~bit; rr=r&~bit
                for label in labels:
                    qq=q+(label==1)
                    if qq>k: continue
                    if label==0:
                        key=(aa,bb,rr,qq); nxt[key]=ga(nxt[key],weight); transitions+=1
                        continue
                    if label==1 and self.A[v]==0: continue
                    left=((aa,rr,ONE),) if ia else self._open(v,label,aa,bb,rr)
                    for aaa,rrr,za in left:
                        right=((bb,rrr,ONE),) if ib else self._open(v,label,bb,aaa,rrr)
                        for bbb,rrrr,zb in right:
                            key=(aaa,bbb,rrrr,qq)
                            term=gm(weight,gm(za,gc(zb)))
                            if label==1: term=gs(term,self.A[v])
                            nxt[key]=ga(nxt[key],term); transitions+=1
            current={key:val for key,val in nxt.items() if val!=ZERO}
            peak=max(peak,len(current))
        value=current.get((0,0,0,k),ZERO)
        if value[1]!=0 or value[0]<0: raise ArithmeticError(('nonreal/negative norm',value))
        self.stats={'width':self.width,'peak_states':peak,'transitions':transitions,
                    'weight_bits':value[0].bit_length()}
        return value[0]

    def partition(self,k,allowed=None):
        return Fraction(self.integer_partition(k,allowed),(self.Fden*self.Fden*self.Aden)**k)

    def point_weight(self,I,J):
        if len(I)!=len(J) or set(I)&set(J): return Fraction(0)
        z=determinant([[self.G[i][j] for j in J] for i in I])
        ans=z[0]*z[0]+z[1]*z[1]
        for i in I: ans*=self.A[i]
        return ans/Fraction((self.Fden*self.Fden*self.Aden)**len(I))

    def sample(self,k,rng=None,allowed=None,max_bit_trials=None):
        """Expected finite fair-random-bit exact self-reduction.

        rng.randrange/getrandbits are assumed uniform ideal random primitives.
        With max_bit_trials=R, every run is bounded, and its TV error is at
        most n*2**(-R) by coupling to the uncapped exact rejection sampler.
        The implementation repeats exact DP; no signed DP edge is sampled.
        Returns site labels and original paired-line row set / auxiliary col set.
        """
        rng=random.SystemRandom() if rng is None else rng
        fixed={} if allowed is None else {v:tuple(vals) for v,vals in allowed.items()}
        total=self.integer_partition(k,fixed)
        if total==0: raise ValueError('zero sector')
        labels=[]; fallback_events=0; random_bits=0
        for v in range(self.n):
            options=[]
            for a in fixed.get(v,(-1,0,1)):
                child=dict(fixed); child[v]=(a,)
                z=self.integer_partition(k,child)
                options.append((a,z))
            if sum(z for a,z in options)!=total: raise AssertionError('self reduction mass mismatch')
            if max_bit_trials is None:
                draw=rng.randrange(total)
            else:
                if max_bit_trials<1: raise ValueError('positive random-bit trial cap required')
                nbits=(total-1).bit_length()
                draw=None
                for _ in range(max_bit_trials):
                    candidate=rng.getrandbits(nbits); random_bits+=nbits
                    if candidate<total:
                        draw=candidate;break
                if draw is None:
                    # Choose an acquired positive branch on rare random-bit
                    # failure. This yields a bounded program, TV loss bounded
                    # by n*2**(-max_bit_trials), not exact conditional success.
                    fallback_events+=1;draw=0
            chosen=None
            for a,z in options:
                if draw<z: chosen=a; total=z; break
                draw-=z
            if chosen is None: raise AssertionError('categorical selection failed')
            fixed[v]=(chosen,); labels.append(chosen)
        I=tuple(self.order[i] for i,a in enumerate(labels) if a==1)
        J=tuple(self.order[i] for i,a in enumerate(labels) if a==-1)
        return {'labels_ordered':tuple(labels),'I':I,'J':J,'fallback_events':fallback_events,'charged_random_bits':random_bits if max_bit_trials is not None else 'UNKNOWN'}

def brute(F,k,activities=None,allowed=None):
    n=len(F); aa=[Fraction(1)]*n if activities is None else list(map(Fraction,activities))
    allowed={} if allowed is None else allowed
    result=Fraction(0)
    for I in combinations(range(n),k):
        for J in combinations([x for x in range(n) if x not in I],k):
            labels={x:(1 if x in I else -1 if x in J else 0) for x in range(n)}
            if any(labels[v] not in vals for v,vals in allowed.items()): continue
            z=determinant([[F[i][j] for j in J] for i in I])
            w=z[0]*z[0]+z[1]*z[1]
            for i in I: w*=aa[i]
            result+=w
    return result
