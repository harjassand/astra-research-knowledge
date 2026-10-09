#!/usr/bin/env python3
"""Finite exact diagnostic of v1's intrinsic maps, not a good-code test.

Toy cells are a product of two-vertex, three-parallel-edge graphs. The source
global strict-intersection/mixing hypotheses are not asserted for this toy.
It tests the local array algebra under independently chosen nonorthogonal
F_2 stalk bases, including the L=2 homology chase and arbitrary noisy input.
Only the Python standard library is used.
"""
import argparse
import itertools
import json
import random
from pathlib import Path


def apply(rows, x):
    return sum(((r & x).bit_count() & 1) << i for i, r in enumerate(rows))


def compose(a, b):
    out = []
    for row in a:
        value = 0
        for j in range(len(b)):
            if row >> j & 1:
                value ^= b[j]
        out.append(value)
    return out


def inverse(rows):
    n = len(rows)
    z = [r | (1 << (n+i)) for i, r in enumerate(rows)]
    for j in range(n):
        q = next(i for i in range(j, n) if z[i] >> j & 1)
        z[j], z[q] = z[q], z[j]
        for i in range(n):
            if i != j and z[i] >> j & 1:
                z[i] ^= z[j]
    assert [v & ((1 << n)-1) for v in z] == [1 << i for i in range(n)]
    return [v >> n for v in z]


def transpose(rows, ncol):
    return [sum(((r >> j) & 1) << i for i, r in enumerate(rows))
            for j in range(ncol)]


def random_gl(n, rng):
    rows = [1 << i for i in range(n)]
    if n > 1:
        for _ in range(5*n):
            i, j = rng.sample(range(n), 2)
            if rng.randrange(2):
                rows[i] ^= rows[j]
            else:
                rows[i], rows[j] = rows[j], rows[i]
    inverse(rows)
    return rows


def xor(*arrays):
    out = {}
    for a in arrays:
        for pair, val in a.items():
            out[pair] = out.get(pair, 0) ^ val
            if not out[pair]:
                del out[pair]
    return out


def weight(a):
    return len({f for f, _ in a})


class ImageSection:
    """Linear right inverse on the image, projected linear extension outside."""
    def __init__(self, columns):
        self.basis = {}
        self.kernel = []
        for i, col in enumerate(columns):
            y, x = col, 1 << i
            while y:
                pivot = y.bit_length()-1
                if pivot in self.basis:
                    b, pre = self.basis[pivot]
                    y, x = y ^ b, x ^ pre
                else:
                    self.basis[pivot] = (y, x)
                    break
            if not y:
                self.kernel.append(x)

    def lift(self, y):
        x = 0
        for pivot in sorted(self.basis, reverse=True):
            if y >> pivot & 1:
                b, pre = self.basis[pivot]
                y, x = y ^ b, x ^ pre
        return x

    def contains(self, y):
        for pivot in sorted(self.basis, reverse=True):
            if y >> pivot & 1:
                y ^= self.basis[pivot][0]
        return y == 0


