"""Self-authored finite exact algebra checks; not a universal proof or search.

Reads no scientific source code. Uses the already available SymPy library.
Every asserted matrix identity is exact over rational complex entries.
"""
from pathlib import Path
from time import perf_counter
import json
import platform
import sympy as s

START = perf_counter()
BASE = Path(__file__).resolve().parent
I = s.I
R = s.Rational
CHECKS = []


def zero(a):
    return all(s.simplify(v) == 0 for v in a)


def eq(a, b):
    assert a.shape == b.shape
    assert zero(a - b)


def record(name, **details):
    CHECKS.append(dict(name=name, passed=True, **details))


def digits(n, dims):
    out = []
    for d in reversed(dims):
        out.append(n % d)
        n //= d
    return list(reversed(out))


def index(ds, dims):
    n = 0
    for v, d in zip(ds, dims):
        n = n * d + v
    return n


def reorder(a, dims, order):
    target = [dims[k] for k in order]
    entries = {}
    for (r, c), v in s.SparseMatrix(a).todok().items():
        rr, cc = digits(r, dims), digits(c, dims)
        entries[index([rr[k] for k in order], target),
                index([cc[k] for k in order], target)] = v
    n = s.prod(target)
    return s.SparseMatrix(n, n, entries)


def trace_factors(a, dims, remove):
    keep = [k for k in range(len(dims)) if k not in remove]
    target = [dims[k] for k in keep]
    entries = {}
    for (r, c), v in s.SparseMatrix(a).todok().items():
        rr, cc = digits(r, dims), digits(c, dims)
        if any(rr[k] != cc[k] for k in remove):
            continue
        key = (index([rr[k] for k in keep], target),
               index([cc[k] for k in keep], target))
        entries[key] = entries.get(key, 0) + v
    n = s.prod(target)
    return s.SparseMatrix(n, n, entries)


def dagger(a):
    return a.conjugate().T


# 1. Two private parity bits, two message bits and a bath qubit.
q, b = 4, 2
copy = s.zeros(q*q*b)
for a in range(q):
    for m in range(q):
        for e in range(b):
            copy[(a*q+(m ^ a))*b+e, (a*q+m)*b+e] = 1
rot = s.Matrix([[R(3, 5), R(4, 5)], [-R(4, 5), R(3, 5)]])
perm = s.zeros(8)
for m in range(4):
    for e in range(2):
        # Swap the first message bit with the bath and also mix the bits.
        m1, m2 = m >> 1, m & 1
        mm, ee = (e << 1) | (m2 ^ m1), m1
        perm[mm*2+ee, m*2+e] = 1
phases = s.diag(1, I, -1, -I, 1, -I, -1, I)
u = perm * s.kronecker_product(rot, rot, rot) * phases
eq(dagger(u)*u, s.eye(8))
whole = copy * s.kronecker_product(s.eye(q), u) * copy
kraus = []
for m in range(q):
    k = s.zeros(q*b)
    for a in range(q):
        for aa in range(q):
            k[a*b:(a+1)*b, aa*b:(aa+1)*b] = whole[
                (a*q+m)*b:(a*q+m+1)*b, (aa*q)*b:(aa*q+1)*b]
    kraus.append(k)
zs = [s.diag(*[(-1)**((a >> bit) & 1) for a in range(q)])
      for bit in range(2)]
for k in kraus:
    for z in zs:
        zz = s.kronecker_product(z, s.eye(b))
        eq(k*zz, zz*k)
eq(sum((dagger(k)*k for k in kraus), s.zeros(q*b)), s.eye(q*b))
assert any(not zero(k) for k in kraus[1:])
record('arbitrary_joint_prover_preserves_both_private_parities',
       whole_dimension=32, induced_kraus_dimension=8,
       returned_garbage_can_be_nonzero=True, postselection=False)


# 2. Exact lossless controlled-bath simulation, including message reset.
blocks = [s.eye(2), s.Matrix([[0, 1], [1, 0]]), s.diag(I, -I), rot]
d = s.diag(*blocks)
whole_d = copy * s.kronecker_product(s.eye(q), d) * copy
for m in range(q):
    k = s.zeros(q*b)
    for a in range(q):
        for aa in range(q):
            k[a*b:(a+1)*b, aa*b:(aa+1)*b] = whole_d[
                (a*q+m)*b:(a*q+m+1)*b, (aa*q)*b:(aa*q+1)*b]
    eq(k, d if m == 0 else s.zeros(q*b))
