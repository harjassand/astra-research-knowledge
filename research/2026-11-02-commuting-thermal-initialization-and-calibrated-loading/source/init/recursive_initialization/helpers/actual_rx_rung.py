"""Actual §3.2.2 RX of the one-square Bell seed. Integer-bitset matrices.
Cell coordinates are the flattened Tanner ell-grid, not separated layers.
Cx=cochains of double m*m square joined along right/top boundary cylinder.
Cqa,Cqb=shifted cochains of doubled m-edge arms joined only at z endpoint.
Cz=two points. All local/gluing check rows are retained.
"""
from patch_rank_certificate import rank, patch_defect
import json, math

def build(ell):
    assert ell>=3 and ell%2
    m=(ell-1)//2
    xs=[]; qs=[]; zs=[]; pos={}; edges={}; faces={}
    def x(v,xy): xs.append(v); pos[v]=xy
    def q(v,xy,boundary=None):
        qs.append(v); pos[v]=xy
        if boundary is not None: edges[v]=boundary
    def z(v,xy,boundary=None):
        zs.append(v); pos[v]=xy
        if boundary is not None: faces[v]=boundary
    for layer in (0,1):
        for i in range(m+1):
            for j in range(m+1): x(('xv',layer,i,j),(2*i,2*j))
        for i in range(m):
            for j in range(m+1):
                q(('xh',layer,i,j),(2*i+1,2*j),[('xv',layer,i,j),('xv',layer,i+1,j)])
        for i in range(m+1):
            for j in range(m):
                q(('xv_edge',layer,i,j),(2*i,2*j+1),[('xv',layer,i,j),('xv',layer,i,j+1)])
        for i in range(m):
            for j in range(m):
                z(('xf',layer,i,j),(2*i+1,2*j+1),[('xh',layer,i,j),('xh',layer,i,j+1),('xv_edge',layer,i,j),('xv_edge',layer,i+1,j)])
    bdry=[(m,j) for j in range(m+1)]+[(i,m) for i in range(m)]
    for i,j in bdry:
        q(('xr',i,j),(2*i,2*j),[('xv',0,i,j),('xv',1,i,j)])
    for arm in ('a','b'):
        def ij(k): return (m,k) if arm=='a' else (k,m)
        def sheetedge(l,k): return ('xv_edge',l,m,k) if arm=='a' else ('xh',l,k,m)
        for k in range(m):
            i,j=ij(k); ii,jj=ij(k+1)
            z(('xcf',arm,k),((2*i+2*ii)/2,(2*j+2*jj)/2),[sheetedge(0,k),sheetedge(1,k),('xr',i,j),('xr',ii,jj)])
        for l in (0,1):
            for k in range(m+1):
                i,j=ij(k)
                xy=(ell,2*k) if arm=='a' else (2*k,ell)
                # g_xq^0 is restriction of sheet vertex to this arm vertex.
                q(('qv',arm,l,k),xy,[('xv',l,i,j)])
            for k in range(m):
                xy=(ell,2*k+1) if arm=='a' else (2*k+1,ell)
                z(('qe',arm,l,k),xy,[('qv',arm,l,k),('qv',arm,l,k+1),sheetedge(l,k)])
        # g_xq^1 restricts the cylinder rung to the endpoint vertical edge.
        xy=(ell,2*m) if arm=='a' else (2*m,ell)
        z(('qr',arm),xy,[('qv',arm,0,m),('qv',arm,1,m),('xr',m,m)])
    for l in (0,1):
        z(('z',l),(ell,ell),[('qv','a',l,m),('qv','b',l,m)])
    qi={v:i for i,v in enumerate(qs)}; xi={v:i for i,v in enumerate(xs)}
    X=[0]*len(xs)
    for v,b in edges.items():
        for a in b: X[xi[a]] ^= 1<<qi[v]
    Z=[sum(1<<qi[q] for q in faces[v]) for v in zs]
    assert all((a&b).bit_count()%2==0 for a in X for b in Z)
    assert len(qs)-rank(X)-rank(Z)==0  # Bell seed encodes no logical qubit.
    return dict(ell=ell,m=m,xs=xs,qs=qs,zs=zs,pos=pos,qi=qi,X=X,Z=Z)

def test(ell,j):
    c=build(ell); m=c['m']; qi=c['qi']; Z=c['Z']; zs=c['zs']; pos=c['pos']
    rung_names=[('qv','a',0,j),('qv','a',1,j),('xr',m,j)]
    R=sum(1<<qi[v] for v in rung_names)
    witness_names=[('qr','a')]
    for k in range(j,m): witness_names += [('qe','a',0,k),('qe','a',1,k),('xcf','a',k)]
    w=0
    for v in witness_names: w ^= Z[zs.index(v)]
    assert w==R
    assert rank(Z)==rank(Z+[R])
    center=(ell-.5,2*j)
    d2=[(pos[q][0]-center[0])**2+(pos[q][1]-center[1])**2 for q in c['qs']]
    def mask(r2): return sum(1<<i for i,d in enumerate(d2) if d<=r2+1e-9)
    # A radius .5 ball contains exactly these three qubits (layers coincide).
    A=mask(.25); assert A==R
    thresholds=sorted(set(d2))
    minimal=None
    for r2 in thresholds:
        B=mask(r2); local=[z for z in Z if not z&~B]
        if rank(local)==rank(local+[R]): minimal=r2; break
    expected=.25+(2*(m-j))**2
    assert minimal==expected,(ell,j,minimal,expected)
    unitB=mask(1.5**2) # radius .5 initial ball plus unit collar
    return dict(ell=ell,j=j,qubits=len(qi),Xchecks=len(c['X']),Zchecks=len(Z),
        rung_weight=R.bit_count(),explicit_filling_checks=len(witness_names),
        initial_radius=.5,minimum_filling_ball_radius=math.sqrt(minimal),
        exact_radius_squared=minimal,unit_collar_defect=patch_defect(Z,len(qi),A,unitB)['defect'])

if __name__=='__main__':
    results=[test(e,j) for e in (3,5,7,9,13) for j in range((e-1)//2)]
    print(json.dumps(results,indent=2))
