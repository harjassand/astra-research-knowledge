#!/usr/bin/env python3
"""Independent exact tests: bounded-center -logdet learner (not performance evidence)."""
from pathlib import Path
from hashlib import sha256
import json
import sympy as s

HERE=Path(__file__).resolve().parent
SOURCE=HERE/'ordinary_prequential_bounded_center_precision_20261028.md'
EXPECTED='35efeef37e8ae0ed38b0b8d6a049cd98c15c8143b81e79565921fdfdf1333f4c'
INITIAL=HERE/'ordinary_prequential_bounded_center_precision_20261028_initial.md'
assert sha256(INITIAL.read_bytes()).hexdigest()=='cd891307be95358ee5102394c259c2c30717813d084e7d75d03f2f6ff04e2ef5'
assert sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
BASE=HERE/'ordinary_prequential_small_loss_decoder_bandit_20261028.md'
assert sha256(BASE.read_bytes()).hexdigest()=='6edb6a3af1118947c1a864113a24d77eef437386eafb7d8694a4aa651dc8d1dc'
Q=s.Rational
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
E=[s.kronecker_product(A,B) for A in [X,Y,Z] for B in [I,X,Y,Z]]
d=2; k=4; D=12; zeta=Q(1,16); mu=zeta/k; eta=Q(1,64*D*D); delta=eta/64
C0=s.eye(k)/k
V=s.diag(*([Q(1,32)]*8+[Q(1,128)]*4))
U=V.inv().T
axis=8
xi=min(delta**2*mu**4/(512*k),mu**2/512)
assert 32*k*xi/mu**4<=delta**2/16
assert 2*xi/mu**2<=Q(1,256)

def ptr(M):
    return M[:d,:d]+M[d:,d:]
def mineig_diagonal(M):
    assert M.is_diagonal()
    return min(M.diagonal())
def radius2(A,B):
    diff=B-A
    return s.simplify(s.trace(A.inv()*diff*A.inv()*diff))
def grad(C):
    return s.Matrix([-s.trace(C.inv()*a) for a in E])
def hess(C):
    ci=C.inv()
    return s.Matrix([[s.trace(ci*a*ci*b) for b in E] for a in E])
def maxbits(M):
    vals=[s.re(x) for x in M]+[s.im(x) for x in M]
    return max(max(abs(int(v.p)).bit_length(),int(v.q).bit_length()) for v in vals)
def dyadic_below(x):
    q=Q(1); n=0
    while q>x:
        q/=2; n+=1
    return q,n

checks=[]
for h in [Q(0),Q(1,2**20)]:
    theta_star=(1-zeta)/4
    theta_t=theta_star-h
    Ct=C0+theta_t*E[axis]
    Cstar=C0+theta_star*E[axis]
    H=hess(Ct); A=V.T*H*V
    assert A.is_diagonal()
    assert min(A.diagonal())>=Q(1,2) and max(A.diagonal())<=1
    assert U.T*H.inv()*U==A.inv()
    g=-2*D*U[:,axis]
    assert g[axis]==-3072 and all(g[j]==0 for j in range(D) if j!=axis)
    p=eta*g+grad(Cstar)-grad(Ct)
    assert p[axis]<0 and all(p[j]==0 for j in range(D) if j!=axis)
    # p is a support normal at the floor, so the convex objective's unique
    # constrained minimizer is Cstar; no vanishing tangent gradient is used.
    B=sum((p[j]*E[j] for j in range(D)),s.zeros(k))/k
    dual=(p[axis]/k)*s.eye(d)
    dual_slack=B-s.kronecker_product(I,dual)
    assert mineig_diagonal(dual_slack)>=0
    cert=s.simplify(p[axis]*theta_star-(1-zeta)*s.trace(dual)/d)
    assert cert==0
    r2=radius2(Ct,Cstar)
    a2=s.simplify(eta**2*(g.T*H.inv()*g)[0])
    assert a2<Q(1,256) and r2<=a2 and r2<Q(1,225)
    monotonic=s.simplify(((grad(Cstar)-grad(Ct)).T*s.Matrix([h if j==axis else 0 for j in range(D)]))[0])
    assert monotonic<=h/3
    # Actual outward Dikin action is physical, TP, and outside center domain.
    Cplay=Ct+V[axis,axis]*E[axis]/2
    assert ptr(Cplay)==I/d
    play_min=mineig_diagonal(Cplay)
    assert play_min>=mu/2 and play_min<mu
    # Construct a finite feasible approximation with objective gap <= xi/4
    # from the universal G-Lipschitz bound, then certify VI exactly.
    e,bits=dyadic_below(xi*mu/(12*k))
    Capprox=Cstar-e*E[axis]
    theta_approx=theta_star-e
    assert 3*k*e/mu<=xi/4
    papprox=eta*g+grad(Capprox)-grad(Ct)
    assert papprox[axis]<0
    bapprox=sum((papprox[j]*E[j] for j in range(D)),s.zeros(k))/k
    yapprox=(papprox[axis]/k)*I
    assert mineig_diagonal(bapprox-s.kronecker_product(I,yapprox))>=0
    vi=s.simplify(papprox[axis]*theta_approx-(1-zeta)*s.trace(yapprox)/d)
    assert vi>=0 and vi<=delta/4
    assert radius2(Ct,Capprox)<=Q(1,4)
    assert mineig_diagonal(Capprox)>=mu and ptr(Capprox)==I/d
    assert abs(papprox[axis])>delta # tangent stationarity is the wrong test
    checks.append(dict(center_offset=str(h),whitening_lower=str(min(A.diagonal())),whitening_upper=str(max(A.diagonal())),exact_minimizer_vi=str(cert),nonzero_gradient=str(p[axis]),radius_squared=str(r2),a_squared=str(a2),played_min_eigenvalue=str(play_min),center_floor=str(mu),approx_offset_denominator_bits=bits,approx_vi=str(vi),approx_max_matrix_entry_bits=maxbits(Capprox)))

