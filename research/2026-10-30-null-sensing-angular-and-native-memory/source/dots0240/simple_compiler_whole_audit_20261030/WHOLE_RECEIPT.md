# Independent whole-theorem receipt: guarded Hamiltonian / onsite-reset simple compiler

2026-10-30. This is a scientific audit of the **actual composition**, not an inheritance of the component receipts. The original V1 and CSS clarification were read and preserved. Their exact copies are in `reviewed_sources/`; SHA-256 hashes of the reviewed inputs are in `SOURCE_SHA256.txt`.

## Verdict

**PASS, with the explicit scope and hypotheses below.** No remaining mathematical composition defect was found in `FULL_SIMPLE_COMPILER_MANUSCRIPT_V1.md` together with `FULL_SIMPLE_COMPILER_V1_CSS_CLARIFICATION.md`. The argument supplies the advertised full-Hilbert, finite-rate weighted barrier for the **specifically engineered bounded-body guarded Hamiltonian with onsite auxiliary resets**. Dirty and illegal controller sectors are genuinely included; they are not identified with ideal correction channels or discarded by a projection.

This acceptance is conditional on the expressly imported SSF/FGL small-reduced-error confinement and active-hub interface, the component-safe canonical local-edge theorem, and uniformly bounded support/incidence and dilation-stable noise norms. It covers a fixed initially logical-independent retained bath and the stated ideal frame-inverse/canonical-decoder output. It does **not** establish native two-site synthesis, the separate transactional scheduler, fixed-dimensional Euclidean hardware, arbitrary Stinespring completions, arbitrary logical-dependent initial baths, or noisy physical readout.

The useful clarifications are proof precision rather than new assumptions: (1) augmented containers contain exactly their component syndrome among occupied **syndrome** vertices, not among all occupied token/check vertices; (2) the no-jump lower comparison uses `[B_h,C'_j]=0`, not merely that B is auxiliary-only; (3) pushing a restricted inequality through T uses Schrödinger basin preservation, while commutation of F with the basin separately uses syndrome covariance and mask preservation; (4) read the dressing parameter as `tau`, distinct from elapsed physical time `T`. The finite-size initialization qualification can be closed by the explicit elementary extension in Section 8 below.

## 1. Exact model and theorem statement accepted

Work in each CSS sector with fixed minimum-Hamming-weight syndrome representatives. Every reduced error of size below ell has the stated confinement and actual active-hub mass. All declared DATA/read, correction, reset, gauge, noise and loss supports have fixed size and incidence; graph enlargements are made **before** selecting component/animal constants. The allowed local noise acts on a bounded physical patch and an arbitrary retained common bath, with a uniform cb or equivalent generator-form norm budget. Bath-only evolution is unrestricted subject to existence of the joint propagator.

There are fixed positive choices of kappa, nu=g/kappa, tau and eta_0, independent of N, and a positive full-space observable

    F = T(V_+),    F >= V_0,

such that on the raw component-safe low-V_0 basin,

    P (L* + N_T*) F P <= -lambda P T(W_+) P + b N P
                       <= -lambda P F P + b N P.

The gauge coordinates are those of the **explicit** guarded XOR/controlled-Pauli unitary in V1. Physical quantities are obtained by conjugating back. With encoded arbitrary logical/reference input, all auxiliaries ready, and one fixed bath state, the prescribed terminal frame inverse and ideal DATA decoder obey

    || Dec_frame E_T Enc - id_L ||_diamond
        <= min{2, C N^(3/2) T exp(-b_ell ell)}.

The constants can be extremely unfavorable. The theorem asserts existence of a positive threshold, not a practical parameter estimate.

## 2. Full-Hilbert gauge, raw resets, and flags

### 2.1 Idempotent channel

The complete local consulted syndrome includes every check changed by a permitted local correction. Choosing identity on every already minimal orbit element, including ties, is essential. The first channel application measures the local syndrome and produces a block-diagonal sum of local-minimum sectors; the second measures those same sectors and applies identity. Thus Phi_h^2=Phi_h on all operators, and

    d_h = V_+ - Phi_h*(V_+) >= 0,
    Phi_h*(d_h)=0.

