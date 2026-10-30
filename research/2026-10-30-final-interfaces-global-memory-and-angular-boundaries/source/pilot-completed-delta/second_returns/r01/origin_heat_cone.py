#!/usr/bin/env python3
"""Exact regular-origin heat certificate cone for |A|^4+c det(A)^2.

No optimizer or numerical premise. Requires SymPy only. The theorem for
arbitrary C2-origin closed forms uses the Taylor reduction in PROOF.txt.
"""
from itertools import product,combinations
from pathlib import Path
import sympy as s

A=s.symbols('a b c d',real=True)
a,b,c,d=A
cc,u,v,rho=s.symbols('cc u v rho',real=True)
T=sum(z*z for z in A);q=a*d-b*c
theta=s.Matrix([-b,a,-d,c])
chi=s.Matrix([-c,-d,a,b])


def zero(M):return all(s.expand(x)==0 for x in M)


def density(F,P):
    H=s.hessian(F,A)
    W=s.Matrix(4,4,lambda i,j:s.diff(P[j],A[i])-s.diff(P[i],A[j]))
    C=s.zeros(6);p1,p2=(0,1,3,4),(1,2,4,5)
    for p in (p1,p2):
        for i in range(4):
            for j in range(4):C[p[i],p[j]]+=H[i,j]
    for i in range(4):
        for j in range(4):
            C[p1[i],p2[j]]+=W[i,j]/2
            C[p2[j],p1[i]]+=W[i,j]/2
    return C.applyfunc(s.expand),W


def symmetry_dimension():
    mon=[s.prod(x**j for x,j in zip(A,e))
         for e in product(range(4),repeat=4) if sum(e)==3]
    z=s.symbols('z:80')
    P=s.Matrix([sum(z[20*i+j]*m for j,m in enumerate(mon)) for i in range(4)])
    L=s.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
    R=s.Matrix([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]])
    equations=list(P.jacobian(A)*L*s.Matrix(A)+L.T*P)
    equations+=list(P.jacobian(A)*R*s.Matrix(A)+R.T*P)
    for signs,character in [((1,1,-1,-1),1),((1,-1,1,-1),-1)]:
        for i in range(4):
            equations.append(signs[i]*P[i].subs(dict(zip(A,[sgn*x for sgn,x in zip(signs,A)])),simultaneous=True)-character*P[i])
    rows=[]
    for pp in equations:rows+=s.Poly(s.expand(pp),*A).coeffs()
    M,_=s.linear_eq_to_matrix(rows,z)
    basis=s.Matrix.hstack(*(s.Matrix([s.Poly(Pi,*A).coeff_monomial(m)
                            for Pi in pp for m in mon]) for pp in (T*theta,q*chi)))
    assert M.rank()==78 and basis.rank()==2 and zero(M*basis)
    return M.shape,78,2


