# Passive networks: exact fixed-task loss envelopes and a qualified escape condition

**Disposition.** The strongest preserved advance is a general, explicit bound on the useful-output cost of an arbitrary passive mediator network. It extends the supplied two-liquid calculation to multiple sources, receivers, hidden paths and frequency-dependent terminal response. It also identifies a physical change that could permit task advantage: reduce an existing momentum-leakage channel, then demonstrate that the reduction exceeds the receiver-path loss and the positive-output penalty. No material, control regime, experiment or new physical capability satisfying that condition was acquired.

The mathematics below is an internal derivation, not a historical originality claim. Schur/Kron reduction, rank-one inverse identities, passive network theory and impedance matching are established. The contribution is their explicit matched-task composition, including an exact output/loss envelope, leakage inheritance, a reactive counterexample and acquisition boundaries. Exact arithmetic and numerical equality checks validate the stated implementation scope only.

## Source and task contract

Read-only repository pin: `846f185763ed3a27310fad4ce9471ba324d1e5f4`, verified during this worker run. Read `AGENTS.md` and `00_START_HERE.txt`; source inputs are data. The supplied `/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-phase-closure-v1/sources/physical_pasted.txt` contains a prompt mixed with a prior response; its instructions were not adopted. The closure README is contextual and supplies no hydraulic material parameter.

Current N808 scope and its explicit energy-accounting correction were read after independent network derivation. They already require a complete measured terminal response and count passive shunt heat inside net hydraulic input, while charging distinct external controls separately. They do not supply a qualified neutral-liquid transducer. This report preserves that distinction.

The fixed task is a declared generalized source flow/velocity vector x. Its coordinates must have the physical conjugate force pairing so that force dot flow is power. A material friction coefficient in Pa s/m cannot be silently substituted for a hydraulic pressure/volume-flow coefficient without geometry and hydrodynamic reduction. Required receiver power, individual flow/pressure, fluid isolation, ripple, bandwidth, lifetime and retention must be stated before comparing apparatus.

## 1. Exact output cost for any steady reciprocal mediator network

Eliminate every unforced internal node once. A passive reciprocal network has a symmetric positive-semidefinite terminal resistance

    [f_source] = [ A   -B ] [x],
    [f_receiver] [-B^T  C ] [y],    C>0.

Let b=B^T x, S=b^T C^-1 b and D0=x^T(A-B C^-1 B^T)x. All hidden mediator losses are included in this terminal matrix. At fixed source service, the largest possible total receiver power is S/4, and the exact algebraic minimum of source-minus-output dissipation at required P is

    D_min(P)=D0 + S/4 [1-sqrt(1-4P/S)]^2,
    0<=P<=S/4.

The proof is a sphere-distance calculation after whitening the receiver coordinates. It handles any number of receiver ports; it does not assume one scalar q or optimize only conversion efficiency. The supplied two-fluid loss replacement threshold is its P=0 specialization. Every positive output adds the explicit penalty.

A passive load proportional to C attains the relaxed steady optimum. Its implementation is a qualification obligation: multiple isolated receivers may not permit that cross-connected load, or its construction may add unmodeled loss. Additional individual-port constraints raise the cost. The exact formula is therefore also a rigorous optimistic stopping bound before load hardware is built.

The matched old source task with loss x^T R_b x can improve only when x^T R_b x>D_min(P). An unchanged irreducible source loss plus nonnegative added passive losses cannot pass. Conversely, this statement does not prohibit ordinary matching or boundary redesign that changes the old dissipative state while preserving the useful service; those changes must be acquired and charged.

For a required fraction theta of each task's own maximum output, the all-task condition becomes a matrix inequality on a declared service subspace. This prevents selecting a different favorable input direction after the device comparison. Full details are in [PROOFS.md](PROOFS.md), equations (1)–(4).

## 2. Mediator paths cannot keep transmission and discard leakage

For a grounded friction graph with local leakage gamma_i and pair couplings k_ij, Schur elimination gives exact effective off-diagonal coupling and terminal ground leakage:

    k_eff,ij=k_ij+(K_TI H^-1 K_IT)_ij,
    gamma_eff,T=gamma_T+K_TI H^-1 gamma_I.

