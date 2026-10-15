# Exact capital connections: finite controls, accessible relaxation and phase index

15 October 2026. Main pin `b7cada92d2eb304578be5ed974f1e44b10a89928`. New deductions below are separate from producer claims. Historical priority, external mathematical correctness and physical capability remain UNKNOWN. Standard inverse updates, Gaussian integration and Schur elimination are established machinery.

## 1. A finite-action response family from forward measurements

Let A0 be any invertible real n-by-n matrix, possibly nonreciprocal. Suppose an **acquired global constitutive contract**, valid over a declared set of controls, is

    A(S)=A0+V S Vᵀ,      A(S)x(S)=b,

where V has r independent columns, S is a known r-by-r control matrix, b is unchanged and every admitted A(S) is invertible and physically settled. Symmetric S describes stiffness/conductance changes; the algebra does not require symmetry. Static invertibility alone does not certify dynamic stability or physical accessibility.

Acquire calibrated responses to b and the r columns of V, with the same loaded A0:

    x=A0⁻¹b, W=A0⁻¹V, C=VᵀW, t=Vᵀx.

Only the required objective/sensor rows of x,W and the projections C,t are needed. Then for every admitted finite control,

    d(S)=(I+SC)⁻¹ S t,
    x(S)=x−W d(S).                                      (1)

Proof: multiplication by A0+VSVᵀ gives

    (A0+VSVᵀ)(x−Wd)=b+V[St−(I+SC)d]=b.

The determinant identity gives invertibility of I+SC exactly when A(S) is invertible. Thus (1) is exact for the complete declared family; it is not a first-order sensitivity extrapolation. An alternative form `(S⁻¹+C)⁻¹t` is usable only when S is invertible and should not be imposed on zero/rank-deficient settings.

For a known score of the sensed state and a fixed finite control library, these data predict each candidate's finite score under the contract. They support an actual finite decision rather than merely a gradient. This is a consequence of established Woodbury machinery, not a new physical optimization principle or priority claim. A legal uniform affine family is a stronger premise than knowing the derivatives at one operating point.

For an exact falsifier to discarding that stronger premise, compare the scalar
families `A(p)=1+p` and `Ã(p)=1+p−(3/2)p²`, 0≤p≤1, with b=c=1.
Both are positive throughout that interval and have the same A(0)=1 and
A'(0)=1. Their local objective derivatives agree, but their scores at p=1 are
1/2 and 2. The nonlinear family is positive by concavity and its endpoint
values. A local derivative does not identify the finite response law. This is
a mathematical countermodel for a generic setting parameter, not for a knob
already acquired to be the actual conductance itself.

### A scoped correction to the merged PR90 abandoned-port illustration

The actual merged scientific-power native report, Section3 lines30–34, writes
the rank-one response difference as `−αvvᵀ/(1+αr)` for an arbitrary invertible
L, with `v=BᵀL⁻¹b`. The general real-matrix identity is instead

    Bᵀ[(L+αbbᵀ)⁻¹−L⁻¹]B
      =−α(BᵀL⁻¹b)(bᵀL⁻¹B)/(1+αbᵀL⁻¹b).             (1a)

The two factors coincide as transposes under reciprocity, or under an explicitly
supplied equality for the relevant vectors. Arbitrary nonreciprocal L does not
supply it. Take `L=[[1,1],[0,1]]`, B=I, b=e1, α=1. Its symmetric part is positive
definite, but the true difference is `[[-1/2,1/2],[0,0]]`; the displayed vvᵀ
formula gives `[[-1/2,0],[0,0]]`. This correction affects that abandoned-route
illustration only. It does not alter the separate quartic path-information
theorem. The original report is preserved unchanged; (1a) and this witness are
separately labelled current audit deductions. Equation(1) above does not make
the same symmetry substitution.

### Costs and relationship to port completion

The acquisition is r+1 settled source profiles, plus joint calibration, sensor readings, repeated blocks and model/range validation. For s objective rows and calibrated V-projections, the stored array has O(sr+r²) entries. One dense solve per candidate costs O(r³), with conditioning and target precision paid. Measuring V-projections may require extra actual sensor channels; a formal matrix product is not a native aggregator.

If the control space lies in the closure source's accessible port space, V=PL, then W=YL and C=LᵀHL are already determined by its port acquisitions. No extra V profiles are needed. The source's k+2 profiles can then support finite controls **if** the global affine load law is additionally acquired. For controls outside that span, a sensor at an endpoint does not imply a legal signed source injection there. In the general setting (1) requires that extra access. For a small number of legal directions, this is an equally informed forward-response comparator that needs no exterior-reciprocity-support premise; for a large control rank, its acquisition can be more expensive than a port-completed local gradient. No universal cost advantage is asserted.

