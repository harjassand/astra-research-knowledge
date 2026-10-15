# Independent audit of structured coherent-noise proposal budgets

16 October 2026, Brisbane. Worker `fz_proposal_budget_audit`.

**Verdict:** the exact minimum proposal rate, the coefficient-box minimax value,
and the diagonal-ellipsoid minimax value are correct under the root's stated
orthogonal Pauli assumptions. The memory consequence is a valid **conditional
composition** with the receiving completed-sweep theorem. This audit does not
prove that theorem's inherited LSS/HT, envelope, finite-torus, or homology
premises. It does not establish physical implementation or historical novelty.

The root input is snapshotted in `SOURCE_ROOT_THEOREM.md` and the receiver in
`SOURCE_RECEIVER_THEOREM.md`. `INPUT_RECEIPT.json` records their original paths,
exact SHA-256 hashes, capture time, and the independently checked Git pin
`3dde9ce74d829a93388e64032d27351b36dd2221`. No root code was run or reused.
The proof below was reconstructed directly from the generator and normalized
Choi definition. `exact_cases.py` independently constructs Choi matrices on
matrix units; `EXACT_CASES.json` reports only bounded exact algebra checks.

## 1. Exact theorem, including all zero-floor cases

Let the finite patch have dimension `d=2^n`. Choose nonidentity Hermitian
Pauli strings `P_1,...,P_m` satisfying

`P_i^2=I`, `Tr(P_i)=0`, and `Tr(P_i P_j)/d=delta_ij`.

Commutation among the strings is unnecessary. Their physical supports can be
strictly smaller than the enclosing patch. Let `h_i` be real and `gamma_i>=0`.
Any real scalar identity term in the Hamiltonian can be discarded. Put

`G(A)=-i[sum_i h_i P_i,A]+sum_i gamma_i(P_i A P_i-A)`.

A finite nonnegative proposal decomposition means exactly

`G = integral lambda(da) (Phi_a-Id)`,

where each `Phi_a` is a state-independent CPTP map and `r=integral lambda`
is finite. Finite sums and countably many summable rates are included. There
is no additional uncharged deterministic Hamiltonian during waiting times.
State-dependent jumps, signed rates, and an optimization over different
physical generators are different interfaces.

The exact answer is

```
r_min = sum_i gamma_i + sum_{i:gamma_i>0} h_i^2/gamma_i
        if h_i=0 whenever gamma_i=0;
r_min = +infinity otherwise.
```

If all `h_i=gamma_i=0`, the zero generator has the empty decomposition of
total rate zero. The expression `G=r(Psi-Id)` at `r=0` should be interpreted
this way rather than by division by zero.

### 1.1 Explicit unitary proposal and existence

For every `gamma_i>0`, define

```
lambda_i = gamma_i+h_i^2/gamma_i,
U_i = (h_i I-i gamma_i P_i)/sqrt(h_i^2+gamma_i^2).
```

Hermiticity and `P_i^2=I` give

`(h_i I+i gamma_i P_i)(h_i I-i gamma_i P_i)=(h_i^2+gamma_i^2)I`,

so `U_i` is unitary. For any matrix `A`, direct multiplication gives

```
U_i A U_i^dagger
 = [h_i^2 A+gamma_i^2 P_i A P_i-i h_i gamma_i[P_i,A]]
     /(h_i^2+gamma_i^2).
```

Multiplication by `lambda_i=(h_i^2+gamma_i^2)/gamma_i` and subtraction of
`lambda_i A` gives exactly

`lambda_i(Ad_{U_i}-Id)(A)=-i h_i[P_i,A]+gamma_i(P_i A P_i-A)`.

The support of `U_i` is contained in the support of `P_i`: the identity
summand introduces no new spatial support. If `h_i=0`, `U_i=-iP_i` and the
rate is `gamma_i`. Terms with both coefficients zero can be omitted.
Summing proves existence at the displayed `r_min`. If `r_min>0`, the single
proposal channel is the convex mixture