def main():
    dims=symmetry_dimension()
    F=T*T+cc*q*q
    C,W=density(F,u*T*theta+v*q*chi)
    canonical=C.subs({a:1,b:0,c:0,d:rho}).applyfunc(s.expand)
    # Finite necessary inequalities at rank-one and conformal matrices.
    at0=canonical.subs(rho,0)
    assert s.expand(at0.extract((0,2),(0,2)).det()-(48-4*u*u))==0
    assert s.expand(at0.extract((3,5),(3,5)).det()-(8*cc+16-(u-v/2)**2))==0
    h=s.Matrix([1,0,-1,0,-1,0])
    assert s.expand((h.T*canonical.subs(rho,1)*h)[0]-4*(8-2*cc-2*u-v))==0
    assert at0[5,5]==2*cc+4
    root=s.sqrt(3)
    cstar=12+8*root
    endpoint={cc:cstar,u:-2*root,v:-16-12*root}
    endpointC=canonical.subs(endpoint).applyfunc(s.expand)
    I,J=(0,2,4),(1,3,5)
    first,second=endpointC.extract(I,I),endpointC.extract(J,J)
    reverse=s.Matrix([[0,0,1],[0,1,0],[1,0,0]])
    assert zero(second-rho*rho*reverse*first.subs(rho,1/rho)*reverse)
    assert s.simplify(first.det())==0
    minors={}
    for size in (1,2,3):
        for ids in combinations(range(3),size):
            minors[ids]=s.factor(first.extract(ids,ids).det(),extension=root)
    assert s.simplify(minors[(0,)]-(12+(28+16*root)*rho*rho))==0
    assert s.simplify(minors[(1,)]-4*(1+rho*rho))==0
    assert s.simplify(minors[(2,)]-(16+8*root)*(1+rho*rho))==0
    assert s.simplify(minors[(0,1)]-128*(2+root)*rho*rho)==0
    assert s.simplify(minors[(1,2)]-(64+32*root)*(1+rho*rho)**2)==0
    assert s.simplify(minors[(0,2)]-(832+480*root)*(rho*rho+3-2*root)**2)==0
    # Combining the three necessary inequalities gives this exact endpoint.
    assert s.expand((cc-4-4*root)**2-(8*cc+16)-(cc-4)*(cc-cstar))==0
    # Explicitly exhibit the nonclosed pointwise correction that cancels all
    # determinant curvature, illustrating why closedness is an obligation.
    sigma=s.zeros(4)
    sigma[0,2]=sigma[1,3]=1
    sigma[2,0]=sigma[3,1]=-1
    nonclosed=-4*cc*q*sigma
    defect=s.diff(nonclosed[1,2],a)-s.diff(nonclosed[0,2],b)+s.diff(nonclosed[0,1],c)
    assert s.expand(defect+4*cc*c)==0
    hh=s.symbols('h:6',real=True)
    B1=s.Matrix([hh[i] for i in (0,1,3,4)])
    B2=s.Matrix([hh[i] for i in (1,2,4,5)])
    H=s.hessian(F,A)
    nc_density=(B1.T*H*B1)[0]+(B2.T*H*B2)[0]+(B1.T*nonclosed*B2)[0]
    cofq=s.Matrix([d,-c,-b,a])
    squares=sum(8*(s.Matrix(A).dot(Bj))**2+4*T*Bj.dot(Bj)
                +2*cc*(cofq.dot(Bj))**2 for Bj in (B1,B2))
    assert s.expand(nc_density-squares)==0
    lines=[
        'EXACT C2-ORIGIN CLOSED HEAT CERTIFICATE CONE',
        'For F=|A|^4+cc det(A)^2, a C2-origin closed heat correction exists iff -2 <= cc <= 12+8 sqrt(3).',
        'Equivalently F_(0,r) admits such a correction iff 1/2 <= r <= 4+2 sqrt(3).',
        'Cubic invariant primitive coefficient dimension: '+str(dims),
        'All averaged cubic primitives are u*T*theta+v*q*chi.',
        'Necessary inequalities: cc>=-2; u^2<=12; (u-v/2)^2<=8cc+16; 2cc+2u+v<=8.',
        'Endpoint primitive: u=-2sqrt(3), v=-16-12sqrt(3).',
        'Endpoint corrected density splits into two 3x3 blocks; each is PSD for every real rho.',
        'First block = '+str(first),
        'First block principal minors:',
    ]
    lines += [str(ids)+' : '+str(value) for ids,value in minors.items()]
    lines += [
        'Second block is rho^2 times the reversed first block at 1/rho, with continuity at zero.',
        'All intermediate coefficients follow by convex interpolation with F_(cc=-2)=Tr((A^T A)^2).',
        'The obstruction beyond the endpoint covers every polynomial primitive and every closed form C2 near the zero matrix, by the origin Taylor lemma.',
        'The nonclosed correction -4cc*q*(da wedge dc+db wedge dd) is pointwise positive for cc>=0 but has nonzero exterior derivative. Its selected dOmega component = '+str(defect)+'.',
        'Its density is exactly sum_j [8(A:B_j)^2+4T|B_j|^2+2cc(cof A:B_j)^2], strictly positive for nonzero compatible Hessian pairs when A!=0 and cc>=0.',
        'This is a classification of a regular-origin heat proof, not a quasiconvexity classification: the full cc>=-2 family is already polyconvex.',
    ]
    output='\n'.join(lines)+'\n'
    (Path(__file__).resolve().parent/'ORIGIN_CONE_RESULTS.txt').write_text(output)
    print(output)


if __name__=='__main__':main()
