# Capital connections: exact developed consequences

15 October 2026. Inputs are the supplied phase-density and closure packets and main `846f185763ed3a27310fad4ce9471ba324d1e5f4`. These deductions are separate from their producers' claims. Historical priority and independent correctness are UNKNOWN. No physical response, actuator, detector, thermal library or device advantage is acquired here.

## 1. A complete affine-direction amplitude certificate

Let Ω be bounded Lipschitz, F:R^(m×n)→R a rank-one-convex homogeneous quartic polynomial, B a constant matrix, c a constant target translation, and

    u0(x)=Bx+c,   u(x)=a(x)u0(x),   a=1 on ∂Ω.

Initially take a smooth; the result extends by strong W1,4 approximation. No rotational invariance, positivity of a, mass constraint, nonvanishing u0 or special phase equation is required. Positive a literally preserves the unit direction; signed a preserves the pointwise affine line and is an additional consequence of the direct even-quartic polynomial proof. Define P=DF(B), Q=u0⊗∇a and

    R_F(C,Q)=F(C+Q)−F(C)−DF(C):Q.

Then the pointwise identity is

    F(Du)−F(B)
      =R_F(aB,Q)+div[((a^4−1)/4) P^T u0].                 (1)

Indeed Du=aB+Q, F(aB)=a^4F(B), DF(aB)=a^3P, and Euler gives P:B=4F(B). Differentiating the displayed flux gives exactly `(a^4−1)F(B)+a^3P:Q`. The boundary flux vanishes because a=1. Q has rank at most one, so integrating gives

    ∫[F(Du)−F(B)] ≥0.                                    (2)

Use the supplied quartic scalar remainder lemma, independently reconstructed: a convex quartic `At^4+Lt^3+C2t²+Dt+E` has C2≥3L²/(8A), hence its t=1 tangent remainder is at least A/3. If A=0, global convexity forces L=0 and C2≥0. Therefore, with

    μ_F=min{F(R):rank R=1, |R|=1},

equation (1) strengthens to

    ∫[F(Du)−F(B)] ≥(1/3)∫F(Q)
                     ≥(μ_F/3)∫|u0|^4|∇a|^4.             (3)

The polynomial identity also covers zeros of u0, avoiding a singular phase chart. For bounded Ω, multiplication by u0 is continuous on W1,4, so the extension is direct. For a general positively p-homogeneous F and positive a, the same identity has `(a^p−1)/p`; the real signed-amplitude version above uses even quartic polynomial homogeneity.

This is a concrete consequence of the incoming direction-preserving Picone mechanism, not a universal quasiconvexity theorem. For full-rank B and a depending on every coordinate, the direction field of Bx+c has nonlinear phase and need not lie in N812's affine-phase or separated sheared-phase templates. The class still fixes that direction pointwise; arbitrary test fields do not have this form. AIPS radial-map Jensen results and Brasco–Franzina hidden convexity/Picone results are substantial prior machinery; no originality claim follows.

### Explicit scalar dual and the signed boundary term

When m=n=2, F is left-SO(2)-invariant and u0 never vanishes, write r=|u0| and n=u0/r. Use the incoming density chart σ=r^4. Its exact calibrated flux is

    j_B=DF(B)^T u0/|u0|^4.                               (4)

In the source notation `aσ=∇σ/(4σ)` and `f_k(aσ)=F(B)/r^4`. Direct differentiation gives

    div j_B=4F(B)/r^4−4aσ·j_B,
    gσ=f_k(aσ)−aσ·j_B−div j_B/4=0.                       (5)

For any amplitude retaining the affine boundary, its boundary density is r^4, so

    (1/4)∫∂Ω ρ j_B·ν
      =(1/4)∫Ω div[P^T u0]=|Ω|F(B).                     (6)

This supplies an explicit adequate flux for the affine-direction sector of the source's remaining all-direction obligation. It requires no unknown scalar inverse or optimized amplitude. The interior lower bound is zero; the affine comparison is carried by the fixed boundary flux. Omitting that term is an invalid transfer.

For the source G,

    G(A)=3(u+v−2q)^2+(35/24)u²+q²−(5/2)qu,
    μ_G=3,   G(I)=−1/24.

