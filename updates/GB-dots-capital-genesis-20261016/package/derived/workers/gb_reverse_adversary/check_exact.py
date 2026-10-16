"""Bounded independent exact checks; universal statements are proved in REPORT.md.

Uses SymPy only. Does not import, run, or modify any supplied package script.
"""
import json
from pathlib import Path
import sympy as S

F = S.Rational
I = S.eye(2)
X = S.Matrix([[0, 1], [1, 0]])
Y = S.Matrix([[0, -S.I], [S.I, 0]])
Z = S.diag(1, -1)
out = {}


def simple(x):
    return S.simplify(S.factor(x))


def qubit_sld(B, H):
    """Solve the complete qubit Sylvester equation, including nonzero traces."""
    b = S.trace(B) / 2
    h = S.trace(H) / 2
    B0, H0 = B - b * I, H - h * I
    l0 = simple((b * h - S.trace(B0 * H0) / 2) /
                (b * b - S.trace(B0 * B0) / 2))
    L = (l0 * I + (H0 - l0 * B0) / b).applyfunc(simple)
    assert (B * L + L * B - 2 * H).applyfunc(simple) == S.zeros(2)
    return simple(S.trace(H * L))


def pd2(A):
    assert A == A.conjugate().T
    assert A[0, 0] > 0 and simple(A.det()) > 0


# Exact radius and a concrete failure of general decision/simulation transfer.
T = S.Matrix([[F(1, 2), F(1, 6), F(1, 3)],
              [F(1, 3), F(1, 2), F(1, 6)],
              [F(1, 6), F(1, 3), F(1, 2)]])
u = S.Matrix([F(3, 11)] * 3)
p = [F(1, 3)] * 3
primal = [simple(sum((T[y, i] - u[y]) ** 2 / T[y, i]
                     for y in range(3))) for i in range(3)]
dual = 1 - sum(1 / sum(p[i] / T[y, i] for i in range(3))
               for y in range(3))
assert primal == [F(2, 11)] * 3 and dual == F(2, 11)
q = F(1, 4)
w = S.Matrix([F(1, 3)] * 3)
D = S.Matrix.hstack(*[(T[:, i] - (1 - q) * w) / q
                      for i in range(3)], w)
E = S.Matrix.vstack(q * S.eye(3), S.ones(1, 3) * (1 - q))
assert D * E == T and D.T * S.ones(3, 1) == S.ones(4, 1)
for i in range(3):
    M = S.diag(*T[:, i]) - D * S.diag(*E[:, i]) * D.T
    assert all(v >= 0 for v in M.eigenvals())
tv = sum(abs(T[y, 0] - T[y, 1]) for y in range(3)) / 2
guess_T, guess_E = (1 + tv) / 2, (1 + q) / 2
mmse_T = 1 - sum((T[y, 0] - T[y, 1]) ** 2 /
                  (2 * (T[y, 0] + T[y, 1])) for y in range(3))
simulation_q = 1 - sum(min(T[y, i] for i in range(3)) for y in range(3))
assert tv == F(1, 3) and guess_T == F(2, 3) and guess_E == F(5, 8)
assert mmse_T == F(157, 180) and 1 - q == F(3, 4)
assert simulation_q == F(1, 2) and min(D) == -F(1, 3)
out['cyclic'] = dict(complete_threshold=str(dual), chosen_q=str(q),
                     guess_target=str(guess_T), guess_erasure=str(guess_E),
                     mmse_target=str(mmse_T), mmse_erasure=str(1-q),
                     stochastic_simulation_threshold=str(simulation_q))

# Noncommuting faithful CQ primal and harmonic dual; no optimizer used.
sig = [(I + F(3, 5) * P) / 2 for P in (X, Y, Z)]
M = sum((A.inv() / 3 for A in sig), S.zeros(2))
U = M.inv()
cost = [simple(S.trace((A-U) * A.inv() * (A-U))) for A in sig]
assert cost == [F(3, 11)] * 3 and 1 - S.trace(U) == F(3, 11)
assert S.trace(U) == F(8, 11)
out['pauli_radius'] = dict(complete=str(cost[0]), ordinary_sld='9/50',
                           ordinary_rld='9/41', trace_free_center=str(S.trace(U)))
frame = [S.Matrix([1, 0]), S.Matrix([-F(1,2), S.sqrt(3)/2]),
         S.Matrix([-F(1,2), -S.sqrt(3)/2])]
Rframe = [F(2,3)*v*v.T for v in frame]
Hframe = [Rframe[0], -Rframe[1], S.zeros(2)]
Kframe = sum(Hframe, S.zeros(2))
Eframe = simple(sum(S.trace(h*R.pinv()*h) for h,R in zip(Hframe,Rframe))
                - S.trace(Kframe*Kframe))
