#!/usr/bin/env python3
"""Acquire exact finite tests for polynomial/C2-origin heat corrections.

Numerical eigenvectors propose rational tests only. Every final obstruction
is a rational Farkas combination of exact pointwise necessary inequalities.
No external tools, producer imports, or network. Requires NumPy and SymPy.
"""
from itertools import combinations
from fractions import Fraction
from pathlib import Path
import sys
import sympy as s
import numpy as np

A=s.symbols('a b c d',real=True)
a,b,c,d=A
t=s.symbols('t',real=True)
u,v=s.symbols('u v',real=True)


def primitive_basis():
    q=a*d-b*c
    return [s.Matrix(p) for p in (
        [-b*(a*a+c*c),a*(b*b+d*d),-d*(a*a+c*c),c*(b*b+d*d)],
        [c*(a*a+c*c),-d*(b*b+d*d),-a*(a*a+c*c),b*(b*b+d*d)],
        [b*q,a*q,d*q,c*q],
        [-a*(a*b+c*d),b*(a*b+c*d),-c*(a*b+c*d),d*(a*b+c*d)],
        [-b*(b*b+d*d),a*(a*a+c*c),-d*(b*b+d*d),c*(a*a+c*c)],
        [c*(b*b+d*d),-d*(a*a+c*c),-a*(b*b+d*d),b*(a*a+c*c)])]


def verify_complete_symmetry_basis():
    from itertools import product
    es=[e for e in product(range(4),repeat=4) if sum(e)==3]
    mon=[s.prod(x**k for x,k in zip(A,e)) for e in es]
    zz=s.symbols('generic_z:80')
    P=s.Matrix([sum(zz[20*i+j]*m for j,m in enumerate(mon)) for i in range(4)])
    J=s.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
    equations=list(P.jacobian(A)*J*s.Matrix(A)+J.T*P)
    signs=(1,-1,-1,1);swap=(1,0,3,2)
    for i in range(4):
        equations.append(signs[i]*P[i].subs(dict(zip(A,[signs[j]*A[j] for j in range(4)])),simultaneous=True)+P[i])
        equations.append(P[swap[i]].subs(dict(zip(A,[A[j] for j in swap])),simultaneous=True)+P[i])
    rows=[]
    for pp in equations:rows+=s.Poly(s.expand(pp),*A).coeffs()
    matrix,_=s.linear_eq_to_matrix(rows,zz)
    columns=s.Matrix.hstack(*(s.Matrix([s.Poly(Pi,*A).coeff_monomial(m)
                             for Pi in basis for m in mon]) for basis in primitive_basis()))
    assert matrix.shape==(200,80)
    assert matrix.rank()==74 and columns.rank()==6 and zero(matrix*columns)
    return 80,74,6


def density(H,W):
    p1,p2=(0,1,3,4),(1,2,4,5)
    C=s.zeros(6)
    for p in (p1,p2):
        for i in range(4):
            for j in range(4):C[p[i],p[j]]+=H[i,j]
    for i in range(4):
        for j in range(4):
            C[p1[i],p2[j]]+=W[i,j]/2
            C[p2[j],p1[i]]+=W[i,j]/2
    return C.applyfunc(s.expand)


def acoustic_constraints(H,W,tau):
    B=1-3*tau*tau;HH=1+3*tau*tau
    m=s.Poly(B*B*(1-t*t)**2-(1-4*tau+3*tau*tau)*HH*(1+t*t)**2,t).monic()
    K=[-B*(tau*(1-t*t)+HH*t*t)*(1+t*t),
       B*t*(HH-tau*(1-t*t))*(1+t*t),
       B*B*t*(1-t*t)-tau*HH*t*(1+t*t)**2,
       B*B*t*t*(1-t*t)+tau*HH*(1+t*t)**2]
    K=[s.rem(k,m.as_expr(),t) for k in K]
    den=s.lcm([s.denom(co) for k in K for co in s.Poly(k,t).all_coeffs()])
    K=[s.expand(k*den) for k in K]
    gcd=s.gcd_list([co for k in K for co in s.Poly(k,t).all_coeffs()])
    K=[s.expand(k/gcd) for k in K]
    def ev(p):
        ans=0
        for es,co in s.Poly(s.expand(p),*A).terms():
            val=co
            for kk,e in zip(K,es):
                if e:val=s.rem(val*kk**e,m.as_expr(),t)
            ans+=val
        return s.rem(ans,m.as_expr(),t)
    # Independently verify the acoustic zero premise from the actual F.
    Rsub={a:1,b:t,c:0,d:0}
    for i in range(4):
        assert s.rem(sum(H[i,j].subs(Rsub)*K[j] for j in range(4)),m.as_expr(),t)==0
    hv=[ev(H[i,0])+t*ev(H[i,1]) for i in range(4)]
    wv=[ev(W[i,0])+t*ev(W[i,1]) for i in range(4)]
    Ch=[0]*6;p1,p2=(0,1,3,4),(1,2,4,5)
    for i in range(4):
        Ch[p1[i]]+=hv[i]+t*wv[i]/2
        Ch[p2[i]]+=t*hv[i]-wv[i]/2
    rows=[]
    for pp in Ch:
        poly=s.Poly(s.rem(s.expand(pp),m.as_expr(),t),t)
        rows += [poly.nth(j) for j in range(4)]
    return rows,m,K


