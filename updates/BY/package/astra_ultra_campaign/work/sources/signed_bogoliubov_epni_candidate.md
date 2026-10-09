# A signed KMS-interpolation route to the amplifier entropy photon-number inequality

**Research status (9 October 2026): Unreviewed candidate derivation. NOT a certified theorem, an accepted proof, or a 10/10 discovery.** This document identifies and proves the central new *signed-weight transfer* and gives a proposed variational proof of the amplifier EPnI, with the remaining audit obligations identified. Nothing here has been submitted, merged or published.

## Source revisions and provenance

- OpenAI Math: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Source: `preprints/The-entropy-photon-number-inequality-September-24-2026/build/sections/{02-interpolation,03-minimization,04-metric,05-stationarity}.tex`. The four-weight interpolation theorem and the passive beam-splitter variational proof are the **source results**, not new results of this note. The corresponding proof-bearing Lean module is `lean/OAI/InformationTheory/PhotonNumber/Inequality.lean`; the interpolation Lean module is `lean/OAI/InformationTheory/PhotonNumber/Interpolation.lean` (no `sorry` in these two inspected modules). The comparator challenge statement `lean/ComparatorChallenges/EntropyPhotonNumber.lean` contains a deliberate `sorry` placeholder and is **not** the proof module.
- Astra: `031ce532f7f6d1c070387f6213a00204893be79d`; navigation started with `00_START_HERE.txt`. Cards N363–N368, N371–N373 and the corresponding proof-source archive distinguish internally sourced broadcasting/KMS statements from externally unreviewed claims. None of the Astra claims is assumed in the derivation below.
- Historical antecedent: De Palma, Mari and Giovannetti, *A generalization of the Entropy Power Inequality to Bosonic Quantum Systems* (2014), specifically their amplifier EPnI conjecture, Eq. (32). Existing one-mode fixed-thermal-input amplifier optimizers are not a solution of the two-arbitrary-input problem.

Throughout, `g(t)=(t+1) log(t+1)-t log t`, `h(t)=g'(t)=log((t+1)/t)` for positive `t`, and `N(ρ)=g^{-1}(S(ρ)/n)` for an `n`-mode density operator.

## 1. Proposed historical target

For **all** finite `n>=1`, **all** finite-energy `n`-mode input states `ρ_A, ρ_B`, independent *across* the two input groups, and each gain `G>1`, let `γ` be the retained output from the two-mode squeezing transformation in each mode

`c_j = sqrt(G) a_j + sqrt(G-1) b_j†`.

The proposed claim is

`N(γ) >= G N(ρ_A) + (G-1)(N(ρ_B)+1)`.  (AEPnI)

Equivalently, at fixed input entropies `S(ρ_A)=n g(a)`, `S(ρ_B)=n g(b)`, the output entropy should obey `S(γ)>=n g(Ga+(G-1)(b+1))`. Product thermal inputs attain the right side. Internal entanglement across the `n` modes of either input is allowed; arbitrary shared quantum references are **not** included.

A more general *proposed* signed-port theorem replaces the single annihilation and single creation ports with independent port groups:

`c_j=Σ_{s∈P} sqrt(λ_s) a_{s,j}+Σ_{s∈M}sqrt(λ_s) a_{s,j}†`,

where all `λ_s>0` and `Σ_{P}λ_s-Σ_Mλ_s=1`. The conjectured lower bound is `N(γ)>=Σ_P λ_s N(ρ_s)+Σ_M λ_s(N(ρ_s)+1)`. The proof pattern below uses only finiteness of the number of input groups. The two-input amplifier suffices to resolve the historically named problem and is the main focus.

## 2. The exact signed thermal balance (proved algebraically)

For the two-input amplifier and positive reference means `r_A,r_B`, define

`r_* = G r_A+(G-1)(r_B+1)`.

Then the two identities needed for the interpolation step are

`r_* = G r_A+(G-1)(r_B+1)`,

`r_*+1=G(r_A+1)+(G-1)r_B`.

The first identity is the thermal output occupation, the second is equivalent to the canonical commutation relation `G-(G-1)=1`. Importantly, it is **false** that `G(r_A+1)+(G-1)(r_B+1)=r_*+1`. The second input must have its absorption/emission roles exchanged.

To obtain strict scalar slack and a faithful thermal reference, add a small downstream passive mixing port `D`, with transmission `1-u` from the squeezed output and transmission `u` from an independent thermal state `τ_{r_D}`. Put

`λ_A=(1-u)G`, `λ_B=(1-u)(G-1)`, `λ_D=u`,

`r_0=λ_A r_A+λ_B(r_B+1)+λ_D r_D`.

