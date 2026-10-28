# Coherent calibration discovers a near-optimal encoder for unrestricted recovery

27 October 2026. Constructive mathematical bridge, not a hardware experiment or a novelty claim. The calibration interface is **strictly stronger** than ordinary labelled, output-only probes. The retained logical reference and encoder control are used only in calibration; neither bypasses noise with the deployed payload.

## 0. Result, access contract, and what is newly assembled

Let N:L(C^p)→L(C^s) be a stationary, independently reset unknown CPTP channel. Let V0:C²→C^p be a known isometry and

    V_x=E(x)V0,   E(x)=Σ_(i=0)^3 x_i E_i,   x∈S³⊂R⁴,

be a physically executable quaternion family: every real unit x makes E(x) unitary. The known E_i and V0 have supplied implementable circuit descriptions. Their relative phases, not merely their individual quantum channels, are calibrated. Define E_x=N∘Ad_(V_x) and

    ℓ_opt(x)=min_(D:C^s→C² CPTP) [1−F_e(D E_x)],
    ℓ_*=min_(x∈S³) ℓ_opt(x).

No receiver syndrome measurement is imposed. The decoder comparator is the full CPTP class. A supplied valid integer R bounds the normalized Choi rank of **each of the four anchor channels** E_i=N∘Ad_(E_i V0). No spectral floor, environment access, unknown-source controlled gate, inverse, adjoint, or supplied support basis is available.

The stronger calibration resource is the ability to prepare a logical Bell pair on A,L; encode L with V0; prepare I in (1/2)Σ_i|i>; apply the known controlled E_i to the physical data; send **only the physical data** through N; and retain I,A coherently outside N. The normalized state on I,A,B is Γ. One such preparation costs one actual call to N. Arbitrary coherent receiver processing of stored copies is allowed. A is one retained qubit and I is two; protected memory or a quantum link/co-location is an additional physical resource, not free ordinary source access.

**Encoder discovery.** For 0<α,e≤1, a finite procedure outputs a classical, explicitly specified x with

    E ℓ_opt(x) ≤ (1+α)ℓ_*+e.                              (T1)

It consumes

    n_s=ceil[40960 D_s(log(2D_s)+1)/(α e)],
    k=min(s,8R), d=8k, r_s=min(4R,d),
    D_s=2^ceil(log₂(d r_s)) < 512R²                        (T2)

coherent calibration calls. Receiver gates and classical bit operations are polynomial in R,1/(αe),log s and requested precision, in addition to the supplied encoder-preparation/control costs. The finite global encoder net has O((αe)^−3/2) points, but these cost only classical SDPs: **there is no net-size source-query multiplier**. An alternative high-confidence version below returns ℓ_opt(x)≤(1+α)ℓ_*+e with probability at least 1−β, using O(R² log(R/β)/(αe)) calls and confidence-scale implementation accuracy.

**Ordinary deployment.** Discard the compressed decoder used during discovery. After x has been selected, acquire a fresh ordinary six-input Bures bank for E_x and jointly reduce that whole bank with the actual independent payload output. The received direct-CPTP theorem then gives, conditional on x and averaged over this fresh bank,

    ℓ_deploy(x) ≤ (1+θ)ℓ_opt(x)+e_d.                      (T3)

Use the valid deployment rank bound **R_d=4R**, not R, unless an additional uniform R bound was supplied. With α=θ=γ/3, e=ε/4, e_d=ε/2, 0<γ,ε≤1, the resulting ordinary deployed channel, averaged over discovery and fresh recovery banks, obeys

    ℓ_deploy ≤ (1+γ)ℓ_*+ε.                               (T4)

There is one payload call in addition to the calibration calls. Each later payload needs its own fresh recovery bank, unless the separate one-common-frame batch theorem is explicitly used. The selected encoder is reusable classical information; a reusable physical-space decoder has **not** been learned.

For s=1 the source is constant and ℓ_opt(x)=3/4 for every x. A fixed maximally mixed logical replacement is optimal, with no learning bank needed. The remainder treats s≥2.

### Imported, already received primitives

