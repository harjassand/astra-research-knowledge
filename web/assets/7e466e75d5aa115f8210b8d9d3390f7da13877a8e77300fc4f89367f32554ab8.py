"""Exact exterior-algebra Gaussian MPS acquisition and hard-parity contraction.

Field Q(i), no SVD/truncation, no coefficient oracle. Exponential in the
acquired ranks across the supplied site order. Every residual polynomial
is represented relative to an exact RREF basis of the cross row span.
"""
from fractions import Fraction
from pathlib import Path
import sys, random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from frontier_sampler import qr,ga,gm,gc,gs,qdiv

ZERO=qr(0);ONE=qr(1)

def clean(d):return {key:v for key,v in d.items() if v!=ZERO}

def rref(rows,ncols):
    a=[[qr(x) for x in row] for row in rows]
    pivots=[];r=0
    for c in range(ncols):
        j=next((j for j in range(r,len(a)) if a[j][c]!=ZERO),None)
        if j is None:continue
        a[r],a[j]=a[j],a[r]
        z=a[r][c];a[r]=[qdiv(v,z) for v in a[r]]
        for j in range(len(a)):
            if j==r or a[j][c]==ZERO:continue
            z=a[j][c];a[j]=[ga(a[j][h],gs(gm(z,a[r][h]),-1)) for h in range(ncols)]
        pivots.append(c);r+=1
        if r==len(a):break
    return a[:r],pivots

def wedge_sign(a,b):
    inv=sum((b&((1<<j)-1)).bit_count() for j in range(a.bit_length()) if a>>j&1)
    return -1 if inv%2 else 1

def wedge(x,y):
    result={}
    for a,ca in x.items():
        for b,cb in y.items():
            if a&b:continue
            m=a|b;term=gs(gm(ca,cb),wedge_sign(a,b))
            result[m]=ga(result.get(m,ZERO),term)
    return clean(result)

def add(x,y):
    z=dict(x)
    for m,c in y.items():z[m]=ga(z.get(m,ZERO),c)
    return clean(z)

def scale(x,c):return clean({m:gm(a,c) for m,a in x.items()})
def parity(x):return {m:gs(c,-1 if m.bit_count()%2 else 1) for m,c in x.items()}
def linear(row):return {1<<j:qr(c) for j,c in enumerate(row) if c!=ZERO}

def compose(second,first):
    # Sparse columns of second @ first.
    out=[]
    for col in first:
        current={}
        for mid,c in col.items():current=add(current,scale(second[mid],c))
        out.append(current)
    return out

