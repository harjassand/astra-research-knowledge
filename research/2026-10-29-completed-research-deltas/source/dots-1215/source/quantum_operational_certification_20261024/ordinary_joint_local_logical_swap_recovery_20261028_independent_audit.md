# Independent audit: joint recovery through local learned reflection controls

28 October 2026. Auditor: `producer-workspace/audit_algebra_extraction`.

**Received under the exact source-family, locality, reset-access, and paid finite-control contracts.** Reviewed source: `ordinary_joint_local_logical_swap_recovery_20261028.md`, SHA-256 `f22c549bcb545387b4761ff31ec90886ff7b677c1d1f32a411b05e65024f89c0`. The previously received one-logical theorem and CPTP-ERM addendum remain unchanged. This is a proof-level joint-channel bridge, not a new count-acquired experiment, not naive marginal composition, and not a quantum/conventional learner separation.

## 1. Scope of the acquisition import

The q-logical channel has one common unknown encoding unitary, operator-valued Pauli error weights, independently reset source calls, and exact compatible logical Pauli pairs, each supported on an unknown width-w interval in known physical coordinates. Calibration prepares one requested logical Pauli eigenstate and maximally mixed states on all other input qubits. The other logical factors join the proof gauge. Thus each logical module is precisely a one-logical local-calibration problem, with the SAME physical marginal `rho=U(I_L/2^q tensor Gbar)U†` and the same weighted true generators used later in the joint proof.

Only two-axis relative calibration margins are needed to import local acquisition and excess-risk comparison. The separately asserted global optimum is not smuggled into those imports. No 4^q table of gauge matrices or Pauli labels is reconstructed. Selected local CPTP maps are used to acquire observables; they are not applied sequentially to the unknown joint state.

For each module, `m=kappa² eta/256` and the received ERM bound give `r_min<=22kappa eta/256<kappa eta/8`. The displayed comparison cap is exactly `512L/(kappa t)` with `t=kappa eta/(4h²)`. The tournament therefore gives

`r_selected <=2r_min+t h² <kappa eta/2`,

and `ell0_i<=2r_selected/kappa<eta`. The one-candidate case skips all zero-height/log-zero formulas. Fresh banks, the coarse conditioning, colored disjoint-patch marginal experiments, and the complete finite CPTP feasibility repair retain their earlier contracts. Failure probabilities sum over all q modules; their source calls are not implicitly shared.

## 2. Sign rounding of actual CPTP pullbacks

For a CPTP qubit channel, Bell/Pauli-twirl positivity gives the individual inequality `1-t_jj<=2ell0_i`, not merely a sum over axes. Since `A_j=D_i†sigma_j` is a Hermitian contraction,

`Tr rho(A_j-B_j)² <=2(1-t_jj)<=4eta`.

Because the true B commutes with rho, simultaneously diagonalize them for proof. For each true eigenvalue `b=+/-1` and each eigenvalue c of a Hermitian C, an opposite sign satisfies `|b-c|>=1`. In the overlap expansion weighted by the eigenvalues of rho,

`Tr rho(B-sign C)² <=4 Tr rho(B-C)²`.

This includes arbitrary reflection completions on the zero eigenspace of C. It requires no commutation of C with rho, no lower eigenvalue bound for rho, and no spectral gap at zero. The weighted Hilbert–Schmidt triangle inequality plus `||C-A||<=sqrt(eta)/2` gives the stated `delta_j<=25eta`.

A backward-diagonal representation with a known exactly unitary reference circuit and signed finite labels produces an actual reflection control. Its universal-gate implementation is separately approximated under the whole-process budget. Neither learned within-pair anticommutation nor learned cross-pair commutation is assumed. Cross-frame alignment is not supplied: the operators are acquired in the same known physical coordinate system, with their known input labels fixing the intended logical axes.

## 3. Exact invariant marginal and the full reference

For global entanglement fidelity, purify the entire q-logical maximally mixed input by a reference R, the gauge state by E, and the receiver ancilla mixtures by local references S. These are proof registers; no training algorithm sends or retains a protected reference through the source. The initial reduced state on the physical register P and ALL receiver ancillas A is

`rho_PA=(U tensor I_A)[I_(L,A)/2^(2q) tensor Gbar](U† tensor I_A)`.