This proof imports the exact arbitrary-operator joint-reduction identity, actual random-purification channel, finite-Clifford tomography and finite-feasible decoder optimization/known-matrix synthesis from `../direct_cptp_bures_bridge_20261027/DIRECT_CPTP_BURES_RISK_RECOVERY.md`, Sections 1, 5 and 6. Its primary-source attributions and circuit scope remain in that received file. Those representation-theoretic circuits are not proved again here. The explicit global S³ geometry comes from `../ordinary_encoder_global_petz_discovery.md`, not an unknown-optimum oracle. The stronger coherent-control and transfer boundaries are retained from `../coherent_program_joint_encoder_recovery_discovery.md` and `../coherent_program_deployment_transfer_budget.md`.

The new assembly is a **single coherent encoder Choi state**, a positive full-decoder loss, uniform Bures-risk transfer across both encoder and decoder, a classical global net/SDP search, and a fresh ordinary deployment stage. It does not promote the older ordinary-probe theorem to a stronger access model silently.

## 1. The physical state and its exact ordinary-deployment contraction

Choose any Stinespring isometry W_N:C^p→C^s⊗H_E for N and set

    |ψ_i>_(A B E)=(id_A⊗W_N E_i V0)|Φ₂>,
    |Ψ>_(I A B E)=(1/2)Σ_i |i>_I |ψ_i>,
    Γ=Tr_E |Ψ><Ψ|.

All |ψ_i> are unit vectors and the orthogonal control labels make |Ψ> normalized. The environment is a proof system and is never supplied. For every real unit x,

    (<x|_I⊗I)|Ψ>=(1/2)(id_A⊗W_N V_x)|Φ₂>,
    <x|Γ|x>=J_x/4,                                      (1)

where J_x is the normalized Choi state of E_x. The real coefficients and coherent relative phases are essential. In particular Tr<x|Γ|x>=1/4, independent of x. This is not a deterministic accepted Choi oracle: physically postselecting x would have probability 1/4 and all failed preparations would still cost calls. The algorithm does **not** postselect; it tomographs the whole Γ.

For a CPTP decoder D define

    Q_D=I_(A B)−(id_A⊗D†)(Φ₂),
    B_(x,D)=4|x><x|⊗Q_D.

Since id⊗D† is completely positive and unital,

    0≤Q_D≤I,   0≤B_(x,D)≤4I,
    Tr(Γ B_(x,D))=1−F_e(D E_x)=:ℓ(x,D).                  (2)

The identity term must be retained. For an arbitrary estimated density τ, even one inconsistent with any encoder family or TP source, define

    R_τ(x,D)=Tr(τ B_(x,D))∈[0,4].                        (3)

Positivity of (3), not a signed process reconstruction or postselection normalization, is the reason one Bures estimate suffices.

## 2. Four anchor ranks control the entire coherent family

Let ω_i=Tr_(A B)|ψ_i><ψ_i|. Purity gives rank ω_i=rank J_i≤R. The environment marginal of |Ψ> is

    ω=(1/4)Σ_i ω_i,

so rank Γ=rank ω≤Σ_i rank ω_i≤4R. Also

    Γ_B=(1/4)Σ_i E_i(I₂/2),
    rank E_i(I₂/2)≤2 rank J_i≤2R,
    rank Γ_B≤8R.                                        (4)

For any positive bipartite matrix, its support is contained in the full first factor tensor the support of its second marginal. Thus Γ is supported on I⊗A⊗S, where S=supp Γ_B and dim S≤k.

Every |ψ_i> has environment support in supp ω. Every linear combination |ψ_x>=Σ_i x_i|ψ_i> therefore has that same environment support, proving

    rank J_x≤4R for every x.                             (5)

Every ordinary output of every E_x likewise lies in S. One way to see this is that all N-Kraus images of all E_i V0 lie in the span of the anchor output supports, and the images of V_x are their linear combinations.

The factors four and eight are genuinely necessary from anchor information alone. Take input control₂⊗tag₂⊗logical₂, V0=|Φ₂>_(control,tag)⊗I₂, and E_i=(I,iX,iY,iZ) on control. The four states b_i=(E_i⊗I)|Φ₂> form an orthonormal Bell basis. Let N have Kraus operators

    K_i=(|i>_(output label)⊗I₂)(<b_i|⊗I₂),

