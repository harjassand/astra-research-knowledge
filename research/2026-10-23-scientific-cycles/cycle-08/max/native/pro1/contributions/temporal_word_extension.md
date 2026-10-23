# Exact three-case classification of the temporal endpoint coefficient

Cycle7 constructive contribution. The actual Cycle6 main proof, constructive
note and token replay were read. This note proves a new all-length operation;
bounded executable checks below are diagnostics, not its proof.

## Interface and conventions

Use the unchanged device, its charge-pinched **bulk** coefficient `G1`, and
the endpoint decomposition from Cycle6. On endpoint charge `01`, the pair
coefficient is

\[
 K_{ij}=C_j^-C_i^+-C_i^+C_j^-,\qquad 0\le i<j<k.
\]

The adjoint occupies the disjoint reverse endpoint sector. Different endpoint
pairs and different complete binary charge patterns have orthogonal weighted
matrix blocks. Conditional on a complete charge pattern, all input color
wires are independent maximally mixed qubits under `sigma`.

For a fixed complete pattern with `z_i=0,z_j=1`, let

* `m` and `h` be the unmatched pop and push counts in the prefix before `i`;
* `d` and `e` be the unmatched pop and push counts in the middle `(i,j)`.

Matching is the usual last-in-first-out cancellation of a push followed by
its later pop. Equivalently, with a walk step `+1` for a colored port and
`-1` for zero,

\[
 h=S_i-\min_{0\le t\le i}S_t,\qquad
 d=-\min_{0\le t\le j-i-1}T_t.
\]

These depend on different disjoint input charge bits. The case `i=0` has
`m=h=0`; the empty middle has `d=e=0`.

## The exact token normal form

Write `E=U_(i-1)...U_0`, `M=U_(j-1)...U_(i+1)`, and
`D=M* U_j M`. Direct cancellation of involutions gives

\[
 C_jC_i=E^*U_iDE,\qquad C_iC_j=E^*DU_iE.                 \tag{1}
\]

We first evaluate these raw words on a sufficiently deep coordinate core,
so no displayed call hits the vacuum. The established finite-prefix
representation then identifies the same coefficient on every initial depth
at least `k`. This is a **bulk proof**; it does not claim the new identities
hold through an arbitrary vacuum encounter.

Let the original bath colors be `B_0,B_1,...`. Give the unmatched prefix
pushes the chronological color names `a_1,...,a_h`. Dyck matched factors
are input-color permutations tensor bath identity; their inverses cancel
even if the intervening bath changes. After `E`, the unmatched prefix pops
hold `B_0,...,B_(m-1)` and the bath stack is

\[
 P=(a_h,\ldots,a_1,B_m,B_{m+1},\ldots).                 \tag{2}
\]

Let the unmatched middle pushes carry chronological colors
`u_1,...,u_e`, and let the endpoint `j` carry color `z`. The toggle `D`
has the following exact normal form:

1. If `e>0`, remove `w=u_1` from the first unmatched middle push, shift
   the remaining middle colors one position toward the first, and put `z`
   into the last such position. If `e=0`, put `w=z`.
2. Set port `j` to zero.
3. Insert `w` into the bath at zero-based index `d`.

All matched middle colors are restored, and its unmatched pop ports return
to zero. To verify the claim, `M` temporarily removes the top `d` bath
colors, then pushes `u_1,...,u_e`. The call at `j` pushes `z`. In `M*`,
the reverse unmatched pushes pop the shifted queue, leaving `u_1` (or `z`)
on top of the unconsumed bath. The reverse unmatched pops restore the
temporarily removed `d` colors above it. This proves precisely an insertion
at index `d`, with no averaging of amplitudes.

Let `Ins_d(w,P)` mean this insertion and `Pop` remove the top color into
port `i`. In (1) the two local actions therefore are

\[
 A=\operatorname{Pop}\circ\operatorname{Ins}_d(w,\cdot),\qquad
 B=\operatorname{Ins}_d(w,\cdot)\circ\operatorname{Pop}. \tag{3}
\]

They have identical middle-color shifts. For `d=0`, action `A` puts `w`
into port `i` and leaves `P` unchanged, whereas `B` puts `P_0` into `i`
and replaces the top stack color by `w`. For `d>=1`, both put `P_0` into
port `i`, and their stacks are respectively

\[
 \begin{split}
 A &: (P_1,\ldots,P_{d-1},w,P_d,P_{d+1},\ldots),\\
 B &: (P_1,\ldots,P_{d-1},P_d,w,P_{d+1},\ldots).
 \end{split}                                                    \tag{4}
\]