Every ideal elementary encoded CNOT acts only on L and A, identically on the gauge. Consequently every ideal elementary prefix preserves this exact reduced state. This remains true when physical supports overlap and the gauge is correlated across those supports. It is an unconditioned identity; it need not hold for a pure receiver-ancilla initialization, a coin-conditioned history, an arbitrary payload marginal, or an approximate learned prefix. Discarding the receiver mixture preparation record is therefore part of the stated operational service.

The ideal three-CNOT sequence for each i swaps encoded logical i with its distinctly labeled ancilla A_i. Common-U compatibility of the TRUE generators makes all those ideal swaps jointly correct. The actual gates are unitary simply because their learned controls are reflections; they need not form a Pauli representation. The whole physical register and all already extracted output ancillas are retained until the sequence ends.

Let `Delta_Z=C_Z(B')-C_Z(B)`. Then

`Delta_Z=(B'-B) tensor (I-X_A)/2`.

The invariant ancilla mixture satisfies `Tr[(I_A/2)(I-X_A)²]=2`, giving squared vector error `delta_Z/2`. For `Delta_X=(B'-B) tensor |1><1|_A`, the squared error is `delta_X/2`. These values use only the relevant reduced state, so the entire reference R and the purifying E,S remain present in the underlying vector calculation.

## 4. Joint hybrid bound, not marginal-channel composition

Telescope the full actual-minus-ideal unitary product with IDEAL gates before each difference and ACTUAL gates after it. Every latter suffix is unitary and preserves vector norm. The former ideal prefix has the invariant reduced state just proved. Cauchy–Schwarz over the 3q elementary errors yields

`||psi_actual-psi_ideal||² <=3q sum_i(delta_Zi+delta_Xi/2)`.

The ideal final pure state has the complete `|Phi>_(R,A)` as a tensor factor. Let `Pi=|Phi><Phi|_(R,A) tensor I_(P,E,S)`. Then

`ell0_joint=||(I-Pi)psi_actual||²`

`=||(I-Pi)(psi_actual-psi_ideal)||² <=||psi_actual-psi_ideal||²`.

This proves the JOINT Bell-loss bound, including entanglement between logical inputs and with the whole reference. No separate marginal fidelity is being multiplied or promoted to a joint channel guarantee. Substituting `delta_j<=25eta` gives `ell0_joint<=(225/2)q² eta` exactly as stated. The conservative q² amplification is paid explicitly.

The three logical CNOTs can be implemented using three controlled local reflection gates and four receiver-ancilla Hadamards per logical qubit. A maximally mixed ancilla may be prepared by a reset, a fair private bit and a conditional X, followed by discarding that bit. The finite reference-state proof does not require physically retaining S or supplying entanglement to the source.

## 5. Global comparator: the extra dominance promise is indispensable

Let `d=2^q` and let `K=(id_R tensor D†)(|Phi><Phi|_(R,out))` after pulling back the common encoding. For each complete Bell-Pauli basis vector `|Phi_alpha>_(R,L)`, define the positive gauge effect

`T_alpha=<Phi_alpha|K|Phi_alpha>_(R,L)`.

Summing over the full d² Bell basis gives

`sum_alpha T_alpha=Tr_(R,L)K`

`=Tr_L[D†(I_out/d)]=Tr_L[I_(L,g)/d]=I_g`.

Thus these effects form a proof-only POVM for EVERY full CPTP decoder, with no dimension-dependent normalization missing. The noisy-source fidelity is `sum_alpha Tr G_alpha T_alpha`. The separate all-alpha operator dominance `G_I>=G_alpha` implies the unrestricted optimum `Tr G_I`. Moreover

`regret=sum_(alpha!=I)Tr(G_I-G_alpha)T_alpha`

`<=Tr G(x)(I-T_I)<=4Tr Gbar(I-T_I)=4ell0_joint`.

The final inequality follows by scalarizing the positive four-coordinate matrix quadratic: its value on a unit x is at most its coefficient trace, which is four times the anchor average. There is no factor 4^q in this transfer and the proof POVM is not acquired.

The extra dominance condition does not follow from the local margins. The source's q=4 example is correct. Independently, already at q=2 the scalar weights `p_I=3/10`, `p_(X1X2)=4/10`, `p_(Z1Z2)=3/10` have both local generator contrasts positive but make identity correction suboptimal. Without dominance, the virtual ideal-channel joint extraction theorem survives, while the claimed unrestricted noisy-source near-oracle transfer does not.

With `eta=epsilon/(16384q²)`, the uniform noisy-source decoder regret is at most `450epsilon/16384<epsilon/20`.

## 6. Actual global ordinary validation and encoder acquisition