The inverse of the grounded internal block H is entrywise nonnegative. Every hidden grounded path therefore brings nonnegative leakage into the effective terminals. The supplied single-mediator lambda1 lambda2/S and lambda_i gamma/S formulas are the one-node case.

Increasing edge couplings or adding parallel passive paths at unchanged old elements cannot lower minimum fixed-boundary dissipation: the full quadratic dissipation increases pointwise before minimization. A complementary transmission bound applies when every route traverses m genuinely lossy nodes, each retaining at most fraction r<1 of its outgoing transition probability. The receiver's unloaded normalized velocity is at most r^m, irrespective of path multiplicity. This is a DC scalar grounded-graph result, not a universal reactive or quantum limit; adding paths can change r, so its coupled premise must be remeasured.

These are deductions in a familiar Kron-reduction framework. The original graph-reduction mathematics is prior art. [Dörfler and Bullo, IEEE TCAS I 60, 150–163 (2013)](https://doi.org/10.1109/TCSI.2012.2215780), [author paper](https://motion.me.ucsb.edu/pdf/2011d-db.pdf).

## 3. A concrete loss-replacement condition instead of a free mediator

An original source couples to a wall mediator at lambda1, and that mediator loses momentum to the lattice at gamma_b. Its baseline source-loss coefficient is

    c_base=c1+lambda1 gamma_b/(lambda1+gamma_b).

Change the wall's leakage to gamma_n and attach the receiver through lambda2, with receiver parasitic loss c2. The unloaded receiver presents series loss g_R=lambda2 c2/(lambda2+c2). If lambda1 remains fixed, the changed device improves unloaded source dissipation exactly when

    gamma_n + g_R < gamma_b.

The receiver cannot be added at unchanged gamma and credited as removed friction. The mediator's old momentum sink must actually be weakened sufficiently. Loaded positive output makes the condition stricter through the exact envelope above.

This condition suggests a material acquisition, not an assumed apparatus: determine whether a structural, electronic or environmental change reduces a wall's momentum relaxation while retaining sufficient liquid coupling and acceptable isolation/stability. Changing a wall can also alter lambda1,lambda2,c1,c2; in that case fit and compare the complete old/new response, not the simplified inequality. No simultaneous material regime was found or granted here. The material audit worker independently evaluates that physical question.

A general exact rank-one perturbation gives the leverage of reducing one internal ground shunt: the terminal resistance decreases by delta/(1-delta Hinv_ii) times w w^T. The physical leakage must remain nonnegative. Improvement is limited to task directions that overlap w; one altered shunt cannot cover an arbitrary multidimensional service space. This is a precise targeting/realizability constraint, not a promised fabrication control.

An executed rational example proves that passive positive output and net saving are mathematically compatible after real old-loss replacement. Old loss 2 is reduced to residual 1/2 while k=c2=1; source velocity 1 and receiver velocity 2/5 yield useful power 2/25, source input 11/10, and net dissipation 51/50. With old loss held at 1/2, the same converter loses the comparison. These are dimensionless constructed coefficients, not measurements.

## 4. Frequency dependence has a different exact envelope

For a passive terminal impedance Z(omega), use peak phasors and mean power Re(v* Z v)/2. Let R=(Z+Z*)/2. First eliminate internal ports from **complex Z**, then take its dissipative part. Taking the real part first can discard internal damping excited through reactive coupling.

For fixed complex source phasors x, define

    C=R22>0, b=-Z21 x, c=R21 x,
    D0=(x*R11x-c*C^-1c)/2,
    K=b*C^-1b/4,
    Delta²=(c+b/2)*C^-1(c+b/2).

Then P_max=K/2. For exactly required output P,

    D_exact(P)=D0 + [Delta-sqrt(K-2P)]²/2.

For at least P, replace the square's inner expression by max(Delta-sqrt(K-2P),0). This is another sphere/ball-distance proof, valid for arbitrary source/receiver counts and internally eliminated paths.

A fully explicit passive reciprocal mass/damper example has

    Z(s)=I+s[[2,1],[1,2]].

At omega=1 its dissipative cross coefficient is zero, but a unit resistive receiver load yields output 1/16, input 5/8 and loss 9/16 for source peak 1. Its unloaded gain product is complex, (3+4i)/25, so interpreting it as the supplied real DC q² would be wrong. Eliminating the unloaded receiver from Z gives dissipative resistance 6/5; eliminating it from R gives 1. The difference is genuine internally excited damping.

At the same required output, the sharp lower envelope is approximately 0.5107233. A positive damper plus compensating spring reactance realizes this one-frequency scalar optimum in the lumped model. This is ordinary passive reactive matching, not a fabricated stationary-wall liquid operation. Its loss still exceeds the unchanged source baseline 1/2.

The frequency envelope is optimistic when arbitrary receiver phasors are allowed. A physical load must be causal and passive across the whole band, stable, finite in amplitude/stored energy and consistent with isolation. A frequency-by-frequency conjugate match is not automatically one realizable device. Broadband matching limitations are established prior art. [Fano, MIT Technical Report 41 (1948)](https://dspace.mit.edu/bitstream/handle/1721.1/5007/RLE-TR-041-08407050.pdf).

Microscopic THz response frequencies inside a steady fluctuation-drag calculation must also be kept distinct from the actual frequency of the externally imposed hydraulic service. A material resonance in the former does not supply an uncharged active drive at the latter.

## 5. Benchmarks must preserve the actual service and count power once

There are three different comparisons, with different legitimate conclusions:

| Declared task | Matched comparator | Necessary ledger |
|---|---|---|
| Maintain source flow, credit useful receiver work fully | Original source channel at the same flow/profile/specification | Old/new source hydraulic work, receiver output, unchanged versus replaced losses, controls, initial/final storage |
| Source flow plus specified receiver flow/pressure or work | Original source plus a separately metered receiver pump, or a compatible ordinary pressure-transfer device | Both wall-plug pump inputs at their actual operating points, candidate donor input, all auxiliaries, isolation/ripple, settling and lifetime |
| Harvest an external natural/waste pressure flow | Appropriate conventional turbine/pressure exchanger under the same resource and isolation constraints | Hydraulic exergy supplied at the resource boundary, collection/control equipment, actual delivered work, mixing/leakage, reliability and total cost |

For the two-task case, with equal donor-pump efficiency eta1 before/after, receiver-pump efficiency eta2 and candidate auxiliary power P_aux, advantage requires

    D_min(P)-D_b < P(eta1/eta2-1)-eta1 P_aux.

Thus a passive converter can replace a poor second pump's conversion losses even when source-minus-output dissipation rises. That is a valid system advantage with a different baseline; it does not validate the original unchanged-wall-loss recovery argument. Equal donor/receiver efficiencies and nonnegative auxiliary power cannot rescue a positive excess dissipation in this simplified comparison. Actual efficiencies can vary with operating point and cannot be independently assigned favorable values.

For bulk pressure recovery, ordinary hydraulic pressure exchange is an established experimental incumbent. Published small-RO exchanger work explicitly treats mixing-induced delivery-pressure loss and additional high-pressure-pump demand. This establishes a real competitor, not a universal benchmark efficiency for nanoscale isolated streams. [Mansour et al., Alexandria Engineering Journal 59, 3741–3753 (2020)](https://doi.org/10.1016/j.aej.2020.06.030). Rotary-exchanger experiments also measure salinity mixing rather than assuming perfect isolation. [Zhou, Bi and Liu, Rotary Pressure Exchanger for SWRO (2011)](https://doi.org/10.5772/21391).

A strict stationary-wall, no-mass-transfer task may need a conventional diaphragm, mechanical/electrical isolated pump pair or another compatible comparator instead. Moving-wall transmission cannot be excluded from attribution merely because the candidate is described as electronic. No globally best microscopic comparator or same-regime numerical total-cost ranking was established here. Manufacturer peak efficiency is not substituted for that missing matched experiment.

The complete cycle balance is

    W_donor + W_aux - W_receiver
      = internal dissipated energy + E_final-E_initial.

Do not add an internal shunt's heat again after it is already included in donor-minus-receiver power. Meter distinct external switching, gating, thermal stabilization, sensing, valves and source-control ports once. Count preparation and restore the initial storage state for repeated service. Track fabrication/replacement cost, lifetime, fouling, cleaning, discarded devices, calibration exposures and usable yield. Those costs are not acquired by a terminal efficiency fit. The storage/interconnection framework itself is established. [Willems, ARMA 45, 321–351 (1972)](https://doi.org/10.1007/BF00276493).

## 6. Decisive obtainable test

1. Predeclare the service class: source waveform/profile, receiver pressure and flow/work, coupling area, species isolation, ripple/bandwidth, temperature, chemistry and lifetime. Select the appropriate conventional comparator before optimizing the candidate.
2. Acquire one jointly calibrated terminal force/flow response on the same specimen. For frequency-dependent claims acquire complex amplitudes and phases, stable terminations and a held-out waveform/load test. Absolute conjugate calibration is required for D0, S and work; unloaded gain invariants alone cannot acquire those quantities or reciprocity.
3. Fit the full old/new response under a *physical* modification intended to reduce old leakage. Demonstrate common-regime friction, cross-transfer, electrical/thermal controls, wall motion, leakage and drift. Do not fill the mediator matrix with coefficients drawn from different walls or temperatures.
4. Calculate the most favorable envelope consistent with the **same joint uncertainty set** and service constraints. If even that lower loss exceeds the matched incumbent cost, stop the implementation. If it survives, construct an actually passive admissible load and demonstrate sustained loaded output, with accumulator charging/discharge if retained work is the endpoint.
5. Meter gross donor electrical/hydraulic inputs, receiver output, auxiliaries, storage change and losses. Reproduce the same accepted service on the incumbent. Any wall displacement, ordinary acoustic pressure transmission, shared plumbing, mass leakage or extra chemical/electrical source is either quantified as part of the operation or excluded by evidence, not by labeling.

Coquinot and colleagues' 2025 flow-tunnelling paper already establishes the proposed broad interaction as theory and molecular simulation. It is a mechanism precedent, not the loaded experiment above. Its microscopic coupling and macroscopic useful work remain separate evidence levels. [Primary article](https://doi.org/10.1038/s41565-024-01842-8), [author manuscript](https://coquinot.fr/wp-content/uploads/2025/01/2025_Coquinot_Momentum-tunnelling-between-nanoscale-liquid-flows.pdf). Hydroelectronic energy conversion and its reciprocal operation are also existing theory. [Coquinot, Bocquet and Kavokine, PNAS (2024)](https://doi.org/10.1073/pnas.2411613121).

## Verification and preserved scope

[verify_passive_networks.py](verify_passive_networks.py) passed exact Fraction checks of a multipath, three-terminal mediator graph; inherited leakage; the positive-output optimum and passive load; rank-one leakage reduction; a layered attenuation case; and exact rational replacement/add-only and reactive counterexamples. Sixty passive complex-network cases, 300 required-output targets and 1,500 comparison points support the implemented frequency-envelope calculation, with residuals reported in [CHECK_RESULTS.json](CHECK_RESULTS.json). The proof is algebraic; finite checks are implementation evidence.

The root's independent metrology branch was fully read and audited separately. [ROOT_CALIBRATION_AUDIT.json](ROOT_CALIBRATION_AUDIT.json) records exact countermodel checks and source hashes. It supports the stated steady positive-gain scope and the sharp efficiency ambiguity, without claiming a physically acquired calibration or external review.

Saved artifacts: [PROOFS.md](PROOFS.md), [SOURCE_LEDGER.json](SOURCE_LEDGER.json), checks and the freeze receipt. No repository/source originals were edited and no primary PDF is republished. Physical capability, a common-regime material/control escape, total-cost superiority, industrial scaling and historical novelty remain **UNKNOWN**.