class Toy:
    def __init__(self, t, seed):
        self.t = t
        self.rng = random.Random(seed)
        self.faces = sorted(itertools.product(range(5), repeat=t))
        self.level = {d: [f for f in self.faces if self.degree(f)==d]
                      for d in range(t+1)}
        self.dim = {f: 1 << (t-self.degree(f)) for f in self.faces}
        self.above = {f: {p: [u for u in self.level[p] if self.leq(f,u)]
                          for p in range(self.degree(f), t+1)} for f in self.faces}
        self.up = {f: self.above[f].get(self.degree(f)+1, []) for f in self.faces}
        self.down = {u: [f for f in self.level.get(self.degree(u)-1, [])
                         if self.leq(f,u)] for u in self.faces}
        self.gauge = {f: random_gl(self.dim[f], self.rng) for f in self.faces}
        self.gauge_inv = {f: inverse(q) for f,q in self.gauge.items()}
        self.rt = {}
        for f in self.faces:
            inactive = [i for i in range(t) if f[i] < 2]
            for u in self.up[f]:
                j = next(i for i in range(t) if f[i] != u[i])
                other = [i for i in inactive if i != j]
                erow = (1,2,3)[u[j]-2]
                ref = []
                for outidx in range(self.dim[u]):
                    row = 0
                    for b in range(2):
                        if erow >> b & 1:
                            idx = 0
                            for a,i in enumerate(inactive):
                                bit = b if i==j else ((outidx >> other.index(i)) & 1)
                                idx |= bit << a
                            row |= 1 << idx
                    ref.append(row)
                actual = compose(self.gauge_inv[u], compose(ref, self.gauge[f]))
                self.rt[u,f] = transpose(actual, self.dim[f])
        self.sections = {}
        self.ksections = {}
        for f in self.faces:
            r = self.degree(f)
            for p in range(r,t):
                cols=[]
                for u in self.above[f][p+1]:
                    for bit in range(self.dim[u]):
                        cols.append(self.pack(f,p,self.T({(f,u):1<<bit})))
                self.sections[f,p] = ImageSection(cols)
            top = self.sections.get((f,t-1))
            if top is None:
                # At a top anchor there are no equations, and K is its full stalk.
                kernel = [1]
            else:
                kernel = top.kernel
            self.ksections[f] = ImageSection(kernel)
        cols=[]
        for u in self.level[2]:
            for bit in range(self.dim[u]):
                cols.append(self.pack_global(1,self.B({u:1<<bit})))
        self.boundaries = ImageSection(cols)

    @staticmethod
    def degree(f):
        return sum(a>=2 for a in f)

    @staticmethod
    def leq(f,u):
        return all(a==b if b<2 else (a<2 or a==b) for a,b in zip(f,u))

    def pack(self,f,p,a):
        value=offset=0
        for u in self.above[f][p]:
            value |= a.get((f,u),0) << offset
            offset += self.dim[u]
        return value

    def unpack(self,f,p,value):
        out={}
        for u in self.above[f][p]:
            x=value & ((1<<self.dim[u])-1)
            if x: out[f,u]=x
            value >>= self.dim[u]
        assert value==0
        return out

    def pack_global(self,p,a):
        value=offset=0
        for f in self.level[p]:
            value |= a.get(f,0) << offset
            offset += self.dim[f]
        return value

    def T(self,a):
        out={}
        for (f,u),x in a.items():
            for v in self.down[u]:
                if self.leq(f,v):
                    out=xor(out,{(f,v):apply(self.rt[u,v],x)})
        return out

    def Delta(self,a):
        out={}
        for (f,u),x in a.items():
            for g in self.up[f]:
                if self.leq(g,u): out=xor(out,{(g,u):x})
        return out

    def H(self,a):
        out={}
        for (f,u),x in a.items():
            active=[i for i in range(self.t) if u[i]>=2]
            for pos,i in enumerate(active):
                if f[i]>=2 and all(f[j]==0 for j in active[:pos]):
                    for labels in itertools.product(range(2),repeat=pos):
                        g=list(f); g[i]=1
                        for j,b in zip(active[:pos],labels): g[j]=b
                        out=xor(out,{(tuple(g),u):x})
        return out

    def P(self,a):
        if not a or self.degree(next(iter(a))[0])>0: return {}
        return self.copy(self.J(a))

    def J(self,a):
        out={}
        for u in {u for _,u in a}:
            v=tuple(0 if x>=2 else x for x in u)
            x=a.get((v,u),0)
            if x: out[u]=x
        return out

    def copy(self,e):
        return {(v,u):x for u,x in e.items() for v in self.level[0]
                if self.leq(v,u) and x}

    def B(self,e):
        out={}
        for u,x in e.items():
            for f in self.down[u]:
                val=out.get(f,0)^apply(self.rt[u,f],x)
                if val: out[f]=val
                elif f in out: del out[f]
        return out

    def lift(self,a,r,p):
        out={}
        for f in self.level[r]:
            x=self.pack(f,p,a)
            if x: out=xor(out,self.unpack(f,p+1,self.sections[f,p].lift(x)))
        return out

    def Kproject(self,a,r):
        out={}
        for f in self.level[r]:
            sec=self.ksections[f]
            x=self.pack(f,self.t,a)
            y=0
            for pivot in sorted(sec.basis,reverse=True):
                if x>>pivot&1:
                    b,_=sec.basis[pivot]; x^=b; y^=b
            out=xor(out,self.unpack(f,self.t,y))
        return out

    def randomK(self,r):
        out={}
        for f in self.level[r]:
            sec=self.ksections[f]
            x=0
            for b,_ in sec.basis.values():
                if self.rng.randrange(2): x^=b
            out=xor(out,self.unpack(f,self.t,x))
        assert not self.T(out)
        return out

    def forward(self,y,k):
        g=[self.lift(self.copy(y),0,k-1)]
        for r in range(1,self.t-k+1):
            g.append(self.lift(self.Delta(g[-1]),r,k+r-1))
        return g,self.Kproject(self.Delta(g[-1]),self.t-k+1)

    def reverse(self,g,topcorrection,k):
        a=xor(g[-1],topcorrection)
        for r in range(len(g)-2,-1,-1):
            a=xor(g[r],self.T(self.H(a)))
        return self.J(a)

    def clean_top_error(self,e,g,k):
        x=self.copy(e)
        for r in range(self.t-k):
            z=self.lift(xor(g[r],x),r,k+r)
            assert self.T(z)==xor(g[r],x)
            x=self.Delta(z)
        c=xor(g[-1],x)
        assert not self.T(c)
        assert self.Delta(c)==self.Delta(g[-1])
        return c

    def basis_arrays(self):
        for p in range(self.t+1):
            for r in range(p+1):
                for u in self.level[p]:
                    for f in self.level[r]:
                        if self.leq(f,u):
                            for bit in range(self.dim[u]):
                                yield r,p,{(f,u):1<<bit}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--t',type=int,default=3)
    ap.add_argument('--seed',type=int,default=640210)
    ap.add_argument('--trials',type=int,default=64)
    ap.add_argument('--output',default=None)
    args=ap.parse_args()
    toy=Toy(args.t,args.seed)
    checks={"array_basis_vectors":0,"homology_trials":0,"noise_trials":0}
    for r,p,a in toy.basis_arrays():
        assert not toy.T(toy.T(a))
        assert not toy.Delta(toy.Delta(a))
        assert toy.T(toy.Delta(a))==toy.Delta(toy.T(a))
        assert xor(toy.Delta(toy.H(a)),toy.H(toy.Delta(a)))==xor(a,toy.P(a))
        checks['array_basis_vectors']+=1
    k=args.t-2 if args.t>=4 else 1
    L=args.t-k
    for _ in range(args.trials):
        e={f:toy.rng.randrange(1<<toy.dim[f]) for f in toy.level[k]}
        e={f:x for f,x in e.items() if x}
        g,s=toy.forward(toy.B(e),k)
        c=toy.clean_top_error(e,g,k)
        assert s==toy.Delta(c)
        q=toy.randomK(L-1)
        corrected=xor(c,toy.Delta(q))
        f=toy.reverse(g,corrected,k)
        residual={u:e.get(u,0)^f.get(u,0) for u in toy.level[k]}
        residual={u:x for u,x in residual.items() if x}
        # B_{k+1} boundary basis: t=3,k=1 uses precomputed B2; t=4,k=2 builds B3.
        if k==1:
            boundaries=toy.boundaries
        else:
            cols=[]
            for u in toy.level[k+1]:
                for bit in range(toy.dim[u]):
                    cols.append(toy.pack_global(k,toy.B({u:1<<bit})))
            boundaries=ImageSection(cols)
        assert boundaries.contains(toy.pack_global(k,residual))
        checks['homology_trials']+=1
        m={f:toy.rng.randrange(1<<toy.dim[f]) for f in toy.level[k-1]}
        m={f:x for f,x in m.items() if x}
        y={u:toy.B(e).get(u,0)^m.get(u,0) for u in toy.level[k-1]}
        y={u:x for u,x in y.items() if x}
        gn,sn=toy.forward(y,k)
        D=3*args.t; cm=1<<(k-1)
        for r in range(L+1):
            assert weight(xor(gn[r],g[r]))<=cm*(D**r)*len(m)
        assert weight(xor(sn,s))<=cm*(D**(L+1))*len(m)
        # An assumed K-decoder output with an explicit residual w. This is not
        # an operational decoder test; it isolates the reverse transport map.
        w=toy.randomK(L) if m else {}
        noisycorrection=xor(corrected,w)
        fn=toy.reverse(gn,noisycorrection,k)
        alphaK=len({a for a,_ in w})/max(1,len(m))
        H=(4*3)**args.t; G=(2*3)**args.t
        bound=G*cm*(sum((H*D)**r for r in range(L))
                    +(H*D)**L*(1+alphaK*D))*len(m)
        assert len({u for u in toy.level[k] if fn.get(u,0)!=f.get(u,0)})<=bound
        checks['noise_trials']+=1
    result={"status":"PASS","scope":"finite intrinsic-array algebra only",
            "t":args.t,"k":k,"seed":args.seed,"n_i":3,
            "independently_nonorthogonal_stalk_bases":True,
            "good_qLTC_or_global_expansion_validated":False,**checks}
    print(json.dumps(result,indent=2))
    if args.output: Path(args.output).write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__': main()
