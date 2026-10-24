# Exact block references, canonical number, and charge-conserving observables

24 October 2026. Owned constructive continuation; internal theorem candidate.
This extends the computable weak-bridge regime to strongly resonating finite
reference blocks and closes a marked-observable operation. It remains a
certificate-bearing state evaluator, not a generic sampler, a physical
preparation scheme, a ground-state solver, or a demonstrated material advantage.
The generic KP and stability machinery is established; state-specific acquisition
and the complete canonical/observable interface are the content being checked.

## 1. Input and actual representation acquisition

Supply a symmetric zero-diagonal `F in Q(i)^(n by n)`, `n=2m`, describing the
opposite-spin projected state in CANONICAL_CONTRACTION.md. Read its full entries.
Supply a target pair count `k`, relative norm error, or a bounded Hermitian
operator `O` conserving total particle number and supported on a fixed number
`r` of reference blocks. Matrix elements or a finite fermionic polynomial for
`O`, and a verified norm bound, are inputs. Rescale to `||O||<=1`. All fermionic
ordering signs remain explicit. An even distant hopping/pair-transfer operator
is allowed; its two endpoints are not replaced by independent local averages.

Acquire a finite block partition by an actual search, not an oracle. For each
candidate threshold between the sorted exact squared edge magnitudes, form the
components of edges above threshold. Retain candidates whose component sizes
are at most the fixed block bound `b`, then compute the exact block data below
and verify all bridge/charge tests. There are polynomially many such thresholds.
Alternatively accept any supplied partition and verify it. This is a sound
certificate search for threshold-separated bounded blocks, not a complete or
optimal partition algorithm. Failed candidates give no negative claim about
the physical state. General diagonal `DFD` still requires occupation filters;
it is not used to change the supplied finite-hole state for free.

Write `F=F_internal+E_cross`. The graph of nonzero cross-block couplings has
maximum block degree `D`; maximum physical cross degree is `Delta`; a rational
envelope bounds `|E_e|<=lambda`. Block sizes, degrees, envelopes and entry bit
lengths are verified from the explicit matrix. Let there be `M` blocks.

On each block compute exactly

```
|Omega_B(z)> = P_no-double,B exp(sqrt(z) sum_(ij internal B)
                               F_ij c†_i↑ c†_j↓)|vac>,
B_B(z) = sum_q ||Omega_(B,q)||² z^q.
```

These finite polynomials and sector vectors cost `exp(O(b))` rational-complex
work by explicit determinant or partial-matching enumeration. Their constant
term is one. The hard scalar-charge stability theorem reconstructed in the
previous note applies to EACH native block, so `B_B` has only negative real
roots, with degree `d_B<=floor(|B|/2)`. This is an internally reconstructed
structural premise, not a new externally validated fact or a free counting
oracle for the whole state.

Internal correlations need not be weak. For example a four-site block with
`F_01=F_23=F_02=F_13=1` has two equal-strength valence-bond coverings and

```
B_B(z)=1+8z+4z².
```

At `z=1/2`, its mean pair count is one and its pair-count variance is `1/3`.
Thus identical such strongly resonating blocks have extensive charge variance.
The zero-bridge product and its canonical projection are solved by ordinary
polynomial coefficient DP; this is the equally informed baseline.

## 2. Exact edge operation and the parity gain

On the hard no-double-occupancy space set
`C_e†=P_no-double B_e† P_no-double`, where `B_e†` is the singlet creator on a cross
edge. Its norm is at most two. It squares to zero. Two such projected creators
sharing a site have product zero; disjoint even creators commute. Creation
cannot repair an already doubly occupied site. Consequently the FULL projected
state has the exact representation

```
|psi(z)> = product_(cross edges e) (I+sqrt(z) E_e C_e†)
            tensor_B |Omega_B(z)>.                               (1)
```

For complex fugacity, this notation is used to derive the analytic norm
polynomial (the bra uses the same formal fugacity), not to equate it to a Hilbert
norm at complex `z`. It can instead be expanded coefficient by coefficient with
no square-root branch. For real positive `z` (1) is the ordinary state identity.