An FGL improving candidate proves that the measured sector is not an orbit minimum, so the new rule retains every required active hub. Every nonidentity selected move decreases global syndrome count by at least one. Retuning beta and all animal constants is sufficient; no global minimization is performed.

### 2.2 Explicit unitary and Hamiltonian

On the excited label space, syndrome-controlled XOR followed by label-controlled Pauli is a unitary on the **whole** DATA/label Hilbert space, including impossible/unused labels (where the chosen F_s is identity). Its restriction to reference label zero is precisely the Stinespring isometry. Both factors normalize the global syndrome/label diagonal algebra. The guarded U_h commute: adjacent nontrivial sectors exclude one another, and nonadjacent DATA supports are disjoint. A coloring gives fixed depth.

Conjugation by U makes the guarded drive exactly DATA-independent, with ready/reference good-qubit X_h. The cancellation is an operator identity, not a restriction to valid histories. The conjugated resets remain bounded-support partial monomial operators on joint syndrome/label sectors. A partial monomial map is injective on its supported source sectors, so its adjoint maps diagonal observables to diagonal observables. This justifies the raw potential calculation without pinching or a classical-noise approximation.

### 2.3 Combined flags

K_s K_t^dagger=0 for s!=t makes E_h syndrome/label diagonal. The physical projector C_h=Q_h-G_hE_h simultaneously marks a dark excitation or any occupied box with an occupied neighbor. It commutes with the clean Hamiltonian and other C_j. A physical reset clears its own flag and cannot create a previously zero flag: any occupied neighbor that can be exposed as dark was already flagged by the illegal edge. This is a source-subspace statement for every individual reset, not an assertion about expectation values.

In the selected gauge,

    C'_h = Q_h-G_hR_h,

which is purely auxiliary. A good reset therefore has exactly the intended direct K_hs action. A bad reset need not: its actual changed syndrome and flag pattern are retained. R identical unary tokens per flag, with R>k_reset, ensure a bad reset has strictly positive removed-minus-added occupancy. Its own bundle is removed, no flag bundle is created, and the total changed set has bounded size.