`Psi = sum_i (lambda_i/r_min) Ad_{U_i}`.

Every larger rate `r` is achievable by adding identity proposals of rate
`r-r_min`. Identity amplitudes inside `U_i` do not permit a subtraction from
the counted rate. The full Poisson event rate is charged to a location-based
fault envelope, even when the channel happens to be close to identity.

### 1.2 Normalized Choi necessity and minimality over every proposal family

Use `|Phi_d>=d^(-1/2)sum_j |j>|j>` and
`|A>=(A tensor I)|Phi_d>`. Then

`<A|B>=Tr(A^dagger B)/d`.

In particular, `|I>,|P_1>,...,|P_m>` are orthonormal. For the convention
`J(F)=(F tensor Id)(|Phi_d><Phi_d|)`, direct application to matrix units yields

```
J(Id)=|I><I|,
J(Ad_P)=|P><P|,
J(-i[H,.])=-i|H><I|+i|I><H|.
```

The last identity follows because left multiplication by `H` acts on the
output ket, and right multiplication acts on its bra. Therefore, in this
orthonormal span and with `Gamma=sum_i gamma_i`,

```
J(r Id+G) = [ r-Gamma       i h^T       ]
            [ -i h         D_gamma     ],
D_gamma=diag(gamma_1,...,gamma_m).
```

The Choi matrix vanishes on the orthogonal complement. There is no omitted
dimension-dependent factor. For positive `gamma_i`, completing the square
in its quadratic form gives

```
(a,z)^dagger J(r Id+G)(a,z)
 = (z-i D_gamma^(-1) h a)^dagger D_gamma
       (z-i D_gamma^(-1) h a)
   +[r-Gamma-h^T D_gamma^(-1)h]|a|^2.
```

Thus it is positive semidefinite exactly at or above the proposed rate.
Equivalently, below the boundary the vector with coordinates
`a=1, z=i D_gamma^(-1)h` has quadratic form `r-r_min<0`.

For singular `D_gamma`, positivity first requires
`h in Ran(D_gamma)`. To see the necessity without invoking an inverse, any
coordinate with `gamma_i=0` has the principal block

`[[r-Gamma, i h_i],[-i h_i,0]]`,

whose determinant is `-h_i^2`. If that coordinate has `h_i=0`, its row and
column vanish and can be deleted. On the remaining coordinates the previous
argument applies. The exact unified formula is

`r_min=Gamma+h^T D_gamma^+ h` subject to `h in Ran(D_gamma)`,

where `+` denotes the Moore-Penrose inverse. Trace annihilation of `G`
ensures that `Id+G/r` is trace preserving whenever `r>0`. In finite dimension
the Choi positivity criterion therefore proves both necessity and sufficiency.

For any finite-total-rate proposal measure, averaging gives the CPTP map

`Psi = r^(-1) integral lambda(da) Phi_a`,

and hence `Psi=Id+G/r`. Convexity and closedness of the finite-dimensional
CPTP set justify the integral and countable-sum cases as limits of convex
averages; all CPTP maps have uniformly bounded norm. The same Choi necessity
therefore rules out every such decomposition with total rate below `r_min`.
Allowing unrestricted supported channels in place of the explicit unitaries
cannot lower this total rate for this fixed generator.

### 1.3 The exact zero-floor rule is not an unrestricted continuity claim

For a fixed nonzero `h_i`, `gamma_i downarrow 0` forces `h_i^2/gamma_i` to
infinity. For a fixed zero `h_i`, a vanishing floor can be deleted. Joint
limits are path dependent even though all the generators below tend to zero:

| `h(t)` | `gamma(t)` | `r_min(t)` | limit |
|---|---|---|---|
| `t` | `t^2` | `1+t^2` | `1` |
| `t^2` | `t^2` | `2t^2` | `0` |
| `t` | `t^4` | `t^4+t^(-2)` | infinity |