In a bra/ket edge expansion, the reference on every block has even fermion
parity. A matrix element with an odd total number of incident cross-edge
creators/annihilators on that block therefore vanishes. A nonzero active block
has at least TWO incidences across the two copies. If the active component has
`s` blocks, its number of selected weak edges counted across both copies is
at least `s`. This gain does not require the INTERNAL block state to be a product
of dimers, nor does it require a block Hamiltonian gap. It uses exact local
parity and the actual reference tensors.

Group selected cross edges into connected block components. Norms factor across
disjoint components with graded fermionic signs retained. Every inactive block
contributes `B_B(z)`. Let `A_C(z)` be the exact unnormalized local component
polynomial. The disjoint gas identity is

```
Z(z)=sum_(disjoint Gamma) product_(C in Gamma) A_C(z)
                            product_(B outside union Gamma) B_B(z). (2)
```

Each `A_C` is computed by finite block/edge expansions on its actual support;
it is signed/complex, not a probability. Compatibility is overlap only. At most
`b Delta s/2` physical cross edges lie inside an `s`-block support; their ordered
bra/ket subsets have at most `2^(b Delta s)` patterns. All local calculation
costs are `exp(O_(b,Delta)(s))` with polynomial bit overhead.

## 3. Uniform sector control independent of internal resonance

For a native block and `|arg z|<=2pi/3`, negative real roots imply

```
|B_B(z)| >= 2^(-d_B) B_B(|z|).                                   (3)
```

For each root factor use `|1+u e^(i theta)|>=(1+u)/2` when `cos theta>=-1/2`,
then multiply. Thus arbitrary internal phases/cancellations do not introduce an
unpriced inner-sector denominator condition number; its conservative bound is
controlled by the finite block charge degree.

Suppose the real tilt will lie in `[r0/2,2r0]`. Use a slightly larger logarithmic
domain of radius `s0=1/8` around `|arg z|<=pi/2`, with `|z|<=R=4r0`. Acquire a
rational upper bound

```
v >= 2 sqrt(R) lambda,   v<=1,
K=2^(d_max+2),
h=K 2^(b Delta) v,             d_max=max_B d_B.                    (4)
```

The square root is bounded by dyadic intervals/squared rational comparisons.
It is not an exact-real oracle; the encoding cost includes `log r0`. Local
Cauchy and the edge norm in (1), the pattern count, and the parity step yield

```
|A_C(z)/product_(B in C) B_B(z)| <= h^|C|.                        (5)
```

In detail, each selected cross-edge factor has norm at most `v`, the reference
norm divided by its analytic block polynomial costs at most `2^d_B` per active
block, and a term has at least `s` edge factors. This avoids counting every
internal matching as a new weak resource. Extra factors in `K` reserve margin
for the marked filter below. On the real-radius circle a component's unnormalized
weight divided by `product B_B(r)` is also at most `h^s`.

For fixed degree/size choose and verify

```
x=4 D 3^5 h <= 1/4,
S=x²/[4D(1-x)],
S <= nu s0/128,
S+(D+1)h 3^d_max <= nu/16.                                      (6)
```

Here `nu>0` is a fixed verified extensive reference charge-variance margin,
acquired next. `D=0` is handled by exact block coefficient DP. These tests are
nonempty for sufficiently small ACTUAL cross bridges; no assertion is made that
an arbitrary useful pairing state passes them. The standard KP rooted bound
then gives `|Q|<=M S`, `|Q^(j)|<=j! M S/s0^j` for
`Q(t)=log[Z(e^t)/product B_B(e^t)]`, plus computable exponential cutoff tails.
The old connected-support/Mobius log algorithm applies unchanged to these new
actual local tensors. Mann--Minko's framework is allowed the same representation.

## 4. Acquire the tilt and check whether charge fluctuations suffice

The reference polynomial `Z0(z)=product_B B_B(z)` is computed by ordinary
coefficient DP, with polynomially growing rational bit lengths. Check reference
feasibility of `k` directly from its coefficient. For interior feasible `k`,
acquire a positive rational `r0` with

