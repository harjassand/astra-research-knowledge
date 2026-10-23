# Matched ordinary independence-MH comparator

The reference method starts at the same q and uses the same unnormalized target
and known proposal evaluations. It applies G alone. No target table, normalizer,
off-proposal target queries or population-KL estimator is added. Full caching
is allowed to both methods. If a full normalized target table were already
available, direct sampling would be a stronger ordinary option; this theorem
does not create a computational advantage in that information setting.

The established sharp minimax statement is

    (log n) sup_{D(pi||q)<=K} ||qG^n-pi||_TV -> K.

For receiving use, a short complete proof is included here. It is a reconstruction
of the preserved ordinary comparison, not a new Cycle5 research claim.

Let H={W>R}, a=pi(H), R>e. Couple X0~q and Y0~pi using common iid proposals
from q and common acceptance uniforms for their independence-MH updates; once
equal, keep them equal. If both current weights are at most R, a proposal
has probability at least pi(W<=R)/R=(1-a)/R of being accepted by both chains.
Before coupling, their weights remain at most R unless a proposal of weight
above R occurs, in which case both accept and coupling occurs. Thus, after
charging the initial high-weight event by q(H)+pi(H)<=a/R+a,

    TV(qG^n,pi) <= a+a/R+exp[-n(1-a)/R].

The binary log-sum bound a<=K/(log R-1), with R=n/(log n)^2, gives the
uniform limsup K after multiplication by log n.

For any fixed k<K, take two states with rare target mass p=k/log n and
proposal mass q_rare=p/[n(log n)^2]. The complement carries the remaining
mass. Its forward KL tends to k, so it is eventually strictly admitted.
For large n the rare state has maximal weight n(log n)^2; the nontrivial
eigenvalue of G is 1-1/[n(log n)^2]. Its proposal-start TV at n is exactly

    (p-q_rare)(1-1/[n(log n)^2])^n ~ k/log n.

Increase k to K. This proves the matching lower and hence the comparator.
For any fixed positive constant kappa, replacing n by floor(kappa n) leaves
the leading coefficient K unchanged. Consequently matching a fixed expected
global-attempt fraction alpha/2 does not erase the hybrid's adverse critical
amplitude. This is an asymptotic law comparison, not a finite-time TV ordering.

One hybrid step holds with probability 1/2, globally proposes with alpha/2,
and locally proposes with beta/2. Local screening adds q ratios, uniforms,
potential target calls and implementation/maintenance obligations; its exact
cache misses and target latency are not measured here. The new absorbed
process is a proof device, not an implemented alternate sampler. No useful
speedup or physical performance follows from the endpoint theorem. The new
scientific contribution is the sharp robustness boundary and its information
allocation mechanism.
