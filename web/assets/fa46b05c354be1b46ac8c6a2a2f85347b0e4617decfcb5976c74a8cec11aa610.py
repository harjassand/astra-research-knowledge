"""Fixed finite diagnostics for the independently frozen all-p KMS profile.

No optimization or catalogue scan. Writes exactly one exclusive-create JSON.
Do not run again against an existing output; use the read-only replay helper.
"""
from pathlib import Path
import hashlib
import json
import math
import numpy as np

HERE = Path(__file__).resolve().parent
PS = (1.25, 1.5, 2.0, 3.0, 5.0)


def spectral_power(a, exponent):
    vals, vecs = np.linalg.eigh((a+a.conj().T)/2)
    assert vals.min() > 0, vals
    return (vecs * vals**exponent) @ vecs.conj().T


def density(a):
    return a / np.trace(a).real


def kernel(x, y, t):
    return (np.cosh((x+y)/2)*np.cosh(t*(x-y)/2)/np.cosh((x-y)/2)
            -np.cosh(t*(x+y)/2))


def choi(fn, n):
    out = np.zeros((n*n,n*n), complex)
    for a in range(n):
        for b in range(n):
            e = np.zeros((n,n), complex)
            e[a,b] = 1
            out += np.kron(fn(e),e)
    return out


