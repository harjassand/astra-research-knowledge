"""Exact/small numerical verification of the sparse-damage construction.

This is a dense reference diagnostic, NOT an implementation of the
near-linear preprocessing bound. Requires numpy and sympy.
Run: python verify_sparse_damage.py
"""
from __future__ import annotations
import itertools
import json
import math
from pathlib import Path
import numpy as np
import sympy as sp


def incidence(n: int, edges: list[tuple[int, int]]) -> sp.Matrix:
    B = sp.zeros(n - 1, len(edges))
    for e, (u, v) in enumerate(edges):
        if u < n - 1:
            B[u, e] = 1
        if v < n - 1:
            B[v, e] = -1
    return B


def pair_load(n: int, s: int, t: int) -> sp.Matrix:
    f = sp.zeros(n - 1, 1)
    if s < n - 1:
        f[s] += 1
    if t < n - 1:
        f[t] -= 1
    return f


def compatible_quadratic(M: sp.Matrix, v: sp.Matrix):
    """Infinity if incompatible; exact rational v^T M^+ v otherwise."""
    for h in M.nullspace():
        if (h.T * v)[0] != 0:
            return sp.oo
    sol, params = M.gauss_jordan_solve(v)
    sol = sol.subs({p: 0 for p in params})
    return sp.factor((v.T * sol)[0])


def exact_identity_checks() -> dict:
    n = 5
    edges = [(0,1),(1,2),(2,3),(3,4),(0,4),(0,2),(1,3)]
    B = incidence(n, edges)
    w = sp.Matrix([1,4,1,4,1,4,1])
    W = sp.diag(*w)
    K = B * W * B.T
    Ki = K.inv()
    Gamma = W.inv() - B.T * Ki * B
    checked = 0
    singular_finite = 0
    infinite = 0
    for s,t in [(0,4),(1,3)]:
        f = pair_load(n,s,t)
        z = B.T * Ki * f
        c = (f.T * Ki * f)[0]
        for size in [1,2,3]:
            for S in itertools.combinations(range(len(edges)),size):
                for d in itertools.product([sp.Rational(1,2),sp.Integer(1)],repeat=size):
                    D = sp.diag(*[d[i]*w[S[i]] for i in range(size)])
                    Ks = K-B[:,list(S)]*D*B[:,list(S)].T
                    truth = compatible_quadratic(Ks,f)
                    GS=Gamma.extract(S,S)
                    R=sp.diag(*[(1-d[i])/(d[i]*w[S[i]]) for i in range(size)])
                    extra=compatible_quadratic(GS+R,z[list(S),:])
                    estimate = sp.oo if extra is sp.oo else sp.factor(c+extra)
                    assert truth == estimate, (S,d,truth,estimate)
                    if truth is sp.oo:
                        infinite += 1
                    elif Ks.det() == 0:
                        singular_finite += 1
                    checked += 1
    return {'cases':checked,'infinite_cases':infinite,
            'disconnected_graph_but_finite_pair_cases':singular_finite}


