# Source-exact Brownian cube completion and a boundary-aware heat split

## 1. A physically acquired continuous completion

Use standard isotropic Brownian motion, generator (1/2)Delta, stopped at its first exit from Q=(-1,1)^3. Its covariance is a sum of the three coordinate-axis null covariances, so this is the already admissible isotropic null-diffusion operation. Points initially on the boundary stop immediately. After exit, complete the remaining coordinates to cube corners by the same mean-preserving axis Bernoulli splits as before.

For each corner s, the function p_s(x)=product_i(1+s_i x_i)/8 is harmonic and bounded on the closed cube. Optional stopping therefore preserves its expectation exactly. The Brownian-first completion and direct axis completion have the SAME corner law for every starting point, not only after averaging. The original source mu and actual selected endpoint law eta are not changed or replaced by an uncharged seed.

Let G_Q be the Dirichlet Green kernel for -Delta, omega_nu the actual stopped Brownian exit law, and A_omega the positive subsequent axis-completion occupation. Then

    R_nu^B = (G_Q nu) I + A_(omega_nu),
    DivDiv R_nu^B = C_nu - nu,  J:R_nu^B=0.

The occupation normalization is G_Q nu=(1/2) integral_0^infinity P_t^Q nu dt. Immediate boundary atoms contribute to omega_nu, not to G_Q nu. With the exact cubic face stress T and delta=c_mu-c_eta already received,

    S_B = M_eta + [G_Q(eta-mu)] I
                + A_(omega_eta)-A_(omega_mu) + delta T

has original source mu-delta_0, is J-null, and is supported in the closed cube. The continuous volume occupations of BOTH laws can cancel. The previous1/4 line-versus-volume obstruction does not apply. No positivity follows just because both terms are absolutely continuous.

## 2. Boundary flux and face/edge occupation ledger

For an interior source, omega has face density -partial_n G_Q nu. Actual boundary source atoms are immediate exit atoms and must be retained separately. Immediate atoms on edges or corners are completed ONCE in the fixed global coordinate order, not counted once for every incident face. Interior Brownian harmonic flux has no edge mass. For the present E-supported law, cube-edge points are only the four E vertices, whose subsequent coordinate completion has zero occupation. On face i, with remaining coordinates u<v, the first remaining axis-completion occupation is the one-dimensional Dirichlet Green inverse in u of that face measure, in tensor direction e_u e_u^T. The subsequent edge source at u=s is the face measure weighted by (1+s u)/2 and integrated in u. Its edge occupation is the one-dimensional Green inverse in v. Adjacent-face contributions to a common edge are added before taking negative parts. These are actual continuations, not a guessed flux correction.

In the sine basis phi_k(x)=product_i sin(pi k_i(x_i+1)/2), lambda_k=pi^2|k|^2/4. A Green coefficient is E_(eta-mu) phi_k / lambda_k. At the negative face its exit coefficient multiplier is pi k_i/2; at the positive face it is (-1)^(k_i+1) pi k_i/2. Face completion divides by the appropriate one-dimensional eigenvalue. The Bernoulli edge integration multipliers are2/(k pi) on the negative side and2(-1)^(k+1)/(k pi) on the positive side. This gives the full volume, face, and edge ledger.

## 3. One failed undamped spectral gate

The frozen degree16 diagnostic used the actual selected proxy mixture, source phase96, saved volume queries, and fixed face64/edge128 Gaussian rules. Runtime1.43 seconds,136MiB. It reported volume negative mass0.006183, face0.025200, edge0, but those are NOT received values.

The conservation checks decisively failed: signed completion trace0.061524 instead of required0.013288; truncated interior exit mass+0.050983 instead of -0.080280. The endpoint proxy has0.080280 immediate-boundary mass (all classified boundary coordinates are exactly +/-1, not merely near the threshold). The omitted positive boundary-face lines and explicitly included boundary-edge completion are accounted for in the diagnostic; the large discrepancy is the undamped boundary-sensitive sine truncation. No small-N claim or degree increase follows.

An explicit near-face illustration is x=(1023/1024,0,0). The same undamped16-mode nearest-face probability is only about0.01464, while an elementary actual stopping argument gives probability at least0.9956 of eventual exit on that nearest face. A boundary-aware decomposition is essential.

## 4. Fixed heat-time split: no normalization of the failed fit

Fix t0=1/8. Write

    G_Q nu = (1/2) integral_0^t0 P_t^Q nu dt
                + sum_k exp(-lambda_k t0/2) phi_k E_nu phi_k/lambda_k.

The short-time part is the positive killed-heat contribution. The long-time sine coefficients now have exponential damping exp(-pi^2|k|^2/64), rather than an unweighted algebraic Green tail.

Let s(t,x) be one-dimensional interval survival and S(t,x)=product_i s(t,x_i). The actual late exit mass is E_nu S(t0,X). The early exit mass, INCLUDING any immediate boundary atoms, is1-E_nu S(t0,X). For the signed eta-mu difference, the early and late masses are exact negatives of the SAME quantity. This is a stopped-process identity, not an imposed normalization or two unrelated interval estimates.

The one-dimensional series is

    s(t0,x)=(4/pi) sum_(n odd>=1) exp(-pi^2 n^2/64)
                       sin(n pi(x+1)/2)/n.

The executed receiver evaluates modes1,3,...,15 outward, with an explicit tail from17. It separately receives the actual endpoint-proxy payment and a source-Haar midpoint error for this smooth survival function. The source points are acquired independently as the same exact Haar source, not borrowed as an unreceived density. The product survival is S3 invariant, so orbit representatives are legitimate without expanding their six copies.

