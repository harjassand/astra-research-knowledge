"""Exact unitary intertwiner from the peer's acquired real-spin source."""
import sys
sys.dont_write_bytecode = True
import importlib.util, hashlib, json
import sympy as S
from positive_gate import BASE, spin

SOURCE = BASE/'sources/source_local_gibbs_gate.py'


def run():
    spec = importlib.util.spec_from_file_location('read_only_spin_source', SOURCE)
    source = importlib.util.module_from_spec(spec); spec.loader.exec_module(source)
    g, _, hsource = source.exact_spin2(); J = [S.I*x for x in g]
    eig = (J[2]+2*S.eye(5)).nullspace()[0]
    eig = eig/S.sqrt((eig.conjugate().T*eig)[0])
    vectors = [eig]; raising = J[0]+S.I*J[1]
    for m in range(-2, 2):
        vectors.append((raising*vectors[-1]/S.sqrt(6-m*(m+1))).applyfunc(S.simplify))
    U = S.Matrix.hstack(*vectors)
    ms, z, plus, minus, hmarshall = spin()
    assert (U.conjugate().T*U).applyfunc(S.simplify) == S.eye(5)
    assert (U.conjugate().T*J[2]*U).applyfunc(S.simplify) == z
    assert (U.conjugate().T*raising*U).applyfunc(S.simplify) == plus
    D = S.diag(1, -1, 1, -1, 1)
    W = S.kronecker_product(U*D, U)
    assert (W.conjugate().T*hsource*W-hmarshall).applyfunc(S.simplify) == S.zeros(25)
    words = [S.eye(5)]; current = [S.eye(5)]; ranks = []
    for degree in range(5):
        if degree:
            current = [(a*b).applyfunc(S.simplify) for a in current for b in g]
            words.extend(current)
        ranks.append(S.Matrix.hstack(*(w.reshape(25, 1) for w in words)).rank())
    assert ranks == [1, 4, 9, 16, 25]
    result = dict(status='EXACT_SOURCE_UNITARY_AND_BIPARTITE_MARSHALL_GAUGE_VERIFIED',
        source=str(SOURCE), source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        U=[[str(U[i, j]) for j in range(5)] for i in range(5)],
        one_sublattice_D=[1, -1, 1, -1, 1],
        cumulative_generator_word_span_ranks_degree0_to4=ranks,
        identity='(U D tensor U)^dagger Hbond_source (U D tensor U) = Hbond_Marshall',
        scope='Every even periodic ring has a consistent alternating local unitary. Exact polynomial and exponential gates inherit the same physical trace conjugacy.')
    (BASE/'results/SOURCE_GAUGE_CHECK.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
