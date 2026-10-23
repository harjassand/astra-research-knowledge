# Independent check: faithful-reference stationary tree reservoir

Date: 2026-10-21. Reviewer: `/root/recurrent_bath_literature`.

**Status update:** This document preserves the first proved route and the intermediate capacity interval. The later colored Dyck code and Kraus-rank converse determine exact capacity; see `EXACT_CAPACITY_CODE_REVIEW.md` and the parent's matching-converse proof. The open-capacity statements below record the earlier checkpoint and are superseded. Their inequalities and construction remain valid.

This is a direct construction check requested by the parent, not a new literature campaign or priority claim. The main constructive proof remains with the parent. The calculation below verifies that replacing the maximally mixed reference by an arbitrary faithful reference is a substantive change: the resulting stationary normal unitary reservoir need not be uniformly approximable by bounded-rank Choi processes, and its unassisted quantum communication rate can be strictly below the full input rate.

## 1. Construction and normalization

Fix an integer `d>=3`. Let `T_d` be the infinite rooted `d`-regular tree: the root has `d` children; every other vertex has one parent and `d-1` children. Write `b=d-1`. The countable vertex set defines the separable Hilbert space

`E = ell²(V(T_d))`.

At each nonroot vertex label its parent edge by port `0` and its children by ports `1,...,d-1`. At the root label its children by ports `0,...,d-1`. Define the unitary on `C^d⊗E` by

`U|a,v> = |a',w>`,

where the edge selected by port `a` at `v` leads to `w` and is labelled `a'` at `w`. Every directed edge is paired with its reverse. Hence this is a bijective permutation of the complete orthonormal basis, `U*=U`, and `U²=I`.

Let `eta=diag(p_0,...,p_(d-1))` with all entries positive and

`p:=p_0>1/2`, `q:=(1-p)/p<1`.

Assign root mass `pi(o)=C`. For each parent-to-child edge with parent port `a`, assign

`pi(child)=pi(parent) p_a/p`.

Root edges permit `a=0`; all other parent-to-child edges have `a>=1`. The reverse port at the child is always `0`. The total mass at depth one is `C/p`, since the root’s outgoing probabilities sum to one. The total mass at depth `k>=1` is

`M_k = (C/p) q^(k-1)`.

Therefore

`sum_v pi(v) = C + C/[p(1-q)] = C [1+1/(2p-1)]`.

The correct normalization is

`C=(2p-1)/(2p)`.

All masses are positive. Thus `tau=diag(pi)` is a faithful normal density on `B(E)`. The equalities remain valid without requiring the nonzero child-port probabilities to be equal.

For the symmetric specialization used by the parent,

`p_a=(1-p)/b` for `a>=1`,

all ratios on deeper edges equal `q/b`. The root’s port-zero child has mass exactly `C`; this finite degeneracy is harmless.

The radius-`L` projector `Q_L` onto all vertices of depths at most `L` has

`r_L = 1+d(b^L-1)/(d-2) = (d b^L-2)/(d-2)`

and omitted mass

`eta_L = sum_(k>L) M_k = q^L/(2p)`.

These identities also hold for `L=0`.

## 2. Exact stationarity for the faithful reference

For an edge `v -> w` with endpoint port labels `a,a'`, the mass definition gives

`pi(v) p_a = pi(w) p_(a')`.

This is true for every orientation, including the root’s port-zero edge. Consequently the diagonal density `eta⊗tau` has the same weight on every basis pair exchanged by `U`. Therefore

`U(eta⊗tau)U* = eta⊗tau`.

The faithful-reference bath channel

`Phi_eta(x)=Tr_S[U(eta⊗x)U*]`

fixes `tau` exactly. The reference input and bath are again in product form after each use. This is stronger than subsequential return under that particular reference input.

The model uses only one fixed global unitary and the normal initial state on the counted bath. No fresh bath cells, hidden discards, time-dependent control, or post-initialization noise are introduced.

## 3. Uniform inputs give a transient walk with an exponential operator-norm bound

Replace the reference input by `I/d` and retain the same `U,tau`. Diagonal bath states remain diagonal. Their probability vectors evolve by the simple random-walk operator

`(Pf)(v)=(1/d) sum_(w~v) f(w)`.

Thus `tau_n=diag(P^n pi)`. The regularity of the graph makes `P` self-adjoint on `ell²(V)`.

A direct weighted Schur bound avoids invoking an unproved probabilistic transience result. Put

`h(v)=b^(-depth(v)/2)`.

At every nonroot vertex,

`(Ph)(v)/h(v) = [sqrt(b)+b/sqrt(b)]/d = 2sqrt(b)/d`.

At the root,

`(Ph)(o)/h(o)=1/sqrt(b) <= 2sqrt(b)/d`,

since `d<=2(d-1)`. For finitely supported complex `f`, the edgewise inequality

`2|f(v)f(w)| <= [h(w)/h(v)]|f(v)|² + [h(v)/h(w)]|f(w)|²`

gives `|<f,Pf>|<=rho ||f||²`, where

