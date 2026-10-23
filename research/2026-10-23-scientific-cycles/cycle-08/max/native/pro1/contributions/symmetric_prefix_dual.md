# An exact symmetric-prefix minimizer and a scalar operator certificate

Cycle7 distinct contribution. This note supplies the full-prefix dual and
operator consequence of the all-length token trichotomy proved independently
in `temporal_word_extension.md`. It uses the actual Cycle6 bulk coefficient,
not a finite reflecting bath or a fresh-channel model. The author read the
Cycle6 `TEMPORAL_GROWTH.tex`, temporal operator note, exact k4 rational
certificate, root-retaining representation and token replay before deriving
this extension. The proof below is analytic; bounded replays are diagnostics.

## 1. Definitions and exact interface

Let sigma=diag(1/2,1/4,1/4)^tensor k and Q count colored input ports.
Let G1 be the first b=beta^2 coefficient of the charge-pinched physical bulk
displacement, acting on the k input ports and their first k bath colors.
For a prefix density zeta define

    H_zeta = Tr_F[(I tensor zeta)G1]+2Q-kI,
    T(X) = Tr_A[(X tensor I)G1],
    v_k = min_zeta Tr(sigma H_zeta^2).

Every density, including arbitrary coherent and entangled prefix densities,
is admitted. These are finite-dimensional analytic dual variables. None is
physically prepared, no reachability claim is needed, and the actual normal
initializer is unchanged.

The Cycle6 endpoint decomposition expresses the input-offdiagonal part of
G1 as a sum of Hermitian endpoint terms. For fixed i<j, choose input endpoint
bits01; all other input charge bits are fixed. Its offdiagonal block is the
raw ordered-toggle difference K between that complete charge sector and
its endpoint-swapped sector. The use of the raw word as the graded coefficient
is a BULK identity; the actual root remains in the coding theorem.

The all-length token theorem gives three possibilities, determined solely by
h, the number of unmatched pushes in the prefix before i, and d, the deficit
of the middle word (i,j):

* h>d: K=P(I-S_ab) tensor I_F. Here a,b are distinct input color wires,
  P is an input color permutation to the target sector, and both raw words
  restore the entire initial bath.
* h=d: K=(P tensor I_F)(I-S_a,m). Here S_a,m swaps one input color with
  one initial bath coordinate m, the first raw word restores the bath, and
  the second has exactly that input/bath exchange. The other bath colors
  and untouched tail remain identities.
* h<d: each raw word exports exactly one input color and extracts the same
  initial bath color. The two final bath words differ only in the position
  where that exported color is inserted among initial bath colors. On a
  bath tensor power |u>^tensor k, their input-operator contractions are
  identical for every unit color vector u.

The final clause is equality after contraction, not a claim that either
raw branch leaves the bath unchanged. It follows directly from the two
explicit word outputs in the token proof: all initial bath tokens have
color u; the inserted input color contributes the same <u| bra, and the
extracted token contributes the same |u> ket. Changing its insertion position
among copies of u has no remaining effect. The equality holds before any
average over u. All affected original bath coordinates lie within the
first k colors: in Case III the last one is m+(d-h)<=i+(j-i-1)<=k-2;
in Case II the exchanged coordinate m<=i<=k-2. Thus a finite k-coordinate
tensor-power prefix suffices, with the remaining bath tail untouched.

## 2. Universal contribution of each charge-pattern block

On a fixed complete charge sector with q colored input ports, sigma is a
scalar times the normalized color density I/2^q. Denote its normalized
Hilbert--Schmidt square by ||A||_col^2=2^-q Tr(A* A).

For h>d, normalized trace of a swap on two distinct qubit colors is1/2,
so

    ||K_zeta||_col^2 = ||I-S_ab||_col^2 = 1

for every zeta. For h=d, partial trace of an input/bath swap is precisely
the reduced density zeta_m on that bath coordinate (no transposition in the
specified convention). Consequently

    K_zeta = P(I-zeta_m),
    ||K_zeta||_col^2 = (1/2)Tr[(I-zeta_m)^2]
       = 1/4 + (1/2)Tr[(zeta_m-I/2)^2] >= 1/4.

This step uses only positivity and unit trace of the reduced density. It
allows all coherences and correlations with every other prefix coordinate.
For h<d, the square is nonnegative; no false pointwise-zero claim is made.

Distinct endpoint pairs occupy orthogonal complete charge-pattern blocks.
For the same pair, distinct full charge patterns are likewise orthogonal.
Thus their nonnegative squares add, without cancellation from other paths.
The reverse-oriented block is the adjoint; it has the same q and therefore
identical sigma weight. This permits a factor of two only between these
specified disjoint endpoint orientations.

## 3. One density attains every bound simultaneously

Define the symmetric-prefix density

    zeta_sym = integral |u><u|^tensor k du = P_sym,k/(k+1),

where du is normalized unitarily invariant measure on pure qubit colors.
This identity can be checked without invoking an asymptotic de Finetti
statement: write u=sqrt(t)|1>+exp(i phi)sqrt(1-t)|2>, take uniform t in[0,1]
and uniform phi in[0,2pi], and integrate matrix entries. Only entries with
equal color weight r survive, and their common value is

    integral_0^1 t^(k-r)(1-t)^r dt
      = 1/[(k+1) binom(k,r)].

That is exactly the normalized projector onto the symmetric subspace.
In particular each one-coordinate marginal is I/2.