The root's phrase “support/range limits” should be replaced by the explicit
range condition. No failure of the positive-floor theorem is involved.

## 2. Robust coefficient-box floor design

The order of quantifiers is: receive bounds `epsilon_i>=0`; choose one fixed
floor vector; then tolerate every fixed real coefficient vector satisfying
`|h_i|<=epsilon_i`. On coordinates with positive uncertainty a zero floor
would violate the range condition, so it cannot give a finite worst rate.

For positive floors, all squared coefficients increase the rate. Consequently

`sup_{|h_i|<=epsilon_i} r_min = sum_i (gamma_i+epsilon_i^2/gamma_i)`.

The supremum is attained at any box vertex on the nonzero coordinates.
For each coordinate the exact identity

`gamma_i+epsilon_i^2/gamma_i-2epsilon_i=(gamma_i-epsilon_i)^2/gamma_i`

proves the lower bound and identifies the unique optimum on positive axes:

`gamma_i=epsilon_i`, with worst rate `2sum_i epsilon_i`.

Coordinates with `epsilon_i=0` can and should have zero floor and be omitted.
If strict positive floors were artificially required on such coordinates,
the same value would be an infimum, not an attained minimum. If every bound
is zero, the optimal rate is zero.

This is exact minimax optimization over diagonal Pauli dephasing floors for
the fixed catalog and the total-rate objective. It is not an optimum over
all noise interventions, correction-generator redesigns, energy costs, or
maximum spatial touching rates.

## 3. Robust diagonal-ellipsoid floor design

For positive axes `b_i` receive

`sum_i h_i^2/b_i^2 <= 1`.

At fixed floors the quadratic term is
`sum_i (b_i^2/gamma_i)(h_i/b_i)^2`. Its exact supremum is
`z=max_i b_i^2/gamma_i`, attained on an axis attaining this maximum. Thus the
worst rate is `sum_i gamma_i+z`.

Put `B=sqrt(sum_i b_i^2)>0`. The inequalities

`gamma_i>=b_i^2/z`, `sum_i gamma_i>=B^2/z`, and
`z+B^2/z-2B=(z-B)^2/z>=0`

give a universal lower bound `2B`. Equality requires and is achieved by

`z=B`, `gamma_i=b_i^2/B`.

Indeed at these floors the rate for every feasible coefficient vector is

`r_min=B[1+sum_i h_i^2/b_i^2] <= 2B`.

Every point on the ellipsoid boundary has rate exactly `2B`; the optimized
floor equalizes all boundary directions. Zero axes are handled by imposing
the corresponding `h_i=0` and deleting the coordinate. If every axis is
zero, the optimal floor and rate are zero. A coordinate-aligned ellipsoid is
the stated input contract; a general rotated ellipsoid would require a new
floor optimization in the chosen Pauli frame.

For a Euclidean coefficient ball of radius `rho`, all `b_i=rho`, so the
optimal rate is `2rho sqrt(m)` and every floor equals `rho/sqrt(m)`. The box
with marginal bounds `rho` instead has rate `2m rho`. Correlation information
cannot be inferred from marginal bounds.

## 4. Catalog size, geometric incidence, and the receiving rate convention

No factor `d` or `d^2` occurs in the exact Choi answer. Tensoring all strings
with spectator identities preserves their normalized inner products and the
minimum rate. The independent one- and two-qubit spectator check confirms
this finite case. The general statement already follows from the proof.

Catalog size remains a real cost. All weight-at-most-`k` nonidentity Pauli
strings on `n` qubits number

`m(n,k)=sum_{w=1}^{min(k,n)} 3^w binomial(n,w)`.

The unrestricted catalog has `4^n-1` strings. A six-qubit cell has 153
weight-at-most-two strings versus 4095 unrestricted nonidentity strings.
Fixed weight alone is not fixed geometric range: a two-body string joining
sites at distance proportional to `L` violates the receiver's support
contract. Uniformly bounded diameter and uniformly bounded incidence must
be stated separately from weight.

