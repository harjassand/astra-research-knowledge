# Complete positive-block receiving for signed record flags
30 October 2026. New local proof, not an independent-review receipt.

This closes a norm-composition step. It uses the actual coefficientwise operator family in COEFFICIENTWISE_ROOT_MOMENT_FAMILY.md, not products of marginal expectations. No positivity of a flag is asserted. Quantum DATA is an arbitrary retained input/bath; no quantum consumer Lyapunov factor is included.

## 1. A simultaneous moment norm
Fix a finite remaining-record set R and a designated subset E of records which will be marked later along the component being estimated. Let phi_E be a product of commuting positive phase weights, each >=I. Let Z_j>=I be the rooted factors in their actual time-specific chart. Define

 H_A = phi_E product_(j in A) Z_j,  A subset R.

All these observables commute with one another and the current cuts. They need not commute with the actual state. Choose M>=1. For any trace-class X, including an arbitrary retained reference, define ||X||_(E,R;M) as the infimum of C such that there exist positive Y_L,Y_R with

 [[Y_L,X],[X^dagger,Y_R]] >=0,
 Tr(H_A Y_L), Tr(H_A Y_R) <= C M^|A| for EVERY A subset R.       (P1)

The infimum can be replaced by arbitrarily close feasible envelopes. If X=PXP for the remaining good-cut projection P and all tests commute with P, replace both envelopes by P Y_L,R P. Positive-block feasibility is preserved and every moment decreases. Thus all envelopes used for a good-basin witness can and must be taken on that corner. This is a norm: homogeneity uses reciprocal scaling of the block rows, triangle inequality uses addition of positive blocks, and H_empty>=I implies ||X||_1<=C. The last fact follows from the positive-block factorization X=Y_L^(1/2) K Y_R^(1/2), ||K||<=1. Reference stabilization defines the corresponding complete norm. This definition does not presume one envelope separately optimized for each A: the SAME pair must work for all A.

For positive X, the choice Y_L=Y_R=X shows the maximum normalized moment is an upper bound. Conversely diagonal block positivity and Cauchy--Schwarz imply each such moment of positive X is at most C. Thus the norm on positive X equals max_A M^(-|A|) Tr(H_A X).

## 2. Actual CP intervals preserve the same envelope
Suppose an actual CP, possibly trace-decreasing propagator T obeys

 T^* H_A,out <= g sum_(B subset R) c_(A,B) H_B,in,
 c_(A,B)>=0, sum_B c_(A,B) M^|B| <= M^|A|.                    (P2)

Apply T, with an identity on the two-dimensional block index, to (P1). Its two positive diagonal images are simultaneous envelopes for T(X). Every output moment is <=g C M^|A|. Hence the complete induced norm is <=g. No dimension or number-of-subsets factor occurs.

The coefficientwise affine family in the preceding note gives exactly (P2): c_(A,B) is product a_j over B and b_j over A\B, with b_j<=(1-a_j)M. A phase integrating factor supplies g. Exact copy/graph endpoint pullbacks that decrease each H_A also satisfy (P2). Complete-loss compression is allowed because it is CP and because its actual diagonal-metric inequalities were established on the cut corner.

## 3. One cross map with simultaneous weight inequalities
Let C(X)=U X V^dagger, permitting auxiliary Stinespring output spaces. Suppose for every output index A there is an allowed incoming index i(A) with |i(A)|=|A| and

 U^dagger H'_A U <= alpha^2 H_i(A),
 V^dagger H'_A V <= beta^2 H_i(A).                            (P3)

Then diag(U,V) maps a feasible block in (P1) to a positive block. Its diagonal moment bounds are alpha^2 C and beta^2 C. Multiply the first diagonal envelope by beta/alpha and the second by alpha/beta; reciprocal scaling preserves block positivity and leaves the cross X unchanged. This gives

 ||C(X)||_out <= alpha beta ||X||_in.                         (P4)

Zero coefficients follow by a limit. Sums of cross maps use the triangle inequality. Partial trace over an auxiliary space preserves the bounds. The SAME U,V and diagonal envelopes work for every A; separate weighted trace-norm estimates would not establish this lemma.

