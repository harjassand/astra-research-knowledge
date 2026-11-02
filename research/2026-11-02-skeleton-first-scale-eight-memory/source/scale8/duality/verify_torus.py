"""Independent F_2 matrix check of the local construction on a 3x3 square torus.
Constant sheaf has one coordinate per cell; its dual is the same sheaf here.
Uses only per-closed-cell and per-costar elimination, never global contraction.
"""
import numpy as np

def mm(a,b): return (a@b)%2

def pivcols(a):
    z=a.copy(); row=0; out=[]
    for c in range(z.shape[1]):
        ps=np.flatnonzero(z[row:,c])
        if not len(ps): continue
        k=row+ps[0]; z[[row,k]]=z[[k,row]]
        for j in range(z.shape[0]):
            if j!=row and z[j,c]: z[j]^=z[row]
        out.append(c); row+=1
        if row==z.shape[0]:break
    return out

def inv(a):
    n=len(a); z=np.concatenate([a.copy(),np.eye(n,dtype=np.int64)],1)
    for c in range(n):
        ps=np.flatnonzero(z[c:,c]); assert len(ps)
        k=c+ps[0]; z[[c,k]]=z[[k,c]]
        for j in range(n):
            if j!=c and z[j,c]:z[j]^=z[c]
    assert np.array_equal(z[:,:n],np.eye(n,dtype=np.int64))
    return z[:,n:]

def contract(d,i):
    n=len(d); cols=pivcols(d); L=np.eye(n,dtype=np.int64)[:,cols]; B=mm(d,L)
    S=np.concatenate([B,i,L],axis=1); assert S.shape==(n,n)
    si=inv(S); r=len(cols); m=i.shape[1]
    p=si[r:r+m,:]; h=mm(L,si[:r,:])
    assert np.array_equal((mm(d,h)+mm(h,d)+mm(i,p))%2,np.eye(n,dtype=np.int64))
    assert not mm(h,h).any() and not mm(h,i).any() and not mm(p,h).any()
    return p,h

n=3
verts=[('v',x,y) for x in range(n) for y in range(n)]
edges=[(a,x,y) for a in ('h','e') for x in range(n) for y in range(n)]
faces=[('f',x,y) for x in range(n) for y in range(n)]
cells=verts+edges+faces; dim={x:(0 if x[0]=='v' else 2 if x[0]=='f' else 1) for x in cells}
bound={v:[] for v in verts}
for a,x,y in edges:bound[a,x,y]=[('v',x,y),('v',(x+1)%n,y) if a=='h' else ('v',x,(y+1)%n)]
for a,x,y in faces:bound[a,x,y]=[('h',x,y),('h',x,(y+1)%n),('e',x,y),('e',(x+1)%n,y)]
def closure(t):
    s={t}
    for x in bound[t]:s|=closure(x)
    return s
cl={t:closure(t) for t in cells}
coords=[(s,t) for s in cells for t in cells if s in cl[t]]; ix={z:j for j,z in enumerate(coords)}; N=len(coords)
dh=np.zeros((N,N),dtype=np.int64);dv=dh.copy()
for (s,t),j in ix.items():
    for sp in cells:
        if s in bound[sp] and sp in cl[t]:dh[ix[sp,t],j]=1
    for tp in bound[t]:
        if s in cl[tp]:dv[ix[s,tp],j]=1
assert not mm(dh,dh).any() and not mm(dv,dv).any()
assert np.array_equal(mm(dh,dv),mm(dv,dh))
A=faces+edges+verts;B=cells; ai={x:j for j,x in enumerate(A)};bi={x:j for j,x in enumerate(B)}
ia=np.zeros((N,len(A)),dtype=np.int64); ib=np.zeros((N,len(B)),dtype=np.int64)
pa=ia.T.copy();pb=ib.T.copy();ha=dh.copy()*0;hb=ha.copy()
for t in cells:
    inds=[j for j,(s,u) in enumerate(coords) if u==t]
    loc=np.array([[int(dim[coords[j][0]]==0)] for j in inds],dtype=np.int64)
    p,h=contract(dh[np.ix_(inds,inds)],loc)
    ia[inds,ai[t]]=loc[:,0];pa[ai[t],inds]=p[0];ha[np.ix_(inds,inds)]=h
for s in cells:
    inds=[j for j,(u,t) in enumerate(coords) if u==s]
    loc=np.array([[int(dim[coords[j][1]]==2)] for j in inds],dtype=np.int64)
    p,h=contract(dv[np.ix_(inds,inds)],loc)
    ib[inds,bi[s]]=loc[:,0];pb[bi[s],inds]=p[0];hb[np.ix_(inds,inds)]=h

def series(z):return (np.eye(N,dtype=np.int64)+z+mm(z,z))%2
PA=mm(pa,series(mm(dv,ha)));PB=mm(pb,series(mm(dh,hb)))
HA=mm(ha,series(mm(dv,ha)));HB=mm(hb,series(mm(dh,hb)))
DA=mm(pa,mm(dv,ia));DB=mm(pb,mm(dh,ib));DT=(dh+dv)%2
for P,I,H,d in [(PA,ia,HA,DA),(PB,ib,HB,DB)]:
    assert np.array_equal(mm(P,I),np.eye(len(d),dtype=np.int64))
    assert np.array_equal(mm(DT,I),mm(I,d))
    assert np.array_equal(mm(P,DT),mm(d,P))
    assert np.array_equal((np.eye(N,dtype=np.int64)+mm(I,P))%2,(mm(DT,H)+mm(H,DT))%2)
F=mm(PB,ia);G=mm(PA,ib);H=mm(PA,mm(HB,ia));K=mm(PB,mm(HA,ib))
assert np.array_equal(mm(F,DA),mm(DB,F))
assert np.array_equal(mm(G,DB),mm(DA,G))
assert np.array_equal((np.eye(len(A),dtype=np.int64)+mm(G,F))%2,(mm(DA,H)+mm(H,DA))%2)
assert np.array_equal((np.eye(len(B),dtype=np.int64)+mm(F,G))%2,(mm(DB,K)+mm(K,DB))%2)
for name,z in [('F',F),('G',G),('H',H),('K',K)]: print(name,'shape',z.shape,'max row',z.sum(1).max(),'max column',z.sum(0).max())
print('PASS: all local contractions, perturbed contractions, cochain maps and two homotopies verified over F_2.')

# Exhaustive top-degree removability check. Never assume tau valid beforehand.
a1=[ai[x] for x in edges]; a2=[ai[x] for x in verts]
b1=[bi[x] for x in edges]; b2=[bi[x] for x in faces]
da=DA[np.ix_(a2,a1)]; db=DB[np.ix_(b2,b1)]
f2=F[np.ix_(b2,a2)]; g1=G[np.ix_(a1,b1)]; h2=H[np.ix_(a1,a2)]
cs=pivcols(db); lookup={}
for mask in range(1<<len(cs)):
    r=np.zeros(len(edges),dtype=np.int64)
    for j,c in enumerate(cs):r[c]=(mask>>j)&1
    lookup[tuple(mm(db,r))]=r
verified=0
for mask in range(1<<len(verts)):
    tau=np.array([(mask>>j)&1 for j in range(len(verts))],dtype=np.int64)
    u=mm(f2,tau)
    if tuple(u) not in lookup:continue
    r=lookup[tuple(u)]; correction=(mm(g1,r)+mm(h2,tau))%2
    assert np.array_equal(mm(da,correction),tau)
    verified+=1
print('PASS: top-degree removability checked for all',1<<len(verts),'physical subsets;',verified,'have valid dual image and certified physical filling.')
