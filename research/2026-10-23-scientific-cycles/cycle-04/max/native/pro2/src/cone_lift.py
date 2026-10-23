"""Exact coning of supplied rational local witnesses; records every action."""
from fractions import Fraction as F
from exact_ops import dot,null,action,frob2


def build(local_builder,apex=F(1)):
    k=2; copies=3; m=12; q=3
    X=[[F(0),F(0),apex]]; blocks=[]; local_data=[]
    for j in range(copies):
        Z=[]; V=[]
        for i in range(m):
            z=([F(1),F(0)],[F(0),F(1)],[F(3,5),F(4,5)])[(i+j)%3]
            Z.append([F(3,5)*x for x in z])
            V.append(F(4,5)*(1 if ((i+j*j)%4)<2 else -1))
            X.append(Z[-1]+[V[-1]])
        r=local_builder(Z,0); B=r['flow_entries']
        BZ=action(m,k,B,Z); R=[v/apex for v in V]
        constraint=[sum((R[i]*BZ[i][a] for i in range(m)),F(0)) for a in range(k)]
        blocks.append((B,R,Z));local_data.append({'Z':Z,'R':R,'B':B,'constraint':constraint})
    alpha,rank=null([[d['constraint'][a] for d in local_data] for a in range(k)],copies)
    scale=max(abs(a) for a in alpha); alpha=[a/scale for a in alpha]
    D={}; edges=set(); A00=F(0)
    for j,(B,R,Z) in enumerate(blocks):
        off=1+j*m
        edges.update((0,off+i) for i in range(m));edges.update((off+i,off+i+1) for i in range(m-1))
        BR=[F(0)]*m
        for (i,l),a in B.items():
            a*=alpha[j]
            if a:D[(off+i,off+l)]=a
            BR[i]+=a*R[l]
            if i!=l:BR[l]+=a*R[i]
        for i,a in enumerate(BR):
            if a:D[(0,off+i)]=-a
        A00+=dot(R,BR)
    if A00:D[(0,0)]=A00
    Y=action(len(X),q,D,X);assert not any(Y[0])
    assert all(row[-1]==0 for row in Y)
    A2=frob2(Y); op2=max(a*a for (i,j),a in D.items() if i>0)
    return {'schema':'astra.cone_core_witness.v1','kind':'cone_lift',
      'n':len(X),'q':q,'X':X,'edges':sorted(edges),'D':D,
      'parameters':{'k':k,'copies':copies,'m':m,'apex':apex},
      'local_data':local_data,'alpha':alpha,'constraint_rank':rank,
      'action_squared':A2,'operator_lower_squared':op2,'ratio_lower_squared':op2/A2}
