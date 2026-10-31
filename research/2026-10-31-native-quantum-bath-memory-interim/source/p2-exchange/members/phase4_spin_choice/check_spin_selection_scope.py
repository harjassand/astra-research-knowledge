"""Exact counterexamples and selection-rule checks for singlet erasure codes.

The correlated-noise example distinguishes rejected vector jump operators
from the complete accepted CP map.  No Monte Carlo or twirling is used.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import eigh
from check_exchange_lru import spinops, dot, singlet, up, down, norm


def kron_all(xs):
    out = np.array([1.], dtype=complex)
    for x in xs:
        out = np.kron(out, x)
    return out


def trace_distance(a, b):
    return float(np.sum(np.abs(np.linalg.eigvalsh(a-b)))/2)


def main():
    s = spinops(4)
    total = [sum(s[i][a] for i in range(4)) for a in range(3)]
    total2 = sum(x@x for x in total)
    l0 = np.kron(singlet, singlet)
    tp = np.kron(up, up)
    tm = np.kron(down, down)
    tz = (np.kron(up, down)+np.kron(down, up))/np.sqrt(2)
    l1 = (np.kron(tp,tm)-np.kron(tz,tz)+np.kron(tm,tp))/np.sqrt(3)
    vc = np.column_stack([l0,l1])
    assert norm(total2@vc) < 1e-14
    eye = np.eye(16)
    p0 = vc@vc.conj().T
    vals, vs = eigh(total2)
    p1 = vs[:,np.abs(vals-2)<1e-9]@vs[:,np.abs(vals-2)<1e-9].conj().T
    p2 = vs[:,np.abs(vals-6)<1e-9]@vs[:,np.abs(vals-6)<1e-9].conj().T
    x = np.array([[0,1],[1,0]],complex)
    z = np.diag([1.,-1.])
    xxxx = kron_all([x]*4)
    zzzz = kron_all([z]*4)
    pstab = (eye+xxxx)@(eye+zzzz)/4
    assert norm(pstab@p0-p0)<1e-14
    stabilizer_spins = [float(np.trace(pstab@p).real) for p in [p0,p1,p2]]
    vector_restriction = max(norm(vc.conj().T@s[i][a]@vc)
                             for i in range(4) for a in range(3))
    kl = vc.conj().T@s[0][2]@s[1][2]@vc

    # One spatially correlated vector jump.  Its individual jump is rejected,
    # but its survival operator is not scalar on the code.
    jump = s[0][2]+s[1][2]
    q = vc.conj().T@jump@jump@vc
    assert norm(q-np.diag([0.,2/3])) < 1e-14
    psi = (l0+l1)/np.sqrt(2)
    rho = np.outer(psi,psi.conj())
    rho_code = np.ones((2,2),complex)/2
    ldiag = np.diag(jump).real
    correlated = []
    for t in [.1,.01,.001,.0001]:
        # Exact Hermitian-Lindblad dephasing in the jump eigenbasis.
        rho_t = rho*np.exp(-t*(ldiag[:,None]-ldiag[None,:])**2/2)
        accepted = vc.conj().T@rho_t@vc
        survival = float(np.trace(accepted).real)
        dist = trace_distance(accepted/survival, rho_code)
        correlated.append({'rate_times_duration':t,'acceptance':survival,
                           'conditional_trace_distance':dist,
                           'distance_divided_by_time':dist/t})

    # Scalar exchange faults remain inside code and are not caught.
    scalar_logical = vc.conj().T@dot(s,0,1)@vc
    leakage_norm_scalar = norm((eye-p0)@dot(s,0,1)@vc)
    # A generic scalar evolution can spread a vector error to multi-spin
    # support without changing its tensor rank.  Use two different full
    # eight-spin exchange Hamiltonians, including inter-block edges.
    s8 = spinops(8)
    vc8 = np.kron(vc,vc)
    rng = np.random.default_rng(873)
    edges = [(i,j) for i in range(8) for j in range(i+1,8)]
    hs = []
    for k in range(2):
        h = np.zeros((256,256),complex)
        for i,j in edges:
            h += rng.uniform(.01,.8)*dot(s8,i,j)
        vals,vecs = eigh(h)
        hs.append((vecs*np.exp(-1j*(.7+.2*k)*vals))@vecs.conj().T)
    before = hs[0]@vc8
    afterbra = vc8.conj().T@hs[1]
    fault_matrix_norms = [norm(afterbra@s8[i][a]@before)
                          for i in range(8) for a in range(3)]
    out = {
        'four_spin_vector_code_restriction_max_norm':vector_restriction,
        'XXXX_ZZZZ_accepted_dimensions_by_spin_0_1_2':stabilizer_spins,
        'KL_cross_error_eigenvalues':np.linalg.eigvalsh(kl).real.tolist(),
        'correlated_vector_jump_code_effect':q.real.tolist(),
        'correlated_vector_noise_exact_accepted_channel':correlated,
        'undetected_scalar_exchange_logical_matrix':scalar_logical.real.tolist(),
        'scalar_exchange_leakage_norm':leakage_norm_scalar,
        'eight_spin_arbitrary_scalar_control_vector_insertion_max_norm':max(fault_matrix_norms),
        'scope':'Exact finite spin checks. Vector insertion detection is not general circuit fault tolerance.'
    }
    assert max(fault_matrix_norms)<1e-12
    Path(__file__).with_name('spin_selection_scope_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__ == '__main__':
    main()
