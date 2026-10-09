"""Targeted finite diagnostics for the frozen modular Gram proof.

No optimization, no broad scan, no write outside the owned Cycle08 directory.
Output is exclusive-create; never overwrite a frozen artifact on replay.
"""
from pathlib import Path
import hashlib
import json
import math
import numpy as np

HERE = Path(__file__).resolve().parent


def spectral_f(a, fn):
    vals, vecs = np.linalg.eigh(a)
    assert vals.min() > 0, vals
    return (vecs * fn(vals)) @ vecs.conj().T


def density(a):
    return a / np.trace(a).real


def kernel(x, y, kappa):
    lam = kappa / 2
    return (x*np.sinh(y)+y*np.sinh(x)
            -4*lam*np.sinh(x/2)*np.sinh(y/2))/(2*np.cosh((x-y)/2))


def hermitian_traceless_basis(n):
    out = []
    for a in range(n):
        for b in range(a+1, n):
            f = np.zeros((n, n), complex)
            f[a,b] = f[b,a] = 1/math.sqrt(2)
            out.append(f)
            f = np.zeros((n, n), complex)
            f[a,b], f[b,a] = -1j/math.sqrt(2), 1j/math.sqrt(2)
            out.append(f)
    for k in range(1, n):
        f = np.zeros((n,n), complex)
        f[np.arange(k),np.arange(k)] = 1/math.sqrt(k*(k+1))
        f[k,k] = -k/math.sqrt(k*(k+1))
        out.append(f)
    assert len(out) == n*n-1
    return out


def choi(fn, n):
    c = np.zeros((n*n,n*n), complex)
    for a in range(n):
        for b in range(n):
            e = np.zeros((n,n), complex)
            e[a,b] = 1
            c += np.kron(fn(e), e)
    return c