```
|mu0(r0)-k|<=1/64,
V0(r0)=d mu0/d log r >= nu M.                                   (7)
```

Here means/variances are exact rational functions of known finite polynomials,
not measured or oracle-supplied statistics. Use rational power-of-two bracketing
and bisection. The total positive coefficient ranges have polynomial input-bit
bounds, so a polynomial number of fugacity bits brackets any interior feasible
sector, as in the reconstructed N89 argument. Return `UNKNOWN` if the chosen
fixed variance margin fails; do not treat very small susceptibility as free.

Poisson-binomial root factors show that under a factor-two tilt change their
variance changes by at most a factor two. Thus throughout `[r0/2,2r0]`,
`V0(r)>=nu M/2`. Reference endpoint means differ from the desired `k` by at least
`nu M/4-1/64`, since `log 2>1/2`. Equation (6) makes the KP mean perturbation
`|Q'|<=M S/s0` much smaller. For all sufficiently large `M` (an explicit constant
depending on `nu`) the FULL means bracket `k`. For the finite smaller range use
exact determinant enumeration, charged as a constant at fixed `b,nu`.

Differentiate truncated clusters to absolute mean error `1/32` and bisect this
rational bracket until `|mu(r)-k|<=1/4`. The global unfiltered charge polynomial
has the internally reconstructed negative-root theorem, so its variance is at
most `m/4`; this supplies a paid finite stopping width as in the dimer proof.
The resulting point mass satisfies `Pr_r(K=k)>=3/[4(m+1)^2]`.

The dependence on `nu` is real: this is a polynomial-time scheme at fixed positive
variance margin. If a promised `nu` shrinks with size/bit length, the constants,
outer-error fallback and runtime dependence must be retained. No general
low-susceptibility or endpoint theorem is being asserted.

## 5. Heterogeneous outer bound, including all negative-reference zeros

On the circle define `u_B(theta)=|B_B(r e^(i theta))|/B_B(r)`. Each native block's
Poisson-binomial representation gives

```
u_B(theta)<=exp[-2 V_B(r) sin²(theta/2)],  V_B(r)<=d_max/4.
```

The forest injection used in the dimer proof applies to (2), even at block
reference zeros. It yields

```
|Z(r e^(i theta))|/Z0(r)
 <= product_B [u_B(theta)+(D+1)h]
 <= exp[-2 V0(r) sin²(theta/2)+(D+1)h 3^d_max M].                 (8)
```

For the second inequality replace each `u_B` by its exponential upper bound and
use `1+y<=exp y` and `exp(2V_B)<=3^d_max`. Divide by the positive-real KP lower
bound `Z(r)>=Z0(r) exp(-M S)`. Equations (6),(7) imply exponential outer-arc
decay at least `exp(-nu M/4)` for `|theta|>=pi/2`. All block zeros on the negative
ray are therefore handled by an ABSOLUTE bound; no invalid log evaluator is
called through them.

The exact `(m+1)`-point Fourier inversion now gives the canonical norm with the
same algorithm as before. Inner values have a relative sector-KP evaluator;
outer values are omitted only under an explicit tolerance test. Otherwise exact
enumeration costs `9^m=exp(O_b(M))`; a failed outer-error test implies
`M=O_(b,nu)(log(1/epsilon)+1)`. Thus that fallback remains polynomial in
`1/epsilon`. Root-of-unity and rational/exponential precision are charged.

## 6. A complete marked observable operation

Let `R_O` be the `r` blocks touched by the bounded charge-conserving Hermitian
`O`. Merge them into ONE superblock, even if geographically far apart. Include
all native `F` edges internal to this union in its exact reference. Outside it
the original blocks are unchanged. Maximum block size becomes at most `rb` and
degree at most `rD`; these are fixed costs. A fermionic permutation can place
these modes contiguously. Its signs and the transformed finite operator are
computed, not discarded. The merged reference has even parity and is a native
projected-BCS state, so its own unfiltered charge polynomial still obeys (3).