## 4. Local flags satisfy the simultaneous inequalities
Use E as the set of FUTURE marks; take only a fixed terminal marked set D when estimating v_D, so E shrinks as those marks occur. All other selected records U=S\D carry only their rooted factors. The family may be indexed by all remaining R, but no phase weight is needed on U.

For a new mark set J subset E, drop phi_J and remove J from R. An elementary ket/bra term of Gamma_(J|past) has at least one source-strip projector for every j in J. Each such projector lies where its phase weight >=B_j. In the actual common diagonal/PRE chart, all cut/strip/projector weights commute. For unaffected record factors the weights cancel. A bounded-leg local system operator changes each touched rooted factor by at most its fixed orbit ratio, uniformly in the subset A; at most q' records are touched. The phase-weight local ratio is likewise fixed. Therefore (P3) holds with

 alpha beta <= C_local product_(j in J) B_j^(-1/2),           (P5)

uniformly for EVERY A subset R\J. A record violating on both sides improves the power. The incoming index is simply the SAME A; there is no M^|J| factor from dropping root factors. Source-strip information belongs on the corresponding ket or bra, not on an invented positive event.

For an actual bath-coupled local HP superoperator, use its finite SYSTEM matrix-unit expansion. The coefficients are normal completely bounded bath maps, with total cb norm bounded by a fixed system-dimension multiple of the supplied incident-cb norm. Each bath map has a 2-by-2 completely positive dilation with diagonal effect norms bounded by its cb norm (the standard completely-bounded-map factorization). Those diagonal maps commute the system-only H_A. Applying the block argument to this dilation gives the same simultaneous bound. Constants depend on the fixed system-leg dimension, not bath dimension. This is not a Choi/Kraus expansion whose number of terms grows with the bath dimension. For infinite baths retain the source contract's normality/dilation hypothesis; no stronger analytic extension is claimed here.

The continuous source-strip and incidence bounds are exactly those already used in ROOT_SPECTRAL_FLAG_EXPANSION.md. Thus that proof's local estimate upgrades to this norm, rather than being extrapolated from one positive input.

## 5. Endpoint maps, including PRE to POST
At a growth endpoint, let incoming phase A_j and outgoing phase B_j obey B_j<=A_j, with the failed-new-cut pullback Q_j satisfying P_old Q_j<=P_old A_j/b_j. Let outgoing rooted-factor pullbacks be no larger than the incoming rooted factors. For each unmarked record use the good-cut leg and the actual pullback; (P3) holds with coefficient1. For newly marked j the phase factor is dropped, and one ket/bra leg has coefficient b_j^(-1/2). Summing QXQ,QXP,PXQ gives a factor3 per marked record. This proves the reviewed two-metric endpoint bound in the simultaneous norm, including the opposite-consensus case detected by the PRE weight. The actual noisy PRE propagator must precede this endpoint; it cannot be skipped.

## 6. Receiving the actual seed
The reviewed genuine-classical seed has uniform JOINT effect inequalities for products of defect cones and weights. For a fixed initial ket/bra sector pair, use the two positive diagonal maps from its common Stinespring dilation as Y_L,Y_R. The same mixed defect/weight expansion bounds all their moments simultaneously. Reciprocal scaling gives the per-initial-mark factor 3 sqrt(p_seed), while future phase factors cost at most A_seed per record. Set M>=A_seed for root-only factors. This constructs one feasible pair for the whole family, not a separate Cauchy--Schwarz witness for each subset. All constants are uniform conditional on the genuine historical outcome m and arbitrary retained DATA/bath/reference.

## 7. What has and has not been proved
The signed triangular expansion can now be propagated and summed in a norm which retains all rooted subset moments. The exact D-dependent generating-function argument and geometric prefix cost apply with the same per-mark barriers. This is a receiving lemma for actual scheduled atomic capture once the reviewed phase/root/seed inequalities are supplied.

It does not yet prove the long-time final-retention inequality, a quantum DATA consumer bound, native two-site acquisition, or a detector's external output guarantee. A separate note must instantiate retention and extract the positive distribution of PHYSICAL PORT errors from the signed components. The signed components themselves never become probabilities.