We can choose `r_D=r_*` so that `r_0=r_*` at every fixed `u`. The companion relation is

`r_0+1=λ_A(r_A+1)+λ_B r_B+λ_D(r_D+1)`.

Consequently, with `u>0`, both scalar inequalities below hold for some `ε>0`:

`(1+ε)[λ_A r_A+λ_B(r_B+1)]<=r_0`,

`(1+ε)[λ_A(r_A+1)+λ_B r_B]<=r_0+1`.

The exact slacks at `ε=0` are `u r_D` and `u(r_D+1)` respectively. This is the first essential change from passive mixing; simply copying the passive `r_s` coefficients would be invalid.

## 3. A signed interpolation lemma (complete reduction to the verified source lemma)

For a faithful reference state `ρ_s=diag(p_l)` and `h_s=h(r_s)`, the BKM observable inner product is weighted by `h_s ℓ(p_l,p_r)`, where `ℓ(a,b)=(a-b)/(log a-log b)`. Let `v_s(l,r)=log(p_l/p_r)/h_s`, and write

`f(x)=x/sinh(x)`, `b_s(v)=v coth(h_s v/2)/2` (continuous at zero),

`R_{s,±}(v)=b_s(v)±v/2`.

Let `s=0` denote the output, `s=A` the annihilation input, and `s=B` the creation input. Assume linear centered slice maps `L_A,L_B` obey the two arithmetic-form comparisons

`Σ_i w_i ||L_i Z||^2_{R_{i,±}} <= ||Z||^2_{R_{0,±}}`,

and the two **signed** constant-weight BKM comparisons

`w_A r_A ||L_A Z||_A² + w_B (r_B+1) ||L_B Z||_B² <=r_0 ||Z||_0²`,

`w_A (r_A+1)||L_A Z||_A² + w_B r_B ||L_B Z||_B² <=(r_0+1)||Z||_0²`.

Define the ordinary thermal metric for the output and annihilation input by

`F_s^↓(v)=(1/h_s) f(h_s v/2)f(-h_s/2)/f(h_s(v-1)/2)`;

and the **reversed** metric for the creation input by

`F_B^↑(v)=(1/h_B) f(h_B v/2)f(+h_B/2)/f(h_B(v+1)/2)=F_B^↓(-v)`.

**Signed interpolation lemma.** The four comparisons above imply

`w_A ||L_A Z||²_{F_A^↓}+w_B||L_B Z||²_{F_B^↑}<=||Z||²_{F_0^↓}`.

**Proof.** Apply OpenAI Math's four-weight interpolation theorem with parameters `m_s=1/h_s`, `x_s=h_s v_s/2`, and `y_0=y_A=-h_s/2`, but `y_B=+h_B/2`. The four generated weights are exactly `R_+`, `R_-`, and the **two different signed constant families** above, because `(1/h)f(h/2)e^{+h/2}=r+1` and `(1/h)f(h/2)e^{-h/2}=r`. The theorem returns the claimed `f(x)f(y)/f(x+y)` weights. Each `F_s` is positive and bounded above/below by positive constants depending only on `r_s`: `F_B^↑(v)=F_B^↓(-v)` and the source gives the bounds for `F^↓`. No transposition channel or quantum-reference interface has been introduced. QED.

The proof depends on the **full analytic four-weight interpolation theorem** in source Section 02, not just its headline. The theorem is separately present in the inspected Lean module `OAI/InformationTheory/PhotonNumber/Interpolation.lean`. The signed application is a new deduction, not a theorem in the original paper.

## 4. Reversed defect identity (proved on the common bounded-observable domain)

For each input mode let `d=a-μ`, where `μ=Trρ a`. Define the normal thermal defect

`q_r^↓(Z)=(r+1)Tr ρ d† Z-r Trρ Z d†`.

For the creation port define instead

`q_r^↑(Z)=r Trρ d Z-(r+1)Trρ Z d`.

Both vanish on the thermal state `τ_r` (and on its coherent displacements after centering). They obey

`q_r^↑(Z)=-conj(q_r^↓(Z†))`.

Because conjugation reverses the modular frequency and `ℓ(p_l,p_r)` is symmetric,

`||Z||_{F^↑}=||Z†||_{F^↓}`,

and therefore the dual norms obey the **exact equality**

`||q_r^↑||_{F^↑,*}=||q_r^↓||_{F^↓,*}`.

The latter identifies the reversed-port defect with exactly the entropy-production quantity of the original (ordinary) thermal relaxation generator. No new entropy-production formula is hypothesized.

For the raw squeezed output `γ`, its centered defect at mean reference `r_*` satisfies the **signed convolution identity**

