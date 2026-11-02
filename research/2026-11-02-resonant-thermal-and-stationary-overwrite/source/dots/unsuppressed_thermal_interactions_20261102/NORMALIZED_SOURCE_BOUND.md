# Scalar-pressure normalized source-column bound

2026-11-02. Follow-up to root's resonance compiler. This is a constructive bound for a **fixed collection of marked source clocks**, conditional on the audited signed-rod representation and its KP correlation/partition-ratio consequence. It is not, by itself, a completed connected-source polymer theorem.

## 1. Notation and exact pressure cancellation

Use untuned weak-endcap scaling `g=eta*t/K`, path `A=t(2I-T)`, and

`M0=2g²/t=K J0`, `M1=g²(K-1)/t²`, `J0=2g²/(tK)`.

The infinite-time nonwinding one-rod pressure is exactly

`h_nv = M0-J0 = 2g²(K-1)/(tK)`.

Let rod charge be `a(l)=a0+b*l`, with `a0=64x/K`, `b=32x*t/K²`, `x=Dbar*eta²`, as in root's established resonance KP bound. Set `M0(b)=g² vᵀ(A-bI)^-1 v`, and `r=b/mu<1`.

Define the important residual

`p = exp(a0) M0(b)-M0`.

The resolvent identity and spectral positivity give

`0 <= M0(b)-M0 <= b M1/(1-r)`.

Therefore

`p/J0 <= K[exp(a0)-1] + exp(a0) * b*K*(K-1)/(2t*(1-r))`.

Substituting a0,b,

`p/J0 <= 64x exp(a0) + 16x exp(a0)/(1-r)`.

For example, if a0<=log 2 and r<=1/2, then `p/J0<=192x`. This is uniform in K. The crucial cancellation is

`exp(a0)M0(b)-h_nv = J0+p <= J0(1+192x)`.

Bounding the source by its bandwidth loses this identity. Even the improved bound exp(beta*M0) loses the factor K unless the background scalar pressure is removed first.

## 2. Full-spectrum source transfer matrix

Summing absolute trajectories on a marked clock, with the rod-length tilt charged only while the clock is nonzero, gives the K-level comparison transfer matrix

`H_tilt = [[0, -g exp(a0/2) vᵀ],[-g exp(a0/2)v, A-bI]]`.

All path-internal hops retain t. A complete ordinary excursion has two endpoint hops and therefore picks up exp(a0), exactly as required. An interval whose endpoint is supplied by a source matrix unit instead of a vacuum hop needs a separate endpoint charge; at most a fixed number of exp(a0) factors per source insertion pays these intervals. Never-vacuum source histories also require one endpoint charge, not deletion from the trace.

Schur complement for any negative eigenvalue E gives

`-E = g² exp(a0) vᵀ(A-bI-E)^-1 v <= exp(a0) M0(b)`.

Thus `lambda_min(H_tilt)>=-exp(a0)M0(b)` and

`Tr exp(-beta H_tilt) <= K exp[beta exp(a0)M0(b)]`.

For arbitrary ordered source matrix units B_j of norm at most one, generalized Schatten Hölder gives

`|Tr exp(-tau_0 H_tilt) B_1 ... B_m exp(-tau_m H_tilt)| <= Tr exp(-beta H_tilt)`

when all tau_j>=0 and sum tau_j=beta. Here absolute trajectory weights are nonnegative after matrix-unit labels are fixed, so this bounds the fully summed pinned history, not merely a single path. Matrix-unit decompositions of arbitrary local operators must be charged separately; they cost a fixed polynomial in K for bounded source support.

After scalar normalization,

`exp(-beta h_nv) * summed_tilted_source <= K exp[beta(J0+p)] * endpoint_factors`.

**This includes every source clock level and every pin time.** No ground-band approximation or zero-clock projection occurs.

## 3. Finite-beta singleton tail and background deletion

To replace the exact finite-beta nonwinding singleton pressure by h_nv, retain a tail term

`delta_beta = integral_beta^infty rho(l) dl`.