def check_case(name, sigma_diagonal, B, rho, refdim):
    sigma = np.diag(np.asarray(sigma_diagonal, float))
    n = len(sigma_diagonal)
    assert np.allclose(B,B.conj().T)
    assert rho.shape == (refdim*n,refdim*n)
    svals = np.sqrt(np.asarray(sigma_diagonal, float))
    s, d = np.diag(svals), np.diag(np.sqrt(svals))
    dinv = np.diag(1/np.sqrt(svals))
    V = 2*(B@s@B)/(svals[:,None]+svals[None,:])
    K, D = d@B@dinv, d@V@dinv
    def hlocal(x):
        return (V@x+x@V)/2-B@x@B
    eyeR = np.eye(refdim)
    Bb, Vb = np.kron(eyeR,B), np.kron(eyeR,V)
    Kb, Db = np.kron(eyeR,K), np.kron(eyeR,D)
    def hfull(x):
        return (Vb@x+x@Vb)/2-Bb@x@Bb
    def lfull(x):
        return (Db@x+x@Db.conj().T)/2-Kb@x@Kb.conj().T

    q = spectral_f(rho,np.sqrt)
    log_rho = spectral_f(rho,np.log)
    log_sigma = np.kron(eyeR,np.diag(np.log(sigma_diagonal)))
    J = np.trace(lfull(rho)@(log_rho-log_sigma)).real
    E = np.trace(q@hfull(q)).real
    P = K.conj().T@np.diag(np.log(sigma_diagonal))@K
    P -= (D.conj().T@np.diag(np.log(sigma_diagonal))
          +np.diag(np.log(sigma_diagonal))@D)/2
    u = np.log(svals)
    freqs = {}
    for a in range(n):
        for b in range(n):
            if B[a,b] != 0:
                alpha = round(float(u[a]-u[b]),13)
                freqs.setdefault(alpha,np.zeros_like(B))[a,b] += B[a,b]
    alphas = np.asarray(sorted(freqs))
    parts = [freqs[a] for a in alphas]
    eigenvalues, U = np.linalg.eigh(rho)
    roots = np.sqrt(eigenvalues)
    components = np.asarray([U.conj().T@np.kron(eyeR,ba)@U for ba in parts])
    results = {}
    for kappa in (2.0, math.pi):
        gram = 0j
        min_gram_eigenvalue = 0.0
        imaginary_cross_mass = 0.0
        diagonal_gram = 0j
        pot = np.zeros_like(B)
        for a,ba in zip(alphas,parts):
            for g,bg in zip(alphas,parts):
                m,h = (a+g)/2,(a-g)/2
                coef = 2*np.exp(m)*(m-h*np.tanh(h))+kappa*(1-np.exp(m)/np.cosh(h))
                pot += coef*(ba.conj().T@bg)
        for i in range(len(roots)):
            for j in range(len(roots)):
                beta = np.log(roots[i]/roots[j])
                nodes = beta-alphas
                A = kernel(nodes[:,None],nodes[None,:],kappa)
                min_gram_eigenvalue = min(min_gram_eigenvalue,float(np.linalg.eigvalsh(A).min()))
                c = components[:,i,j]
                contribution = 2*roots[i]*roots[j]*np.vdot(c,A@c)
                gram += contribution
                if i == j:
                    diagonal_gram += contribution
                imaginary_cross_mass += float(np.abs(np.outer(c.conj(),c).imag).sum())
        direct = J-kappa*E
        identity_error = abs(gram-direct)
        pot_error = np.linalg.norm(pot-(P-kappa*(V-B@B)))
        assert identity_error <= 3e-10*(1+abs(direct)), (name,kappa,identity_error)
        assert pot_error <= 3e-10*(1+np.linalg.norm(P-kappa*(V-B@B))), (name,pot_error)
        assert min_gram_eigenvalue >= -3e-9, (name,min_gram_eigenvalue)
        assert direct >= -3e-9, (name,direct)
        results[str(kappa)] = {
            "direct_gap":float(direct),"complete_gram_real":float(gram.real),
            "identity_absolute_error":float(identity_error),
            "potential_operator_error":float(pot_error),
            "minimum_gram_eigenvalue":min_gram_eigenvalue,
            "diagonal_gram_real":float(diagonal_gram.real),
            "imaginary_cross_product_mass":imaginary_cross_mass,
        }

    # Independent finite control of the general generator Choi reconstruction.
    Cminus = choi(lambda x:-hlocal(x),n)
    vecI = np.eye(n).reshape(-1)
    Q = np.eye(n*n)-np.outer(vecI,vecI)/(n)
    Y = Q@Cminus@Q
    basis = hermitian_traceless_basis(n)
    W = np.stack([f.reshape(-1) for f in basis],axis=1)
    real_chart = W.conj().T@Y@W
    assert np.linalg.norm(real_chart.imag) <= 2e-10
    evals, evecs = np.linalg.eigh(real_chart.real)
    assert evals.min() >= -2e-10
    noises = []
    for l,v in enumerate(evals):
        if v > 1e-10:
            noises.append(sum(math.sqrt(v)*evecs[k,l]*basis[k] for k in range(len(basis))))
    def reconstructed(x):
        out = np.zeros_like(x,dtype=complex)
        for bnoise in noises:
            vp = 2*(bnoise@s@bnoise)/(svals[:,None]+svals[None,:])
            out += (vp@x+x@vp)/2-bnoise@x@bnoise
        return out
    reconstruction_error = np.linalg.norm(choi(reconstructed,n)-choi(hlocal,n))
    assert reconstruction_error <= 3e-10
    hsmap = np.stack([hlocal(np.eye(n*n)[k].reshape(n,n)).reshape(-1)
                      for k in range(n*n)],axis=1)
    min_h = float(np.linalg.eigvalsh(hsmap).min())
    trace_error = abs(np.trace(lfull(rho)))
    stationarity_error = np.linalg.norm((D@sigma+sigma@D.conj().T)/2-K@sigma@K.conj().T)
    lindblad_error = np.linalg.norm((D+D.conj().T)/2-K.conj().T@K)
    assert max(trace_error,stationarity_error,lindblad_error) <= 3e-10
    assert min_h >= -3e-10
    return {
        "case":name,"local_dimension":n,"reference_dimension":refdim,
        "frequency_count":len(alphas),"J":float(J),"E":float(E),
        "rho_min_eigenvalue":float(eigenvalues.min()),
        "sigma_min_eigenvalue":float(min(sigma_diagonal)),
        "physical_hamiltonian_norm":float(np.linalg.norm((D-D.conj().T)/(2j))),
        "trace_preservation_error":float(trace_error),
        "stationarity_error":float(stationarity_error),
        "physical_lindblad_error":float(lindblad_error),
        "minimum_H_eigenvalue":min_h,
        "general_choi_reconstruction_error":float(reconstruction_error),
        "endpoint_checks":results,
    }


