"""Exact FPT uniform sampler of valid binary-additive sunflower differences.
Input blocks are lists of binary linear functional masks. Runtime is
5**w * polynomial(explicit input size); merging identical systems is optional.
Only integer arithmetic and Python standard library are used.
"""
from itertools import product
from random import Random
from pathlib import Path
import json,time

def homogeneous_basis(rows):
    basis={}
    for row in rows:
        while row:
            p=row.bit_length()-1
            if p in basis:row^=basis[p]
            else:basis[p]=row;break
    # Unique reduced row-echelon form for merging identical constraint spaces.
    for p in sorted(basis):
        for q in sorted(basis):
            if q>p and basis[q]>>p&1:basis[q]^=basis[p]
    return tuple(basis[p]for p in sorted(basis,reverse=True))

def affine_count(basis,n,prefix):
    pivots={row.bit_length()-1:(row,0)for row in basis}
    for i,bit in enumerate(prefix):
        row=1<<i;rhs=bit
        while row:
            p=row.bit_length()-1
            if p in pivots:
                old,oldrhs=pivots[p];row^=old;rhs^=oldrhs
            else:pivots[p]=(row,rhs);break
        if not row and rhs:return 0
    return 1<<(n-len(pivots))

class Sampler:
    def __init__(self,m,blocks):
        self.m=m;self.blocks=blocks;self.expanded_terms=5**len(blocks)
        block_terms=[]
        for rows in blocks:
            assert all(0<=r<1<<m for r in rows)
            u=tuple(rows);v=tuple(r<<m for r in rows);s=tuple(r^(r<<m)for r in rows)
            block_terms.append([(1,()),(-1,u),(-1,v),(-1,s),(3,u+v)])
        merged={}
        for choices in product(*block_terms):
            coeff=1;rows=[]
            for c,rs in choices:coeff*=c;rows.extend(rs)
            basis=homogeneous_basis(rows);merged[basis]=merged.get(basis,0)+coeff
        self.terms=[(c,b)for b,c in merged.items()if c]
        self.total=self.count(())
        assert 1<=self.total<=4**m
    def count(self,prefix):
        assert len(prefix)<=2*self.m
        count=sum(c*affine_count(b,2*self.m,prefix)for c,b in self.terms)
        assert count>=0
        return count
    def unrank(self,index):
        assert 0<=index<self.total
        prefix=[];n=self.total
        for _ in range(2*self.m):
            n0=self.count(prefix+[0]);assert 0<=n0<=n
            bit=int(index>=n0)
            if bit:index-=n0
            prefix.append(bit);n=n-n0 if bit else n0
            assert n>0
        assert n==1 and index==0
        z=sum(b<<i for i,b in enumerate(prefix));mask=(1<<self.m)-1
        return z&mask,z>>self.m
    def draw(self,rng):
        return self.unrank(rng.randrange(self.total))
    def valid(self,u,v):
        def image(rows,x):return sum(((x&r).bit_count()&1)<<j for j,r in enumerate(rows))
        return all((a==b==0)or(a!=0 and b!=0 and a!=b)
                   for a,b in ((image(rows,u),image(rows,v))for rows in self.blocks))

def replay():
    rng=Random(20261010);counts=0;prefixes=0;draws=0;exp_terms=0
    for m in range(4):
        for w in range(4):
            for rep in range(5):
                blocks=[[rng.randrange(1<<m)for _ in range(rng.randrange(m+2))]for _ in range(w)]
                S=Sampler(m,blocks);exp_terms+=S.expanded_terms
                C=[u|(v<<m)for u in range(1<<m)for v in range(1<<m)if S.valid(u,v)]
                assert S.total==len(C);counts+=1
                assert {u|(v<<m) for u,v in (S.unrank(i) for i in range(S.total))}==set(C)
                for k in range(2*m+1):
                    for bits in product((0,1),repeat=k):
                        z=sum(b<<i for i,b in enumerate(bits));mask=(1<<k)-1
                        assert S.count(bits)==sum(t&mask==z for t in C);prefixes+=1
                for _ in range(10):
                    u,v=S.draw(rng);assert S.valid(u,v);draws+=1
    # Large alphabets: exact product formula, without enumerating the code.
    m=30;blocks=[[1<<i for i in range(j*10,(j+1)*10)]for j in range(3)]
    S=Sampler(m,blocks);expected=(4**10-3*2**10+3)**3
    assert S.total==expected
    for _ in range(5):
        u,v=S.draw(rng);assert S.valid(u,v);draws+=1
    return {'seed':20261010,'small_cases':counts,'prefix_counts_exhaustively_checked':prefixes,'uniform_algorithm_draws_validated':draws,'small_expanded_terms':exp_terms,'large_case':{'m':m,'w':3,'output_ranks':[10,10,10],'count':S.total,'expected_count':expected,'expanded_terms':S.expanded_terms,'merged_nonzero_terms':len(S.terms)},'scope':'Exact prefix counts and exhaustive small-case unranking images validate the implementation; finite sampling frequencies are not used as a uniformity proof. Algorithm proof is in RESULT.md.'}
if __name__=='__main__':
    t=time.time();r=replay();r['seconds']=time.time()-t
    Path(__file__).with_name('fpt_sampler_results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
