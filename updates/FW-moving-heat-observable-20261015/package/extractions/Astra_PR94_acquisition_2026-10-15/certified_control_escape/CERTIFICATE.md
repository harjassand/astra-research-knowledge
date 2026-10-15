# A data-dependent, finite-noise scalar prediction certificate

This is a constructive sufficient certificate, not a universal query-complexity theorem or physical demonstration. It uses the scalar model and exact reconstruction identities in ../N854_SOURCE_PROOF.txt; the exponential finite-noise obstruction in noisy_control_obstruction/THEOREM.md remains intact.

## 1. Precisely what is supplied

Assume a fixed real linear plant with calibrated additive rank-one controls,
A(u)=A+P diag(u) P^T, f(u)=c^T A(u)^(-1)b, 0<=u_i<=U.
Linearity, fixed source/detector, actuator independence and calibration, actual control amplitudes, settling, drift bounds, and reproducible reset are supplied or separately established. These are not certified by a finite scalar response table. Also assume sym(A)>0 when using physical passivity to motivate existence of the certificate. Calibration must keep the same plant throughout.

For w_i=(P^T A^(-1)b)_i nonzero, gauge reduction gives
f(u)=f0-a^T T_H(D)1, T_H(D)=D(I+HD)^(-1).
Here H=W^(-1)Hphysical W, Hphysical=P^T A^(-1)P, W=diag(w), and a_i=v_i w_i.

The acquisition below initially also requires intervals excluding zero for a_i and the singleton/pair inversion denominators. If these fail it reports an inconclusive result, refines measurements when permitted, or uses a different acquisition/model-fitting method. Zero discriminants, however, need NOT force failure.

## 2. The uniform operator lemma

For positive diagonal Λ define ||x||Λ=sqrt(x^TΛx), ||M||Λ=||Λ^(1/2)MΛ^(-1/2)||2, and ||a||Λ^-1=sqrt(a^TΛ^(-1)a).
Suppose
(H^TΛ+ΛH)/2 >= hΛ, h>=0.
Then, simultaneously for every 0<=D<=UI,

  ||T_H(D)||Λ <= M(h,U):=U/(1+hU).

For U=0 the response is identically f0. For U>0 and D>0, transform H by Λ^(1/2), which commutes with D. Since T_H(D)=(D^(-1)+H)^(-1), the transformed inverse has symmetric part of its pre-inverse at least (1/U+h)I. Cauchy-Schwarz applied to x^T(D^(-1)+H)x proves the inverse bound. For zero entries in D, restrict to its active principal submatrix; T is zero off the active rows/columns and equals (D_active^(-1)+H_active)^(-1) on that block. The same proof applies. Equivalently use continuity.

Thus no minimum nonzero control amplitude enters. The bound is <=U and, for h>0, <1/h. Invertibility for the whole cube follows as part of the same argument.

For two such models H and Hhat, direct multiplication, or the resolvent identity on positive D followed by continuity, gives

  T_H(D)-T_Hhat(D)=-T_H(D)(H-Hhat)T_Hhat(D).

## 3. A finite, independently checkable certificate

Suppose acquisition has enclosed at least one response-equivalent true representation in
|f0-fhat0|<=e0, ||a-ahat||Λ^-1<=ea, ||H-Hhat||Λ<=eH.
No statistical independence among these parameter errors is needed.

Find a diagonal Λ>0 and hhat>=0 such that

  (Hhat^TΛ+ΛHhat)/2 >= hhat Λ,
  h:=hhat-eH>=0.

Then every member of the H enclosure is weighted accretive with margin h. Put Mtrue=M(h,U) and Mcenter=M(hhat,U). Uniformly on the entire cube,

  |f(u)-fhat(u)| <= e0
    + ea Mtrue ||1||Λ
    + ||ahat||Λ^-1 Mtrue Mcenter eH ||1||Λ.          (C)

Proof: expand a^T T_H-ahat^T T_Hhat as (a-ahat)^T T_H + ahat^T(T_H-T_Hhat), then use the operator lemma and the dual weighted vector norm. Replacing Mcenter by Mtrue is a slightly looser valid bound, used in the numerical receipts below.

This is an a posteriori certificate: stop as soon as its right-hand side meets the requested error, even if directed-edge orientation is unresolved. For approximate minimization/maximization, optimizing fhat to additive tolerance κ gives true regret <=2(C)+κ. Global optimization cost is separate; this certificate does not solve it.

### Obtaining Λ without a free oracle

Search for Λ=diag(λ_i), λ_i>0, with normalization sum λ_i=m, by a diagonal Lyapunov feasibility SDP. For a fixed trial hhat the inequalities are linear in λ_i; bisection over hhat is permitted. Strict positivity can be imposed with λ_i>=ell>0, reducing ell if needed. Numerical SDP output is only a candidate. Rationalize its diagonal and verify the displayed matrix inequality with exact rational LDL decomposition, principal-minor methods, or rigorous interval eigenvalue bounds. Gershgorin bounds often suffice. If no candidate verifies, the certificate is inconclusive; do not infer the plant is nonpassive.

