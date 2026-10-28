"""Exact-rational two-sided residual check; no equipment operations."""
from itertools import product, combinations
import json
from pathlib import Path
from fractions import Fraction

Q = Fraction

class Mat:
    def __init__(self, data):
        if not isinstance(data[0], (list, tuple)):
            data = [[x] for x in data]
        self.a = [[Q(x) for x in row] for row in data]
        self.rows, self.cols = len(self.a), len(self.a[0])
    def __getitem__(self, index):
        return self.a[index[0]][index[1]] if isinstance(index, tuple) else self.a[index][0]
    def __eq__(self, other):
        return self.a == other.a
    @property
    def T(self):
        return Mat(list(zip(*self.a)))
    def __add__(self, other):
        return Mat([[x+y for x,y in zip(ar,br)] for ar,br in zip(self.a,other.a)])
    def __sub__(self, other):
        return self + (-1)*other
    def __mul__(self, other):
        if isinstance(other, Mat):
            return Mat([[sum((x*y for x,y in zip(row,col)),Q(0))
                         for col in zip(*other.a)] for row in self.a])
        return Mat([[other*x for x in row] for row in self.a])
    __rmul__ = __mul__
    def __truediv__(self, other):
        return self * (Q(1)/other)
    def extract(self, rows, cols):
        return Mat([[self.a[j][k] for k in cols] for j in rows])
    def det(self):
        if self.rows == 1:
            return self.a[0][0]
        return sum(((-1)**k*self.a[0][k]*self.extract(range(1,self.rows),
                    [j for j in range(self.cols) if j != k]).det()
                    for k in range(self.cols)),Q(0))

def diag(*entries):
    return Mat([[entries[j] if j == k else 0 for k in range(len(entries))]
                for j in range(len(entries))])
P = Mat([[0, 0], [0, 1]])
Qaxis = Mat([[Q(9, 25), Q(12, 25)], [Q(12, 25), Q(16, 25)]])
primitives = [P, Qaxis]
blocks = [Qaxis*P, P*Qaxis]
block_words = [(0, 1), (1, 0)]
b = Mat([0, 1])
dictionary = [(), (0, 1), ()]

def native_state(word):
    x = b
    for i in word:
        x = primitives[i]*x
    return x

def moment(word):
    return (b.T*native_state(word))[0]/2

def acquired(left, middle, right):
    return moment(tuple(right)+tuple(middle)+tuple(left)[::-1])

def psd(a):
    assert a == a.T
    return all(a.extract(subset, subset).det() >= 0
               for size in range(1, a.rows+1)
               for subset in combinations(range(a.rows), size))

V = Mat([[native_state(w)[j] for w in dictionary] for j in range(2)])
G = V.T*V/2
c = Mat([1, 0, 0])
assert G.det() == 0 and G.extract((0,1),(0,1)).det() > 0 and V*c == b
T = [Mat([[Q(1,5),Q(1,40),0],[-Q(1,50),Q(1,4),Q(1,100)],
                [Q(1,100),0,Q(1,6)]]),
     Mat([[Q(1,6),0,Q(1,30)],[Q(1,100),Q(1,5),0],
                [0,-Q(1,40),Q(1,4)]])]
W = diag(1, 2, 3)
Winv = diag(1, Q(1,2), Q(1,3))
U = [Winv*t.T*W for t in T]
rho = Q(1,2)
for t, u in zip(T, U):
    assert psd(rho**2*W-t.T*W*t)
    assert psd(rho**2*W-u.T*W*u)
D, R, S, E, F = [], [], [], [], []
entry_checks = 0
for i, B in enumerate(blocks):
    M = V.T*B*V/2
    Np, Nm = V.T*B.T*B*V/2, V.T*B*B.T*V/2
    bw = block_words[i]
    for j, left in enumerate(dictionary):
        for k, right in enumerate(dictionary):
            assert G[j,k] == acquired(left, (), right)
            assert M[j,k] == acquired(left, bw, right)
            assert Np[j,k] == acquired(left, bw+bw[::-1], right)
            assert Nm[j,k] == acquired(left, bw[::-1]+bw, right)
            entry_checks += 4
    e, f = B*V-V*T[i], B.T*V-V*U[i]
    d = M-G*T[i]
    r = Np-M.T*T[i]-T[i].T*M+T[i].T*G*T[i]
    s = Nm-M*U[i]-U[i].T*M.T+U[i].T*G*U[i]
    assert d == V.T*e/2 and r == e.T*e/2 and s == f.T*f/2
    assert psd(r) and psd(s) and r != s
    assert psd(4*W-r) and psd(4*W-s)
    D.append(d); R.append(r); S.append(s); E.append(e); F.append(f)
