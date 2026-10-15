#!/usr/bin/env python3
"""Exact verifier for the global compatible-positivity completion.

Run: python verify_global_structure.py [GLOBAL_COMPLETION_CERTIFICATE.json]
Requires SymPy. Reads no discovery files, pickles, repository, or optimizer.
The analytic theorem is in RESEARCH_REPORT.md; exact algebra is not external review.
"""
from __future__ import annotations
import hashlib
import json
import sys
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import sympy as s


def require(value: bool, label: str) -> None:
    if not value:
        raise AssertionError(label)


def zero(M: s.Matrix) -> bool:
    return all(s.cancel(p) == 0 for p in M)


def load_certificate(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    r = s.Symbol("r", real=True)
    def load(name: str) -> s.Matrix:
        blocks = [s.Matrix([[s.Rational(v) for v in row] for row in block])
                  for block in data[name]]
        require(bool(blocks), name + " nonempty")
        require(all(M.shape == blocks[0].shape for M in blocks), name + " dimensions")
        return (sum((r**i*M for i, M in enumerate(blocks)),
                    s.zeros(*blocks[0].shape))/(r+1)).applyfunc(s.cancel)
    def const(name: str) -> s.Matrix:
        return s.Matrix([[s.Rational(v) for v in row] for row in data[name]])
    return dict(data=data, r=r, C=load("C_numerator"),
                S0=load("S0_numerator"), SK=load("Snull_numerator"),
                W0=load("W0_numerator"), WK=load("Wnull_numerator"),
                SH=const("SH"), N=const("N"), R=const("R"))


def completion_at(p: dict, parameter: s.Rational, method: str = "gershgorin") -> dict:
    """Evaluate an exact sufficient completion at a rational parameter."""
    rr = s.Rational(parameter)
    require(rr*(rr+2) > 0, "completion requires r(r+2)>0")
    r = p["r"]
    order = p["data"]["P6"] + p["data"]["P4"]
    N = p["N"][:, order]
    R = p["R"]
    S0, SK, SH = p["S0"].subs(r, rr), p["SK"].subs(r, rr), p["SH"]
    T10 = N.T*S0*N
    A, B, E = T10[:6,:6], T10[:6,6:], T10[6:,6:]
    K4 = E-B.T*A.inv()*B
    if method == "gershgorin":
        lam = 1+max(sum(abs(K4[i,j]) for j in range(4)) for i in range(4))
    elif method == "trace":
        lam = 1+s.trace(B.T*A.inv()*B)+s.trace(E*E)
    else:
        raise ValueError("method must be 'gershgorin' or 'trace'")
    S1 = S0+lam*SK
    P10, U, V = N.T*S1*N, N.T*S1*R, R.T*S1*R
    K8 = V-U.T*P10.inv()*U
    H8 = R.T*SH*R
    if method == "gershgorin":
        LH,DH = H8.LDLdecomposition(hermitian=False)
        Li = LH.inv()
        KT = Li*K8*Li.T
        mu = 1+max(sum(abs(KT[i,j]) for j in range(8))/DH[i,i] for i in range(8))
    else:
        mu = 1+s.trace((H8.inv()*K8)**2)
    gram = S1+mu*SH
    L, DD = gram.LDLdecomposition(hermitian=False)
    require(L*DD*L.T == gram, "instance LDL reconstruction")
    require(all(v > 0 for v in DD.diagonal()), "instance positive LDL pivots")
    return dict(r=rr, lambda_value=lam, mu_value=mu, alpha_star=4+mu,
                gram_for_subtracted_integrand=gram, omega=p["W0"].subs(r,rr)+lam*p["WK"].subs(r,rr),
                pivots=list(DD.diagonal()), method=method)


def verify(path: Path) -> dict:
    p = load_certificate(path)
    data,r = p["data"],p["r"]
    C,S0,SK,W0,WK,SH,N,R = [p[k] for k in ["C","S0","SK","W0","WK","SH","N","R"]]
    require(data["diffusion"] == [[1,0],[0,1]], "ordinary isotropic heat")
    require(data["polynomial_denominator"] == "r+1", "denominator convention")
    require(C.shape == (24,18) and all(M.shape==(18,18) for M in [S0,SK,SH]), "Gram dimensions")
    require(W0.shape == WK.shape == (6,10), "two-form dimensions")
    require(all(zero(M-M.T) for M in [S0,SK,SH]), "Gram symmetry")
    x=s.Matrix(s.symbols("a b c d",real=True)); a,b,c,d=x
    z=s.Matrix(s.symbols("z0:6",real=True))
    B1=s.Matrix([z[0],z[1],z[3],z[4]])
    B2=s.Matrix([z[1],z[2],z[4],z[5]])
    Z=s.kronecker_product(x,z)
    pairs=list(combinations(range(4),2))
    mons=list(combinations_with_replacement(range(4),2))
    require(data["omega_pairs"] == [list(v) for v in pairs], "two-form pair ordering")
    require(data["omega_monomials"] == [list(v) for v in mons], "two-form monomial ordering")
    mon=s.Matrix([x[i]*x[j] for i,j in mons])
    def omega(W):
        O=s.zeros(4)
        for (i,j), pol in zip(pairs,W*mon): O[i,j]=pol; O[j,i]=-pol
        return O
    def heat(F):
        hh=s.hessian(F,x)
        return s.expand((B1.T*hh*B1)[0]+(B2.T*hh*B2)[0])
    u=a*a+c*c; jj=a*d-b*c; H=((a-d)**2+(b+c)**2)**2
    F=3*H+r*(r-1)*u*u/6+jj*jj+r*u*jj
    ell=((r+1)*C.T*Z).applyfunc(s.expand)
    for S,W,Fv,label in [(S0,W0,F,"base"),(SK,WK,s.S.Zero,"null")]:
        SN=((r+1)*S).applyfunc(s.cancel)
        WN=((r+1)*W).applyfunc(s.cancel)
        O=omega(WN)
        residual=s.expand((ell.T*SN*ell)[0]-(r+1)**3*heat(Fv)-(r+1)**2*(B1.T*O*B2)[0])
        require(residual==0,label+" universal polynomial identity")
        for i,j,k in combinations(range(4),3):
            require(s.expand(s.diff(O[j,k],x[i])-s.diff(O[i,k],x[j])+s.diff(O[i,j],x[k]))==0,label+" closedness")
        primitive=O.T*x/4
        for i,j in pairs:
            require(s.expand(s.diff(primitive[j],x[i])-s.diff(primitive[i],x[j])-O[i,j])==0,label+" primitive")
    require(s.expand((ell.T*SH*ell)[0]-(r+1)**2*heat(H))==0,"distortion heat identity")
    print("PASS: universal base, null-correction, distortion identities; closedness and primitives",flush=True)
    # The natural convex heat Gram for H is a sum of explicitly generated squares.
    natural=s.zeros(24)
    defect=[a-d,b+c]
    defectjets=[[z[0]-z[4],z[1]+z[3]],[z[1]-z[5],z[2]+z[4]]]
    def vec(pol): return s.Matrix([s.expand(pol).coeff(xi).coeff(zi) for xi in x for zi in z])
    for dz in defectjets:
        v0=vec(defect[0]*dz[0]+defect[1]*dz[1]); natural+=8*v0*v0.T
        for h in defect:
            for k in dz:
                vv=vec(h*k);natural+=4*vv*vv.T
    require(zero(C*SH*C.T-natural),"natural distortion SOS")
    pivotrows=[0,3,6,7,9,10,12,13,14,15,16,17,18,19,20,21,22,23]
    require(zero(C[pivotrows,:]-s.eye(18)),"moving basis rank 18")
    require(N.shape==(18,10) and R.shape==(18,8) and N.rank()==10,"quotient dimensions")
    require(SH*N==s.zeros(18,10),"ten-dimensional distortion kernel")
    order=data["P6"]+data["P4"]
    require(sorted(order)==list(range(10)),"quotient permutation")
    NB=N[:,order]
    basis=NB.row_join(R)
    require(basis.det()!=0,"full quotient/complement basis")
    H8=R.T*SH*R
    LH,DH=H8.LDLdecomposition(hermitian=False)
    hp=list(DH.diagonal())
    require(hp==list(map(s.Rational,[12,4,4,s.Rational(32,3),s.Rational(5,2),12,s.Rational(20,3),4])),"eight convex-block pivots")
    require(LH*DH*LH.T==H8 and all(h>0 for h in hp),"convex-block positivity")
    T10=(NB.T*S0*NB).applyfunc(s.cancel)
    q=r*(r+2); ss=r+1
    A6=s.Matrix([
      [2*q/3,0,0,0,0,0],
      [0,2*q/3+2,-2*ss,0,-2*ss,0],
      [0,-2*ss,2*ss**2,0,4*q/3+2,0],
      [0,0,0,2*ss**2,0,0],
      [0,-2*ss,4*q/3+2,0,2*ss**2,0],
      [0,0,0,0,0,2*q/3]])
    require(zero(T10[:6,:6]-A6),"universal six-dimensional acoustic block")
    require(zero(NB.T*SK*NB-s.diag(s.zeros(6),s.eye(4))),"null correction fills only four residual directions")
    LA,DA=A6.LDLdecomposition(hermitian=False)
    ap=[2*q/3,2*(q+3)/3,2*q*ss**2/(q+3),2*ss**2,2*q*(5*q+3)/(9*ss**2),2*q/3]
    require(all(s.cancel(v-w)==0 for v,w in zip(DA.diagonal(),ap)),"six acoustic pivots")
    require(zero(LA*DA*LA.T-A6),"acoustic LDL reconstruction")
    require(s.factor(A6.det()-64*q**4*ss**2*(5*q+3)/243)==0,"acoustic determinant")
    print("PASS: moving rank-18 support; 6+4 quotient completion; rank-8 convex complement",flush=True)
    # Necessary ROC conditions and exact shear-face equations.
    al,be,ga,de,t,h=s.symbols("alpha beta gamma delta t h",real=True)
    FF=al*H+be*u*u+ga*jj*jj+de*u*jj
    point={a:1,b:-h*t,c:h*t,d:1}
    direction=s.Matrix([t,1,0,0])
    ah=(direction.T*s.hessian(FF,x).subs(point)*direction)[0]
    desired=(12*be+2*ga*(1-h)**2+(6-4*h)*de)*t*t+2*h*h*(2*be+de)*t**4
    require(s.expand(ah-desired)==0,"arbitrary acoustic-curve identity")
    acoustic11=s.diff(FF,a,2)
    sub=s.hessian(acoustic11,[b,c])/2
    expect=s.Matrix([[4*al,4*al-de],[4*al-de,4*(al+be)]])
    require(sub==expect and s.expand(sub.det()-(8*al*(2*be+de)-de*de))==0,"strict-side principal minor")
    require(s.diff(FF,b,2).subs({a:0,b:1,c:-1,d:0})==2*ga,"gamma necessity")
    require(FF.subs({a:0,b:1,c:0,d:0})==al,"alpha necessity")
    bv=r*(r-1)/6
    require(s.expand((8*al*(2*be+de)-de**2).subs({be:bv,de:r})-(s.Rational(8,3)*al*q-r*r))==0,"parameter obstruction")
    require(s.expand(F.subs({a:1,b:0,c:0,d:1})-(r+2)*(r+3)/6)==0,"conformal negative values")
    v=b*b+d*d;w=a*b+c*d
    fb=[u*u,v*v,u*v,w*w,u*w,v*w,u*jj,v*jj,w*jj]
    coeff=s.symbols("f0:9");full=sum(c0*b0 for c0,b0 in zip(coeff,fb));n,m=s.symbols("n m")
    rr=s.Matrix([n,m,0,0]);ac=(rr.T*s.hessian(full,x)*rr)[0]
    pt={a:1,b:0,c:0,d:1,n:0,m:1}
    eq=[s.diff(ac,y).subs(pt) for y in list(x)+[n,m]]
    CM,_=s.linear_eq_to_matrix(eq,coeff)
    require(CM.rank()==5,"shear-contact codimension five")
    # Compare the kernel to the coefficient vectors of H,u²,j²,uj directly.
    basis_coeff=s.Matrix.hstack(s.Matrix([1,1,6,-4,0,0,-4,-4,0]),
                                s.Matrix([1,0,0,0,0,0,0,0,0]),
                                s.Matrix([0,0,1,-1,0,0,0,0,0]),
                                s.Matrix([0,0,0,0,0,0,1,0,0]))
    require(basis_coeff.rank()==4 and CM*basis_coeff==s.zeros(6,4),"entire shear-contact linear space")
    gamma0=de*de/(6*be+de);r0=(6*be+de)/de
    lower=gamma0*(al/gamma0*H+r0*(r0-1)/6*u*u+jj*jj+r0*u*jj)+(ga-gamma0)*jj*jj
    require(s.cancel(lower-FF)==0,"full coefficient projection decomposition")
    print("PASS: full shear-face projection identities and genuine r=-2 obstruction",flush=True)
    # Actual compatible periodic trajectory with negative integrated heat dissipation for det².
    X,Y,k=s.symbols("X Y k",nonzero=True)
    ii=s.I
    sx=(X-X**-1)/(2*ii);sy=(Y-Y**-1)/(2*ii)
    cx=(X+X**-1)/2;cy=(Y+Y**-1)/2
    c2x=(X**2+X**-2)/2;c2y=(Y**2+Y**-2)/2
    f=k*(sx+sy)
    g=-k**4*(c2x+c2y)/2+2*k**2*sx*sy
    dx=lambda P:s.expand(ii*X*s.diff(P,X))
    dy=lambda P:s.expand(ii*Y*s.diff(P,Y))
    dt=lambda P:s.expand(-k*s.diff(P,k))
    require(s.expand(dt(f)-dx(dx(f))-dy(dy(f)))==0,"first component heat equation")
    require(s.expand(dt(g)-dx(dx(g))-dy(dy(g)))==0,"second component heat equation")
    AF=s.Matrix([dx(f),dy(f),dx(g),dy(g)])
    JF=s.expand(AF[0]*AF[3]-AF[1]*AF[2])
    require(s.expand(JF-2*(k**3-k**5)*cx*cy*(sx-sy))==0,"exact compatible determinant")
    ct=lambda pol:s.expand(pol).coeff(X,0).coeff(Y,0)
    energy=s.factor(ct(JF*JF))
    require(s.expand(energy-(k**3-k**5)**2/2)==0,"normalized torus energy")
    ep=s.factor(dt(energy))
    require(s.expand(ep-k**6*(1-k*k)*(5*k*k-3))==0,"positive energy derivative formula")
    k0=s.Rational(9,10);ev=s.Rational(212044959,2000000000)
    require(ep.subs(k,k0)==ev and ev>0,"exact positive derivative")
    AA=AF.subs(k,k0)
    JH=s.hessian(jj*jj,x).subs(dict(zip(x,AA)))
    DX=AA.applyfunc(dx);DY=AA.applyfunc(dy)
    diss=ct((DX.T*JH*DX)[0]+(DY.T*JH*DY)[0])
    require(s.expand(diss)+ev==0,"direct negative integrated Hessian dissipation")
    print("PASS: actual compatible det² heat trajectory, exact negative dissipation",flush=True)
    instances=[]
    for parameter in [s.Rational(-11,4),s.Rational(-9,4),s.Rational(1,2)]:
        ex=completion_at(p,parameter)
        instances.append({key:str(ex[key]) for key in ["r","lambda_value","mu_value","alpha_star"]})
    example=completion_at(p,s.Rational(-11,4))
    require(example["alpha_star"]<27,"simple alpha=27 example sufficient")
    sex=S0.subs(r,-s.Rational(11,4))+example["lambda_value"]*SK.subs(r,-s.Rational(11,4))+23*SH
    L,Dex=sex.LDLdecomposition(hermitian=False)
    require(L*Dex*L.T==sex and all(v>0 for v in Dex.diagonal()),"alpha=27 subtraction certificate")
    # Exact lifted Jensen witness, not a compatible-gradient counterexample.
    FI=-s.Rational(1,32)
    FJ=s.Rational(13999,32)
    M=s.Integer(120)
    expected=M*M/(1+M*M)*(M*M*FI+FJ)
    require(expected==-s.Rational(180450,14401),"example lifted Jensen witness")
    simple={"r":"-11/4","alpha":"27","subtracted_H":"1",
            "nonpolyconvex_witness":{"M":"120","F_I":"-1/32","F_J":"13999/32",
                 "mean_matrix":"0","mean_determinant":"0","expected_energy":str(expected),
                 "law":"each +/- M I has mass 1/[2(1+M^2)]; each +/- diag(1,-1) has mass M^2/[2(1+M^2)]"},
            "lambda":str(example["lambda_value"]),
            "positive_ldl_pivots":[str(v) for v in Dex.diagonal()],
            "integrand":"27 H + (55/32) u^2 + j^2 - (11/4) u j",
            "integrated_margin":"4/1875"}
    path.with_name("SIMPLE_NONPOLYCONVEX_EXAMPLE.json").write_text(json.dumps(simple,indent=2)+"\n",encoding="utf-8")
    print("PASS: exact rational completions and alpha=27 non-polyconvex example",flush=True)
    return dict(status="EXACT_ALGEBRA_PASS",certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                sympy_version=s.__version__,diffusion="identity",universal_identities=True,closedness=True,
                primitive=True,moving_rank=18,distortion_rank=8,quotient_split=[6,4],
                acoustic_pivots=[str(s.factor(v)) for v in ap],convex_pivots=[str(v) for v in hp],
                parameter_condition="r*(r+2)>0",shear_projection_identities=True,
                determinant_square_heat_derivative=str(ev),determinant_square_dissipation=str(-ev),
                exact_instances=instances,scope="Exact finite algebra. Universal positivity uses the two Schur-complement arguments in RESEARCH_REPORT.md. Analytic correctness, external review, and priority are separate.")


if __name__ == "__main__":
    try:
        source=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name("GLOBAL_COMPLETION_CERTIFICATE.json")
        receipt=verify(source)
        target=source.with_name("GLOBAL_VERIFICATION.json")
        target.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
        print(f"EXACT_ALGEBRA_PASS: {target}")
    except Exception as exc:
        print(f"VERIFICATION FAILED: {exc}",file=sys.stderr)
        raise
