"""Finite-response conditional elimination, with explicit local rates and sources.

All arithmetic inside eliminate() is rational when its input is Fraction-valued.
The response interval uses outward rational square-root brackets in exact mode.
No full many-body configurations are represented by this algorithm.
"""
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from itertools import product
import json
from pathlib import Path
import time

SPIN=(-1,1)

def tensor3(zero):
    return [[[zero for _ in range(2)] for _ in range(2)] for _ in range(2)]

@dataclass
class Chain:
    unary: list
    edge: list
    rate: list
    a: list
    b: list
    constant: object=0

    @property
    def n(self): return len(self.unary)

    def cond(self,i,left=0,right=0):
        w=[]
        for s in range(2):
            v=self.unary[i][s]
            if i: v*=self.edge[i-1][left][s]
            if i+1<self.n: v*=self.edge[i][s][right]
            w.append(v)
        total=sum(w)
        return [x/total for x in w]

    def marginals(self):
        n=self.n; one=self.unary[0][0]*0+1
        back=[[one,one] for _ in range(n)]
        for i in range(n-2,-1,-1):
            row=[sum(self.edge[i][s][t]*self.unary[i+1][t]*back[i+1][t]
                     for t in range(2)) for s in range(2)]
            scale=sum(row); back[i]=[x/scale for x in row]
        first=[self.unary[0][s]*back[0][s] for s in range(2)]
        norm=sum(first); marg=[[x/norm for x in first]]; trans=[]
        for i in range(n-1):
            tab=[]
            for s in range(2):
                row=[self.edge[i][s][t]*self.unary[i+1][t]*back[i+1][t] for t in range(2)]
                z=sum(row); tab.append([x/z for x in row])
            trans.append(tab)
            marg.append([sum(marg[-1][s]*tab[s][t] for s in range(2)) for t in range(2)])
        return marg,trans

    def mean_source(self):
        marg,tr=self.marginals()
        value=self.constant+sum(self.a[i]*sum(SPIN[s]*marg[i][s] for s in range(2)) for i in range(self.n))
        value+=sum(self.b[i]*sum(SPIN[s]*SPIN[t]*marg[i][s]*tr[i][s][t]
                                  for s,t in product(range(2),repeat=2)) for i in range(self.n-1))
        return value

def small_expansion(values,coordinates,zero):
    """Walsh coefficients of a function of at most two actual slow spins."""
    out={}
    for mask in range(1<<len(coordinates)):
        key=tuple(coordinates[j] for j in range(len(coordinates)) if (mask>>j)&1)
        out[key]=sum(value*prod_spin(bits,mask) for bits,value in values)/(1<<len(coordinates))
    return out

def prod_spin(bits,mask):
    s=1
    for j,b in enumerate(bits):
        if (mask>>j)&1:s*=SPIN[b]
    return s