`q_γ^↓(Z)=sqrt(G) q_A^↓(T_AZ)-sqrt(G-1) q_B^↑(T_BZ)`.

To verify it algebraically, pull the bounded output observable back through the squeezing unitary, and write `c†=sqrt(G)a†+sqrt(G-1)b`. Subtract the right side from `(r_*+1)Trγ c†Z-r_*Trγ Zc†`, using the centered-input means. The remaining uncentered terms are

`sqrt(G)(r_*-r_A) Tr[a†,Z] + sqrt(G-1)(r_*+r_B+1)Tr[b,Z]`.

For an output observable `Z`, the commutator identities after the squeeze are

`[a†,Z]=sqrt(G)[c†,Z]`, `[b,Z]=-sqrt(G-1)[c†,Z]`.

Their total coefficient is

`G(r_*-r_A)-(G-1)(r_*+r_B+1)=r_*-G r_A-(G-1)(r_B+1)=0`.

The fixed downstream thermal port contributes its ordinary annihilation defect, identically zero. If `T_i` includes the pullback through that downstream attenuator and `L_i Z=(T_iZ-⟨γZ⟩I)/sqrt(λ_i)`, the general identity becomes

`q_γ(Z)=λ_A q_A^↓(L_AZ)-λ_B q_B^↑(L_BZ)`.

All these equations hold as weak traces against bounded observables on finite-energy inputs; passing to unbounded commutators without regularization would be impermissible. The displayed derivation indicates how to justify them by finite number cutoffs and weighted Hilbert–Schmidt factors, exactly as in OpenAI source Section 04.

## 5. Thermal relaxation intertwining (proved by characteristic functions)

Let `L_r` be the standard quantum Ornstein–Uhlenbeck Lindblad generator with invariant `τ_r` and semigroup `T_t^{(r)}`. For any finite-energy state its symmetric Weyl characteristic function evolves as

`χ_{T_t^{(r)}ρ}(z)=χ_ρ(e^{-t/2}z) exp[-(r+1/2)(1-e^{-t})|z|²]`

(modewise tensor product for `n` modes). The squeezed-output characteristic function factorizes across the independent input groups:

`χ_γ(z)=χ_A(sqrt(G)z) χ_B(-sqrt(G-1) conjugate(z))`.

The extra vacuum/thermal downstream port introduces the factor `χ_D(sqrt(u)z)` and scales the first two arguments by `sqrt(1-u)`. Evolving each input with its own thermal OU semigroup, multiplication of the Gaussian factors produces coefficient

`λ_A(r_A+1/2)+λ_B(r_B+1/2)+λ_D(r_D+1/2)=r_0+1/2`, 

where the last equality uses the **signed** canonical normalization `λ_A−λ_B+λ_D=1`. It follows that applying the independent OU semigroups *before* the Bogoliubov channel is exactly the same as applying `T_t^{(r_0)}` *after* the channel. Differentiating yields the generator covariance needed in the original proof:

`L_{r_0}(γ)=Φ_A(L_{r_A}ρ_A)+Φ_B(L_{r_B}ρ_B)`

(the fixed thermal third input has zero generator), where `Φ_i` denotes the derivative of the physical output with respect to input `i`, holding the others fixed. This identity is for the product-input channel and does not assert complete positivity of time reversal.

**Analytic audit still required:** Differentiation and the equality above must be checked in the precise `W²`-weighted trace topology, not merely at the level of characteristic functions. The source's passive-mixer proof uses total-number preservation, which is unavailable for squeezing. Section 7 records a replacement weighted graph bound; a complete independent audit must check that its use closes every weighted-trace step.

## 6. Centered output energy and regularization identities

The raw output has mean

`μ_γ=sqrt(λ_A) μ_A+sqrt(λ_B) conj(μ_B)`

(with the fixed thermal input mean zero) and centered energy

`e'_γ=λ_A e'_A+λ_B(e'_B+n)+λ_D n r_D`.

Subtracting `nr_0` gives

`e'_γ-nr_0=λ_A(e'_A-nr_A)+λ_B(e'_B-nr_B)`.

Now introduce a distinct small *output replacement* parameter `0<θ<1` and let

`ρ_0=(1-θ)γ+θ τ_{r_0}`, `w_i=(1-θ)λ_i`.

Then

`e'_0-nr_0=Σ_{i=A,B}w_i(e'_i-nr_i)+θ(1-θ)|μ_γ|²`.

The defect satisfies

`q_0=(1-θ)q_γ+θ(1-θ)conj(μ_γ)Tr[(γ-τ_{r_0}) · ]`,