def exact_near_cut_checks() -> list[dict]:
    n=3
    edges=[(0,1),(1,2),(0,2)]
    B=incidence(n,edges)
    K=B*B.T
    Ki=K.inv()
    Gamma=sp.eye(3)-B.T*Ki*B
    S=[0,2]
    GS=Gamma.extract(S,S)
    # An exact rational Gram approximation with precisely the correct kernel.
    Ghat=sp.Rational(101,100)**2*GS
    rows=[]
    for s,t in [(1,2),(0,1)]:
        f=pair_load(n,s,t)
        z=B.T*Ki*f
        c=(f.T*Ki*f)[0]
        # Feasible current on the tree with edges 0 and 1.
        jt=B[:,[0,1]].inv()*f
        j0=sp.Matrix([jt[0],jt[1],0])
        h0=j0[S,:]
        zh=z[S,:]+sp.Matrix([sp.Rational(1,1000),sp.Rational(2,1000)])
        # Preserve the load globally: add a circulation to the electrical flow.
        # The actual preprocessing obtains such a feasible approximation by
        # solving once and restoring its divergence along a spanning tree.
        jhat=z+sp.Rational(1,1000)*sp.Matrix([1,1,-1])
        assert B*jhat==f
        zr=jhat[S,:]
        chat=(jhat.T*jhat)[0]
        for power in [20,80,200]:
            eta=sp.Rational(1,2**power)
            R=(eta/(1-eta))*sp.eye(2)
            wt=sp.diag(eta,1,eta)
            truth=compatible_quadratic(B*wt*B.T,f)
            repaired=chat+compatible_quadratic(Ghat+R,zr)
            unrepaired=c+compatible_quadratic(Ghat+R,zh)
            leaky=chat+compatible_quadratic(Ghat+R+sp.Rational(1,10**12)*sp.eye(2),zr)
            rel=float(abs(repaired/truth-1))
            assert rel < 0.03
            rows.append({'pair':[s,t], 'retained_fraction_power':power,
                         'true_resistance_log2':float(sp.log(truth,2)),
                         'conservative_flow_relative_error':rel,
                         'unrepaired_relative_error':float(abs(unrepaired/truth-1)),
                         'kernel_leak_relative_error':float(abs(leaky/truth-1))})
        for pair_expected in [None]:
            actual=compatible_quadratic(B*sp.diag(0,1,0)*B.T,f)
            pred_extra=compatible_quadratic(Ghat,zr)
            pred=sp.oo if pred_extra is sp.oo else chat+pred_extra
            assert (actual is sp.oo)==(pred is sp.oo)
    return rows


def numerical_uniform_sketch() -> dict:
    rng=np.random.default_rng(19041)
    n=18
    edges=[(i,i+1) for i in range(n-1)]
    possible=[(i,j) for i in range(n) for j in range(i+2,n)]
    ix=rng.choice(len(possible),size=22,replace=False)
    edges += [possible[i] for i in ix]
    B=np.array(incidence(n,edges)).astype(float)
    m=len(edges)
    w=np.exp(rng.uniform(-1,1,m))
    K=(B*w)@B.T
    Ki=np.linalg.inv(K)
    root=np.sqrt(w)
    P=np.eye(m)-(root[:,None]*B.T)@Ki@(B*root)
    Gamma=P/root[:,None]/root[None,:]
    q=1024
    R=rng.choice([-1.,1.],size=(q,m))/math.sqrt(q)
    Y=R@P/root
    # Enforce exact-flow structure in floating-point by a tree correction;
    # the exact rational version is the algorithmic requirement in the proof.
    T=np.zeros((m,n-1)); T[:n-1,:]=np.linalg.inv(B[:,:n-1])
    J=Y*w
    J=J-(B@J.T).T@T.T
    Y=J/w
    assert np.linalg.norm(B@J.T) < 1e-10
    max_dist=0.
    for size in [1,2,3]:
        for S in itertools.combinations(range(m),size):
            S=list(S)
            G=Gamma[np.ix_(S,S)]
            Gh=Y[:,S].T@Y[:,S]
            eig,U=np.linalg.eigh(G)
            good=eig>1e-10
            if not np.any(good):
                continue
            A=U[:,good]/np.sqrt(eig[good])
            ev=np.linalg.eigvalsh(A.T@Gh@A)
            max_dist=max(max_dist,float(np.max(abs(ev-1))))
    assert max_dist < 0.35
    f=np.array(pair_load(n,0,n-1)).astype(float).ravel()
    u=Ki@f; z=B.T@u; c=float(f@u)
    du=rng.normal(size=n-1)
    du *= 1e-5*math.sqrt(c/(du@K@du))
    uhat=u+du
    jhat=w*(B.T@uhat)+T@(f-K@uhat)
    assert np.linalg.norm(B@jhat-f)<1e-10
    ghat=jhat/w
    chat=float(jhat@ghat)
    flow_error_energy=float((jhat-w*z)@((jhat-w*z)/w))
    assert abs((chat-c)-flow_error_energy)<1e-9
    tests=500; max_rel=0.
    for _ in range(tests):
        S=sorted(rng.choice(m,size=3,replace=False))
        d=rng.uniform(.01,.9999,3)
        G=Y[:,S].T@Y[:,S]+np.diag((1-d)/(d*w[S]))
        est=chat+ghat[S]@np.linalg.solve(G,ghat[S])
        wd=w.copy(); wd[S]*=1-d
        truth=f@np.linalg.solve((B*wd)@B.T,f)
        rel=float(abs(est/truth-1))
        max_rel=max(max_rel,rel)
        assert rel <= max_dist/(1-max_dist)+1e-8
    return {'vertices':n,'edges':m,'sketch_rows':q,
            'supports_checked':sum(math.comb(m,i) for i in [1,2,3]),
            'worst_sparse_gram_distortion':max_dist,
            'damage_queries_tested':tests,'worst_resistance_relative_error':max_rel,
            'feasible_flow_relative_energy_excess':flow_error_energy/c,
            'warning':'Dense diagnostic; not an asymptotic running-time benchmark.'}


