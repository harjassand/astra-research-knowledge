# Task-sensitive stable operator reuse: a constructive certificate and its limits

Work in progress, 31 October 2026. Author construction, not independently
reviewed. No novelty or superiority over equally informed retained numerical
methods is claimed. The acquisition algorithm below is deliberately an
ordinary bidirectional generalized Krylov method; the question is whether a
task-sensitive certificate buys something beyond exact algebra closure and
first-order state-error certification.

## Task, rather than a supplied useful representation

Receive finitely many explicit rational row-stochastic matrices A_a of size n,
and rational column observables b,c. Later queries give a word w of length at
most L and request the scalar correlation

    f(w) = c^T H A_w b,       H = diag(pi).

The task is repeated evaluation of supplied kernel schedules, not optimization
over the best schedule, sampling a hidden physical law, or producing the full
state. The common equilibrium pi is NOT supplied. Acquire the normalized
stationary vector of A_0 by rational linear algebra, require its uniqueness and
strict positivity, and verify pi^T A_a=pi^T for every generator. Check all row
sums and nonnegative entries exactly. Failure is INCONCLUSIVE for this route.
These checks cost input inspection and polynomial rational linear algebra.

For such kernels Jensen's inequality gives

    ||A_a x||_H^2 <= sum_i pi_i sum_j A_a[i,j] x_j^2 = ||x||_H^2.

Thus the acquired metric supplies a common contraction certificate, without
equating stochasticity with Euclidean 2-norm contraction. The weighted adjoint
is A_a^*=H^{-1} A_a^T H and is also a contraction. Reversibility is optional;
when checked, A_a^*=A_a. The cost and conditioning of pi, including small
pi_min, are not omitted from finite arithmetic.

## 1. A second-order uniform observable certificate

Let V be any full-column-rank rational matrix whose span contains b and c.
Define G=V^T H V, P=V G^{-1} V^T H, and Q=I-P. These are analysis matrices;
the learned representation stores B_a=G^{-1} V^T H A_a V. Let b=Vu,c=Vv.
Return the reduced scalar v^T G B_w u.

Suppose finite certificates establish

    ||Q A_a P||_H <= e_in,
    ||P A_a Q||_H <= e_out,
    ||Q A_a Q||_H <= alpha <= 1

for every generator. Then every word of length l has

    |f(w)-f_reduced(w)|
      <= ||b||_H ||c||_H e_in e_out S_l(alpha),
    S_l(alpha) = sum_(j=0)^(l-2) (l-1-j) alpha^j.

The empty sum is zero. For alpha<1,

    S_l(alpha) <= (l-1)/(1-alpha),

and always S_l(alpha)<=l(l-1)/2. This is a uniform statement about every
supplied word, not an average over training words and not a planning oracle.

**Proof.** Set x_t=A_(a_t)...A_(a_1)b, p_t=Px_t, q_t=Qx_t. Since the FULL
dynamics is contractive, ||p_t||_H<=||b||_H. Starting with q_0=0,

    ||q_t||_H <= alpha ||q_(t-1)||_H + e_in ||b||_H
               <= e_in ||b||_H sum_(j=0)^(t-1) alpha^j.

Let z_t be the compressed trajectory lifted to range(P). The recursion for
d_t=p_t-z_t is

    d_t = P A_(a_t) P d_(t-1) + P A_(a_t) Q q_(t-1).

The P block is contractive. Sum the displayed q bounds and pair with c in
range(P). The result follows. In particular there is no exponential
comparison-matrix growth: replacing the norm of the full state by a loose
positive two-sector envelope would unnecessarily lose contractivity. QED.

The two leakage factors express leaving and returning to the observable
subspace. This is closely related to established projection/memory-kernel
arguments, not a claim to invent Mori--Zwanzig reduction.

### Tightness of the length/gap dependence

For 0<g<1 and small e, the symmetric contraction

    A = [[1-e^2/g, e], [e, 1-g]]

has eigenvalues 1 and 1-g-e^2/g, both in [0,1] when e is sufficiently small.
Take P=diag(1,0), b=c=(1,0). The reduction is the scalar 1-e^2/g. Expansion
at e=0 for any fixed l gives an error e^2 S_l(1-g)+O(e^4). Hence the quadratic
coefficient above is sharp at fixed l. For l much larger than g/e^2 the exact
observable can remain order one while the reduced one tends to zero. Small
one-step leakage does not license unlimited reuse at arbitrary horizons.
This illustrative contraction is not itself offered as a row-stochastic
counterexample with a retained stationary vector.

## 2. Certificates are acquired, not optimal-norm oracles

The implementation keeps H-orthogonal rational columns V_j. Their squared
norms G_jj are positive rationals. It explicitly evaluates A_a V_j and
A_a^* V_j. With residuals E_(a,j)=Q A_a V_j and F_(a,j)=Q A_a^* V_j,

    e_in^2 <= max_a sum_j ||E_(a,j)||_H^2/G_jj,
    e_out^2 <= max_a sum_j ||F_(a,j)||_H^2/G_jj.

These are Frobenius upper bounds in orthonormalized coordinates, not estimates
from random directions. All quantities on the right are exactly rational.
The rational number k=(e_in_bound_squared+e_out_bound_squared)/2 bounds
e_in e_out by arithmetic-geometric mean. The program checks

    k^2 S_L(alpha)^2 (b^T H b)(c^T H c) <= requested_error^2.

No square-root accuracy is hidden in this final test. A tighter optional
rational PSD certificate on e^2 G-E^T H E is possible, but is not treated as
free or silently substituted for the executable Frobenius bound.

