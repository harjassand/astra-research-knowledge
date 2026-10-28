# Reusable recovery from a low-rank Choi deviation from a known scalar background

2026-10-27. Candidate for independent receiving. Extends the received reusable canonical construction without assuming a known signal spectrum or a spectral gap.

## Contract
A qutrit-input channel E has physical output dimension s and normalized Choi density J of dimension d=3s. Known parameters satisfy
0<=b, 1<=k<=d, ||J||<=L, rank(J-bI)<=k.
Assume some CPTP complete decoder D_* obeys D_* E=G_p exactly, where known p>0 is the accepted identity throughput and G_p has a classical erasure outcome. The learner receives iid normalized Choi copies, each costing one physical query. No unknown purification, eigenbasis, whitening, or source-dependent quantum deployment storage is available. Calibration may use collective measurement.

For 0<nu<=1, a purely classical reusable decoder with training-averaged complete unhalved diamond error <=nu p can be learned using
O((d/L) [1+(kL/(nu^2 p))^2] log(d/(nu p)))
source copies. Constants below are deliberately conservative. The output is a finite decoder SDP solution, not a reusable quantum program.

## 1. Generic bounded-norm operator estimator
Use the independently checked debiased-Keyl moment inequality from canonical_reusable_quadratic_receiver.md:
E Y=J,
E(Y-J)^2 <= [(dL+1)/n0+d^2/n0^2]I.
Since J is a density, L>=1/d. Let n0=ceil(100d/L). Then
E Y^2 <= [1+2/100+1/10000]L^2 I <=2L^2 I.
For any 0<epsilon<=1, clip Y spectrally to [-8L/epsilon,8L/epsilon], obtaining X. Functional calculus gives
||E X-J||<=epsilon L/4,
E(X-E X)^2<=2L^2 I,
||X-E X||<=16L/epsilon.
Averaging t=ceil(64 epsilon^(-2)ln(2d/beta)) independent batches and applying matrix Bernstein therefore gives
||Jtilde-J||<=epsilon L
with failure probability at most beta. Fixed cap is N=t n0. These are precisely the received clipping/Bernstein arguments after rescaling; neither the estimator nor clipping uses J's eigenbasis.

## 2. Threshold the known background, then make a density
Write tau=epsilon L. Diagonalize Jtilde. Replace every observed eigenvalue in [b-2tau,b+2tau] by b and keep the other observed eigenvalues. Call this Hermitian matrix A. Since J-bI has rank at most k and ||Jtilde-J||<=tau, Weyl's sorted eigenvalue inequality implies that at most k observed eigenvalues lie outside [b-tau,b+tau]. Thus rank(A-bI)<=k.

Also ||A-Jtilde||<=2tau, so ||A-J||<=3tau. Replace negative eigenvalues of A by zero to obtain A_+. Since J>=0, the removed negative part has norm at most3tau. Thus
||A_+-J||<=6tau.
The background b is nonnegative; clipping only alters eigenvalues already in the exceptional subspace, so rank(A_+-bI)<=k. Consequently
rank(A_+-J)<=2k,
||A_+-J||_1<=12k tau.
If 12k tau<1, tr A_+>0. Define the density Jbar=A_+/tr A_+. Then
||Jbar-J||_1 <= ||A_+-J||_1+|tr A_+-1| <=24k tau,
and root infidelity is at most delta0:=12k epsilon L by the Fuchs–van de Graaf inequality.

This uses neither a gap at b nor minimum signal eigenvalues. Jbar need not have the channel Choi marginal constraint. The rank bound is only used before trace normalization; no false low-rank claim is made about Jbar-bI.

## 3. Parameters and complete decoder
Set
 epsilon=min(1, nu^2 p/(10^6 kL)), beta=nu p/8.
Then 12k epsilon L<=12nu^2 p/10^6<1, so normalization is valid on the good event. If A_+=0 on a bad event, output any fixed density instead.

Run the received density-only fidelity decoder SDP on Jbar, targeting J_(G_p), with additive objective tolerance delta0=12k epsilon L. Enforce classical accepted/erased output dephasing. The true exact decoder is a feasible comparator. Monotonicity and the Bures triangle inequality give actual recovered root infidelity at most6delta0=72k epsilon L<=72nu^2 p/10^6.

The received rare-throughput lemma gives complete error at most
12sqrt(2p times 6delta0)+12 times 6delta0
 <=(.144+.000864)nu p <nu p/4.
The one-off bad training event costs at most2beta=nu p/4, hence average error is below nu p/2. For all outcomes the deployed decoder is CPTP and is described classically; repeated deployment requires no new source query. Joint multi-use error and one-off bad-training confidence are charged exactly as in the received canonical theorem.

Since L may be supplied as a loose upper bound, replace it by min(L,1) initially if needed; then d/L>=1 and the displayed sample scaling absorbs all ceilings. The algorithm does not require Jbar to be a physical Choi state.

## 4. Unknown-spectrum flat-reset application
Known integers 1<=r<=D, p=r/D, unknown isometry U on C^3 tensor C^D, unknown flag density sigma supported on a known-reference r-dimensional flag subspace before U, with ||sigma||<=C/r for known C>=1. Consider
E_U,sigma(X)=U[p X tensor sigma + Tr(X) I_3/(3D) tensor (I_D-P_r)]U*.
The second term has total mass1-p; for D=r it vanishes. This is exact orthogonal erasure noise, but the success flag spectrum is unknown and may have arbitrarily small or zero eigenvalues.

Its normalized Choi is the output-unitary conjugate of
p Phi_3 tensor sigma + I_9/(9D) tensor (I_D-P_r).
Take d=9D, b=1/(9D), k=9r, and L=min(C/D,1). Then rank(J-bI)<=9r, ||J||<=L, and the exact known-source decoder exists by conjugating U*, checking the code and tracing the flag. The learner does not know this decoder.

The generic theorem yields O(C D^2 nu^(-4) log(D/(nu p))) copies (or a smaller bound if the cap L=1 is active), at fixed relative accuracy quadratic in r/p. No success-spectrum knowledge or minimum eigenvalue is needed. For C constant this preserves the canonical rank/signal exponent while allowing nonflat mixed success flags. The physical reset remains flat on the orthogonal complement; arbitrary reset spectra or entropy-only perturbations are NOT covered.

Dependencies and primaries: canonical_reusable_quadratic_receiver.md; reusable_rare_recovery_infidelity_tomography.md; PSW arXiv:2510.07788, author PDF https://people.eecs.berkeley.edu/~jswright/papers/debiased-keyl.pdf ; Tropp arXiv:1004.4389 Theorem1.4. No historical novelty claim; no efficient collective-measurement implementation is asserted.
