from itertools import product
from collections import defaultdict
from fractions import Fraction
import json
from pathlib import Path

class DSU:
    def __init__(self,n): self.p=list(range(n));self.s=[0]*n;self.ok=True
    def find(self,x):
        if self.p[x]!=x:
            y=self.p[x];r,q=self.find(y);self.s[x]^=q;self.p[x]=r
        return self.p[x],self.s[x]
    def add(self,x,y,p):
        rx,sx=self.find(x);ry,sy=self.find(y)
        if rx==ry:
            if sx^sy!=p:self.ok=False
        else:
            self.p[rx]=ry;self.s[rx]=sx^sy^p
    def components(self):return len({self.find(i)[0] for i in range(len(self.p))})

def trace(n,edges,word,erase=False):
    d=DSU(n*(len(edges)+1))
    for k,((i,j),q) in enumerate(zip(edges,word)):
        pre=lambda z:k*n+z
        post=lambda z:(k+1)*n+z
        for z in range(n):
            if z not in (i,j):d.add(pre(z),post(z),0)
        if q=='a':
            d.add(pre(i),post(i),0);d.add(pre(j),post(j),0)
        elif q=='c':
            d.add(pre(i),pre(j),not erase);d.add(post(i),post(j),not erase)
        elif q=='d':
            d.add(pre(i),post(j),not erase);d.add(pre(j),post(i),not erase)
    for z in range(n):d.add(z,len(edges)*n+z,0)
    loops=d.components()
    return (2**loops if d.ok else 0),loops

edges=[(0,1),(0,2),(1,2)]
true=defaultdict(int); erased=defaultdict(int);bad=[]
rows=[]
for word in product('acd',repeat=3):
    q,L=trace(3,edges,word);q0,L0=trace(3,edges,word,True)
    assert L==L0
    monomial=tuple(word.count(z) for z in 'acd')
    true[monomial]+=q;erased[monomial]+=q0
    if not q:bad.append(''.join(word))
    rows.append({'word':''.join(word),'loops':L,'trace':q,'erased_trace':q0})
coeff={'a':Fraction(1),'c':Fraction(1,4),'d':Fraction(3,4)}
Z=sum(Fraction(r['trace'])*__import__('functools').reduce(lambda x,z:x*coeff[z],r['word'],Fraction(1)) for r in rows)
Z0=sum(Fraction(r['erased_trace'])*__import__('functools').reduce(lambda x,z:x*coeff[z],r['word'],Fraction(1)) for r in rows)
result={'triangle_edges':edges,'weights':{k:str(v) for k,v in coeff.items()},'true_polynomial':{str(k):v for k,v in true.items()},'erased_polynomial':{str(k):v for k,v in erased.items()},'frustrated_words':bad,'Z':str(Z),'Z_erased':str(Z0),'acceptance':str(Z/Z0),'rows':rows,'acceptance_100_triangles_float':float(Z/Z0)**100}
Path('work/agents/epr_parity/results/triangle_projection.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__ == "__main__":print(json.dumps(result,indent=2))
