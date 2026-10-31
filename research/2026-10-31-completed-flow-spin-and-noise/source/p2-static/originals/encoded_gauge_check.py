"""Full finite-fermion checks for gauge-covariant singlet computation.

This is a matrix verification of stated identities, not a material model or
interval certificate. It includes all two-particle states of three admitted
spinful orbitals and a retained, noncommuting source. No spin-only projection
is used to verify the Hubbard contact/instrument.
"""
from pathlib import Path
from itertools import combinations
import json
import numpy as np
from scipy.linalg import expm, block_diag

HERE = Path(__file__).resolve().parent
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1., -1.]).astype(complex)
S = np.array([0, 1, -1, 0], complex)/np.sqrt(2)
PS = np.outer(S, S.conj())
PT = np.eye(4)-PS

def norm(a):
    return float(np.linalg.norm(a, 2))

def tensor(*xs):
    a = np.array([[1]], complex)
    for x in xs:
        a = np.kron(a, x)
    return a

class Fock:
    def __init__(self, modes, particles):
        self.modes = modes
        self.occ = list(combinations(range(modes), particles))
        self.bits = [sum(1 << q for q in qs) for qs in self.occ]
        self.index = {b: i for i, b in enumerate(self.bits)}
        self.dim = len(self.bits)

    def hop(self, a, b):
        out = np.zeros((self.dim, self.dim), complex)
        for j, old in enumerate(self.bits):
            if not ((old >> b) & 1):
                continue
            sign = (-1)**((old & ((1 << b)-1)).bit_count())
            middle = old ^ (1 << b)
            if (middle >> a) & 1:
                continue
            sign *= (-1)**((middle & ((1 << a)-1)).bit_count())
            new = middle | (1 << a)
            out[self.index[new], j] = sign
        return out

    def number(self, site):
        return self.hop(2*site, 2*site)+self.hop(2*site+1, 2*site+1)

    def lift(self, u):
        return np.array([[np.linalg.det(u[np.ix_(a, b)])
                          for b in self.occ] for a in self.occ])

    def charge_projector(self, charges):
        vals = []
        for b in self.bits:
            vals.append(all(((b >> (2*j)) & 1)+((b >> (2*j+1)) & 1) == q
                            for j, q in enumerate(charges)))
        return np.diag(vals).astype(complex)

def spin_embedding(f):
    v = np.zeros((f.dim, 4), complex)
    for a in range(2):
        for b in range(2):
            v[f.index[(1 << a) | (1 << (2+b))], 2*a+b] = 1
    return v

def sector_source_block(k, p):
    # K_{s e, t f}; trace the spin sector to recover its source coefficient.
    return np.einsum('ts,setf->ef', p, k.reshape(4, 2, 4, 2))/np.trace(p)