`rho=2sqrt(d-1)/d<1`.

Density and self-adjointness yield `||P||_(2->2)<=rho`. Since every probability vector has `ell²` norm at most one,

`||tau_n||_infinity = ||P^n pi||_infinity <= ||P^n pi||_2 <= rho^n`.

In particular, the mass of every fixed finite set tends to zero. No trace-norm subsequence returns to `tau`. This contrasts exact stationarity under `eta` with escape under `I/d`; it does not rely on an entropy calculation.

The bath state has finite entropy in this construction. For arbitrary positive port probabilities, every `-ln pi(v)` grows at most linearly with depth, while the depth law has a geometric tail. Thus infinite initial entropy is not needed for this boundary example.

## 4. Choi-spectrum decay: the fixed purification argument is valid

Purify the initial bath as

`|Psi_tau>_(ER)=sum_v sqrt(pi(v)) |v>_E |v>_R`.

For the `n`-port normalized Choi experiment, supply halves of maximally entangled pairs at the input ports and keep their external references. The entire external-output/reference plus `ER` state is pure. Let `Gamma_n` be its external marginal and `omega_(ER,n)` its complementary marginal. Their nonzero spectra coincide, so

`lambda_max(Gamma_n)=||omega_(ER,n)||_infinity`.

The `E` marginal of `omega_(ER,n)` is exactly `tau_n`, because tracing the external input references replaces each supplied input by `I/d`. The untouched purifying register has the fixed marginal `tau_R=diag(pi)` for every `n`.

This is the **standard maximally mixed-input Choi state**. It is not the weighted process state obtained by purifying `eta`. Stationarity of the latter experiment does not provide the coding upper bound below.

Let `Q` be a rank-`r` projection on `R`, set `P_Q=I_E⊗Q`, and let

`epsilon=Tr[(I_R-Q)tau_R]`.

Write the compressed positive operator `A=P_Q omega P_Q` in an orthonormal basis of `Q`. Its diagonal blocks satisfy

`sum_(i=1)^r A_ii <= tau_n`.

For `x=sum_i x_i⊗|i>`, positivity gives

`<x,Ax> <= (sum_i sqrt(<x_i,A_ii x_i>))²`

`<= r sum_i <x_i,A_ii x_i> <= r ||tau_n||_infinity ||x||²`.

Hence

`||A||_infinity <= r ||tau_n||_infinity`.

The complementary block `C=(I-P_Q)omega(I-P_Q)` has trace `epsilon`, so `||C||_infinity<=epsilon`.

For every positive block operator `omega`, its off-diagonal block obeys the quadratic-form Cauchy–Schwarz inequality. It follows that

`||omega||_infinity <= ||A||_infinity+||C||_infinity`.

Indeed, decompose any unit vector as `x+y` in the two projection ranges; its quadratic form is at most

`(sqrt(||A||)||x|| + sqrt(||C||)||y||)² <= ||A||+||C||`.

Therefore the useful bound is

`lambda_max(Gamma_n) <= r ||tau_n||_infinity + epsilon`.

The parent’s proposed gentle-projection argument is also valid, giving a weaker tail term. The positive-block bound above is direct and sufficient.

Taking any fixed finite-rank purifier cutoff and then `n->infinity`, followed by cutoff error `epsilon->0`, proves

`lambda_max(Gamma_n)->0`.

For any density `sigma_n` of rank at most `k`, with support projection `F_n`,

`(1/2)||Gamma_n-sigma_n||_1 >= 1-Tr(F_n Gamma_n)`

`>= 1-k lambda_max(Gamma_n) -> 1`.

This permits the rank-`k` comparison state and its support to change with `n`. Thus the example rules out uniform approximation by bounded-rank normalized Choi states, and therefore rules out the earlier fixed-finite-environment unitary approximation conclusion. It is not merely a failure of the previous proof strategy.

## 5. Exponential rate and constants

Use `Q=Q_L` on the purifier, and put

`A=d/(d-2)`, `s=-ln rho>0`, `beta=ln b>0`, `t=-ln q>0`.

The preceding exact rank and tail formulas give

`lambda_max(Gamma_n) <= A b^L rho^n + q^L/(2p)`.

Choose

`alpha=s/(beta+t)`, `L_n=floor(alpha n)`, `c=s t/(beta+t)>0`.

For the first term, `b^(L_n)<=exp(beta alpha n)`, hence

`A b^(L_n)rho^n <= A exp(-c n)`.

For the second term, `L_n>alpha n-1`, hence

`q^(L_n)/(2p) <= [1/(2p q)] exp(-c n)`

`= [1/(2(1-p))] exp(-c n)`.

Thus the parent’s constant and exponent are correct:

`lambda_max(Gamma_n) <= C0 exp(-c n)`,

`C0=d/(d-2)+1/[2(1-p)]`,

`c=[-ln(2sqrt(d-1)/d)] [-ln((1-p)/p)] / [ln(d-1)-ln((1-p)/p)]`.

The estimate may be capped at one for small `n`. No uniform lower bound on `c` is asserted as `p` approaches the endpoint `1/2`.

