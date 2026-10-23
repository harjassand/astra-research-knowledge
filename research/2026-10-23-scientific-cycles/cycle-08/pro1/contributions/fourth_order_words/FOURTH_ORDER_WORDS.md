# Exact fourth-order contraction and counterexamples

Contributor: `/root/cycle8_fourth_order_words`, 22 October 2026.

This contribution uses the actual Cycle7 bulk observable and explicit optimizer.
It does not reopen the sharp susceptibility theorem. The useful new operation
is an exact coefficient representation that keeps final-bath overlaps, followed
by finite exact counterexamples to two tempting nonlinear shortcuts.

## 1. Model and scope

Retain the root-retaining unitary, one evolving bath, charge Q, and the physical
ordered k-call product from `SHARP_TEMPORAL_GROWTH.tex`. Put b=beta^2. Let
G(b)=G0+b G1+b^2 G2+... be its input-charge-pinched finite bulk displacement.
For initial depth at least k, every history avoids a vacuum exchange before its
last call, and its paired amplitudes depend only on the first k initial colors.
The actual root is not replaced by a cutoff. The finite coefficient is tensor
identity on the seed and untouched tail.

Let sigma=diag(1/2,1/4,1/4)^tensor k and H be the exact Cycle7 optimizer.
Write H=sum_{i<j} H_ij, where H_ij connects complete binary charge patterns
that differ at exactly i,j, with endpoints 01 and10. All other charge bits agree.
The input color values need not agree: their actual permutations are retained.

All statements below are finite bulk coefficient identities. An analytic
deleted-call process is only a representation of a coefficient of the original
coherent device. It does not remove physical calls from the communication cost,
replace the device by a noisy classical channel, or provide bath access.

## 2. Full G2 from raw physical histories

For a stay mask M subset {0,...,k-1}, let U_M be the ordered physical word with
I at calls in M and U at the other calls. The coherent amplitude is

    alpha^(k-|M|) (i beta)^|M| U_M.

On a fixed input-charge sector q and a common output charge word o, the bath
displacement is q-|o|. Equal final bath coordinates and common output word
must be retained when pairing histories. Define D_(2r) as the sum of these
paired displacement operators with |M|+|N|=2r and phase i^(|N|-|M|).
Equivalently this is the charge pinching of

    sum_{|M|+|N|=2r} i^(|N|-|M|)
      [ Q U_M* U_N - U_M* Q U_N ].

No subtraction of unbounded bath-depth expectations is used. The equal-charge
bulk matrix blocks have even total stay count. Therefore, exactly,

    G(b)=sum_{r=0}^k b^r (1-b)^(k-r) D_(2r),
    G0=D0,
    G1=D2-k D0,
    G2=D4-(k-1)D2+binom(k,2)D0.

As H is input-offdiagonal and the all-move D0=(2Q-k) tensor I is diagonal,
Tr_A[(sigma H tensor I)D0]=0. The completed Cycle7 scalar certificate then gives

    K2 := Tr_A[(sigma H tensor I)G2]
       = Tr_A[(sigma H tensor I)D4] - (k-1) v_k I.       (1)

This is an all-k exact identity, not an asymptotic approximation.

## 3. Charge selection reduces D4 to one spectator deletion

For a bulk input charge bit z_l and stay bit m_l, the output charge is

    o_l = z_l if m_l=1, and 1-z_l if m_l=0.

Suppose the two input charge patterns differ exactly at endpoints i,j. Equal
output charges force their stay masks to agree at every spectator and to be
complementary at i,j. Thus there is one common spectator mask S and a choice
a subset {i,j} such that M=S union a, N=S union ({i,j}\a).

The total stay count is 2+2|S|, and the two amplitudes have the common magnitude

    b(1-b) b^|S| (1-b)^(k-2-|S|).

The endpoint phases are -,+,+,- for a=00,01,10,11. For the convention that
the first input pattern has endpoint charges 01 and the mask tuple is
(stay_i,stay_j), the output endpoint charges are 10,11,00,01. After cancellation
of the common output-charge term by unitarity, the residual signed endpoint
coefficient is A_10-A_01. Reversing the endpoint/mask convention reverses these
labels, not the physical coefficient. This sign convention is relevant when
comparing independent formulae.

Let B_ij^S be the endpoint coefficient of G1 for the ordered word with
spectator calls S deleted, embedded as identity on those input ports. Define

    A_ij,S = Tr_A[(sigma H_ij tensor I) B_ij^S].

The *full original* H_ij remains in this formula. It is not the optimizer for
the shortened word. Summing the exact paired amplitudes gives

    Tr_A[(sigma H tensor I)G(b)]
      = b(1-b) sum_{i<j} sum_{S subset spectators(i,j)}
          b^|S| (1-b)^(k-2-|S|) A_ij,S.                (2)

