# Exact law for independent covariant physical preprocessing

Continuation of the fixed homogeneous tracial partial-SWAP problem, 5 November 2026.
This is a new extension of the accepted flagged-erasure calculation, not a solution
of arbitrary causal coherent compression. All earlier crossing/instrument/loss
proofs remain unchanged. Petz composition and the sharp fidelity comparison are
existing machinery (Petz; Renes, PRA 96, 042328 (2017), Eq. 13).

## Model and scope

Each emitted qubit is independently processed by a physical channel L_j from a
qubit to any finite quantum-classical output B_j. Its independent initialized
ancillas and any classical outcomes are part of this CPTP map. It does not act on
earlier quantum outputs. The resulting B_j are available for arbitrary collective
final decoding. This includes coherent processing followed by discard within each
individual carrier, and is more general than deleting a carrier before access.
It does not include a shared persistent coherent receiver register or feedback
between these maps.

Write tau=I/2, sigma_j=L_j(tau), and let R_j be the Petz channel for this reference,
with any trace-preserving extension off the support of sigma_j. Suppose

  R_j L_j = Delta_{lambda_j},   0 <= lambda_j <= 1,

where Delta_lambda fixes identity and multiplies the three Paulis by lambda.
SU(2) covariance of L_j, including covariance on recorded classical outcomes, is a
sufficient condition: its Petz composition is covariant, bistochastic, self-adjoint
and positive as a Hilbert-space operator, hence has precisely this form.
The theorem only needs the displayed Petz-composition premise, not a particular
covariance implementation.

Set c=cos(theta), s=sin(theta). Starting with a_0=0, q_0=1, define

  a_j = a_(j-1) + lambda_j s^4 q_(j-1),
  q_j = (c^4 + 2 lambda_j c^2 s^2) q_(j-1).

For E=(tensor_j L_j) C_N, its physical Petz decoder is

  R_E = D_N (tensor_j R_j),

where D_N is the accepted mixed-dummy inverse collision circuit, in reverse
chronological order. Exactly,

  R_E E = a_N id + (1-a_N) R_tau.

Thus the half-diamond error of this operation is 3(1-a_N)/4. Every decoder,
including collective initialized quantum computation on all B_j, obeys

  epsilon_opt >= (3/4)(1-sqrt(a_N)).

These upper/lower errors differ by at most a factor two.

## Proof

The all-output acquisition channel C_N sends tau to the tracial bath state
tau_E. The product preprocessor sends tau_E to tensor_j sigma_j. Substitution in
the Petz formula gives R_E=R_C (tensor R_j)=D_N(tensor R_j). In particular,

  R_E E = D_N (tensor Delta_lambda_j) C_N.

Let J_N(X)=U^(N)(X tensor I_E)U^(N)* in normalized Hilbert-Schmidt spaces, and let
P be the orthogonal projection onto source-identity operators. The last display
is the weighted Gram operator

  J_N* P (id_S tensor tensor Delta_lambda_j) P J_N.

To compute it, propagate a logical traceless operator while applying the
positive Hilbert-space square root of Delta_lambda_j on each newly emitted
carrier. Each such operation commutes with all later source collisions and
with P. Split the current operator as a source-identity part PZ and a
source-traceless part QZ. The old PZ is unchanged on adding an identity carrier.
For every source-traceless term X tensor A_old, the collision produces three
orthogonal terms, whose squared normalized norms are

  c^4 ||X tensor A_old||_2^2           (source traceless, new carrier identity),
  s^4 ||X tensor A_old||_2^2           (source identity, new carrier traceless),
  2 c^2 s^2 ||X tensor A_old||_2^2    (source and new carrier traceless).

The last equality follows directly by expanding i c s [SWAP,X tensor I].
All cross terms vanish, including arbitrary old-bath coefficients and different
logical Pauli components, by normalized trace and polarization. The square root
of Delta_lambda multiplies each new-carrier-traceless term by sqrt(lambda).
The emitted source-identity contribution is orthogonal to the old PZ, which has
identity on the new site. Hence their squared norms follow precisely the two
recurrences. Initially PZ=0 and ||QZ||_2^2=||X||_2^2. Polarization gives a_N id
on the entire traceless qubit space, while identity is fixed. This proves the
channel equality including all inaccessible reference correlations.

The half-diamond formula for depolarization is exact. Renes's inequality
F_P >= F_opt^2 + (1-F_opt)^2/3 with F_P=(1+3a_N)/4 gives
F_opt <=(1+3 sqrt(a_N))/4, proving the converse via the Bell input.

## Homogeneous preprocessing and the joint quantifiers

For lambda_j=lambda, let f=c^4+2 lambda c^2 s^2. Then

  a_N = lambda s^4 (1-f^N)/(1-f),
  a_infinity = lambda s^2/[s^2+2(1-lambda)c^2].

For 0<epsilon<3/4 put A=(1-4epsilon/3)^2. A necessary condition even with
unbounded collision count and unrestricted final decoding is

  lambda >= A (1+c^2)/(s^2+2 A c^2).

Equivalently,

  1-lambda <= (1-A) s^2/(s^2+2 A c^2).

A strict sufficient condition allowing finite collision count is the analogous
inequality with A replaced by B=1-4epsilon/3, because the explicit decoder then
has asymptotic error strictly below epsilon and its finite-count excess is
(3/4) a_infinity f^N. The exact finite N requirement is

  (3/4)[1-a_infinity+a_infinity f^N] <= epsilon.

Consequently, for simultaneous high accuracy and weak angle, the admissible
local Petz loss 1-lambda is of order epsilon theta^2. For lambda fixed below
one, epsilon_opt tends to 3/4 as theta tends to zero, even allowing N to grow
arbitrarily. If 1-lambda=kappa theta^2, a_infinity tends to 1/(1+2kappa).
These are uniform finite-formula deductions, not a fixed-angle assertion.

Examples: flagged erasure with retention p has lambda=p, reproducing the prior
exact loss law. An unflagged depolarizing map of visibility v has lambda=v^2,
so it has a different physical interpretation and a different tolerance when
expressed in v. General local CPTP preprocessing with the same Petz composition
has the same recovery curve; its discarded environments need not be erasures.

## A paid-storage implication, with its exact limitation

For a quantum-classical output L(tau)=direct_sum_x p_x sigma_x, define
h_Q=sum_x p_x S(sigma_x), in bits. Let e=3(1-lambda)/4. The recovered Bell state
is isotropic with coherent information 1-h_2(e)-e log_2(3). Data processing of
coherent information under the Petz decoder and nonnegativity of conditional
branch entropies imply

  h_Q >= 1-h_2(e)-e log_2(3).

Indeed I(R>B)_Choi <= sum_x p_x S(sigma_x), while I(R>B) is at least the
coherent information after recovery. The carrier average inputs are exactly
product tracial, so independent preprocessing also has a product average output.
Thus a strategy which faithfully stores these preprocessed quantum outputs by
ordinary source compression has rate near one qubit per carrier when high
acquisition fidelity requires 1-lambda=O(epsilon theta^2).

This last statement is NOT a lower bound on every task-specific coherent
compression of the B_j: such a compression may exploit correlations with the
one logical payload instead of faithfully storing all B_j. Nor is h_Q by itself
a one-shot peak-register dimension. This distinction is the remaining central
operation and must not be erased from a final account.