Thus (3) has coefficient one for this unresolved nonpolyconvex energy at every B in the stated radial-affine family. Even the affine map `u0=x+c` on the unit square has negative absolute energy −1/24. Equations (5)–(6) show why a zero interior dual residual does not imply nonnegative absolute energy. The correct quasiconvexity comparison is against the same affine baseline, not zero. No Fstar-to-G positive-orbit transfer is used; the previously refuted orbit argument remains refuted.

### An explicit scale and topology falsifier

The source's continuum positive phase is `θ=y+(3/25)sin x+(1/10)sin y+(2/25)sin(x+y)`, winding (0,1) on the torus. Its certified gσ≥1 is a theorem for that phase, not a uniform phase theorem.

For R>1 consider the actual periodic map

    u_R=(R+sin x,sin y),   r_R=|u_R|,   n_R=u_R/r_R.

Its first component is positive, so n_R has a globally periodic half-plane phase with winding (0,0). Its phase and gradient are O(1/R), but Du_R=diag(cos x,cos y) does not shrink. Normalized torus averaging gives exactly

    E r_R^4=R^4+4R²+5/4,
    E G(Du_R)=483/64.

The normalized amplitude minimum for n_R therefore obeys

    λ(n_R)≤(483/64)/(R^4+4R²+5/4)→0.                     (7)

No positive phase-uniform lower floor such as one can extend to all translated, zero-winding phase charts. This is not a negative Jensen test or a disproof of a zero floor. It makes the translation/topology mismatch quantitative and retains the source warning that small phase with unbounded amplitude is not a simplification of the full problem.

## 2. A joint-response decision certificate with calibrated interactions

The closure source correctly replaces a bulk homogeneous thermal hull by a weighted sum of local hulls. Its module-level support bound then assumes additive outputs or an independently justified residual bound. Native joint-response failure is not repaired merely by more exact isolated calibrations.

Let accessible control modes be x_i∈{1,...,K_i}, and suppose a fixed decision score and resource cost have the **acquired** finite-factor representations

    J(x)≤J0+Σ_i J_i(x_i)+Σ_(ij) J_ij(x_i,x_j)+κ,
    C(x)≥Σ_i c_i(x_i)+Σ_(ij)c_ij(x_i,x_j).

κ is a uniform upper error for all omitted interactions, drift and model discrepancy on the allowed configurations. It is not inferred from the local fits. Costs must include applicable overhead and history costs, or have a separate conservative lower certificate. No assumption that the mode choices are statistically independent is needed.

Use nonnegative node marginals m_i and edge marginals m_ij satisfying unit normalization and edge/node consistency. Constrain the expected displayed cost to at most B, and maximize the displayed score. Every deterministic configuration, and every correlated mixture of configurations, maps into this local-marginal LP. Consequently

    J≤U_local(B)+κ                                         (8)

is a conservative bound for the declared control class, including hard-budget configurations as a subset. On a tree, every locally consistent family has a global distribution: sample a root from m_root and each child using `m_parent,child/m_parent` on positive-mass states. Zero-mass events are irrelevant. Thus on trees the LP is exact for the **randomized-configuration expected-budget relaxation**. It is not necessarily exact for a hard budget on every realization or for physically replayable time sharing. On cyclic graphs it remains an outer bound and can be loose.

A directly checkable dual certificate avoids trusting a numerical optimum. For β≥0 and arbitrary edge-to-node functions λ_ij→i, set

    α_i=max_a[J_i(a)−βc_i(a)+Σ_j λ_ij→i(a)],
    ζ_ij=max_ab[J_ij(a,b)−βc_ij(a,b)
                         −λ_ij→i(a)−λ_ij→j(b)].

Messages cancel on every configuration, giving

    U=J0+βB+Σ_i α_i+Σ_(ij)ζ_ij+κ.                        (9)

The empty-edge case recovers the closure packet's independent-module dual. This is established finite LP/graphical-model machinery applied to a precisely enlarged calibration contract, not a new abstract duality or a proof that hidden interactions were acquired. A fixed common affine detector can be incorporated in J; changing detector channels must enlarge the uncertainty set.

### Exact thermal-compatible falsifier and repaired toy

Two binary heater controls can share one reacting hotspot. In a purely synthetic positive Arrhenius model, take `E/Rgas=5000 log 2 K` and `T(x)=5000/(10−x1−x2) K`. Relative to 500 K, the thermal rate is exactly

    J(x)=2^(x1+x2)=1+x1+x2+x1x2.

One-heater calibrations identify baseline one and two individual increments one; their additive extrapolation predicts three at (1,1), while the actual entirely thermal rate is four. This rejects the additive-model transfer, not a known independently qualified reactor-array experiment.

