# Exact endpoint response and a uniform operator remainder

Author: `/root/cycle8_weighted_remainder`, 22 October 2026.

## Scope and receiving interface

This is an all-length analytic bound for the unchanged bulk coefficient of the
actual recurrent qutrit device. It does not truncate, reset, or prepare its bath.
It applies to the Cycle7 input observable H, with

    sigma = diag(1/2,1/4,1/4)^(tensor k),
    E_sigma(B) = Tr_A[(sigma tensor I) B],
    G(b) = G0 + b G1 + R_b,  b=beta^2,
    E_sigma[(H tensor I)G1] = v_k I.

The equality at first order and the explicit blocks of H are inherited from
the actual Cycle7 proof, not reproved here. The new statement controls the
exact nonlinear contraction, uniformly on the entire coherent prefix space.
Initial physical bath depths at least k have this finite-prefix coefficient.
The root sector must still be handled by the existing operator Lyapunov and
coding theorem. All estimates below are operator norms, not prefix averages.

Put N=k(k-1)/2 and a=1-b. For every k>=2 and 0<=b<=1 there is a Hermitian
operator polynomial F_k(b) such that

    E_sigma[(H tensor I)G(b)] = b(1-b) F_k(b),
    F_k(0) = v_k I,
    ||F_k(b)-v_k I|| <= N[1-(1-b)^(k-2)] <= N(k-2)b.          (1)

The k=2 right side is zero. In particular the exact contraction of the
old remainder obeys

    ||E_sigma[(H tensor I)R_b]||
      <= b^2 v_k + b(1-b)N[1-(1-b)^(k-2)]
      <= b^2[v_k + N(k-2)].                                  (2)

Thus the contracted remainder is O(k^3 b^2), with explicit constants and
no small-b premise. It is not obtained by applying ||H|| to a global
fourth-derivative estimate.

## 1. Exact two-endpoint selection

Let P_z project onto a complete input binary charge pattern z in {0,1}^k.
Write H=sum_{i<j} H_ij, where H_ij connects only patterns differing by
01 <-> 10 at i,j and identical at every other site. Its block formula,
in the forward orientation z_i=0,z_j=1, is the inherited one:

    P(I-SWAP) if h>d;   P/2 if h=d;   0 if h<d,

with the reverse block its adjoint. Here P is a color-wire unitary between
the two equal-dimensional charge sectors. In particular H_ij is Hermitian
and commutes with sigma.

Expand each physical call as alpha U+i beta I. On a bulk history U flips
the local charge and I preserves it. In a matrix element between input
patterns differing only at i,j, a common output charge word forces both
histories to make the same move/stay choice at every other site. Their
choices at i,j are complementary. This is an exact charge selection rule,
including coherent initial bath vectors and their final overlaps.

Let S be the common set of stays among the k-2 spectator sites. Its scalar
weight in the two-history product is

    w_S(b)=b^|S| (1-b)^(k-2-|S|),

and the two endpoints supply the common factor b(1-b). These weights are
nonnegative and sum to one. The residual signed endpoint operator is
independent of b.

For precision, use endpoint masks m=(m_i,m_j) with m=1 meaning MOVE in
the ket history whose initial charges are (0,1). The bra endpoint mask is
(1-m_i,1-m_j). The two endpoint phases are

    epsilon_00=epsilon_11=-1,
    epsilon_01=epsilon_10=+1.

The common output endpoint charge is 1+m_i-m_j. At fixed S and the fixed
input charge pattern, the spectator output charge is also fixed. Let A_m
be the associated compressed product of two raw unitary histories; each
has operator norm at most one. Unitarity of the physical device with the
spectator calls fixed to U or I gives

    sum_m epsilon_m A_m = 0.

Consequently the spectator output charge plus the constant endpoint charge
one cancels in Q-W*QW. The surviving block is

    K_S = A_01 - A_10,

and has norm at most two. If a stay mask is used instead, the two subscripts
are reversed; the physical operator and all conclusions are unchanged.

Let B_ij^S be this block together with its adjoint, over all charge patterns.
The pattern pairs are disjoint, so

    ||B_ij^S|| <= 2.                                         (3)

Equivalently B_ij^S is the endpoint component of the first bulk coefficient
of the reduced ordered device which skips S, embedded as identity on the
skipped input ports. This equivalence is only a way to identify an operator:
no physical calls are omitted from the actual k-call channel or its cost.

The source/target charge support of H_ij selects just this endpoint component.
Therefore, with

    A_ij,S = Tr_A[(sigma H_ij tensor I) B_ij^S],

the exact identity is

    F_k(b) = sum_{i<j} sum_{S subset spectators} w_S(b) A_ij,S. (4)

Each A_ij,S is Hermitian. For example partial trace cyclicity for the
input-only Hermitian sigma H_ij shows that its adjoint is itself. No
commutation of H_ij with B_ij^S is needed.

This derivation uses the physical history products, not independent output
error probabilities. The positive weights appear only after the exact
two-history charge constraint has eliminated all mismatched spectator
histories. The final bath overlaps remain inside B_ij^S.

## 2. The weighted trace norm of an endpoint input block

On a complete input charge pattern with q colors, the normalized color
weight is the identity divided by 2^q. In the h>d case,

    |P(I-SWAP)| = I-SWAP,
    normalized Tr(I-SWAP) = 1/2.

