# Anchored reference filtering: a strict high-noise payment

26 October 2026. This is an asymptotic guard for the accepted-only GLS comparison, not a proof of that comparison at finite noise.

Fix d>0, A0>0 on C3 and an invertible reference filter Z. Write k=lambda_min(Z*Z)>0 and

 S_s=3d P_Phi+I3 tensor (s A0),
 S_s^Z=(I3 tensor Z)S_s(I3 tensor Z*).

The proposed anchored inequality is Delta(S_s^Z)>=k Delta(S_s). It is not inherited from generic reference-filter monotonicity, which is false on nonmaximally entangled pure sources. Nevertheless this inequality is strictly received for all sufficiently large s whenever Z*Z is nonscalar.

## 1. High-noise quadratic coefficient

Let E(X)=I3/3 tensor Tr_phys X and B=I3 tensor A0. The deficit and its first variation vanish at every reference-only positive baseline. On such a baseline, physical identity and physical-traceless directions are orthogonal in the BKM metric

 g_B(H)=integral Tr[H(B+t)^(-1)H(B+t)^(-1)]dt.

WH3 fixes the former and multiplies the squared metric of the latter by1/4. Consequently, with

 H=3d(P_Phi-I9/9),

 Delta(S_s)=(1/(4s))g_B(H)+O(s^(-2)).

The same expansion holds after the fixed reference filter, because physical E commutes with it:

 Delta(S_s^Z)=(1/(4s))g_(ZBZ*)(ZHZ*)+O(s^(-2)).

Here Z on a joint matrix abbreviates I3 tensor Z. All dimensions and positive baselines are fixed, so ordinary entropy Taylor expansion receives the remainder.

## 2. Actual inverse-filter channel and quantitative BKM payment

The reference operator K=sqrt(k) Z^(-1) is a contraction. Complete its success branch to the deterministic CPTP map

 Lambda(T)=K T K* direct_sum Tr[(I-K*K)T]|fail><fail|.

Apply id_phys tensor Lambda to the filtered baseline and tangent. The success branch is exactly kB,kH. Put

 F=Z*Z-kI>=0.

The rejection baseline is beta I3, beta=Tr(A0 F), and the rejection tangent is

 H_rej=d[F^T-(TrF/3)I3].

BKM data processing (equivalently the second variation of relative-entropy DPI) and direct-sum additivity give

 g_(ZBZ*)(ZHZ*) >= k g_B(H)+g_(beta I3)(H_rej).

For nonscalar Z*Z, F is nonzero, beta>0, and

 g_(beta I3)(H_rej)
 = d^2 Tr[(F-(TrF/3)I3)^2]/Tr(A0 F)>0.

The strictness uses min eigenvalue F=0: a scalar F would therefore be zero, corresponding precisely to Z*Z=kI.

Thus the exact asymptotic lower payment is

 lim_(s -> infinity) s[Delta(S_s^Z)-k Delta(S_s)]
 >= (d^2/4) Tr[(F-(TrF/3)I3)^2]/Tr(A0 F)>0.

If Z*Z=kI, reference-unitary invariance and homogeneity instead give equality for every s.

## Scope

This covers arbitrary noncommuting A0 and Z; it is not a diagonal-fixture diagnostic. It excludes sufficiently high-noise counterexamples to the anchored comparison for every fixed nonscalar filter. The threshold is source-dependent; no uniformity near singular A0 or scalar-filter degeneracy is asserted. The theorem does not pay the finite pure/noise interaction, generic reference-filter monotonicity, or an arbitrary original-source postprocessing inequality.

## Differential rank-one expansion (new local-score addendum)

The same DPI argument receives a genuinely differential guard. Let
X_s=P_psi+s I3 tensor A0, A0>0, with arbitrary fixed psi. For a unit
reference vector v set a=<v,A0v> and chi=(I tensor <v|)psi. Define the
reference-congruence score at the identity by

 Q_v(s)=d/depsilon Delta[(I tensor Z_epsilon)X_s(I tensor Z_epsilon)]|0,
 Z_epsilon=I+(sqrt(1+epsilon)-1)P_v.

Then

 lim_(s->infinity) s Q_v(s) >= ||chi||^4/(6a).        (D1)

In particular the score is strictly positive for sufficiently high noise
whenever chi!=0. This does not require v to be a Schmidt eigenvector.

To prove it, let B=I tensor A0 and H=P_psi-I3/3 tensor psi_R.
The uniform local entropy expansion is

 Delta(X_s)=g_B(H)/(4s)+O(s^-2).

It is C1 in epsilon on a fixed neighborhood of zero because the baseline
is faithful there. Apply the exact inverse-filter CPTP map to the filtered
baseline and tangent. Its success branch is B,H. Its rejection branch is

 epsilon a I3,
 epsilon M,   M=chi chi*-(||chi||^2/3)I3.

Consequently BKM DPI gives the finite-epsilon inequality

 g_(Z_epsilon B Z_epsilon)(Z_epsilon H Z_epsilon)
 >=g_B(H)+epsilon Tr(M^2)/a.

Differentiate from epsilon>=0 at zero (the metric is smooth) and use
Tr(M^2)=2||chi||^4/3, yielding (D1). The high-noise threshold is
source-dependent; no uniform assertion through singular A0 or chi=0 is
made. This is stronger than the earlier finite anchored-gap calibration
only as a local derivative statement, not a proof at finite noise.