def eliminate(chain):
    """Eliminate even positions; slow odd positions form the smaller chain.

    Returns the exact averaged model, b=<q,F^-1q>, c=<F^-1q,KS F^-1q>,
    and an acquired local theta satisfying B*F^-1 B <= theta A.
    """
    n=chain.n
    if n<3 or n%2==0: raise ValueError('Use odd lengths n=2^L-1 for complete recursion.')
    zero=chain.unary[0][0]*0; one=zero+1
    slow=list(range(1,n,2)); fast=list(range(0,n,2)); ns=len(slow)
    un=[list(chain.unary[i]) for i in slow]; edges=[]
    # Exact marginal equilibrium factors, integrating one fast spin per gap.
    for j in fast:
        if j==0:
            for s in range(2):
                un[0][s]*=sum(chain.unary[j][x]*chain.edge[j][x][s] for x in range(2))
        elif j==n-1:
            for s in range(2):
                un[-1][s]*=sum(chain.unary[j][x]*chain.edge[j-1][s][x] for x in range(2))
        else:
            tab=[[sum(chain.unary[j][x]*chain.edge[j-1][l][x]*chain.edge[j][x][r]
                      for x in range(2)) for r in range(2)] for l in range(2)]
            scale=max(max(row) for row in tab); edges.append([[x/scale for x in row] for row in tab])
    for row in un:
        scale=max(row); row[:]=[x/scale for x in row]
    coarse_rates=[]
    for k,i in enumerate(slow):
        tab=tensor3(zero)
        for l,c,r in product(range(2),repeat=3):
            pl=chain.cond(i-1,l if i>1 else 0,c)
            pr=chain.cond(i+1,c,r if i+2<n else 0)
            tab[l][c][r]=sum(pl[x]*pr[y]*chain.rate[i][x][c][y] for x,y in product(range(2),repeat=2))
        coarse_rates.append(tab)
    ca=[chain.a[i] for i in slow]; cb=[zero for _ in range(ns-1)]; cc=chain.constant
    # f=P f+q, retaining every unary/edge term. q is conditionally one-spin.
    for j in fast:
        coordinates=[]
        if j: coordinates.append((j-1)//2)
        if j+1<n: coordinates.append(j//2)
        vals=[]
        for bits in product(range(2),repeat=len(coordinates)):
            p=0; l=0; r=0
            if j: l=bits[p];p+=1
            if j+1<n:r=bits[p]
            probs=chain.cond(j,l,r); mean=probs[1]-probs[0]
            amp=chain.a[j]
            if j: amp+=chain.b[j-1]*SPIN[l]
            if j+1<n:amp+=chain.b[j]*SPIN[r]
            vals.append((bits,amp*mean))
        coeff=small_expansion(vals,coordinates,zero)
        cc+=coeff[()]
        for key,value in coeff.items():
            if len(key)==1:ca[key[0]]+=value
            elif len(key)==2:
                assert key[1]==key[0]+1
                cb[key[0]]+=value
    co=Chain(un,edges,coarse_rates,ca,cb,cc)
    marg,tr=co.marginals()

    def fast_data(j,l,r):
        probs=chain.cond(j,l,r); mean=probs[1]-probs[0]
        var=4*probs[0]*probs[1]
        gap=chain.rate[j][l][0][r]+chain.rate[j][l][1][r]
        amp=chain.a[j]
        if j:amp+=chain.b[j-1]*SPIN[l]
        if j+1<n:amp+=chain.b[j]*SPIN[r]
        return probs,mean,var,gap,amp

    b=zero
    for j in fast:
        for l,r in product(range(2),repeat=2):
            if j==0:
                if l:continue
                prob=marg[0][r]
            elif j==n-1:
                if r:continue
                prob=marg[-1][l]
            else:
                k=(j-1)//2;prob=marg[k][l]*tr[k][l][r]
            _,mean,var,gap,amp=fast_data(j,l,r)
            b+=prob*amp*amp*var/gap

    cfast=zero;theta=zero;localtheta=[]
    for k,i in enumerate(slow):
        thi=zero
        ls=range(2) if k else [0]
        rs=range(2) if k+1<ns else [0]
        for l,c,r in product(ls,range(2),rs):
            if k:
                prob=marg[k-1][l]*tr[k-1][l][c]
            else:prob=marg[k][c]
            if k+1<ns:prob*=tr[k][c][r]
            pl,ml,vl,gl,al=fast_data(i-1,l,c)
            pr,mr,vr,gr,ar=fast_data(i+1,c,r)
            pl2,ml2,vl2,gl2,al2=fast_data(i-1,l,1-c)
            pr2,mr2,vr2,gr2,ar2=fast_data(i+1,1-c,r)
            wbar=zero;covl=zero;covr=zero;covlr=zero;ce=zero
            for x,y in product(range(2),repeat=2):
                p=pl[x]*pr[y]; w=chain.rate[i][x][c][y]
                dl=SPIN[x]-ml;dr=SPIN[y]-mr
                wbar+=p*w;covl+=p*w*dl;covr+=p*w*dr;covlr+=p*w*dl*dr
                v=al*dl/gl+ar*dr/gr
                v2=al2*(SPIN[x]-ml2)/gl2+ar2*(SPIN[y]-mr2)/gr2
                ce+=p*w*(v-v2)**2/2
            # Singleton fast modes can be shared by two slow updates;
            # the pair mode occurs in only one neighborhood.
            dlcount=1 if i-1==0 else 2
            drcount=1 if i+1==n-1 else 2
            invvar=dlcount*covl*covl/(vl*gl)+drcount*covr*covr/(vr*gr)+covlr*covlr/(vl*vr*(gl+gr))
            thi=max(thi,2*invvar/wbar)
            cfast+=prob*ce
        localtheta.append(thi);theta=max(theta,thi)
    return co,dict(b=b,c=cfast,theta=theta,localtheta=localtheta)

def sqrt_upper(x,bits=100):
    if x<0: raise ValueError('Negative square-root argument')
    if isinstance(x,Fraction):
        scale=1<<bits
        floor=isqrt((x.numerator*scale*scale)//x.denominator)
        if floor*floor*x.denominator==x.numerator*scale*scale:return Fraction(floor,scale)
        return Fraction(floor+1,scale)
    return x**.5

def solve(chain,exact_sqrt_bits=160):
    levels=[];cur=chain
    while cur.n>1:
        co,data=eliminate(cur)
        data['n']=cur.n;levels.append(data);cur=co
    probs=cur.cond(0);var=4*probs[0]*probs[1]
    base=cur.a[0]**2*var/(cur.rate[0][0][0][0]+cur.rate[0][0][1][0])
    lower=upper=base
    for data in reversed(levels):
        b,c,theta=data['b'],data['c'],data['theta']
        cross=sqrt_upper(theta*upper*b,exact_sqrt_bits)
        residual=max(b-cross,b*0)
        lower=lower+(residual*residual/(b+c) if b+c else 0)
        upper=(1+theta)*upper+b+2*cross
        data['lower']=lower;data['upper']=upper
    return dict(lower=lower,upper=upper,base=base,levels=levels)

def v2(k):
    return (k & -k).bit_length()-1

def initial(n,sep=Fraction(1,10000),exact=False,source='magnetization',fields=True):
    if (n+1)&n:raise ValueError('n must be 2^L-1')
    cast=Fraction if exact else float
    one=cast(1);R=cast(n+1)
    un=[[one,one+(cast(1) if i%3 else -cast(1))/(2*n)] if fields else [one,one] for i in range(n)]
    ed=[[[R,one],[one,R]] for _ in range(n-1)]
    a=[one for _ in range(n)];b=[cast(0) for _ in range(n-1)]
    # Algebraic energy-like observable avoids logarithms in the exact backend.
    if source=='bonds':a=[cast(0) for _ in range(n)];b=[one for _ in range(n-1)]
    elif source=='mixed':b=[cast(1)/3 for _ in range(n-1)]
    out=Chain(un,ed,[],a,b,cast(0))
    for i in range(n):
        nu=cast(sep)**v2(i+1);tab=tensor3(cast(0))
        for l,c,r in product(range(2),repeat=3):
            if i and i+1<n:mult=one+cast(3)/10*SPIN[l]*SPIN[r]+cast(1)/5*SPIN[l]
            else:mult=one+cast(1)/5*SPIN[r if i==0 else l]
            tab[l][c][r]=nu*mult*out.cond(i,l,r)[1-c]
        out.rate.append(tab)
    out.constant=-out.mean_source()
    return out

def encode(x):
    if isinstance(x,Fraction):return {'numerator':str(x.numerator),'denominator':str(x.denominator),'float':float(x)}
    if isinstance(x,list):return [encode(y) for y in x]
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    return x

def summary(result):
    L,U=result['lower'],result['upper']
    return dict(lower=encode(L),upper=encode(U),relative_width=float((U-L)/L) if L else None,
                levels=[{'n':v['n'],'theta':float(v['theta']),'b':float(v['b']),'c':float(v['c'])} for v in result['levels']])

if __name__=='__main__':
    results=[]
    for n in [31,127,511,2047]:
        t=time.perf_counter();ch=initial(n)
        out=solve(ch)
        results.append(dict(n=n,source='total magnetization',sep=1e-4,fields=True,mode='float64 evaluation of proved enclosure',seconds=time.perf_counter()-t,**summary(out)))
        print(n,results[-1]['relative_width'],results[-1]['seconds'],flush=True)
    for n in [7,15]:
        t=time.perf_counter();ch=initial(n,exact=True,source='mixed')
        out=solve(ch)
        results.append(dict(n=n,source='magnetization plus one-third bond sum',sep='1/10000',fields=True,mode='exact rational local tables with outward rational square roots',seconds=time.perf_counter()-t,**summary(out)))
        print('exact',n,results[-1]['relative_width'],results[-1]['seconds'],flush=True)
    path=Path(__file__).with_name('conditional_response_results.json')
    path.write_text(json.dumps(results,indent=2)+'\n')