def check_case(name, sigma_diagonal, B, rho, tau):
    sigma_diagonal = np.asarray(sigma_diagonal, float)
    sigma = np.diag(sigma_diagonal)
    n, refdim = len(sigma_diagonal), len(tau)
    assert np.allclose(B, B.conj().T)
    assert rho.shape == (refdim*n,refdim*n)
    svals = np.sqrt(sigma_diagonal)
    s, d, dinv = np.diag(svals), np.diag(np.sqrt(svals)), np.diag(1/np.sqrt(svals))
    V = 2*(B@s@B)/(svals[:,None]+svals[None,:])
    K, C = d@B@dinv, d@V@dinv
    Bb, Vb = np.kron(np.eye(refdim),B), np.kron(np.eye(refdim),V)
    omega = np.kron(tau,sigma)
    st = spectral_power(omega,.5)
    dt, dit = spectral_power(omega,.25), spectral_power(omega,-.25)

    def H(x):
        return (Vb@x+x@Vb)/2-Bb@x@Bb

    def L(x):
        return dit@H(dt@x@dt)@dit

    roots, U = np.linalg.eigh(rho)
    assert roots.min() > 0
    sqrt_lam = np.sqrt(roots)
    sqrho = spectral_power(rho,.5)
    eroot = np.trace(sqrho@H(sqrho)).real
    u = np.log(svals)
    parts_dict = {}
    for a in range(n):
        for b in range(n):
            if B[a,b] != 0:
                alpha = round(float(u[a]-u[b]),13)
                parts_dict.setdefault(alpha,np.zeros_like(B))[a,b] += B[a,b]
    alphas = np.asarray(sorted(parts_dict))
    parts = [parts_dict[alpha] for alpha in alphas]
    components = np.asarray([U.conj().T@np.kron(np.eye(refdim),part)@U for part in parts])
    rows = []
    for p in PS:
        r, a, t = 1/p, .5-1/p, 1-2/p
        eta, cp = math.sin(math.pi/p), p*math.sin(math.pi/p)/(2*(p-1))
        sr, sinvr = spectral_power(omega,r/2), spectral_power(omega,-r/2)
        f = sinvr@spectral_power(rho,r)@sinvr
        bare = sr@f@sr
        outer_q = spectral_power(omega,-(1-r)/2)
        iq = outer_q@spectral_power(bare,p-1)@outer_q
        i2 = dit@spectral_power(bare,p/2)@dit
        ep_direct = p/(2*(p-1))*np.trace(st@iq@st@L(f)).real
        eroot_direct = np.trace(st@i2@st@L(i2)).real
        sa, sma = spectral_power(omega,a/2), spectral_power(omega,-a/2)
        h = sa@spectral_power(rho,r)@sa
        g = sma@spectral_power(rho,1-r)@sma
        tr = np.trace(g@H(h)).real
        transport_error = max(np.linalg.norm(dt@f@dt-h),
                              np.linalg.norm(dt@iq@dt-g),
                              np.linalg.norm(dt@i2@dt-sqrho))
        ep_error = abs(ep_direct-tr/(2*(1-r)))
        root_error = abs(eroot_direct-eroot)
        complete_gram = 0j
        root_gram = 0j
        diagonal_gram = 0j
        imaginary_cross_mass = 0.0
        min_difference_gram_eigenvalue = 0.0
        max_hardy_congruence_error = 0.0
        for i in range(len(roots)):
            for j in range(len(roots)):
                beta = math.log(sqrt_lam[i]/sqrt_lam[j])
                nodes = beta-alphas
                xx, yy = nodes[:,None], nodes[None,:]
                kt, k0 = kernel(xx,yy,t), kernel(xx,yy,0)
                difference = kt-eta*k0
                min_difference_gram_eigenvalue = min(min_difference_gram_eigenvalue,
                    float(np.linalg.eigvalsh(difference).min()))
                c = components[:,i,j]
                weight = sqrt_lam[i]*sqrt_lam[j]
                term = weight*np.vdot(c,kt@c)
                complete_gram += term
                root_gram += weight*np.vdot(c,k0@c)
                if i == j:
                    diagonal_gram += term
                imaginary_cross_mass += float(np.abs(np.outer(c.conj(),c).imag).sum())
                v = np.tanh(nodes/2)
                cc = np.cosh(t*nodes/2)
                psi = np.full_like(v,t)
                nonzero = np.abs(v) > 1e-14
                psi[nonzero] = np.tanh(t*nodes[nonzero]/2)/v[nonzero]
                bb = 1/cc
                nn = (1-np.outer(psi,psi)-eta*np.outer(bb,bb))/(1-np.outer(v,v))
                congruence = 2*np.outer(v*cc,v*cc)*nn
                max_hardy_congruence_error = max(max_hardy_congruence_error,
                    float(np.linalg.norm(congruence-difference)))
        gram_error = abs(complete_gram-tr)
        root_gram_error = abs(root_gram-eroot)
        potential_from_frequencies = np.zeros_like(B)
        for alpha, ba in zip(alphas,parts):
            for gamma, bg in zip(alphas,parts):
                m, h0 = (alpha+gamma)/2,(alpha-gamma)/2
                potential_from_frequencies += (np.exp(m)*np.cosh(t*h0)/np.cosh(h0))*(ba.conj().T@bg)
        sla, slma = np.diag(svals**a),np.diag(svals**(-a))
        potential_direct = (sla@V@slma+slma@V@sla)/2
        potential_error = np.linalg.norm(potential_from_frequencies-potential_direct)
        profile_gap = ep_direct-cp*eroot
        scale = 1+abs(tr)+abs(eroot)
        assert max(transport_error,ep_error,root_error,gram_error,root_gram_error,
                   potential_error,max_hardy_congruence_error) <= 1e-9*scale, (name,p,scale)
        assert profile_gap >= -3e-10*scale, (name,p,profile_gap)
        assert min_difference_gram_eigenvalue >= -3e-9*scale, (name,p,min_difference_gram_eigenvalue)
        rows.append({"p":p,"coefficient":cp,"E_p":float(ep_direct),"E_root":float(eroot),
            "profile_gap":float(profile_gap),"T_r":float(tr),
            "transport_operator_error":float(transport_error),"E_p_normalization_error":float(ep_error),
            "E_root_normalization_error":float(root_error),"complete_gram_real":float(complete_gram.real),
            "complete_gram_imaginary":float(complete_gram.imag),"identity_absolute_error":float(gram_error),
            "root_gram_absolute_error":float(root_gram_error),"potential_operator_error":float(potential_error),
            "minimum_difference_gram_eigenvalue":float(min_difference_gram_eigenvalue),
            "maximum_hardy_congruence_error":float(max_hardy_congruence_error),
            "diagonal_gram_real":float(diagonal_gram.real),
            "imaginary_cross_product_mass":float(imaginary_cross_mass)})
    duality_errors = {}
    for p, q in ((1.25,5.0),(1.5,3.0)):
        ep = next(row["E_p"] for row in rows if row["p"] == p)
        eq = next(row["E_p"] for row in rows if row["p"] == q)
        error = abs(eq-(p-1)*ep)
        assert error <= 1e-9*(1+abs(eq)+abs(ep))
        duality_errors[str(p)] = float(error)
    lindblad_error = np.linalg.norm((C+C.conj().T)/2-K.conj().T@K)
    stationarity_error = np.linalg.norm((C@sigma+sigma@C.conj().T)/2-K@sigma@K.conj().T)
    assert max(lindblad_error,stationarity_error) <= 3e-10
    return {"case":name,"local_dimension":n,"reference_dimension":refdim,
            "frequency_count":len(alphas),"rho_min_eigenvalue":float(roots.min()),
            "reference_min_eigenvalue":float(np.linalg.eigvalsh(tau).min()),
            "physical_hamiltonian_norm":float(np.linalg.norm((C-C.conj().T)/(2j))),
            "physical_lindblad_error":float(lindblad_error),"stationarity_error":float(stationarity_error),
            "same_rho_conjugate_duality_errors":duality_errors,"p_checks":rows}


