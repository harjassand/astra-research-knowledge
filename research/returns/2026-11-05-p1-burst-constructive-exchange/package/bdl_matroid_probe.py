"""Exact GF(2) exploration of the BDL main RX replacement, minimal subdivision.

Implements the local cellular complexes and restriction maps in BDL §3.2.2.
ell=3 means (ell-1)/2=1 subdivision. This does not itself establish a
minor reduction from the theorem's much larger fixed subdivision constant.
No quantum dynamics or physical device is simulated.
"""
from collections import defaultdict, Counter
import json
from pathlib import Path

def canonical_edge(u,v):
    return tuple(sorted((u,v),key=repr))

class Tanner:
    def __init__(self,X,Q,Z,xq,qz,faces):
        self.X=sorted(X,key=repr); self.Q=sorted(Q,key=repr); self.Z=sorted(Z,key=repr)
        self.xq=set(xq); self.qz=set(qz); self.faces=sorted(faces,key=repr)
    def dual(self):
        return Tanner(self.Z,self.Q,self.X,{(z,q) for q,z in self.qz},
                      {(q,x) for x,q in self.xq},[(z,q1,x,q2) for x,q1,z,q2 in self.faces])
    def check(self):
        paths=defaultdict(set)
        qzs=defaultdict(list)
        for q,z in self.qz:qzs[q].append(z)
        for x,q in self.xq:
            for z in qzs[q]:paths[x,z].add(q)
        actual=defaultdict(list)
        for x,q1,z,q2 in self.faces:
            assert q1 != q2
            assert (x,q1) in self.xq and (x,q2) in self.xq
            assert (q1,z) in self.qz and (q2,z) in self.qz
            actual[x,z]+=[q1,q2]
        for k,v in paths.items():
            assert len(v)%2==0,(k,v)
            assert Counter(actual[k])==Counter(v),(k,len(v),len(actual[k]))
        return True
    def matrices(self):
        qi={q:i for i,q in enumerate(self.Q)}
        xrows=defaultdict(int);zrows=defaultdict(int)
        for x,q in self.xq:xrows[x]|=1<<qi[q]
        for q,z in self.qz:zrows[z]|=1<<qi[q]
        hx=[xrows[x] for x in self.X];hz=[zrows[z] for z in self.Z]
        return hx,hz

def relation_columns(rels,count):
    cols=[0]*count
    for j,r in enumerate(rels):
        while r:
            bit=r&-r;cols[bit.bit_length()-1]|=1<<j;r^=bit
    return cols

def seed():
    X=['x0','x1'];Q=list(range(5));Z=['z0','z1']
    xq={('x0',q) for q in [0,1,2]}|{('x1',q) for q in [0,3,4]}
    qz={(q,'z0') for q in [0,1,3]}|{(q,'z1') for q in [0,2,4]}
    faces=[('x0',0,'z0',1),('x0',0,'z1',2),('x1',0,'z0',3),('x1',0,'z1',4)]
    return Tanner(X,Q,Z,xq,qz,faces)