The program includes the constant observable 1 in V. It acquires a conservative
complement gap from the raw kernels:

    d = min_(a,i,j) A_a[i,j]/pi_j.

One has 0<=d<=1. If d<1, R_a=(A_a-d*1*pi^T)/(1-d) is another row-stochastic
kernel with stationary pi. Every Q vector has pi-mean zero, so A_a Q=(1-d)R_a Q.
Consequently ||Q A_a Q||_H<=1-d. At d=1 the complement is zero. At d=0 the
gapless quadratic certificate remains valid. Computing d costs actual entry
inspection; for sparse local kernels it commonly gives zero. Better spectral
or Nyström bounds may be acquired separately, but their verification must be
paid. No good gap is assumed.

## 3. Automatic acquisition and full ledger

Start from the task observables 1,b,c, discarding exact dependencies by rational
H-orthogonalization. Evaluate both actions of every generator on each newly
added basis column, retaining those images. At a failed certificate, choose the
stored forward/adjoint image with the largest normalized residual and append
that residual after exact orthogonalization. Recompute the finite residual
certificate. If all residuals vanish the representation is invariant; otherwise
each expansion increases rank, so at most n columns are acquired. The full
dimension is an honest possible outcome, not evidence of low-dimensional
structure. No preselected good coordinates or useful experimental probes are
input to this procedure.

This is a familiar retained bidirectional/generalized Krylov acquisition, NOT
a new discovery algorithm. It uses at most 2*m*r generator/adjoint vector
products for final rank r when images are retained, plus all exact metric,
orthogonalization, residual checking and unsuccessful expansion work. The
simple prototype can spend more scalar work than an optimized Householder
implementation; its counters and timing do not erase that cost. Rational
numerator/denominator lengths in the representation and complete serialized
rational certificate are reported separately. Intermediate arithmetic bit
costs are NOT fully instrumented; the displayed vector-product count is not
a complete bit-operation estimate. Exact arithmetic and unsuccessful work
are included in measured acquisition time, which is environment-dependent.

After successful acquisition, a new word takes O(l*r^2) rational operations,
plus reading its l symbols and output arithmetic. This is not an O(l*r^2)
BIT bound: exact coefficient/output denominators grow with word length, and
a small but poorly conditioned rational basis can be more expensive than raw
on-demand multiplication. Query-state bit sizes and storage are charged in
the retaining-comparator experiment. The learned matrices and
task coordinates occupy O(m*r^2) scalar entries; construction may retain
O(m*n*r) image entries. New b,c outside the learned span are NOT admitted by
this two-sided certificate. Within-span coordinates still cost acquisition if
they are not supplied as part of the learned task interface.

The mathematical verifier receives the expected horizon and absolute tolerance
as explicit caller inputs, and binds them to the record. A valid certificate
for an easier task cannot be substituted for the requested one. It checks the
mathematical representation and bound, not timing or acquisition-ledger
metadata. The executable accepts zero task observables as an exact-zero case.

An ordinary first-order state comparison on exactly the SAME learned basis
gives error <=||b||_H||c||_H*l*e_in. It can require a much smaller residual
than the scalar certificate. But an equally informed retained Krylov,
randomized-range/Nyström, balanced-truncation, or spectral method may use the
same improved certificate. A win over only the first-order stopping rule is
not a win over those strong methods.

All acquisition, verification and storage costs must be amortized against
actual future query savings. Dense on-demand application, sparse application,
retained prefix products, repeated-word caching, and any recognizable input
structure remain legitimate competitors. No tiny-fixture speed difference is
promoted to a consequential capability.

## 4. Exact closure is a separate, unstable question

Arbitrarily small generic perturbations can make the generated algebra on the
mean-zero subspace full-dimensional even when the above finite-task certificate
stops at small rank. A modular full-rank word witness can certify full rational
algebra generation: if all rational denominators are invertible modulo a prime
and the vectorized word matrices have full modular rank, their rational rank
is full. This is an exact witness, not a floating rank threshold. Conversely a
failure to find such a witness is inconclusive.

The planned fixtures supply only raw rational kernels and localized task
observables to acquisition. Hidden block coordinates used by a generator are
not inputs to a learner or withheld from strong baselines as privileged advice.
Any available raw structure is available to every comparator.

## 5. Prior machinery and unresolved claim

Kiefer--Wachter, *Stability and Complexity of Minimising Probabilistic
Automata* (2014), explicitly develops generalized Arnoldi/Householder
minimization and finite word-error bounds:
https://arxiv.org/abs/1404.6673 . Its numerical-norm hypotheses must be checked;
row-stochasticity alone is not Euclidean 2-norm contraction.

Maehara--Murota already studies error-controlled simultaneous block
diagonalization through the commutant:
https://doi.org/10.1137/090779966 . Exact-algebra discovery is not new here.

Switched-system balanced truncation already treats retained multiple modes,
Gramian acquisition and error estimates:
https://arxiv.org/abs/1302.0221 and https://arxiv.org/abs/1712.02158 .
Randomized range acquisition is strong ordinary machinery:
https://arxiv.org/abs/0909.4061 .

Projection memory terms and their computational acquisition burden are
explicit in the primary Mori--Zwanzig study
https://arxiv.org/abs/1611.06277 . Markov state-reduction error bounds also have
direct primary antecedents: https://arxiv.org/abs/2403.07618 .

The current constructive result is a particular uniformly certified observable
reuse interface with a fully acquired metric and a second-order residual
bound. Whether it yields a genuinely new acquisition/transfer benefit beyond
equally informed existing retained methods is still unresolved. No general
learning limitation follows from a hard adversarial switching language.
