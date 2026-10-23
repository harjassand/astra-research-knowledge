# Cycle8 exact finite check contract — frozen before first execution

Scientific target: check NEW finite identities used by the asymmetry-budget
criterion. No earlier scientific suite, stochastic simulation, search, parameter
fit, or asymptotic claim from matrix powers is authorized by this contract.

## Fixed energy fixtures

Five native states. q_i=(i+1)^4/979; pi=(1,1,1,500,5000)/5503.
Low set A={0,1,2} is defined by W<1/5. The remaining states are B.
The two proposal ratios are R=(17/16)^4 and R=(3/2)^4.
On directed edges (0,1),(1,2),(2,0),(0,3),(0,4), forward Q=1/(8R)
and reverse Q=1/8. Actual remaining diagonals complete Q.
The cycle is nonreversible. All edge asymmetries equal log R.

Use eta in {1/2,3/4}, kappa in {0,2 eta}, alpha in {1/2,3/4},
w in {1,2}, every E subset B, theta=1/2, p=2.
There are 128 combinations. The scalar U=wR is rational. All three
relaxed-envelope regimes occur: tau=0; positive-tau interior maximum;
positive-tau endpoint maximum. These are diagnostic proof parameters,
not the much smaller asymptotic theta used for the uniform upper.

Acceptance: exact nonnegativity, row sums and detailed balance for native G,L,C;
reverse-proposal coefficient identity and column bound; actual-diagonal
powered row bound; exact LDL reconstruction with strictly positive pivots
for the local and mixed all-vector quadratic energy slack matrices;
actual killed/absorbed mixture identity; exact equality of absorbed first-hit
mass and independent finite first-hit decomposition for N=1,3,7, followed
by the squared Holder upper bound. For each of the 16 distinct native
kernels, verify the full original-return decomposition at n=8,N=3.
KL admission is max(pi/q)<2, which implies D(pi||q)<log2<1.

## Fixed multilevel native fixtures

Use R=9/4 (noninteger), M=ceil R=3, depth J=2, scale=4,
b=1/64, p=1/16, eta=1/2.
Both expansion with kappa=2 and coalescence with kappa=0 are included.
The same exact q,pi,Q in each orientation is also evaluated with matched
kappa=eta as a control. Use alpha=1/2 and 3/4, giving eight configurations.

Construct all 14 labelled native states and matrices BEFORE lumping.
Per-edge Q, level masses, and individual-state acceptance ratios follow
Section 7 of ASYMMETRY_BUDGET_THEOREM.md. This finite rational target p is
an identity-check fixture; it is not substituted for p_n=1/[log(n)^2(1+V)]
in the asymptotic proof. KL admission is certified by the rational upper
sum_{W>1} pi ceil(log_2 W)<1, using log2<1.

Acceptance: actual public reverse-Q ratios; positive probabilities, row sums
and detailed balance; exact S=1 for mismatched forward edges, and the
computed matched screens 2/3 (coalescence), 8/27 (expansion); actual local
forward/reverse aggregate probabilities and rejection diagonals; strong
lumping from each native row; equality of native and quotient full TV at
horizons 4,8,16; whole-terminal-union escape (distinct from a single leaf's
diagonal); marked-path capture on actual mixture choices, deterministic
window lower bound, and actual full-chain retention; pure-IMH full-return
upper on the SAME native inputs.

Twenty-four native law comparisons and twenty-four capture/ordinary bounds
are required. Any failed assertion must be preserved. It must be classified
as a mathematical defect, a fixture/admission problem, or a code problem
before any narrowly justified repair and rerun.

## Reproduction and scope

Run Python 3 with assertions enabled:
python3 code/exact_checks.py --output-dir evidence/exact

All state, probability, matrix, energy, and law assertions use Fraction
arithmetic. No floating tolerance certifies positivity or normalization.
Wall/CPU resource readings alone are floating values. The deterministic
JSON input/results are replayable. Resource receipts vary between runs.

A PASS checks finite algebra at these fixed inputs. The general theorem
is proved in the principal source and reviewed independently. No rate,
optimal constant, asymptotic floor, historical originality, finite-word
robustness, practical speedup, or research-method superiority is inferred
from this run. No parameter will be tuned for a favorable sampler curve.