For entrywise H intervals about Hhat with radii E_ij, a directly computable bound is
  eH <= sqrt(sum_ij (λ_i/λ_j) E_ij^2).
For a radii A_i,
  ea <= sqrt(sum_i A_i^2/λ_i).
Round these upper bounds outward. All proof checks can be rational, replacing square roots with rational upper bounds. Poor diagonal scaling and gauge conditioning are thereby visible in the certificate.

Physical existence is motivation, not free information: sym(A^(-1))=A^(-T)sym(A)A^(-1)>0, hence sym(Hphysical)>=0, strictly if P has full column rank. The original gauge has Λ=W^2. For the response-equivalent weighted transpose Hstar=R^(-1)H^T R, R=diag(a), write V=diag(v); Hstar=V^(-1)Hphysical^T V and Λ=V^2 works. These weights are generally unknown and must be found/verified, not assumed accessible. Real nonzero w_i and a_i make both diagonal weights positive even when the port entries have signs.

## 4. Safe acquisition with intervals and optional separation

Each actual scalar reading supplies a certified interval Y_q. Use exact rational/outward-rounded interval arithmetic, retaining dependencies when convenient but never relying on them without proof.

1. Measure the baseline and two singleton levels t1!=t2>0. Apply N854's rational singleton formulas to intervals; require denominators and a_i to exclude zero.
2. Measure two settings per pair. Apply its formulas for p,q. Require the pair response-difference denominator to exclude zero.
3. For Δ=q^2-4a_i a_j p, a negative upper endpoint contradicts the promised real model on the confidence event (or indicates arithmetic/model/noise failure). If the upper endpoint is nonnegative, intersect Δ with [0,infinity), then enclose both roots and their paired reverse entries. A lower endpoint at zero is allowed. Use the direct paired expressions (q±sqrt Δ)/(2a_i), (q∓sqrt Δ)/(2a_j) to reduce interval inflation.
4. Take the entrywise hull of BOTH pair orientations for every edge. This contains the true gauge matrix without any global branch enumeration. Try certificate (C) immediately. Near reciprocity, two individually unstable orientations can be so close that their entire union already predicts accurately.
5. If the hull is too wide, use actual triple measurements to reject branches whose predicted response intervals are disjoint from the observed interval. An interval prediction must itself have a verified denominator/invertibility; otherwise it cannot be discarded. N854's anchored sequence has at most four local candidates per first-stage triple and two per subsequent triple when earlier choices are certified. A candidate is selected only if every other candidate has disjoint response intervals. The correct candidate necessarily survives on the simultaneous coverage event.
6. Where initial edge roots are separated, fixing either initial orientation is justified by the global weighted-transpose invariance, with the true a belonging to its interval. Sequential unique triple selection then retains a response-equivalent true matrix. If an unresolved orientation cannot be safely propagated, keep a conservative enclosure of all admissible branches or retain the original pair hull; do not assert a polynomial-time exact correlated branch search. Adaptive extra triples, alternative anchors, or full-support queries may tighten the enclosure but all are charged.

A root gap, a singleton denominator margin, a pair denominator margin, and separation between competing triple predictions are measured quantities, not generic positive constants. For generic data with all required margins positive and a strict diagonal-Lyapunov witness, shrinking measurement intervals eventually makes the anchored procedure succeed and its prediction error tend to zero. This is pointwise convergence conditional on arbitrarily improving precision and a stationary model, not a uniform stopping-time bound. Non-generic cases may also pass the task-first hull certificate, as below.

## 5. Complete noise and measurement accounting

A deterministic adversarial error bound eta yields fixed response intervals of radius eta. Repeating a reading does NOT reduce that radius without an additional noise model. Failure at that precision is honestly inconclusive. A known residual bias/drift bound must be added to every radius and does not average away.

For independent, conditionally mean-zero σ-sub-Gaussian read noise, n readings at a fixed setting give radius r with failure probability <=2 exp(-n r^2/(2σ^2)). For K predetermined settings and one fixed stage, choose
  n=ceil[(2σ^2/r^2) log(2K/alpha)]
per setting for simultaneous coverage >=1-alpha. Gaussian noise is a special case. This charges K*n scalar reads, not K queries alone. Unknown variance needs a justified confidence procedure; a sample standard deviation is not a replacement for the assumed bound.

For adaptive batches/stopping, assign the jth batch failure budget alpha_j=6alpha/(pi^2 j^2), use fresh samples and conditional sub-Gaussian bounds, and let its radius be r_j=sqrt[2σ_j^2 log(2/alpha_j)/n_j]. The union bound gives coverage at every attempted stopping time. Reusing or combining old samples requires an appropriate time-uniform confidence sequence or another valid union allocation. Either way the actual cost is sum_j n_j, with inverse-variance budget sum_j n_j/σ_j^2. Record attempted/rejected settings, discarded batches, reset/switch counts, source exposure and settling time, precision costs, controls' magnitudes, computation and verified reuse lifetime. Independent bounded centered noise supports averaging; arbitrary bounded noise does not.