Set `t=2^(-d_* -5)`, where `d_*` bounds the charge degrees of ALL blocks in the
new partition, including every unmarked block. The safe choice
`d_*=floor(rb/2)` suffices; using just the actual merged block's degree need not
bound an unmarked reference in the outer factor `3^d_*`. Apply the mathematical
norm filters

```
A_+=I+tO,      A_-=I-tO.
```

This is a classical contraction device, not an acquired physical filter. They
are invertible, charge conserving and even. For every pair-number sector,

```
(1-t)^2 c_k <= c_k^± := ||A_± psi_k||² <= (1+t)^2 c_k,             (9)
c_k^+-c_k^- = 4t <psi_k|O|psi_k>.
```

The marked reference charge polynomial need NOT remain real-rooted. Instead,
coefficientwise its difference from the native merged-block polynomial is at
most `(2t+t²)` times the latter's positive coefficient. Combining with (3),

```
|B_mark,±(z)-B_mark,0(z)|
 <= (2t+t²) B_mark,0(|z|)
 <= (2t+t²) 2^d_* |B_mark,0(z)| <= (1/8)|B_mark,0(z)|.
```

Thus the marked sector denominator is nonzero, and its local operator-norm
condition number is at most `2^(d_*+2)`. The parity gain of §2 remains true:
the local filter preserves even parity, so an active merged block still needs
at least two incident cross factors. In the actual marked activities insert
`A_±† A_±` AFTER the cross-edge operations on the marked block; the filter is
not commuted through creation operators and (1) is not reused with a fictitious
filtered input state. The operator-norm estimate uses this inserted finite
matrix, while an inactive marked block has the stated filtered reference norm.
Recompute the actual coarse graph and
the conservative envelope/tests (4)--(6) with the enlarged constant block size.
If these tests fail, return `UNKNOWN` for this observable, even if an earlier
unmarked norm certificate passed. For any fixed `r,b`, a nonempty uniform
sufficient bridge regime exists; this is not an unconditional observable oracle.

Use the SAME acquired full-state tilt `r` from §4. Do NOT search for a new
filtered real-root representation or assume one. Equation (9) and the analogous
grand-norm bound give

```
Pr_r,±(K=k) >= [(1-t)/(1+t)]² Pr_r(K=k).                          (10)
```

For the marked outer bound, ignore the marked block's characteristic function
(it is at most one because its norm polynomial has nonnegative coefficients).
The unmarked blocks retain native negative roots. Their total reference charge
variance is at least the original `V0(r)` minus `r d_max/4`; merging removes only
that many constant degrees. Use the ACTUAL merged coarse count `M'`, recomputed
envelope `h'`, KP bound `S'`, graph degree `D'`, and charge-degree bound `d_*`.
Compute the exact rational variance sum `V_u(r)` of the unmarked references and
verify

```
V_u(r)>=nu M'/4,
S'+(D'+1)h' 3^d_*<=nu/16.
```

The same forest proof, with only native unmarked characteristic bounds, gives
the explicit estimate

```
|Z_±(r e^(i theta))|/Z_±(r)
 <= exp[-V_u(r)+M'(S'+(D'+1)h'3^d_*)]
 <= exp[-3nu M'/16],                   pi/2<=|theta|<=pi.         (10a)
```

No unspecified prefactor or exponent is needed. Use the rational upper bound
`2^(-floor(3nu M'/16))` in the actual outer omission/tolerance test, with the
filtered mass lower bound (10). A failure invokes exact enumeration as above;
the linear exponent makes that branch polynomial in `1/epsilon` at fixed
`b,r,nu`. Merging removes only constant reference variance, so the variance
test is inherited for sufficiently large `M` from (7); the finite exceptional
range can be enumerated exactly. Alternatively retaining the exact positive
exponent `V_u-M'(S'+(D'+1)h'3^d_*)` improves the explicit tolerance, while its
linear lower bound must still be retained for the complexity statement.
This prices both the merged block and its variance. There is no unobserved
rare-event or infinite-bandwidth primitive.