Aframe = sum((S.kronecker_product(sig[i], Rframe[i]) for i in range(3)), S.zeros(4))
Jframe = sum((S.kronecker_product(sig[i], Hframe[i]) for i in range(3)), S.zeros(4))
Nframe = simple(S.trace(Jframe*Aframe.inv()*Jframe)-S.trace(Kframe*Kframe))
assert Eframe == F(2,3) and Nframe == F(2,11)
out['pauli_same_dimension_supported_witness'] = dict(reference_dimension=2,
                                                    input_excess=str(Eframe),
                                                    output_excess=str(Nframe),
                                                    unequal_reference_marginals=True)

# Pure-state pseudoinverse counterexample and supported regularization limit.
v0, v1 = S.Matrix([1, 0]), S.Matrix([F(3, 5), F(4, 5)])
P0, P1 = v0*v0.T, v1*v1.T
assert (S.eye(2) - P0).nullspace()[0] is not None
assert S.Matrix.hstack(v0, v1).det() != 0
naive = 1 - S.trace(((P0 + P1) / 2).inv())
assert naive == -F(21, 4)
e = S.symbols('e', positive=True)
harmonic = ((P0 + e*I).inv()/2 + (P1 + e*I).inv()/2).inv()
assert harmonic.applyfunc(lambda x: S.limit(x, e, 0)) == S.zeros(2)
out['singular_pure_pair'] = dict(common_support_dimension=0, true_threshold='1',
                                 invalid_naive_pseudoinverse_value=str(naive))

# Nonzero common support example: intersect span(e0,e1), span(e0,e2).
A0, A1 = S.diag(F(1, 2), F(1, 2), 0), S.diag(F(1, 4), 0, F(3, 4))
harmonic3 = ((A0 + e*S.eye(3)).inv()/2 +
             (A1 + e*S.eye(3)).inv()/2).inv()
limit3 = harmonic3.applyfunc(lambda x: S.limit(x, e, 0))
assert limit3 == S.diag(F(1, 3), 0, 0)
# The fixed-common-support dual optimum is at p=(0,1), but this is a LIMIT
# of positive-prior witnesses and must not be evaluated using a changed support.
U3 = S.diag(F(1, 4), 0, 0)
f3 = [simple(1 - 2*S.trace(U3) + S.trace(U3*A.pinv()*U3)) for A in (A0,A1)]
assert f3 == [F(5, 8), F(3, 4)]
assert 1 - F(1, 4) == F(3, 4)
out['singular_common_support'] = dict(common_support_dimension=1,
                                      threshold='3/4', half_prior_harmonic_trace='1/3',
                                      boundary_prior_requires_positive_approximation=True)


def bell_fixture(a2, b, delta, t, reveal):
    """All-parameter Bell observable checked against the full 4D equation."""
    a = S.sqrt(a2)
    Ap = (I + b * Z) / 2
    raw_B = S.kronecker_product(Ap, S.diag(1, delta))
    raw_H = a * S.kronecker_product(X, X) / 2
    lp, lm = (1+b)/2, (1-b)/2
    O = S.zeros(4)
    O[0, 3] = O[3, 0] = t*a/(lp+delta*lm)
    O[1, 2] = O[2, 1] = t*a/(lm+delta*lp)
    assert (raw_B*O + O*raw_B - 2*t*raw_H).applyfunc(simple) == S.zeros(4)
    source = simple(1 - reveal*4*t*t/(1+delta)**2)
    target = simple(1 - S.trace(t*raw_H*O)/(1+delta))
    for sign in (-1, 1):
        pd2(S.Matrix([[1, sign*t], [sign*t, delta]])/(1+delta))
    bell = [S.Matrix([1, 0, 0, s])/S.sqrt(2) for s in (1, -1)]
    bell += [S.Matrix([0, 1, s, 0])/S.sqrt(2) for s in (1, -1)]
    for vec in bell:
        assert (O*vec - (vec.T*O*vec)[0]*vec).applyfunc(simple) == S.zeros(4,1)
    return source, target, simple(source-target)


# Independent exact preferred Bell-protocol risks.
source, target, gap = bell_fixture(F(81, 200), 9/(10*S.sqrt(2)),
                                    F(1, 10), F(3, 10), F(9, 20))
assert source == F(524, 605) and target == F(14723, 17639)
assert gap == F(335421, 10671595)
out['preferred_bell'] = dict(source_mmse=str(source), target_mmse=str(target), gap=str(gap))

# Fully finite pure-output witness; reference inputs are faithful, output
# union support is 2D even though each prepared output has rank one.
source, target, gap = bell_fixture(F(1, 2), 1/S.sqrt(2),
                                    F(1, 16), F(1, 5), F(3, 4))
assert gap == F(24832, 2550425) > 0
out['finite_singular_sld_witness'] = dict(reference_dimension=2,
                                        q='3/4', gap=str(gap), faithful_encoding=True,
                                        equal_reference_marginals=True)

