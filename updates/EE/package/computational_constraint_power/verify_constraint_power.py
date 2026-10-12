"""Diagnostics for a constraint-preserving nonlinear-interface oracle.

This is a small dense mathematical test, not an implementation of fast sparse
preprocessing or a performance benchmark. Exact checks use SymPy rationals;
optimization checks use SciPy SLSQP and report feasibility and objective errors.
"""
from __future__ import annotations
import itertools, json, math
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import minimize, LinearConstraint, Bounds
from scipy.linalg import eigh

OUT=Path(__file__).resolve().parent
rng=np.random.default_rng(1201026)
n,r,d,q=6,2,2,64
A=sp.Matrix([[1,0,1,-1,2,0],[0,1,1,1,0,-1]])
T=sp.zeros(n,r); T[0,0]=T[1,1]=1
G=sp.eye(n).col_join(sp.Matrix([[1,1,0,-1,0,1],[0,1,-1,0,1,0]]))
H=G.T*G
F=sp.eye(r)
Hi=H.inv(); L=A*Hi*A.T
X=Hi*A.T*L.inv()*F
K=Hi-Hi*A.T*L.inv()*A*Hi
C=sp.eye(n).col_join(sp.Matrix([[1,1,0,0,0,0],[0,0,1,-1,0,0],[2,2,0,0,0,0]]))
N=sp.Matrix.hstack(*A.nullspace())
R=sp.Matrix(rng.choice([-1,1],size=(q,G.rows)).tolist())/8
J0=K*G.T*R.T

def round_dyadic(M,bits):
    den=2**bits
    return M.applyfunc(lambda x: sp.Rational(round(x*den),den))

V=round_dyadic(J0,12)
J=V-T*(A*V)
Xh=round_dyadic(X,12)
Xh=Xh+T*(F-A*Xh)
Y=J.T*C.T
Gamma=C*K*C.T
Ch=Xh.T*H*Xh
C0=X.T*H*X
Dh=C*Xh; D0=C*X
assert A*J==sp.zeros(r,q)
assert A*Xh==F

def npf(M): return np.array(M.tolist(),dtype=float)

def quad_consistent(M,v):
    sol,parameters=M.gauss_jordan_solve(v)
    sol=sol.subs({a:0 for a in parameters})
    return (v.T*sol)[0]

hf,npK,npX,npXh,npC=npf(H),npf(K),npf(X),npf(Xh),npf(C)
eta2=float(max(eigh(npf(Ch-C0),npf(C0),eigvals_only=True)))
eta=math.sqrt(max(eta2,0.0))
all_supports=[s for k in range(1,4) for s in itertools.combinations(range(C.rows),k)]
rank_checks=0; max_distortion=0.0
for S in all_supports:
    g=Gamma.extract(S,S); gh=Y[:,S].T*Y[:,S]
    assert g.rank()==gh.rank()
    assert all(gh*v==sp.zeros(len(S),1) for v in g.nullspace())
    gg=npf(g); hh=npf(gh)
    w,U=np.linalg.eigh(gg); U=U[:,w>1e-10]; w=w[w>1e-10]
    if len(w):
        inv=U/np.sqrt(w)
        vals=np.linalg.eigvalsh(inv.T@hh@inv)
        max_distortion=max(max_distortion,float(np.max(np.abs(vals-1))))
    rank_checks+=1

point_checks=0; max_point_rel=0.0; max_identity_error=0.0
for _ in range(40):
    S=tuple(sorted(rng.choice(C.rows,size=3,replace=False)))
    alpha=sp.Matrix(rng.integers(-3,4,size=d).tolist())
    v=sp.Matrix(rng.integers(-3,4,size=N.cols).tolist())
    feasible=T*F*alpha+N*v
    y=C[list(S),:]*feasible
    gs=Gamma.extract(S,S); ghs=Y[:,S].T*Y[:,S]
    rhs=y-D0[list(S),:]*alpha
    rhsh=y-Dh[list(S),:]*alpha
    true=(alpha.T*C0*alpha)[0]+quad_consistent(gs,rhs)
    est=(alpha.T*Ch*alpha)[0]+quad_consistent(ghs,rhsh)
    B=A.col_join(C[list(S),:]); b=(F*alpha).col_join(y)
    direct=quad_consistent(B*Hi*B.T,b)
    assert sp.simplify(true-direct)==0
    if true:
        max_point_rel=max(max_point_rel,abs(float(est/true)-1))
    else:
        assert est==0
    point_checks+=1