def exact_conservation_checks() -> dict:
    n=5
    edges=[(0,1),(1,2),(2,3),(3,4),(0,4),(0,2),(1,3)]
    B=incidence(n,edges); m=len(edges)
    w=sp.Matrix([1,4,1,4,1,4,1]); W=sp.diag(*w)
    K=B*W*B.T; Ki=K.inv()
    T=sp.zeros(m,n-1); T[:n-1,:]=B[:,:n-1].inv()
    assert B*T==sp.eye(n-1)
    den=sp.Integer(2)**20
    def rnd(v):
        return v.applyfunc(lambda x: sp.Rational(int(sp.floor(x*den+sp.Rational(1,2))),den))
    rng=np.random.default_rng(4077)
    Yrows=[]
    for _ in range(16):
        signs=rng.choice([-1,1],m)
        a=sp.Matrix([sp.Rational(int(signs[e]),4)*sp.sqrt(w[e]) for e in range(m)])
        uh=rnd(Ki*B*a)
        j=a-W*B.T*uh-T*(B*a-K*uh)
        assert B*j==sp.zeros(n-1,1)
        Yrows.append((W.inv()*j).T)
    Y=sp.Matrix.vstack(*Yrows)
    Gamma=W.inv()-B.T*Ki*B
    checked=0
    for size in [1,2,3]:
        for S in itertools.combinations(range(m),size):
            Ys=Y[:,list(S)]
            G=Gamma.extract(S,S)
            assert Ys.rank()==G.rank()
            for v in G.nullspace():
                assert Ys*v==sp.zeros(Y.rows,1)
            checked+=1
    f=pair_load(n,0,4); uh=rnd(Ki*f)
    jf=W*B.T*uh+T*(f-K*uh)
    assert B*jf==f
    truth=(f.T*Ki*f)[0]
    energy=(jf.T*W.inv()*jf)[0]
    err=jf-W*B.T*Ki*f
    assert sp.factor(energy-truth-(err.T*W.inv()*err)[0])==0
    return {'exactly_divergence_free_rows':Y.rows,
            'local_kernels_checked':checked,
            'rounding_fractional_bits':20,
            'feasible_flow_relative_energy_excess':float(energy/truth-1)}

if __name__=='__main__':
    out={'exact_identity':exact_identity_checks(),
         'exact_conservation':exact_conservation_checks(),
         'near_cut':exact_near_cut_checks(),
         'random_sketch':numerical_uniform_sketch()}
    path=Path(__file__).with_name('verification_results.json')
    path.write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