with output dimension eight. Each anchor is an isometry and has Choi rank one. But Γ has rank four, Γ_B has rank eight, and a generic x with all coordinates nonzero gives J_x=Σ_i x_i² |i><i|⊗Φ₂ of rank four. The finite checker verifies these facts directly.

## 3. One physical common frame, preserving the known control and reference

Mathematically extend S to a k-dimensional subspace and write its inclusion as V:C^k→C^s; V is not given to the learner. Acquire n_s independent Γ copies and keep all I,A,B systems unmeasured. Apply **one** known joint reduction R_(s→k)^(n_s) to all B registers, leaving I,A untouched. The imported arbitrary-operator identity extends with these untouched references and gives the exact mixture

    ∫ Γ_U^⊗n_s dU,
    Γ_U=(id_(I A)⊗Ad_U)(Γ_0),                            (6)

where Γ=(id⊗Ad_V)(Γ_0). It is not n_s independently twirled copies. Conditional on the mathematical U, the whole-IAB samples are iid copies of Γ_U in dimension d=8k, with rank at most r_s. That is precisely the input interface for the actual random-purification/tomography primitive.

An unrestricted decoder can be restricted along V or U, and a compressed decoder extended by arbitrary replacement outside the support. Hence for every x,

    min_(D:C^k→C²) ℓ_U(x,D)=ℓ_opt(x),                    (7)

and the joint minimum is ℓ_*. No implemented V†, recovered U, source inverse, or learned support basis is required. All I,A bases remain physically known because those registers were untouched by reduction.

After (6), run random purification on the **whole homogeneous IAB bank**, not on four different anchor banks and not on B alone. It creates the received mixture of n_s copies of a purification in C^d⊗C^r_s. Whole-state finite-Clifford tomography then produces a genuine density τ on IAB. Analysis may condition on U and on the purification variable; all bounds below are uniform in both. The purification environment is created locally by a known channel, not read from N.

## 4. One Bures estimate controls all encoder/decoder policies at once

Write f(ρ,τ)=||sqrtρ sqrtτ||₁ and δ=1−f(Γ_U,τ). Choose Uhlmann purifications u,v with ||u−v||²=2δ. For every x,D, reverse triangle inequality applied to sqrt(B_(x,D))u and sqrt(B_(x,D))v gives

    |sqrtℓ_U(x,D)−sqrt R_τ(x,D)|≤sqrt(8δ).                (8)

This is simultaneous over the entire feasible policy class; it is not a union bound over a grid. Let (x_hat,D_hat) be a feasible η-optimal pair for the empirical problem. Twice using (8), with a true minimizing pair as comparator, gives pointwise

    sqrtℓ_U(x_hat,D_hat)
      ≤sqrtℓ_*+2sqrt(8δ)+sqrtη.                          (9)

If Eδ≤m, Minkowski and Young yield, for 0<α≤1,

    E ℓ_U(x_hat,D_hat)
      ≤(1+α)ℓ_*+128m/α+4η/α.                            (10)

Indeed z=2sqrt(8m)+sqrtη obeys z²≤64m+2η, and 1+1/α≤2/α. The same result holds pointwise on δ≤m. Since ℓ_opt(x_hat)≤ℓ_U(x_hat,D_hat), (10) proves the desired encoder-quality statement, without retaining D_hat for future physical data.

This transfer is uniform even though τ need not obey the physical contractions (1). Physical true loss is at most one; empirical risk can be as large as four. Confusing these bounds would undercharge net curvature and Bures transfer.

## 5. Certified global classical optimization: no extra source queries

For each fixed decoder, R_τ(x,D)=x^T G_D x for a real symmetric 4×4 matrix G_D. Equation (3) for all real unit x implies 0≤G_D≤4I. At a global empirical minimizing pair (x*,D*), x* is a minimum eigenvector of G_(D*). For any unit y at chord distance at most h,

    R_τ(y,D*)−R_τ(x*,D*)
       ≤4[1−|<x*,y>|²]≤4h².                            (11)