Product marginal pass/fail tests are insufficient for global Bell loss. The source instead permits known Clifford entanglement WITHIN the q-qubit input block, without a protected external reference. A uniform Clifford applied to `|0^q>` produces the finite stabilizer-state ensemble. Its two-design proof is self-contained: Pauli random signs eliminate distinct Pauli cross terms, Clifford transitivity makes all nonidentity Pauli second moments equal, and purity fixes their sum to d-1. Therefore

`E[rho_s tensor rho_s]=(I+Swap)/(d(d+1))`.

For every TP joint channel, including nonunital ones, preparing such a state and measuring its survival after the actual joint decoder has Bernoulli error `d/(d+1)*ell_global`. The multiplier is bounded away from zero, so the ten-feature nonnegative quadratic encoder design has no exponential variance penalty. At tolerance `epsilon/8`, its additive Bell penalty is at most `epsilon/4`, and (21) is the corresponding conservative deterministic count cap.

The exact ideal Clifford sampler can recursively sample a nonzero vector in the current symplectic complement, then a uniform partner in the affine hyperplane with symplectic product one, and recurse on their common complement. The number of continuations is independent of the chosen pair, giving the uniform symplectic group. Adding uniform Pauli signs gives the Clifford action up to irrelevant global phase. Partners are sampled directly by linear algebra; only nonzero-vector trials require rejection, with failure at most 1/4. Capping all such trials with a union-bound budget supplies the declared finite whole-process discrepancy. Symplectic elimination gives polynomial-q known Clifford gates; all gate, random-bit, readout and routing costs remain paid.

If known entangled input-block states or their inverse-Clifford output measurement are disallowed, this particular global fast validation is not available. The source expressly marks that weaker product-only model as outside this conclusion.

## 7. Complete physical ledger and the diamond distinction

The complete cap contains q separate local acquisition modules, global encoder counts, and one final payload. The joint receiver is invoked only for the `N_count+1` global tests/payload, while local modules pay their own measurements. Each block source call carries q logical input qubits and emits n output qubits; the stated qubit-use/exposure ledger prevents conflating block counts with single-qubit communication.

The deployed receiver retains n physical plus q ancillary data qubits and uses 3q controlled width-w reflections and 4q Hadamards. Unknown-patch acquisition requires collective copy memory and its interconnect. Ancilla labels and physical-coordinate tracking/restoration are necessary on a nearest-neighbor line; the stated `O(q(n+q))` routing witness is conservative. Output Clifford validation adds its own polynomial-q gates and routing. A single linked operational error budget covers every adaptive invocation, numerical-control synthesis, mixed-ancilla preparation and truncated random sampler.

Bell fidelity is a joint reference-sensitive statement but not a dimension-free untwirled diamond guarantee: the displayed general bound `min(2,2*2^q*sqrt(ell))` is safe. The optional discarded-key whole-logical Pauli twirl changes the averaged service to a possibly correlated Pauli channel with the same Bell loss, for which unhalved diamond error equals `2ell`. This requires the additional before/after Pauli controls and hidden/discarded randomness; it is not a per-key or key-exporting statement.

## 8. Exact deterministic evidence and boundary

`joint_local_logical_swap_independent_check_20261028.py` uses prescribed rational matrices only: no source calls, RNG, acquisition run or external-reference experiment. It checks two logical qubits encoded into three physical qubits with a mixed gauge, overlapping true supports, learned crosscommutation failure, and learned within-pair anticommutation failure. All six ideal prefixes preserve the reduced physical-plus-ancilla state exactly. Gate errors are exactly the displayed `delta/2`. A separate Kraus-trace calculation gives

- joint Bell loss `509100501/10510100501`;
- purified hybrid squared norm `60602/1030301`;
- displayed upper bound `36/101`.

It also confirms the ideal joint fidelity is one and that replacing receiver mixtures by pure `|00>` generally breaks the invariant-state proof. A second exact check enumerates all 60 two-qubit stabilizer states and verifies the complete projective-two-design moment. A nonunital amplitude-damping test has global Bell loss `9/25` and ordinary stabilizer-test error `36/125`, exactly the factor 4/5 required by (20). All checks pass and are supplemental to, not substitutes for, the general proofs.

Received claims do not include approximate source locality, incompatible true algebras, nonreset/drifting sources, automatic global dominance, product-only global validation, multiple-input-block source memories, low practical constants, a sampled experiment, or advantage over the equally informed conventional learner. The latter has the same local ERM, reflection-control, joint-swap and global-validation construction.
