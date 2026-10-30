# A finite-rate guarded SSF controller with a full-Hilbert weighted barrier
## Stable composition manuscript V1 — 2026-10-30

**Scope.** This manuscript concerns a specifically engineered SIMPLE guarded Stinespring controller: bounded-support, generally many-body Hamiltonians and on-site auxiliary reset jumps. All coupling rates, footprint sizes, local Hilbert dimensions and overlap degrees are fixed independently of code size. It does NOT prove native two-site synthesis, does NOT cover the separate transactional acquisition/lock/forest scheduler, and does NOT replace quantum clocks by Poisson attempts. The full-Hilbert controller/noise bridge below is composed from locally audited ingredients; an independent whole-composition review is requested.

## 1. Theorem interface and initialization

Assume the previously verified SSF/FGL interface on a bounded-degree CSS code family: every stabilizer-reduced DATA error component of size below ell has syndrome size at least h times its size and at least kappa_A times its syndrome size distinct active hubs. Full read footprints, possible correction footprints and declared primitive/noise supports have bounded size and incidence. Minimum-weight representatives and the component-safe local-edge lemma are those in FULL_ANIMAL_KILLED_BASIN_CANDIDATE.md; after every fixed geometry enlargement below, recompute their constants and use the corresponding component graph/cutoff. Do not impose FGL confinement on auxiliary defects.

Under these assumptions the construction below gives positive constants g,kappa,eta_0,lambda,b,C,boundary_exponent independent of N, and a positive observable F on the ENTIRE physical DATA/controller Hilbert space (expressed in a bounded-depth frame), such that on the stated component-safe low-potential basin,

    (L_phys^*+N_t^*)F <= -lambda T(W_+) + b N I
                         <= -lambda F + b N I

for every sustained bounded-incidence local Hamiltonian/Lindblad perturbation of strength at most eta_0, including operators coupled to a retained common bath. All local norm conditions are completely bounded or equivalent dilation-stable bounded-generator conditions. A bath-only Hamiltonian is unrestricted and commutes with the barrier. No shared-bath erasure, Pauli-noise reduction or added data depolarization is used.

Initialize Enc(rho_LR) tensor |all auxiliaries ready><ready| tensor sigma_B, with one FIXED bath state sigma_B independent of the arbitrary logical/reference input. At readout apply the finite-depth frame inverse and then the fixed ideal mathematical DATA decoder; discard controller and bath. The existing killed-basin local-edge proof then gives

    ||Dec_frame E_t Enc - id_L||_diamond
      <= min{2, C N^(3/2) t exp(-b_ell ell)}.

This is a decoded-channel statement with the stated fixed bath initialization and ideal output convention. It is not a claim that noisy physical extraction has been constructed. For ell proportional to sqrt(N), the bound has an exponential-in-sqrt(N) time scale. The constants may be extremely poor.

## 2. Idempotent local SSF maps

At hub h, measure the complete fixed consulted syndrome s. Enumerate the finite affine orbit obtained by all subsets of its generator support. If s already minimizes local syndrome Hamming weight, apply identity, including ties. Otherwise apply a fixed Pauli F_s taking s to one chosen minimum. This uses a fixed finite truth table, not a global optimization oracle.

Write K_hs=F_s Pi_s and Phi_h(rho)=sum_s K_hs rho K_hs^dagger. Every output is block diagonal in locally minimal syndrome sectors, so the second application measures deterministically and applies identity:

    Phi_h^2=Phi_h

as a full CPTP map. Every nontrivial move lowers global syndrome count by at least one; if k_data bounds its changed-check size, beta_data=1/k_data suffices. Every hub admitting an FGL candidate remains active, so the candidate-mass lower bound still supplies the required active-hub density. Rechoose all animal constants for this possibly smaller beta.

## 3. Actual physical controller and explicit full-Hilbert frame

Give h one ready level and an excited m-bit label register (dimension 2^m), with reference excited label 0. Here m is the fixed number of consulted syndrome bits. Let P_h be ready, Q_h=I-P_h, and G_h=product_{j~h}P_j, where the overlap graph includes every full DATA/read overlap. Define

    V_h=sum_s K_hs tensor |excited s><ready|,
    H=g sum_h G_h(V_h+V_h^dagger),
    L_hs=sqrt(kappa) I_DATA tensor |ready><excited s|.