The decoder-optimized landscape may be nonsmooth; it is not differentiated. Use all eight signed cube faces in R⁴, grid their three free coordinates at spacing 2/M0, and normalize, where

    h²≤η/8,   M0=ceil(sqrt(24/η)),
    K≤8(M0+1)³.                                         (12)

For a target x choose a largest absolute coordinate, rescale it to the corresponding signed face, round the other three coordinates, then normalize. The rounding distance is ≤sqrt3/M0. Normalization restricted to that face is 1-Lipschitz, since the line segment stays at norm at least one. Thus (12) is a genuine chord-h net. It includes rational direction vectors whose normalized outer products xx^T are rational.

At each grid x, solve the decoder SDP to certified additive risk accuracy η/2, and choose the least achieved **certified primal objective**. The grid costs at most η/2 by (11), so the selected feasible pair is η-optimal. Any additional objective-comparison rounding must be paid within that η/2 solver/comparison budget, or eliminated by exact rational comparison. There are K conventional SDPs and no new calls to N. Coordinate descent, local optimization, or a floating solver success flag does not substitute for this global/certified contract.

### Explicit positive decoder coefficient and finite certificates

Put σ_x=<x|τ|x> on A⊗B, t_x=Tr σ_x≤1. Let S swap A,B into B,A order. For the unnormalized decoder Choi C on B⊗Q, define

    H_x=4[σ_(x,B)^T⊗I₂−(1/2)S σ_x^T S†],
    minimize Tr(H_x C),   C≥0, Tr_Q C=I_k;               (13)
    maximize Tr Y,        H_x−Y⊗I₂≥0, Y=Y†.             (14)

The transpose is the **full** transpose, not a partial transpose. The Bell identity makes (13) equal R_τ(x,D). The universal inequality σ_AB≤2 I_A⊗σ_B proves

    H_x≥0,   ||H_x||≤4,   Tr H_x=6t_x≤6.                (15)

For completeness, prove that inequality on a pure state using its at-most-two Schmidt terms and Cauchy–Schwarz, and sum a pure-state decomposition for mixed σ. Strict feasible points are C0=I_k⊗I₂/2 and Y0=−I_k. The feasible primal set has trace k and is compact. A near-optimal dual can be restricted to polynomial norm: Y≤4I and Tr Y≥−1 imply λ_min(Y)≥−1−4(k−1).

The rational τ construction below and rational xx^T allow exact rational H_x coefficients with polynomial bit length. The received finite SDP machinery therefore applies with the objective trace bound 6 in place of 3/2. Here is an explicit sufficient repair for desired per-grid tolerance ζ_sdp≤η/2. Obtain a rational weak primal C~ with λ_min≥−κ, ||Tr_Q C~−I||≤κ, a weak dual with slack defect ≤δ_dual, and weak primal/dual gap ≤ζ_sdp/8. Set

    λ=ζ_sdp/40, κ≤ζ_sdp/480,
    e_round≤ζ_sdp/640, δ_dual≤ζ_sdp/(8k).

Correct the affine constraint by C1=C~−(Tr_Q C~−I)⊗I₂/2, mix C2=(1−λ)C1+λC0, round to Hermitian operator error e_round, and repeat the affine correction. The final rational C is exactly TP and strictly PSD: its margin before rounding is ≥λ/2−3κ/2, and the last perturbation is ≤2e_round. Shift the dual down by δ_dual I. The upward primal-objective change is at most 3κ+5λ+12e_round (C1's objective is at least −9κ, while C0's is at most four), and the dual shift costs kδ_dual. Together with the initial gap these total at most 0.4ζ_sdp. The slack permits certified comparison arithmetic. Finally verify the actual rational primal/dual gap ≤ζ_sdp. Interval/certified eigenvalue bounds, not solver status alone, certify the inequalities. If coefficients are instead approximated, a separate bound ||H~−H||≤h changes every feasible objective by at most kh; pay both optimization comparisons and dual feasibility explicitly.

No decoder needs to be synthesized during encoder discovery. The fresh ordinary deployment stage uses its own received feasible SDP and known-matrix synthesis. Factoring (13)'s solution merely to evaluate a Bell risk is unnecessary.