def check_qutrit_counterfamily():
    r, t, eta = 1/3,1/3,8/9
    us = np.array([101/100,2.0])
    xs = 3*np.log(us)
    vs = (us**3-1)/(us**3+1)
    psi = (us**2-us+1)/(us**2+us+1)
    bb = 2*np.sqrt(us)/(us+1)
    cc = (us+1)/(2*np.sqrt(us))
    N = (1-np.outer(psi,psi)-eta*np.outer(bb,bb))/(1-np.outer(vs,vs))
    assert 0<N[0,0]<1e-5 and N[0,1]>.01
    assert abs(N[1,1]-13/196)<1e-13 and np.linalg.det(N)<0
    y = np.array([1,-N[0,1]/N[1,1]])
    s0 = 1/math.sqrt(1+float(np.exp(-2*xs).sum()))
    sv = s0*np.r_[1,np.exp(-xs)]
    s, sigma = np.diag(sv),np.diag(sv**2)
    B = np.zeros((3,3),complex)
    B[1:,1:] = 1
    A0 = float(sv[1:].sum())
    V = 2*(B@s@B)/(sv[:,None]+sv[None,:])
    d = np.exp(xs/2)/np.sinh(r*xs)
    qnodes = math.sqrt(2)*vs*cc
    z = y/(d*qnodes)
    Q = np.zeros((3,3),complex)
    Q[0,1:] = Q[1:,0] = z
    di = np.diag(1/np.sqrt(sv))
    A = di@Q@di
    dr, cr = np.sinh((1-r)*xs)/np.sinh(r*xs),np.sinh(xs/2)/np.sinh(r*xs)
    DQ, CQ = Q.copy(),Q.copy()
    DQ[0,1:] = DQ[1:,0] = dr*z
    CQ[0,1:] = CQ[1:,0] = cr*z
    M = V[1:,1:]*((dr[:,None]+dr[None,:])/2-eta*np.outer(cr,cr))
    Lt, L0 = kernel(xs[:,None],xs[None,:],t),kernel(xs[:,None],xs[None,:],0)
    congruent_M = A0/(2*s0)*np.outer(d,d)*(Lt-eta*L0)
    M_error = np.linalg.norm(M-congruent_M)
    N_error = np.linalg.norm(Lt-eta*L0-np.outer(qnodes,qnodes)*N)
    assert max(M_error,N_error)<1e-11

    def HB(x):
        return (V@x+x@V)/2-B@x@B

    def HR(x):
        return x-s*np.trace(s@x)

    mB = np.trace(DQ@HB(Q)).real-eta*np.trace(CQ@HB(CQ)).real
    mR = np.trace(DQ@HR(Q)).real-eta*np.trace(CQ@HR(CQ)).real
    delta = -mB/(2*(1+abs(mR)))
    assert mB<0 and delta>0
    assert abs(mB-z@M@z)<1e-11 and mB+delta*mR<=mB/2+1e-12

    def H(x):
        return HB(x)+delta*HR(x)

    df = np.diag(np.sqrt(sv))
    K, C = df@B@di,df@V@di
    lindblad_error = np.linalg.norm((C+C.conj().T)/2-K.conj().T@K)
    stationarity_error = np.linalg.norm(H(s))
    n = 3
    hs = np.stack([H(np.eye(n*n)[k].reshape(n,n)).reshape(-1) for k in range(n*n)],axis=1)
    h_evals, h_vecs = np.linalg.eigh(hs)
    assert abs(h_evals[0])<1e-11 and h_evals[1] >= delta-1e-11
    semigroup_hs = (h_vecs*np.exp(-.2*h_evals))@h_vecs.conj().T
    def heisenberg_semigroup(x):
        return di@(semigroup_hs@(df@x@df).reshape(-1)).reshape(n,n)@di
    semigroup_choi_min = float(np.linalg.eigvalsh(choi(heisenberg_semigroup,n)).min())
    assert semigroup_choi_min >= -1e-11
    rows = []
    A_norm = float(np.linalg.norm(A,2))
    for relative_step in (.005,.0025):
        epsilon = relative_step/A_norm
        f = np.eye(3)+epsilon*A
        assert np.linalg.eigvalsh(f).min()>0
        bare = np.diag(sv**r)@f@np.diag(sv**r)
        rho = spectral_power(bare,1/r)
        h = df@f@df
        iq = np.diag(sv**(-(1-r)))@spectral_power(bare,(1-r)/r)@np.diag(sv**(-(1-r)))
        g = df@iq@df
        tr = np.trace(g@H(h)).real
        root = spectral_power(rho,.5)
        eroot = np.trace(root@H(root)).real
        ep3 = tr/(2*(1-r))
        strong_gap = ep3-(2/3)*eroot
        sharp_gap = ep3-(3*math.sqrt(3)/8)*eroot
        normalized_hessian = (tr-eta*eroot)/epsilon**2
        rq = 1-r
        aq = .5-rq
        hq = np.diag(sv**aq)@spectral_power(rho,rq)@np.diag(sv**aq)
        gq = np.diag(sv**(-aq))@spectral_power(rho,1-rq)@np.diag(sv**(-aq))
        epq = np.trace(gq@H(hq)).real/(2*(1-rq))
        dual_error = abs(epq-2*ep3)
        assert strong_gap<0 and sharp_gap>0
        assert normalized_hessian<0
        assert abs(normalized_hessian-(mB+delta*mR))<=.005*(1+abs(mB+delta*mR))
        assert dual_error <= 3e-11
        assert epq-(4/3)*eroot<0
        rows.append({"relative_positive_step":relative_step,"epsilon":epsilon,
            "f_min_eigenvalue":float(np.linalg.eigvalsh(f).min()),
            "rho_min_eigenvalue":float(np.linalg.eigvalsh(rho).min()),
            "E_3":float(ep3),"E_root":float(eroot),"strong_p3_gap":float(strong_gap),
            "sharp_profile_gap":float(sharp_gap),"normalized_hessian_residual":float(normalized_hessian),
            "E_conjugate_1_5":float(epq),"same_rho_duality_error":float(dual_error),
            "strong_p1_5_gap":float(epq-(4/3)*eroot)})
    return {"local_dimension":3,"p":3,"N":N.tolist(),"N_determinant":float(np.linalg.det(N)),
            "negative_N_vector":y.tolist(),"sigma_diagonal":(sv**2).tolist(),
            "physical_coherence_z":z.tolist(),"primitive_replacer_delta":float(delta),
            "base_negative_hessian":float(mB),"replacer_hessian":float(mR),
            "primitive_negative_hessian":float(mB+delta*mR),
            "minimum_nonzero_H_eigenvalue":float(h_evals[1]),
            "semigroup_time_0_2_choi_min_eigenvalue":semigroup_choi_min,
            "physical_lindblad_error":float(lindblad_error),"stationarity_error":float(stationarity_error),
            "physical_hamiltonian_norm":float(np.linalg.norm((C-C.conj().T)/(2j))),
            "hessian_congruence_error":float(M_error),"hardy_congruence_error":float(N_error),
            "positive_state_checks":rows}


