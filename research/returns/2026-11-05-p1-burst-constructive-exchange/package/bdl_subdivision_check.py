"""Independent literal subdivision check for the all-ell wheel bridge.
Builds actual cellular replacements with m=2,3, not by repeating a matrix.
Only the first two levels are needed to check the preserved corner wheel.
"""
from collections import defaultdict
from pathlib import Path
import json
from bdl_matroid_probe import Tanner,seed,canonical_edge,rank_and_relations
from rx_relations import rx_Z_relations

# Canonical subdivided-edge vertices shared by independently built local stars.
def point(u,v,j,m):
    if j==0:return u
    if j==m:return v
    e=canonical_edge(u,v)
    return ('S',e,j if u==e[0] else m-j,m)

def square_grid(f,m):
    x,q,z,r=f
    corners=[('x',x),('q',q),('z',z),('q',r)]
    def v(i,j):
        if j==0:return point(corners[0],corners[1],i,m)
        if i==m:return point(corners[1],corners[2],j,m)
        if j==m:return point(corners[3],corners[2],i,m)
        if i==0:return point(corners[0],corners[3],j,m)
        return ('I',f,i,j,m)
    return [(v(i,j),v(i+1,j),v(i+1,j+1),v(i,j+1)) for i in range(m) for j in range(m)]

def rx_m(old,m):
    X=[];Q=[];Z=[];xq=set();qz=set();faces=[];meta={};local_x={};local_q={}
    qzs=defaultdict(list);xqs=defaultdict(list);xfaces=defaultdict(list)
    for q,z in sorted(old.qz,key=repr):qzs[q].append(z)
    for x,q in sorted(old.xq,key=repr):xqs[x].append(q)
    for f in old.faces:xfaces[f[0]].append(f)
    for x in old.X:
        fs=xfaces[x];small=[]
        for i,f in enumerate(fs):
            small.extend((i,cell) for cell in square_grid(f,m))
        coarsebdry=sorted({canonical_edge(('q',q),('z',z)) for q in xqs[x] for z in qzs[q]},key=repr)
        bdry=[]
        for k,(u,v) in enumerate(coarsebdry):
            bdry.extend((k,canonical_edge(point(u,v,j,m),point(u,v,j+1,m))) for j in range(m))
        basefaces=[f for i,f in small];baseedges={canonical_edge(f[j-1],f[j]) for f in basefaces for j in range(4)}
        baseverts={v for e in baseedges for v in e};bverts={v for k,e in bdry for v in e}
        yverts={(v,t) for v in baseverts for t in (0,1)}
        yedges={canonical_edge((u,t),(v,t)) for u,v in baseedges for t in (0,1)}
        yedges|={canonical_edge((v,0),(v,1)) for v in bverts}
        yfaces=[];origins=[]
        for i,f in small:
            for t in (0,1):yfaces.append(tuple((v,t) for v in f));origins.append(('XF',x,2*i+t))
        for k,(u,v) in bdry:
            yfaces.append(((u,0),(v,0),(v,1),(u,1)));origins.append(('XF',x,2*len(fs)+k))
        xv={v:('XV',x,v) for v in yverts};qe={e:('XE',x,e) for e in yedges};zf={i:('XF',x,i) for i in range(len(yfaces))}
        X+=list(xv.values());Q+=list(qe.values());Z+=list(zf.values())
        for e,q in qe.items():
            for v in e:xq.add((xv[v],q))
        for i,f in enumerate(yfaces):
            meta[zf[i]]=origins[i]
            for j,v in enumerate(f):
                e1=canonical_edge(f[j-1],v);e2=canonical_edge(v,f[(j+1)%4])
                qz.add((qe[e1],zf[i]));qz.add((qe[e2],zf[i]));faces.append((xv[v],qe[e1],zf[i],qe[e2]))
        local_x[x]=(xv,qe)
    for q in old.Q:
        baseverts={('q',q)};yedges=set();origins={}
        for z in qzs[q]:
            u,v=('q',q),('z',z)
            baseverts.update(point(u,v,j,m) for j in range(m+1))
            for t in (0,1):
                original=('QE',q,canonical_edge((u,t),(v,t)))
                for j in range(m):
                    e=canonical_edge((point(u,v,j,m),t),(point(u,v,j+1,m),t));yedges.add(e);origins[e]=original
            e=canonical_edge((v,0),(v,1));yedges.add(e);origins[e]=('QE',q,e)
        yverts={(v,t) for v in baseverts for t in (0,1)}
        qv={v:('QV',q,v) for v in yverts};ze={e:('QE',q,e) for e in yedges}
        Q+=list(qv.values());Z+=list(ze.values())
        for e,znew in ze.items():
            meta[znew]=origins[e]
            for v in e:qz.add((qv[v],znew))
        for x in old.X:
            if q not in xqs[x]:continue
            xv,qe=local_x[x]
            for v in yverts:xq.add((xv[v],qv[v]))
            for e in yedges:
                qz.add((qe[e],ze[e]))
                for v in e:faces.append((xv[v],qe[e],ze[e],qv[v]))
        local_q[q]=qv
    for z in old.Z:
        for t in (0,1):
            zz=('ZV',z,t);Z.append(zz);meta[zz]=zz
            for q,zzold in old.qz:
                if zzold==z:qz.add((local_q[q][(('z',z),t)],zz))
            for x,q,zzold,r in old.faces:
                if zzold==z:faces.append((local_x[x][0][(('z',z),t)],local_q[q][(('z',z),t)],zz,local_q[r][(('z',z),t)]))
    ans=Tanner(X,Q,Z,xq,qz,faces);ans.check();return ans,meta

