# Exact failure of standard streaming Schur compression at the acquisition scale

## Result and scope

Let a block contain `b` consecutive outgoing carriers, and write

\[
x=\sin^2\theta,\qquad r=1-x^2,\qquad
B_b=1-r^b,\qquad
g_b=\frac{b(b-1)}2(1-x)^{2b-2}x^2.
\]

Consider the physical streaming Schur instrument which successively couples
the current spin to the next qubit using real Clebsch–Gordan coefficients,
measures the resulting spin, records the entire spin path classically, and
retains the final spin register. It uses at most logarithmically many qubits
while processing one block. Give the receiver every classical path label and
every final spin register from every block, with unrestricted later decoding.

**Exact bound.** Each independent block compression loses at least `g_b q`
of the source-traceless balanced-Petz quantity, where `q` is its value before
that block. This holds for every finite `b >= 2`, every allowed angle, and
arbitrary old quantum coefficient operators, including nonzero cross Gram
entries. Consequently, after `K` independently compressed blocks,

\[
a_K\le
\frac{B_b}{B_b+g_b}
\left[1-(r^b-g_b)^K\right]
\le \frac{B_b}{B_b+g_b}.
\tag{1}
\]

The upper bound in (1) has the uniform joint asymptotic

\[
\frac{B_b}{B_b+g_b}
=\frac{2}{b+1}\bigl[1+O(b\sin^2\theta)\bigr]
\quad\text{when }b\sin^2\theta\longrightarrow0.
\tag{2}
\]

Thus choosing blocks that grow while satisfying `b theta^2 -> 0` makes this
particular compression progressively worse for recovery. It does not produce
per-block loss `o(b theta^4)`: its exact unavoidable loss is asymptotically
`b(b-1) theta^4 / 2` per unit residual signal. Applying the accepted decoder
inequality to (1) gives

\[
\epsilon\ge\frac34\left(1-\sqrt{a_K}\right).
\tag{3}
\]

This is a restricted obstruction to the specified Schur instrument and to
discarding the Schur multiplicity altogether. It does **not** rule out a
different instrument that coherently retains appropriate multiplicity and
inter-irrep information. In particular, it does not contradict the separate
three-carrier rank-two/rank-six instrument constructed by the algebra agent.

## What the two cited theorems supply

Kuperberg's Theorem 1 gives convergence of the spectral distribution of each
fixed self-adjoint noncommutative polynomial of normalized i.i.d. sums, under
a tracial state, to its classical Gaussian counterpart. Its conclusion is
distributional; it does not supply a physical compression or a
reference-preserving channel estimate.

