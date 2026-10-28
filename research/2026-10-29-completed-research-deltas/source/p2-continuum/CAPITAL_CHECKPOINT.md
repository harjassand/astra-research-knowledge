# Astra P2: from a bath representation to complete quantum instruments

28 October 2026. Successor research checkpoint. The original handoff and its acquired archives remain unchanged; the exact uploaded handoff ZIP is preserved inside this package.

## Outcome and scientific ownership

I selected a reusable instrument for solving nonlinear continuum dynamics and computing detector records. The inherited baseline bath representation is already accurately controlled. Its missing strong propagator, physical output collection, and complete error correlations now have greater leverage than a smaller scalar representation bound or another isolated gate.

The new work constructs a conditional channel-certificate interface, proves how coupling and detector kernels determine a compatible instrument, supplies an actual interval-certified nonlinear continuum example, and extends the calculation to an untruncated oscillator source and to a finite smooth waveform. The latter two remain numerical diagnostics where their error integrals and compression arithmetic have not been enclosed. A new temporal-span obstruction explains why a seemingly reasonable representation cannot be repaired just by adding more photon capacity or shrinking time steps.

This is progress in evaluating and discriminating physical mechanisms. It does not establish a useful computing operation, a compatible physical P2 device, a logical error rate, an efficient general simulator, or a computing advantage.

## 1. What the new instrument takes as input

Let f_x be the bath vectors used by the source vertices. Supply the coupling kernel G(x,y)=<f_x,f_y> and, for each collected detector port r, a kernel D_r(x,y)=<f_x,E_r f_y>. The consistency requirement is that every finite matrix D_r is positive and sum_r D_r<=G. These conditions suffice to realize a one-particle Hilbert space and a passive output collection with effects E_r. The proof uses bounded positive forms on the quotient by the null space of G, followed by a passive dilation.

A local scalar spectral density supplies G for a single coupling coordinate but does not specify D_r. A beamsplitter after the interaction changes which detector sees a photon without changing the source's local bath density. This is a material physical interface, especially when an LC trap has intrinsic loss or a readout port has a finite collection window.

Represent the source-output map as V=sum_j X_j tensor |alpha_j>. The coefficients X_j act on the complete chosen input code, not one fitted input state. Exact coherent overlaps and Weyl displacement identities evaluate its source-reference Gram matrices. Source sine vertices may be represented by displaced-Fock input packets: the input labels |0>,|1> do not truncate physical output leakage.

For a no-click set D, the bath operator is Gamma(I-sum_D E_r), giving kernel

    K_D(k,j)=exp[-(||alpha_k||²+||alpha_j||²)/2
                 +<alpha_k,(I-sum_D E_r)alpha_j>].

The unnormalized source record map is sum_jk K_D(k,j)X_j rho X_k†. Inclusion-exclusion gives every binary record. It retains quantum interference, unobserved reservoirs and correlations. In general Gamma(I-E1)Gamma(I-E2) is not the same experiment as joint no-click Gamma(I-E1-E2). Independent matched-converter formulas cannot be imported from port marginals alone.

## 2. The actual complete-channel certificate

For a piecewise differentiable proposed map V(t), define R=dot V+iHV. On a declared d-dimensional input code, including arbitrary entanglement with a reference,

    ||V_exact(T)-V(T)|| <= initial error
        +integral sqrt(lambda_max[R†R])dt +sum knot-jump norms.

For an isometric endpoint this is also a full-output half-diamond bound. Otherwise a finite input-Gram polar repair costs at most a factor two in the displayed error. This repair is mathematical channel construction; it is not a physical erasure flag.

R itself is a finite packet list, so R†R is obtained from finite Gram contractions. The exterior part must be retained. In particular, Q†H²Q cannot be replaced by (Q†HQ)². Kernel arithmetic, source approximation, packet compression and time quadrature remain separately chargeable.

An exact compression theorem complements the residual: for isometry V and retained projection P, with delta²=lambda_max[V†(I-P)V]<1, polar-repaired compression has error sqrt[2(1-sqrt(1-delta²))]. This scales as discarded amplitude, not discarded population.

The assumptions explicitly use strong measurability and integrable norm bounds. Weyl paths need not be norm-continuous. For the inherited ideal-line spectrum, a divergent second frequency moment also makes an unqualified derivative of f_t invalid. Fixed packets within each smooth interval avoid that problem.

The full proof is `theory/CONTINUUM_PACKET_CHANNEL_THEOREM.md`. The actual independent proof reading is hash-pinned in `physical_attack/ROOT_THEOREM_PROOF_REVIEW.md`. The detector-kernel realization has a separate proof and actual review.

## 3. A genuinely evaluated continuum example

