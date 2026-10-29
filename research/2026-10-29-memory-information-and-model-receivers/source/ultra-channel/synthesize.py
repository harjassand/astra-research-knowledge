"""Construct graph channels and the noncommuting rational qubit receiver."""
import json
from pathlib import Path
from time import perf_counter
import sympy as s
from compile_order import compile_channel

HERE = Path(__file__).resolve().parent


def graph_channels(n, edges, weight, erasure, crossover):
    w, e, d = map(s.Rational, (weight, erasure, crossover))
    P, Q = [], []
    incident = [s.Rational(0)] * n
    for i, j in edges:
        assert 0 <= i < j < n
        incident[i] += w
        incident[j] += w
        P.extend([{i: w*(1-e)}, {j: w*(1-e)}, {i: w*e, j: w*e}])
        Q.extend([{i: w*(1-d), j: w*d}, {i: w*d, j: w*(1-d)}])
    for i, mass in enumerate(incident):
        assert 0 <= mass <= 1
        if mass < 1:
            P.append({i: 1-mass})
            Q.append({i: 1-mass})
    return {"n": n, "P": [{str(i): str(x) for i,x in row.items()} for row in P],
            "Q": [{str(i): str(x) for i,x in row.items()} for row in Q]}


def matrix_json(M):
    return [[[str(s.re(z)), str(s.im(z))] for z in M.row(i)] for i in range(M.rows)]


def quantum_receiver(d):
    I = s.eye(2)
    pauli = [s.Matrix([[0,1],[1,0]]), s.Matrix([[0,-s.I],[s.I,0]]),
             s.diag(1,-1)]
    signs = [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
    primitive = [I/4 + sum((v*z/16 for v,z in zip(sg,pauli)), s.zeros(2)) for sg in signs]
    E = [sum((s.Rational(a)*primitive[int(i)] for i,a in r.items()),s.zeros(2)) for r in d['P']]
    F = [sum((s.Rational(a)*primitive[int(i)] for i,a in r.items()),s.zeros(2)) for r in d['Q']]
    for rows in [primitive,E,F]:
        assert sum(rows,s.zeros(2)) == I
        for M in rows:
            assert M == M.conjugate().T and M[0,0]>0 and s.det(M)>0
    D = (pauli[1]+pauli[2])/4
    rho_plus, rho_minus = I/2+D, I/2-D
    scores = {}
    for name, rows in [('E',E),('F',F)]:
        z = [s.simplify(s.trace(M*D)) for M in rows]
        assert sum(z)==0
        scores[name] = {'scores':list(map(str,z)), 'guess_success':str((1+sum(abs(a) for a in z))/2)}
    gap=s.Rational(scores['F']['guess_success'])-s.Rational(scores['E']['guess_success'])
    assert gap==s.Rational(1,640)
    coordinates=s.Matrix([[s.trace(M*z)/2 for z in [I]+pauli] for M in primitive])
    comm=primitive[0]*primitive[1]-primitive[1]*primitive[0]
    return {'primitive':[matrix_json(M) for M in primitive],
            'primitive_coordinate_determinant':str(coordinates.det()),
            'primitive_commutator_HS_squared':str(s.simplify(s.trace(comm.conjugate().T*comm))),
            'primitive_min_eigenvalue_lower':'1/8',
            'E':[matrix_json(M) for M in E], 'F':[matrix_json(M) for M in F],
            'rho_plus':matrix_json(rho_plus),'rho_minus':matrix_json(rho_minus),
            'signed_primitive_probabilities':list(map(str,[s.simplify(s.trace(M*D)) for M in primitive])),
            'binary_guessing':scores,'F_minus_E_guess_success':str(gap),
            'no_degrader_certificate':{'edge':[0,1],'P_erasure_common_mass':'3/40',
                                      'Q_total_common_capacity':'1/20', 'strict_deficit':'1/40'}}


def main():
    begin=perf_counter()
    d=graph_channels(4,[(0,1),(1,2),(2,3)],s.Rational(1,4),s.Rational(3,10),s.Rational(1,10))
    (HERE/'CHANNELS.json').write_text(json.dumps(d,indent=2)+'\n')
    good=compile_channel(d)
    good['quantum_receiver']=quantum_receiver(d)
    # Reverse the same source to exercise the exact failure-witness branch.
    bad={'n':d['n'],'P':d['Q'],'Q':d['P']}
    failure=compile_channel(bad)
    assert good['complete_order'] and not failure['complete_order']
    out={'ordered_source':good,'reversed_same_source':failure,
         'total_synthesis_seconds':perf_counter()-begin,
         'scope':'exact rational constructed channels; no device/source inference or sampled references'}
    (HERE/'SYNTHESIS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'complete_order':good['complete_order'],'failure_gap':failure['failure_witness']['gap'],
                      'guessing_reversal':good['quantum_receiver']['F_minus_E_guess_success'],
                      'seconds':out['total_synthesis_seconds']}))


if __name__=='__main__':
    main()
