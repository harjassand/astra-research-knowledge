"""Exact classical circuit-spec acquisition for positive rational open chains.
No quantum gate backend; no exponential source-state table. Inputs are onsite
factors u_i[bit] and nearest-neighbor factors v_i[left][right]."""
from fractions import Fraction as F
from dataclasses import dataclass
import json


def rat(x):
    if isinstance(x, bool) or not isinstance(x, (int, str, F)):
        raise ValueError('factors must be exact integers, rational strings or Fractions')
    try:
        q=F(x)
    except (ValueError, ZeroDivisionError):
        raise ValueError('invalid rational factor') from None
    if q<=0: raise ValueError('factors must be strictly positive')
    return q


def checked_inputs(onsite, edges):
    if not isinstance(onsite,(list,tuple)) or not onsite:
        raise ValueError('nonempty onsite factor list required')
    if any(not isinstance(row,(list,tuple)) or len(row)!=2 for row in onsite):
        raise ValueError('each onsite factor must have two entries')
    u=tuple(tuple(rat(v) for v in row) for row in onsite)
    if not isinstance(edges,(list,tuple)) or len(edges)!=len(u)-1:
        raise ValueError('open chain requires exactly n-1 edges')
    e=[]
    for mat in edges:
        if not isinstance(mat,(list,tuple)) or len(mat)!=2 or any(not isinstance(row,(list,tuple)) or len(row)!=2 for row in mat):
            raise ValueError('each edge must be a 2x2 factor')
        e.append(tuple(tuple(rat(v) for v in row) for row in mat))
    return u,tuple(e)


def ceil_fraction(x): return (x.numerator+x.denominator-1)//x.denominator


def ceil_log2_positive(x):
    """For rational x>=1, smallest integer l with 2^l>=x."""
    if x<1: raise ValueError('x>=1 required')
    l=max(0,x.numerator.bit_length()-x.denominator.bit_length())
    while (1<<l)*x.denominator<x.numerator: l+=1
    while l and (1<<(l-1))*x.denominator>=x.numerator: l-=1
    return l


@dataclass(frozen=True)
class Color:
    site:int
    direction:int
    upper:F
    delta:F


