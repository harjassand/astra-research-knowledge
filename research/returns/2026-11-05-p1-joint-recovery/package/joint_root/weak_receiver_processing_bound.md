# A general processing-strength obstruction for weak causal readers

5 November 2026. This continues the same homogeneous tracial partial-SWAP
problem. The inaccessible-environment observable and martingale argument were
constructed by the independent algebraic branch in
`joint_algebra/coherent_flag_audit.md`. This extension replaces that crossed
filter by an arbitrary carrier-dependent isometry close to a receiver-only
isometry. It is a processing principle, not the optimal memory-width law.

## Physical scope

The source collision is U=cI+is SWAP, 0<theta<pi/2. Purify each fresh thermal
carrier E_j by an inaccessible F_j in the normalized Bell state Phi_EF.
Dilate each examined receiver step as W_j:M_j E_j -> M'_j E_j, including all
retained flags, buffers and initialized workspace in M'. The designated spent
E_j is discarded. Suppose some receiver-only isometry V_j:M_j->M'_j satisfies

  ||W_j - V_j tensor I_E|| <= delta_j.

This condition is on the full physical Stinespring update, uniformly over
classical histories, not on a marginal or a postselected branch. Arbitrarily
strong retained-register controls and feedback may be included in V_j.
Any other discarded local receiver environments can be retained in a converse
relaxation, strengthening the receiver. Coherent copies of classical histories
can likewise be included. A swap into a raw carrier buffer, a strong incoming
measurement, or another operation not satisfying this bound is outside this
restricted class; all remain allowed in the original full question.

## Environmental witness

Set O_j=i[Z_Ej,Phi_EjFj], with ||O_j||=1. These commute for distinct j. Write
u_theta=||U-I||=2sin(theta/2). Suppressing j, put

  Q=W^dagger O W - I_M tensor O,
  B=<Phi_EF|Q|Phi_EF>.

Isometricity gives ||Q||<=2delta and ||B||<=2delta. Direct expansion of the
partial SWAP gives the exact identity

  <Phi_EF|U^dagger O U|Phi_EF> = cs Z_S.

The c^2 and s^2 terms vanish; the cross term is cs Z_S. Hence the effective
pre-collision observable satisfies

  A=<Phi_EF|U^dagger W^dagger O W U|Phi_EF>=cs Z_S+B+R,
  ||R||<=4delta u_theta,
  ||A||<=h_j:=cs+2delta_j+4delta_j u_theta.

The remainder is the Bell expectation of U^dagger Q U-Q, bounded by
2||U-I|| ||Q||. No differentiability of W_j as a function of theta is assumed.

## Exact finite-parameter leak and error bound

For logical inputs |0><0| and |1><1|, the source polarizations after k
collisions are exactly +/-c^(2k), independently of every receiver action.
The all-receiver acquisition ledger gives, for any receiver observable B,

  |Tr B [E_j(|0><0|)-E_j(|1><1|)]|<=2||B|| sqrt(3a_j),
  a_j<=1-(1-s^4)^j<=j s^4.

Examine n consecutive weak-reader steps after any k preceding collisions.
The preceding receiver operations may be arbitrary. For the sum of the
environmental measurement outcomes,

  Delta:=E_+(sum O_j)-E_-(sum O_j)>=B_weak,
  B_weak=2cs c^(2k)(1-c^(2n))/s^2
       -4sqrt(3)s^2 sum_(j=1)^n delta_j sqrt(k+j-1)
       -8u_theta sum_(j=1)^n delta_j.

Put H=sum_j h_j. Conditional on previous converse measurements, each fresh
Bell pair is still independent and its conditional mean is at most h_j in
absolute value. The sum of martingale differences has second moment at most
n; the predictable drift has magnitude at most H. Thus the sum of the two
input second moments is at most 4n+4H^2. Weighted Cauchy-Schwarz for the two
classical distributions yields

  D_env >= [max(B_weak,0)]^2 / [8(n+H^2)].

If final half-diamond recovery error is at most epsilon, Bell fidelity is at
least 1-epsilon. Purification and Uhlmann's theorem make the complementary
Choi state within trace distance sqrt(epsilon) of a product with the logical
reference. Measuring that reference in the z basis and using the triangle
inequality gives D_env<=2sqrt(epsilon). Therefore every continuation obeys

  epsilon >= [max(B_weak,0)]^4 / [256(n+H^2)^2].       (FINITE)

This is a finite-parameter bound, with no exchange of growing-prefix limits.
The receiver is never given access to the environmental witness.

The same proof works for a predetermined subset J of examined steps within
the first T collisions. Replace n by |J|, H by sum_(j in J)h_j, and B_weak by

  2cs sum_(j in J)c^(2(j-1))
   -4sqrt(3)s^2 sum_(j in J)delta_j sqrt(j-1)
   -8u_theta sum_(j in J)delta_j.

All other steps may use arbitrary strong processing or raw retention.
A subset chosen using a hidden input-dependent classical history is not
covered by this deterministic-subset statement.

## Weak-angle consequence

Let delta_j<=kappa theta, with fixed finite kappa, and let the stream extend
through n=floor(alpha/theta^2), with fixed alpha>0. For k=0,

  theta B_weak ->2(1-exp(-alpha)),
  limsup theta H <=alpha(1+2kappa).

The negative terms in B_weak are O(1); the positive term is order 1/theta.
The exact finite bound therefore proves, regardless of memory dimension,

  liminf_(theta->0) epsilon >=
    (1-exp(-alpha))^4 /
    [16 alpha^2 {1+alpha(1+2kappa)^2}^2] >0.

A uniformly weak carrier-coupled reader that discards each spent carrier
cannot achieve arbitrarily accurate acquisition, even with all flags
coherent, arbitrary initialized workspace and classical feedback.
The conclusion is compatible with nonzero accessible information in a
fixed-memory weak-angle limit: it is an error floor, not a claim that all
such readers acquire zero information.

If the arbitrary preceding prefix satisfies k theta^2->beta<infinity, the
numerator acquires the factor exp(-4beta). Use (FINITE), not this limiting
expression, if beta or kappa diverges.

For a predetermined weak-step subset with |J|theta^2->f alpha within the
first floor(alpha/theta^2) collisions, bounding each source polarization
below by c^(2T) instead gives

  liminf epsilon >= f^2 alpha^2 exp(-4alpha) /
             [16{1+f alpha(1+2kappa)^2}^2].

Thus a fixed positive fraction of uniformly weak discard steps in the initial
diffusive window prevents vanishing error even if every other step is
arbitrarily strong. Strong processing is a necessary escape from this class;
the theorem does not say that it is sufficient for recovery.

## Interaction action and scope

In an interaction picture removing receiver-only controls, Duhamel's estimate
gives delta_j<=integral ||H_int(t)||dt (hbar=1). The theorem consequently
applies to a uniform carrier-coupling action budget O(theta). It does not give
a universal gate or service-time bill without specified strength and locality
constraints. Passive retention is not a weak discarded-carrier update merely
because no active gate was used: the retained physical carrier counts as
quantum memory and is not the designated discarded E in this theorem.

The unrestricted joint memory/processing law is still unresolved. This
result excludes a broad mechanism without assuming a tracial receiver,
discarding coherent histories, or changing the source.
