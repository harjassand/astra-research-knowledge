"""No-supplied-basis generic ternary parity-gauge recognition, exact local fields."""
from fractions import Fraction as Q
from math import lcm,prod
from fields import Rational,Prime,Quadratic,Degenerate


def det(A,F):return F.sub(F.mul(A[0][0],A[1][1]),F.mul(A[0][1],A[1][0]))
def inv(A,F):
    d=F.inv(det(A,F));return [[F.mul(A[1][1],d),F.neg(F.mul(A[0][1],d))],[F.neg(F.mul(A[1][0],d)),F.mul(A[0][0],d)]]
def transpose(A):return [list(row) for row in zip(*A)]
def mm(A,B,F):return [[F.add(F.mul(A[i][0],B[0][j]),F.mul(A[i][1],B[1][j])) for j in range(2)] for i in range(2)]

def pencil(T,B):
    T0=[[B.embed(T[2*j+k]) for k in range(2)] for j in range(2)]
    T1=[[B.embed(T[4+2*j+k]) for k in range(2)] for j in range(2)]
    chosen=None
    for lam in (0,1,-1):
        A=[[B.add(T0[i][j],B.mul(B.embed(lam),T1[i][j])) for j in range(2)] for i in range(2)]
        if det(A,B)!=B.zero:chosen=(lam,A);break
    if chosen is None:raise Degenerate('no invertible ternary pencil slice')
    lam,A=chosen;M=mm(T1,inv(A,B),B);tr=B.add(M[0][0],M[1][1]);delta=B.sub(B.mul(tr,tr),B.mul(B.embed(4),det(M,B)))
    if delta==B.zero:raise Degenerate('zero ternary hyperdeterminant/pencil discriminant')
    return lam,A,M,delta

def cp(T,B,F,pen=None):
    lam,A,M,delta=pen or pencil(T,B);a=[[F.embed(v) for v in row] for row in A];m=[[F.embed(v) for v in row] for row in M]
    root=F.sqrt_base(delta);half=F.inv(F.embed(2));tr=F.add(m[0][0],m[1][1]);mus=[F.mul(F.add(tr,root),half),F.mul(F.sub(tr,root),half)]
    if M[0][1]!=B.zero:U=[[m[0][1],m[0][1]],[F.sub(mu,m[0][0]) for mu in mus]]
    elif M[1][0]!=B.zero:U=[[F.sub(mu,m[1][1]) for mu in mus],[m[1][0],m[1][0]]]
    else:
        U=[[F.one,F.zero],[F.zero,F.one]];mus=[m[0][0],m[1][1]]
    V=transpose(mm(inv(U,F),a,F));first=[[F.sub(F.one,F.mul(F.embed(lam),mu)) for mu in mus],mus]
    mats=[first,U,V]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                value=F.add(F.mul(F.mul(first[i][0],U[j][0]),V[k][0]),F.mul(F.mul(first[i][1],U[j][1]),V[k][1]))
                if value!=F.embed(T[4*i+2*j+k]):raise ArithmeticError('CP tensor identity failed')
    if any(det(A,F)==F.zero for A in mats):raise ArithmeticError('CP factor singular')
    return mats

def determinant_quadratic(T,leg,x,F):
    other=[j for j in range(3) if j!=leg];A=[[F.zero]*2 for _ in range(2)]
    for i in range(2):
        for j in range(2):
            bits=[0,0,0];bits[other[0]]=i;bits[other[1]]=j
            bits[leg]=0;a=T[4*bits[0]+2*bits[1]+bits[2]];bits[leg]=1;b=T[4*bits[0]+2*bits[1]+bits[2]]
            A[i][j]=F.add(F.mul(x[0],F.embed(a)),F.mul(x[1],F.embed(b)))
    return det(A,F)

def clear_input(data):
    ts=[];Ds=[]
    for raw in data['tensors']:
        if len(raw)!=8:raise ValueError('eight entries per ternary tensor required')
        vals=[Q(v) for v in raw];D=lcm(*(x.denominator for x in vals));ts.append([int(x*D) for x in vals]);Ds.append(D)
    n=len(ts);ports=[[None]*3 for _ in range(n)]
    for eid,edge in enumerate(data['edges']):
        if len(edge)!=4:raise ValueError('edges are [vertex,port,vertex,port]')
        v,i,w,j=edge
        if any(type(x) is not int for x in edge) or v==w or not (0<=v<n and 0<=w<n and 0<=i<3 and 0<=j<3):raise ValueError('bad edge/loop')
        if ports[v][i] is not None or ports[w][j] is not None:raise ValueError('duplicate port')
        ports[v][i]=(eid,w,j);ports[w][j]=(eid,v,i)
    if any(p is None for row in ports for p in row):raise ValueError('every ternary port needs exactly one edge')
    bound=(1<<len(data['edges']))*prod(max(map(abs,t)) for t in ts)
    return ts,Ds,ports,bound

def recognize(ts,ports):
    """Complete in the nonzero-hyperdeterminant/nonzero-CP-edge class.
    No global algebraic coefficient field or supplied gauge is built.
    """
    B=Rational();locals=[];bad=1
    def charge(q):
        nonlocal bad
        q=Q(q)
        if q:bad*=abs(q.numerator)*q.denominator
    for v,T in enumerate(ts):
        pen=pencil(T,B);F=Quadratic(pen[3]);A=cp(T,B,F,pen);locals.append((F,A,pen))
        charge(pen[3]);charge(det(pen[1],B))
        for row in pen[2]:
            for x in row:charge(x)
        for mat in A:
            for row in mat:
                for x in row:
                    for coef in x:charge(coef)
    receipts=[]
    for v,(F,A,pen) in enumerate(locals):
        P=[F.one,F.one];qs=[]
        for leg,(_,w,wleg) in enumerate(ports[v]):
            row=[]
            for s in range(2):
                x=[A[leg][i][s] for i in range(2)];q=determinant_quadratic(ts[w],wleg,x,F);norm=F.norm(q)
                if not norm:raise Degenerate('zero CP-edge entry: outside generic recognition promise')
                charge(norm)
                for coef in q:charge(coef)
                P[s]=F.mul(P[s],q);row.append(list(map(str,q)))
            qs.append(row)
        if P[0]!=P[1]:return {'recognized':False,'reason':'LOCAL_BALANCE_FAILED','vertex':v,'delta':str(F.delta),'P0':list(map(str,P[0])),'P1':list(map(str,P[1]))},bad
        receipts.append({'vertex':v,'delta':str(F.delta),'pencil_lambda':pen[0],'neighbor_quadratic_values':qs,'P0_equals_P1':list(map(str,P[0]))})
    return {'recognized':True,'scope':'generic ternary parity-gauge class; no hardness conclusion outside it','local_certificates':receipts},bad