The reset jumps are on-site auxiliary operations. H is bounded-support but generally high-body. No fast-reset limit is taken; later g/kappa is a small fixed positive number.

On the ENTIRE excited DATA/label space use the explicit unitary

    U_exc,h=(sum_s F_s tensor |s><s|)
             (sum_s Pi_s tensor X_label^s).

Define F_s=I on unused labels. The second factor coherently XORs the measured syndrome into the label; both factors are unitary. On reference label0 their product is the required Stinespring isometry. Extend as identity on ready and guard by neighboring auxiliaries ready. These guarded U_h commute: adjacent nontrivial sectors are mutually excluded; nonadjacent DATA supports are disjoint. Their product U has a bounded-depth local implementation by coloring.

In the frame U^dagger the Hamiltonian is EXACTLY

    H_g=g sum_h G_h X_h^good,

where X_h^good couples ready to the fixed good excited reference, and acts trivially on DATA. This identity holds on the full Hilbert space, not only legal clocks. Each gauged reset is U^dagger L_hs U and remains a bounded-support instantaneous DATA/controller instrument. Only in a good source sector does it implement Phi_h.

The explicit U normalizes the joint global syndrome/auxiliary-label diagonal algebra: it is a syndrome-controlled label permutation followed by controlled Paulis. Thus every gauged reset is partial monomial on joint sectors, up to degeneracy-space unitaries. Its adjoint preserves that diagonal algebra exactly, including dirty sectors.

## 4. Commuting combined bad flags and raw token descent

In physical coordinates let E_h=V_hV_h^dagger and

    C_h=Q_h-G_h E_h.

Since K_hs K_ht^dagger=0 for s!=t, E_h=sum_s F_s Pi_s F_s^dagger tensor |s><s| is syndrome/label diagonal. C_h flags a dark excitation OR an occupied box with an occupied neighbor. The C_h are commuting projectors and commute with the clean Hamiltonian. On illegal occupancy sectors they are identity on the occupied local box; on isolated occupied boxes their DATA supports are disjoint. In the gauge,

    C_h'=Q_h-G_h R_h,   R_h=|good reference><good reference|,

so the flags are purely auxiliary.

Every physical reset clears its own flag and creates no previously zero flag. A neighbor exposed as dark after clearing an illegal edge was already flagged before that reset. Ready neighbors stay ready; nonneighbors are unaffected. These are exact source-subspace inclusions C_j L_hs(I-C_j)=0, preserved by gauge conjugation, not a stochastic bookkeeping assumption.

Let k_reset bound DATA syndrome bits changed by any gauged reset, including neighboring frame changes, and let D_flag bound the number of flag bundles it can clear. Add R identical unary token vertices per flag, with R>k_reset. All copies are occupied iff C_h'=1; independence is neither required nor assumed. A bad-source reset removes its R own tokens, creates none, and changes at most k_reset DATA syndrome bits. Its occupied-vertex flip D therefore obeys

    removed-minus-added >=R-k_reset,
    |D|<=R D_flag+k_reset,
    beta_bad=(R-k_reset)/(R D_flag+k_reset)>0.

Make each possible bounded reset footprint a clique of the augmented animal graph. In a fixed joint sector the reset has a deterministic target sector, because the chosen gauge is monomial. Thus the original full-animal per-move charging applies exactly, not after a classical approximation or pinching.

## 5. Full augmented animals and actual weighted coverage

The augmented bounded-degree graph contains DATA dummy vertices (always empty), syndrome checks, and the unary flag tokens. Enlarge the original single-site footprints/containers to include all token/reset supports; define DATA error components through intersections of these enlarged footprints. Distinct component containers remain disjoint, and their sizes are bounded by a fixed multiple of syndrome size through the original FGL confinement hypothesis.

For every nonempty connected animal A, with NO size truncation, put

    f_A^a=exp(a|A|) theta^{|A|-occupied(A)},
    V_a=sum_A f_A^a,   W_a=sum_A |A| f_A^a,
    a=c log(1/theta), 0<c<1.

Choose beta=min(beta_data,beta_bad). The original completion A -> A union D proves, for every accepted DATA move and every actual bad reset,

    decrement V_a >= (1-theta)/2 sum_{B containing D} f_B^a

