"""Exact five-qubit seed controls for finite-rate history restoration.

These are conditional instrument identities, not sampled Poisson histories
or a memory-lifetime benchmark. The all-size proof is in PROOF.md.
"""
from itertools import combinations, product
from fractions import Fraction
from pathlib import Path
from time import perf_counter
import hashlib
import json
import resource
import sympy as s

HERE = Path(__file__).resolve().parent
ONE = s.eye(2)
P1 = {'I': ONE, 'X': s.Matrix([[0, 1], [1, 0]]),
      'Y': s.Matrix([[0, -s.I], [s.I, 0]]), 'Z': s.diag(1, -1)}


def canon(M):
    return M.applyfunc(s.expand)


def matrix(word):
    return s.kronecker_product(*(P1[a] for a in word))


def binary(word):
    x = sum((a in 'XY') << i for i, a in enumerate(word))
    z = sum((a in 'YZ') << i for i, a in enumerate(word))
    return x, z


def syndrome(word, checks):
    x, z = binary(word)
    return tuple(((x & zz).bit_count()+(z & xx).bit_count()) % 2
                 for xx, zz in checks)


def one_site(P, j, n=5):
    return s.kronecker_product(*(P if i == j else ONE for i in range(n)))


def process_chi(kraus):
    # K=sum_P a_P P, a_P=Tr(P^dagger K)/2.
    out = s.zeros(4)
    for K in kraus:
        a = s.Matrix([s.expand(s.trace(P1[p].H*K)/2) for p in 'IXYZ'])
        out += a*a.H
    return canon(out)


def nonzero_offdiag(M):
    return {f'{"IXYZ"[i]}{ "IXYZ"[j]}': str(M[i,j])
            for i in range(4) for j in range(4) if i != j and M[i,j] != 0}