## 6. Actual tomography, finite expected-risk allocation, and gates

Pad d r_s into the power-of-two D_s. Apply the received random-purification channel and finite-Clifford pure-state tomography in that dimension. Its actual measurement record is X=(D_s+1)P−I, where P is the Born-selected Clifford basis projector. The received moment bounds and matrix Bernstein bound are

    E X=Φ, E(X−Φ)²≤2D_s I,
    Pr(||Xbar−Φ||≥t)≤2D_s exp[−n_s t²/(5D_s)], 0<t≤1.

A top-vector estimate with total backward Hermitian/vector-normalization error a_eig, followed by tracing the known local purification register and TP completion of padding leakage, yields a genuine density τ and

    E[1−f(Γ_U,τ)]≤40D_s[log(2D_s)+1]/n_s+8a_eig².        (16)

Use a finite normalized rational-vector outer product to describe τ; normalization by its positive rational squared norm preserves exact density positivity and trace. The arithmetic error is already included in a_eig. No empirical eigengap promise is needed.

For (T1), set

    m≤αe/512, η≤αe/16,
    n_s as in (T2), a_eig²≤αe/8192.                      (17)

The two terms in (16) are each at most αe/1024. Equation (10) then contributes e/4 from tomography and e/4 from optimization. Let ν_s≤e be the total **unhalved diamond discrepancy** of the implemented discovery/encoder-label-output channel from the exact-reference procedure. It includes all n_s Bell/control preparations, the one B-only joint reduction, the one whole-IAB random-purification channel, truncated/rounded Clifford sampling, and finite quantum operations not already included in (16). Telescoping bounds their sum. The resulting distribution of the finite label x changes in total variation by at most ν_s/2. Since ℓ_opt(x)∈[0,1], its expected value changes by at most ν_s/2. This proves (T1).

The exact Haar variable in (6) is an analysis decomposition. An approximate reduction need not retain a literal U. Its finite error is transferred only at the complete physical-protocol/output-distribution level as above. Eigenvector and SDP arithmetic already paid in m,η must not be charged twice; unaccounted errors must not be omitted.

A deterministic source cap is n_s. Exact finite-bit uniform Clifford sampling need not be falsely asserted: use a capped generator with failure assigned to a fixed fallback, charge twice its total-variation discrepancy to ν_s, and use the received finite gate synthesis. The error allocation can be made over an explicit polynomial gate cap G with per-operation discrepancy O(ν_s/G), and over n_s preparations with per-preparation discrepancy O(ν_s/n_s). These are ideal computational approximation requirements, not a proof that unknown hardware errors obey them.

Initial coherent storage is n_s(ceil(log₂s)+3) qubits, plus preparation/receiver workspace. The controlled encoder preparation is called n_s times. Subsequent Schur reduction, purification and Clifford circuitry have the imported polynomial precision/gate bounds. Dense accumulation of tomography matrices costs at most polynomial work in n_s,D_s; K SDPs of size 2k and polynomial coefficient precision are also polynomial for the fixed three-dimensional encoder parameter space. **Arbitrary supplied encoders may themselves have large circuit cost**; charge n_s times their controlled-preparation cost and ordinary-bank/payload encoder costs separately. No polynomial-in-log p synthesis claim for arbitrary V0 or E_i is made. Multiple encoder slots grow the net dimension and can destroy this polynomial scalability.

## 7. High confidence in the classical encoder, not in a realized decoder bank

An optional confidence theorem is possible because the exported result is x, not a decoder in an inaccessible frame. Choose

    m=αe/256, η=αe/8,
    a_eig≤sqrt(m)/4,
    n_s≥ceil[(80D_s/m) log(4D_s/β)].                     (18)

The received Bernstein/top-vector proof, with t=sqrt(m)/4, makes δ≤m except probability β/2. On that event (10) gives ℓ_opt(x)≤(1+α)ℓ_*+e. Implement the entire discovery-to-label channel to unhalved diamond discrepancy ν_s≤β. This changes the probability of any label event by at most β/2, proving

    Pr_x{ℓ_opt(x)≤(1+α)ℓ_*+e}≥1−β.                      (19)