class RankParity:
    def __init__(self,F,activities=None,order=None):
        self.n=len(F);self.order=list(range(self.n)) if order is None else list(order)
        if sorted(self.order)!=list(range(self.n)):raise ValueError('permutation required')
        self.F=[[qr(F[i][j]) for j in self.order] for i in self.order]
        self.activities=[Fraction(1)]*self.n if activities is None else [Fraction(activities[i]) for i in self.order]
        if any(a<0 for a in self.activities):raise ValueError('nonnegative activities required')
        self.m=2*self.n
        K=[[ZERO for _ in range(self.m)] for _ in range(self.m)]
        for i in range(self.n):
            for j in range(self.n):
                K[2*i][2*j+1]=self.F[i][j]
                K[2*j+1][2*i]=gs(self.F[i][j],-1)
        self.K=K;self.bases=[];self.pivots=[]
        for p in range(self.m+1):
            B,cols=rref([row[p:] for row in K[:p]],self.m-p)
            self.bases.append(B);self.pivots.append(cols)
        self.ranks=[len(B) for B in self.bases]
        self.mode_transfers=[]
        for p in range(self.m):
            B=self.bases[p];C=self.bases[p+1];pivs=self.pivots[p+1]
            beta=[row[0] for row in B]
            T=[[row[1:][j] for j in pivs] for row in B]
            ell=[K[p][p+1:][j] for j in pivs]
            # Explicitly verify every coordinate reconstruction: no rank
            # factor or solver pivot is used as unverified data.
            for a,row in enumerate(B):
                reconstructed=[]
                for j in range(self.m-p-1):
                    z=ZERO
                    for t,c in zip(T[a],C):z=ga(z,gm(t,c[j]))
                    reconstructed.append(z)
                if reconstructed!=row[1:]:raise AssertionError('basis transition mismatch')
            reconstructed=[]
            for j in range(self.m-p-1):
                z=ZERO
                for t,c in zip(ell,C):z=ga(z,gm(t,c[j]))
                reconstructed.append(z)
            if reconstructed!=K[p][p+1:]:raise AssertionError('new edge form mismatch')
            zero=[];one=[];ellpoly=linear(ell)
            for mask in range(1<<len(B)):
                p0={0:ONE};p1={};old_degree=0
                for a in range(len(B)):
                    if not (mask>>a&1):continue
                    tpoly=linear(T[a])
                    next_p1=add(wedge(p1,tpoly),scale(p0,gs(beta[a],-1 if old_degree%2 else 1)))
                    p0=wedge(p0,tpoly);p1=next_p1;old_degree+=1
                zero.append(p0)
                one.append(add(p1,wedge(parity(p0),ellpoly)))
            self.mode_transfers.append((zero,one))
        self.tensors=[]
        for i in range(self.n):
            first=self.mode_transfers[2*i];second=self.mode_transfers[2*i+1]
            self.tensors.append({0:compose(second[0],first[0]),
                                 1:compose(second[0],first[1]),
                                -1:compose(second[1],first[0])})
        self.stats={}

    def amplitude(self,labels):
        v={0:ONE}
        for i,s in enumerate(labels):
            vv={}
            for old,c in v.items():vv=add(vv,scale(self.tensors[i][s][old],c))
            v=vv
        return v.get(0,ZERO)

    def partition(self,k,allowed=None):
        allowed={} if allowed is None else allowed
        if k<0 or 2*k>self.n:return Fraction(0)
        current={(0,0,0):ONE};peak=1;transitions=0
        for i in range(self.n):
            nxt={}
            for (a,b,q),v in current.items():
                for label in allowed.get(i,(-1,0,1)):
                    qq=q+(label==1)
                    if qq>k:continue
                    activity=self.activities[i] if label==1 else Fraction(1)
                    for aa,c in self.tensors[i][label][a].items():
                        for bb,d in self.tensors[i][label][b].items():
                            key=(aa,bb,qq)
                            term=gs(gm(v,gm(c,gc(d))),activity)
                            nxt[key]=ga(nxt.get(key,ZERO),term);transitions+=1
            current=clean(nxt);peak=max(peak,len(current))
        ans=current.get((0,0,k),ZERO)
        if ans[1] or ans[0]<0:raise ArithmeticError(('nonnegative norm violated',ans))
        self.stats={'max_site_cross_rank':max(self.ranks[::2],default=0),
                    'max_mode_cross_rank':max(self.ranks,default=0),
                    'peak_norm_states':peak,'norm_transitions':transitions}
        return ans[0]

    def sample(self,k,rng=None,allowed=None,max_bit_trials=None):
        rng=random.SystemRandom() if rng is None else rng
        fixed={} if allowed is None else {v:tuple(a) for v,a in allowed.items()}
        total=self.partition(k,fixed)
        if not total:raise ValueError('zero sector')
        labels=[];fallback=0;bits=0
        for i in range(self.n):
            options=[]
            for a in fixed.get(i,(-1,0,1)):
                child={**fixed,i:(a,)}
                options.append((a,self.partition(k,child)))
            if sum(z for a,z in options)!=total:raise AssertionError('prefix norm mismatch')
            from math import lcm
            den=1
            for a,z in options:den=lcm(den,z.denominator)
            weights=[(a,int(z*den)) for a,z in options]
            mass=sum(w for a,w in weights)
            if max_bit_trials is None:draw=rng.randrange(mass)
            else:
                if max_bit_trials<1:raise ValueError('positive bit cap required')
                nb=(mass-1).bit_length();draw=None
                for _ in range(max_bit_trials):
                    t=rng.getrandbits(nb);bits+=nb
                    if t<mass:draw=t;break
                if draw is None:draw=0;fallback+=1
            for a,w in weights:
                if draw<w:
                    chosen=a;break
                draw-=w
            fixed[i]=(chosen,);labels.append(chosen)
            total=next(z for a,z in options if a==chosen)
        return {'labels_ordered':tuple(labels),'I':tuple(self.order[i] for i,a in enumerate(labels) if a==1),
                'J':tuple(self.order[i] for i,a in enumerate(labels) if a==-1),
                'fallback_events':fallback,'charged_random_bits':bits if max_bit_trials is not None else 'UNKNOWN'}