More generally, distance from every rank-`k_n` state tends to its maximal value whenever `k_n exp(-c n)->0`.

## 6. Consequence for unassisted quantum capacity

The parent and rank reviewer independently checked the following elementary coding inequality. I reproduce the derivation to keep this review self-contained.

Let `N` be a channel on a `D`-dimensional input and output space, with normalized Choi state `Gamma`. Let an arbitrary CPTP encoder `E:C^K->C^D` have Kraus operators `E_a`, and an arbitrary CPTP decoder `R:C^D->C^K` have Kraus operators `R_b`. Write channel Kraus operators as `A_j`. Entanglement fidelity on a maximally entangled `K`-dimensional state is

`f=(1/K²) sum_(a,b,j) |Tr(R_b A_j E_a)|²`.

With column-vectorization and cyclicity of trace, define

`X=sum_(a,b) |(E_a R_b)*>><<(E_a R_b)*|`.

Then

`f=(D/K²) Tr(Gamma X)`.

The transpose/conjugation convention for vectorization can equivalently be fixed by the identity `<<B|A>>=Tr(B* A)`; the displayed choice makes `<< (E_aR_b)* | A_j >>=Tr(E_aR_b A_j)`.

Trace preservation of both encoder and decoder gives

`Tr X = sum_(a,b) Tr(R_b* E_a* E_a R_b)`

`=sum_b Tr(R_b* R_b)=D`.

Therefore

`f <= lambda_max(Gamma) (D/K)²`.

This argument does not assume that the encoder is an isometry, that noise is independent across uses, or that the decoder sees the reservoir. Apply it to the tree block channel with `D=d^n`:

`f_n <= C0 exp[-c n + 2n ln d -2 ln K_n]`.

If `liminf_n (ln K_n)/n > ln d-c/2`, entanglement fidelity tends to zero exponentially. In particular, for ordinary block coding without feedback or prior shared entanglement,

`Q_unassisted <= ln d-c/2 < ln d`  (nats per use),

or

`Q_unassisted <= log_2 d-c/(2 ln 2)`  (qubits per use).

This is a strong-converse upper bound above the displayed threshold, not an exact capacity formula. Exact capacity, achievable lower bounds, feedback-assisted capacity, and entanglement-assisted capacity are not determined here. In particular, no conclusion about adaptive feedback protocols follows merely by inserting them into this block-encoder/decoder calculation.

## 7. Exact two-use achievable code

The parent subsequently supplied an elementary matching lower-bound mechanism, independently verified here. Let the logical input be any state on

`C_child=span{|1>,...,|d-1>}`.

Feed that state at the first port and the fixed state `|0>` at the second. For every vertex `v` and every `a>=1`, port `a` leads to a child `w_a(v)`, whose return port is `0`. The two successive interactions therefore act as

`|a>_(S1)|0>_(S2)|v>_E`

`-> |0>_(B1)|0>_(S2)|w_a(v)>_E`

`-> |0>_(B1)|a>_(B2)|v>_E`.

The first outgoing register is fixed, the second contains the logical input exactly, and the bath returns exactly to its initial state. Linearity proves this identity for arbitrary superpositions of `a,v`, including all initial bath coherences, purifications, and external entanglement of the logical data. The root is covered because its ports `1,...,d-1` are children too.

Repeating the pair supplies an exact quantum code of dimension `(d-1)^m` in `2m` calls, with rate

`(1/2)ln(d-1)` nats per use, or `(1/2)log_2(d-1)` qubits per use.

The encoder only inserts a fixed zero between logical symbols; the decoder keeps the even outgoing ports. Neither operation requires access to the bath or knowledge of its initial vertex. This gives the rigorous interval

`(1/2)ln(d-1) <= Q_unassisted <= ln d-c/2`.

Return occurs after each complete pair, not necessarily after its first call. The exact channel identity, rather than a marginal-state comparison, establishes correctness on entangled logical messages.

## 8. Verdict and continuation boundary

The following claims are verified by the displayed proofs:

- The fixed tree-edge permutation is a valid normal unitary device on finite ports and a separable counted bath.
- A faithful product reference `eta⊗tau` is exactly stationary.
- The maximally mixed reference produces exponentially spreading bath probability.
- The normalized Choi largest eigenvalue decays exponentially.
- Uniform approximation by fixed-rank Choi states fails maximally.
- The unassisted quantum rate is bounded strictly below `ln d` despite faithful-reference stationarity.
- An explicit two-use code achieves `(1/2)ln(d-1)` nats per call with zero error and exact bath restoration after every pair.

Accordingly, the proposed continuation “does arbitrary faithful-reference recurrence still imply full unassisted capacity?” is already closed negatively by this construction and coding bound. A precise different operation is whether collective quantum codes can exceed the explicit pair rate while retaining the same fixed device and initialization. The interval above makes that a meaningful capacity question, distinct from improving a bound’s constants. No exact-capacity, assisted-capacity, or historical-novelty conclusion is supplied here.
