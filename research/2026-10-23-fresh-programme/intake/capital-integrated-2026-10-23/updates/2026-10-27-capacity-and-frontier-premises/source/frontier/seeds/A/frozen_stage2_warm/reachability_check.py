"""Exact complex check of the fixed-output reachability identity.
No assertion about reachable cones at unbounded copy number.
"""
import sympy as s
from itertools import product
import json
R=s.Rational

def dd(a,b):return int(a==b)

def first_pair(a,b,c,d):return dd(a,c)*dd(b,d)

def p2(a,b,c,d):return R(dd(a,b)*dd(c,d),2)

def sector(sign,second):
    inds=list(product(range(3),range(2),range(3),range(2)))
    def entry(r,c):
        a,x,b,y=r;e,z,f,w=c
        first=R(first_pair(a,b,e,f)+sign*dd(a,f)*dd(b,e),2)
        p=p2(x,y,z,w);ident=dd(x,z)*dd(y,w)
        return first*(p if second=='P' else ident-p)
    return s.Matrix(36,36,lambda i,j:entry(inds[i],inds[j]))

PM=sector(-1,'P');QM=sector(-1,'Q');PP=sector(1,'P');QP=sector(1,'Q')

def coords(sig):return [(p*sig).trace()/d for p,d in zip((PM,QM,PP,QP),(3,9,6,18))]

def norm2(c):return s.simplify((c.adjoint()*c).trace())

def qone(c):return s.simplify(norm2(c)-abs(c.trace())**2/2)

def qtwo(c):
    t0=s.Matrix(3,3,lambda a,b:sum(c[i*3+a,i*3+b] for i in range(3)))
    t1=s.Matrix(3,3,lambda a,b:sum(c[a*3+i,b*3+i] for i in range(3)))
    return s.simplify(norm2(c)-(norm2(t0)+norm2(t1))/2+abs(c.trace())**2/4)

def main():
    out=[]
    for m in (0,1):
        N=3**m
        A=s.Matrix(6,N,lambda i,j: (i+2*j+1)%5-2+s.I*((2*i+j)%3-1))
        B=s.Matrix(6,N,lambda i,j: (3*i+j+2)%7-3+s.I*((i+2*j+1)%3-1))
        rho=s.ones(1) if not m else s.Matrix(9,9,lambda i,j:R(2*dd(i,j)-dd(i//3,j%3)*dd(i%3,j//3),15))
        K=s.kronecker_product(A,B);sig=K*rho*K.adjoint()
        a,b,c,d=coords(sig);ell=s.simplify(-3*a+9*b-2*c+6*d)
        # U_a[i,x]=conj(A[i,a;x]); V_a[j,y]=conj(B[j,a;y]).
        U=[s.Matrix(3*N,1,lambda k,j:s.conjugate(A[(k//N)*2+a,k%N])) for a in (0,1)]
        V=[s.Matrix(3*N,1,lambda k,j:s.conjugate(B[(k//N)*2+a,k%N])) for a in (0,1)]
        C=U[0]*V[1].adjoint()-U[1]*V[0].adjoint()
        q=qone(C) if not m else qtwo(C)
        rhs=s.simplify(R(15,2)**(m+1)*ell/5)
        if s.simplify(q-rhs)!=0:raise AssertionError((m,q,rhs))
        out.append({'m':m,'complex_filter_shape':[6,N],'rank_C':C.rank(),'q':str(q),'rhs':str(rhs),'residual':'0'})
    # Independently construct both separable zero states before the group twirl.
    av=s.zeros(6,1);bv=s.zeros(6,1);av[0]=1;av[3]=1;bv[1]=1;bv[2]=-1
    raw=s.kronecker_product(av,bv);internal=coords(raw*raw.adjoint()/4)
    av=s.zeros(6,1);bv=s.zeros(6,1);av[0]=1;bv[0]=1;bv[2]=1
    raw=s.kronecker_product(av,bv);classical=coords(raw*raw.adjoint()/2)
    z=tuple(s.simplify((x+y)/2) for x,y in zip(internal,classical))
    if z!=(R(1,16),R(1,144),R(1,32),R(1,32)):raise AssertionError(z)
    a,b,c,d=z
    pe=((a+b+c+d)/4,(-a+3*b-c+3*d)/4,(-a-b+2*c+2*d)/2,(a-3*b-2*c+6*d)/2)
    if -3*a+9*b-2*c+6*d or min(pe)<=0 or min(z)<=0:raise AssertionError((z,pe))
    print(json.dumps({'scope':'exact fixed-copy algebra checks only','identity_checks':out,
                     'internal_product_twirl_coefficients':[str(x) for x in internal],'classical_product_twirl_coefficients':[str(x) for x in classical],'separable_boundary_z_coefficients':[str(x) for x in z],
                     'z_PPT_sector_eigenvalues':[str(x) for x in pe],
                     'z_minimum_Bound':'1/144','zGamma_minimum_bound':'1/192'},indent=2))

if __name__=='__main__':main()