The actual supplied 64-state fixture does **not** meet the port-span condition.
Its 30 conductance edges are supported among nodes0–11, whereas P injects at
nodes12–15, b=e0, c=e16 and the sensors cover0–16. The incidence control space
has rank at most11, but is disjoint from the P-column space. Starting from
scratch, a complete control-space response comparator therefore needs up to12
profiles including b, and the additional source access at control nodes must be
granted. Extending the already acquired six-profile adjoint experiment instead
adds up to11 direction profiles; its previous acquisition cannot be refunded.
The exact three-state port-supported fixture in our checker is a separately
declared construction, not a validation of that 64-state receiving hypothesis.

### Exact receiving-hypothesis falsifier and repair

Use the incoming closure counterexample

    A±=I±e2 e4ᵀ, b=e1, c=e2, P=[e3,e5], v=e1−e4.

Both symmetric parts are strictly positive. Responses to b,c,P agree, H=I, yet after adding pvvᵀ,

    J±(p)=cᵀ(A±+pvvᵀ)⁻¹b=∓p/(1+2p), p≥0.             (2)

The baseline port protocol cannot decide the sign because its support assumption fails. If an **additional legal v-source** is granted, `A±⁻¹v=v±e2`, `vᵀA±⁻¹v=2`, `vᵀx=1`; equation (1) then recovers (2) exactly. This repairs the information interface by adding a discriminating probe. It does not infer that the original interface already permitted it.

## 2. A joint-error finite-decision certificate

Let U be the sensed rows of W and x_o the sensed baseline state. Suppose one simultaneous acquired uncertainty event supplies

    ||C−Ĉ||≤εC, ||t−t̂||≤εt,
    ||U−Û||≤εU, ||x_o−x̂_o||≤εx.

The norm is a consistently induced Euclidean matrix/vector norm. These can be deterministic bounds or simultaneous confidence bounds; independent marginal error bars do not automatically supply this event. Define

    Ĝ=I+SĈ, d̂=Ĝ⁻¹St̂, γ=||Ĝ⁻¹|| ||S|| εC.

If γ<1, the true denominator is invertible and

    K=||Ĝ⁻¹||/(1−γ),
    ||d−d̂||≤K||S||(εt+εC||d̂||)=εd,
    ||x_o(S)−[x̂_o−Ûd̂]||
      ≤εx+εU||d̂||+(||Û||+εU)εd.                       (3)

Proof: the inverse perturbation bound gives ||G⁻¹||≤K, while

    G(d−d̂)=S(t−t̂)−S(C−Ĉ)d̂.

Then expand the output difference as baseline error, `(U−Û)d̂`, and `U(d−d̂)`. No probabilistic independence is used. A known L-Lipschitz objective converts (3) to an objective error bound. A separately acquired model-discrepancy bound must cover departures from the global affine law, source/loading drift and the valid operating range. Near a response pole the denominator test can fail and the resulting bound can be large; source precision is not free.

For a finite list Sj, simultaneous score intervals and resource intervals support an ordinary conservative comparison. A candidate lower score above an incumbent upper score establishes improvement only within those acquired intervals and the declared cost/task class. This supplies a concrete receiving interface for the existing FS decision-level closure contract. It does not identify a microscopic mechanism or acquire the intervals by writing a formula.

## 3. What the same inverse update does and does not give for transport

The incoming transport model is an equilibrium common-host Gaussian calculation. Its K is a symmetric positive definite energy Hessian; a generic nonreciprocal response A cannot replace K. Let P inject r physically accessible mechanical support coordinates, H=PᵀK⁻¹P, and m_s=PᵀK⁻¹f_s for each occupied or constrained transition state s. For a passive support S≽0, Gaussian integration and the inverse update give

    ΔF_s=½m_sᵀ M(S)m_s+(kBT/2)log det(I+SH),
    M(S)=S½(I+S½HS½)⁻¹S½,
    ΔB_s=½[m_sᵀM(S)m_s−m_AᵀM(S)m_A].                  (4)

The square-root expression works at singular S. The determinant term cancels between states only under the common-K/common-coordinate classical assumptions. For a rank-one S=κwwᵀ, equation (4) reduces exactly to the source's χ(R_s−R_A). As stiffness tends to infinity on the full port space, M tends to H⁻¹. Thus accessible port means/compliance suffice for the conditional barrier calculation; neither the full hidden K nor the full force vectors need be reconstructed.

