"""Exact least-cost composition for a fixed rank-one covariance catalogue.

Inputs are rational: H_i=F''(R_i), G_i with columns grad C_j(R_i),
positive covariance weights w_i, and columns of cubic-moment targets L.
The canonical sources minimize the cost Gram matrix in Loewner order.
A range failure returns an exact annihilator of this fixed catalogue.
"""
from fractions import Fraction as R

class RangeObstruction(ValueError):
    def __init__(self,annihilator,target_values):
        self.annihilator=annihilator;self.target_values=target_values
        super().__init__('Target is outside the range; an exact annihilator is attached.')

def transpose(A):return list(map(list,zip(*A)))
def mm(A,B):return [[sum((x*y for x,y in zip(row,col)),R(0)) for col in zip(*B)] for row in A]
def add(*mats):return [[sum((A[i][j] for A in mats),R(0)) for j in range(len(mats[0][0]))] for i in range(len(mats[0]))]
def scale(A,c):return [[c*x for x in row] for row in A]

def solve_range(A,B):
    """Solve AX=B over Q; free variables are zero. Return X and rank."""
    A=[list(map(R,row)) for row in A];B=[list(map(R,row)) for row in B]
    n,m=len(A),len(A[0]);r=len(B[0]);assert len(B)==n
    rows=[a+bb+[R(int(i==j)) for j in range(n)] for i,(a,bb) in enumerate(zip(A,B))]
    pivot=0;pivots=[]
    for j in range(m):
        k=next((k for k in range(pivot,n) if rows[k][j]),None)
        if k is None:continue
        rows[pivot],rows[k]=rows[k],rows[pivot];p=rows[pivot][j];rows[pivot]=[v/p for v in rows[pivot]]
        for i in range(n):
            if i!=pivot and rows[i][j]:
                co=rows[i][j];rows[i]=[x-co*y for x,y in zip(rows[i],rows[pivot])]
        pivots.append(j);pivot+=1
        if pivot==n:break
    for i in range(pivot,n):
        if any(rows[i][m:m+r]):raise RangeObstruction(rows[i][m+r:],rows[i][m:m+r])
    X=[[R(0) for _ in range(r)] for _ in range(m)]
    for i,j in enumerate(pivots):X[j]=rows[i][m:m+r]
    assert mm(A,X)==B
    return X,pivot

def canonical(hessians,gradients,weights,targets):
    weights=list(map(R,weights));assert all(w>0 for w in weights)
    targets=[list(map(R,row)) for row in targets];d=len(targets);r=len(targets[0]);Ys=[];terms=[]
    for H,G,w in zip(hessians,gradients,weights):
        try:Y,_=solve_range(H,G)
        except RangeObstruction as exc:raise ValueError('A cubic gradient lies outside the acoustic Hessian range.') from exc
        Ys.append(Y);terms.append(scale(mm(transpose(G),Y),w))
    W=add(*terms);V,rank=solve_range(W,targets)
    sources=[scale(mm(Y,V),w) for Y,w in zip(Ys,weights)]
    assert add(*(mm(transpose(G),Z) for G,Z in zip(gradients,sources)))==targets
    cost=scale(mm(transpose(targets),V),R(1,2))
    direct=add(*(scale(mm(transpose(Z),mm(H,Z)),1/(2*w)) for H,Z,w in zip(hessians,sources,weights)))
    assert cost==direct and cost==transpose(cost)
    return {'sources':sources,'cost_matrix':cost,'capacity_matrix':W,'capacity_rank':rank}

def quotient(W,target,f,translation_dimension=4):
    """Remove translation modes from a positive-capacity system exactly."""
    k=translation_dimension;n=len(W);assert len(target)==n
    H=[row[:k] for row in W[:k]];B=[row[k:] for row in W[:k]];D=[row[k:] for row in W[k:]]
    v=[[x] for x in target[:k]];c=[[x] for x in target[k:]];Hv,hrank=solve_range(H,v);HB,_=solve_range(H,B)
    Lambda=add(D,scale(mm(transpose(B),HB),-1));residual=add(c,scale(mm(transpose(B),Hv),-1))
    z,lrank=solve_range(Lambda,residual);a=2*R(f)-mm(transpose(v),Hv)[0][0]
    correlation_cost=mm(transpose(residual),z)[0][0]
    return {'translation_rank':hrank,'translation_block':H,'mixed_block':B,'quotient_capacity':Lambda,'quotient_rank':lrank,'correlation_target':[row[0] for row in residual],'leading_budget_a':a,'correlation_cost':correlation_cost,'quartic_budget':(a-correlation_cost)/2}
