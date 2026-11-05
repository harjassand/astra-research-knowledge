"""BDL Sec.3.2.2 ell=3 combinatorial diagnostic, no geometry claim."""
from dataclasses import dataclass
from collections import defaultdict
import random,json,argparse
@dataclass
class Tanner:
    nx:int
    nq:int
    nz:int
    xq:list
    qz:list
    faces:list
    def dual(self):
        return Tanner(self.nz,self.nq,self.nx,[(z,q) for q,z in self.qz],[(q,x) for x,q in self.xq],[(z,q,x,p) for x,q,z,p in self.faces])
    def columns(self,s):
        a=[0]*(self.nx if s=='X' else self.nz)
        for c,q in (self.xq if s=='X' else [(z,q) for q,z in self.qz]):a[c]^=1<<q
        return a
    def validate(self):
        a,b=self.columns('X'),self.columns('Z')
        assert all((x&z).bit_count()%2==0 for x in a for z in b)
        pairs=defaultdict(list);ex=set(self.xq);ez=set(self.qz)
        for x,q,z,p in self.faces:
            assert (x,q) in ex and (x,p) in ex and (q,z) in ez and (p,z) in ez
            pairs[x,z].extend([q,p])
        for x,u in enumerate(a):
            for z,v in enumerate(b):
                common=u&v
                assert sorted(pairs[x,z])==bits(common)
        return [self.nx,self.nq,self.nz,rank(a),rank(b)]
def bits(v):
    a=[]
    while v:
        p=v&-v;a.append(p.bit_length()-1);v^=p
    return a
def base():
    return Tanner(2,5,2,[(0,0),(0,1),(0,2),(1,2),(1,3),(1,4)],[(0,0),(2,0),(3,0),(1,1),(2,1),(4,1)],[(0,0,0,2),(0,1,1,2),(1,2,0,3),(1,2,1,4)])
def rank(cols):
    p={}
    for v in cols:
        while v:
            k=v.bit_length()-1
            if k in p:v^=p[k]
            else:p[k]=v;break
    return len(p)
def basis_reduce(cols,order):
    piv={};ids=[];coeff={};out=[0]*len(cols)
    for i in order:
        v=cols[i];c=0
        while v:
            p=v.bit_length()-1
            if p in piv:v^=piv[p];c^=coeff[p]
            else:
                k=len(ids);ids.append(i);piv[p]=v;coeff[p]=c^(1<<k);c=1<<k;break
        out[i]=c
    return ids,out
def fano_search(cols,tries=1000,seed=0):
    rng=random.Random(seed)
    for attempt in range(tries):
        order=list(range(len(cols)));rng.shuffle(order);ids,cs=basis_reduce(cols,order)
        if len(ids)<3:return None
        keep=sorted(rng.sample(range(len(ids)),3));b={}
        for i,v in enumerate(cs):
            p=sum(((v>>k)&1)<<j for j,k in enumerate(keep))
            if p:b.setdefault(p,i)
        if len(b)==7:return dict(attempt=attempt,contract=[i for j,i in enumerate(ids) if j not in keep],retain=[b[p] for p in range(1,8)],projection_columns=list(range(1,8)),basis=ids,kept_basis_positions=keep)
    return None