The first equality follows because P is unitary and I-SWAP is positive.
The two swapped color wires are distinct input qubits. In the h=d case
the absolute value is I/2 and its normalized trace is again 1/2. In the
remaining case it is zero. The reverse offdiagonal block has the same
singular values. Under sigma the combined endpoint charge probability
of 01 and 10 is 1/2. Hence

    ||sigma H_ij||_1 = Tr(sigma |H_ij|) <= 1/4.                (5)

This bound uses the actual H, not only ||H_ij||<=2. For any trace-class
Hermitian input X and bounded joint operator B,

    ||Tr_A[(X tensor I)B]|| <= ||X||_1 ||B||.

To prove it, diagonalize X, take the corresponding input diagonal blocks
of B, and sum their norms with the absolute eigenvalues of X. This also
works on an infinite output Hilbert space. Equations (3) and (5) give

    ||A_ij,S|| <= 1/2.                                      (6)

The proof does not select a bath density, discard coherent prefixes or
normalize a signed branch. It is a full operator estimate.

## 3. The uniform bound

The S=empty weight is a^(k-2). Denote A_ij,empty by A_ij,0. By the exact
Cycle7 certificate,

    sum_{i<j} A_ij,0 = v_k I.

For each pair, (6) and the normalized positive weights imply

    ||sum_S w_S A_ij,S - A_ij,0||
      <= (1-a^(k-2))/2 + (1-a^(k-2))/2
      = 1-a^(k-2).

Summing N pairs proves the first estimate in (1). Bernoulli's inequality
proves its second estimate, uniformly for 0<=b<=1. The identity

    E_sigma[H R_b]
      = b(1-b)(F_k(b)-v_k I) - b^2 v_k I

proves (2). H is input-charge offdiagonal, so E_sigma[H G0]=0.

For arbitrary pair-supported Hermitian K=sum K_ij commuting with sigma,
the same argument gives a reusable interface: replace the 1/4 in (5)
by t_ij=||sigma K_ij||_1, and the right side of the first estimate in (1)
by 4(sum t_ij)[1-a^(k-2)]. A known operator F_k(0), rather than a scalar,
can be used throughout. The constant scalar here comes from the actual
Cycle7 certificate and is not a general property of endpoint operators.

## 4. Consequence for the parent's physical transfer

For the actual Cycle7 input rho=sigma+bX+b^2Y, with

    X=-(ln2/2)sigma H,
    m=3(ln2)v_k/16,
    Y=(4m/k)sigma(Q-k/2),

the diagonal history law gives D_b(Y)=2m(1-b) I exactly in the bulk.
Together with the exact zero drift of sigma, (4) yields

    D_b(rho)=(ln2)b^2(1-b)[3v_k I/8 - F_k(b)/2].             (7)

No generic remainder is charged against sigma. Since v_k>=N/8, (1) gives

    ||F_k(b)-v_k I||/v_k <= 8[1-a^(k-2)] <= 8(k-2)b.

For example, if b(k-2)<=1/64, (7) implies the exact inward drift

    D_b(rho) <= -(ln2)v_k b^2(1-b) I/16.

The parent investigator retains responsibility for positivity, entropy,
parameter selection and the full physical coding theorem. The estimate
shows that nonlinear response need not impose the old b k^4 window;
the existing sufficient positivity scale b k^2 can become dominant.
This contribution alone does not assert a capacity exponent or finite-code
efficiency. The root correction cannot be deleted from the coding bridge.

## 5. What is not proved, and what fails without the premises

The degree-two endpoint selection is essential. A general charge-preserving
input operator may connect patterns differing at four or more sites; those
matrix elements have more complementary move/stay choices and do not obey
the two-endpoint formula (4). An actual four-call witness is the matrix
element with input bra (0,1,0,1), input ket (1,0,1,0), and both initial bath
prefixes (1,2,1,1). The physical-history expansion gives exactly
b^2(1-b)^2, while its G0 and G1 entries vanish. The companion
`../fourth_order_words/exact_coefficients.json` records the eight nonzero
raw path pairs, their identical outputs/final baths, phases, and signed
displacements, whose sum is one. Thus the omitted sector is not merely a
formal possibility or an artifact of a norm estimate.

Likewise at the physical vacuum U need not flip
the local charge because of R. The argument cannot turn into a global root
grading theorem. These are actual scope conditions, not notational choices.

The exact scalar first coefficient does not imply that F_k(b) is scalar.
The independent fourth-order contribution supplies an actual k=4 non-scalar
coefficient witness. Uniform norm control, rather than extrapolated scalar
stationarity, is the receiving operation here.

The skipped-call representation also does not permit replacing the original
H by the optimizer of a shorter block. At k=3 the original-H single-deletion
contractions for deleting positions 0,1,2 are respectively I/8, I/32, I/8,
whereas the two-call optimal value is I/8. The original input-color wire
operator remains in every A_ij,S. The companion exact certificate includes
this finite counterexample as well.

The polynomial coefficients can be read from (4), but this proof does not
use a finite list of such coefficients or a finite matrix check to assert
the all-length bound. No scientific computation was needed for this lemma.
Inference, discovery and review resource totals are unknown.