The full N854 schedule has K=(3m^2-m+4)/2 distinct settings for m>=2, but repeated observations and extra settings are additional costs. No uniform polynomial bound on the required sum n_j follows. The noisy needle family can force arbitrarily poor separation or conditioning, and its inverse-variance lower bound remains compatible with every statement here.

## 6. Exact-rational worked example: separated nonreciprocal branches

Use m=3, U=1, t1=1/2, t2=t3=1, f0=10, a=(1,2,3), and
  H = [[2,1/5,1/2], [3/10,2,11/10], [7/10,13/10,2]].

This is physically realizable within the mathematical model: set G=[[10,a^T],[1,H]], A=G^(-1), P=[0;I3], b=c=e0. Then the extracted w=1 and v=a. Gershgorin gives sym(H)>=I/5; the exact Schur complement of sym(H) in sym(G) is 7258/927>0, so sym(G)>0 and sym(A)>0. This is a synthetic realization, not a fabricated apparatus.

The measurement receipt consists of the exact scalar responses at all 14 settings, each declared with radius 10^-8. Exact rational interval calculations in worked_example.py verify:
- Every singleton and pair denominator excludes zero.
- Pair discriminant intervals are approximately [0.15870255,0.16129748], [2.55750086,2.56249918], [2.88578494,2.89421508].
- The four exact triple predictions, fixing the lower root on edge {1,2}, are 190800/21829, 571720/65589, 582960/67007, 192280/22007.
- Their interval predictions are [8.73982269304,8.74150943207], [8.71570350661,8.71770747293], [8.69903696206,8.70093632507], [8.73612063967,8.73831938077]. Only the first intersects observed [8.7406660764,8.7406660964].

Choose the displayed rational H,a as nominal rounded estimates; all error radii are computed against the recovered intervals, so the fact these happen to equal the synthetic truth is not used by the certificate. The largest H entry error radius is <0.000869442; the largest a radius is <0.000000500001. With Λ=I, eH<0.002608326, robust h>0.197391674 and Mtrue<0.835149. Using ||ahat||2||1||2=sqrt(42)<6.5 and the conservative Mcenter<=Mtrue proves a uniform error <0.011827 over the whole cube, not merely held-out sample accuracy.

For a hypothetical σ=10^-7 independent Gaussian interface and alpha=.01, n=1588 readings per setting produce simultaneous radius 10^-8, costing 22,232 scalar reads. The displayed deterministic receipt is illustrative; it is not claimed to be an actual Gaussian experiment or a guaranteed successful random transcript. A real transcript must pass the same interval tests. The frequentist statement is P(pass and false certificate)<=.01, not generally P(correct given pass)>=.99. All 22,232 reads, setting time, resets, settling, and reuse validity must be charged.

## 7. Exact reciprocity: stop without root separation or triples

Let a=(1,1,1), f0=10 and
  H=[[2,1/5,3/10],[1/5,2,2/5],[3/10,2/5,2]].
Use the same t1,t2,U and radius 10^-8. Each true pair discriminant is exactly zero. The observed interval discriminants straddle zero, so a mandatory generic root-gap test would never succeed at the true zero limit.

Instead, reciprocal_example.py clips the discriminants at zero and takes the hull of both roots on every pair. After only baseline, six singleton and six pair settings (13 settings), it verifies max H-entry radius <0.015474500, eH<0.046423500, and max a-entry radius <0.000000500001. Gershgorin gives center margin 1.3, robust h>1.2535765. Certificate (C), even with Mcenter replaced by Mtrue, is <0.027424. Thus a requested uniform tolerance .03 is certified without measuring a triple or resolving any directed orientation. No exponential branch enumeration is used. This symmetric example is realizable with G=[[10,1^T],[1,H]], sym(G)>0 by the Schur bound 10-3/1.3>0.

## 8. Strong measured-model baseline and honest conclusion

The relevant strong comparator receives exactly the same raw scalar readings, noise assumptions, calibrated rank-one actuator law, passivity premise, setting amplitudes and reuse lifetime. It fits the reduced rational scalar-response model subject to all measurement intervals and, when available, diagonal stability. It can retain the entire feasible model set and certify its prediction envelope by verified optimization/interval branch-and-bound. This is a physics-compliant measured-model baseline, not an oracle given the hidden plant.

Our explicit interval construction encloses that feasible set whenever the chosen gauge/branch reduction is valid; thus a sufficiently powerful verified feasible-set baseline can match or improve our worst-case prediction interval with the same data. Our procedure supplies a transparent algebraic initializer, local branch-elimination schedule, and inexpensive sufficient uniform certificate; neither example establishes fewer measurements, superior physical precision, or a fundamental capability advantage over that baseline. The baseline's global verified feasibility computation may be expensive; our conservative hull may fail where it succeeds. Charge both computation and experiments, and compare empirical totals rather than attributing a win from Q(m) alone.

The defensible escape is conditional usefulness: favorable actual measurement separations, moderate gauge weighting, and a verified passivity margin can support finite-noise uniform scalar prediction with a completely charged, auditable certificate. It is not a loophole in the all-adaptive noisy lower bound.