# Reconstruct the rational qubit-reference fixed receiver from the specified
# state and observable data, including the nonzero erased-reference term.
base = Path('/Users/harjas/Downloads/Dots/Astra_qubit_reference_Bell_addendum_2026-10-15/checks')
fixture = json.loads((base/'fixture.json').read_text())
receiver = json.loads((base/'receiver.json').read_text())
# Schema is intentionally read as data below; no supplied executable imported.
out['fixture_schema'] = dict(fixture_keys=sorted(fixture), receiver_keys=sorted(receiver))
states = []
for real, imag in zip(fixture['real_numerators'], fixture['imag_numerators']):
    blocks = [(S.Matrix(re)+S.I*S.Matrix(im))/fixture['denominator']
              for re, im in zip(real,imag)]
    assert sum(S.trace(B) for B in blocks) == 1
    for B in blocks:
        pd2(B-I/1000)
        pd2(F(3,5)*I-B)
    states.append(blocks)
Bs = [(a+b)/2 for a,b in zip(*states)]
Hs = [(a-b)/2 for a,b in zip(*states)]
W, K = sum(Bs,S.zeros(2)), sum(Hs,S.zeros(2))
assert K != S.zeros(2)
Ginput = sum(qubit_sld(B,H) for B,H in zip(Bs,Hs))
Gref = qubit_sld(W,K)
source_gain = simple(Ginput/5+4*Gref/5)
A = sum((S.kronecker_product(s,B) for s,B in zip(sig,Bs)), S.zeros(4))
J = sum((S.kronecker_product(s,H) for s,H in zip(sig,Hs)), S.zeros(4))
Lfixed = (S.Matrix(receiver['real_numerators'])+
          S.I*S.Matrix(receiver['imag_numerators']))/receiver['denominator']
assert Lfixed == Lfixed.conjugate().T
fixed_gain = simple(2*S.trace(J*Lfixed)-S.trace(A*Lfixed*Lfixed))
gap = simple(fixed_gain-source_gain)
assert Gref == F(43227124794193,892341237500000)
assert fixed_gain == F(2151143651639,20000000000000)
assert gap == F(8360352958858328928696700289758492365162202649,
                1602805342290558616614381584839931820000000000000)
assert gap > F(1,200)
out['rational_three_input_fixed_receiver'] = dict(reference_dimension=2,
                                                 source_explained=str(source_gain),
                                                 reference_explained=str(Gref),
                                                 target_fixed_explained=str(fixed_gain),
                                                 achieved_gap=str(gap),
                                                 erased_reference_term_retained=True)

# Dimension-sensitive projection lemma's exact scalar identity.
rank, pp, qq = S.symbols('rank pp qq', real=True)
assert S.expand(rank**2*pp+qq-(rank+1)**2*pp*qq -
                ((rank*pp-qq)**2+(1-pp-qq)*(rank**2*pp+qq))) == 0
assert F(1,4)/(F(1,2)+F(1,8)*F(3,2)) == F(4,11)
out['finite_reference_law'] = dict(m=4, r=2, lambda_value='1/2', coefficient='4/11',
                                   scalar='1/3', complete='3/8', projection_identity=True)

# The sharper simulator identity is algebraic; its uniform quantifier is
# established separately in REPORT.md. Square-root comparisons are positive.
aa, bb, reveal, L = S.symbols('aa bb reveal L', real=True)
sim = S.Matrix([reveal*aa/L, 0, 1-reveal+reveal*(bb-1+reveal)/L])
desired = S.Matrix([aa, 0, bb])
assert S.simplify(desired-sim - (1-reveal/L)*S.Matrix([aa,0,bb-1+reveal])) == S.zeros(3,1)
assert S.expand(aa**2+(bb-1+reveal)**2 - (reveal**2+2*(1-reveal)*(1-bb))).subs(aa**2,1-bb**2).expand() == 0
x, A, Q = S.symbols('x A Q', positive=True)
bell_gap = (1-x)*(A/(1-(1-A)*x)-Q)
xstar = (1-A/S.sqrt(Q))/(1-A)
assert simple(bell_gap.subs(x,xstar) - A/(1-A)*(1-S.sqrt(Q))**2) == 0
assert simple(S.diff(bell_gap,x) - (Q-A*A/(1-(1-A)*x)**2)) == 0
out['pure_pair_payoff'] = dict(simulator_trace_norm='sqrt(q^2+2(1-q)(1-b))-q',
                               all_encoding_mmse_upper='2*(sqrt(q^2+2(1-q)(1-b))-q)',
                               bell_family_stationary_sup='a^2/(1-a^2)*(1-sqrt(q))^2',
                               stationary_formula_condition='0<a<1 and a^4<=q<=1',
                               other_branch='q<a^4: supremum a^2-q')

print(json.dumps(out, indent=2))