def full_fock_check():
    f = Fock(6, 2)
    frames = [expm(.83j*X), expm(-1.17j*Y)@expm(.41j*Z), expm(.77j*Z)]
    gf = f.lift(block_diag(*frames))
    joint_g = np.kron(gf, I)
    ns = [f.number(j) for j in range(3)]
    ds = [f.hop(2*j, 2*j)@f.hop(2*j+1, 2*j+1) for j in range(3)]

    def hamiltonian(physical, phase, general_network):
        h = np.kron(np.eye(f.dim), 19.3*Y+phase*X)
        for j in range(3):
            h += np.kron(ns[j], (.27*j-.13)*Z+(.17*j+.09)*X)
            h += np.kron(ds[j], (.12*j+.03)*Z+(.07*j-.02)*X)
        h += np.kron(ns[0]@ns[1], .06*Y)
        edges = [(0, 1)] + ([(1, 2), (0, 2)] if general_network else [])
        for j, k in edges:
            w = frames[j]@frames[k].conj().T if physical else I
            b = (1.4+.07*j)*I + .21*X + .09*np.cos(phase)*Z
            if general_network:
                b = b + .13j*Y
            term = np.zeros_like(h)
            for s in range(2):
                for t in range(2):
                    term += np.kron(f.hop(2*j+s, 2*k+t)*w[s,t], b)
            h -= term+term.conj().T
        # Density-assisted hopping gives genuinely unequal S->D_L and
        # S->D_R source matrices while remaining spin independent in the
        # common frame. This is retained in the full fermionic model.
        w01 = frames[0]@frames[1].conj().T if physical else I
        hop01 = sum((w01[s,t]*f.hop(s,2+t)
                     for s in range(2) for t in range(2)),
                    np.zeros((f.dim,f.dim),complex))
        assisted = (ns[0]@hop01+hop01@ns[0])/2
        csource = .047*Z+.031j*X
        ac = np.kron(assisted,csource)
        h += ac+ac.conj().T
        # Local singlet pair hopping is gauge invariant (det G_j = 1).
        pair = f.hop(0,2)@f.hop(1,3)
        pc = np.kron(pair,.063*X+.017j*Y)
        h += pc+pc.conj().T
        return h

    h0 = hamiltonian(False, .31, True)
    ha = hamiltonian(True, .31, True)
    full_residual = norm(joint_g.conj().T@ha@joint_g-h0)
    charge_residual = max(norm(gf.conj().T@n@gf-n) for n in ns)

    v = spin_embedding(f)
    va = np.kron(gf@v, I)
    p11 = np.kron(f.charge_projector([1,1,0]), I)
    p20 = np.kron(f.charge_projector([2,0,0]), I)
    p02 = np.kron(f.charge_projector([0,2,0]), I)
    u1 = expm(-.31j*hamiltonian(True, .17, False))
    u2 = expm(-.29j*hamiltonian(True, -.39, False))
    null = va.conj().T@p11@u1@va
    a = sector_source_block(null, PS)
    b = sector_source_block(null, PT)
    null_residual = norm(null-np.kron(PS,a)-np.kron(PT,b))
    returned = []
    for label, double in [('20',p20), ('02',p02)]:
        k = va.conj().T@p11@u2@double@u1@va
        source = sector_source_block(k, PS)
        returned.append(dict(charge=label,
                             factorization_residual=norm(k-np.kron(PS,source)),
                             success_effect_min=float(np.linalg.eigvalsh(source.conj().T@source).min())))
    triplet_opacity = norm((p20+p02)@u1@va@np.kron(PT,I))
    # A local filled orbital is invariant because det(frame)=1.
    dl = np.diag(f.charge_projector([2,0,0])).astype(complex)
    local_pair_residual = norm(gf@dl-dl)
    dr = np.diag(f.charge_projector([0,2,0])).astype(complex)
    singlet_fock = v@S
    hs = hamiltonian(False,.17,False)
    vs = np.kron(singlet_fock[:,None],I)
    vl = np.kron(dl[:,None],I)
    vr = np.kron(dr[:,None],I)
    tl = vl.conj().T@hs@vs
    tr = vr.conj().T@hs@vs
    unequal_contact_norm = norm(tl-tr)
    pair_source_norm = norm(vl.conj().T@hs@vr)
    # Every charge record has a full Fock-space conjugate counterpart.
    ub0 = expm(-.22j*hamiltonian(False, .31, True))
    uba = expm(-.22j*hamiltonian(True, .31, True))
    records = []
    for qs in [(2,0,0),(0,2,0),(0,0,2),(1,1,0),(1,0,1),(0,1,1)]:
        p = np.kron(f.charge_projector(qs),I)
        records.append(norm(p@uba-joint_g@(p@ub0)@joint_g.conj().T))
    return dict(fermion_dimension=f.dim, joint_source_dimension=2*f.dim,
                full_hamiltonian_conjugacy=full_residual,
                charge_invariance=charge_residual,
                full_charge_record_conjugacy=max(records),
                null_singlet_triplet_factorization=null_residual,
                triplet_capture_amplitude=triplet_opacity,
                local_pair_source_invariance=local_pair_residual,
                unequal_contact_operator_norm=unequal_contact_norm,
                retained_double_pair_hopping_norm=pair_source_norm,
                returned_records=returned)

