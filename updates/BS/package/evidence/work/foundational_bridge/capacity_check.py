"""Exact finite audit of subdivision deletion and capacity charge.

All partition values are independently computed by path-run enumeration,
followed by a sum-product DP enforcing that each terminal is used once.
No source formulas for deletion factors are used by that partition oracle.
Capacity is independently maximized over every pairing of each small set.
"""
from fractions import Fraction as F
from itertools import combinations
from functools import lru_cache
from random import Random
import json
from pathlib import Path

rng = Random(20261010)

def closure(matrix):
    b = [row[:] for row in matrix]
    for k in range(len(b)):
        for i in range(len(b)):
            for j in range(i):
                b[i][j] = b[j][i] = max(b[i][j], min(b[i][k],b[k][j]))
    return b

def phi(b, U):
    @lru_cache(None)
    def go(u):
        if not u: return F(1)
        x, rest = u[0],u[1:]
        return max(b[x][y]*go(rest[:j]+rest[j+1:]) for j,y in enumerate(rest))
    return go(tuple(sorted(U)))

class Model:
    def __init__(self,n,K,activities):
        self.n=n; self.p=2*K+2
        self.lam={e:F(a) for e,a in zip(combinations(range(n),2),activities)}
        raw=[[F(1) for _ in range(n)] for _ in range(n)]
        for (u,v),a in self.lam.items(): raw[u][v]=raw[v][u]=max(1,a)
        self.b=closure(raw); h=[max(row) for row in self.b]
        self.paths={}; self.C0=F(1); nextv=n
        for (u,v),a in self.lam.items():
            verts=[u]+list(range(nextv,nextv+4*self.p))+[v]
            nextv+=4*self.p
            t=[None]+[F(0)]*(4*self.p+1)
            for r in range(1,self.p+1):
                t[2*r-1]=t[2*r]=max(self.b[u][v],h[u]/(2**(r-1)))
                t[4*self.p+3-2*r]=t[4*self.p+2-2*r]=max(self.b[u][v],h[v]/(2**(r-1)))
            t[2*self.p+1]=a
            self.paths[u,v]=(verts,t)
            for j in range(2,4*self.p+2,2): self.C0*=t[j]
        self.N=nextv
        raw=[[F(1) for _ in range(nextv)] for _ in range(nextv)]
        for verts,t in self.paths.values():
            for j in range(1,len(verts)):
                raw[verts[j-1]][verts[j]]=raw[verts[j]][verts[j-1]]=max(F(1),t[j])
        self.bp=closure(raw)

    def logical(self,R,forbidden=()):
        R=set(R); forbidden=set(forbidden)
        def go(rem):
            if not rem:return F(1)
            x,rest=rem[0],rem[1:]
            return sum((self.lam[x,y]*go(rest[:j]+rest[j+1:]) for j,y in enumerate(rest) if (x,y) not in forbidden),F(0))
        return go(tuple(v for v in range(self.n) if v not in R))

    def independent_real(self,U):
        U=set(U); states={0:F(1)}
        for (u,v),(verts,t) in self.paths.items():
            alternatives=[]
            for occupancy in range(4):
                selected=set()
                if occupancy&1:selected.add(u)
                if occupancy&2:selected.add(v)
                if selected&U: continue
                present=[i for i,x in enumerate(verts) if x not in U and (i not in (0,len(verts)-1) or x in selected)]
                w=F(1); pos=0
                while pos<len(present):
                    end=pos+1
                    while end<len(present) and present[end]==present[end-1]+1:end+=1
                    if (end-pos)%2: w=F(0);break
                    for j in range(pos,end,2): w*=t[present[j+1]]
                    pos=end
                if w: alternatives.append((sum(1<<x for x in selected),w))
            new={}
            for mask,w in states.items():
                for other,vw in alternatives:
                    if not(mask&other):new[mask|other]=new.get(mask|other,F(0))+w*vw
            states=new
        target=sum(1<<x for x in range(self.n) if x not in U)
        return states.get(target,F(0))

    def factors(self,U):
        U=set(U); R=[x for x in U if x<self.n]; f=F(1); broken=[]
        for e,(verts,t) in self.paths.items():
            holes=[j for j in range(1,len(verts)-1) if verts[j] in U]
            if not holes:continue
            broken.append(e)
            assert all((b-a)%2 for a,b in zip(holes,holes[1:])), (U,holes)
            def strength(j):return t[j] if j<=2*self.p else t[j+1]
            if holes[0]%2==0:
                j=holes.pop(0);R.append(e[0])
                if j>2*self.p:f*=self.lam[e]/strength(j)
            if holes and holes[-1]%2==1:
                j=holes.pop();R.append(e[1])
                if j<=2*self.p:f*=self.lam[e]/strength(j)
            assert len(holes)%2==0
            for j,k in zip(holes[::2],holes[1::2]):
                assert j%2==1 and k%2==0
                if k<=2*self.p:f/=strength(j)
                elif j>2*self.p:f/=strength(k)
                else:f*=self.lam[e]/(strength(j)*strength(k))
        assert len(set(R))==len(R) and len(R)%2==0
        return R,f,broken

def check(model,sets,label):
    records={"label":label,"n":model.n,"K":(model.p-2)//2,"N":model.N,"activities":{str(e):str(a) for e,a in model.lam.items()},"sets_checked":0,"feasible_sets":0,"deletion_failures":0,"charge_failures":0,"max_charge_ratio":"0"}
    assert model.independent_real([])==model.C0*model.logical([])
    maxratio=F(0)
    for U in sets:
        records['sets_checked']+=1
        z=model.independent_real(U)
        if not z:continue
        records['feasible_sets']+=1
        R,f,broken=model.factors(U)
        predicted=model.C0*f*model.logical(R,broken)
        assert z==predicted, ('deletion_identity',U,z,predicted)
        ratio=f*phi(model.bp,U)/phi(model.b,R)
        assert ratio<=1, ('charge',U,R,f,ratio)
        maxratio=max(maxratio,ratio)
    records['max_charge_ratio']=str(maxratio)
    print(json.dumps(records),flush=True)
    return records

def sets_for(m,exhaustive=False):
    if exhaustive:
        for k in range(0,m.N+1,2):yield from combinations(range(m.N),k)
    else:
        yield ()
        yield from combinations(range(m.N),2)
        for k in (4,6,8):
            for _ in range(300):yield tuple(sorted(rng.sample(range(m.N),k)))

if __name__=='__main__':
    cases=[(2,0,['1/2'],True,'n2 K0 exhaustive'),
           (4,0,['1/8','1/2','1','1/4','1/2','1'],False,'n4 subunit'),
           (4,1,['4','1/8','1/2','2','1/4','1'],False,'n4 K1 nonuniform'),
           (4,2,['16','1/8','1/2','4','1/4','2'],False,'n4 K2 gradients')]
    out=[]
    for n,K,a,ex,label in cases:
        m=Model(n,K,a);out.append(check(m,sets_for(m,ex),label))
    path=Path(__file__).with_name('capacity_results.json')
    path.write_text(json.dumps({'exact_arithmetic':True,'seed':20261010,'records':out},indent=2)+'\n')
