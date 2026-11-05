# Exact directed continuity identities for the matched-cascade slow generator

The starting fixed-width generator is the independently derived channel
constructor result in `../joint_channel/slow_generator_derivation.md`:

\[
G_n(X)=-\frac1{32}\sum_a[Y_a,[Y_a,X]]+\frac{i}{8}[C_n,X],
\]

on the simultaneous-SU(2) invariant algebra, where
`Y=sum_(i<j) sigma_i cross sigma_j` and
`C=sum_(i<j<k) sigma_i dot (sigma_j cross sigma_k)`.
The adjoint on observables has the **negative** chirality sign.

## 1. Exact causality, before taking any limit

Let `T_(n,theta)` be the actual channel where one tracial carrier collides in
order with sites `1,...,n`. For an observable `X` on the first `ell` sites,

\[
T_{n,\theta}^*(X\otimes I)
=T_{\ell,\theta}^*(X)\otimes I.
\tag{1}
\]

In the Heisenberg circuit every later collision commutes with the input
observable and cancels against its inverse before any earlier collision is
encountered. Taking normalized carrier trace proves (1), with no assumption
on `X`, angle, or bath length.

If `X` is invariant on the prefix, it is also invariant on the whole chain.
Equating the fourth-order coefficients gives

\[
G_n^*(X\otimes I)=G_\ell^*(X)\otimes I.
\tag{2}
\]

Thus the prefix invariant algebras form an invariant flag. A basis adapted
to the flag gives a block-triangular generator, and the spectrum of every
prefix generator is contained in the longer-chain spectrum. This proves
directionality and spectral nesting. It does not determine the new diagonal
blocks, their spectra, or possible Jordan growth.

## 2. An exact local-density continuity law

Write

\[
D_j=\boldsymbol\sigma_j\cdot\boldsymbol\sigma_{j+1},\qquad
J_{[1,j]}=\sum_{i=1}^j\boldsymbol\sigma_i,
\qquad F_j=J_{[1,j]}\cdot\boldsymbol\sigma_{j+1},\quad F_0=0.
\]

Then for every `n>=2` and `1<=j<n`,

\[
\boxed{G_n^*(D_j)=F_{j-1}-F_j.}
\tag{3}
\]

Equivalently,

\[
G_n^*(D_j)=-D_j+
\sum_{i<j}(\boldsymbol\sigma_i\cdot\boldsymbol\sigma_j
-\boldsymbol\sigma_i\cdot\boldsymbol\sigma_{j+1}).
\tag{4}
\]

For the open nearest-neighbor exchange Hamiltonian `H_n=sum_(j=1)^(n-1)D_j`,
the bulk terms telescope:

\[
\boxed{G_n^*(H_n)=-F_{n-1}
=-J_{[1,n-1]}\cdot\boldsymbol\sigma_n.}
\tag{5}
\]

This is a genuine directed continuity identity with an end current. The
current is nonlocal in the upstream spin; it is not a uniformly bounded
local boundary observable.

### Derivation and signs

Let `P_j=SWAP_(j,j+1)=(I+D_j)/2`,
`A= sigma_j cross sigma_(j+1)`, and let `J_L,J_R` denote the total spin
strictly to the left and right of that pair. Adjacent transposition changes
the sign of exactly its own pair in `Y`, giving

\[
P_jY_aP_j=Y_a-2A_a,\qquad [Y_a,P_j]=2A_aP_j.
\]

The triples in `C` containing both adjacent sites give

\[
[C,P_j]=2A\cdot(J_L+J_R)P_j.
\]

Using that `A` is a vector for `sigma_j+sigma_(j+1)`,

\[
\sum_a[Y_a,A_a]=4i A\cdot(J_L-J_R),\qquad
\sum_a A_a^2=8I-4P_j.
\]

Therefore

\[
G_n^*(P_j)=
\left[-\frac{i}{2}A\cdot J_L-\frac18\sum_a A_a^2\right]P_j.
\]

The `J_R` terms cancel exactly between dissipation and the adjoint
Hamiltonian. Finally
`A_aP_j=i(sigma_j^a-sigma_(j+1)^a)` gives

