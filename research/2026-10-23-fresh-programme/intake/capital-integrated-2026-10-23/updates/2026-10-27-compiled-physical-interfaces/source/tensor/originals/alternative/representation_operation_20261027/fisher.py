"""Established Fisher/FKT backend, adapted with credit, not a new algorithm.

Rotation/GF2-orientation/reference-sign design reused from independent ordinary
comparator finite_field_gate_check.py (read-only source in sibling directory).
Adaptations: explicit port IDs, multiple components, field-operation interface,
Gauss-Jordan inverse and correct prefactor-aware ORIGINAL edge-pin derivative.
"""
from fields import Degenerate


def pfaffian(A,F):
    A=[row[:] for row in A];out=F.one;n=len(A)
    for i in range(0,n,2):
        j=next((j for j in range(i+1,n) if A[i][j]!=F.zero),None)
        if j is None:return F.zero
        if j!=i+1:
            A[i+1],A[j]=A[j],A[i+1]
            for row in A:row[i+1],row[j]=row[j],row[i+1]
            out=F.neg(out)
        pivot=A[i][i+1];out=F.mul(out,pivot);pi=F.inv(pivot)
        for j in range(i+2,n):
            for k in range(j+1,n):
                correction=F.mul(F.sub(F.mul(A[i+1][j],A[i][k]),F.mul(A[i][j],A[i+1][k])),pi)
                A[j][k]=F.add(A[j][k],correction);A[k][j]=F.neg(A[j][k])
    return out


def matrix_inverse(A,F):
    n=len(A);a=[row[:]+[F.one if i==j else F.zero for j in range(n)] for i,row in enumerate(A)]
    for i in range(n):
        pivot=next((j for j in range(i,n) if a[j][i]!=F.zero),None)
        if pivot is None:raise Degenerate('singular FKT matrix; no normalized marginals at this prime')
        a[i],a[pivot]=a[pivot],a[i];inv=F.inv(a[i][i]);a[i]=[F.mul(v,inv) for v in a[i]]
        for j in range(n):
            if j==i or a[j][i]==F.zero:continue
            mult=a[j][i];a[j]=[F.sub(x,F.mul(mult,y)) for x,y in zip(a[j],a[i])]
    return [row[n:] for row in a]


def topology(n,edges):
    ports={}
    for v,i,w,j in edges:ports[3*v+i]=3*w+j;ports[3*w+j]=3*v+i
    rotation={u:[ports[u],3*(u//3)+(u%3+1)%3,3*(u//3)+(u%3-1)%3] for u in range(3*n)}
    e_set={tuple(sorted((u,v))) for u,ws in rotation.items() for v in ws};edge_list=sorted(e_set);edge_index={e:i for i,e in enumerate(edge_list)}
    component={};components=[]
    for u in rotation:
        if u in component:continue
        comp=[];cid=len(components);component[u]=cid;stack=[u]
        while stack:
            a=stack.pop();comp.append(a)
            for b in rotation[a]:
                if b not in component:component[b]=cid;stack.append(b)
        components.append(comp)
    seen=set();faces=[];face_comp=[]
    for u,ws in rotation.items():
        for v in ws:
            if (u,v) in seen:continue
            start=(u,v);dart=start;face=[]
            while dart not in seen:
                seen.add(dart);face.append(dart);a,b=dart;dart=(b,rotation[b][(rotation[b].index(a)-1)%3])
            if dart!=start:raise ValueError('invalid rotation permutation')
            faces.append(face);face_comp.append(component[u])
    for cid,comp in enumerate(components):
        f=sum(c==cid for c in face_comp)
        if len(comp)-3*len(comp)//2+f!=2:raise ValueError('supplied cyclic port order is not a planar embedding')
    rows=[];outer=set()
    for face,cid in zip(faces,face_comp):
        if cid not in outer:outer.add(cid);continue
        mask=0;rhs=1
        for a,b in face:mask^=1<<edge_index[tuple(sorted((a,b)))];rhs^=int(a>b)
        rows.append((mask,rhs))
    pivots={}
    for mask,rhs in rows:
        while mask:
            col=(mask&-mask).bit_length()-1
            if col not in pivots:pivots[col]=(mask,rhs);break
            a,b=pivots[col];mask^=a;rhs^=b
        else:
            if rhs:raise ArithmeticError('inconsistent Kasteleyn face equations')
    solution=0
    for col in sorted(pivots,reverse=True):
        mask,rhs=pivots[col]
        if ((mask&solution).bit_count()&1)!=rhs:solution^=1<<col
    if any(((mask&solution).bit_count()&1)!=rhs for mask,rhs in rows):raise ArithmeticError('bad orientation certificate')
    arrows={e:(1 if (solution>>i)&1 else -1) for i,e in enumerate(edge_list)}
    external=[tuple(sorted((3*v+i,3*w+j))) for v,i,w,j in edges];refsign=1
    for e in external:refsign*=arrows[e]
    for i,(a,b) in enumerate(external):
        for c,d in external[i+1:]:
            if a<c<b<d or c<a<d<b:refsign=-refsign
    return {'n':n,'edge_list':edge_list,'arrows':arrows,'external':external,'reference_sign':refsign,'face_count':len(faces),'component_of_port':component,'components':components}


def evaluate(weights,top,F,with_marginals=False):
    n=top['n'];N=3*n;A=[[F.zero]*N for _ in range(N)];pref=F.inv(F.embed(pow(2,n//2,F.p)));eig=[]
    values={e:F.one for e in top['edge_list']}
    for e,(a,b) in zip(top['external'],weights):
        w0,w1=F.add(a,b),F.sub(a,b)
        if w0==F.zero or w1==F.zero:raise Degenerate('singular symmetrized edge')
        x=F.div(w0,w1);values[e]=x;pref=F.mul(pref,w1);eig.append((w0,w1,x))
    for (u,v),w in values.items():A[u][v]=F.mul(F.embed(top['arrows'][u,v]),w);A[v][u]=F.neg(A[u][v])
    C=F.mul(pref,F.embed(top['reference_sign']));z=F.mul(C,pfaffian(A,F))
    if not with_marginals or z==F.zero:return z,None
    inverse=matrix_inverse(A,F);grad=[]
    for e,(w0,w1,x) in zip(top['external'],eig):
        u,v=e;h=F.mul(F.mul(x,F.embed(top['arrows'][e])),inverse[v][u])
        # Log derivatives include BOTH the external edge and product(w1) prefactor.
        d0=F.div(h,w0);d1=F.div(F.sub(F.one,h),w1)
        grad.append((d0,d1))
    return z,grad
