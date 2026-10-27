# Quantitative Jensen representation for Schmidt-rank-two main and isotropic physical reset

Status: exact positive decomposition; independent audit pending. VALUE COVERAGE IS ALREADY RECEIVED in `wh3_physical_two_plus_one_block_entropy_theorem.md`, which allows arbitrary physical2+1 blocks. This note supplies a shorter explicit quantitative lower representation, not new value coverage. Reference dimension is arbitrary and no TP or commutation hypothesis is used.

Let psi in C3 tensor R have Schmidt rank at most2, and let A>=0 be any finite-dimensional reference operator. Define

X=|psi><psi|+I3 tensor A,
H=Tr_physical |psi><psi|.

Then the homogeneous WH3 deficit obeys the explicit bound

D(X)>=f(A)+3f(A+H/3)-4f(A+H/4)>=0.                  (1)

It is strictly positive if psi!=0. For psi=0 the source is reset-only and the deficit is0. This receives, in particular, all rank-deficient filtered qutrit-reset seeds, including noncommuting reset and Schmidt Gram. It does not compare their value to an unfiltered seed.

## 1. Exact physical output acquisition

A physical unitary places psi in an active two-dimensional physical plane. Put

M_t=I2 tensor A+t |psi><psi|, t>=0.

The input spectrum is that of M_1 direct-sum A. The reference marginal is3A+H. The WH output spectrum is that of

M_(1/2) direct-sum(A+H/2).                           (2)

Indeed on the active physical plane, the map X -> Tr(X)I2-X^T is unitary conjugation by the fixed antisymmetric qubit matrix J=[[0,-1],[1,0]]. Thus the active WH block is I2 tensor A+(J tensor I)|psi><psi|(J* tensor I)/2, unitarily equivalent to M_(1/2). The unused third physical output block is A+H/2. There are no off-block terms because psi has no third physical component. This is an exact source spectrum statement, not a partial-transpose entropy assumption.

Using f(3A+H)=3f(A+H/3)+Tr(3A+H)log3 cancels the deficit's trace-log3 normalization. Consequently

D(X)=J_in+3f(A+H/3)-2f(A+H/2)-f(A),
J_in=f(M_1)-2f(M_(1/2))+f(M_0), f(M_0)=2f(A).

## 2. Relative-entropy data processing pays the negative marginal gap

J_in is the midpoint Jensen gap for f, equivalently the sum of the two generalized relative entropies from M_1 and M_0 to their midpoint. Partial trace over the active physical qubit is CPTP and sends these three matrices to2A+H,2A,and2A+H/2. Relative-entropy data processing therefore gives

J_in>=f(2A+H)-2f(2A+H/2)+f(2A).

This holds for unnormalized positive operators: their individual traces are preserved by the partial trace, and the classical mass terms in the relative-entropy representation cancel. Singular matrices follow by common positive regularization and continuity of the finite entropy gaps.

Expand the factors2 in the last display. Their trace-log2 terms cancel exactly, giving

J_in>=2f(A+H/2)-4f(A+H/4)+2f(A).

Substitution proves the first inequality in(1).

## 3. Final Jensen payment and strictness

Since

A+H/4=(1/4)A+(3/4)(A+H/3),

trace convexity of xlogx gives the second inequality in(1). Strict convexity gives a strict final gap whenever H!=0. The pure endpoint A=0 yields the sharp lower payment Tr(H)log(4/3); equality in that lower bound holds for every pure main of Schmidt rank at most2: on the rank-two probability-simplex boundary the two scalar entropy sums cancel exactly.

No inverse-floor or faithful-reset assumption is needed. This differs from the aligned CQ-dilation theorem: here the pure Schmidt rank is restricted but the reference reset is arbitrary and may fail to commute with H. The former allows full Schmidt rank but requires alignment.