def rx(T):
    xqs=defaultdict(list);qzs=defaultdict(list);xfs=defaultdict(list)
    for x,q in T.xq:xqs[x].append(q)
    for q,z in T.qz:qzs[q].append(z)
    for f in T.faces:xfs[f[0]].append(f)
    X={};Q={};Z={};ex=[];ez=[];fs=[];qlocal={}
    def idx(d,k):
        if k not in d:d[k]=len(d)
        return d[k]
    def vv(v,b):return (v,b)
    def ee(u,v,b):return ('layer',tuple(sorted((u,v))),b)
    def br(v):return ('bridge',v)
    for x in range(T.nx):
        root=('x',x);qs=[('q',q) for q in xqs[x]]
        be={tuple(sorted((('q',q),('z',z)))) for q in xqs[x] for z in qzs[q]}
        bv={v for e in be for v in e};vs={root}|bv
        edges={tuple(sorted((root,q))) for q in qs}|be
        yv=[vv(v,b) for v in sorted(vs) for b in (0,1)]
        ye={ee(*e,b):(vv(e[0],b),vv(e[1],b)) for e in sorted(edges) for b in (0,1)}
        ye.update({br(v):(vv(v,0),vv(v,1)) for v in sorted(bv)})
        yf={}
        for fi,(_,q,z,p) in enumerate(xfs[x]):
            cyc=[root,('q',q),('z',z),('q',p)]
            for b in (0,1):yf['layerface',fi,b]=[ee(cyc[j],cyc[(j+1)%4],b) for j in range(4)]
        for u,v in sorted(be):yf['sideface',(u,v)]=[ee(u,v,0),br(v),ee(u,v,1),br(u)]
        for v in yv:idx(X,(x,v))
        for e,ends in ye.items():
            qi=idx(Q,('x',x,e))
            for v in ends:ex.append((idx(X,(x,v)),qi))
        for f,es in yf.items():
            zi=idx(Z,('x',x,f));inc=defaultdict(list)
            for e in es:
                qi=idx(Q,('x',x,e));ez.append((qi,zi))
                for v in ye[e]:inc[v].append(qi)
            for v,qq in inc.items():
                assert len(qq)==2
                fs.append((idx(X,(x,v)),qq[0],zi,qq[1]))
    for q in range(T.nq):
        root=('q',q);zs=[('z',z) for z in qzs[q]]
        yv=[vv(v,b) for v in [root]+zs for b in (0,1)]
        ye={ee(root,z,b):(vv(root,b),vv(z,b)) for z in zs for b in (0,1)}
        ye.update({br(z):(vv(z,0),vv(z,1)) for z in zs});qlocal[q]=(yv,ye)
        for v in yv:idx(Q,('q',q,v))
        for e,ends in ye.items():
            zi=idx(Z,('q',q,e))
            for v in ends:ez.append((idx(Q,('q',q,v)),zi))
    for z in range(T.nz):
        for b in (0,1):idx(Z,('z',z,b))
    for x,q in T.xq:
        vs,es=qlocal[q]
        for v in vs:ex.append((idx(X,(x,v)),idx(Q,('q',q,v))))
        for e,ends in es.items():
            qi=idx(Q,('x',x,e));zi=idx(Z,('q',q,e));ez.append((qi,zi))
            for v in ends:fs.append((idx(X,(x,v)),qi,zi,idx(Q,('q',q,v))))
    for q,z in T.qz:
        for b in (0,1):ez.append((idx(Q,('q',q,vv(('z',z),b))),idx(Z,('z',z,b))))
    for x,q,z,p in T.faces:
        for b in (0,1):fs.append((idx(X,(x,vv(('z',z),b))),idx(Q,('q',q,vv(('z',z),b))),idx(Z,('z',z,b)),idx(Q,('q',p,vv(('z',z),b)))))
    assert len(ex)==len(set(ex)) and len(ez)==len(set(ez))
    result=Tanner(len(X),len(Q),len(Z),ex,ez,fs)
    result.xlabels=list(X);result.qlabels=list(Q);result.zlabels=list(Z)
    return result
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--depth',type=int,default=2);ap.add_argument('--tries',type=int,default=300);a=ap.parse_args();T=base()
    for d in range(a.depth+1):
        print('level',d,'dimensions/ranks',T.validate(),flush=True)
        for s in ['X','Z']:
            cert=fano_search(T.columns(s),a.tries)
            print('sector',s,'fano',None if cert is None else {k:v for k,v in cert.items() if k not in ['basis','contract']},flush=True)
            if cert:
                cert.update(level=d,sector=s)
                with open(f'exchange_work/sampler_route/fano_level{d}_{s}.json','w') as f:json.dump(cert,f,indent=2)
        if d<a.depth:T=rx(T) if d%2==0 else rx(T.dual()).dual()
if __name__=='__main__':main()
