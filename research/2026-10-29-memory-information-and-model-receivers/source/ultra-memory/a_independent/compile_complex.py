"""Exact binary replacement consumer for arXiv:2605.10943v1 §§3.2.2–6.

This constructs the total complex from doubled/subdivided local cell stars and
restriction maps.  It does not acquire the primary random geometric embedding.
Python integers are exact GF(2) vectors.  No source-program imports.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations
import argparse, json, time
from pathlib import Path


def basis(rows):
    b = {}
    for x in rows:
        while x:
            p = x.bit_length()-1
            if p in b: x ^= b[p]
            else:
                b[p] = x
                break
    return b


def reduce(x, b):
    while x:
        p = x.bit_length()-1
        if p not in b: return x
        x ^= b[p]
    return 0


def bits(x):
    while x:
        t = x & -x
        yield t.bit_length()-1
        x ^= t


def transpose(rows, n):
    out = [0]*n
    for i, x in enumerate(rows):
        for j in bits(x): out[j] |= 1 << i
    return out


@dataclass
class Code:
    n: int
    xs: list[int]
    zs: list[int]
    # faces use integer x, q, z, q labels of their respective vertex colors
    faces: list[tuple[int,int,int,int]]

    def dual(self):
        return Code(self.n, self.zs, self.xs,
                    [(z,q,x,r) for x,q,z,r in self.faces])

    def qualify(self):
        for x in self.xs:
            assert all((x&z).bit_count()%2 == 0 for z in self.zs)
        # Every shared qubit must occur in an allowed square; all source
        # consumers here retain the actual cancellation pairing, not all-pairs.
        covered = {}
        for x,q,z,r in self.faces:
            assert q != r and ((self.xs[x]&self.zs[z])>>q)&1
            assert ((self.xs[x]&self.zs[z])>>r)&1
            covered[x,z] = covered.get((x,z),0) | (1<<q) | (1<<r)
        assert all(covered.get((i,j),0) == x&z
                   for i,x in enumerate(self.xs) for j,z in enumerate(self.zs))
        return {"n":self.n,"X_checks":len(self.xs),"Z_checks":len(self.zs),
                "rank_X":len(basis(self.xs)),"rank_Z":len(basis(self.zs)),
                "logical_qubits":self.n-len(basis(self.xs))-len(basis(self.zs)),
                "faces":len(self.faces),"max_X_weight":max(map(int.bit_count,self.xs)),
                "max_Z_weight":max(map(int.bit_count,self.zs))}


def ordered(a,b): return tuple(sorted((a,b)))


def subdivided_vertex(face, i, j, t, fid):
    x,q,z,r = face
    vs = (("x",x),("q",q),("z",z),("q",r))
    if i==0 and j==0: return ("v",vs[0])
    if i==t and j==0: return ("v",vs[1])
    if i==t and j==t: return ("v",vs[2])
    if i==0 and j==t: return ("v",vs[3])
    if j==0: a,b,k=vs[0],vs[1],i
    elif i==t: a,b,k=vs[1],vs[2],j
    elif j==t: a,b,k=vs[3],vs[2],i
    elif i==0: a,b,k=vs[0],vs[3],j
    else: return ("f",fid,i,j)
    if b<a: a,b,k=b,a,t-k
    return ("e",a,b,k,t)


def edge_subdivision(a,b,t):
    if b<a: a,b=b,a
    return [("v",a)]+[("e",a,b,k,t) for k in range(1,t)]+[("v",b)]


def double(vertices,edges,faces,bverts,bedges):
    v = {(s,x) for s in (0,1) for x in vertices}
    e = {ordered((s,a),(s,b)) for s in (0,1) for a,b in edges}
    f = [tuple((s,x) for x in face) for s in (0,1) for face in faces]
    for x in bverts: e.add(ordered((0,x),(1,x)))
    for a,b in bedges: f.append(((0,a),(0,b),(1,b),(1,a)))
    return sorted(v),sorted(e),f


def rx(code, ell=3, with_data=False):
    assert ell>=3 and ell%2
    t=(ell-1)//2
    qz = [list(bits(x)) for x in transpose(code.zs,code.n)]
    xq = [list(bits(x)) for x in code.xs]
    localx=[]
    for xi in range(len(code.xs)):
        verts=set(); edges=set(); faces=[]; bedges=set(); bverts=set()
        for fi,face in enumerate(code.faces):
            if face[0]!=xi: continue
            grid={(i,j):subdivided_vertex(face,i,j,t,fi)
                  for i in range(t+1) for j in range(t+1)}
            verts.update(grid.values())
            for i in range(t):
                for j in range(t+1): edges.add(ordered(grid[i,j],grid[i+1,j]))
            for i in range(t+1):
                for j in range(t): edges.add(ordered(grid[i,j],grid[i,j+1]))
            for i in range(t):
                for j in range(t):
                    faces.append((grid[i,j],grid[i+1,j],grid[i+1,j+1],grid[i,j+1]))
        for q in xq[xi]:
            for z in qz[q]:
                path=edge_subdivision(("q",q),("z",z),t)
                bverts.update(path)
                bedges.update(ordered(a,b) for a,b in zip(path,path[1:]))
        assert bverts<=verts and bedges<=edges
        # Connected ∂X_x is the primary's stated local premise.
        seen={next(iter(bverts))}
        while True:
            old=len(seen)
            for a,b in bedges:
                if a in seen or b in seen: seen.update((a,b))
            if old==len(seen): break
        assert seen==bverts, (xi,"disconnected star boundary")
        localx.append(double(verts,edges,faces,bverts,bedges))
    localq=[]
    for q in range(code.n):
        verts=set();edges=set();bverts=set()
        for z in qz[q]:
            path=edge_subdivision(("q",q),("z",z),t)
            verts.update(path);edges.update(ordered(a,b) for a,b in zip(path,path[1:]))
            bverts.add(("v",("z",z)))
        assert verts
        localq.append(double(verts,edges,[],bverts,set()))
    # Total-complex bases.
    xv=[(x,v) for x,(vs,_,_) in enumerate(localx) for v in vs]
    xe=[(x,e) for x,(_,es,_) in enumerate(localx) for e in es]
    xf=[(x,f) for x,(_,_,fs) in enumerate(localx) for f in fs]
    qv=[(q,v) for q,(vs,_,_) in enumerate(localq) for v in vs]
    qe=[(q,e) for q,(_,es,_) in enumerate(localq) for e in es]
    zp=[(z,s) for z in range(len(code.zs)) for s in (0,1)]
    id_xv={x:i for i,x in enumerate(xv)}
    id_xe={x:i for i,x in enumerate(xe)}
    id_qv={x:i+len(xe) for i,x in enumerate(qv)}
    id_xf={x:i for i,x in enumerate(xf)}
    id_qe={x:i+len(xf) for i,x in enumerate(qe)}
    id_zp={x:i+len(xf)+len(qe) for i,x in enumerate(zp)}
    xs=[0]*len(xv);zs=[0]*(len(xf)+len(qe)+len(zp))
    for (x,(a,b)),qi in id_xe.items():
        xs[id_xv[x,a]] |= 1<<qi
        xs[id_xv[x,b]] |= 1<<qi
    for (q,v),qi in id_qv.items():
        for x in range(len(code.xs)):
            if (code.xs[x]>>q)&1:
                assert (x,v) in id_xv
                xs[id_xv[x,v]] |= 1<<qi
    for (x,f),zi in id_xf.items():
        for a,b in zip(f,f[1:]+f[:1]): zs[zi] |= 1<<id_xe[x,ordered(a,b)]
    for (q,(a,b)),zi in id_qe.items():
        zs[zi] |= (1<<id_qv[q,a]) | (1<<id_qv[q,b])
        for x in range(len(code.xs)):
            if (code.xs[x]>>q)&1:
                zs[zi] |= 1<<id_xe[x,ordered(a,b)]
    for (z,s),zi in id_zp.items():
        for q in bits(code.zs[z]): zs[zi] |= 1<<id_qv[q,(s,("v",("z",z)))]
    # The first two square types are local cellular/restriction cancellations.
    faces=[]
    for xi,x in enumerate(xs):
        for zi,z in enumerate(zs):
            common=list(bits(x&z))
            if not common: continue
            if zi<len(xf)+len(qe):
                assert len(common)==2
                faces.append((xi,common[0],zi,common[1]))
    # The g_QZ*g_XQ=0 squares retain the input's cancellation pairing.
    for x,q,z,r in code.faces:
        for s in (0,1):
            v=(s,("v",("z",z)))
            faces.append((id_xv[x,v],id_qv[q,v],id_zp[z,s],id_qv[r,v]))
    result=Code(len(xe)+len(qv),xs,zs,faces)
    if with_data:
        return result,dict(t=t,localx=localx,localq=localq,xv=xv,xe=xe,xf=xf,qv=qv,qe=qe,zp=zp,
                           id_xv=id_xv,id_xe=id_xe,id_qv=id_qv,id_xf=id_xf,id_qe=id_qe,id_zp=id_zp,
                           qz=qz,xq=xq)
    return result


def seed():
    # Planar CSS [[5,1,2]] seed: four overlaps of size two.
    xs=[0b00111,0b11100]
    zs=[0b01101,0b10110]
    faces=[]
    for x,a in enumerate(xs):
        for z,b in enumerate(zs):
            q,r=list(bits(a&b));faces.append((x,q,z,r))
    return Code(5,xs,zs,faces)


def save(code,path):
    path.write_text(json.dumps({"n":code.n,"xs":[str(x) for x in code.xs],
                               "zs":[str(x) for x in code.zs],"faces":code.faces}))


def load(path):
    d=json.loads(path.read_text());return Code(d['n'],list(map(int,d['xs'])),list(map(int,d['zs'])),[tuple(x) for x in d['faces']])


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--levels',type=int,default=2)
    parser.add_argument('--ell',type=int,default=3);args=parser.parse_args()
    p=Path(__file__).parent/'complexes';p.mkdir(exist_ok=True)
    c=seed();records=[];start=time.perf_counter()
    for level in range(args.levels+1):
        t0=time.perf_counter();d=c.qualify();d.update(level=level,qualification_seconds=time.perf_counter()-t0)
        save(c,p/f'level_{level}.json');records.append(d);print(json.dumps(d),flush=True)
        if level<args.levels:
            c=rx(c,args.ell) if level%2==0 else rx(c.dual(),args.ell).dual()
    out={'ell':args.ell,'records':records,'wall_seconds':time.perf_counter()-start,
         'scope':'Exact finite GF(2) total complexes and input cancellation pairings; no random geometric embedding or all-level TQO theorem.'}
    (Path(__file__).parent/'COMPLEX_EXECUTION.json').write_text(json.dumps(out,indent=2))


if __name__=='__main__':main()