The rigorous small example has one source qubit and a continuum rho(omega)=2.1exp(-omega), omega>=0. Time and frequency are dimensionless. Two specified nonlinear kicks use Pauli X and Z, areas 1/2 and 3/4, at times 0 and 3/5. The bath is vacuum. Collection is explicitly E1=.6I, E2=.25I. This is not the baseline circuit, a notch spectrum, or an approximation to the delivered P2 waveform.

The exact Bessel expansion, truncated at |n|<=8 for each kick, uses 289 coherent packets. Retained Bessel coefficients are rational Taylor midpoints with charged remainders. The complete omitted tail is bounded rationally. Kernel sums use outward Decimal intervals, rigorous trigonometric remainders and exact rational arguments. No bath frequency grid or photon cutoff enters the certificate.

The unnormalized map error is <=8.734220304380286...e-10. Its explicit polar CPTP construction has complete-output, arbitrary-reference half-diamond error

    <1.747e-9.

This is an evaluated benchmark channel error, not the predecessor's representation error and not a device error rate. Exact-model event intervals follow from max(0,sqrt(p_V)-epsilon)² <= p <= min(1,(sqrt(p_V)+epsilon)²).

| Record, source input | Certified conservative interval |
|---|---|
| Neither, basis state 0 | [0.6952296340,0.6952296371] |
| Only 1, basis state 0 | [0.1542934052,0.1542934066] |
| Only 2, basis state 0 | [0.0472082401,0.0472082409] |
| Both, basis state 0 | [0.1032687175,0.1032687187] |
| Neither, plus-i superposition | [0.5722791839,0.5722791866] |

The source coherence materially changes the records. A further outward-arithmetic consequence gives actual both-click probability about .103268718, while the product of port marginals is about .038757165: the covariance lies in [.0645115520,.0645115541]. Marginal multiplication would be a large model error here, not numerical noise.

`code/certified_continuum_kicks.py`, `data/certified_continuum_kicks.json`, `theory/CERTIFIED_KICK_EXAMPLE.md`, and `code/certified_correlation.py` preserve the construction. Its first execution took about 17 seconds here, which is a small-instance observation only. The actual independent audit replays the exact intervals and separately checks phases and a converged Fock implementation; that Fock calculation does not replace the rational/interval certificate.

## 4. Stronger source and finite-waveform tests, at their actual scope

The oscillator benchmark retains the full product-sine interaction, source inputs span{|0>,|1>}, and all source/bath Fock outputs through displaced-Fock packets. Two noncommuting-time kicks of areas 1.5 and 1.2 are evaluated for a one-oscillator bath and for a genuine positive-frequency shifted-gamma continuum. In the latter, the two pulse times span two collective directions exactly for that kicked model, without frequency discretization.

The continuum run retains 744 packets. Its summed floating compression-map norm diagnostic is 8.53e-4 and its selected Gram condition is 3.65e7. Full-input differences from an independent three-oscillator calculation decrease from .03078 at cutoff 12 to .0005784 at cutoff 44. The comparison includes the packet mass outside the reference cutoff. This checks closure and signs, but is not a certified compression error or physical capture probability. An unweighted selection failed by choosing remote low-weight directions and exhausting memory; that failure is preserved. A 512-rank ceiling also produced a larger error floor.

The next attack was an actual smooth, strong continuum waveform:

    H(t)=12sin²(pi t/.6)[cos(t)X+sin(t)Y] sin Phi(f_t),
    rho(omega)=2.1exp(-omega), T=.6, action=3.6.

A fixed-packet Galerkin trajectory uses a projected-Hamiltonian exponential on each time cell. Its equation residual is evaluated against the continuously varying full Hamiltonian. The complete input residual matrix uses the exact full-space sine-square kernel. It includes both temporal freezing and omitted packet directions.

| Trial space | Rank | Cells | Integrated full residual diagnostic |
|---|---:|---:|---:|
| Two temporal directions, displacement integers -4..4 | 81 | 80 | .36501 |
| Three temporal directions, -2..2 | 125 | 320 | .05572 |
| Three temporal directions, -3..3 | 343 | 160 | .03327 |
| Four temporal directions, only -1..1 | 81 | 160 | .17689 |

These are floating diagnostics, not certified channel bounds. In the 125-direction/80-cell run, changing per-cell quadrature from order four to eight changes the integral by 3.0115e-4. In the largest trial the exterior form has a sampled minimum eigenvalue around -8.19e-11, and the Gram condition is about 5.47e6. Both limitations remain in the data. Refining time alone cannot cure the missing bath span; adding temporal directions without displacement depth is also inadequate.

### A useful representation obstruction

For a fixed temporal one-particle span W, write f_t=p_t+q_t and tau=||q_t||². The omitted vacuum factor has orthogonal even and odd residual components. Their squared coefficients are (1-exp(-tau))²/2 and (1-exp(-2tau))/2. For a unitary source Pauli and every normalized trial confined to the entire Fock space over W, the equation residual is at least

    |A(t)|(1-exp(-tau(t)))/sqrt(2).

