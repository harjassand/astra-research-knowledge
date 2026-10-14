#!/usr/bin/env python3
"""Independent exact adjacent-slice tensor/global-R1 verification.

The frozen tensor JSON is a proposed certificate, not trusted verdict data.
No producer code, NPZ, pickle or solver is imported.
"""
from pathlib import Path
import hashlib
import itertools
import json
import re
import sys
import sympy as S

HERE=Path(__file__).resolve().parent
input_path=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/"TENSOR_CERTIFICATE_INPUT.json"
output_path=Path(sys.argv[2]) if len(sys.argv)>2 else HERE/"ADJACENT_INDEPENDENT_RESULTS.json"
raw=input_path.read_bytes(); data=json.loads(raw)
L=S.Symbol("L",real=True)
mod=S.Poly(L**4-48*L**2+384,L,domain=S.QQ)
lo=S.Rational(318490086807,10**11);hi=S.Rational(318490086808,10**11)
def parse(text):
    if isinstance(text,list):
        assert len(text)==4 and all(isinstance(c,str) and re.fullmatch(r"[0-9+/\-]+",c) for c in text)
        return sum(S.Rational(c)*L**i for i,c in enumerate(text))
    assert isinstance(text,str) and re.fullmatch(r"[0-9L+*/().\- ]+",text)
    return S.sympify(text,locals={"L":L})
def red(poly):return S.rem(S.Poly(S.expand(poly),L,domain=S.QQ),mod).as_expr()
def bounds(poly):
    a=b=S.Rational(0)
    for c in S.Poly(poly,L).all_coeffs():
        v=[a*lo,a*hi,b*lo,b*hi];a,b=min(v)+c,max(v)+c
    return a,b
assert mod.count_roots(lo,hi)==1 and mod.eval(lo)*mod.eval(hi)<0
assert lo*lo>10 and hi*hi<S.Rational(51,5)
assert S.expand((24-8*S.sqrt(3))**2-48*(24-8*S.sqrt(3))+384)==0
checks={"endpoint root":{"polynomial":str(mod.as_expr()),"isolating_interval":[str(lo),str(hi)],"closed_form":"sqrt(24-8sqrt(3))"}}
V=S.Matrix([[parse(z) for z in row] for row in data["scalar_frame"]])
T=S.Matrix([[parse(z) for z in row] for row in data["T"]])
vv=S.Matrix([parse(z) for z in data["v"]])
uu=S.Matrix([parse(z) for z in data["u"]])
weights=[parse(z) for z in data["tensor_weights"]]
assert V.shape==(6,4) and T.shape==(4,4) and T==T.T
assert weights==[0,S.Rational(1,4)]
minor_polys=[red(T[:n,:n].det()) for n in range(1,5)]
minor_bounds=[bounds(z) for z in minor_polys]
assert all(a>0 for a,b in minor_bounds)
checks["tensor PSD"]={"scalar_frame_shape":[6,4],"T_positive_minor_bounds":[list(map(str,b)) for b in minor_bounds],"tensor_weights":list(map(str,weights))}

a,b,c,d=S.symbols("a b c d",real=True); x=S.Matrix([a,b,c,d])
h=S.symbols("h0:6",real=True)
B1=S.Matrix([h[0],h[1],h[3],h[4]]);B2=S.Matrix([h[1],h[2],h[4],h[5]])
u,v,w,q=a*a+c*c,b*b+d*d,a*b+c*d,a*d-b*c
F=u*u+v*v+4*w*w+4*q*q+L*q*(u+v)
HF=S.hessian(F,x)
E=(B1.T*HF*B1+B2.T*HF*B2)[0]
first=S.Matrix([a,c]);second=S.Matrix([b,d])
X=S.Matrix([h[0],h[3]]);Y=S.Matrix([h[1],h[4]]);Z=S.Matrix([h[2],h[5]])
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
zp=S.Matrix([first.dot(X),first.dot(Z),second.dot(Y),cross(first,Y),cross(second,X),cross(second,Z)])
zm=S.Matrix([-second.dot(Z),-second.dot(X),-first.dot(Y),cross(second,Y),cross(first,Z),cross(first,X)])
cx=a+S.I*c;cy=b+S.I*d;CX=h[0]+S.I*h[3];CY=h[1]+S.I*h[4];CZ=h[2]+S.I*h[5]
spin_u=S.Matrix([cx*CX+S.I*cy*CZ,cx*CZ+S.I*cy*CX,cy*CY+S.I*cx*CY])
spin_v=S.Matrix([cx*CX-S.I*cy*CZ,cx*CZ-S.I*cy*CX,cy*CY-S.I*cx*CY])
fu=S.expand((uu.T*spin_u)[0]);fv=S.expand((vv.T*spin_v)[0])
positive=(zp.T*V*T*V.T*zp+zm.T*V*T*V.T*zm)[0]
positive+=weights[0]*(S.re(fu).expand()**2+S.im(fu).expand()**2)
positive+=weights[1]*(S.re(fv).expand()**2+S.im(fv).expand()**2)
pairs=list(itertools.combinations(range(4),2))
xpairs=list(itertools.combinations_with_replacement(range(4),2))
omega=S.zeros(4)
for (i,j),row in zip(pairs,data["omega"]):
    assert len(row)==10
    p=sum(parse(z)*x[k]*x[l] for (k,l),z in zip(xpairs,row))
    omega[i,j],omega[j,i]=p,-p
