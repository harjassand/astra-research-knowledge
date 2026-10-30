"""Exact lower-quadratic ROC classification for the exceptional s=1/3 face.

We multiply the input polynomial by 3 and use conformal coordinates
  z=(a+d,c-b), w=(a-d,c+b).
The leading polynomial is F=|w|^4+2|z|^2|w|^2. No numerical admission.
The finite two-variable sign decision uses projection and exact Sturm counts.
"""
from itertools import combinations
import sympy as S
x,y,u,v=S.symbols('x y u v',real=True)
z=S.Matrix([x,y]);w=S.Matrix([u,v]);VARS=[x,y,u,v]
r=x*x+y*y;t=u*u+v*v;F=t*t+2*r*t
nu=S.Matrix([u*u-v*v,2*u*v])
h,k=S.symbols('h k',real=True)

def normal_form(C,Q):
    """Return V,M,Qnew for p(B-V), or None if no quadratic can make p ROC."""
    vv=S.symbols('V0:4');mm=S.symbols('m0:4');M=S.Matrix(2,2,mm)
    target=sum(S.diff(F,a)*b for a,b in zip(VARS,vv))+(z.T*M*nu)[0]
    equations=S.Poly(S.expand(C-target),VARS).coeffs()
    solutions=S.solve(equations,[*vv,*mm],dict=True)
    if len(solutions)!=1 or any(a not in solutions[0] for a in [*vv,*mm]):return None
    so=solutions[0];VV=S.Matrix([so[a] for a in vv]);MM=M.subs(so)
    Qnew=S.expand(Q-sum(S.diff(C,a)*b for a,b in zip(VARS,VV))+(VV.T*S.hessian(F,VARS)*VV)[0]/2)
    return VV,MM,Qnew

def score_polynomial(M,Q):
    da=1+h*h;db=1+k*k
    a=S.Matrix([1-h*h,2*h])/da;b=S.Matrix([1-k*k,2*k])/db
    nn=S.Matrix([b[0]**2-b[1]**2,2*b[0]*b[1]]);ee=S.Matrix([-nn[1],nn[0]])
    q=Q.subs(dict(zip(VARS,[*a,*b])),simultaneous=True)
    score=8*q-(M*nn).dot(M*nn)-2*(a.dot(M*ee))**2
    return S.Poly(S.cancel(score*da**2*db**4),h,k,domain=S.QQ)

def univariate_nonnegative(poly,var):
    p=S.Poly(poly,var,domain=S.QQ)
    if p.is_zero:return True
    if p.degree()%2 or p.LC()<0:return False
    for factor,multiplicity in p.sqf_list()[1]:
        if multiplicity%2 and factor.count_roots(-S.oo,S.oo):return False
    return True

def projection_polynomial(P):
    """All possible changes of the real-root topology of P(h,k)."""
    if P.is_zero:return S.Poly(1,k)
    factors=[S.Poly(f,h,k) for f,m in P.sqf_list()[1]]
    projections=[];positive_h=[]
    for factor in factors:
        ff=S.Poly(factor.as_expr(),h)
        if ff.degree()==0:projections.append(ff.as_expr());continue
        positive_h.append(ff)
        projections.append(ff.LC())
        if ff.degree()>1:projections.append(S.discriminant(ff.as_expr(),h))
    for p,q in combinations(positive_h,2):projections.append(S.resultant(p.as_expr(),q.as_expr(),h))
    pp=S.Poly(1,k,domain=S.QQ)
    for item in projections:
        pol=S.Poly(item,k,domain=S.QQ)
        if pol.is_zero:raise ArithmeticError('Unexpected zero projection; global squarefree factorization failed')
        if pol.degree():pp=S.lcm(pp,pol.sqf_part())
    return pp.monic()

def finite_nonnegative(P):
    """Complete decision including weak boundaries; returns a negative rational fiber when false.

    A strict negative point has an open neighborhood. It therefore suffices
    to inspect the open projection cells; negative values solely on excluded
    algebraic fibers cannot occur by continuity. Repeated polynomial factors
    are retained in the original P and removed only in the projection.
    """
    projection=projection_polynomial(P)
    if projection.degree()==0:samples=[S.Rational(0)]
    else:
        eps=S.Rational(1,16)
        while True:
            intervals=[pair for pair,m in projection.intervals(eps=eps)]
            if all(intervals[i][1]<intervals[i+1][0] for i in range(len(intervals)-1)):break
            eps/=16
        if not intervals:samples=[S.Rational(0)]
        else:
            samples=[intervals[0][0]-1]
            samples += [(left[1]+right[0])/2 for left,right in zip(intervals,intervals[1:])]
            samples += [intervals[-1][1]+1]
    for sample in samples:
        if not univariate_nonnegative(P.as_expr().subs(k,sample),h):
            return False,{'projection_degree':projection.degree(),'open_cells':len(samples),'negative_fiber_k':sample}
    return True,{'projection_degree':projection.degree(),'open_cells':len(samples)}

def classify(C,Q):
    normal=normal_form(C,Q)
    if normal is None:return False,{'reason':'cubic fails the complete eight-mode acoustic condition'}
    VV,MM,Qnew=normal
    P=score_polynomial(MM,Qnew)
    admitted,info=finite_nonnegative(P)
    info.update(translation=VV,nontranslation=MM,reduced_quadratic=Qnew,score_bidegree=(P.degree(h),P.degree(k)))
    return admitted,info

def main():
    C=x*(u*u-v*v)+2*y*u*v
    for coefficient in [S.Rational(3,16),S.Rational(187,1000),S.Rational(1,4)]:
        ok,info=classify(C,coefficient*(r+t))
        print('Q coefficient',coefficient,'ROC',ok,'finite decision',info)
    # Non-isotropic, genuinely boundary quadratic; determinant lineality is allowed.
    ok,info=classify(0,(x+u)**2+(y+v)**2+3*(r-t))
    print('degenerate quadratic boundary ROC',ok,info)
    # Translation normalization is tested on an arbitrary reduced cubic.
    C0=2*x*(u*u-v*v)+2*y*u*v;Q0=2*(r+t);shift=S.Matrix([1,-2,3,-1]);
    Ctrans=S.expand(C0+sum(S.diff(F,a)*b for a,b in zip(VARS,shift)))
    Qtrans=S.expand(Q0+sum(S.diff(C0,a)*b for a,b in zip(VARS,shift))+(shift.T*S.hessian(F,VARS)*shift)[0]/2)
    nv,nm,nq=normal_form(Ctrans,Qtrans);assert nv==shift and S.expand(nq-Q0)==0 and nm==S.diag(2,1)
    print('exact arbitrary-translation normalization replay passed')
    # General non-diagonal cubic and nonzero cross terms in Q.
    Mgen=S.Matrix([[2,1],[0,1]]);Cgen=(z.T*Mgen*nu)[0]
    Qgen=r+t+(x+u+v)**2/7+(y-2*u)**2/5
    ok,info=classify(Cgen,Qgen);assert ok
    print('general rational M and cross-quadratic ROC',ok,info)
if __name__=='__main__':main()
