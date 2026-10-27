"""Checked prime-fibre acquisition of a hidden parity gauge and FKT evaluation."""
from fields import Prime,QuadraticFinite,Degenerate
from local_recognition import cp,mm,transpose
from fisher import evaluate


def stage(ts,edges,ports,top,p,with_marginals=True,branch_flips=()):
    F=QuadraticFinite(p);B=Prime(p);n=len(ts);A=[cp(t,B,F) for t in ts]
    for v in branch_flips:
        A[v]=[[list(reversed(row)) for row in mat] for mat in A[v]]
    g=[F.one for _ in ts];rhos=[];weights=[];Ws=[]
    for v,i,w,j in edges:
        W=mm(transpose(A[v][i]),A[w][j],F)
        if any(x==F.zero for row in W for x in row):raise Degenerate('zero CP edge entry at this prime')
        rv2=F.div(F.mul(W[1][1],W[1][0]),F.mul(W[0][0],W[0][1]))
        rw2=F.div(F.mul(W[1][1],W[0][1]),F.mul(W[0][0],W[1][0]))
        r=F.sqrt_f2(rv2);s=F.div(W[1][1],F.mul(W[0][0],r))
        if F.mul(r,r)!=rv2 or F.mul(s,s)!=rw2 or F.div(r,s)!=F.div(W[1][0],W[0][1]):raise ArithmeticError('edge-root certificate failed')
        g[v]=F.mul(g[v],r);g[w]=F.mul(g[w],s);rhos.append([r,s]);Ws.append(W);weights.append([W[1][1],F.mul(r,W[0][1])])
    if any(F.mul(x,x)!=F.one for x in g):raise Degenerate('local squared field balance fails mod prime')
    comp_sign={}
    for v in range(n):
        cid=top['component_of_port'][3*v];comp_sign[cid]=F.mul(comp_sign.get(cid,F.one),g[v])
    minus=F.neg(F.one)
    if any(s not in (F.one,minus) for s in comp_sign.values()):raise ArithmeticError('invalid parity sign')
    info={'prime':p,'field_degree':2,'quadratic_nonresidue':F.nu,'Tonelli_nonresidue_Fp2':list(F.kappa),'cp_tensor_and_edge_identities_checked':True,'component_parities':{str(k):(1 if x==F.one else -1) for k,x in comp_sign.items()}}
    if any(s==minus for s in comp_sign.values()):return {**info,'status':'ODD_PARITY_ZERO_RESIDUE','residue':0,'pin_residues':None}
    seen=set()
    for root in range(n):
        if root in seen:continue
        parent={root:None};order=[root];seen.add(root)
        for v in order:
            for eid,w,j in ports[v]:
                if w not in seen:seen.add(w);parent[w]=(v,eid);order.append(w)
        for v in reversed(order[1:]):
            w,eid=parent[v]
            if g[v]==minus:
                g[v]=F.neg(g[v]);g[w]=F.neg(g[w]);rhos[eid]=[F.neg(x) for x in rhos[eid]];weights[eid][1]=F.neg(weights[eid][1])
        if g[root]!=F.one:raise ArithmeticError('parity neutralization failed')
    # Validate the full rescaled representation after all tree-sign choices.
    actual=[F.one for _ in ts]
    for eid,(v,i,w,j) in enumerate(edges):
        r,s=rhos[eid];W=Ws[eid];a,b=weights[eid]
        if F.mul(F.mul(r,s),W[0][0])!=a or W[1][1]!=a or F.mul(r,W[0][1])!=b or F.mul(s,W[1][0])!=b:raise ArithmeticError('symmetrized edge identity failed')
        actual[v]=F.mul(actual[v],r);actual[w]=F.mul(actual[w],s)
    if any(x!=F.one for x in actual):raise ArithmeticError('COPY coefficient balance failed')
    z,grad=evaluate(weights,top,F,with_marginals);res=F.base_value(z);pins=None
    if grad is not None:
        pins=[];half=F.inv(F.embed(2))
        for eid,(v,i,w,j) in enumerate(edges):
            r,s=rhos[eid];row=[]
            for bit in range(2):
                E=[[F.mul(A[v][i][bit][a],A[w][j][bit][b]) for b in range(2)] for a in range(2)]
                for a in range(2):
                    for b in range(2):
                        if a==0:E[a][b]=F.mul(E[a][b],r)
                        if b==0:E[a][b]=F.mul(E[a][b],s)
                alpha=F.mul(F.add(E[0][0],E[1][1]),half);beta=F.mul(F.add(E[0][1],E[1][0]),half)
                d0,d1=grad[eid];ratio=F.add(F.mul(F.add(alpha,beta),d0),F.mul(F.sub(alpha,beta),d1))
                row.append(F.base_value(F.mul(z,ratio)))
            if sum(row)%p!=res:raise ArithmeticError('original edge pins did not sum to partition')
            pins.extend(row)
    return {**info,'status':'FKT_RESIDUE','residue':res,'pin_residues':pins,'fisher_vertices':3*n,'reference_matching_sign':top['reference_sign'],'faces':top['face_count']}