record('lossless_joint_parity_diagonal_unitary_and_reset',
       common_bath_dimension=2, message_dimension=4, physical_dimension=8)


# 3. Nonnormal contraction, with singular values exactly 0, 3/5 and 1.
r3 = s.diag(rot, s.ones(1))
w3 = s.Matrix([[0, 1, 0], [0, 0, I], [1, 0, 0]])
p = r3*s.diag(0, R(3, 5), 1)*dagger(r3)
t = r3*s.diag(1, R(4, 5), 0)*dagger(r3)
k = w3*p
up, um = w3*(p+I*t), w3*(p-I*t)
eq(dagger(up)*up, s.eye(3))
eq(dagger(um)*um, s.eye(3))
eq((up+um)/2, k)
z3 = s.zeros(3)
b6 = s.BlockMatrix([[z3, k], [dagger(k), z3]]).as_explicit()
x6 = s.BlockMatrix([[z3, s.eye(3)], [s.eye(3), z3]]).as_explicit()
dp, dm = s.diag(up, s.eye(3)), s.diag(um, s.eye(3))
eq((dp*x6*dagger(dp)+dm*x6*dagger(dm))/2, b6)
lam = s.Symbol('lam')
assert s.expand(b6.charpoly(lam).as_expr()
                - lam**2*(lam**2-R(9,25))*(lam**2-1)) == 0
record('odd_contraction_average_of_two_diagonal_conjugates',
       block_dimension=3, odd_generator_dimension=6,
       exact_singular_values=['0', '3/5', '1'])


# 4. Unequal joint sector ranks (including one empty sector).
j = s.zeros(8, 4)
for old, new in enumerate([0, 2, 3, 6]):
    j[new, old] = 1
eq(dagger(j)*j, s.eye(4))
z_old = [s.diag(1, 1, 1, -1), s.diag(1, -1, -1, -1)]
z_pad = [s.kronecker_product(s.diag(1, 1, -1, -1), s.eye(2)),
         s.kronecker_product(s.diag(1, -1, 1, -1), s.eye(2))]
v1, v2 = s.zeros(4), s.zeros(4)
v1[1,3] = v1[3,1] = R(3,5)
v1[2,3] = v1[3,2] = R(4,5)
v2[0,1] = v2[1,0] = R(3,5)
v2[0,2] = v2[2,0] = R(4,5)
for i, v in enumerate([v1,v2]):
    vv = j*v*dagger(j)
    eq(vv*j, j*v)
    eq(vv*z_pad[i]+z_pad[i]*vv, s.zeros(8))
    eq(vv*z_pad[1-i]-z_pad[1-i]*vv, s.zeros(8))
for z, zz in zip(z_old, z_pad):
    eq(zz*j, j*z)
    for r in range(4):
        for c in range(4):
            e = s.zeros(4); e[r,c] = 1
            old_pinch = (e+z*e*z)/2
            ee = j*e*dagger(j)
            new_pinch = (ee+zz*ee*zz)/2
            eq(j*old_pinch*dagger(j), new_pinch)
record('sector_padding_intertwines_odd_generators_and_actual_pinches',
       sector_ranks=[1,2,0,1], original_dimension=4,
       padded_dimension=8, common_bath_dimension=2,
       pinch_matrix_units_checked=32)


# 5. Three tester turns (two exchanges), with a nontrivial channel Choi factor.
# Prefix factor order is [Y1,Y2,X2] and finally [Y1,Y2,X2,X3].
rho1 = s.Matrix([[R(9,25), R(12,25)], [R(12,25), R(16,25)]])
rho2 = s.diag(R(1,3),R(2,3))
omega = s.Matrix([1,0,0,1])
omega_x = s.Matrix([0,1,1,0])
pref1 = [rho1,rho2]
pref2 = [s.kronecker_product(rho1,omega*dagger(omega)),
         s.kronecker_product(rho2,omega_x*dagger(omega_x))]
pref3 = [s.kronecker_product(a,s.eye(2)) for a in pref2]
for a, r in zip(pref2,pref1):
    eq(trace_factors(a,[2,2,2],[1]),s.kronecker_product(r,s.eye(2)))
