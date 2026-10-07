"""Exact finite diagnostics of the transfer, NOT an FPRAS or quantum circuit."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, random

class G:
    def __init__(self, r=0, i=0): self.r,self.i=F(r),F(i)
    def __add__(self,b):
        b=b if isinstance(b,G) else G(b);return G(self.r+b.r,self.i+b.i)
    __radd__=__add__
    def __neg__(self):return G(-self.r,-self.i)
    def __sub__(self,b):return self+-b
    def __mul__(self,b):
        b=b if isinstance(b,G) else G(b)
        return G(self.r*b.r-self.i*b.i,self.r*b.i+self.i*b.r)
    __rmul__=__mul__
    def conj(self):return G(self.r,-self.i)
    def norm(self):return self.r*self.r+self.i*self.i
    def __truediv__(self,b):
        b=b if isinstance(b,G) else G(b)
        z=self*b.conj();return G(z.r/b.norm(),z.i/b.norm())
    def __bool__(self):return bool(self.r or self.i)
    def __eq__(self,b):return isinstance(b,G) and self.r==b.r and self.i==b.i

def det(a):
    a=[row[:] for row in a];z=G(1);n=len(a)
    for j in range(n):
        k=next((k for k in range(j,n) if a[k][j]),None)
        if k is None:return G()
        if k!=j:a[j],a[k]=a[k],a[j];z=-z
        p=a[j][j];z=z*p
        for k in range(j+1,n):
            q=a[k][j]/p
            for l in range(j+1,n):a[k][l]=a[k][l]-q*a[j][l]
    return z

def gram_det(a,x):
    r=len(a[0]);return det([[sum((a[t][i].conj()*a[t][j]*x[t] for t in range(len(a))),G()) for j in range(r)] for i in range(r)])

def amplitude(a,b):return det([a[2*i+b[i]] for i in range(len(b))])
def fsum(p,h):return sum(v for x,v in p.items() if x[:len(h)]==h)

def check_tree(p,seed):
    rng=random.Random(seed);n=len(next(iter(p)));eta=F(1,50);B=F(0);q={():F(1)}
    for d in range(n):
        nxt={}
        for h,qp in q.items():
            cs=[fsum(p,h+(b,)) for b in [0,1]];ph=sum(cs)
            bad=bool(rng.randrange(5)==0)
            if ph and bad:B+=ph
            est=[]
            for c in cs:
                if not c:est.append(F(0))
                elif bad:est.append(c*F(rng.choice([0,1,100]),1))
                else:est.append(c*(1+rng.choice([-1,1])*eta))
            if not sum(est):
                est=[F(bool(c)) for c in cs]
            if not sum(est):est=[F(1),F(1)]
            for b in [0,1]:nxt[h+(b,)]=qp*est[b]/sum(est)
        q=nxt
    tv=sum(abs(p.get(x,0)-v) for x,v in q.items())/2
    assert tv<=2*n*eta+B,(tv,B)
    assert all(not v or p.get(x,0)>0 for x,v in q.items())
    return tv,B

def main():
    rng=random.Random(691026);identity=0;observables=0;trees=0;worst=F(0)
    for n in [2,3,4]:
      for trial in range(8):
        a=[[G(rng.randrange(-2,3),rng.randrange(-2,3)) for j in range(n)] for i in range(2*n)]
        amps={b:amplitude(a,b) for b in product([0,1],repeat=n)}
        Z=sum(v.norm() for v in amps.values())
        # Independent squarefree coefficient extraction: total degree is 2n.
        coef=G()
        for x in product([0,1],repeat=2*n):
            g=1
            for i in range(n):g*=x[2*i]+x[2*i+1]
            if g:coef+=gram_det(a,x)*(g*((-1)**(2*n-sum(x))))
        assert coef==G(Z),(n,trial,Z,coef.r,coef.i)
        identity+=1
        if not Z:continue
        p={b:v.norm()/Z for b,v in amps.items()}
        # Explicit Hermitian two-site exchange plus diagonal spin terms.
        def oa(b):
            z=amps[b]*F(1 if b[0]==b[1] else -1,4)
            if b[0]!=b[1]:
                c=(b[1],b[0])+b[2:];z+=amps[c]*F(1,2)
            return z
        target=sum((v.conj()*oa(b) for b,v in amps.items()),G())/G(Z)
        estimate=sum((G(p[b])*(oa(b)/v) for b,v in amps.items() if v),G())
        second=sum(p[b]*(oa(b)/v).norm() for b,v in amps.items() if v)
        assert estimate==target
        assert second<=F(9,16) # Operator norm <=3/4.
        observables+=1
        for seed in range(20):
            tv,B=check_tree(p,seed);trees+=1;worst=max(worst,tv)
    # Explicit zero projection despite rank-one spin factors.
    zero=[[G(1),G(0)],[G(0),G(1)],[G(0),G(0)],[G(0),G(0)]]
    assert all(not amplitude(zero,b) for b in product([0,1],repeat=2))
    out={'scope':'Exact finite transfer diagnostics; no source FPRAS/circuit execution',
         'determinant_coefficient_identities':identity,'complex_local_estimator_identities':observables,
         'shared_tape_conditional_tree_inequalities':trees,'largest_tree_TV':str(worst),
         'zero_projection_rank_counterexample':True}
    Path(__file__).with_name('DIAGNOSTICS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