when c>(1-beta)/(1+beta) and theta is sufficiently small. Every nontrivial clean physical reset is therefore V_a-nonincreasing on the full joint diagonal algebra.

Let d_h=(I-Phi_h^*)V_a>=0 be the hypothetical DATA-only decrement, leaving flags fixed; idempotence gives Phi_h^*d_h=0. Let D_h^bad be the actual raw bad-source reset decrement, including its source flag. Completing any animal containing the entire h-token bundle by the actual changed set D gives

    D_h^bad >= c_bad C_h' sum_{A containing all h-tokens} f_A^a.

The completion adds boundedly many vertices and has bounded preimage multiplicity, uniformly over local source patterns. Consequently the actual raw drift satisfies

    L_phys^* V_a <= -kappa sum_h Q_h(1-C_h')d_h
                    -kappa sum_h D_h^bad.

Coverage does not assume expansion for flags. Split animals into total-sparse, flag-dense, and syndrome-dense remainder. Total-sparse animals contribute O(N). Flag-dense animals meet Omega(|A|/R) occupied token bundles; completing one bundle and charging D_bad yields their weighted bound. Syndrome-dense animals use the original rich/poor, ONE-component completion proof with enlarged containers. Added occupied tokens only improve its weight ratio. Thus on the DATA component-safe basin,

    W_a <= C_cov(sum_h d_h+sum_h D_h^bad)+C_vac N.       (5.1)

All constants and cutoff geometry are recomputed after R and the augmented graph are fixed.

## 6. Positive geometric blocker credit

Write nu=g/kappa. For the clean good ready/excited qubit let Y_h=i(a_h-a_h^dagger), with guards included as needed. On the full auxiliary space put

    m_h=sum_{j~h}Q_j,
    B_h=Q_h+2nu G_h Y_h^good+nu^2 f(m_h),
    f_m=f0 r^m,   f0>4, 0<r<1.

In an available ready/good block, B_h has diagonal nu^2f0 and 1+nu^2f0, off-diagonal magnitude2nu, and determinant nu^2(f0-4)+nu^4f0^2>0. Blocked and dark sectors are diagonal. Therefore B_h>=0 with bounded norm. It commutes with EVERY combined flag C_j'. Its square root obeys the explicit uniform estimate

    ||sqrt(B_h(nu))-Q_h||<=C nu.

This follows from the 2x2 square-root formula and the diagonal blocked/dark blocks; generic Holder continuity would be insufficient.

Define a local unital Lindblad superoperator with jumps sqrt(B_h)K_hs:

    Z_h(O)=sum_s K_hs^dagger sqrt(B_h) O sqrt(B_h)K_hs
             -{B_h,O}/2.

It preserves every bad-mask block, and Z_h(V_a)=-B_h d_h. Color its fixed enlarged supports and set T to the ordered finite-depth circuit of exp(t Z_h). T is unital CP; its inverse exists as a local LINEAR circuit, not necessarily CP.

## 7. Clean-block signed service estimate

On a buffered all-good region, exact hard-core clock algebra gives
D n_h=-n_h, D Y_h=-Y_h/2,
i[sum X,Y_h]=2G_h-4n_h-sum_{j~h}(a_j^dagger a_h+a_h^dagger a_j),
Df(m)=m[f(m-1)-f(m)].
The exact linked commutator on a DATA-only decrement is

[L,Z_h]V=-(L_clock B_h)d_h
 -kappa sum_j(a_j^dagger B_h a_j)Delta_j d_h
 +kappa sum_j sqrt(B_h)n_j sqrt(B_h)Delta_h d_j
 +kappa sum_j D_sqrt(B_h)^*(n_j)d_j.

Disjoint terms cancel, not merely become small. The self terms use Delta_h d_h=-d_h and combine to (D_hB_h)d_h. For neighbors, B_h commutes with n_j, D_sqrt(B_h)(n_j)=0, and sqrt(B_h)n_j sqrt(B_h)=nu^2 f(m_h)n_j on legal clocks.

Bounded-patch animal completion gives |Delta_j d_h|<=C d_j and Delta_h d_j<=C d_h for overlapping hubs. Therefore the activated-neighbor term is paid by geometric blocker service if f_{m-1}-f_m>=2C f_m. The remaining neighboring reset term is paid by occupation drift. The own ready/excited coherence of size tnu and exchange terms of size tnu^2 are absorbed by block Young inequalities against the residual negative occupation drift, costing respectively O(t^2nu^2) and O(t^2nu^4). The bounded O(tnu^3) term is absorbed by choosing nu small compared with the minimum positive blocker service.

Thus, on clean buffered blocks, for sufficiently small fixed nu,t,

    (L+t sum_h[L,Z_h])V_a
      <=-(kappa/2)sum_h n_h d_h-c t kappa nu^2 sum_h d_h.

This estimate uses the actual selected idempotent corrections and actual weighted decrements; no clock stationarity or effective rate assumption enters it.

## 8. Full-Hilbert local surgery

The preceding DATA decrement depends on flags; do NOT pretend it is globally clock-independent. For each exact linked local term use a fixed buffer X containing every intermediate gauge/reset/credit support. Split P_X=all flags in X zero and Q_X=I-P_X.

On P_X the actual generator agrees with the legal direct model, local raw resets cannot create flags, and Z preserves masks. Thus the clean-block calculation applies, with remote flags as commuting spectators. Extra reset action on the flags is supported on dirty blocks and is retained below.

**Bad-support completion.** If an animal meets X and C_j'=1 for a nearby j, complete it by a fixed connected patch to the entire j-token bundle. Added size and preimage multiplicity are bounded. The strict raw charge in section 5 pays the result. Summing over the bounded-incidence family X gives

    sum_X sum_{A meeting X} Q_X f_A <= C sum_j D_j^bad.

There is NO additional |A| factor here: a fixed bad hub belongs to boundedly many X. The same bound pays nearby hypothetical d_h Q_X and hence missing clean service.

**Bad diagonal blocks.** Their relative local size in the t-commutator correction is O(tkappa). The displayed completion bound absorbs them into a small part of the instantaneous -kappa D_bad drift for t sufficiently small.

**Clean/dirty cross blocks.** At nu=0, B_h=Q_h, Z_h has jumps Q_hK_hs, and both Z_h and gauged raw resets preserve the joint diagonal algebra. Raw V_a and [L(0),Z_h(0)]V_a are diagonal. Hence the cross P_X/Q_X block vanishes EXACTLY at nu=0. The explicit square-root bound and bounded local generators make its relative size O(kappa nu), not O(kappa). After multiplication by t, the weighted block Young inequality gives

    +/- t(cross block on f_A)
       <=delta kappa Q_X f_A+C_delta kappa t^2nu^2 P_X f_A.

The first term is paid by bad-reset completion. Summing the second over supports meeting A costs exactly one |A| factor, hence O(kappa t^2nu^2)W_a. Local orbit ratios are finite because only boundedly many syndrome/token factors are affected. There is no extensive pair sum.

Combining these estimates, retaining a fixed part of raw bad loss, and using (5.1), yields a full physical first-order bound

    (L_phys+t sum_h[L_phys,Z_h])V_a
       <=-c_1 t kappa nu^2 W_a+b_1 N I,

for arbitrary physical controller states on the DATA component-safe basin. This is where dirty resets are paid as actual faults; they are never identified with Phi_h.

## 9. Exact CP dressing, perturbations, and barrier comparison

For the finite-depth circuit T,

    L_eff=T^{-1}L_phys T
          =L_phys+t sum_h[L_phys,Z_h]+R_t.

Conjugating each local generator through a fixed number of disjoint layers produces a bounded-support local HP identity-annihilating map. Its Taylor remainder has local cb norm at most C kappa t^2, uniformly in N. The augmented local-orbit estimate gives R_t V_a<=C' kappa t^2 W_a. Choose t smaller than a constant times nu^2 c_1; then

    L_eff V_a<=-c_2 t kappa nu^2 W_a+bN,
    L_phys T(V_a)<=-c_2 t kappa nu^2 T(W_a)+bN.       (9.1)

This is an EXACT generator similarity identity and an exact remainder bound. It is not a finite-time simulation estimate and has no exp(time) error.

For any bounded-depth local unital CP circuit T, choose local unitary Stinespring dilation U_T with fresh product environments. If N_Z^* is a local HP identity-annihilating map, define M_Z=Ad_U_T (N_Z^* tensor id) Ad_U_T^dagger. Then exactly

    N_Z^* T(O)=E[U_T^dagger M_Z(O tensor I)U_T].

M_Z has unchanged cb norm and a bounded causal support enlargement. The original joint syndrome/token orbit inequality, followed by positive compression, gives

    N_t^* T(V_a)<=eta C_noise T(W_a).

This includes arbitrary local controller errors and a retained shared bath. Choose eta<c_2 t kappa nu^2/(2C_noise).

For barrier comparison, retain only the clock-only no-jump branch of every credit semigroup in the finite causal cone of A. There are O(|A|) such bounded-norm gates, so

    T(f_A^a)>=exp(-C_T t|A|) f_A^a.

Equivalently one may integrate the local Stinespring relative-generator bound layer by layer. No claim T>=c Id in CP order is made. Reserve exponents a_+>a_0 and require C_Tt<=a_+-a_0. Then

    F=T(V_{a_+})>=V_{a_0}.

Also T(V_{a_+})<=V_{a_+}, since every hypothetical Phi_h is monotone and Z_h(V)=-B_hd_h<=0. The initial encoded/all-ready expectation is therefore O(N).

## 10. Compatible parameter order and killed basin

1. Fix local idempotent truth tables, explicit label registers/gauge, reset footprints k_reset,D_flag, and R>k_reset.
2. Fix the augmented graph and recompute DATA component/container/edge-barrier constants. Set beta=min(beta_data,beta_bad).
3. Choose 0<c_0<c_+<1 sufficiently near1 that both satisfy per-move charging, augmented poor-component completion and the component-edge density margin. Set a_i=c_i log(1/theta); choose theta small for all move, preimage and vacuum-summability inequalities.
4. Obtain the bounded-patch decrement constant C. Choose f0>4 and r<1/(2C+1); the minimum geometric blocker service is a positive fixed constant.
5. Fix kappa>0 and sufficiently small nu>0, then g=kappa nu. Choose t>0 small enough for occupation/dirty-loss absorption, local remainder absorption, and C_Tt<=a_+-a_0.
6. Choose perturbation strength eta below the positive service margin in (9.1). All quantities are fixed independently of N.

Define the analytical killed basin using DATA component safety and the RAW joint diagonal V_{a_0}<M, not a spectral cutoff of F. Choose M a fixed fraction of the enlarged-geometry DATA local-edge barrier exp(b ell). Raw clean good and bad resets are V_{a_0}-nonincreasing; H preserves syndrome and flags. The hypothetical credit channels also preserve this basin. Moreover F remains DATA-syndrome-diagonal and bad-mask-block-diagonal, so its basin projector commutes with F.

Deleting outgoing killed jump gains subtracts positive F contributions. Thus (9.1) and the noise margin give Tr(F rho_killed(t))<=CN. A bounded local operator changes only a fixed number of syndrome/token vertices; a source of a basin exit has V_{a_0}>=cM and hence F>=cM. Boundary mass is O(N/M). The existing component-safe local-edge argument gives identity canonical logical action for every compressed local DATA Pauli edge, including Hamiltonian and loss terms, with arbitrary controller/bath factors. The killed decoded map is therefore a_t id_L for the stated fixed initialization.

The physical generator has O(N) bounded local terms and a fixed Kraus count per hub. Variation of constants plus cross-block Cauchy-Schwarz yields O(Nt sqrt(N/M)) full-vs-killed diamond error, giving the theorem bound in section1. The frame inverse is bounded-depth/local; output uses dressed DATA, not a claim that pending bare physical DATA equal completed logical output.

## 11. Audit status and architecture boundary

Signed geometric service, exact finite-depth remainder, full-tensor DIRECT fresh-K extension, and local-noise transfer were independently audited. COMPILER_LOCAL_SURGERY_INDEPENDENT_AUDIT.md additionally checks the full simple-compiler surgery and explicit monomial/raw-token addendum; no dirty-sector algebra gap was identified. Exact finite fixtures verify the key full-Hilbert flag/frame identities and the direct-clock signed inequality. These tests support, but do not replace, the proofs.

The present composition still depends explicitly on the original SSF/FGL component and killed-basin interfaces. It is a bounded-body guarded-H/on-site-reset theorem candidate for independent whole-composition review. It is NOT a theorem for an arbitrary Stinespring completion, an arbitrary transactional clock graph, a native two-site apparatus, or a fault-tolerant physical readout circuit.
