# Exact primary imports: local two-body synthesis, classical control and comparator

Constructor, 7 November 2026. This supplements the frozen independent initial and `DETERMINISTIC_SWEEP_REVIEW.md`. Sources were downloaded directly from arXiv, SHA-256 pinned below, and PDF text extracted with `pypdf`. `pdftotext` was unavailable. No layout claim is made from extraction.

## 1. Verified fixed-patch two-body compiler

**Barenco et al.** *Elementary gates for quantum computation*, arXiv:quant-ph/9503016v1; Phys. Rev. A 52, 3457 (1995), DOI 10.1103/PhysRevA.52.3457.

Primary PDF `sources/barenco-9503016v1.pdf`, SHA256 `e329e6e56e234a4c572f8eb2d493b07864e308027fe142985fb76e62229e154d`.

Section 7, Corollary 7.6 proves arbitrary (q-1)-controlled one-qubit unitaries have Theta(q^2) basic-operation implementations on q wires. The end of Section 8, PDF pages 27--29 (printed pages 26--28), combines that construction with two-level unitary decomposition and Gray-code paths. It gives an exact Theta(q^3 4^q) basic-operation construction for an arbitrary q-qubit unitary, **using no work bits**. The basic operations are arbitrary one-qubit unitaries and XOR/CNOT. This is the actual source of the conservative m_*(q)<=C q^3 4^q bound in my review; its hypotheses match a fixed DATA-plus-source cooling patch exactly.

The patch size q is a fixed catalogue constant, not N. Thus this exponential-in-q synthesis is a fixed overhead in N and service duration. No uncharged pure ancillary work register is required. All pair couplings inside each patch must be provided or routed; the compiler does not establish a Euclidean layout. Bounded patch size and incidence keep the union interaction graph bounded degree, with a potentially huge constant.

**Dawson--Nielsen.** *The Solovay--Kitaev algorithm*, arXiv:quant-ph/0505030v2.

Primary PDF `sources/dawson-nielsen-0505030v2.pdf`, SHA256 `4cd7033be2dd4265b228ff0a834d07715558b398b8fa16d8365392638fd4ea7e`.

Definition 1 requires a finite instruction set in SU(d), closed under inverse, generating a dense subgroup. Theorem 1 gives operator-norm accuracy epsilon with O(log^c(1/epsilon)) instructions, c about 3.97 for the described algorithm. Section 2 derives a length O(m log^3.97(m/epsilon)) for m separately compiled gates. Global phases do not affect the induced channel. The elementary inequality ||Ad_U-Ad_V||_diamond<=2||U-V||_infinity converts the source's operator error to complete-channel error. Choose every one-qubit approximation to operator error <=delta_syn/(4m_*); the total macro channel error is then <=delta_syn/2.

One-qubit SU(2) compilation with an exact CNOT suffices. Physical CNOT error enters delta_phys. If every primitive comes from a finite universal two-qubit library, use its fixed-dimensional SU(4) instruction-set version and charge its constants. A merely entangling pair of controls does not satisfy the import without a universality proof.

### Nonempty fixed implementation inequalities

Let a>0 be ideal sweep contraction, D_E and q_eff actual energy/support constants, c_cat N macro gates and c_src N fresh thermal spins. Choose operating u_s below all accepted code/distance cutoffs and strict positive fractions

    alpha,zeta <=min[a u_s/(32 D_E q_eff), delta/(64 q_eff)].

Then D_E q_eff(alpha+zeta)<=a u_s/16. Choose a fixed source gap

    Delta_src > beta^(-1) log(8 e c_src/zeta).

This makes p_src<zeta/(8e c_src) at fixed nonzero temperature. In the energy-conserving representation the gap is Jd and beta J must satisfy the corresponding bound; in the powered representation Delta_src is independent of U.

Fix delta_syn<alpha/(64e c_cat), making m_syn a finite constant. Choose per-microgate complete error delta_phys<alpha/(64e c_cat m_syn) and allocate all reset/route/switch/idle contributions another alpha/(32e). These ensure the low-order tail budget after harmless constant rescaling. If continuous noise rate is eta and gate duration tau_micro, eta tau_micro contributes to delta_phys. A finite peak control bound can obstruct this on hardware; it is an explicit feasibility condition, not a measured available parameter.

A physical powered implementation may initialize a source at gap Delta_src, quench its local gap to zero for driven synthesis, and restore the gap before disposal. The quenches, known local phases and finite ramps are charged. Each quench changes energy by <=Delta_src. Alternatively resonant interaction-frame controls retain the gap, with carrier frequency/calibration charged constants. Neither implementation is an energy-conserving thermal operation after JU has been removed.

## 2. Aharonov--Ben-Or: genuine no-classical-control machinery, but quantum interfaces need work