word_checks, max_error = 0, Q(0)
for h in range(7):
    for word in product(range(2), repeat=h):
        a = [c]
        for i in word:
            a.append(T[i]*a[-1])
        z = [None]*(h+1)
        z[h] = c
        for t in range(h-1,-1,-1):
            z[t] = U[word[t]]*z[t+1]
        prediction = (c.T*G*a[h])[0]
        for t,i in enumerate(word):
            prediction += (z[t+1].T*D[i]*a[t])[0]
        x = b
        for i in word:
            x = blocks[i]*x
        truth = (b.T*x)[0]/2
        remainder = Q(0)
        for t in range(h):
            for s in range(t+1,h):
                e = E[word[t]]*a[t]
                for k in range(t+1,s):
                    e = blocks[word[k]]*e
                remainder += ((F[word[s]]*z[s+1]).T*e)[0]/2
        assert truth-prediction == remainder
        assert abs(remainder) <= 16
        max_error = max(max_error, abs(remainder))
        word_checks += 1
wrong_a = moment(block_words[0]+block_words[1])
wrong_b = moment(block_words[1]+block_words[0])
assert wrong_a != wrong_b

# Positive coherent residual and weighted trace identities. This verifies the
# algebra under the stronger block-encoding premise, not that premise itself.
native_ops = []
for word in dictionary:
    op = Mat([[1,0],[0,1]])
    for i in word:
        op = primitives[i]*op
    native_ops.append(op)
beta_squared = Q(1,2)
trace_trials = []
for i,B in enumerate(blocks):
    weights = [Q(1),Q(1,2),Q(1,3)]
    weighted_numerator, normalization_sum = Q(0),Q(0)
    for k in range(3):
        x = Mat([1 if j == k else 0 for j in range(3)])
        tx = T[i]*x
        lcu = Mat([[0,0],[0,0]])
        for j in range(3):
            lcu = lcu+x[j]*(B*native_ops[j])-tx[j]*native_ops[j]
        assert lcu*b == E[i]*x
        C = sum((abs(x[j])+abs(tx[j]) for j in range(3)),Q(0))
        residual_sq = (x.T*R[i]*x)[0]
        probability = residual_sq/(beta_squared*C*C)
        assert 0 <= probability <= 1
        normalization = weights[k]*beta_squared*C*C
        weighted_numerator += normalization*probability
        normalization_sum += normalization
    trace = sum((weights[k]*R[i][k,k] for k in range(3)),Q(0))
    assert weighted_numerator == trace
    assert psd(trace*W-R[i])
    trace_trials.append({'normalization':str(normalization_sum),
                         'success_probability':str(trace/normalization_sum),
                         'trace_residual':str(trace)})

# Nearly sharp uniform certificate despite an exact hidden conserved mode.
sharp_rho, sharp_e = Q(1,2), Q(1,1000)
sharp_A = Mat([[sharp_rho,sharp_e],
               [sharp_e,1-sharp_e**2/(1-sharp_rho)]])
sharp_I = diag(1,1)
sharp_fixed = Mat([sharp_e,1-sharp_rho])
assert psd(sharp_A) and psd(sharp_I-sharp_A)
assert sharp_A*sharp_fixed == sharp_fixed
sharp_limit = sharp_e**2/((1-sharp_rho)**2+sharp_e**2)
sharp_bound = sharp_e**2/(1-sharp_rho)**2
report = {
    'arithmetic': 'exact standard-library Fraction', 'dictionary_columns': 3,
    'dictionary_rank': 2, 'acquired_entry_identities_checked': entry_checks,
    'future_words_checked': word_checks, 'maximum_block_length': 6,
    'rho_computational': str(rho), 'uniform_bound_fixture_only': '16',
    'max_actual_signed_remainder': str(max_error),
    'macro_naive_reversal_centered_values': [str(wrong_a),str(wrong_b)],
    'macro_naive_reversal_survival_values': [str(wrong_a+Q(1,2)),str(wrong_b+Q(1,2))],
    'separate_primal_dual_residual_forms_verified': True,
    'conditional_coherent_residual_trace_checks': trace_trials,
    'uniform_bound_sharpness_ratio':str(sharp_limit/sharp_bound),
    'physical_strict_block_norm': '4/5 on centered x,z subspace',
    'cost_advantage_claim': False}
Path(__file__).with_name('adjoint_block_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
