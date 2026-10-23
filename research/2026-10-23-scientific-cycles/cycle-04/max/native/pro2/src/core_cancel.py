"""Executable exact high-covariance core cancellation.

The supplied port rows repeat orthonormal rational frames. Thus their Gram
is EXACTLY L times the port projection. No numerical eigensolver supplies a
certificate. The universal spectral dichotomy is proved separately.
"""
from fractions import Fraction as F
from exact_ops import dot,null,action,frob2,basis,core_graph,core_rows


def build(t,N,M):
    h=t*(t+1)//2; q=h+t; s=t-1
    m=q*s-t*s//2+2; n0,edges=core_graph(t,m)
    X=core_rows(n0,q); O=basis(q); ports=[]
    child_s=t-1
    child_nonanchor=M+child_s-1
    if child_nonanchor%h: raise ValueError('child rows must balance the h-frame')
    for v in range(s,n0):
        labels=[(v+j)%q for j in range(h)]
        U=[O[j] for j in labels]
        leaves=[]; copies=[]
        for rep in range(N):
            ids=list(range(len(X),len(X)+child_nonanchor))
            # Local K_(t-1) join P_M, anchor is its first clique vertex.
            local=[v]+ids; copies.append(local)
            _,ce=core_graph(t,M)
            edges.update(tuple(sorted((local[a],local[b]))) for a,b in ce)
            for j,i in enumerate(ids): X.append(U[j%h][:]); leaves.append(i)
        ports.append({'vertex':v,'basis':U,'vertices':leaves,'copies':copies,
                      'gram_scale':F(N*child_nonanchor,h)})
    positions=[(i,i) for i in range(n0)]+sorted((a,b) for a,b in edges if b<n0)
    tests=[]
    for v in range(n0):
        if v<s: fs=O
        else:
            port=ports[v-s]
            labels={(v+j)%q for j in range(h)}
            fs=[O[j] for j in range(q) if j not in labels]
        for f in fs:
            row=[]
            for a,b in positions:
                row.append(dot(X[b],f) if a==v else
                           (dot(X[a],f) if b==v else F(0)))
            tests.append(row)
    c,rank=null(tests,len(positions)); scale=max(abs(x) for x in c)
    c=[x/scale for x in c]
    B={p:a for p,a in zip(positions,c) if a}
    rootY=action(n0,q,B,X[:n0]); D=dict(B)
    for p in ports:
        v=p['vertex']; U=p['basis']; L=p['gram_scale']; b=rootY[v]
        assert all(dot(b,f)==0 for f in O if f not in U)
        # A=L P_U, so its inverse on U is exactly 1/L.
        for i in p['vertices']:
            a=-dot(X[i],b)/L
            if a:D[tuple(sorted((v,i)))]=a
    Y=action(len(X),q,D,X); assert all(not any(r) for r in Y[:n0])
    A2=frob2(Y); op2=max(a*a for a in B.values())
    assert op2==1 and A2>0
    return {'schema':'astra.cone_core_witness.v1','kind':'core_cancellation',
      'parameters':{'t':t,'N':N,'M':M,'h':h,'q':q,'root_path':m,'root_n':n0},
      'n':len(X),'q':q,'edges':sorted(edges),'X':X,'D':D,'core_D':B,
      'ports':ports,'constraint_rank':rank,'constraint_rows':len(tests),
      'root_variables':len(positions),'action_squared':A2,
      'operator_lower_squared':op2,'ratio_lower_squared':op2/A2}