**Aharonov--Ben-Or.** *Fault-Tolerant Quantum Computation With Constant Error Rate*, arXiv:quant-ph/9906129v1; journal version SIAM J. Comput. 38 (2008), DOI 10.1137/S0097539799359385.

Primary preliminary PDF `sources/aharonov-benor-9906129v1.pdf`, SHA256 `75b88121b25c7e4a8766c4e5ee31218be946d25fccecf7b3717687011df32d1f`.

Verified source structure:

* Definition 12 gives encoded gate correctness on every superposition. Theorem 4 gives measurement-free CSS gadgets with bounded spread; Theorem 5 gives the polynomial-code version.
* Section 2.8 defines general local noise by tensor products of per-location channels close to identity in a norm with four stated properties; diamond norm is explicitly a choice. Section 2.10 discusses retained environments under a restricted sparse-correlated model. It does **not** give arbitrary coherent common-B local-generator noise merely from a macroscopic per-round budget.
* Lemma 8 proves sparse paths keep encoded states sparse. Lemma 11 bounds the norm of bad signed paths recursively. These are useful ingredients for reconstructing a full quantum-channel theorem.
* Theorems 10--12 state accurate simulation of a classical function. Section 7.1 starts with duplicated classical input. The final criterion is majority classical readout.
* **Critical interface boundary:** Section 4.2 permits encoding garbage to depend on the input basis state and decoding garbage to depend on the value because those interfaces have classical input/output. Such an encoder may dephase an unknown superposition. These theorems cannot be quoted as an unknown/reference-entangled quantum WRITE/READ theorem.

This is a principled source for compiling the *classical* portions of CFG gadgets into noisy coherent computation. It shows noiseless classical processing is not fundamental; it does not automatically remove that premise from CFG. A rigorous substitution needs raw classical-bit -> encoded-packet and encoded-packet -> quantum-control interfaces. Their O(p) boundary faults may be absorbed into original noisy measurement/control locations only after a positive, jointly sparse decomposition is supplied. Internal classical computation can then be compiled to exponentially small error with polynomial overhead.

Unprotected copying of a measured syndrome bit is insufficient: an early corrupt source can be copied everywhere. Saying classical computation is easy does not prove the needed complete interface. Current ledger: no-classical-control machinery **VERIFIED PREDECESSOR**; full same-contract CFG substitution **OPEN/APPLICABILITY WORK REMAINS**. Keep the already proved isolated stochastic/noiseless-classical hybrid intact at its actual scope.

## 3. Strong powered comparator

**Shtanko--Sharma.** *Complexity of Local Quantum Circuits under Nonunital Noise*, arXiv:2411.04819v1.

Primary PDF `sources/shtanko-sharma-2411.04819v1.pdf`, SHA256 `e9f158dd9330f953d695bab621cb4dd595b6ad0cfd9e4582e2e99d93de0103df`.

This already constructs measurement-free refrigeration/RESETs from contracting nonunital single-qubit noise and universal driven circuits. Theorem 1 (formal, equation 136) states simulation of local noiseless-circuit output at sufficiently weak noise, with polarization/noise dependence. Lemma 7 constructs a RESET; Theorem 4 is its measurement-free threshold wrapper. This is a substantive prior capability.

Its contract uses a fixed, local, contracting nonunital single-qubit channel after each unitary layer, with known fixed point/polarization. It does not admit the present arbitrary retained-bath perturbations without an extra theorem. Its proof initializes logical zero states and uses final Z measurements/majority; it is not an unknown-state quantum-port import. I do not import its asserted exact overhead exponent or threshold proof. A separate audit is needed before relying on them; standard concatenated FT's conservative polylog overhead suffices as a matched comparator.

The current candidate differentiating theorem is direct stability of a local energy-restoring sweep under finite-cone coherent common-bath errors. Thermal-ancilla, measurement-free driven correction and fixed-accuracy synthesis are established ideas. Novelty and full-resource advantage remain NOT ESTABLISHED.

## 4. Source reserve, programme and timing scope

A preloaded O(NK) thermal tape is a finite bath model. For K exponentially many strokes, its future tokens must retain the at-use sparse excitation/reset law. A free noninteracting Gibbs reserve is stationary under its Hamiltonian; independent Gibbs-preserving source noise may also preserve the product law. Arbitrary extra depolarization on every unused token for exponentially long waits drives them toward I/2. The DATA threshold does not certify source storage/isolation. At-use source stability, just-in-time refresh or an explicit reserve model must be named and charged.

The same applies to programme/clock bits. Known programme bits can be independently prepared redundantly and protected by classical coding; unknown classical inputs need encoded ports or a boundary floor. Local trigger jitter belongs in the noise model. A common timing failure affecting O(N) operations violates that model and cannot be assigned a sparse rate from its marginal p. These are the exact quantifiers of the claimed finite service.