Consequently `c_k`, `c_k^+`, `c_k^-` all have paid relative approximations at
the same tilt with polynomial conditioning. For relative error `sigma<1/4`
in those three quantities, the polarization estimator

```
<O>_k = (c_k^+-c_k^-)/(4t c_k)
```

has additive error at most

```
sigma/(1-sigma) [ (1+t)^2/(2t)+1 ].                              (11)
```

Taking `sigma=epsilon t/16` suffices. No division by a possibly zero observable
or physical-outcome probability occurs. The real and imaginary parts of a
non-Hermitian number-conserving hopping/pair operator are handled separately,
with their actual norm bounds. Constant-support spin operators preserving
occupation are included. A local Hamiltonian's energy follows with accuracy
allocation `epsilon_E/sum_a |h_a|`; runtime depends on the NUMERICAL ratio
`sum|h_a|/epsilon_E`, which need not be polynomial in coefficient bit length
when coefficients are exponentially large. This is variational energy only.

## 7. What class has actually been opened

The controlled class now permits nonperturbative resonance and interference
inside exactly computed bounded blocks, weak signed fermion bridges on
high-width/nonbipartite graphs, an exact global particle number, and bounded
charge-conserving observables including separated pair transfer. Neither a gap
nor a ground-state promise was inserted. A generic near-product-dimer statement
would miss the strong internal block states; a pointwise real-fugacity KP value
would miss the canonical operation and complex-reference-zero issue.

This is nevertheless not a generic new cluster method. Equally informed
embedded-cluster, tensor-network, and polymer implementations may use these same
blocks, parity, scalar stability and coefficient reconstruction. The zero-bridge
case is ordinary exact DP. The closest physical baseline is projected-BCS VMC
and projected d-wave fPEPS; those reach physically useful parameter regions not
shown to satisfy our small-bridge certificates. We prove no speed advantage on
their instances, and no novel ownership of number projection or Gutzwiller states.

Computing separated pair correlations does not alone prove stable ODLRO,
superfluid stiffness, a material phase or a correct ground state. It now supplies
an actual certified observable operation with which a claimed property of a
supplied state can be checked. Systematic preparation/sampling and a useful
Hamiltonian-optimized or experimentally acquired state remain separate gates.
The reference/matrix/partition data are supplied and algebraically acquired;
they are not native continuous bath access or an ideal physical corrector.

Development exposure: the owner built the canonical/forest operation, then read
the stronger N89 proof in full and reconstructed its primary stability facts.
Root supplied independent contour/filter/mass-transfer suggestions and whole
audits; the four existing exposed Luna supports supplied bounded challenges.
This note is not a blind-independent novelty experiment. Old scientific bytes
and protected proof fields were not edited.

Finite replay and a corrected checker defect: `check_block_observables.py`
enumerates 12 real-rational sites in three strongly resonating four-site blocks.
It checks the projected cross-creator product against an independent full
partial-matching Fock state, every grand/canonical gas coefficient, the parity
zeros, and both distant marked filters. The visible bridge `1/20` is NOT claimed
KP-certified. Separate exact algebraic tests show a nonempty sufficient family
at bridge `1/10^13`, including enlarged marked-block bounds; these are not a
large-system FPTAS execution. In the visible fixture, the Hermitian pair-transfer
expectation at three pairs is exactly `3363203/28264895`, matching polarization.

Root found that the first finite `tensor_states` helper omitted the fermionic
shuffle sign on arbitrary interleaved block mode sets. Even block parity did
not justify that omission. The helper now multiplies by the parity of all cross
inversions of occupied orbitals. The minimal blocks `(0,2),(1,3)` counterexample
exhibits four wrong amplitudes in the OLD ungraded helper, while the corrected
helper matches the full state. A nonzero-bridge 12-site fixture with fully
interleaved blocks `(0,3,6,9),(1,4,7,10),(2,5,8,11)` also passes all gas/parity
and marked-even-operator identities, and its observable equals the contiguous
fixture under the exact fermionic permutation. The theorem already requires
graded signs; the numerical helper was repaired rather than weakening that
requirement. These finite real checks do not certify the general complex proof.