Thus their relative permutation is always the single transposition of
the distinct source wires `w` and `P_d`. Applying the same `E*` afterward
preserves that assertion. Its reverse unmatched pushes remove the first
`h` stack colors into the prefix input positions; its reverse unmatched
pops restore the stored colors `B_0,...,B_(m-1)`. This gives the following
complete classification.

### Case I: `h>d`

Here `P_d=a_(h-d)` is an input color. All changed stack positions in
(3)--(4) are among the first `h` colors consumed by `E*`. Both final baths
are exactly the original bath. The coefficient is

\[
 K_{ij}=P_A(I-\mathrm{SWAP}_{w,a_{h-d}})\otimes I_E,    \tag{5}
\]

on the selected complete charge sector. `P_A` is an input-color unitary
to the endpoint-swapped sector. The two wires are distinct. Its normalized
color Hilbert--Schmidt square is exactly one after **every** prefix density
contraction, including coherent and entangled densities.

### Case II: `h=d`

Now `P_d=B_m`. In action `A`, all modified stack positions are consumed
by `E*`, leaving the original bath. In action `B`, `B_m` goes to the input
wire that action `A` would fill with `w`, and `w` replaces `B_m` in the
bath. Consequently

\[
 K_{ij}=(P_A\otimes I_E)(I-\mathrm{SWAP}_{w,B_m}).       \tag{6}
\]

For an arbitrary prefix density `zeta`, let `zeta_m` be its one-color
reduced density at bath coordinate `m`. Contracting (6) gives

\[
 P_A(I-\zeta_m)_w,\qquad
 2^{-q}\operatorname{Tr}(K_{ij,\zeta}^*K_{ij,\zeta})
   =\tfrac12\operatorname{Tr}(\zeta_m^2)
   =\tfrac14+\tfrac12\operatorname{Tr}(\zeta_m-I/2)^2
   \ge\tfrac14.                                           \tag{7}
\]

The contraction identity follows directly from
`Tr_E[(I tensor zeta) SWAP_(w,B_m)]=zeta_m` on wire `w`; spectators
give identities. No product, diagonal or separable assumption is imposed
on `zeta`.

### Case III: `h<d`

Write `r=d-h>=1`. Both actions export the input color `w` to the bath,
extract `B_m` to the same input location, and shift all other input colors
identically. Their final baths differ only in the adjacent placements

\[
 \begin{split}
 A &: (B_0,\ldots,B_{m-1},B_{m+1},\ldots,B_{m+r-1},
                      w,B_{m+r},B_{m+r+1},\ldots),\\
 B &: (B_0,\ldots,B_{m-1},B_{m+1},\ldots,B_{m+r-1},
                      B_{m+r},w,B_{m+r+1},\ldots).
 \end{split}                                                   \tag{8}
\]

The empty sublists in this formula are omitted. Unlike the first two
cases, no positive universal lower beyond zero is asserted. Against a
pure repeated-color prefix `|u><u|^tensor k`, the two operator contractions
are **identical**: each extracts `u` into the same input wire and multiplies
by `<u|w>`, regardless of the insertion position of `w` in (8). They
therefore cancel. Linearity gives the same cancellation for every mixture
of such repeated-color prefixes.

## Exact simultaneous minimizer and receiving interface

Take the analytic prefix state

\[
 \zeta_{\rm sym}=\int |u\rangle\langle u|^{\otimes k}\,d\mu(u)
                 =P_{\rm sym}/(k+1),                           \tag{9}
\]

where `mu` is the unitary-invariant probability on pure color qubits.
Only the integral representation and its one-site marginal `I/2` are
needed: they follow from unitary invariance. If desired, the equality to
the normalized symmetric projection follows from the elementary qubit
symmetric-power representation, or directly by integrating the binomial
coefficients in the monomial basis.

Case I has fixed square norm one. Case II attains its lower `1/4` because
every one-color marginal of (9) is `I/2`. Case III vanishes by the preceding
pointwise pure-product calculation. Thus (9) simultaneously minimizes
**every** endpoint-pattern contribution. Complete matrix-block
orthogonality then proves exact global optimality, with no assumption
that a prefix average is generally optimal:

\[
 v_k=\frac12\sum_{i=0}^{k-2}\sum_{r=0}^{k-i-2}
 \left[\Pr(H_i>D_r)+\frac14\Pr(H_i=D_r)\right].           \tag{10}
\]