def embed_pair_operator(op, i, j, n=4):
    out = np.zeros((2**n,2**n), complex)
    for b in range(2**n):
        bits = [(b >> (n-1-k)) & 1 for k in range(n)]
        old = 2*bits[i]+bits[j]
        for new in range(4):
            nb = bits.copy()
            nb[i], nb[j] = divmod(new,2)
            a = sum(x << (n-1-k) for k,x in enumerate(nb))
            out[a,b] += op[new,old]
    return out

def encoded_and_failures():
    tp = np.array([1,0,0,0],complex)
    tm = np.array([0,0,0,1],complex)
    t0 = np.array([0,1,1,0],complex)/np.sqrt(2)
    c0 = np.kron(S,S)
    c1 = (np.kron(tp,tm)+np.kron(tm,tp)-np.kron(t0,t0))/np.sqrt(3)
    code = np.column_stack([c0,c1])
    p12 = embed_pair_operator(PS,0,1)
    p23 = embed_pair_operator(PS,1,2)
    z12 = code.conj().T@p12@code
    z23 = code.conj().T@p23@code
    frames = [expm(.33j*X), expm(.87j*Y), expm(-.57j*Z), expm(.19j*(X+Y)/np.sqrt(2))]
    g4 = tensor(*frames)
    physical_code = g4@code
    physical_p23 = g4@p23@g4.conj().T
    encoded_residual = norm(physical_code.conj().T@physical_p23@physical_code-z23)
    # A noncentral unobserved loop on one member changes singlet statistics.
    one_loop = np.kron(1j*Z,I)
    singlet_after_loop = float(abs(np.vdot(S,one_loop@S))**2)
    unresolved_loop_singlet_probability = .5+.5*singlet_after_loop
    # Even a total S=0 acceptance check can filter the encoded qubit.
    both_loop = tensor(1j*Z,1j*Z,I,I)
    restricted = code.conj().T@both_loop@code
    accepted_eigenvalues = np.linalg.eigvalsh(restricted.conj().T@restricted)
    # A rotationally invariant spectator exchange is a logical operation.
    swap = np.eye(4)-2*PS
    spectator = code.conj().T@embed_pair_operator(swap,1,2)@code
    # Every instantaneous 1D connection is flat, yet forward and reverse
    # links at different times need not cancel.
    time_return = (1j*X).conj().T@I
    time_return_fidelity = float(abs(np.vdot(S,np.kron(time_return,I)@S))**2)
    return dict(code_gram_residual=norm(code.conj().T@code-np.eye(2)),
                pair12_in_code=z12.real.tolist(), pair23_in_code=z23.real.tolist(),
                pair_projector_commutator=norm(z12@z23-z23@z12),
                unknown_frame_encoded_instrument_residual=encoded_residual,
                noncentral_loop_singlet_probability=singlet_after_loop,
                unresolved_loop_singlet_probability=unresolved_loop_singlet_probability,
                total_singlet_accepted_operator=restricted.real.tolist(),
                total_singlet_acceptance_eigenvalues=accepted_eigenvalues.tolist(),
                spectator_exchange_in_code=spectator.real.tolist(),
                time_dependent_flat_connection_return_singlet_fidelity=time_return_fidelity)

if __name__ == '__main__':
    result = dict(scope=__doc__,fock=full_fock_check(),encoded=encoded_and_failures())
    for key in ['full_hamiltonian_conjugacy','charge_invariance','full_charge_record_conjugacy',
                'null_singlet_triplet_factorization','triplet_capture_amplitude','local_pair_source_invariance']:
        assert result['fock'][key] < 1e-11, (key,result['fock'][key])
    assert max(x['factorization_residual'] for x in result['fock']['returned_records'])<1e-11
    assert abs(result['encoded']['total_singlet_acceptance_eigenvalues'][0]-1/9)<1e-12
    assert abs(result['encoded']['total_singlet_acceptance_eigenvalues'][1]-1)<1e-12
    assert result['encoded']['unknown_frame_encoded_instrument_residual']<1e-12
    (HERE/'encoded_gauge_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