and the mean obeys `(1-θ)|μ_γ|²<=2Σ_iw_i|μ_i|²`. Notice that **all** the output mean and energy identities have exactly the form required for the original cancellation, despite the non-passive interaction.

## 7. Proposed global variational closure and audit points

The original beam-splitter proof is not an abstract black box for general quantum channels. It uses the following precise steps. The signed algebra above supplies the only interaction-specific changes; however, the infinite-dimensional details have **not** been externally or mechanically reconstructed for squeezing.

1. **Contradiction witness and scalar slack.** Assume `(AEPnI)` is false. Approximate the two input states by finite-number-supported states preserving strict violation (energy-constrained entropy continuity and strong continuity of Gaussian unitaries). Choose positive `r_i` near the entropy photon numbers of the witness. Insert the auxiliary thermal attenuator port with `u>0`, choose `ε>0` meeting both signed scalar-slack inequalities in Section 2, and then choose output replacement `θ>0` small enough. On the fixed witness, the regularized objective below is strictly negative uniformly for all sufficiently small `ζ>0`.

2. **Variational objective.** For input states with finite fourth moment, define

   `J_ζ=(S(ρ_0)-n g(r_0))/h_0 - Σ_i w_i(S(ρ_i)-n g(r_i))/h_i + εΣ_i(w_i/h_i)D(ρ_i||τ_{r_i}) + ζΣ_i Trρ_i(1+N_i)^4`.

   Its sublevels have input energies bounded independently of `ζ`: the relative-entropy terms provide positive linear energy penalties while negative entropies grow only logarithmically. The fixed-`ζ` fourth-moment penalty gives trace-norm compactness and hence a minimizer.

3. **Faithfulness, Gibbs equations and Hessian.** Because `ρ_0>=θ τ_{r_0}`, its logarithm satisfies `0<=H_0=-logρ_0<=C(1+N_0)`. For either varied input, the channel's positive observable slice `T_i` satisfies `0<=T_iH_0<=C_i(1+N_i)`. For squeezing the latter follows by expanding `c†c` and bounding the linear expectation terms by `±(a+a†)<=δ a†a+C_δ`, with the other port's finite first moment; it does **not** require total-number preservation. The relative-entropy majorant from source Section 03 yields a normalized Gibbs state at each minimum, with `H_i<=C_i(1+N_i)^4`, finite seventh moment and the exact stationary Gibbs identity

   `((1+ε)w_i/h_i) H_i =((1-θ)/h_0)T_iH_0+ε w_iN_i+ζ(1+N_i)^4+c_i I`.

   The finite-eigenblock entropy-Hessian argument from source Section 03 is interaction-independent and gives `||L_iZ||_i² <=(1+ε)/(1-θ)||Z||_0²`.

4. **Signed metric comparison.** Conditional expectation in the product input gives both arithmetic-form comparisons. Combine Hessian bounds with signed scalar slack to obtain the two signed constant comparisons. Invoke Section 3's signed interpolation lemma to get the sharp reversed-port metric comparison. By the Section 4 dual defect identity, its dual estimate is

   `||Σ_i w_i q_i^{(sign)} ◦ L_i||_{F_0,*}<=A_*`,

   with `A_*²=Σ_i w_i ||q_i^↓||_{F_i^↓,*}²`. Put `M_*²=Σ_i w_i|μ_i|²`.

5. **Mixture correction.** The mixture variance inequality and two-weight logarithmic-mean comparison (as in source Section 04) give

   `||q_0||_{F_0,*}<=A_*+sqrt(2θ) C_0 M_*`,

   where `C_0=(h_0 inf_v F_0(v))^{-1/2}` depends only on fixed reference means. Choose `θ` after `ε` to obtain `||q_0||²<=A_*²+(ε/2)(A_*²+M_*²)` independently of `ζ`.

6. **Stationarity cancellation.** Write `δ_i=L_{r_i}ρ_i`, `σ_i=Trδ_iH_i/h_i`. The stationary Gibbs identities, together with generator covariance in Section 5, give

   `0=σ_0-(1+ε)Σ_i w_i σ_i+εΣ_i w_i Trδ_i N_i+ζΣ_iTrδ_i(1+N_i)^4`.

   The source's exact entropy-production identity is unchanged at each individual port, namely

   `σ_s=||q_s^↓||_{F_s^↓,*}²-(e'_s-nr_s)`.

   Also `Trδ_iN_i=-(e'_i-nr_i)-|μ_i|²`. Insert the Section 6 signed centered-energy identity: all centered-energy terms cancel, leaving

   `0=||q_0||²-(1+ε)A_*²-εM_*²-θ(1-θ)|μ_γ|²+ζ P`,

   where `P=Σ_iTrδ_i(1+N_i)^4<=C` because the generator's number-moment drift polynomial has negative leading coefficient. Thus `A_*²+M_*²<=O(ζ/ε)` and both vanish as `ζ→0`.

