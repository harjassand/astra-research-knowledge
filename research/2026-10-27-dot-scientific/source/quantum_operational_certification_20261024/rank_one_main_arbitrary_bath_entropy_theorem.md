# Full WH3 value theorem: rank-one main Gram and arbitrary positive bath noise

## Statement

In the balanced scalar-central matrix-bath source, let

 T=[d;sqrt(h)][d;sqrt(h)]*, h>=0,
 Q>=0 arbitrary on the finite bath,
 M=[[Q+dd*,sqrt(h/2)d],[sqrt(h/2)d*,h/2]],
 M0=dd*+2Q, tau=||d||^2+h+2TrQ.

Then the actual full entropy deficit

 Delta(Q)=TrTlogT-2TrMlogM+TrM0logM0
          +tau log(2/3)+||d||^2 log2

is nonnegative. Q need not commute with dd*, and its rank and dimension are unrestricted.

The h=0 or d=0 endpoints are physical-2+1 block diagonal and already paid. Assume h>0 and x=||d||^2>0 below. Keep d,h fixed and minimize over Q.

## 1. Exact Stieltjes gradient and value difference

For s>0 put

 r_Q(s)=d*(Q+sI)^{-1}d,
 a_s=2s/(h+2s),
 k_s(r)=log(1+a_s r)-log(1+r/2),
 w_Q(s)=k_s'(r_Q(s))
       =(a_s-1/2)/[(1+a_s r_Q(s))(1+r_Q(s)/2)].

Let kappa=log(4/3)>0. The exact regularized determinant calculation gives

 Delta(Q)-Delta(0)
 =2kappa TrQ+2 integral_0^infinity [k_s(r_Q(s))-k_s(x/s)]ds.  (1)

This is a convergent DIFFERENCE formula, not an unregularized integral of either separate logarithm. Its normalization constant was independently derived in `rankone_balanced_bath_stieltjes_interface.md`.

For an independent direct check of the gradient, Schur complementation gives

 (M+sI)^{-1}_bb=(Q+sI+a_s dd*)^{-1},
 log M0=log2 I+log(Q+dd*/2).

The logarithmic resolvent identity and Sherman-Morrison then yield, on every positive-support variation of Q,

 (1/2) grad_Q Delta
 =kappa I-integral_0^infinity
    w_Q(s)(Q+sI)^{-1}dd*(Q+sI)^{-1} ds.             (2)

Crucially w_Q(s)<0 below h/2 and >0 above h/2, independently of Q. Supported derivatives remain convergent when Q has a kernel; only strictly positive-support variations will be used.

## 2. Existence of a minimum with the trace payment retained

Let t=TrQ. Since Q<=tI,

 x/(s+t)<=r_Q(s)<=x/s.

For s<h/2 the function k_s is decreasing, so the contribution in (1) is nonnegative. For s>=h/2 it is increasing and 0<=k_s'<=1/2. Therefore

 2 integral_(h/2)^infinity [k_s(r_Q)-k_s(x/s)]ds
 >=-x integral_(h/2)^infinity t/[s(s+t)]ds
 =-x log(1+2t/h).

Thus

 Delta(Q)>=Delta(0)+2kappa t-x log(1+2t/h).          (3)

The right side tends to positive infinity as t tends to infinity. Continuity and finite-dimensional compactness therefore ensure that Delta attains a minimum on the PSD bath cone. No normalization constraint is imposed during this minimization; the paid linear trace term is essential.

## 3. Every minimizing bath has rank at most one

Let Q_* be a minimizer with positive support P. Variations supported on P are unconstrained in both signs for sufficiently small size, so (2) implies

 kappa P=P [integral (Q_*+sI)^{-1}d w_(Q_*)(s)d*(Q_*+sI)^{-1}ds]P.

Apply `single_crossing_resolvent_rank_collapse_lemma.md` with R=d and threshold h/2. It gives rank Q_*<=1.

An equivalent independent scalar proof is available in the positive-eigenvalue basis: offdiagonal stationarity between q_i<q_j forces the signed Cauchy integral integral w/[(q_i+s)(q_j+s)] to vanish. Multiplying by the strictly decreasing ratio (q_j+s)/(q_i+s) makes the q_i diagonal integral negative, contrary to its required positive value kappa/|d_i|^2. Repeated eigenspaces have a d-orthogonal direction with nonzero trace gradient. The short rank lemma handles all these cases simultaneously.

## 4. Receive the minimizer by an actual value theorem

If Q_*=0, the pure main input is paid by the pure/all-projector theorem. If Q_* has rank one, the exact purification dual in `matrix_bath_rank_one_main_rank_one_noise_dual_receiver.md` lies in the already proved stable one-column rank-two-kernel class. Hence Delta(Q_*)>=0 in either case. Since Q_* minimizes the actual value over all baths at the fixed main Gram, Delta(Q)>=0 for EVERY Q. This proves the theorem.

## 5. Whole scalar-bath/operator-central class by self-duality

The result also closes the balanced family with scalar bath D,Q and arbitrary operator-valued central H,C. If Q=0 its value is already paid by the dual-CQ theorem. Otherwise apply the exact operator-family purification duality: writing T=[R;S][R;S]* and scalar Q=ZZ*, the dual main Gram

 T'=[[R*R,sqrt2R*Z],[sqrt2Z*R,2Z*Z]]

has rank one because R and Z have only one row. Its central block is scalar 2Q, while its dual bath noise Q'=S*S/2 is arbitrary positive. The theorem just proved applies. Thus the full scalar-bath/operator-central value class is paid, not merely its faithful stationary points.

## Scope

This is a full-value theorem and a transferable stationary-rank-collapse mechanism. It does not establish the arbitrary matrix-bath/matrix-central balanced target, nor extend the common sign-threshold lemma to an operator-valued weight whose eigenvalues change sign at different shifts.