Even unlimited photon capacity inside W cannot push this fixed-span integrated residual certificate below its integral. Floating evaluations for the smooth model are .0279205 for two endpoint vectors, .000207431 for three time vectors, and .00000255122 for four. The proof is exact; those evaluations are not interval bounds.

This is not a lower bound on actual endpoint channel distance or physical noise. It identifies when to change representation. A root extension replaces the unit source factor by ||S(t)V(t)|| for a nonunitary bounded source operator, so a source sine is not incorrectly treated as an involution. Multiple omitted vertices can interfere and do not inherit a sum of these lower bounds.

The full continuous proof, receipts and endpoint data are in `solver_instrument/`; the root's actual independent proof reading and separately labelled extension are in `reviews/ROOT_CONTINUOUS_PROOF_REVIEW.md`.

## 5. Strong competing physical mechanism

I investigated lowering the multiplier pump below the source frequency. A 5 GHz source and .5 GHz pump can emit three photons around 1.5 GHz while returning energy to the pump. One pump quantum can no longer create a source excitation plus positive-frequency bath radiation.

For the hypothetical delivered pulse e(t)=sin^4(pi t/7ns), peak coefficient <=6 rad/ns, and positive-frequency vacuum bath, the full first Dyson vacuum-excitation vector obeys

    ||psi_1||² <1.056e-13.

The proof uses the source's odd-level energy threshold, the smooth-envelope Fourier tail, and the full product-sine vacuum norm. It covers every odd source level and odd bath multiplicity at this order. It is not an all-orders probability or dark-count certificate. The strong-conversion action still forbids casually dropping later orders.

A concrete omitted channel appears at two vertices: the source can return to vacuum while creating a pair. With finite switching, one member can be detected and the other soft and unobserved. Its exact no-source-cutoff correlator is

    <0|sin(sqrt(x)q(t2))sin(sqrt(x)q(t1))|0>
      =exp(-x)sinh[x exp(-i omega_a(t2-t1))].

It multiplies a four-coherent-packet bath vector, a useful adversarial target for the solver. The long-time sinusoidal screen is distinct: a detected-plus-soft event first becomes on-shell at order four for the .5 GHz pump, rather than the sixth order obtained by confining every photon to the detection band. Nonlinear delivered harmonics and finite-time tails alter that screen.

The competing thermal screen is substantial. With an assumed 20 mK thermal traveling field, .28 GHz rectangular bandwidth, efficiency .9 and 7 ns window, Gaussian counting gives:

| Center frequency | Thermal any-click probability | Equilibrium buffer nonvacuum probability |
|---|---:|---:|
| 1.5 GHz | .0488511 | .0273392 |
| 7 GHz | 9.11256e-8 | 5.06995e-8 |

These are separately declared thermal-model diagnostics, not a noisy multiplier channel or hardware temperatures. Raising the triplet-count threshold costs genuine-event efficiency; passive waiting cannot reset below the assumed thermal equilibrium floor. Passive tripling itself is existing work: Fraudet et al., PRL 134,013804 (2025), arXiv:2405.00411v1. A quiet, switched stored-source measurement remains unconstructed.

The decision is to retain this mechanism without selecting it over the high-frequency notched route. A small first-order vacuum coefficient is insufficient against pair emission, thermal counts, switching, preparation and reset. The instrument is useful because these mechanisms need complete records under one compatible model.

## 6. Prior constructions and stronger alternatives

Coherent-state superpositions and Schrodinger residuals are not inventions of this continuation. Gheeraert, Bera and Florens already combined them for ultrastrong waveguide dynamics; Martinazzo and Burghardt developed local variational error and adaptation. The VariDavy implementation was inspected for practical conditioning machinery, not executed or imported. Its packet grouping and linear solves reinforce that conditioning is an algorithmic issue.

A strong structured-bath alternative is Riva et al., *First-principles study of dispersive readout in circuit QED*, arXiv:2604.11722v1. TEDOPA/MPSDynamics treats driven structured baths without the usual Markov or secular approximation. Its two-level source, linear bath coupling and convergence-based numerical checks differ from this instrument's nonlinear Weyl/full-input certificate interface. It also finds driven behavior sensitive to a notch; that supports evaluating the new bath rather than copying an unpumped or baseline certificate. No superiority over this implementation is proved.

The SWS dual-rail comparator retains its actual delayed-check advantage. Tsunoda, Teoh and colleagues' error-detectable bosonic entangling gates supply error-closure machinery that may help a later actual-gate loss-propagation construction. Neither is dismissed because P2 can defer classical records.

Primary sources used:

- https://arxiv.org/pdf/1601.01545 — coherent packets and residual diagnostics, version 2.
- https://arxiv.org/abs/1601.00531 — single-coherent-packet relaxation artifacts.
- https://arxiv.org/abs/1907.00841 — local variational error.
- https://arxiv.org/html/2604.11722v1 — structured-bath readout; preserve its v1/header date discrepancy.
- https://github.com/Mantas-Jakucionis/VariDavy — inspected implementation, exact blob evidence saved.
- https://doi.org/10.1103/PRXQuantum.4.020354 — error-detectable bosonic gates.
- https://doi.org/10.1038/s41586-026-10822-y — governing SWS version of record; acquired predecessor scope retained.
- https://arxiv.org/abs/2405.00411 — passive photon tripling, published PRL 134,013804.

## 7. Error ledger and the unclosed computing interface

| Quantity | Actual status |
|---|---|
| Inherited baseline strong-core/weak-continuum bound | Accepted representation theorem at its original rounded circuit, dressed vacuum, duration/action assumptions; not replayed anew here |
| New two-kick example <1.747e-9 | Exact-tail/interval-evaluated approximation of its stated finite-source continuum model; specified passive detector records also enclosed |
| Oscillator packet compression | Floating map-norm and independent Fock diagnostics; no interval compression certificate |
| Continuous waveform residual .03327 | Floating all-bath residual diagnostic; quadrature/linear algebra unenclosed |
| Low-pump <1.056e-13 | First-Dyson vacuum-vector squared norm only; not an all-orders physical probability |
| Thermal counts and reset floor | Separate assumed-equilibrium Gaussian model; no coupled thermal converter solution |
| Total physical gate/readout error | Not established |
| Repeated QEC workload error or net computing advantage | Not established |

Preparation, storage/gates, local loss, leakage propagation, delivered waveform, readout, reset, and schedule still need compatible conditions in one operating point. Mathematical polar repair does not flag an erasure. The small example's qubit input is not the unrestricted source of the baseline theorem. A finite collection model is extra physical input, not implicit in the local phase density. No thermal or notch certificate is inherited from the zero-temperature baseline.

## 8. Continuity and actual review evidence

Read `HANDOFF.md`, the latest theorem, its completed internal audit, the hybrid seed scope, and relevant predecessor proofs/reviews. The copied source files remain unchanged. Their missing original six-control CZ and dispersive-parallel bytes remain missing; no historical audit was invented. The existing final-bound audit's source-version limitation is retained rather than retroactively hash-pinned.

Astra Research reported a published refresh failure. The current public fallback was acquired at commit `44b7e51f36b6dd4759a0227f23cc6b11671b1583`. N1127, N1128 and N1133-N1135 plus the governing owner review/correction are preserved. All five packet files match their returned Git blob hashes. The numerical correction to N1127's symbolic endpoint is respected. The accepted quantum-channel undecidability foundations were not reopened.

The latest reported 791-file physical-bath source ZIP was not acquired. Two targeted filename searches returned no match; that is an access/search outcome, not proof that the archive was deleted. The supplied complete proof and actual audit remain usable at their stated scope. This continuation did not recover unrelated gate history.

New actual reviews are distinguished:

- Physical contributor independently read and hash-pinned the root channel theorem; its strong-measurability clarification was applied before acceptance.
- Knowledge contributor independently reviewed and exactly replayed the interval benchmark. It matched all raw effect entries and sixteen probability interval strings. Independent high-precision scalar checks and a different oscillator implementation corroborate the proof. The source is hash-pinned.
- Solver contributor independently read the detector-kernel realization proof; no code replay is claimed by that reader.
- Root independently read the new temporal-span proof and low-pump first-Dyson proof. Root's nonunitary-source extension is separately labelled; thermal numerics were not independently interval-certified.

Corrections preserved: exact integer parity signs instead of negative-power float signs; assertion against a negative probability upper enclosure; strong measurability instead of implied norm-Bochner integrability; explicit two-vertex finite-pulse pair tails in the physical next step. No corrected result is silently substituted for its earlier scope.

## 9. Next justified attack

The representation has now been tested far enough to choose the next work: build an adaptive temporal packet space with validated compression and residual quadrature, guided by the temporal-span obstruction and the actual source exposure. Endpoint-only directions and ever-finer time steps are not a sufficient general strategy. The two-vertex virtual-source pair process provides a compact adversarial test with an exact source correlator.

Then use actual separately specified circuit kernels and collection kernels for the high-frequency notch and the low-work/passive alternative. This requires the necessary source spectrum, control and transfer data; it does not require recovery of unrelated historical gate arguments. A successful full record calculation can feed the existing parity instrument and teleportation composition, but leakage, preparation, reset and workload conditions must still be charged.

This checkpoint is a completed scientific boundary, not a promise of unattended execution. All launched research computations finished before packaging.
