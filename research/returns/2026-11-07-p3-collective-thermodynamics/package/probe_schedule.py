"""Finite positive-time derivative acquisition with exact rational nodes.

The analytic remainder is independent of N under a supplied local incidence
bound. The source supplying the individual records has a separate paid cost.
"""
from fractions import Fraction as Q
from math import factorial,prod


def arctan_bounds(x,tol):
    total=Q(0); power=x; n=0
    while True:
        term=power/(2*n+1)
        total+=term if n%2==0 else -term
        power*=x*x; n+=1
        remainder=power/(2*n+1)
        if remainder<=tol:
            return (total,total+remainder) if n%2==0 else (total-remainder,total)


def pi_bounds(tol):
    a,b=arctan_bounds(Q(1,5),tol/40)
    c,d=arctan_bounds(Q(1,239),tol/40)
    return 16*a-4*d,16*b-4*c


def lobatto_nodes(R,T):
    assert R>=1
    bits=0
    while Q(1,1<<bits)>Q(1,256*R**3): bits+=1
    tol=Q(1,1<<(bits+8)); pl,pu=pi_bounds(tol)
    pm=(pl+pu)/2; out=[Q(0)]
    for j in range(1,R):
        x=pm*j/R; total=Q(1); term=Q(1); n=0
        while True:
            n+=1; term*=-x*x/((2*n-1)*(2*n)); total+=term
            rem=(Q(4)**(2*n+2))/factorial(2*n+2)
            if rem<=tol: break
        node=(1-total)/2
        m=1<<bits
        v=(2*node.numerator*m+node.denominator)//(2*node.denominator)
        rounded=Q(v,m)
        err=(pu-pl)/2+rem/2+Q(1,2*m)
        assert err<=Q(1,16*R**3)
        out.append(T*rounded)
    out.append(T)
    assert all(a<b for a,b in zip(out,out[1:]))
    return out,bits


def derivative_weights(nodes):
    weights=[]
    for j,t in enumerate(nodes):
        if j==0: weights.append(-sum((1/x for x in nodes[1:]),Q(0)))
        else:
            weights.append(prod(-x/(t-x) for l,x in enumerate(nodes) if l not in (0,j))/t)
    assert sum(weights)==0
    assert sum(w*t for w,t in zip(weights,nodes))==1
    return weights


def schedule(K,C,zeta):
    C=Q(C); zeta=Q(zeta)
    assert K>=1 and C>0 and zeta>0
    J=K*C; T=1/(16*K*J)
    R=1
    while 1/(2*T*3**R)>zeta/2: R+=1
    nodes,bits=lobatto_nodes(R,T)
    weights=derivative_weights(nodes); W=sum(abs(w) for w in weights)
    assert W<=4*R*R/T
    bias=1/(2*T*3**R); gamma=zeta/(2*W)
    return {'K':K,'C':C,'J':J,'T':T,'R':R,'node_bits':bits,
            'nodes':nodes,'weights':weights,'W':W,'bias':bias,
            'record_radius':gamma,'gradient_error':(bias+W*gamma)/2}
