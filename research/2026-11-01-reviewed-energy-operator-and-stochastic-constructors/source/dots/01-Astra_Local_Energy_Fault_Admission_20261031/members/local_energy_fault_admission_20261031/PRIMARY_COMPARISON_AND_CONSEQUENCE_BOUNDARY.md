# What the local occupation certificate buys, and what was already available

31 October 2026. Comparison and consequence assessment; separate from the frozen proof and its independent receipt. No novelty or practical-advantage claim follows from this bounded source check.

## 1. Existing threshold machinery is the consumer, not the discovery

The reviewed local proof is `QUANTUM_OCCUPATION_LOCAL_ADMISSION_CANDIDATE.md`, SHA256 `0b0bd7ffa77e9c90323be91d5dec929b5bbd66d0c059ad783357838bf5ba010e`; its receipt is `INDEPENDENT_LOCAL_ADMISSION_REVIEW.md`, SHA256 `5d9fd86eef4e81dd4558515375cf5e0a2da07592e0a0c131362ca2e459fe3238`.

The output is the established inclusive **amplitude** premise: for every selected set S of circuit locations, the norm of the sum of all fault amplitudes containing each selected location is at most eta^|S|. It is not a positive fault probability. There is no need to invent another Pauli-effect or threshold receiver.

Aliferis–Gottesman–Preskill, quant-ph/0504218, Section 11, already develops local non-Markovian amplitude receiving with persistent bath memory. Aharonov–Kitaev–Preskill, quant-ph/0510231, treats shared-bath spatially correlated Hamiltonian noise. Their actual code, gate, preparation, measurement, error-correction and fault-propagation assumptions remain necessary. Their numerical threshold values cannot simply be attached to an uninstantiated schedule here.

Primary links: https://arxiv.org/html/quant-ph/0504218v3 and https://preskill.caltech.edu/pubs/preskill-2006-long-range.pdf .

## 2. Bypassing raw high-frequency norms is also established

Ng–Preskill, *Fault-tolerant quantum computation versus Gaussian noise*, PRA79,032318 (2009), explicitly replaces a restrictive raw interaction-norm condition by a Gaussian correlation criterion. Its Eq9 is the inclusive bad-amplitude condition; Eq27 bounds its strength through a location-to-all-space-time integral of the absolute two-point function. Wick factorization is load-bearing. The paper also states initial-state and entropy-removal/sink premises. Thus neither high-frequency averaging nor a microscopic route to a high-order threshold input is new in itself.

The present certificate differs in assumptions: it allows non-Gaussian finite source qubits, coherent number-conserving transport and arbitrary initial finite-source correlations, but requires the specified initialized Markov loss/injection fields and a number-controlled interaction. The Gaussian theorem and this certificate do not dominate one another wholesale. The correlation formula cannot be used for an interacting non-Gaussian source solely because its covariance is known; conversely this occupation proof does not apply to general oscillator noise.

Actual primary inspected: introduction, Eq9, Wick passage, Eq27 and initial-state/entropy-removal sections, https://preskill.caltech.edu/pubs/preskill-2009-gaussian.pdf .

Preskill, *Sufficient condition on noise correlations for scalable quantum computing*, 1207.6131v2, Section2/Theorem1, already treats spatially distributed many-qubit Hamiltonian terms with a hierarchy of summed operator-norm bounds. Its Section1 explicitly recognizes dressed/coarse-grained qubits and the need for entropy removal. Its criterion is not just independent one-point errors. The new proof does not replace that hierarchy by a covariance assertion: it directly acquires an inclusive-amplitude bound from a separate local occupation inequality. Primary Section2 and the first-insertion proof were inspected: https://arxiv.org/html/1207.6131v2 .

## 3. Randomized compiling is a strong ordinary alternative, not a missing bridge

Winick et al., 2212.07500v1, SectionIII.2 retains a persistent ancillary environment and gives a Pauli-tailored representation. SectionIII.3 explicitly discusses key-dependent leakage that can defeat suppression. Environment-retaining Pauli structure alone is not an arbitrary all-subset p^k bound, and a frame update is not automatically an actual physical sign gate. Here no physical twirling or private key is required: the occupation estimate directly controls fault amplitudes. Existing randomized compiling can still be applied when its actual gates and key-dependent errors are acquired, but it is not credited with a free operation in the proof.

Actual primary relevant sections read: https://arxiv.org/html/2212.07500v1 .

## 4. Accessible Astra capital already supplies the downstream bridges

These actual full source bodies were read; their review scopes remain separate from the new occupation receipt:

- N951, `FINITE_CONTROL_COMPILER.md`, SHA `cb0a668684fa9d7160f77d471fd143d027a1a52a76e3feeaa73e677e241cdbda`: disjoint physical windows, shared bath, selected Pauli effects, finite own-key control defects and signed inclusive paths. Its microscopic inputs are actual integrated interaction/control bounds; source memory is not discarded.
- N1467, `CP_CAVITY_LOCAL_FAULT_BRIDGE.md`, SHA `cd254da562171a38028ca942b3dfbaa85abc5477b464c5defc465c93a488f27f`, plus `FAULT_CLASS_AND_GADGET_RECEIVING.md`, SHA `9576281ca42a4cd0979b3d049b93a7aca84ecc52ac133ef6c72f852f281241b3`: bounded incident complete-norm input, CP cavities and signed disjoint-gadget receiving. No product-probability claim is needed.
- N1483, `08_STANDARD_FT_SUPEROPERATOR_RECEIVING.md`, SHA `751b5452f3bea9bbe31a9d833b569a144b45977d8503931c7f6dcc3aa37da7fc`: actual conventional scheduled code gadgets, finite reset/gate discrepancies, signed good-map factorization and trace-defect normalization. It does not supply an autonomous physical scheduler, raw unknown-state ingress or free readout.

Read-only repository packets: https://github.com/harjassand/astra-research-knowledge/blob/main/knowledge/current/packets/N951.json ; https://github.com/harjassand/astra-research-knowledge/blob/main/knowledge/current/packets/N1467.json ; https://github.com/harjassand/astra-research-knowledge/blob/main/knowledge/current/packets/N1483.json . Their packet metadata and internal receipts must not be relabeled as a new independent audit by this note.

The exact latest P2 commutator-sensitive physical-admission card remains **unlocated**. No locator, theorem equivalence or priority conclusion is fabricated. A large catalog fetch returned a size/unsupported error; no alternate transfer or broad catalog crawl was attempted. This is an explicit comparator boundary, not evidence of absence.

## 5. The concrete new receiving operation in this checkpoint

Given an actual local loss/transport/injection model and complete circuit-location assignment, check

  gamma=1-2 sup_i sum_j |J_ij| >0,
  g=maximum source indices per location,
  b=acquired unwanted coupling bound,
  a=physical injection bound, tau=actual longest location duration.

A source index is assigned to at most one active location. The proof then constructs a backward product weight with selected support; its column-sum decay eliminates exterior volume. Complexifying each selected unwanted coupling gives a single common jump-history dilation. A multivariate Cauchy integral extracts all inclusive fault amplitudes. For ideal supplied gate generators,

  R=gamma sqrt(lambda)/(8b)>1,
  eta=exp[g(1+a tau)/4]/(R-1).

A real control-error budget epsilon_ctl is included by multiplying the numerator by exp(R epsilon_ctl) and choosing R small enough. Strong real exterior density interactions and diagonal source Hamiltonians can remain on because they commute with the weight. The bound is uniform on finite source/system/reference inputs with the loss/injection reservoir fields initialized as specified.

This replaces a potentially useless raw norm sqrt(lambda)b tau by a small occupation-sensitive amplitude. It does not reconstruct a giant reduced channel, assume Gaussianity or factor marginal error probabilities. The ongoing injection term a tau prevents the result from being merely a warm-transient wait/preparation trick.

## 6. Restrictions that decide whether this is physically useful

The proof does NOT provide the hardware that achieves high loss, subcritical transport and low injection. Raising lambda while holding a fixed is a substantive physical resource, not a free rescaling of an arbitrary thermal bath. The coupling n_i A_i cannot create source excitations. If the source interaction creates excitations at order sqrt(lambda), a nonzero leading logical dissipator can survive rapid damping; it must be an intended/correctable operation or an explicitly paid error. Our result does not erase that disturbance.

The complete microscopic graph and local rate/norm certificates, or a known finite program proving uniform bounds, are inputs. Sparse unknown-device measurements do not certify those promises for free. Calibration uncertainty must leave a verified margin in gamma and in the actual gate/control bounds. A small scalar eta is not a full fault-tolerant machine: the actual code, reset supply, encoding, gates, classical control hardware, routing, readout and execution costs remain external acquired operations.

The diagnostic at lambda=10^12 is only a sufficient mathematical amplitude parameter. It is not a demonstrated achievable damping ratio or a competitive resource estimate. No cost comparison against equally informed conventional cooling, decoupling, coding or randomized compiling has shown practical superiority.

## 7. Judgment

This is a more substantive local-energy step than another source-compiler variant: it earns a simultaneous selected-history norm with a quantum interacting source and with exterior interactions retained. It identifies precisely how a local loss/transport certificate can feed existing robust-computation machinery.

It is still a restricted admission theorem built from ordinary components. Further investment is justified only to test a consequential physical mechanism with actual loss/injection/control acquisition, or to close the genuinely harder source-creating/fixed-diffusion case without losing the high-order bound. More broad source coverage or a smaller uninstantiated threshold constant would not by itself establish the north-star consequence.