def rx(old):
    # Local cell keys use old vertex labels, lifted to copy 0/1.
    X=[];Q=[];Z=[];xq=set();qz=set();faces=[]
    locals_x={};locals_q={}
    for x in old.X:
        qs={q for xx,q in old.xq if xx==x}
        local_faces=[(x,q1,z,q2) for xx,q1,z,q2 in old.faces if xx==x]
        zs={f[2] for f in local_faces}
        verts={('x',x)}|{('q',q) for q in qs}|{('z',z) for z in zs}
        bdry_edges={canonical_edge(('q',q),('z',z)) for q,z in old.qz if q in qs}
        orig_edges=bdry_edges|{canonical_edge(('x',x),('q',q)) for q in qs}
        bdry_verts={v for e in bdry_edges for v in e}
        yverts={(v,t) for v in verts for t in [0,1]}
        yedges={canonical_edge((u,t),(v,t)) for u,v in orig_edges for t in [0,1]}
        yedges|={canonical_edge((v,0),(v,1)) for v in bdry_verts}
        yfaces=[]
        for xx,q1,z,q2 in local_faces:
            for t in [0,1]:
                yfaces.append(tuple((v,t) for v in [('x',x),('q',q1),('z',z),('q',q2)]))
        for u,v in sorted(bdry_edges,key=repr):
            yfaces.append(((u,0),(v,0),(v,1),(u,1)))
        xv={v:('XV',x,v) for v in yverts}
        qe={e:('XE',x,e) for e in yedges}
        zf={i:('XF',x,i) for i in range(len(yfaces))}
        X+=list(xv.values());Q+=list(qe.values());Z+=list(zf.values())
        for e,q in qe.items():
            for v in e: xq.add((xv[v],q))
        for i,f in enumerate(yfaces):
            for j,v in enumerate(f):
                e1=canonical_edge(f[j-1],v);e2=canonical_edge(v,f[(j+1)%4])
                qz.add((qe[e1],zf[i]));qz.add((qe[e2],zf[i]))
                faces.append((xv[v],qe[e1],zf[i],qe[e2]))
        locals_x[x]=(xv,qe,zf)
    for q in old.Q:
        zs={z for qq,z in old.qz if qq==q}
        yverts={(v,t) for v in ({('q',q)}|{('z',z) for z in zs}) for t in [0,1]}
        yedges={canonical_edge((('q',q),t),(('z',z),t)) for z in zs for t in [0,1]}
        yedges|={canonical_edge((('z',z),0),(('z',z),1)) for z in zs}
        qv={v:('QV',q,v) for v in yverts};ze={e:('QE',q,e) for e in yedges}
        Q+=list(qv.values());Z+=list(ze.values())
        for e,z in ze.items():
            for v in e:qz.add((qv[v],z))
        for x,qq in old.xq:
            if qq!=q:continue
            xv,qe,zf=locals_x[x]
            for v in yverts:xq.add((xv[v],qv[v]))
            for e in yedges:
                qz.add((qe[e],ze[e]))
                for v in e:faces.append((xv[v],qe[e],ze[e],qv[v]))
        locals_q[q]=(qv,ze)
    for z in old.Z:
        for t in [0,1]:
            zz=('ZV',z,t);Z.append(zz)
            for q,z2 in old.qz:
                if z2==z:qz.add((locals_q[q][0][(('z',z),t)],zz))
            for x,q1,z2,q2 in old.faces:
                if z2==z:
                    faces.append((locals_x[x][0][(('z',z),t)],locals_q[q1][0][(('z',z),t)],zz,locals_q[q2][0][(('z',z),t)]))
    result=Tanner(X,Q,Z,xq,qz,faces)
    result.check()
    return result

def rank_and_relations(rows):
    basis={};rels=[]
    for i,row in enumerate(rows):
        v=row;c=1<<i
        while v:
            p=v.bit_length()-1
            if p not in basis:
                basis[p]=(v,c);break
            b,d=basis[p];v^=b;c^=d
        if not v:rels.append(c)
    return len(basis),rels

def analyze(t):
    hx,hz=t.matrices()
    out={'sizes':{'X':len(t.X),'Q':len(t.Q),'Z':len(t.Z),'faces':len(t.faces)},'tanner_valid':t.check()}
    ranks=[]
    for tag,rows,labels in [('X',hx,t.X),('Z',hz,t.Z)]:
        r,rels=rank_and_relations(rows);ranks.append(r)
        columns=relation_columns(rels,len(rows))
        pats=Counter(columns)
        out[tag]={'rank':r,'nullity':len(rels),'dual_pattern_counts':dict(sorted(pats.items()))}
        if len(rels)==3:
            out[tag]['Fano_restriction_present']=all(v in pats for v in range(1,8))
            if out[tag]['Fano_restriction_present']:
                out[tag]['Fano_labels']={v:repr(labels[columns.index(v)]) for v in range(1,8)}
    out['logical_qubits']=len(t.Q)-sum(ranks)
    return out

def find_fano_minor(columns, attempts=200, seed_value=20261105):
    import random
    rng=random.Random(seed_value)
    cols=list(enumerate(columns))
    r,_=rank_and_relations(columns)
    if r<3:return None
    for attempt in range(attempts):
        rng.shuffle(cols)
        basis={};contract=[]
        for index,col in cols:
            v=col
            while v:
                p=v.bit_length()-1
                if p not in basis:
                    basis[p]=v;contract.append(index);break
                v^=basis[p]
            if len(basis)==r-3:break
        keys=sorted(basis,reverse=True)
        reps={}
        for index,col in enumerate(columns):
            v=col
            for p in keys:
                if (v>>p)&1:v^=basis[p]
            if v and v not in reps:reps[v]=index
        assert len(reps)<=7
        if len(reps)==7:
            return {'rank':r,'attempt':attempt,'contract':contract,'retain':list(reps.values()),'quotient_vectors':list(reps)}
    return None

def main():
    t=seed();results=[analyze(t)]
    for i in range(2):
        t=rx(t) if i%2==0 else rx(t.dual()).dual()
        results.append(analyze(t))
    hx,hz=t.matrices()
    for tag,rows in [('X',hx),('Z',hz)]:
        r,rels=rank_and_relations(rows)
        dualcols=relation_columns(rels,len(rows))
        results[-1][tag]['Fano_dual_minor_search']=find_fano_minor(dualcols)
    print(json.dumps(results,indent=2))
    Path(__file__).with_suffix('.json').write_text(json.dumps(results,indent=2)+'\n')

if __name__=='__main__':main()