Measuring the pair response supplies J12(1,1)=1. At expected cost budget B=1 with c_i=x_i, a half-mixture of (0,0) and (1,1) gives expected score 5/2. Equation (9) certifies the same value with β=3/2 and messages λ_12→i(x_i)=x_i/2. Each node and edge maximum is zero; J0+βB=5/2. The best hard-budget configuration has score two, so the mixture bound is explicitly not an acquired hard-budget emulator.

Higher-order closure remains necessary. For three controls, the two positive response worlds

    J_A=1+Σxi+Σ_(i<j)xi xj,
    J_B=J_A+x1x2x3=2^(x1+x2+x3)

agree on every one- and two-heater calibration with other controls off, but give seven and eight at (1,1,1). J_B has the same ordinary Arrhenius construction with `T=5000/(10−Σxi)`. Pair calibration alone cannot justify κ=0. A physical locality/no-higher-interaction theorem, further factor calibration, or a uniform acquired κ is indispensable. This is the decisive falsifier to an overstrong sparse-calibration capability claim.

The paid calibration scale is Σ_i K_i+Σ_(ij)K_iK_j mode exposures per replicate, plus baseline, detector, drift, held-out joint and omitted-interaction checks. The same raw joint records and uncertainty sets must be supplied to incumbents. A factor graph does not create independent specimens, and stationarity/thermal history cannot be inferred from repeated sensor readings.

## 3. A continuous hydraulic control class under a joint response law

The closure packet supplies only a finite dark library. A finite measured constitutive law can sometimes bound a continuous control class without enumerating every mode. This requires a verified law over the entire allowed range; it is not an extrapolation from isolated favorable points.

For a specified stationary, linear, reciprocal passive two-port hydraulic module let

    L=[[A,K],[K,C]],  A,C>0, K≥0, K²≤AC,
    source pressure=P≥0,  receiver pressure=−p,
    0≤p≤KP/C.

Output power and source input are

    J(p)=KPp−Cp²,     c(p)=AP²−KPp.

The legal range gives nonnegative receiver flow and nonnegative input. Include an off mode J=c=0. For every 0≤β≤1, completing the square gives the exact support

    sup_legal/off [J−βc]
       =max{0,P²[(1+β)²K²/(4C)−βA]}.                    (10)

The interior optimizer is `p=(1+β)KP/(2C)`, which lies in the legal range. For β≥1 the legal maximum is nonpositive before the off mode, so its support is zero. Independent qualified modules with total input budget B satisfy

    ΣJ_i ≤ inf_(0≤β≤1){βB+Σ_i max(0,
        P_i²[(1+β)²K_i²/(4C_i)−βA_i])}.                 (11)

This is an exact continuous-mode version of the resource dual under the stated stationary constitutive contract. With uncertain coefficients, take the supremum over the **same acquired joint matrix uncertainty set** inside each support. Independently optimistic interval endpoints can combine mutually incompatible specimens or loads. Intermodule coupling needs the joint-response treatment of Section 2 or an acquired residual bound.

Equation (11) is a conditional decision upper bound, not a new momentum-transfer mechanism, microscopic proof or device efficiency advantage. The source's original fixed-primary-flow loss-replacement task differs from the fixed-source-pressure class here and must not be silently exchanged. Loaded work/retention, wall motion, leakage, electrical/thermal control, calibration, settling and fixed-task incumbent costs still need measurements. Coquinot et al.'s 2025 primary publication already reports theoretical/simulation flow tunnelling, so the broad physical operation is prior art.

## 4. Exact surviving and incompatible transfers

The incoming Picone identity supplies a constructive affine-direction flux and a new exact restricted G family; it does not provide a scalar lower certificate for every phase, bypass N830's storage-class no-go, or prove G quasiconvex for arbitrary gradients. The independent-module closure bound can be generalized to calibrated joint factors; it does not acquire those factors from local marginal data. Passive hydraulic response can supply a continuous decision envelope only after the full joint response law and its valid load range are acquired.

There is no justified Picone-to-Arrhenius theorem: the latter reaction-rate/detector interface is not a homogeneous rank-one-convex gradient energy. There is no automatic thermodynamic proof from a PSD response matrix alone, and no transfer from hydraulic work to a retained atomic-repair kernel. These incompatible interfaces are retained rather than linked through shared dual vocabulary.