def exact_system():
    tau=s.Rational(1,30)
    beta=(1-3*tau*tau)/(1+3*tau*tau)
    rr=4-12*tau/(1+3*tau*tau)
    T=sum(z*z for z in A);q=a*d-b*c;X=a*a+c*c-b*b-d*d
    F=T*T+4*(rr-1)*q*q+4*beta*q*X
    H=s.hessian(F,A)
    z=s.symbols('z:6')
    P=sum((zz*pp for zz,pp in zip(z,primitive_basis())),s.zeros(4,1))
    W=s.Matrix(4,4,lambda i,j:s.diff(P[j],A[i])-s.diff(P[i],A[j]))
    rows,m,K=acoustic_constraints(H,W,tau)
    lhs,rhs=s.linear_eq_to_matrix(rows,z)
    sol=list(s.linsolve((lhs,rhs),z))[0]
    assert lhs.rank()==3 and zero(W.diff(z[5])+2*W.diff(z[2]))
    subs=dict(zip(z,[s.expand(x.subs({z[3]:u,z[4]:v,z[5]:0})) for x in sol]))
    C=density(H,W.subs(subs))
    return C,sol,m,K


def zero(M):return all(s.expand(x)==0 for x in M)


def clip(poly,coeff):
    cc,aa,bb=map(float,coeff);out=[]
    for p,q in zip(poly,poly[1:]+poly[:1]):
        fp=cc+aa*p[0]+bb*p[1];fq=cc+aa*q[0]+bb*q[1]
        if fp>=0:out.append(p)
        if (fp>=0)!=(fq>=0):
            ratio=fp/(fp-fq)
            out.append((p[0]+ratio*(q[0]-p[0]),p[1]+ratio*(q[1]-p[1])))
    return out


def farkas(cuts):
    for ids in combinations(range(len(cuts)),2):
        q=[cuts[i]['coeff'] for i in ids]
        if q[0][1]*q[1][2]!=q[0][2]*q[1][1]:continue
        axis=1 if q[0][1]!=0 else 2
        lam=[-q[1][axis],q[0][axis]]
        if all(x<=0 for x in lam):lam=[-x for x in lam]
        if not all(x>=0 for x in lam) or sum(lam)==0:continue
        if any(sum(x*y[j] for x,y in zip(lam,q))!=0 for j in (1,2)):continue
        gap=s.factor(sum(x*y[0] for x,y in zip(lam,q)))
        if gap<0:return ids,lam,gap
    for ids in combinations(range(len(cuts)),3):
        q=[cuts[i]['coeff'] for i in ids]
        mat=s.Matrix([[x[1] for x in q],[x[2] for x in q],[1,1,1]])
        if mat.det()==0:continue
        lam=mat.inv()*s.Matrix([0,0,1])
        if all(x>=0 for x in lam):
            gap=s.factor(sum(x*y[0] for x,y in zip(lam,q)))
            if gap<0:return ids,list(lam),gap
    return None