The event is frame-invariant by (7) and is a deterministic property of the classical encoder label. It is therefore a meaningful event in the physical output distribution even though no U is exposed. This does **not** imply quality for every exposed tomography record or every future realized decoder bank. The decoder-loss event from a virtual frame alone would not have this same interpretation. Known encoder implementation errors must still be paid in the later physical-protocol budget or in a separate deployment-transfer premise.

Confidence accuracy is additional: an O(e)-accurate quantum implementation does not preserve a much smaller β. The precision increase is logarithmic in 1/β within the imported computational model. The expected theorem (T1) does not need this β parameter or its extra confidence factor.

## 8. Fresh ordinary deployment and the complete source bill

Condition on the selected x and discard all discovery quantum systems, including D_hat. Equation (5) gives a valid fixed-source Choi-rank bound R_d=4R. Apply the received ordinary-six-input direct-CPTP Bures theorem with parameters θ,e_d. Its deterministic additional calibration cap is

    k_d=min(s,2R_d)=k, r_d=min(R_d,k_d),
    D_d=2^ceil(log₂(k_d r_d))<64R²,
    n_d=ceil[15360 D_d(log(2D_d)+1)/(θe_d)],
    N_d=6n_d.                                           (20)

The bank contains ordinary encoded ±X,±Y,±Z probes with no retained reference or coherent encoder control. After the actual payload has been encoded using x and passed through N, apply a **new single joint reduction** to those N_d outputs and that payload, with its external reference untouched. Fresh Bures tomography, a fresh ordinary CPTP SDP and a compiled known decoder operate in this new common frame. Conditional on x this is exactly the received theorem; selection history is independent of the fresh reset bank and payload. Thus (T3) holds.

Combining (T1),(T3) gives

    E ℓ_deploy ≤(1+θ)(1+α)ℓ_*+(1+θ)e+e_d.               (21)

With α=θ=γ/3, e=ε/4 and e_d=ε/2, (1+γ/3)²≤1+γ and (1+γ/3)ε/4+ε/2≤5ε/6<ε. Both stages' finite implementation errors were already included in their e,e_d guarantees; the spare ε/6 is simply unspent, not authorization for unmodelled errors. Total source calls for one discovered encoder and one deployed payload are

    n_s + 6n_d + 1 = O(R² log(2R)/(γε)) + 1.             (22)

For the confidence route, with probability at least 1−β over discovery, (21) without the discovery expectation bounds the **conditional fresh-bank averaged** ordinary deployed channel. It does not certify each new realized bank. Each additional payload ordinarily costs another N_d+1 calls and consumes that fresh bank. Later batch amortization is a separate interface and must charge its shared frame, latency, memory and whole-block precision.

It is invalid to apply the old compressed D_hat to separately reduced later data. A new coherent Γ bank could alternatively estimate a fixed-x decoder in a new frame jointly containing the payload, but that different implementation is not needed here and is not assumed to reuse an old frame. No noisy payload is retained in I or A from discovery.

## 9. Qualified calibration-to-ordinary-deployment transfer

The exact theorem assumes the stipulated coherent source/control contract. Unknown relative phases, control leakage, memory noise or source drift need a separate qualification statement; calibrating each E_i as a stand-alone quantum channel does not determine its controlled relative phase.

A robust conditional version is available. Suppose an **actual** stationary coherent calibration state Γ~ is learned, with supplied valid actual rank/support bounds adequate for its reduction/purification algorithm. Suppose for the same physical decoder class and the actual ordinary deployed encoder family there is a separately established uniform transfer bound

    sup_(x,D) |Tr(Γ~ B_(x,D))−ℓ_actual-deploy(x,D)|≤ζ.     (23)

Then a calibration selector with risk ≤(1+α)inf_(x,D)TrΓ~B_(x,D)+e yields

    ℓ_actual-opt(x_hat)≤(1+α)ℓ_actual,*+e+(2+α)ζ.         (24)

