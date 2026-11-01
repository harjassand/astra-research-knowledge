# Rate-2 paid interior removal — author component

**Result:** for every fixed epsilon>0 (epsilon<=1/4), all actual chain states of
total n with B,C,D,E>=epsilon n, allowing A=0, satisfy

    P[actual total at physical time 5 <= 7n/8] >= 1-exp(-c_epsilon n)

for all n>=n0(epsilon). Constants are uniform over these states.

Read `PAID_INTERIOR_REMOVAL.md` for the full proof, constant definitions,
acquisition/receiving boundaries, and every-channel clock accounting.

* Explicit positive entry and finite-cover deterministic attraction earn an
  actual entropy-tube entrance on O(1/n) physical time.
* Exact local entropy coercivity is kappa=(1-s)/486, s=(sqrt(7)-1)/2.
* O(n) short actual-chain concentration windows preserve an inward margin;
  no stochastic mixing or original-chain product-Poisson claim is made.
* Actual A-death and immigration clocks finish the fixed-fraction removal.
* The initial deterministic uniform entry time is proved finite but not
  numerically certified. The resulting n0 is an existence constant, not practical.
* No arbitrary-boundary entrance, recurrence, stationary moments, or global
  Foster geometry is claimed.

`check_interior_algebra.py` and `check_results.json` check exact algebra and
margins only, not independent theorem acceptance. The result is author-pending.

Supplier: already-received internal deterministic complex-balanced realization
and the authorized single-linkage global-attraction source receipt in the sibling
rate2_dyadic_continuation directory. No external retrieval was performed here.