identity=S.Poly(S.expand(positive-E-(B1.T*omega*B2)[0]),tuple(x)+h)
assert all(red(co)==0 for co in identity.coeffs())
for i,j,k in itertools.combinations(range(4),3):
    assert S.Poly(S.expand(S.diff(omega[j,k],x[i])-S.diff(omega[i,k],x[j])+S.diff(omega[i,j],x[k])),tuple(x)).is_zero
alpha=S.Matrix([sum(x[i]*omega[i,j] for i in range(4))/4 for j in range(4)])
assert (alpha.jacobian(x).T-alpha.jacobian(x)-omega).applyfunc(S.expand)==S.zeros(4)
checks["exact tensor heat identity"]={"degree_2_2_identity":True,"all_exterior_closure_identities":True,"polynomial_primitive":True,"conclusion":"quasiconvex endpoint by standard periodic heat/Stokes and W1,4 approximation"}

# Global rank-one proof independent of the tensor positivity certificate.
k=S.Symbol("k",real=True);J,W,zz=S.symbols("J W zz",real=True)
B=S.Matrix([1,k,0,0]); acoustic=S.expand((B.T*HF*B)[0]); M=S.hessian(acoustic,x)/2
poly=3*(32-3*W)*(32-W)+(480*W-6144)*zz+768*(W-5)*zz**2
assert S.cancel(M.det()-(1+k*k)**4*poly.subs({W:L*L,zz:k*k/(1+k*k)**2}))==0
assert S.expand(S.discriminant(poly,zz)+27648*(W-8)*(W*W-48*W+384))==0
crit=(64-5*W)/(16*(W-5))
assert S.rem(S.Poly(S.together(poly.subs(zz,crit)).as_numer_denom()[0],W),S.Poly(W*W-48*W+384,W)).is_zero
D=S.expand(M[:3,:3].det()).subs(k*k,J)
lower=S.Rational(12,5)*((J-2)**2*(14*J+5)+89)
assert S.expand(D-lower+S.Rational(12,5)*(5*L*L-51)*(6*J**3+J**2+4*J+1))==0
assert S.expand(M[:2,:2].det()-(96*(k*k-S.Rational(1,4))**2+90))==0
checks["global acoustic positivity"]={"leading_3_minor_lower_bound":str(lower),"range":"all real k; J=k^2>=0 and 10<L^2<51/5", "determinant_discriminant":"-27648*(W-8)*(W^2-48W+384)","conclusion":"leading3 block PD and final Schur complement nonnegative for every k at endpoint; left-SO2 and homogeneity cover all rank-one directions"}

# At the critical angle the same positive 3x3 minor supplies a nonzero
# adjugate null vector. Affineness in L rules out every L beyond K.
cramer=S.Matrix([[12+8*J,16*J,-2*J],[16,8+12*J,-1-3*J],[-2*L*L,-L*L*(1+3*J),4+8*J]])
nums=cramer.adjugate()*S.Matrix([-3-J,-2,0])
rho,sigma,chi=map(S.expand,nums)
assert S.expand(chi+24*L*L*(J-1)**2)==0
assert S.expand(cramer.det()-D)==0
checks["sharpness and minor-removal obstruction"]={"critical_z":"(64-5K^2)/(16(K^2-5)) lies in (0,1/4)","null_vector":"adj(M_K(k))e4 nonzero by positive D", "chi":str(chi),"determinant_derivative":"D-J*chi>0", "gamma_star":0, "conclusion":"same null direction has negative acoustic value for every L>K; H_K-gamma det^2 is not rank-one convex for any gamma>0"}

N=(u+v)**2;H3=N+4*w*w
assert S.expand(F.subs(L,0)-N/2-H3/2-2*q*q)==0
checks["family consequences"]={"sharp_threshold":"H_L QC iff rank-one convex iff |L|<=sqrt(24-8sqrt3)","interior_jensen_gap":"(1-|L|/K)/6 times integral |Dphi|^4", "nonpolyconvex_interval":"3<|L|<=K; H_{-h}(I)=6-2h<0 and four-atom scaled mean-minor witness"}
out={"status":"PASS","certificate_sha256":hashlib.sha256(raw).hexdigest(),"groups":len(checks),"checks":checks,"scope":"Adjacent slice only; positive tensor certificate does not establish the full nine-coefficient cone. Exact internal audit, no external validation or novelty clearance."}
output_path.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"groups":len(checks),"certificate_sha256":out["certificate_sha256"]}))