\[
G_n^*(P_j)=I/2-P_j+
\tfrac12J_L\cdot(\boldsymbol\sigma_j-\boldsymbol\sigma_{j+1}),
\]

which proves (3)–(5). Reversing the chirality sign would reverse the causal
direction, so this also independently checks the orientation convention.

## 3. Quantified low-dissipation exchange profiles

There is an exact Yangian boundary commutator:

\[
[Y_a,H_n]=4i(\sigma_1^a-\sigma_n^a).
\tag{6}
\]

With normalized trace, `||H_n||_2^2=3(n-1)` and

\[
-\langle H_n,G_n^*H_n\rangle
=\frac1{32}\sum_a\|[Y_a,H_n]\|_2^2=3.
\tag{7}
\]

Thus the symmetric Dirichlet Rayleigh ratio is `1/(n-1)`.

More generally let `H_w=sum_j w_j D_j`, with real weights and `w_0=w_n=0`.
Pauli orthogonality and telescoping give the exact formulas

\[
\|H_w\|_2^2=3\sum_{j=1}^{n-1}w_j^2,
\]

\[
-\langle H_w,G_n^*H_w\rangle
=\frac32\sum_{i=1}^{n}(w_i-w_{i-1})^2,
\tag{8}
\]

\[
G_n^*H_w=\sum_{j=1}^{n-1}(w_{j+1}-w_j)F_j,
\qquad
\|G_n^*H_w\|_2^2
=3\sum_{j=1}^{n-1}j(w_{j+1}-w_j)^2.
\tag{9}
\]

The currents `F_j` are mutually orthogonal, with squared norms `3j`.
For `w_j=sin(pi j/n)`, the Dirichlet ratio is exactly

\[
2\sin^2\frac{\pi}{2n}=O(n^{-2}),
\tag{10}
\]

and `||G_n^*H_w||_2/||H_w||_2 <= pi/sqrt(n)`.
Since the semigroup is unital and trace preserving, it contracts normalized
Hilbert–Schmidt norm. Integration therefore proves the actual observable
estimate

\[
\frac{\|e^{tG_n^*}H_w-H_w\|_2}{\|H_w\|_2}
\le\frac{\pi t}{\sqrt n}.
\tag{11}
\]

This is a uniform all-width slow-generator statement. It is not yet a
uniform finite-angle statement, since the physical weak-angle limit still
has width-dependent error constants.

## 4. Why this is not yet an extraction construction

Equations (3)–(11) exhibit directed transport and slowly changing invariant
observables. They do not by themselves encode the three source Pauli
operators in a protected noncommutative subsystem, transfer that subsystem
to the receiver, or give a readout diamond bound for an independently prepared
frame. A single low-dissipation Hermitian charge can protect classical
distinguishability without protecting an unknown qubit.

The current in (5) has tracial norm `sqrt(3(n-1))`; it is not suppressed in
that norm relative to the flat exchange sum. Its nonlocal upstream support
also prevents inferring a finite propagation speed from the displayed
continuity equation.

Nor does the pair-observable sector close. Already at `n=4`,
`G_4^*(sigma_1 dot sigma_4)` has a nonzero bath-weight-four component of
normalized squared norm `24`. Thus iterating (3) does not reduce the full
quantum transport problem to a closed nearest-neighbor classical system.
The triangular flag allows nonnormal/Jordan dynamics; spectral nesting alone
does not establish a width-independent mixing rate or an all-width recovery
obstruction.

## 5. Exact algebra verification

`cascade_continuity_check.py` uses Pauli strings and dyadic Gaussian-rational
coefficients, with no dense state simulation or optimization. It checks all
adjacent identities for `n=2,...,6`, the telescoping law, the Yangian boundary
commutator, and all factors in (7). Every identity has exactly zero residual
in this representation. Results are in `cascade_continuity_checks.json`.

The separate audit of `../joint_algebra/chirality_uniform_obstruction.md`
found its `sqrt(K_n/6)` witness factor, parity isolation, even-tail bound,
nonprojective balanced-map bridge, and diffusive-prefix limit consistent.
Its explicit effect hypotheses must remain in the statement: asymmetric
initial frames can give non-invariant prefix effects even when subsequent
operations are covariant.