B3=np.array([[.3,1,1j],[1,-.2,1+.5j],[-1j,1-.5j,.4]],complex)
sigma3=np.array([1,4,9])/14
X=np.array([[1,.2j,.4],[.3,1.2,-.5j],[.1j,.2,.8]],complex)
rho3=density(X@X.conj().T+.15*np.eye(3))
psi6=np.array([1,0,.4,0,1j,.3],complex)
psi6/=np.linalg.norm(psi6)
rho6=.63*np.outer(psi6,psi6.conj())+.37*np.diag(np.arange(1,7)/21)
tau=np.array([[.6,.2j],[-.2j,.4]],complex)
B4=np.array([[.2,1,1j,.2-.4j],[1,-.1,.3j,1+.2j],
             [-1j,-.3j,.3,.6],[.2+.4j,1-.2j,.6,-.4]],complex)
psi4=np.array([1,.2j,-.3,1j],complex)
psi4/=np.linalg.norm(psi4)
rho4=.55*np.outer(psi4,psi4.conj())+.45*np.eye(4)/4
inputs=[
    ("complex_noncommuting_qutrit",sigma3,B3,rho3,np.ones((1,1))),
    ("entangled_reference_with_nontracial_weight",sigma3,B3,rho6,tau),
    ("stationary_quantum_reference",sigma3,B3,np.kron(tau,np.diag(sigma3)),tau),
    ("tracial_null_remainder_control",np.ones(3)/3,
        np.array([[0,1,0],[1,0,0],[0,0,0]],complex),np.diag([4/9,4/9,1/9]),np.ones((1,1))),
    ("identity_noise_noncommuting_state",sigma3,np.eye(3,dtype=complex),rho3,np.ones((1,1))),
    ("degenerate_local_and_full_state_spectra",np.array([1,1,4,9])/15,B4,rho4,np.ones((1,1))),
]
rows=[check_case(*args) for args in inputs]
pt=rho6.reshape(2,3,2,3).transpose(2,1,0,3).reshape(6,6)
npt_min=float(np.linalg.eigvalsh(pt).min())
assert npt_min<0
qutrit=check_qutrit_counterfamily()
out={"status":"PASS_FINITE_DIAGNOSTICS_ONLY","no_optimization":True,
     "case_count":len(rows),"p_values":list(PS),"case_p_count":len(rows)*len(PS),
     "entangled_reference_partial_transpose_min":npt_min,
     "positive_profile_proof_sha256":hashlib.sha256((HERE/"INDEPENDENT_ALL_P_PROFILE_PROOF.txt").read_bytes()).hexdigest(),
     "qutrit_counterfamily_proof_sha256":hashlib.sha256((HERE/"CONCRETE_QUTRIT_STRONG_P3_COUNTERFAMILY.txt").read_bytes()).hexdigest(),
     "checks":rows,"primitive_qutrit_strong_counterfamily":qutrit,
     "limitations":["Finite diagnostics are not an all-dimension proof",
                    "No external or formal validation","No historical priority certification"]}
with (HERE/"ALL_P_PHYSICAL_CONTROLS.json").open("x") as f:
    json.dump(out,f,indent=2)
    f.write("\n")
print(json.dumps({"status":out["status"],"case_p_count":out["case_p_count"],
    "maximum_general_p_identity_error":max(x["identity_absolute_error"] for row in rows for x in row["p_checks"]),
    "maximum_transport_error":max(x["transport_operator_error"] for row in rows for x in row["p_checks"]),
    "maximum_hardy_congruence_error":max(x["maximum_hardy_congruence_error"] for row in rows for x in row["p_checks"]),
    "qutrit_N_determinant":qutrit["N_determinant"],"qutrit_primitive_delta":qutrit["primitive_replacer_delta"],
    "qutrit_strong_p3_gaps":[x["strong_p3_gap"] for x in qutrit["positive_state_checks"]],
    "qutrit_strong_p1_5_gaps":[x["strong_p1_5_gap"] for x in qutrit["positive_state_checks"]]}))