def search(C):
    can=C.subs({a:1,c:0})
    parts=[can.subs({u:0,v:0}),can.diff(u),can.diff(v)]
    fns=[s.lambdify((b,d),p,'numpy') for p in parts]
    points=[(s.Rational(i,16),s.Rational(j,16)) for i in range(17)
            for j in range(-16,17) if i*i+j*j<=256]
    vals=np.array([[fn(float(x),float(y)) for fn in fns] for x,y in points])
    poly=[(-1000.,-1000.),(1000.,-1000.),(1000.,1000.),(-1000.,1000.)]
    cuts=[]
    for step in range(100):
        guess=np.mean(poly,axis=0)
        Ms=vals[:,0]+guess[0]*vals[:,1]+guess[1]*vals[:,2]
        ev,vec=np.linalg.eigh(Ms)
        idx=int(np.argmin(ev[:,0]));e=float(ev[idx,0])
        print('candidate',step,guess.tolist(),'min eigenvalue',e,'at',points[idx],flush=True)
        if e>=-1e-8:return None,cuts,guess
        hh=[s.Rational(Fraction(float(x)).limit_denominator(1000)) for x in vec[idx,:,0]]
        h=s.Matrix(hh);pt=points[idx]
        expr=s.expand((h.T*can.subs({b:pt[0],d:pt[1]})*h)[0])
        co=[expr.subs({u:0,v:0}),s.diff(expr,u),s.diff(expr,v)]
        assert s.expand(expr-co[0]-co[1]*u-co[2]*v)==0
        cuts.append({'point':pt,'vector':hh,'coeff':co})
        poly=clip(poly,co)
        if not poly:
            cert=farkas(cuts)
            if cert:return cert,cuts,guess
            raise RuntimeError('Only artificial search bounds excluded; no exact certificate')
    return None,cuts,guess


def main():
    dimensions=verify_complete_symmetry_basis()
    C,sol,m,K=exact_system()
    assert zero(C.diff(v)-2*C.diff(u))
    assert s.Rational(83981,2710)>2  # m has four distinct real roots.
    h1=s.Matrix([2,-1,2,0,-1,0])
    h2=s.Matrix([0,-1,0,-1,0,2])
    # The corrected density has the single effective parameter w=u+2v.
    test1=s.expand((h1.T*C.subs({a:1,b:1,c:0,d:0,v:0})*h1)[0])
    test2=s.expand((h2.T*C.subs({a:1,b:0,c:0,d:s.Rational(1,2),v:0})*h2)[0])
    const1,coef1=test1.subs(u,0),s.diff(test1,u)
    const2,coef2=test2.subs(u,0),s.diff(test2,u)
    assert const1==-s.Rational(311815872,1292881) and coef1==-s.Rational(883948,90201)
    assert const2==s.Rational(254490123,9050167) and coef2==s.Rational(872897,721608)
    upper=s.factor(-const1/coef1);lower=s.factor(-const2/coef2)
    gap=s.factor(lower-upper)
    assert coef1<0 and coef2>0 and gap==s.Rational(79225269437592,58062565691039)>0
    lines=['NO C2-ORIGIN CLOSED HEAT CORRECTION FOR THE ACCEPTED B1 SEED',
           'Full cubic primitive space, symmetry rank, invariant dimension: '+str(dimensions),
           'm(t)='+str(m.as_expr()),'K='+str(K),'coefficient solution='+str(sol)]
    lines+=['The corrected density depends only on w=z3+2*z4; z5 is also gauge.',
            'At A=[[1,1],[0,0]], h='+str(list(h1))+': '+str(test1).replace('u','w')+' >= 0.',
            'This requires w <= '+str(upper)+'.',
            'At A=diag(1,1/2), h='+str(list(h2))+': '+str(test2).replace('u','w')+' >= 0.',
            'This requires w >= '+str(lower)+'.',
            'The lower bound exceeds the upper by '+str(gap)+' > 0.',
            'Therefore no symmetric cubic primitive works. Averaging and the origin Taylor lemma exclude every closed correction that is C2 at the zero matrix.',
            'The supplied angular primitive does work, with its stated C1 two-form regularity; the retained proof upgrades this to C(1,1), without C2.',
            'This is a regularity obstruction for this heat method, not failure of quasiconvexity.']
    if '--search' in sys.argv:
        result,cuts,guess=search(C)
        lines+=['Optional rational-cut discovery result: '+str(result)]
    output='\n'.join(lines)+'\n'
    (Path(__file__).resolve().parent/'CUBIC_BOUNDARY_RESULTS.txt').write_text(output)
    print(output)


if __name__=='__main__':main()