class ThresholdSource:
    def __init__(self, onsite, edges):
        self.u,self.e=checked_inputs(onsite,edges)
        self.n=len(self.u)
        self.neighbors=tuple(tuple(j for j in (i-1,i+1) if 0<=j<self.n) for i in range(self.n))
        self.rates={}
        colors=[]
        Ri=[]
        for i in range(self.n):
            maxima=[]
            for b in (0,1):
                vals=[]
                for context in range(1<<len(self.neighbors[i])):
                    x=b<<i
                    for j,neighbor in enumerate(self.neighbors[i]):
                        x|=((context>>j)&1)<<neighbor
                    ratio=self.ratio_flip(x,i)
                    rate=ratio/(1+ratio)
                    self.rates[i,b,context]=rate; vals.append(rate)
                levels=sorted(set(vals)); prev=F(0)
                for level in levels:
                    colors.append(Color(i,b,level,level-prev)); prev=level
                maxima.append(levels[-1])
            Ri.append(sum(maxima,F(0)))
        self.colors=tuple(colors); self.Ri=tuple(Ri); self.R=sum(Ri,F(0))
        assert self.n<=self.R<=2*self.n
        self._build_messages()
        self._build_return_certificate()

    def _label(self,x):
        if type(x) is not int or not 0<=x<(1<<self.n):
            raise ValueError('source label must be an n-bit integer')
        return x

    def _site(self,i):
        if type(i) is not int or not 0<=i<self.n: raise ValueError('invalid site')
        return i

    def ratio_flip(self,x,i):
        self._label(x); self._site(i)
        b=(x>>i)&1
        r=self.u[i][1-b]/self.u[i][b]
        if i: r*=self.e[i-1][(x>>(i-1))&1][1-b]/self.e[i-1][(x>>(i-1))&1][b]
        if i+1<self.n: r*=self.e[i][1-b][(x>>(i+1))&1]/self.e[i][b][(x>>(i+1))&1]
        return r

    def context(self,x,i):
        return sum(((x>>j)&1)<<k for k,j in enumerate(self.neighbors[i]))

    def map(self,color_index,x):
        self._label(x)
        if type(color_index) is not int or not 0<=color_index<len(self.colors):
            raise ValueError('invalid color index')
        c=self.colors[color_index]
        b=(x>>c.site)&1
        if b==c.direction and self.rates[c.site,b,self.context(x,c.site)]>=c.upper:
            return x^(1<<c.site)
        return x

    def column(self,x):
        """Fixed 2F slots, exact probabilities; no square-root backend assumed."""
        self._label(x)
        out=[]
        for f,c in enumerate(self.colors):
            for slot,y in enumerate((x,x^(1<<c.site))):
                p=F(0)
                if self.map(f,y)==x:
                    p=c.delta/self.R
                    if slot: p*=self.ratio_flip(x,c.site)
                out.append({'color':f,'slot':slot,'y':y,'probability':p})
        assert sum((row['probability'] for row in out),F(0))==1
        return out

    def _build_messages(self):
        n=self.n
        right=[[F(1),F(1)] for _ in range(n)]
        minright=[[F(1),F(1)] for _ in range(n)]
        for i in range(n-2,-1,-1):
            for b in (0,1):
                vals=[self.e[i][b][t]*self.u[i+1][t]*right[i+1][t] for t in (0,1)]
                right[i][b]=sum(vals,F(0))
                minright[i][b]=min(self.e[i][b][t]*self.u[i+1][t]*minright[i+1][t] for t in (0,1))
        self.right=tuple(tuple(row) for row in right)
        self.Z=sum((self.u[0][b]*right[0][b] for b in (0,1)),F(0))
        self.pi_min=min(self.u[0][b]*minright[0][b] for b in (0,1))/self.Z
        self.first=tuple(self.u[0][b]*right[0][b]/self.Z for b in (0,1))
        conditional=[]
        for i in range(1,n):
            conditional.append(tuple(tuple(self.e[i-1][prev][b]*self.u[i][b]*right[i][b]/right[i-1][prev] for b in (0,1)) for prev in (0,1)))
        self.conditional=tuple(conditional)

    def weight(self,x):
        self._label(x)
        v=F(1)
        for i in range(self.n):
            b=(x>>i)&1; v*=self.u[i][b]
            if i: v*=self.e[i-1][(x>>(i-1))&1][b]
        return v

    def probability(self,x): return self.weight(x)/self.Z

    def parity_mean(self,mask):
        """Exact source-diagonal Z-string expectation under pi."""
        self._label(mask)
        prev=[self.u[0][b]*(-1 if (mask&1) and b else 1) for b in (0,1)]
        for i in range(1,self.n):
            prev=[self.u[i][b]*(-1 if ((mask>>i)&1) and b else 1)*sum((prev[a]*self.e[i-1][a][b] for a in (0,1)),F(0)) for b in (0,1)]
        return sum(prev,F(0))/self.Z

    def sparse_parity_means(self,masks):
        return {mask:self.parity_mean(mask) for mask in dict.fromkeys(masks)}

    def _build_return_certificate(self):
        # c_ij is maximal conditional probability change at i when j flips.
        influences=[]; column=[F(0) for _ in range(self.n)]
        for i in range(self.n):
            for pos,j in enumerate(self.neighbors[i]):
                changes=[]
                for context in range(1<<len(self.neighbors[i])):
                    if (context>>pos)&1: continue
                    changes.append(abs(self.rates[i,0,context]-self.rates[i,0,context^(1<<pos)]))
                c=max(changes); column[j]+=c; influences.append((i,j,c))
        self.influences=tuple(influences)
        self.kappa=1-max(column)
        self.return_m=None
        if self.kappa>0:
            ell=ceil_log2_positive(F(16*self.n)/self.pi_min)
            self.return_m=ceil_fraction(self.R*ell/self.kappa)
            # (1-kappa/R)^m <= exp(-kappa*m/R) <= 2^-ell.
            assert F(self.kappa*self.return_m/self.R)>=ell
            assert (1<<ell)*self.pi_min>=16*self.n

    def specification(self,masks=()):
        """Serializable raw-input plus exact acquired data; not gate compilation."""
        return {'version':1,'n':self.n,
                'onsite':[[str(x) for x in row] for row in self.u],
                'edges':[[[str(x) for x in row] for row in mat] for mat in self.e],
                'R':str(self.R),'Ri':[str(x) for x in self.Ri],
                'colors':[{'site':c.site,'direction':c.direction,'upper':str(c.upper),'delta':str(c.delta),'weight':str(c.delta/self.R)} for c in self.colors],
                'first':[str(x) for x in self.first],
                'conditional':[[[str(x) for x in row] for row in mat] for mat in self.conditional],
                'pi_min':str(self.pi_min),'kappa':str(self.kappa),'return_m':self.return_m,
                'return_admitted':self.return_m is not None,
                'parity_means':{str(mask):str(v) for mask,v in self.sparse_parity_means(masks).items()},
                'scope':'exact classical circuit-spec acquisition; no executed quantum gates'}


def verify_spec(spec):
    """Reconstruct from raw factors; verifies algebraic record, not external truth."""
    try:
        if not isinstance(spec,dict) or type(spec.get('version')) is not int or spec.get('version')!=1: return False
        source=ThresholdSource(spec['onsite'],spec['edges'])
        masks=[int(x) for x in spec['parity_means']]
        if any(str(mask) not in spec['parity_means'] for mask in masks): return False
        return json.dumps(source.specification(masks),sort_keys=True,allow_nan=False)==json.dumps(spec,sort_keys=True,allow_nan=False)
    except (KeyError,ValueError,TypeError,ZeroDivisionError,OverflowError):
        return False