# Feasibility check: duplicated port rows enforce y_8=2*y_6 exactly.
S=(6,8); ghs=Y[:,S].T*Y[:,S]
try:
    quad_consistent(ghs,sp.Matrix([1,3]))
    raise AssertionError('inconsistent dependent ports accepted')
except ValueError:
    pass

# Coupled convex design: variable loads, port force bounds, and a shared capacity budget.
An=npf(A); Fn=npf(F); Yn=npf(Y); C0n=npf(C0); Chn=npf(Ch); Dhn=npf(Dh)
opt_tests=[]
for trial in range(24):
    S=tuple(sorted(rng.choice(n,size=3,replace=False)))
    k=len(S); CS=npC[list(S),:]
    gh=Yn[:,S].T@Yn[:,S]; DS=Dhn[list(S),:]
    if np.linalg.eigvalsh(gh)[0]<1e-10: continue
    alpha0=np.ones(d)
    x0=npXh@alpha0
    y0=CS@x0
    z0=np.abs(y0)+0.75
    budget=float(z0.sum()+0.25)
    ztarget=rng.uniform(0.05,0.5,size=k)
    ytarget=rng.normal(0,0.5,size=k)
    # Full variables: x, alpha, z. Reduced variables: t, alpha, z.
    lam=0.35; mu=0.2
    def psi(y,z): return lam*np.dot(y-ytarget,y-ytarget)+mu*np.dot(z-ztarget,z-ztarget)
    def full_obj(v):
        x=v[:n]; z=v[n+d:]; y=CS@x
        return x@hf@x+psi(y,z)
    def full_jac(v):
        x=v[:n]; z=v[n+d:]; y=CS@x
        return np.r_[2*hf@x+2*lam*CS.T@(y-ytarget),np.zeros(d),2*mu*(z-ztarget)]
    E=np.c_[An,-Fn,np.zeros((r,k))]
    Icap=np.vstack([np.c_[CS,np.zeros((k,d)),-np.eye(k)],
                    np.c_[-CS,np.zeros((k,d)),-np.eye(k)],
                    np.r_[np.zeros(n+d),np.ones(k)][None,:]])
    bounds=Bounds(np.r_[np.full(n,-np.inf),np.full(d,0.8),np.zeros(k)],
                  np.r_[np.full(n,np.inf),np.full(d,1.2),np.full(k,np.inf)])
    cons=[LinearConstraint(E,np.zeros(r),np.zeros(r)),
          LinearConstraint(Icap,np.full(2*k+1,-np.inf),np.r_[np.zeros(2*k),budget])]
    full=minimize(full_obj,np.r_[x0,alpha0,z0],jac=full_jac,
                  constraints=cons,bounds=bounds,method='SLSQP',
                  options={'ftol':1e-12,'maxiter':600})
    def reduced_obj(v):
        t=v[:k]; al=v[k:k+d]; z=v[k+d:]; y=DS@al+gh@t
        return al@Chn@al+t@gh@t+psi(y,z)
    def reduced_jac(v):
        t=v[:k]; al=v[k:k+d]; z=v[k+d:]; y=DS@al+gh@t
        gy=2*lam*(y-ytarget)
        return np.r_[2*gh@t+gh@gy,2*Chn@al+DS.T@gy,2*mu*(z-ztarget)]
    Ccap=np.vstack([np.c_[gh,DS,-np.eye(k)],np.c_[-gh,-DS,-np.eye(k)],
                   np.r_[np.zeros(k+d),np.ones(k)][None,:]])
    rb=Bounds(np.r_[np.full(k,-np.inf),np.full(d,0.8),np.zeros(k)],
              np.r_[np.full(k,np.inf),np.full(d,1.2),np.full(k,np.inf)])
    red=minimize(reduced_obj,np.r_[np.zeros(k),alpha0,z0],jac=reduced_jac,
                 constraints=[LinearConstraint(Ccap,np.full(2*k+1,-np.inf),np.r_[np.zeros(2*k),budget])],
                 bounds=rb,method='SLSQP',options={'ftol':1e-12,'maxiter':600})
    assert full.success and red.success, (full.message,red.message)
    t=red.x[:k]; al=red.x[k:k+d]; z=red.x[k+d:]; y=DS@al+gh@t
    g=CS@npK@CS.T
    h=y-CS@npX@al
    xstar=npX@al+npK@CS.T@np.linalg.solve(g,h)
    true_val=float(xstar@hf@xstar+psi(y,z))
    feas=max(float(np.max(np.abs(An@xstar-Fn@al))),float(np.max(np.abs(CS@xstar-y))),
             float(np.max(np.abs(y)-z)),float(z.sum()-budget),0.0)
    opt_tests.append({'true_objective_ratio':true_val/float(full.fun),
                      'max_feasibility_residual':feas,
                      'reduced_iterations':int(red.nit),'full_iterations':int(full.nit)})

