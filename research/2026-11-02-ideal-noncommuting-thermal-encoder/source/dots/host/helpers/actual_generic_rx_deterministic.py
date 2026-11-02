"""Whole-star RX constructor from a Tanner complex having overlap-two squares.
No geometric embedding is asserted for the second iteration. All incidences are
built from cellular subdivisions, boundary cylinders, and restriction maps.
"""
from patch_rank_certificate import rank
from actual_rx_rung import build
from collections import deque
import json

def pair(a,b): return tuple(sorted((a,b),key=repr))
def rx(X,Z,n,ell):
    m=(ell-1)//2
    def bits(v):
        while v:
            t=v&-v; yield t.bit_length()-1; v^=t
    xq=[list(bits(v)) for v in X]; zq=[list(bits(v)) for v in Z]
    qx=[[] for _ in range(n)]; qz=[[] for _ in range(n)]
    for a,qs in enumerate(xq):
        for q in qs: qx[q].append(a)
    for a,qs in enumerate(zq):
        for q in qs: qz[q].append(a)
    squares=[]
    for a,v in enumerate(X):
        for b,w in enumerate(Z):
            overlap=list(bits(v&w))
            if overlap:
                assert len(overlap)==2
                squares.append((a,b,*overlap))
    def vert(t,i): return (t,i)
    def enode(a,b,k):
        if k==0:return a
        if k==m:return b
        p=pair(a,b)
        return ('edge',p,k if a==p[0] else m-k)
    xcells=[]
    for x in range(len(X)):
        vs=set(); es=set(); fs=[]; bd=set()
        for fi,(xx,z,qa,qb) in enumerate(squares):
            if xx!=x: continue
            xv=vert('x',x); av=vert('q',qa); bv=vert('q',qb); zv=vert('z',z)
            def node(i,j):
                if j==0:return enode(xv,av,i)
                if i==0:return enode(xv,bv,j)
                if i==m:return enode(av,zv,j)
                if j==m:return enode(bv,zv,i)
                return ('face',fi,i,j)
            for i in range(m+1):
                for j in range(m+1):vs.add(node(i,j))
            for i in range(m):
                for j in range(m+1):es.add(pair(node(i,j),node(i+1,j)))
            for i in range(m+1):
                for j in range(m):es.add(pair(node(i,j),node(i,j+1)))
            for i in range(m):
                for j in range(m):
                    a,b,c,d=node(i,j),node(i+1,j),node(i+1,j+1),node(i,j+1)
                    fs.append([pair(a,b),pair(b,c),pair(c,d),pair(d,a)])
            for k in range(m):
                bd.add(pair(enode(av,zv,k),enode(av,zv,k+1)))
                bd.add(pair(enode(bv,zv,k),enode(bv,zv,k+1)))
        bvs=set(v for e in bd for v in e)
        # doubled cells: vertex=(layer,v); edge=('s',layer,e) or ('r',v)
        V=[(l,v) for l in (0,1) for v in sorted(vs,key=repr)]
        E={('s',l,e):[(l,e[0]),(l,e[1])] for l in (0,1) for e in sorted(es,key=repr)}
        E.update({('r',v):[(0,v),(1,v)] for v in sorted(bvs,key=repr)})
        F=[[('s',l,e) for e in f] for l in (0,1) for f in fs]
        F += [[('s',0,e),('s',1,e),('r',e[0]),('r',e[1])] for e in sorted(bd,key=repr)]
        xcells.append((V,E,F))
    qcells=[]
    for q in range(n):
        vs={vert('q',q)}; es=set()
        for z in qz[q]:
            a,b=vert('q',q),vert('z',z)
            for k in range(m):
                e=pair(enode(a,b,k),enode(a,b,k+1)); es.add(e); vs.update(e)
        V=[(l,v) for l in (0,1) for v in sorted(vs,key=repr)]
        E={('s',l,e):[(l,e[0]),(l,e[1])] for l in (0,1) for e in sorted(es,key=repr)}
        E.update({('r',vert('z',z)):[(0,vert('z',z)),(1,vert('z',z))] for z in qz[q]})
        qcells.append((V,E))
    xn=[]; qn=[]; xchecks={}; zchecks=[]
    for x,(V,E,F) in enumerate(xcells):
        for v in V: xn.append((x,v)); xchecks[x,v]=[]
        for e,vs in E.items():
            qname=('xe',x,e); qn.append(qname)
            for v in vs:xchecks[x,v].append(qname)
        for f in F:zchecks.append([('xe',x,e) for e in f])
    inherited=[]
    for q,(V,E) in enumerate(qcells):
        descendants=[]
        for v in V:
            qname=('qv',q,v); qn.append(qname); descendants.append(qname)
            for x in qx[q]: xchecks[x,v].append(qname)
        inherited.append(descendants)
        for e,vs in E.items():
            row=[('qv',q,v) for v in vs]
            for x in qx[q]:
                assert e in xcells[x][1]
                row.append(('xe',x,e))
            zchecks.append(row)
    for z in range(len(Z)):
        for l in (0,1):zchecks.append([('qv',q,(l,vert('z',z))) for q in zq[z]])
    qi={v:i for i,v in enumerate(qn)}
    def mask(vs):return sum(1<<qi[v] for v in vs)
    XX=[mask(xchecks[x]) for x in xn]; ZZ=[mask(v) for v in zchecks]
    assert all((x&z).bit_count()%2==0 for x in XX for z in ZZ)
    assert len(qn)-rank(XX)-rank(ZZ)==n-rank(X)-rank(Z)
    return XX,ZZ,qn,[mask(v) for v in inherited]