The nonnegative spectator weights arise from matching two coherent histories.
Endpoint interference and exact color/bath overlaps remain inside A_ij,S.
Equation (2) is not a classical independent-error model for the device.

At b=0, sum_{i<j} A_ij,empty=v_k I. Taking the next coefficient yields

    K2 = sum_{i<j} sum_{r notin {i,j}} A_ij,{r}
         -(k-1) v_k I.                               (3)

For any p>=1, the complete coefficient interface is

    Tr_A[(sigma H tensor I)G_p]
      = sum_{i<j} sum_{|S|<=p-1}
          (-1)^(p-1-|S|) binom(k-1-|S|,p-1-|S|) A_ij,S.

The separate weighted-remainder contribution proves the uniform operator-norm
bound needed by the principal investigator's nonlinear and coding transfer.
The identities here identify exactly what that bound controls.

## 4. The scalar certificate does not persist coefficientwise

The included exact physical-history replay gives

    k=2: K2= -I/8,
    k=3: K2= -23 I/32,
    k=4: K2= -113 I/64 - (3/64) SWAP_(first two bath colors).

In the last line the operator is tensor identity on all remaining colors and
the seed. It is not scalar. Its eigenvalues on the symmetric/antisymmetric
first-two-color spaces are respectively -29/16 and -55/32.

For example, with prefix words ordered lexicographically in colors1,2,
the entry between (1,2,1,1) and (2,1,1,1) is exactly -3/64. The replay checks
the entire 16-by-16 prefix matrix against the displayed swap formula, not only
this entry or an averaged expectation.

This finite exact counterexample rules out extending T_k(sigma H)=v_k I
coefficient by coefficient to the nonlinear device. No conclusion about
asymptotic K2 growth is drawn from the k2..5 table.

## 5. Deleting a call does not substitute a reduced optimizer

At k=3 the exact single-deletion contractions are

    sum_{i<j, r notin {i,j}} A_ij,{r}
      = I/8, I/32, I/8 for r=0,1,2, respectively.

Their sum is 9I/32. Replacing each by the reduced two-call certificate v2 I
would give 3I/8, which is false. Equation (3) instead gives

    K2=9I/32-2(1/2)I=-23I/32.

The current optimizer encodes the original temporal geometry. Removing a
physical history call does not remove its correlations from that input matrix.
The inherited H must remain inside every contraction in (2).

## 6. Why the pair-support premise cannot be omitted

For k=4 choose input bra x=(0,1,0,1), input ket y=(1,0,1,0), and the same
bath prefix w=(1,2,1,1) on both sides. These input charges differ at four sites.
The exact physical bulk matrix element is

    <x,w|G(b)|y,w> = b^2(1-b)^2.

In particular G1 has zero at this entry but G2 has value1. The two masks must
be complementary at all four sites, so total stay count is exactly4 and every
matching pair has amplitude factor alpha^4 beta^4. With bit j meaning call j
stays, the nonzero signed displacement terms for the bra masks are

    mask:         1   4   5   7   8  11  13  14
    contribution -1  -1  +2  -1  +1  +1  -1  +1.

Their sum is1. All output words and final bath words are recorded in the JSON
certificate and independently checked by the root-retaining path routine.

Therefore a charge-preserving Hermitian perturbation supported on
|0101><1010|+h.c. is outside the pair-supported interface, even though it
preserves total charge. Charge preservation alone does not justify (2).
Small such perturbations of the strictly positive sigma are admissible densities;
the witness is not an inadmissible formal input.

## 7. Executable source, evidence boundary, and receiving use

Run:

    python exact_coefficients.py --output /absolute/path/exact_coefficients.json

The script is standard-library-only and deliberately bounded to k=2..5. It
constructs paired physical histories with exact integer phases and exact rational
prefix contractions. `inherited_representation.py` is copied unchanged from the
actual Cycle7 physical representation. The script's stored hashes identify both
sources. The JSON retains full contracted K2 matrices, every single-deletion
operator, the finite counterexample, observed process timings and peak RSS.

The analytic derivation in Sections2--3 supplies the all-k coefficient identity.
The small exact matrices supply finite counterexamples and an implementation
check. They do not prove a uniform nonlinear norm, a capacity exponent, efficient
encoding, historical priority, or physical usefulness. Discovery/inference/review
cost totals are unknown; runtime of this bounded replay is reported separately.

Receiving use: the principal proof may invoke (2)--(3) with the explicit original
H, then use the independent uniform norm bound and its own positivity, entropy,
root Lyapunov, and arbitrary-reference coding argument. Preserve the actual
single-bath model and fixed-before-horizon quantifiers throughout.