Uniform derivative bounds |s'|<5/2 and |s''|<6 imply that either pure phase second derivative of S(t0,Z(a,b)) is at most59/2. A phase128 midpoint rule thus costs at most(59/24)(2 pi/128)^2. The actual endpoint survival transfer is at most5 times its received W1 proxy error. Exact mass/mean identities of the actual source are never inferred from proxy cancellation.

## 5. Integrated image bounds for the missing early face flux

For an INTERIOR one-dimensional starting point at distance d in (0,2) from a chosen face, the first-exit density on that face is

    f_d(t)=sum_(m in Z) (d+4m)/(sqrt(2pi) t^(3/2))
                         exp(-(d+4m)^2/(2t)).

The m=0 term is the positive half-space hitting density and captures the near-face singular time scale exactly. Boundary starting points are handled as immediate atoms, not by putting d=0 into this density. For0<t<=1/8 the time-integrated absolute remainder obeys

    integral |f_d-f_d^(0)| dt
      <= 2 sum_(m>=1) exp(-4(4m-2)^2) <= 4 exp(-16).

This follows by integrating each absolute image to an erfc tail and using erfc(u)<=exp(-u^2). In three dimensions, multiply by the two positive tangential killed kernels. Their integrated masses are at most1, so the SAME bound controls the integrated face-flux error of replacing the normal factor by its leading image. The displayed4 exp(-16) is per conditional face and starting point. For the signed eta-mu source (total variation at most2), a single-face bound is8 exp(-16); summing six faces gives48 exp(-16), approximately5.402e-6. The remaining tangential kernels and time/source integration are still required; this note does not assert that face allocation or negative surface stress is received.

For the late part, actual signed source total variation is at most2. The sum of all positive one-dimensional exp(-pi^2 n^2/64) terms is less than3, while the tail from17 is at most2 exp(-pi^2 17^2/64). Consequently truncation to k_i<=16 costs at most72 exp(-pi^2 17^2/64) uniformly in each late face density, and1728 times that exponential in total face L1. The receiver verifies this number directly. There is no divergent boundary derivative series left in the late part.

For the representative x=(1-d,0,0), d=1/1024, the other-face probability is at most2 E tau<=2(2d-d^2), and the opposite first-coordinate face probability is at most d/2. The late survival mass is at most(5/2)d. Thus the early nearest-face probability is at least

    1-2(2d-d^2)-d/2-(5/2)d > 0.993.

This is a received nontrivial near-face flux statement, not a sampled spectral value.

## 6. Remaining interface

The controlled aggregate and image-tail receiver repairs the identified conservation failure and supplies a stable boundary-aware representation. It does NOT yet receive the early flux distribution over individual faces or the signed face/edge negative-part integrals. Those costs remain essential: they cannot be inferred from total mass conservation, positivity of each unsigned heat kernel, or the favorable volume diagnostic. No improved stress bound, global PSD, W1 improvement or source membership is claimed. The selected same-law upper remains0.08612833015763681.

## 7. Positive face-completion kernels, avoiding a differentiated 3D fit

The same representation can be composed with the actual axis completion before numerical evaluation. On a face with normal coordinate i and remaining ordered coordinates u<v, let p_t be the one-dimensional killed interval heat kernel, G_1 its Dirichlet Green kernel for -partial^2, and

    H_t(x,y)=integral G_1(y,z) p_t(x,z) dz
            =G_1(x,y)-(1/2) integral_0^t p_s(x,y) ds.

Then0<=H_t<=G_1<=1/2. The face occupation density in direction e_u e_u^T from an interior start x is exactly

    integral_0^infinity f_i(t,x_i) H_t(x_u,y_u) p_t(x_v,y_v) dt.

Define B_s(t,x)=integral [(1+s z)/2] p_t(x,z) dz for s=+/-1. It is nonnegative and at most1. The corresponding edge occupation kernel is

    integral_0^infinity f_i(t,x_i) B_s(t,x_u) H_t(x_v,y_v) dt.

These identities follow by Tonelli and the actual positive Green occupations, not by assuming the terminal reward is harmonic. They keep the narrow short-time boundary contribution in positive one-dimensional kernels. Integrating a face/edge kernel over a spatial cell can use one-dimensional heat/Green integrals without evaluating a singular face density pointwise.

The total remaining two-coordinate completion trace from any face point is at most1. Therefore the signed all-six-face integrated normal-image error48 exp(-16) also bounds the induced nuclear-L1 error in the COMPLETE face-plus-edge occupation (not an extra factor for each stage). This does not remove the need to receive the actual time/source integrals and the cancellation of their signed measures.

In particular, receiving only cell masses is insufficient for an upper bound on negative mass: convexity gives the opposite Jensen direction. An actual upper receiver still needs within-cell variation, a received common-density cancellation, or another explicit measure comparison. This section supplies the exact positive kernel interface, not an executed face negative-part receiver.

## Independent audit

`INDEPENDENT_HEAT_SPLIT_AUDIT.md` and `independent_heat_split_check.py` / receipt record PASS for the bounded receiver and analytic construction, including section7. Exact actual-root and proxy guards, outward scalar replay, source midpoint budget, early/late correlation, and the signed all-six-face factor are checked. This does not receive short-time face allocation, signed cancellation, or a negative-mass upper. The failed undamped run and excluded unsimplified arithmetic prototype remain excluded.
