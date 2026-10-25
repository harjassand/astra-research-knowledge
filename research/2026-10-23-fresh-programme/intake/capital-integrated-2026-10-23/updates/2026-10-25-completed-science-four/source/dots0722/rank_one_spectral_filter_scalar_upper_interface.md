# A complete rank-one-noise upper certificate with one scalar optimization

2026-10-25. This is a rigorous relaxation of the actual two-atom optimization. It does not assert equality, so it is consistent with the proved necessity of two upper atoms near collinear noise.

## Exact spectral probabilities

Let x=uu*, ||u||=1, and let b be genuinely noncollinear rank-one noise. Set y=x/4+3b/8. On span{u,v}, y has two positive eigenvalues s_i and eigenvectors e_i. Define

pi_i=|<u,e_i>|^2/(4s_i).

The rank-one decomposition of y implies <u|y^(-1)|u>=4. Thus

sum pi_i=1, sum pi_i s_i=1/4.

The exact resolvent kernel is

h(t)=<u|(y+tI)^(-1)|u>/4=sum_i pi_i s_i/(s_i+t).

Let q=Tr(x-3b/2)_+. Since x-3b/2=2x-4y, its positive eigenvalue obeys the rank-one determinant equation

1=2<u|(qI+4y)^(-1)|u>.

Consequently the spectral probabilities also satisfy

**sum_i pi_i q/(q+4s_i)=1/2.**

These are exact physical constraints, not an independently chosen distribution.

## Complete scalar upper bound

For any positive input block with lower block x, retain its exact scalar Schur resolvent g(t). Convexity of -log(1-g h) in h gives pointwise

log(1-g/(1+t))-2log(1-h(t)g)
<=sum_i pi_i {log(1-g/(1+t))-2log[1-s_i g/(s_i+t)]}.

Every logarithm is defined because g<=1 and s_i/(s_i+t)<1. Integrating, the right side is exactly

2 sum_i pi_i C(D_(s_i) B D_(s_i))-C(B),
D_s=diag(I,sqrt(s)).

Filters with s>1 are used only as positive congruences in a mathematical expression, not asserted trace-nonincreasing operations. The mixture has mean s=1/4, which ensures the final scalar optimization is finite.

Purify B into environmental operators A,X. Then C(D_s B D_s)=S(A)+S(sX)-S(A+sX), with Tr X=1. The displayed weighted combination is a balanced TWO-source entropy expression. The accepted binary testing-measure transfer therefore implies

**Gamma(x,b)<=U(pi,s):=sup_(r>=0) [2 sum_i pi_i h(r,s_i)-h(r,1)],**

where h(r,s)=(r+s)log(r+s)-r log r-s log s.

All upper dimensions and Schur remainders are retained in this bound. The function tends to zero as r decreases to zero and to minus infinity as r increases to infinity, because 2 sum pi_i s_i-1=-1/2. Thus its supremum is finite and attained unless the zero value is maximal.

Concavity of h(r,s) in s and sum pi_i s_i=1/4 give U<=k=(1/2)log(32/27). The desired stronger inequality U<=kq remains UNPROVED here. Proving it for every physical spectral pair would prove the actual rank-one positive-part budget. A counterexample to this relaxation would not by itself refute the actual capacity bound.

## A precise scalar dual-majorant target

For fixed r,q, it would suffice to construct real B,C such that, for every s>=0,

2h(r,s)-h(r,1)
<=kq+B(s-1/4)+C[q/(q+4s)-1/2].

The two known moments cancel the last terms after averaging. This is an ordinary scalar supporting-majorant problem, not an operator inequality or a claimed scalar lift.

A concrete tangent-based proposal can be written without choosing a numerical grid. Put f0=2h(r,1/4)-h(r,1). If f0<=kq, ordinary concavity already supplies the majorant with C=0. Otherwise choose

C=-2(1+q)(f0-kq)/(1-q),
B=2log(1+4r)+4q C/(1+q)^2.

The proposed majorant then touches the entropy curve and has matching derivative at s=1/4. Its global nonnegativity is NOT established. In exact Bregman form it requires

h(r,1/4)+log(1+4r)(s-1/4)-h(r,s)
>=(-C/2) * 16q(s-1/4)^2/[(q+4s)(q+1)^2].

This identifies the remaining one-variable sign inequality precisely. No assertion that tangency alone proves it is made.

## Useful checks and limitations

At zero noise the spectral distribution collapses to s=1/4 and U=k. In the fixed-overlap strong-noise limit it converges to the already proved sharp filter capacity kappa(2,(1-rho)/4). At weak noise alpha with fixed overlap rho, evaluating the scalar function at r=1/8 loses (log 3)alpha*rho+o(alpha), whereas the positive-part allowance loses only 4k alpha*rho. This is a local consistency check, not a proof of the global moment inequality.

No arbitrary pointwise g relaxation is used. The Jensen step is calibrated by an actual probability distribution with both mean and resolvent moment fixed; the subsequent transfer is the valid balanced binary one. The full WH3 target remains open.

## Subsequent resolution, 2026-10-25

The scalar moment inequality marked open above is now proved in rank_one_calibrated_log_moment_complete_budget.md by a shifted logarithmic two-point mixture theorem. It gives the stronger pointwise-in-r bound U_r<=q f0(r/q)<=kq. Adding missing spectral probability at s=0 extends the receiving theorem from rank-one noise to arbitrary PSD b, while x remains rank one. The earlier open statements are retained as development history, not current status. Full arbitrary-rank x remains open.