Here `H_i` is the number of unmatched pushes of an independent fair
length-`i` charge walk, and `D_r` the number of unmatched pops of an
independent fair length-`r` walk. The factor `1/2` is twice the oriented
endpoint probability `1/4`; reversing the endpoint orientation adds the
adjoint block, whose weighted norm is equal. Later charge bits are free.

Equation (10) is the receiving interface for the separate combinatorial
summation and operator-dual contribution. The symmetric prefix is an
analytic dual witness, **never a replacement physical initializer**.
To obtain a communication theorem the owner must still use the closest-
point optimizer, actual positivity, exact nonlinear inward drift and the
inherited arbitrary-reference coding bridge at block length fixed before
the coding horizon.

Already (10) gives an elementary all-length quadratic lower without any
asymptotic estimate. By reversal of the first walk, `H_i` has the same
law as the maximum of a length-`i` fair walk, and `D_r` has the analogous
law at length `r` by sign symmetry. The triangle `i+r<=k-2` is symmetric
under interchanging the two lengths. Put

\[
 N=\frac{k(k-1)}2,\qquad
 E_k=\sum_{i+r\le k-2}\Pr(H_i=D_r).
\]

Then the sum of `Pr(H_i>D_r)` is `(N-E_k)/2`. Consequently

\[
 v_k=\frac N4-\frac{E_k}8
     \ge\frac N8=\frac{k(k-1)}{16}
     \ge\frac{k^2}{32}\quad(k\ge2),                    \tag{10a}
\]

because `0<=E_k<=N`. This supplies the exact lower constant in the
previously conditional quadratic-growth transfer. A precise closed form
and sharp leading coefficient are a separate simple summation of (10),
not additional dynamical assumptions.

### A stronger operator equality and explicit optimizer

Put `H_sym=H_(zeta_sym)`. In Case I its pattern block is
`P_A(I-SWAP)`; in Case II it is `P_A/2`; in Case III it is zero,
always with the adjoint block on the reverse endpoint sector. Thus it
has an explicit finite input-only definition without solving a numerical
prefix minimization.

For every prefix density `zeta`, the Case I block of `H_zeta-H_sym`
is zero. The Case II block is `P_A(I/2-zeta_m)`, whose weighted
Hilbert--Schmidt inner product with `P_A/2` is zero because
`Tr(zeta_m-I/2)=0`. The Case III block of `H_sym` is zero.
Matrix-block orthogonality therefore proves

\[
 \langle H_{\rm sym},H_\zeta\rangle_\sigma=v_k,
 \qquad
 \|H_\zeta\|_\sigma^2
   =v_k+\|H_\zeta-H_{\rm sym}\|_\sigma^2.              \tag{11}
\]

Equivalently, for the full operator contraction `T` already defined,

\[
 T_k(\sigma H_{\rm sym})=v_k I.                         \tag{12}
\]

Indeed the expectation of the left side against every density `zeta`
is the first expression in (11), since the diagonal affine term is
orthogonal to `H_sym`. This is stronger than a one-sided closest-point
inequality. The exact optimizer is consequently
`X_*=-(ln2)/2 sigma H_sym` with scalar leading operator drift, although
the **full nonlinear** bath dynamics need not be scalar. No uniqueness
of the minimizing prefix density or efficient compiler is asserted.

## Scope and omission examples

The earlier guard/meander sufficient identity is contained in Case I
but did not count all its patterns. It survives as a stronger whole-bath
raw-word statement on that narrower family. The new classification is
for the **bulk coefficient**, and the actual root must remain in the
subsequent Lyapunov theorem. Omitting that distinction remains invalid.

The word `100111`, endpoints `i=1,j=5`, has `h=d=1`. It is Case II,
not a bath-independent Case I word. Its old failed whole-bath shortcut
is now assigned its legitimate uniform contracted square `>=1/4`.

The word `001`, endpoints `0,2`, has `h=0<d=1`. Both words export its
endpoint color and extract the top bath color. For a repeated-color
prefix their contractions coincide. Thus one cannot assign the Case II
positive lower to every pattern merely because the two raw permutations
differ by one transposition. The source position and final bath overlap
are essential.

## Checks and costs

`temporal_word_extension.py` checks the independent reduced-stack formula
against the original root-retaining raw calls on sufficiently deep exact
symbolic token coordinates. It verifies the three cases, single relative
transposition, bath identity where asserted, and the omitted-premise
witnesses. Its JSON records actual pattern counts, runtime and peak process
memory. None of those bounded checks proves the all-length classification;
the normal form (1)--(8) does. Total inference, discovery and independent
review costs remain unknown. No paid resources or outreach were used.