Taking c=t/K²<=mu/4,

`delta_beta <= exp(-beta*c) M0(c) <= (4/3) M0 exp(-beta*t/K²)`.

Hence `delta_beta/J0 <= (4/3) K exp(-beta*t/K²)`. At the intended beta*J0 cold scale this is extremely small, but it must be included.

The rooted rod theorem bounds all non-singleton clusters touching a fixed clock by

`beta * [exp(a0)M0(b)-M0] + exp(a0) W(b)`

with `W(b)=Tr exp[-beta(A-bI)]`. Including winding singletons, the tail, and wrap singletons gives the conservative local residual pressure bound

`L_beta = beta[J0+delta_beta+p] + exp(a0)W(b)`.

Define `Xi_full` as the reference signed partition function and `Xi_delete(C)` as its rod gas after removing all trajectories on a finite set C of clocks. The cluster expansion then gives

`log Xi_full - log Xi_delete(C) = beta h_nv |C| + R_C`,

`|R_C| <= |C| L_beta`.

This statement follows by marking a clock in C in every removed cluster. It may overcount clusters meeting several clocks, which only weakens the absolute bound. The local bound works equally on finite induced clock graphs, with the same Dbar ceiling.

This deletion ratio, not an absolute bound on Xi_full, supplies the negative pressure needed to normalize each source column.

## 4. Conditional marked-column bound and its exact remaining hypotheses

Take a finite source-clock set C containing **every clock whose trajectory or flux is affected by the chosen source insertions**. Outside C the flux labels must remain those of the reference sector. Fix source trajectories, and regard all their maximal nonzero intervals as external rods.

The KP partition-ratio bound for external rods bounds the outside/background response by `exp(sum_external a(rod))`. It is essential that it uses the actual nonzero intervals. Charging every source clock as a beta-long rod instead would reintroduce exp(beta*b), which is too expensive for the intended estimate. A source interval cut by a matrix-unit insertion is allowed to be open at that insertion; the same overlap measure l+l' bounds its interaction with background rods. Extra endpoint charges pay those cuts.

Dropping source–source signs costs nothing because their moduli are <=1. Integrating the source trajectories with the transfer matrix above, and then applying the background-deletion formula, yields the conservative fixed-support estimate

`|normalized marked contribution|`

` <= K^|C| exp{ |C|[ beta(2J0+2p+delta_beta) + exp(a0)W(b)] }`

`    * exp[O(a0)*(number of insertion endpoints+|C|)] * product insertion norms`.

The coefficient 2 is not optimized; one copy comes from the source comparison and one from the background residual. At x small, and with delta_beta,W(b)/(beta J0) small, this is

`poly(K)^|C| * exp[O(beta J0)|C|] * product insertion norms`.

If each local source affects at most c clocks and has matrix-unit/Pauli expansion overhead poly(K), then |C|<=c*m for m insertions. Integrating ordered insertion times therefore produces the desired per-insertion scale

`q(v) <= poly(K) * exp[C beta J0] * beta*v`,

up to fixed geometry, local dimension, and bath-spin constants.

### What this does not yet prove

This fixed-support normalized moment bound does **not** alone prove convergence of the connected-source polymer expansion. Spatially separated source sets do not factor because background rods may connect them. The connected cumulant/forest step must retain those connecting background clusters and use spare spatial KP charge. A generic bound on all moments cannot silently replace that step.

Likewise, the external-rod partition-ratio estimate must be invoked with trajectory labels, not only length-averaged activities; the existing rod KP bound has that stronger trajectorywise form. If the chosen generic source dictionary creates seams outside C or creates background interactions not representable as the existing modulus-at-most-one pair factors, C/dictionary must be enlarged or that step separately proved.

The normalized pressure mechanism itself encounters no K-dependent obstruction. Its uniform cancellation is an exact resolvent calculation plus the existing rod cluster bounds. It improves the raw exp(beta J0 K) source cost to exp(O(beta J0)) at the fixed marked-support level, without changing the already-positive compiler.