This is a limited information saving, not acquisition of the means: m_U and m_H refer to their actual constrained transition ensembles. Well-state port probes and the closure adjoint do not supply them. State-dependent Hessians also make the determinant terms differ; anharmonic/quantum ensembles and changing dividing surfaces need their own law. Physical source profiles, support modes, conjugate displacement sensors and the same operating regime must be acquired. A low-rank stiffness knob alone does not provide an independently readable transition ensemble.

### Same well and baseline barrier, opposite response

Take the exact two-coordinate harmonic model

    K=[[2,−1],[−1,2]], P=e1, f_A=(1,0), E_A^0=0.

Then H=2/3, m_A=2/3, R_A=m_A²/(2H)=1/3. Two possible useful transition states are

    World−: f_U=(0,1), E_U^0=1, R_U=1/12;
    World+: f_U=(2,0), E_U^0=2, R_U=4/3.

Both have exactly the same well data and the same baseline barrier B_U(0)=1, because the bare transition energies compensate their different relaxation. With κ=3/2, κH=1 and χ=1/2, but

    ΔB_U(World−)=−1/8,
    ΔB_U(World+)=+1/2.                                   (5)

Thus even a baseline barrier, all well responses and complete common K do not determine the sign of clamp benefit. Unknown transition forces or equivalent transition-ensemble moments cannot be supplied for free. All values are invented model inputs, not material data. Net transfer, useful lifetime, other damage paths and full resource costs remain additional obligations even after (4) is known.

## 4. Exact local phase Morse index after amplitude elimination

The incoming direction source proves, for F(A)=|A|⁴ and unit fourth mass on the probability-normalized 2π torus, a smooth globally amplitude-minimized branch near θ=k·x, k∈Z²\{0}. Its reconstructed Hessian has Fourier multiplier

    Λ_k(ξ)=4|k|²|ξ|²+8(k·ξ)²
                    −64|k|²(k·ξ)²/|ξ|², ξ≠0.            (6)

This follows by eliminating all density modes from the positive Laplacian block, not by optimizing a one-mode amplitude ansatz. The source's implicit-function and global-minimum identification hypotheses are retained; finite algebra alone does not establish them.

An exact consequence is a **finite negative index** at each fixed nonzero k. Write t=|ξ|² and z=(k·ξ)²/(|k|²t)∈[0,1]. Then

    Λ_k(ξ)=4|k|²[t(1+2z)−16|k|²z].

Negativity implies `t<16|k|²z/(1+2z)≤16|k|²/3`, so only finitely many integer frequencies can be unstable. Frequencies orthogonal to k are strictly positive. This is a local spectral statement, not global convexity of the direction value.

For k=(0,1), ξ=(p,q), multiply the multiplier by `(p²+q²)/4`:

    sign Λ = sign[(p²+q²)(p²+3q²)−16q²].                (7)

The negative integer frequencies are exactly

    (0,±1), (±1,±1), (0,±2).

There are eight real negative directions, counting sine/cosine for each ± pair. The constant phase is a gauge zero mode; there are no other zero integer modes. On the orthogonal complement of this gauge and these eight directions,

    D²J(y)[h,h]≥(4/5)||h||²_L2,
    D²J(y)[h,h]≥(4/25)||∇h||²_L2.                       (8)

Both constants are sharp at frequencies (±1,±2). To verify the exhaustive claim, the negativity threshold leaves only t≤5. Enumerating those finitely many integer pairs gives the list and constants. For all integer t≥6, `Λ≥4[t+min(0,2t−16)]`, which gives Λ≥8 and Λ/t≥4/3 for 6≤t≤8 and still stronger bounds above 8. Thus the finite enumeration controls every remaining frequency, not just a sampled box.

This refines the incoming local nonconvexity witness into a completely described unstable tangent space and a sharp positive-complement gap. It is compatible with the existing FS high-frequency/cutoff nonconvexity near zero phase: that is a different background, chart and derivative regime. It does not prove a global phase inequality, G quasiconvexity, or correctness of arbitrary alternating iterations. Historical priority and external review of this consequence remain UNKNOWN.

## 5. Exact surviving boundaries

Port response completion, finite-load prediction and harmonic support elimination share inverse-response algebra only after their distinct physical objects and legal probes are supplied. A nonreciprocal driven operator is not an equilibrium energy Hessian. Sensor calibration does not grant injection access. Transition-state response is not well response. A locally known derivative is not a globally qualified affine control law. A positive scalar eliminated block does not make the remaining phase block convex. These are explicit receiving-hypothesis tests, not failures of the source theorems themselves.