For explicit spatial bookkeeping, label strings by `(x,t)`, where every
`P_(x,t)` is supported inside the receiver patch `R_(q,x)`, with fixed `q`.
Charge each physical term once and define

```
lambda_(x,t)=gamma_(x,t)+h_(x,t)^2/gamma_(x,t),
nu_x=sum_t lambda_(x,t),
touch(c)=sum_{x,t: support(P_(x,t)) meets cell c} lambda_(x,t).
```

The receiver's Section 3 and its equation (8) use a **rate per proposal
center**, namely `sup_x nu_x<=nu_q`, and already count the centers whose
bounded support boxes intersect a primitive guard. Applying that convention
requires

```
box:       for every x, 2sum_t epsilon_(x,t) <= nu_q;
ellipsoid: for every x, 2sqrt(sum_t b_(x,t)^2) <= nu_q.
```

All types at an anchor are included in these sums. Faults with another
generator contribution consume additional budget. For a fixed coefficient
vector, the explicit individual clocks realize `nu_x`; alternatively the
whole patch can use one clock at the worst-case rate and an identity-padded
CPTP proposal. The latter makes the location schedule common to all allowed
coefficients. The proof channels need not be experimentally identified.

If a receiving theorem instead stipulates a bound on `touch(c)`, the direct
incidence sum must be used. At box-optimal floors its worst value is

`sup_h touch(c)=2sum_{x,t: c meets support(P_(x,t))} epsilon_(x,t)`.

For a single ellipsoid block at anchor `x`, let `A_(x,c)` be the subset of
its strings touching `c`. At any fixed floors its exact contribution is

`sum_{t in A_(x,c)} gamma_(x,t)+max_{t in A_(x,c)} b_(x,t)^2/gamma_(x,t)`

when the subset is nonempty, and zero otherwise. At globally total-optimal
floors this becomes `B_x+B_(x,c)^2/B_x<=2B_x`, where
`B_(x,c)^2=sum_{t in A_(x,c)}b_(x,t)^2`. Independent ellipsoid blocks add
their separate worst contributions. One should not sum individual axis
maxima within the same correlated block and call the result sharp.

For one patch centered at every geometric cell, a data cell can belong to
at most `(2q+1)^4` of the producer's `q`-patches. Hence a per-center cap `nu`
implies the sufficient touching cap `(2q+1)^4 nu`. There is no extra factor
six from the six face qubits if “touching a cell” is the union of the
proposal events; summing separate face incidences would deliberately
overcount. At `q=1` this patch-incidence bound is 81. More generally the
actual finite catalog incidence is the quantity to count.

The converse conversion is not automatic if an anchor is not contained in
its strings' supports. Either retain the producer's center convention or
reanchor and recompute the range and guard constants. Do not multiply by
the overlap factor a second time after using the producer's center-count
guard. The root's informal “touching each local cell” should be aligned
explicitly with the center-based receiving statement.

Finally, optimizing a block's total rate need not optimize the largest
touching rate. With two disjoint supports and ellipsoid axes `(3,4)`, the
total-optimal floors `(9/5,16/5)` give maximum touching rate `41/5`, whereas
floors `(3,4)` give maximum touching rate `8`. The latter have a larger
worst **total** rate, 11 rather than 10. This does not contradict the root's
minimax proof; it identifies the objective it actually optimizes.

## 5. Conditional transfer to the autonomous-memory certificate

The received hypotheses needed here are:

1. The correction generator has been completed into local CPTP proposal
   channels with fresh state-independent clocks.
2. The prescribed bounded-support fault catalog and its full center-rate
   budget fit the exact geometric receiver threshold.
3. A location-only good event makes the same fixed final decoder correct
   every permitted Pauli history on each good schedule, on the whole code.