prod1=s.kronecker_product(*pref1)
prod2=reorder(s.kronecker_product(*pref2),[2]*6,[0,3,1,4,2,5])
eq(trace_factors(prod2,[2]*6,[2,3]),s.kronecker_product(prod1,s.eye(4)))
prod3=reorder(s.kronecker_product(*pref3),[2]*8,[0,4,1,5,2,6,3,7])
eq(prod3,s.kronecker_product(prod2,s.eye(4)))
assert s.trace(prod3)==16  # Product input dimensions 1*4*4.
record('tensor_comb_prefix_constraints_with_round_regrouping',
       local_turns=3, local_message_exchanges=2,
       local_prefix_dimensions=[2,8,16],
       combined_prefix_dimensions=[4,64,256],
       combined_full_trace=16)


# 6. Distinct own-pinch times in a nine-level independent fresh-sink witness.
def sink_rotation(c, sn, target):
    a=s.eye(3)
    a[0,0]=a[target,target]=c
    a[0,target]=a[target,0]=-I*sn
    return a


def pinch(rho,z):
    return (rho+z*rho*z)/2


early=sink_rotation(R(3,5),R(4,5),1)
late=sink_rotation(R(5,13),R(12,13),2)
z=s.diag(1,-1,-1)
state=s.zeros(9);state[0,0]=1
for a,zz in [
    (s.kronecker_product(early,s.eye(3)),s.kronecker_product(z,s.eye(3))),
    (s.kronecker_product(s.eye(3),early),s.kronecker_product(s.eye(3),z))]:
    state=pinch(a*state*dagger(a),zz)
for a in [s.kronecker_product(late,s.eye(3)),s.kronecker_product(s.eye(3),late)]:
    state=a*state*dagger(a)
target=s.kronecker_product(s.diag(0,1,1),s.diag(0,1,1))
q_single=1-R(9,25)*R(25,169)
p_joint=s.trace(target*state)
assert q_single==R(160,169)
assert p_joint==q_single**2==R(25600,28561)
record('staggered_two_coordinate_fresh_sink_equality',
       physical_dimension=9, own_gaps_per_coordinate=2,
       internal_own_pinches=2, own_pinch_times_distinct=True,
       singleton='160/169',joint='25600/28561')


# 7. Exact prior analytic obstruction arithmetic, retained in its proper class.
c,d=s.symbols('c d',real=True)
poly=(1-c*c)*(3+2*d)**2/25+(1-d*d)*(3+2*c)**2/25
poly+=(1-c*c)*(1-d*d)/25+6*(1-c-d-c*d)**2/25+c*c*d*d/25
assert s.expand(poly-1)==0
abstract_odd=(1-R(16,25))*(3+2*R(4,5))**2/25*2
assert abstract_odd==R(9522,15625)
assert abstract_odd-(1-R(4,5)**4)==R(297,15625)
assert R(3200,3969)-(1-R(2,3)**4)==R(5,1323)
record('abstract_noncausal_obstruction_identities',
       gd_full_norm_identity=True, gd_excess='297/15625',
       supplied_vector_excess='5/1323', legal_hamiltonian_counterexample=False)


# 8. The simulator's two nested splitting operations preserve action exactly.
theta,m,n=s.symbols('theta m n',positive=True)
assert s.simplify(n*m*(theta/(2*m*n)+theta/(2*m*n))-theta)==0
record('exact_nested_lie_trotter_action_accounting',
       total_action='theta', rotation_count='2*m*n')


result={
    'purpose':'finite exact self-authored algebra checks, not proof or exhaustive search',
    'checks':CHECKS,
    'all_passed':all(v['passed'] for v in CHECKS),
    'check_modules':len(CHECKS),
    'arithmetic':'SymPy exact rational complex arithmetic',
    'python_version':platform.python_version(),
    'sympy_version':s.__version__,
    'wall_seconds':perf_counter()-START,
    'acquired_scientific_code_executed':False,
    'source_scientific_code_executed':False,
    'installs':0,'optimizations':0,'random_searches':0,
    'maximum_square_matrix_dimension':256,
    'thinking_tokens':'UNKNOWN; not measured or inferred',
}
(BASE/'EXACT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