def main():
    t0 = perf_counter()
    n = 5
    gs = ['XZZXI', 'IXZZX', 'XIXZZ', 'ZXIXZ']
    gb = [binary(x) for x in gs]
    G = [matrix(x) for x in gs]
    I = s.eye(32)
    P0 = I
    for A in G:
        P0 = P0*(I+A)/2
    P0 = canon(P0)
    v0 = 4*P0[:,0]
    E = canon(s.Matrix.hstack(v0, matrix('XXXXX')*v0))
    assert E.H*E == s.eye(2)
    assert all(A*E == E for A in G)
    stab = {(0, 0)}
    for x, z in gb:
        stab |= {(a ^ x, b ^ z) for a, b in list(stab)}
    # Find an actual minimum-weight normalizer in this admitted five-qubit seed.
    logical_word = None
    distances = []
    for weight in range(1, 4):
        found = []
        for loc in combinations(range(n), weight):
            for letters in product('XYZ', repeat=weight):
                word = ['I']*n
                for j, p in zip(loc, letters):
                    word[j] = p
                word = ''.join(word)
                if syndrome(word, gb) == (0,0,0,0) and binary(word) not in stab:
                    found.append(word)
        distances.append(len(found))
        if found:
            logical_word = found[0]
            assert weight == 3
            break
    assert logical_word is not None
    L = canon(E.H*matrix(logical_word)*E)
    assert any(L == a*P1[p] for a in (-1,1) for p in 'XYZ')

    # The perfect-code MW decoder: one Pauli per each of16 syndromes.
    reps = {(0,0,0,0): 'IIIII'}
    for j, p in product(range(n), 'XYZ'):
        word = ['I']*n
        word[j] = p
        word = ''.join(word)
        syn = syndrome(word, gb)
        assert syn not in reps
        reps[syn] = word
    assert len(reps) == 16
    projectors = {}
    decoder = {}
    for syn, word in reps.items():
        P = I
        for bit, A in zip(syn, G):
            P = P*(I+(-1)**bit*A)/2
        P = canon(P)
        projectors[syn] = P
        decoder[syn] = canon(E.H*matrix(word)*P)
    assert sum(projectors.values(), s.zeros(32)) == I

    def decode(branches):
        K = [canon(D*v) for D in decoder.values() for v in branches]
        K = [a for a in K if a != s.zeros(2)]
        assert canon(sum((a.H*a for a in K), s.zeros(2))) == s.eye(2)
        return process_chi(K)

    def cut(branches):
        out = [canon(P*v) for P in projectors.values() for v in branches]
        return [v for v in out if v != s.zeros(32,2)]

    def rotate(P):
        U = (3*I+4*s.I*P)/5
        assert canon(U.H*U) == I
        return U

    # Two coherent rotations at one site in an uncut component: probabilities
    # must retain interference, rather than pretending the two events twirled.
    PX = one_site(P1['X'], 0)
    U = rotate(PX)
    uncut = canon(U*U*E)
    synx = syndrome('XIIII', gb)
    p_x = canon(projectors[synx]*uncut).norm()**2/2
    p_x = s.simplify(p_x)
    assert p_x == s.Rational(576,625)
    naive = 2*s.Rational(9,25)*s.Rational(16,25)
    assert naive == s.Rational(288,625)
    assert decode([uncut]) == s.diag(1,0,0,0)

    # Arbitrary coherent+nonunital faults on a correctable two-site union,
    # with an intervening nominal syndrome-based correction outside the union.
    Qplus = (I+G[0])/2
    Qminus = one_site(P1['X'], 2)*(I-G[0])/2
    Hphase = (3*I+4*s.I*G[1])/5
    damp = [s.diag(1, s.Rational(3,5)),
            s.Matrix([[0,s.Rational(4,5)],[0,0]])]
    branches = [canon(one_site(A,1)*Hphase*Q*U*E)
                for A in damp for Q in (Qplus,Qminus)]
    chi_small = decode(branches)
    assert not nonzero_offdiag(chi_small)

    # An unsealed component on a minimum logical support really can retain
    # coherent logical noise. This makes the correctability premise necessary.
    rotations = [rotate(one_site(P1[p], j))
                 for j,p in enumerate(logical_word) if p != 'I']
    v = E
    for Uj in rotations:
        v = canon(Uj*v)
    chi_large = decode([v])
    assert nonzero_offdiag(chi_large)
    assert any(abs(x) == s.Rational(3456,15625)
               for i in range(4) for j in range(4) if i != j
               for x in [chi_large[i,j]])

    # The same three events, now separated by actual local-check cuts.
    branches = [E]
    for Uj in rotations:
        branches = cut([canon(Uj*v) for v in branches])
    chi_cut = decode(branches)
    assert not nonzero_offdiag(chi_cut)
    # Strong same-information ordinary comparator: exact Pauli mixture after
    # complete cuts, not an inferred noisy-device process.
    ordinary = s.zeros(4)
    support = [(j,p) for j,p in enumerate(logical_word) if p != 'I']
    for labels in product((0,1), repeat=3):
        P = I
        prob = s.Integer(1)
        for a,(j,p) in zip(labels,support):
            prob *= s.Rational(16 if a else 9,25)
            if a:
                P = one_site(P1[p],j)*P
        ordinary += prob*decode([P*E])
    assert chi_cut == canon(ordinary)

    # Exact one-check interval law, the ordinary Palm/Gamma-Poisson control.
    f = Fraction(1,64)
    gamma = Fraction(1)
    p = f/(f+gamma)
    coefficients = [Fraction(k+1)*(1-p)**2*p**k for k in range(12)]
    tails = [p**(m-1)*(m-(m-1)*p) for m in range(1,9)]
    for m in range(1,8):
        assert tails[m-1]-tails[m] == coefficients[m-1]
    # General constants in the proof: Bernoulli bounds, not b-screen evidence.
    queue_joint_factor = Fraction(128,169)
    assert queue_joint_factor < 1
    result = {
      'scope':'Exact conditional instruments on the SAME five-qubit seed; no sampled trajectories or acquired memory threshold',
      'check_words':gs,
      'nontrivial_normalizers_by_weight_through_distance':distances,
      'distance':3,
      'minimum_logical_word':logical_word,
      'logical_matrix':str(L),
      'uncut_repeated_event_syndrome_probability':str(p_x),
      'incorrect_independent_twirl_probability':str(naive),
      'two_site_nonunital_nominal_correction_chi':str(chi_small),
      'uncut_logical_support_chi':str(chi_large),
      'uncut_logical_support_offdiagonal':nonzero_offdiag(chi_large),
      'separated_same_three_faults_chi':str(chi_cut),
      'matched_exact_pauli_mixture_equal':True,
      'single_check_palm_interval_coefficients':[str(x) for x in coefficients],
      'single_check_palm_cluster_tails':[str(x) for x in tails],
      'universal_queue_joint_factor_upper':str(queue_joint_factor),
      'samples':0,
      'seconds_excluding_imports':perf_counter()-t0,
      'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (HERE/'EXACT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('distance','minimum_logical_word',
        'uncut_logical_support_offdiagonal','matched_exact_pauli_mixture_equal',
        'seconds_excluding_imports','samples')},indent=2))


if __name__ == '__main__':
    main()