B3=np.array([[.3,1,1j],[1,-.2,1+.5j],[-1j,1-.5j,.4]],complex)
sigma3=np.array([1,4,9])/14
X=np.array([[1,.2j,.4],[.3,1.2,-.5j],[.1j,.2,.8]],complex)
rho3=density(X@X.conj().T+.15*np.eye(3))
psi=np.array([1,0,.4,0,1j,.3],complex)
psi=psi/np.linalg.norm(psi)
rho6=.63*np.outer(psi,psi.conj())+.37*np.diag(np.array([1,2,3,4,5,6])/21)
tau=np.array([[.6,.2j],[-.2j,.4]],complex)
B4=np.array([[.2,1,1j,.2-.4j],[1,-.1,.3j,1+.2j],
             [-1j,-.3j,.3,.6],[.2+.4j,1-.2j,.6,-.4]],complex)
psi4=np.array([1,.2j,-.3,1j],complex)
psi4/=np.linalg.norm(psi4)
rho4=.55*np.outer(psi4,psi4.conj())+.45*np.eye(4)/4
case_inputs=[
    ("three_level_complex_noncommuting",sigma3,B3,rho3,1),
    ("three_level_entangled_reference",sigma3,B3,rho6,2),
    ("three_level_stationary_quantum_reference",sigma3,B3,np.kron(tau,np.diag(sigma3)),2),
    ("old_tracial_null_remainder_control",np.ones(3)/3,
     np.array([[0,1,0],[1,0,0],[0,0,0]],complex),np.diag([4/9,4/9,1/9]),1),
    ("identity_noise_noncommuting_state",sigma3,np.eye(3,dtype=complex),rho3,1),
    ("four_level_degenerate_sigma_and_rho",np.array([1,1,4,9])/15,B4,rho4,1),
]
rows=[check_case(*args) for args in case_inputs]
pt=rho6.reshape(2,3,2,3).transpose(2,1,0,3).reshape(6,6)
npt_min=float(np.linalg.eigvalsh(pt).min())
assert npt_min < 0
out={
    "status":"PASS_FINITE_DIAGNOSTICS_ONLY", "case_count":len(rows),
    "no_optimization":True,"entangled_reference_partial_transpose_min":npt_min,
    "proof_sha256":hashlib.sha256((HERE/"INDEPENDENT_MODULAR_GRAM_PROOF.txt").read_bytes()).hexdigest(),
    "checks":rows,
    "limitations":["Not an all-dimension proof","No external or formal validation","No constant optimality claim"],
}
with (HERE/"PHYSICAL_CONTROLS.json").open("x") as f:
    json.dump(out,f,indent=2)
    f.write("\n")
print(json.dumps({"status":out["status"],"cases":len(rows),
    "maximum_identity_error":max(v["identity_absolute_error"] for r in rows for v in r["endpoint_checks"].values()),
    "maximum_choi_reconstruction_error":max(r["general_choi_reconstruction_error"] for r in rows),
    "entangled_reference_partial_transpose_min":npt_min}))