Source: Greg Kuperberg, *A tracial quantum central limit theorem*,
[arXiv:math-ph/0202035](https://arxiv.org/abs/math-ph/0202035),
[Theorem 1 in the full text](https://arxiv.org/html/math-ph/0202035v1).

Cervero-Martín and Mančinska's Algorithm 1 performs the successive
Clebsch–Gordan transform and spin-label measurement. Their theorem establishes
the weak-Schur label distribution. For qubits they give logarithmic quantum
memory and an `O(b^3 log(b/eta))` Clifford+T gate bound at their specified
accuracy. Their task is weak Schur sampling. We analyze the strongest natural
retained output of that algorithm—its spin register together with all path
labels—for the different task of quantum recovery.

Source: Enrique Cervero-Martín and Laura Mančinska, *Weak Schur sampling with
logarithmic quantum memory*,
[arXiv:2309.11947](https://arxiv.org/abs/2309.11947),
[Algorithm 1 and its correctness theorem](https://arxiv.org/html/2309.11947v1).

## 1. The exact physical instrument and its tracial contraction

Use the standard real coupled-spin basis. A complete path `alpha` specifies
the spin after each of the first `1,...,b` qubits. Let

\[
V_\alpha:\mathbb C^{2j_\alpha+1}
\longrightarrow (\mathbb C^2)^{\otimes b},\qquad
P_\alpha=V_\alpha V_\alpha^\dagger.
\]

The `V_alpha` are mutually orthogonal isometries and `sum P_alpha=I`.
The channel retaining the path and final spin is

\[
\mathcal C_b(X)=\bigoplus_\alpha V_\alpha^\dagger X V_\alpha.
\tag{4}
\]

Equation (4) is CPTP. It is executable causally by the successive measured
Clebsch–Gordan steps. Later collisions on the source and unreceived carriers
commute with operations on received carriers, so describing (4) as a block
channel does not require access to the source or a return of any carrier.

At the tracial block input `tau_b=I/2^b`, its output is
`direct_sum_alpha I_(2j_alpha+1)/2^b`. Its tracial Petz-back composition is the
Hilbert–Schmidt orthogonal projection

\[
\mathcal E_b(X)=\sum_\alpha P_\alpha X P_\alpha.
\tag{5}
\]

Thus the balanced norm retained by (4) is exactly the norm of (5). The
different classical branch probabilities introduce no missing normalization:
each embedded output block has the same eigenvalue `2^{-b}` in the output
reference state. The same statement holds with an arbitrary old memory
reference `sigma_M` tensored onto the block, after balancing that old memory.

If only the spin label and spin register are retained and multiplicity is
traced out, the Petz-back composition is instead the permutation twirl. The
argument below also applies to that weaker channel.

## 2. The ordered-area vector is exactly erased

Set

\[
J_a=\sum_{i=1}^b\sigma_i^a,\qquad
Y_a=\sum_{1\le i<j\le b}
 (\boldsymbol\sigma_i\times\boldsymbol\sigma_j)_a.
\tag{6}
\]

The `Y_a` form a Hermitian vector under simultaneous rotations. Let
`Theta_b=(i sigma_y)^{tensor b} K` be physical spin time reversal. Every
single-spin Pauli is odd under `Theta_b`, so `J_a` is odd and `Y_a` is even.
Each standard path projector is a joint spectral projector of prefix total
spin squares and is invariant under `Theta_b`.

Inside one irreducible spin-`j` copy, every Hermitian vector operator is a real
multiple of the spin generator; for `j=0` it vanishes. Hence

\[
P_\alpha Y_a P_\alpha=\kappa_\alpha P_\alpha J_aP_\alpha
\]

for a real scalar `kappa_alpha`. Time reversal leaves the left side unchanged
and negates the right side. Therefore `kappa_alpha=0`, proving

\[
\boxed{\mathcal E_b(Y_a)=0.}
\tag{7}
\]

This proves erasure even when **all classical path information is retained**.
For the permutation-twirl version there is also a shorter argument: reversing
the carrier order leaves every collective `J_a` fixed and sends `Y_a` to
`-Y_a`, so the twirl annihilates it. In fact `Y_a` is tracially orthogonal to
every polynomial in the collective `J` by the same reversal argument.

## 3. Isolating the weight-two source signal without a remainder

For a source Pauli, one collision acts exactly as

\[
\sigma_S^a I_E\longmapsto
c^2\sigma_S^a I_E+s^2I_S\sigma_E^a
-cs(\boldsymbol\sigma_S\times\boldsymbol\sigma_E)_a,
\qquad c=\cos\theta,\quad s=\sin\theta.
\tag{8}
\]

Once the second term in (8) occurs, the source is identity, and all subsequent
source collisions leave that source-identity term unchanged. Consequently a
final source-traceless term with bath Pauli weight exactly two must take the
cross-product branch at exactly two positions `i<j`, and the `c^2` branch at
every other position. Its coefficient is exactly `c^{2b-2}s^2`, independent of
the chosen pair. Its operator for initial component `a` is

\[
T_{ij,a}=\sigma_j^a
 (\boldsymbol\sigma_S\cdot\boldsymbol\sigma_i)
-\sigma_S^a(\boldsymbol\sigma_i\cdot\boldsymbol\sigma_j).
\tag{9}
\]

Let `R` reverse the order of the bath sites and put `T_a=sum_(i<j) T_(ij,a)`.
Its reversal-odd part is exactly

\[
\frac{T_a-RT_aR^\dagger}{2}
=-\frac12 Z_a,\qquad
Z_a=(\boldsymbol\sigma_S\times\mathbf Y)_a.
\tag{10}
\]

The reversal-even part of `T_a` is orthogonal to every `Z_d` under the
normalized tracial Hilbert–Schmidt inner product: reversal is a unitary
involution on that operator Hilbert space. Terms of every other bath Pauli
weight are orthogonal to every `Z_d` because Pauli strings of different
supports are orthogonal. Source-identity terms are also orthogonal to `Z_d`.
Thus no symmetric weight-two term, higher-order term, or source-identity term
can cancel the coefficient isolated in (10).

Direct Pauli-string orthogonality gives

\[
\langle Y_a,Y_d\rangle_{\tau_b}=b(b-1)\delta_{ad},
\qquad
\langle Z_a,Z_d\rangle_{\tau_S\otimes\tau_b}
=2b(b-1)\delta_{ad}.
\tag{11}
\]

Writing `A_a` for the full evolved initial source Pauli, equations (8)–(11)
give the exact projection of its source-traceless part onto the span of the
three `Z` operators:

\[
\Pi_Z(A_a^Q)=-\frac12c^{2b-2}s^2 Z_a.
\tag{12}
\]

There is no Taylor expansion or `O_b(theta^k)` term in (12).

## 4. Arbitrary old coefficient Gram matrix

After balancing an arbitrary old memory reference, write any one logical
source-traceless signal as

\[
X_Q=\sum_{a=1}^3\sigma_S^a\otimes B_a.
\tag{13}
\]

The coefficient operators `B_a` may be noncommuting, linearly dependent, and
nonorthogonal. Let `G_ad=<B_a,B_d>` be their arbitrary positive Gram matrix.
The input squared norm is `sum_a G_aa`. Fresh carriers are tracial and
independent of this old memory. Equation (12) therefore gives

\[
\Pi_Z(X_{Q,\mathrm{after\ collisions}})
=-\frac12c^{2b-2}s^2\sum_a Z_a\otimes B_a.
\tag{14}
\]

Its squared norm, using (11), is

\[
\frac14c^{4b-4}s^4
\sum_{a,d}\langle Z_a,Z_d\rangle G_{ad}
=\frac{b(b-1)}2c^{4b-4}s^4\sum_aG_{aa}.
\tag{15}
\]

The cross Gram entries disappear because the `Z_a` are mutually orthogonal;
no independence assumption about the `B_a` has been made.

By (7), all `Z_a` lie in the kernel of the self-adjoint projection
`id_S tensor E_b`. The loss of squared norm is consequently at least (15).
Averaging over the three logical Pauli components gives exactly

\[
\ell_Q^{(\mathrm{block})}\ge g_b q.
\tag{16}
\]

Classical old histories are direct sums with positive weights, so the same
inequality holds after summing them. A source-identity old coefficient has
fresh bath identity throughout; it has zero projection onto (14). Independent
ancillas and later CPTP processing cannot recover a component already erased
by (4). The restriction is that the specified block instrument acts on the
fresh block; a coherent old-memory-assisted replacement is a different
operation and is not excluded by this theorem.

## 5. Repeating blocks and the uniform joint limit

Before block compression, `b` exact collisions acquire `B_b q` and leave
`r^b q`. Compression can only reduce the accessible norm, and (16) reduces
the residual norm by at least `g_b q`. Thus

\[
a_{k+1}\le a_k+B_b q_k,\qquad
q_{k+1}\le(r^b-g_b)q_k.
\tag{17}
\]

Start with `a_0=0,q_0=1` and sum the geometric series to obtain (1).
The factor `r^b-g_b` is nonnegative: the full bath-weight-two Q norm is
`4g_b`, which is part of the total Q norm `r^b`.

Uniformity in growing `b` follows from elementary finite inequalities. Put

\[
A_b=\frac{1-(1-x^2)^b}{b x^2}
=\frac1b\sum_{k=0}^{b-1}(1-x^2)^k.
\]

Then `(1-x^2)^{b-1} <= A_b <= 1`, giving the exact bounds

\[
\frac{b-1}{2}(1-x)^{2b-2}
\le \frac{g_b}{B_b}
\le \frac{b-1}{2}
\left(\frac{1-x}{1+x}\right)^{b-1}
\le\frac{b-1}{2}.
\tag{18}
\]

Therefore

\[
\frac{2}{b+1}
\le\frac{B_b}{B_b+g_b}
\le\frac{2}{2+(b-1)(1-x)^{2b-2}}.
\tag{19}
\]

Bernoulli's inequality bounds the difference between the denominators in
(19) by `2(b-1)^2 x`. In particular, for `2(b-1)x <= 1/2`, the ratio of the
rightmost bound in (19) to `2/(b+1)` is at most `1+4(b-1)x`. This establishes
(2) with an absolute constant, uniformly in `b`; no fixed-block remainder has
been extrapolated. For fixed `b`, the ratio tends to `2/(b+1)`. For growing
`b` with `b theta^2 -> 0`, it is asymptotic to `2/(b+1)` and tends to zero.

## 6. Accuracy required of a genuinely different block transducer

The collective central-limit variables do not include the missing vector:

\[
\|Y_a/b\|_{2,\tau_b}^2=(b-1)/b\longrightarrow1,
\]

while `Y_a` is orthogonal to the entire collective-`J` algebra. Its normalized
size does not vanish. An operation claiming `o(b theta^4)` block loss must
preserve the weighted ordered-area signal as well as the leading collective
spin, with a quantitative channel or balanced-norm estimate at that scale.
Distributional convergence of the collective variables does not give this.

There is another exact bookkeeping constraint. From (8), the bath-weight-`k`
part of the Q signal of one initial source Pauli has squared norm

\[
q_{b,k}=\binom bk c^{4b-2k}2^k s^{2k},\qquad
\sum_{k=0}^bq_{b,k}=r^b.
\tag{20}
\]

For `b x -> 0`, the weight-three mass is asymptotic to
`8 binom(b,3) x^3`, whereas the block's acquisition is asymptotic to `b x^2`.
For growing `b`, their ratio is of order `b^2 x`. Thus a purely formal
discarding of every weight above two is not justified by `b theta^2 << 1`;
even that truncation would require the stronger `b theta -> 0` at the desired
accuracy. Operator weight is not a state-support subspace, so truncation is
not itself a CPTP compression. A physical map preserving suitable lower
operators might also preserve some higher ones; (20) is an accuracy check,
not a general lower bound against such a map.

The missing constructive step is a causal physical instrument that keeps the
necessary `J`, `Y`, and higher ordered information with total ledger loss at
the recovery scale while releasing quantum carriers. No such instrument or
matching unrestricted memory lower bound is established here. The independent
algebra hierarchy retains additional quantum multiplicity information and is
a distinct candidate for that step.

## 7. Paid implementation costs and verification

Even the failed Schur primitive has nontrivial processing cost. Keeping its
compressed block outputs consumes up to `K ceil(log2(b+1))` qubits, in
addition to the active block workspace and compilation ancillas. Applying the
cited gate bound block by block gives `O(N b^2 log(b/eta))` gates for `N=Kb`.
Classical path storage is allowed but does not replace this quantum storage.
The cited sampling-accuracy statement alone should not be read as a
diamond-norm bound on the retained instrument; such a bound can instead be
enforced by compiling its actual constituent unitaries with a total error
budget. Routing, gates during carrier arrival, any resulting input queue,
protection, and classical-feedback latency must still be paid. None can
repair the ideal information loss (16).

`schur_block_obstruction.py` builds the full real-path instrument for blocks
`b=2,...,6`, at angles `.03,.1,.3,.7`. Its twenty checks verify completeness,
`P_alpha Y_a P_alpha=0`, the exact coefficient (12), the norm and full
weight distribution, and the physical Q-loss lower bound. Maximum Y-block
residual was `1.162e-15`, maximum weight-distribution residual was
`4.164e-16`, and minimum lower-bound slack was `-2.274e-16` (roundoff).
The results are recorded in `schur_block_checks.json`.

At angle `.03`, the actual repeated-block accessible limits from this physical
instrument were approximately `.66647,.49966,.39955,.33281,.28514` for block
lengths `2,...,6`, consistent with the limiting sequence `2/(b+1)`. These
numbers are verification of a restricted theorem, not an optimization result.