For h>d the universal block value remains1. For h=d all marginals I/2
give K_sym=P/2 and square1/4. For h<d the two contracted raw words agree
for each pure tensor bath |u>^tensor k by the explicit token outputs, hence
K_sym=0 by linearity of the integral. The same density works for every
endpoint and every full charge pattern. Therefore the universal lower is
attained simultaneously and is the exact full-prefix minimum, not a
restriction to symmetric or product dual variables.

If N_00 and N_01 count complete binary charge-pattern/endpoint pairs in
the first two types with oriented endpoints01, then

    v_k = (2/2^k)(N_00+N_01/4).

The parent proof supplies the all-length random-walk count. In particular,
with independent fair-walk maxima M_i,M_r,

    v_k=(1/2) sum_{i,r>=0, i+r<=k-2}
             [Pr(M_i>M_r)+(1/4)Pr(M_i=M_r)].

The formula is an exact operator optimum because the preceding argument
holds for every zeta and provides one actual admissible minimizer.

## 4. The dual gradient is exactly scalar at every length

Let H=H_(zeta_sym). In fact the stronger identity

    T(sigma H) = v_k I_F

holds, not merely the closest-point inequality T(sigma H)>=v_k I_F.
To prove it, perform the same blockwise trace over input colors. The input
diagonal part of G1 has zero pairing with input-offdiagonal H. In type00,
H=K is input-only, so its input trace with K is the constant1 times I_F.
In type01, H=P/2 and K=(P tensor I)(I-S_a,m), and

    2^-q Tr_input[H* K]
       = (1/2)(I_F-(1/2)I_F) = (1/4)I_F,

using normalized partial trace of the qubit swap equal to I_F/2. In type11,
H=0 and the contribution vanishes. Adding sigma weights and adjoint
orientations gives exactly the same constant v_k as the variance count.
All prefix coordinates, including off-diagonal elements and all coherent
vectors, are covered by this matrix identity.

The preserved closest-point theorem now gives

    A_k=(ln2)v_k/8,
    X_*=-(ln2/2)sigma H,
    T(X_*)=-(ln2/2)v_k I_F.

No rank assumption on zeta_sym is needed; its rank is k+1, generally below
2^k. This explicit minimizer removes the unresolved finite-dimensional
minimization from the leading-order construction. It does not provide an
efficient code compiler, control the growing-block nonlinear remainder by
itself, or establish a capacity formula.

## 5. Necessary scope distinctions and failed shortcut

The k4 values are not translation invariant by endpoint distance: under
zeta_sym, contributions for pairs(0,1),(1,2),(2,3),(0,2),(0,3),(1,3)
are respectively1/8,5/16,5/16,1/16,1/16,3/16. Thus a distance-only
endpoint formula is false. The parent's eventual aggregate convolution
identity uses symmetry of prefix and middle walk lengths after summation;
it cannot be promoted to a termwise identity.

The h<d term need not vanish for arbitrary prefix states. An exact witness
is the charge word001 with endpoints i=0,j=2, hence h=0<d=1. Take the
first two initial bath colors1,2. The two raw words send input[0,0,z]
to output[1,0,0] and bath[z,2,...], or to that same output and bath[2,z,...],
respectively. Contraction against the original bath gives |1><1| for the
first branch and zero for the second. The normalized color square is1/2,
whereas zeta_sym makes the difference zero. Its disappearance
is a property of the analytic symmetric density. Replacing this density by
the actual physical initializer would be an inadmissible operation and is
unnecessary. Conversely replacing the whole full-prefix minimization by
one average without a universal lower would not establish the theorem.

Root exchange is not removed: the raw word proof and the bulk grading have
different scopes, and the later operator-drift/coding transfer retains the
finite root remainder. No terminal return is inferred. A source-complete
uniform transfer is still required for any communication consequence.

## Status and observed costs

The present proof is contingent only on the explicit all-length token
normal form in the accompanying constructive source and the preserved
Cycle6 endpoint decomposition. Those mathematical sources, not a finite
check count, carry the argument. A focused exact token diagnostic through
k8 identified the three cases in under a second on the local process; that
is not the cost of discovery. Total inference, design and review costs are
unknown. No external acceptance, historical originality, practical encoding
complexity or physical device performance is asserted.

## Focused independent challenge of the written normal form

I subsequently read the actual `temporal_word_extension.md`, equations(1)--(8),
and independently checked the three cases, rather than accepting the
reported token counts. For an arbitrary fixed binary word, each matched
Dyck factor acts as an input-color permutation tensor bath identity. It
therefore cancels with its inverse even though the middle inserted color
changes the intervening bath. The unmatched prefix leaves precisely the
stack (a_h,...,a_1,B_m,...). The unmatched middle insertion at depth d
then yields the two stacks in equation(4). The h colors consumed by E*
put the swapped pair wholly in the input when d<h, across the input/bath
cut when d=h, and wholly in the final bath when d>h. The d=0 cases obey
the separately displayed pop/insert formula and give the same classification.
No normal-form gap was identified.

The index bound above checks the only remaining finite-prefix uniformity
point in the simultaneous-minimizer proof. The raw toggles were evaluated
on the sufficiently deep algebraic core, then identified with the inherited
physical finite-prefix coefficient; no vacuum claim was inferred. This
focused challenge does not repeat the old coding audit, certify historical
priority or establish anything about later source edits.