def main():
    output=[];s=seed();names,coarsecols=rx_Z_relations(s)
    for m in (1,2,3):
        t1,meta=rx_m(s,m)
        cols={z:coarsecols[meta[z]] for z in t1.Z}
        sums=defaultdict(int)
        for q,z in t1.qz:sums[q]^=cols[z]
        assert not any(sums.values())
        _,hz=t1.matrices();rank,_=rank_and_relations(hz)
        crank,_=rank_and_relations(list(cols.values()))
        assert crank==len(t1.Z)-rank==3
        # The two retained dependency coordinates are a_q0,z0=w and s_z0=u.
        images={}
        for i,name in enumerate(names):
            if name==('s','z0'):images[i]=2
            elif name[0]=='a':images[i]=1
            else:images[i]=0
        def project(v):
            ans=0
            for i,b in images.items():
                if (v>>i)&1:ans^=b
            return ans
        u=('XV','x0',(('z','z0'),0))
        # Actual old-corner wheel. Exact new qubit labels, including m>1 edges.
        A=('XE','x0',canonical_edge((point(('q',0),('z','z0'),m-1,m),0),(('z','z0'),0)))
        B=('XE','x0',canonical_edge((point(('q',1),('z','z0'),m-1,m),0),(('z','z0'),0)))
        C=('XE','x0',canonical_edge((('z','z0'),0),(('z','z0'),1)))
        D=('QV',0,(('z','z0'),0));E=('QV',1,(('z','z0'),0))
        inv={A:'A',B:'B',C:'C',D:'D',E:'E'}
        edges={tuple(sorted((inv[q],inv[r]))):z for x,q,z,r in t1.faces if x==u}
        edgeorder=[('A','B'),('A','C'),('B','C'),('A','D'),('B','E'),('C','D'),('C','E'),('D','E')]
        assert set(edges)==set(edgeorder)
        pattern=[project(cols[edges[e]]) for e in edgeorder]
        assert pattern==[0,1,0,1,0,3,2,2]
        # Check the next RZ terminal corner reproduces this wheel literally.
        dual2,_=rx_m(t1.dual(),m);t2=dual2.dual();v=('ZV',u,0)
        qmap={('QV',q,(('z',u),0)):letter for q,letter in inv.items()}
        pairs=[];values=[]
        for x,q,z,r in t2.faces:
            if x==v:
                e=tuple(sorted((qmap[q],qmap[r])));pairs.append(e)
                assert z[0]=='XV'
                values.append((e,project(cols[z[1]])))
        assert set(pairs)==set(edgeorder)
        assert dict(values)==dict(zip(edgeorder,pattern))
        output.append({'m':m,'ell':2*m+1,'level1_qubits':len(t1.Q),'level2_qubits':len(t2.Q),'full_level1_relation_space_verified':True,'corner_wheel_and_RZ_preservation_verified':True,'inherited_patterns':pattern})
        print(output[-1],flush=True)
    path=Path(__file__).parent/'matroid_certificates/subdivision_verification.json'
    path.write_text(json.dumps(output,indent=2)+'\n')
if __name__=='__main__':main()