7. **Limit.** Uniform input energy bounds and compactness yield subsequential trace-norm limits. The vanishing centered defects and means imply in number-basis weak form `(r_i+1)a_{i,j}ρ_i=r_i ρ_i a_{i,j}`. This forces the `n`-mode geometric product thermal state `ρ_i=τ_{r_i}` by number-basis recurrence, regardless of correlations inside input group. The Gaussian mixer of independent thermal inputs is precisely `τ_{r_0}`, and the output mixture shares this limit. Energy-constrained entropy continuity makes the entropy part of `J_ζ` tend to zero, while its two penalties are nonnegative, contradicting the fixed strictly negative minimum.

If every domain passage in this outline is justified at the source's standard, this proves `(AEPnI)` and its signed multiport analogue. **Those passages have not all received a fresh line-by-line independent audit in this investigation, so the proof is presently a candidate, not an established historic resolution.**

### The non-passive Sobolev replacement needed for step 6

Let `U` be a finite-mode Gaussian Bogoliubov unitary, and `W=1+N_tot` on its complete input/output Fock space. For each integer `k>=0` there is `C_{U,k}<∞` with

`|| W^{k/2} Uψ || <=C_{U,k}||W^{k/2}ψ||`.

Proof sketch: the weighted Fock number norm of order `k` is equivalent to the sum of `||a_{j_1}...a_{j_m}ψ||²` over words in annihilators of length `0<=m<=k`. Since `U† a_j U` is a finite linear combination of creation and annihilation operators, expand each product into finite words. Every length-`m` word is bounded by the `W^{m/2}` graph norm using number-basis shift bounds and the canonical commutation relations. This yields the estimate, and applies to `U†` as well. By taking `k=4,6,7`, this substitutes for the passive source's exact conservation of total number at the weighted trace-class steps. In particular, `K=(W_out²⊗I) U W_in^{-2}` is bounded, so

`||W_out² Tr_env[U X U†]W_out²||_1 <=||K||² ||W_in² X W_in²||_1`

for weighted trace-class `X` (interpret via the weighted factorization). A complete audit must check the corresponding generator approximation and entropy pairings, rather than substituting a bare operator-power monotonicity that is false for exponent `>1`.

## 8. Independent phase-space check: why the shortcut is not CP

The Heisenberg Weyl identities give the exact characteristic-function relation between the amplifier output and a passive mixer of `ρ_A` with the *Fock transpose* `ρ_B^T`: set `t=2G-1` and `η=G/t`; if `τ=BS_η(ρ_A,ρ_B^T)` then

`χ_γ(z)=χ_τ(sqrt(t)z)`.

Hence Weyl Plancherel gives the exact purity identity

`Trγ²=t^{-n}Trτ²<=t^{-n}`.

This purity bound is consistent with existing Rényi-2 bosonic inequalities and does **not** by itself imply the von Neumann EPnI. The linear phase-space dilation `D_t` defined formally by `χ_{D_tρ}(z)=χ_ρ(sqrt(t)z)` is not a positive map for `t>1` on all states. For one mode, take `ρ=|1><1|`, whose characteristic function is `e^{-|z|²/2}(1-|z|²)`. Weyl overlap with vacuum yields

`<0|D_t(ρ)|0>=2(1-t)/(1+t)²<0`.

Thus a proof that treats this dilation as a CPTP channel is invalid. The signed-KMS variational route avoids this nonphysical operation entirely.

## 9. Verification boundary

The signed interpolation lemma, the two signed thermal-balance equalities, the normal-versus-reversed defect adjoint identity, the weak Bogoliubov commutator cancellation, the Weyl covariance of thermal OU semigroups, and the exact centered-energy identity are independently checkable mathematical calculations. The full variational closure above is an **unreviewed mathematical argument** importing substantial machinery from OpenAI's source. The crucial remaining tasks before asserting the 2014 conjecture is solved are: independently audit all infinite-dimensional weighted trace and logarithmic-domain steps under squeezing; verify the non-passive Sobolev replacement in the precise generator topology; check the signed interpolation application against the Lean formalized four-weight theorem; try direct nonGaussian finite-energy counterexamples; and perform an up-to-date specialist prior-art and correctness review. No unrestricted diamond norm, correlated-input, entangled-reference, efficient algorithm or practical experiment claim is made.

This file is a research candidate for review, not a publication-ready mathematical result.