The full-animal completion lemma applies to each actual deterministic raw sector move after its bounded changed set is made a clique. Therefore the raw drift is exactly of the required form

    L*V_+ <= -kappa sum_h (Q_h-C'_h)d_h
             -kappa sum_h D_h^bad,

with a uniform strict charge of D_h^bad to every animal containing h's full token bundle. The explicit charge and enlarged-geometry construction are proved in `coverage_review.md`, rather than inferred from earlier audit language.

## 3. Augmented coverage and sector addition

The graph construction can be ordered noncircularly: first fix bounded sets J_x including dummy/check/token/reset neighborhoods; then include DATA edges whenever J_x and J_y intersect, plus all declared support cliques; finally put those dummy edges, J_x spokes, and move cliques in the animal graph. Every degree and footprint remains bounded. A component container J(C) is connected, containers for distinct components are disjoint, and |J(C)|<=D0|C|. Its occupied syndrome vertices are exactly sigma(C); arbitrary occupied token vertices are permitted.

The accepted confinement theorem applies because every component is a reduced subset of a minimum representative and has size below ell. It is not an expansion theorem for token defects. The original active-hub assignment is still valid because the enlarged graph contains complete read footprints.

For each animal split occupied mass into syndrome and flag-token mass. Total-sparse animals have a summable O(N) weighted total. Flag-dense animals meet linearly many distinct occupied bundles and are charged by completing just one bundle at bounded multiplicity. The syndrome-dense remainder is charged by the original covered/poor-component argument, completing **one** poor component at a time. Its extra occupied tokens only improve the completion ratio. Entropy is paid before summing component charges, so neither an uncontrolled component count nor an extra |A| appears. This proves

    W_+ <= C_cov (sum_h d_h+sum_h D_h^bad) + C_vac N.

The detailed derivation, including an explicit uniform bad-charge coefficient, is in `coverage_review.md`.

For CSS, run this construction separately in each syndrome graph. The same physical flag has R combinatorial copies in each graph, not independent auxiliary registers. Every bad reset decreases each sector's augmented potential under the same physical rate. Opposite-sector intended corrections leave a sector's raw potential unchanged. The drift and coverage inequalities therefore add with common worst-case constants. No mixed X/Z container-disjointness is needed.

## 4. Geometric credit and clean-block service

### 4.1 Positivity and flag commutation

The only offdiagonal part of

    B_h=Q_h+2nu G_hY_h+nu^2 f0 r^(m_h)

connects ready and reference-good at h with every neighbor ready. Both endpoints have the same complete bad mask. Hence B_h and sqrt(B_h) commute with every C'_j. The available 2x2 determinant is nu^2(f0-4)+nu^4 f0^2>0; all blocked and dark sectors are diagonal and positive.

The explicit 2x2 square-root formula, together with the diagonal blocks, gives

    ||sqrt(B_h)-Q_h|| <= C nu.

This is stronger than generic square-root Holder continuity and has the power needed for the cross-mask estimate. The associated Z_h is unital Lindblad because sum_s K_hs^dagger B_h K_hs=B_h. It preserves all exact bad-mask blocks, and Z_h(V_+)=-B_h d_h.

### 4.2 Signed clean calculation

On a buffered all-good local block, actual resets agree with the legal hard-core direct K model; remote flags commute with every local operation and are spectators. The linked commutator is the actual four-term expression in V1. In particular the j=h terms use Delta_h d_h=-d_h and combine into (D_h B_h)d_h; there is no assumed commutation of B_h with n_h. Disjoint centers cancel because both the full DATA/read maps and their relevant clock factors commute.

I checked the signs against the exact clock identities: the exchange term in i[H0,Y_h] is negative; L_clock B_h has diagonal service 4G_h-8n_h plus positive m_h(f_(m_h-1)-f_mh), and the self-cancellation leaves the own-coherence term -nu Y_h. The bounded-patch inequalities on actual deterministic local moves are valid by completing each noncancelling animal to the paying move plus its fixed overlap patch. Inactive paying moves give zero, as required.

For neighboring j, sqrt(B_h)n_j sqrt(B_h)=nu^2 f(m_h)n_j. Thus the activated-neighbor contribution is paid **sectorwise** by choosing f_(m-1)-f_m>=2C f_m. The remaining reset term is bounded by a constant times n_jd_j and is paid by baseline occupation loss. The positive 8tau nu^2 n_h curvature is also baseline-paid.

Own-coherence Young bounds cost a reserved portion of n_hd_h plus O(tau^2 nu^2)d_h. Exchange bounds cost reserved n_hd_h plus O(tau^2 nu^4)n_jd_h; the latter is paid by the uniform service for the same h, not by falsely replacing d_h with d_j. The residual O(tau nu^3)d_h is smaller than the minimum geometric service once nu is sufficiently small. With nu chosen first and tau small afterward, the clean estimate is

    (L*+tau sum_h[L*,Z_h])V_+
       <= -(kappa/2)sum_h n_hd_h
           -c tau kappa nu^2 sum_h d_h.

## 5. The actual local surgery closes the dirty-sector composition

This is the key new bridge beyond the previously accepted clean-range/direct model.

Group first-order commutators by their **full buffered supports**, including every intermediate gauge, reset and credit support. Each support X has bounded size and incidence. Let P_X select all relevant flags zero and Q_X=I-P_X. The P_X diagonal block is exactly the clean calculation above. Negative occupation/service reservations can be grouped with their local terms; multiplying by buffered clean projectors is legitimate because all clean clock coefficients and the decrements preserve the masks. The missing service is localized to Q_Xd_h and is paid below.

For a local animal term meeting X and a nearby bad hub j, adjoin a fixed connected patch from the animal's meeting point to j's complete token bundle. The added size and preimage count are bounded. Strict raw bad-reset charge pays the completed animal. A given bad hub belongs to only boundedly many buffered X, hence

    sum_X sum_(A meeting X) Q_X f_A <= C sum_j D_j^bad.

There is no hidden |A| here. The same completion pays Q_Xd_h and hence missing clean service. The positive dirty diagonal part of the first-order correction costs O(tau kappa) times this charge and is absorbed into a fixed portion of raw -kappa D_bad.

For cross blocks, at nu=0 the physical Hamiltonian vanishes, B_h=Q_h, and both Z_h(0) and every gauged raw reset adjoint preserve the joint syndrome/label diagonal algebra. Therefore

    P_X [L*(0),Z_h(0)]V_+ Q_X = 0

**exactly**. The explicit square-root estimate and local generator bounds make the cross coefficient O(kappa nu), not O(kappa). For each f_A, local orbit ratios provide a uniform relative form bound even if A is large. Since f_A commutes P_X and Q_X, block Young gives

    +/- tau cross_X(f_A)
       <= delta kappa Q_Xf_A
          +C_delta kappa tau^2 nu^2 P_Xf_A.

Choose delta small enough for the summed bad-side completion constant. The first term is raw-bad-loss-paid. The clean-side term sums over the O(|A|) supports meeting A, giving only C kappa tau^2 nu^2 W_+. No extensive pair sum and no second animal-size factor occur.

Consequently, after reserving baseline and bad losses, coverage yields

    (L*+tau sum_h[L*,Z_h])V_+
        <= -c_1 tau kappa nu^2 W_+ + b_1 N.

This verifies the actual dirty-reset/good-dirty-coherence interface. It does not import the full-tensor fresh-K generator as if it were the same physical process.

## 6. Exact similarity, generic noise, and the raw basin

A fixed-depth ordered circuit of exp(tau Z_h) has a local linear inverse circuit. Conjugating each local generator through it meets only a bounded causal cone; disjoint gates cancel algebraically. Taylor expansion in tau therefore yields bounded-incidence local HP identity-annihilating remainders of cb norm O(kappa tau^2), without a global inverse norm. The augmented local-orbit estimate bounds their sum on V_+ by C kappa tau^2 W_+. Choosing tau sufficiently small relative to nu^2 absorbs this exact remainder. This is a pointwise exact similarity estimate, not a long-time approximation.

The similarity inverse is used only for that exact identity. It is not treated as positive. To push a basin-restricted inequality through the positive T, one separately proves that T_* preserves the raw basin: every K_hs branch leaves flags fixed and decreases V_0; the component-edge theorem prevents a component-unsafe target below M_edge; every sqrt(B_h) and no-jump factor preserves syndrome and mask. Thus all gate Kraus histories preserve P, and P A P<=0 implies P T(A)P<=0 by testing against P-supported positive states.

The independent `basin_review.md` proves the remaining details explicitly:

- A selected no-jump factor is exp(-tau B_h/2). Because B_h commutes **both syndrome and every flag**, it commutes every raw f_A. Selecting all no-jump branches in the structural O(|A|) cone yields T(f_A)>=exp(-C_T tau|A|)f_A. Two nearby tuned exponents give F=T(V_+)>=V_0. Conversely T(V_+)<=V_+.
- Mere P-preservation would not imply [P,F]=0. Here each K_s has fixed stabilizer character, giving syndrome covariance, and every credit jump preserves masks. Therefore F is syndrome-block-diagonal and mask-block-diagonal. The basin projector is a function of those labels, so [P,F]=0 exactly.
- A local unitary Stinespring dilation of T uses fresh proof environments, not the retained bath. Conjugating a physical local HP identity-annihilating perturbation by that unitary preserves its cb norm and enlarges only its bounded physical support. The orbit bound then gives N_T*F<=eta C_noise T(W_+). Shared bath correlations are retained; no reduced-DATA noise approximation is used.

These properties remove the generic CP-dressing pitfalls identified in the earlier direct-model review.

## 7. Killed process and logical gauge

With [P,F]=0, complete-loss compression has adjoint drift

    (L^P)*(PFP)=P L*(F)P
                -sum_K P K^dagger (I-P)F(I-P) K P.

The removed term is positive. The dressed drift therefore gives an O(N) killed F-moment, and F>=V_0 bounds the raw moment. The augmented edge argument applies to the same enlarged DATA geometry: occupied tokens only improve its source-weight lower bound. Thus exits must cross the raw potential cutoff and all source blocks for QHP, QKP and QK^dagger KP lie in V_0>=cM. Their **union**, not a sum carrying an extra N, has mass O(N/M).

Every gauged local Hamiltonian/reset/noise/loss operator has a finite local DATA Pauli expansion with arbitrary controller/bath coefficients. The canonical local-edge theorem gives identity logical action for every retained edge, including complete losses and Hamiltonian terms. The compressed generator consequently acts as I_L tensor an ancillary generator. Fixed logical-independent initialization makes the killed decoded map exactly a_T id_L, with a_T independent of the logical/reference input.

Variation of constants and boundary cross-block Cauchy–Schwarz cost the O(N) total non-bath local norm budget times sqrt(N/M), producing O(N^(3/2)T/sqrt(M)). Trace preservation controls 1-a_T by the same comparison. Terminal U^dagger is necessary: the theorem is about framed DATA, not pending bare DATA. Bath-only evolution contributes no boundary or logical term.

## 8. Compatible parameters and explicit finite-size qualification

Choose the enlarged graph/token multiplicity first; then choose two exponents c_0<c_+<1 inside all strict move/completion/edge margins, and theta sufficiently small for both. Next compute bounded-patch constants, choose f0>4 and r<1/(2C+1), then nu>0 small compared with the positive geometric-service minimum. Finally choose tau>0 satisfying all occupation/dirty/cross/remainder bounds and C_T tau<=a_+-a_0, and eta below the resulting positive service margin. These are finitely many compatible upper bounds on fixed positive parameters, independent of N.

The killed proof is directly initialized when V_0(vacuum)<M and ell>=8s, with ell below the code distance and confinement cutoff. For ell proportional to sqrt(N), these hold for sufficiently large N.

A uniform small-size/low-barrier extension needs no new controller theorem. Let M_edge=exp(alpha ell), M=M_edge/2, V_0(vacuum)<=C_vac N, and let the total non-bath generator norm budget be <=C_gen N. In the bath-only interaction picture, the decoded channel has the elementary bound

    ||Dec_frame E_T Enc-id||_diamond <= min(2,C_gen N T).

If exp(alpha ell)<=2C_vac N, then

    N^(3/2)exp(-alpha ell/2) >= N/sqrt(2C_vac),

so enlarging the prefactor proves the claimed form directly. If ell<8s, exp(alpha ell/2) is itself bounded by a fixed constant and the same argument applies. Otherwise the initialized killed argument applies. Thus the usual large-N qualification can be made explicit or absorbed into a larger constant without pretending the vacuum was inside a nonexistent basin. The distance/confinement and well-posed-joint-dynamics assumptions remain necessary.

## 9. Independent regression and limits of numerical evidence

`check_full_compiler.py` independently constructs the actual two-hub, one-DATA-qubit onsite-reset model on all 18 dimensions. It uses the explicit XOR/controlled-X completion, not the earlier hand-selected swap completion; both bad/dark and adjacent-occupied sectors are present. A complete five-vertex animal graph contains one syndrome vertex and two repeated tokens per flag.

The recorded fixture verifies exact unitarity, all flag-credit commutators, and exact raw drift decomposition; zero-drive clean/dirty commutators vanish exactly. The tested full-Hilbert first-order residual has maximum eigenvalue relative to ||V|| of 5.99e-18. Exact finite-dimensional CP exponentials preserve masks, lower V, and obey the selected no-jump lower bound on every nonempty animal. See `check_full_compiler.json` for parameters/results.

These are independent finite regression checks, not a proof of general coverage, parameter scaling, or a hardware threshold. The whole acceptance rests on the structural proofs above and the stated imported code/edge interface.

## Actions and final scope

No frozen source was edited. No external write, publication, native-hardware claim, or novelty claim was made. The final theorem scope is the full physical Hilbert space of the engineered **bounded-body guarded-H / onsite-reset simple compiler**, with sustained bounded-incidence local quantum/common-bath noise and ideal framed mathematical readout. The native two-site and transactional problems remain separate open tasks.