def graph_radius(X,Z,n,R):
    # Bipartite Tanner distance from support: return minimum support-neighborhood
    # radius that permits filling R using Z generators. Checks of both types
    # determine graph geometry, but only Z checks may fill R.
    checks=X+Z; adj=[[] for _ in range(n+len(checks))]
    for j,c in enumerate(checks):
        for i in range(n):
            if c>>i&1:adj[i].append(n+j);adj[n+j].append(i)
    ds=[None]*len(adj); queue=deque()
    for i in range(n):
        if R>>i&1:ds[i]=0;queue.append(i)
    while queue:
        i=queue.popleft()
        for j in adj[i]:
            if ds[j] is None:ds[j]=ds[i]+1;queue.append(j)
    for r in sorted(set(d for d in ds[:n] if d is not None)):
        B=sum(1<<i for i,d in enumerate(ds[:n]) if d is not None and d<=r)
        local=[c for c in Z if not c&~B]
        if rank(local)==rank(local+[R]):return r
    raise AssertionError('R not global stabilizer')

if __name__=='__main__':
    out=[]
    for ell1,ell2 in [(3,3),(5,3),(5,5),(7,3)]:
        c=build(ell1);m=c['m'];j=0
        R=sum(1<<c['qi'][v] for v in [('qv','a',0,j),('qv','a',1,j),('xr',m,j)])
        # RZ=transpose(RX(transpose(C))). Canonical Z lift repeats each old
        # qubit on every 0-cell of its RX-dual Yq.
        dualX,dualZ,qn,F=rx(c['Z'],c['X'],len(c['qs']),ell2)
        X,Z=dualZ,dualX
        lifted=0
        for i in range(len(F)):
            if R>>i&1:lifted^=F[i]
        assert rank(Z)==rank(Z+[lifted])
        out.append(dict(ell1=ell1,ell2=ell2,n1=len(c['qs']),n2=len(qn),rung_weight=3,lifted_weight=lifted.bit_count(),first_graph_collar=graph_radius(c['X'],c['Z'],len(c['qs']),R),second_graph_collar=graph_radius(X,Z,len(qn),lifted)))
        print(json.dumps(out[-1]),flush=True)
    open('actual_rx_rz_results.json','w').write(json.dumps(out,indent=2))