# Exact singular-limit test: A=[1,rho], H=I, fix x_1=0; energy is rho^-2.
near=[]
for bits in [10,50,100,200]:
    rho=sp.Rational(1,2**bits)
    aa=sp.Matrix([[1,rho]]); hh=sp.eye(2)
    xx=aa.T/(1+rho*rho)
    vv=sp.Matrix([-rho,1])
    kh=vv*vv.T/(1+rho*rho)
    gs=kh[:1,:1]
    # Relative geometry perturbation and exactly feasible frame perturbation.
    gh=sp.Rational(101,100)*gs
    xhat=xx+sp.Rational(1,10000)*vv
    chat=(xhat.T*xhat)[0]
    est=chat+xhat[0]**2/gh[0,0]
    true=rho**-2
    naive=(xx.T*xx)[0]+xx[0]**2/(gs[0,0]+sp.Rational(1,10**12))
    near.append({'rho_exponent':-bits,'relative_error':float(abs(est/true-1)),
                 'naive_relative_error':float(abs(naive/true-1))})

# Multi-load counterexample: individually accurate, feasible columns are insufficient.
rho=sp.Rational(1,2**80); delta=sp.Rational(1,1000)
Xmulti=sp.Matrix([[1,1],[0,rho],[delta,-delta]])
al=sp.Matrix([1,-1]); exact_energy=rho**2
bad_ratio=(al.T*Xmulti.T*Xmulti*al)[0]/exact_energy

# Full-state recovery from an approximate port model, using only baseline solves.
CS=npC[[0,2,4],:]; YS=Yn[:,[0,2,4]]; gh=YS.T@YS; gg=CS@npK@CS.T
al=np.array([1.0,-0.5]); desired=CS@(npXh@al+npf(N)@np.array([0.1,-0.2,0.15,0.25]))
h=desired-CS@npXh@al
v=np.zeros(n); Jn=npf(J); gamma=max(0.1,1-max_distortion)
start_norm=float(math.sqrt(h@np.linalg.solve(gg,h)))
residual_norms=[]
for iteration in range(30):
    residual=h-CS@v
    residual_norms.append(float(math.sqrt(max(0.0,residual@np.linalg.solve(gg,residual)))))
    ideal=gamma*npK@CS.T@np.linalg.solve(gh,residual)
    direction=npf(N)@rng.normal(size=N.cols)
    direction/=math.sqrt(direction@hf@direction)
    # Inject a known energy-relative solve error; it remains exactly homogeneous algebraically.
    correction=ideal+1e-6*math.sqrt(max(0.0,ideal@hf@ideal))*direction
    v+=correction
residual=h-CS@v
v+=Jn@YS@np.linalg.solve(gh,residual)
xrec=npXh@al+v
xmin=npX@al+npK@CS.T@np.linalg.solve(gg,desired-CS@npX@al)
recovery={
    'baseline_solve_calls':30,
    'initial_port_residual_energy_norm':start_norm,
    'final_port_residual_energy_norm_before_exact_lift':residual_norms[-1],
    'final_physical_balance_residual':float(np.linalg.norm(An@xrec-Fn@al)),
    'final_port_residual':float(np.linalg.norm(CS@xrec-desired)),
    'host_energy_ratio':float((xrec@hf@xrec)/(xmin@hf@xmin))
}

results={
 'scope':'Small dense algebra/optimization diagnostics, not a sparse-performance or novelty test.',
 'dimensions':{'state':n,'conservation_rows':r,'load_basis':d,'candidate_ports':C.rows,'sketch_rows':q},
 'exact_conservation':True,'exact_load_feasibility':True,
 'support_kernel_checks':rank_checks,'pointwise_identity_checks':point_checks,
 'dependent_port_infeasibility_detected':True,
 'uniform_frame_energy_error_eta_squared':eta2,
 'observed_max_port_spectral_distortion':max_distortion,
 'observed_max_pointwise_energy_relative_error':max_point_rel,
 'convex_design_cases':len(opt_tests),
 'max_design_true_objective_ratio':max(t['true_objective_ratio'] for t in opt_tests),
 'max_design_feasibility_residual':max(t['max_feasibility_residual'] for t in opt_tests),
 'near_singular_cases':near,
 'naive_multiload_energy_ratio':float(bad_ratio),
 'full_state_recovery':recovery,
 'note':'The diagnostic sketch is larger than the small host; these tests do not demonstrate compression at scale.'
}
(OUT/'verification_results.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