The proof pays ζ for the returned pair and (1+α)ζ for the comparator. For an averaged finite-implementation version, apply this ideal-selector argument first and then transfer the bounded physical quantity ℓ_actual-opt(x)∈[0,1] through the output-law discrepancy, costing ν_s/2. Transferring the possibly-four-valued calibration risk itself instead would cost up to 2ν_s; the main ν_s/2 budget must not be reused for that larger surrogate. It does not require that the actual deployed encoder loss remain exactly quadratic; only the calibrated surrogate is quadratically optimized. After fresh ordinary deployment, (24)'s added term is multiplied by (1+θ), and the ordinary deployment theorem needs its own valid actual-source rank bound. The four ideal anchor ranks alone cannot promise these facts for arbitrary faulty controls.

One sufficient transfer certificate, separate from rank qualification, is

    ||Γ~−Γ_ideal||₁≤ξ,
    sup_(x,D)|ℓ_ideal(x,D)−ℓ_actual-deploy(x,D)|≤ζ_dep.

Since Tr(Γ~−Γ_ideal)=0 and 0≤B≤4I, (23) follows with

    ζ=2ξ+ζ_dep.                                         (25)

A uniform unhalved diamond distance δ_dep between the ideal and actual ordinary encoder-source channels suffices for ζ_dep≤δ_dep/2 by the Bell test and decoder contractivity. Equation (25) concerns a single calibration state. It is **not** itself a low-rank certificate: arbitrarily small full-rank contamination can invalidate exact-rank purification assumptions. Either the actual rank/support promises must be separately supplied, a paid approximate-support theorem must be explicitly imported, or the full n_s-copy preparation discrepancy must be charged to ν_s (which can be much stricter than a single-state transfer bound). This proof makes none of those costs vanish.

Operationally acquiring/qualifying (23) using ordinary output/process measurements can have ε^−2-scale costs when ζ=O(ε), and dependence on the actual physical dimension, destroying the advertised fast source-query advantage. A selected-candidate holdout certifies that candidate's performance, but cannot establish uniform global transfer or optimality. The Õ(R²/(γε)) theorem is therefore conditional on a qualified stronger calibration interface; it is not a recipe for certifying unknown faulty hardware for free.

## 10. Fair comparison and precise exclusions

1. The equally informed coherent conventional learner receives the **same** Bell/control memory, calibrated relative phases, quantum output access, source calls, and global optimization rights. It may tomograph the same Γ or its operational Gram and perform the same certified encoder/decoder search. This construction is such a tomography-plus-SDP method after quantum dimension reduction, not a separation from that alternative.
2. A fully known channel plus global encoder search and unrestricted decoder SDP is an information-stronger comparator. Physical-space process tomography may compile a reusable decoder and can be preferable for many payloads, while its output-dimension, control, memory and finite-precision costs must be honestly charged. There is no established source-complexity lower bound for this joint encoder problem here.
3. Compared with the old ordinary net-and-Petz construction, this bridge removes its factor-two recovery loss and net-size quantum-query multiplication, but it does so under a genuinely stronger coherent calibration interface and imported collective receiver primitives. It does not prove ordinary-probe access can emulate that interface at the same cost.
4. No complete environment is reconstructed; there is nevertheless explicit state tomography of a reduced operational Choi state. Rank R can grow exponentially with physical qubit count. No generic-noise scalability, experimentally competitive constants, robust hardware threshold, unknown-rank adaptation, temporal-drift robustness, or first-in-history environment-free recovery claim is made.
5. The decoder benchmark is entanglement infidelity. A separate framed or complete-error theorem may be composed only with its own interface and record/key scope. This note does not identify the generic unframed diamond-optimal decoder.
6. Calibration references bypass noise; deployed unknown information does not. No controlled N, N†, N^−1, postselection without its probability, supplied support basis, coherent reversal of measured tomography/SDP work, or reused unknown frame is hidden in the construction.

## Evidence and reproduction

`coherent_encoder_bures_checks.py` and its JSON output test the coherent contraction and positive-effect identities on actual Kraus channels, tight rank inflation, arbitrary-density SDP coefficients, Bures risk transfer, stationary-net geometry, and scalar sample/error allocations. They do not execute collective Schur circuits, solve every SDP, qualify hardware, or establish practical source counts. Independent review and its hash-bound receipt are separate files; no received source proof is changed by this work.