# Exact rational repair, deliberately non-TP and slightly nonpositive input.
rho=Q(1,2**20)
Ktilde=s.diag(1-rho/2,1-rho/2,-rho/2,-rho/2)
assert mineig_diagonal(Ktilde)>=-rho
assert ptr(Ktilde)-I==-rho*I
Khat=Ktilde+s.kronecker_product(I/2,I-ptr(Ktilde))
Kphys=(Khat+2*rho*s.eye(k))/(1+4*rho)
Zphys=Kphys/d
assert ptr(Zphys)==I/d and mineig_diagonal(Zphys)>0
repair_diff=Zphys-Ktilde/d
assert s.trace(repair_diff.H*repair_diff)<=81*rho**2
Cphys=mu*s.eye(k)+(1-zeta)*Zphys
assert ptr(Cphys)==I/d and mineig_diagonal(Cphys)>=mu

# Formal exact three-point identity, with a nonzero residual p.
Ru,Rx,Ry,eta_g=s.symbols('Ru Rx Ry eta_g')
u,x,y,gx,gy=s.symbols('u x y gx gy')
Bux=Ru-Rx-gx*(u-x); Buy=Ru-Ry-gy*(u-y); Byx=Ry-Rx-gx*(y-x)
p=eta_g+gy-gx
assert s.expand(eta_g*(y-u)-(Bux-Buy-Byx+p*(y-u)))==0

# Precision scaling at fixed d, with epsilon=2^-m and gamma=1.
scaling=[]
for m in [0,4,16,64]:
    eps=Q(1,2**m); mm=eps/(16*k); dd=eta*eps/64
    xx=min(dd**2*mm**4/(512*k),mm**2/512)
    rr=xx*mm/(1000*k)
    _,meshbits=dyadic_below(rr/(64*d))
    threshold=int(512*D*D*k*(m+4)/eps)
    horizon=1 << (threshold-1).bit_length()
    scaling.append(dict(epsilon_power=m,uniform_floor_denominator_bits=int(mm.q).bit_length(),xi_denominator_bits=int(xx.q).bit_length(),prescribed_repair_mesh_bits=meshbits,source_horizon=str(horizon),old_floor_denominator_bits=str(horizon+2+2+1)))

out=dict(status='PASS exact rational checks',source_sha256=EXPECTED,base_sha256=sha256(BASE.read_bytes()).hexdigest(),checks=checks,repair=dict(rho=str(rho),min_Zphys=str(mineig_diagonal(Zphys)),floor_guard=True,tp_guard=True,frobenius_error_squared=str(s.trace(repair_diff.H*repair_diff)),fixed_denominator_example=str(Zphys[0,0].q)),xi=str(xi),precision_scaling=scaling,scope='Deterministic exact fixtures, not generic convex-solver execution, sampled acquisition, performance pilot, or hardware evidence.')
( HERE/'bounded_center_precision_independent_check_20261028.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
