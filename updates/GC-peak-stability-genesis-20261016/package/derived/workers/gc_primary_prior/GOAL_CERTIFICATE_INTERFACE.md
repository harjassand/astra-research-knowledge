# Finite-chain output certificate interface

This is an independent reconstruction of ordinary adjoint/comparison identities. It is not a target-specific successful bound or a claim of novelty. The primary source comparison is in `REPORT.md`.

Let G be the exact finite conservative **column** generator of the retained eight-site process plus its separate overflow sink. Freeze every target-grid column as specified; do not add a duplicate success sink. Let p'=Gp with the exact initial probability p0. For scalar first-hit output use ell=1_B, with ell(overflow)=0.

## Exact adjoint identity

For an arbitrary differentiable saved approximation q, put r=q'-Gq and e0=q(0)-p0. Let

    z(t)=exp(G^T(h-t))*ell.

Then z'=-G^T z, z(h)=ell, and 0<=z<=1 by the stochastic semigroup. Direct differentiation gives

    ell^T[q(h)-p(h)] = z(0)^T e0 + integral_0^h z(t)^T r(t) dt.

All signs follow by differentiating z^T(q-p). Signed q is allowed; positivity belongs to the exact semigroup. A large full l1 residual can coexist with a small output pairing, but this identity does not make the unknown z free.

If a computable zhat is certified with sup_t ||z-zhat||_infinity<=delta, then

    |output error| <= |zhat(0)^T e0 + integral zhat^T r|
                      + delta*(||e0||_1 + integral ||r||_1).

The signed pairing and remainder require outward arithmetic and the *full exact* generator. A reduced residual, an uncharged compressed residual, or an assumed delta supplies no certificate. Exact tensor contractions of a signed pairing may be cheaper than an l1 norm, but tight rank/precision/verification costs remain to be demonstrated.

## Direct upper/lower output witnesses

If a differentiable finite vector v(t) satisfies

    v(h)>=ell,          v'(t)+G^T v(t)<=0 componentwise,

then differentiating v^T p gives

    ell^T p(h) <= v(h)^T p(h) <= v(0)^T p0.

Reversing both inequalities gives a lower bound. These conditions do not require a forward approximation q. A source computed only in a reduced norm is insufficient: each component inequality must be proved on every retained continuation/target/sink coordinate, or replaced by a rigorously proved dominating construction. Finite-state comparison avoids unbounded-chain optional-sampling obligations; transfer back to the original unbounded model still pays the separate overflow error.

For a stopped local-region construction, bound the payoff on **every** artificial exit consistently with the desired upper/lower direction. Setting an exit payoff to zero while claiming an upper bound can change the event. Any added scalar sink must correspond to an actual declared absorbing/exit event; freezing the physical cap or deleting outward hops changes the generator.

## Discrete uniformization analogue

With a proved theta>=maximum exit rate, P=I+G/theta is stochastic. Let pi_k be exact Poisson weights, approximate powers fhat_j, and full recurrence residuals

    r0=fhat0-q0,       rj=fhatj-P*fhat(j-1).

Define aj=sum_{k=j}^m pi_k*(P^T)^(k-j)*ell. Direct exchange of finite sums gives

    ell^T(what_m-w_m)=sum_j aj^T rj.

Since 0<=aj<=cj*1, cj=sum_{k=j}^m pi_k,

    |ell^T(what_m-w_m)|<=sum_j cj*||rj||_1.

The first equality retains goal-specific cancellation; the second is the standard safe full-norm fallback. Poisson tail, incoming error, approximate weights, final contraction/rounding, and operator mismatch are separate charges unless already enclosed by the exact final residual. No ranks, runtime, or computed witness are supplied here.

## Receiving gate

A first-slab scalar interval below its allowed absolute error passes only that stated output subgoal. It does not give an accurate propagated full state, a nontrivial relative error for a very small probability, or the original T=1 probability. A full-horizon adjoint witness would instead have the actual deadline-one terminal payoff. N893's total-count-only obstruction has its own fixed horizon and exact envelope class; none of the identities above removes that obstruction.