4. The inherited envelope, torus replay, and homology proof genuinely provide
   the advertised bound on the probability of the bad event.

Adding the chosen actual Pauli dephasing floors and the scalar-coefficient
Hamiltonian gives the exact generator identity from Section 1 at every
anchor. The required fault channels are therefore ordinary local CPTP
proposals. No first-order approximation, Trotter error, or remainder growing
with time is used. Their exact or uniformly padded clocks fit the receiver
once the budget in Section 4 is imposed.

For completeness, the receiver's coherent-span step has the following
finite-dimensional justification. Fix a good location schedule. Expand each
fault Kraus operator in the Pauli basis of its own support, retaining complex
coefficients. Fix the correction Kraus labels and the final decoder Kraus
label. On an encoded state, a correction projector either annihilates each
Pauli summand or applies its legal syndrome-dependent Pauli correction.
Every surviving summand is consequently one of the histories covered by the
common good event. If `V` is the encoder and `A_r` a recovered composite
Kraus operator, exact correction by the same decoder on the whole code gives

`A_r V=c_r I_logical`.

Here `c_r` is the complex sum of the surviving branch coefficients and
phases. Different histories can interfere. Trace preservation of the
conditional circuit gives `sum_r |c_r|^2=1`; the good-schedule logical
channel is exactly identity, including on an untouched reference system.

Because the schedule law is state independent, averaging over schedules
gives

`Dec exp(TG_total) Enc=(1-p_bad)Id+p_bad B_T`,

where `B_T` is a CPTP channel when `p_bad>0`. Therefore

`||Dec exp(TG_total) Enc-Id||_diamond <= 2p_bad`.

No Kraus-outcome probability is treated as independent of the logical input.
There is no global absolute-Pauli-coefficient loss and no requirement that
the total extensive generator norm times `T` be small. These deductions
verify the algebraic interface of the transfer. They do not verify the
fourth received hypothesis or make its threshold practical.

The modified generator includes both the completed corrector and actual
deliberate dephasing. Equality with the original uncompleted generator on
cross-syndrome coherences has not been asserted or established. Likewise the
minimum rate for the isolated structured perturbation is not a lower bound
on every possible joint decomposition or redesign of the full baseline.

## 6. Explicit boundaries and singular countermodels

### 6.1 Repeated or signed Pauli directions

Canonical nonidentity Pauli strings are orthogonal. Merely calling signed
strings “distinct” is insufficient: `P` and `-P` represent the same direction.
For `P_1=P_2=Z`, `h=(1,-1)`, and `gamma=(1,1)`, the Hamiltonian cancels and
the true generator is `2(Ad_Z-Id)`, with rate 2. Applying the unmerged
coordinate formula would give 4. The same example can use nominally distinct
signed strings `Z,-Z` with `h=(1,1)`.

Thus repeated directions must be merged before calling the formula minimal.
The root explicitly assumes delta-orthogonality and avoids this failure.
Noncommuting orthogonal Paulis cause no problem. Nonorthogonality alone in a
larger class is not automatically a counterexample: some independent
traceless unitary frames admit the same rate after their Gram geometry is
handled. This audit makes no such extension.

### 6.2 A dephasing floor in the wrong direction does not suffice

For pure `H=Z` and no floor, the normalized Choi block of `r Id-i[Z,.]` on
`|I>,|Z>` has determinant `-1` for every finite `r`. No finite proposal rate
exists. For `H=X` with only a `Z` floor, the `|I>,|X>` block still has
determinant `-1`. A floor must supply the Hamiltonian's Choi directions;
the existence of some unrelated Lindblad noise is not enough.

An additional out-of-class check uses amplitude damping. For
`V=|0><1|`, the `|00>,|11>` principal minor of
`J(r Id+D[V])` has determinant `-1/16` for every finite `r`. Thus being a
perfectly valid Lindblad generator does not itself imply a finite
`r(Psi-Id)` representation. This is consistent with the receiver's warnings.

### 6.3 A system-only floor does not absorb a shared-bath Hamiltonian

Take one system qubit and one bath qubit,

`H=Z_system tensor Z_bath`,

with only the floor `gamma(Ad_{Z_system tensor I_bath}-Id)`. In the normalized
joint Choi space, the Hamiltonian direction `|Z tensor Z>` is orthogonal to
the floor direction `|Z tensor I>`. The `|I tensor I>,|Z tensor Z>` principal
block of `J(r Id+G)` has determinant `-1`, for all finite `r` and any floor
strength. The scalar-coefficient formula cannot absorb this interaction.

For a maximally mixed initially uncorrelated bath the reduced coherence is
proportional to `exp(-2gamma t) cos(2t)`, showing why replacing the bath by
an unknown fixed scalar is not justified. Reduced dynamics can have memory
and coherence revival. A separate theorem for already-Poisson joint
system-bath proposal channels does not supply this missing continuous
Hamiltonian-to-proposal step. The root correctly excludes it.

### 6.4 Operator norm and coefficient norms

With `H=(3X+4Z)/5`, `H^2=I`, so `||H||_op=1`, while `sum_i |h_i|=7/5`.
The pointwise best diagonal-floor rate is `14/5`; silently replacing it by
`2||H||_op=2` would be false for this floor family.

There is a valid explicit conversion for an acquired orthogonal catalog:

`sum_i h_i^2=Tr(H_0^2)/d <= ||H_0||_op^2`,

where `H_0` is the traceless part. In particular, a supplied bound on the
traceless `||H||_op` by `eta` gives a coefficient ball of radius `eta`, and
the ellipsoid construction gives sufficient rate `2eta sqrt(m)`. Also
`sum_i |h_i|<=sqrt(m)||H_0||_op`. If the supplied bound is instead on an
unshifted `H`, `Tr(H_0^2)/d=Tr(H^2)/d-(Tr(H)/d)^2<=||H||_op^2` still gives
the same coefficient-ball bound directly. For an unrestricted `n`-qubit
Hamiltonian, `m=4^n-1`, so this conversion is exponential. It cannot be
presented as dimension-free tolerance for arbitrary dense patch drift.

## 7. Physical and priority scope

The normalized Choi argument removes an unnecessary enclosing-dimension
factor for the stated sparse scalar Pauli interface. It does not remove
catalog size, geometry, acquisition of a trustworthy coefficient expansion,
implementation of the deliberate floor and correctors, or preparation,
reset, energy, calibration, and readout costs. Unknown `U_i` are legitimate
proof channels because their existence represents the already specified
generator; that statement alone is not a device construction or benchmark.

The displaced-jump identity is known gauge machinery. The primary paper
[Shang and França, *Hamiltonian dynamics from pure dissipation*, arXiv
2604.18533v1, equation (4)](https://arxiv.org/html/2604.18533v1)
was checked live: it explicitly expands the dissipator for `F=I-i delta H`
into a Hamiltonian commutator plus its quadratic dissipative term. The
Pauli specialization and its scalar normalization are elementary algebra
of that primitive. This audit does not certify firstness of the exact
minimum-rate statement or minimax budget. The root's stated attribution and
historical `UNKNOWN` boundary are appropriate.

The only requested corrections are precision improvements: exact singular
range language, explicit center-versus-touch incidence, and the distinction
between optimizing total proposal rate and spatial maximum rate. The core
three formulas pass this internal analytic audit. External independent
correctness, the inherited asymptotic memory theorem, historical priority,
and physical usefulness retain their separate evidence requirements.

The parent's subsequent v0002 spatial allocation statement was audited
separately in `SPATIAL_ADDENDUM.md`. Its feasibility test is valid, and a
stronger exact closed form handles arbitrary overlaps for its stated single
global ellipsoid and common scalar spatial cap. This addendum does not change
the original theorem or its physical scope.
