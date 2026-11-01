# Independent noncommuting construction and bath-access barrier

Derived from the target and factual obstruction before seeing the parent's preferred hypotheses. All statements below are direct finite-dimensional calculations, not claims of a general noncommuting Gibbs loader.

## 1. An exact positive terminal-noise inversion mechanism

Take N disjoint memory–bath qubit dimers with actual storage Hamiltonian

H = sum_j (h X_{M_j} + J Z_{M_j} Z_{B_j}),  hJ != 0.

Terms within a dimer do not commute. Set r=sqrt(h²+J²), t=tanh(beta r). The full actual joint Gibbs state is a tensor product of

rho_j = [I - (t/r)(h X_M + J Z_M Z_B)]/4.

Let the actual final memory noise be the calibrated independent depolarizing channel D_lambda, with D_lambda(P)=lambda P for nonidentity Pauli P. The exact preimage is

sigma_j = [I - (t/(lambda r))(h X_M + J Z_M Z_B)]/4.

It is positive iff t <= lambda. Consequently D_lambda^{tensor N}(sigma_1 tensor ... tensor sigma_N)=rho exactly: no extensive residual error, despite noncommuting memory–bath interactions. The preparation state is a colder Gibbs state of the SAME dimer Hamiltonian, with beta' = arctanh(t/lambda)/r when t<lambda. This is a resource requirement, not permission to retune a physical thermalizer for free.

If both qubits have known terminal depolarizing shrink factors lambda_M,lambda_B, the preimage becomes

sigma_j=[I-(t/r)((h/lambda_M)X_M +(J/(lambda_M lambda_B))Z_M Z_B)]/4,

and exists iff (t/r)^2[(h/lambda_M)^2+(J/(lambda_M lambda_B))^2] <= 1. The two inverse-scaled Paulis anticommute, so this condition is exact. Below this positivity threshold no input state can work: the invertible channel has this unique, nonpositive preimage. This is a channel-range obstruction, not a gate-complexity issue.

### Operational accounting

One valid implementation is calibrated two-qubit mixed-state synthesis: diagonalize each sigma_j, prepare a purification with fresh ancillas, apply the required local unitary, discard/reset purifying ancillas, and then allow the specified terminal channel. This requires actual bath-qubit control, suitable neighboring scratch qubits, calibrated h,J,beta,lambda, and entropy disposal/reset access. Alternatively one must explicitly supply a colder reservoir and equilibration guarantee. Merely possessing the actual H and memory controls is not sufficient. Generic unknown terminal channels or generic cross-dimer interactions are not covered.

For total trace-distance tolerance eta, per-dimer implementation errors <=eta/N suffice by telescoping. Fixed nonzero local calibration errors generally become globally distinguishable as N grows; an N-independent calibration promise cannot justify vanishing global error. With a known smooth product family, fidelity can improve the sufficient scaling to order eta/sqrt(N), but this must be established for that family, not presumed.

### Relation to reference-entangled logical storage

The calculation establishes a genuinely noncommuting *joint thermal sector loader*, not logical protection. It can be combined with an exact noiseless logical subsystem only if the ACTUAL Hamiltonian acts as I_L tensor H_GB (with the specified physical locality), and the specified terminal loading map preserves or correctly restores the reference-entangled logical subsystem. Then the thermal-sector construction leaves logical-reference entanglement unchanged, and storage is infinite rather than stretched exponential. A commuting-code thermal loader can be tensor-composed with this dimer sector if the physical architecture truly factorizes. That is an informative restricted regime, NOT a solution for generic interactions between code spins and bath. Embedding noncommuting dimers into an exactly protected gauge subsystem while maintaining physical locality and compensating generic physical output noise is a separate obligation.

## 2. A rigorous obstruction even with actual-H evolution and arbitrary memory control

Take instead independent dimers

H_j=h X_M+g Z_M+J Z_M Z_B,

with nonzero h,g,J. Allow arbitrary memory-only control channels, including measurements, resets, feedback, and evolution under the actual H. No operation acts on bath qubits directly. Every allowed operation preserves the classical distribution of the joint bath Z string, because [H,Z_{B_j}]=0 and memory operations are trace preserving. This remains true for adaptive protocols when all outcomes are included; postselection is not deterministic preparation and its success cost must be counted.

Initially let bath Z strings be uniformly distributed. In the ACTUAL full Gibbs target the independent bath bias is

q = [cosh(beta r_+) - cosh(beta r_-)]/[cosh(beta r_+) + cosh(beta r_-)],
r_+ = sqrt(h²+(g+J)²), r_- = sqrt(h²+(g-J)²).

At high temperature q=beta² gJ + higher orders. It is nonzero even for arbitrarily weak J. A bath-Z measurement distinguishes the unbiased initial distribution from the target biased product distribution. For q>0, thresholding sum_j Z_{B_j} at Nq/2 gives, by Hoeffding,

D(prepared joint state, target joint state) >= 1 - 2 exp(-N q²/8),

where D=(1/2)||rho-sigma||_1; the same bound uses |q| for q<0. Thus global error approaches one. This holds irrespective of memory circuit fault tolerance or preparation duration. Adding a reference-entangled logical spectator does not change the bound. The example is a nonergodic bounded-spin bath; an assumption of controllability/ergodicity or a supplied correct bath population distribution is precisely what excludes it.

The broader invariant-observable principle is: whenever permitted preparation controls preserve a bath observable's probability distribution, target preparation error is at least the classical total-variation mismatch in that distribution. If no permitted process changes the bath marginal at all, its trace-distance mismatch itself lower-bounds preparation error. Do not use the latter claim when actual M–B dynamics can change the marginal.

## 3. Unknown couplings: a conditional identifiability barrier

For the first dimer model, targets at coupling +J and -J have squared Uhlmann fidelity F=1-(J²/r²)t². For N dimers their root fidelity is [1-(J²/r²)t²]^(N/2). Hence their trace distance is at least one minus that expression. A preparation map that has no access to sign information and no usable coupling-dependent dynamics must incur worst-case error at least half that lower bound. Unknown couplings ALONE are not an impossibility theorem: actual-H equilibration can imprint the correct state without learning their classical descriptions. The condition excluding such a physical oracle is essential.

## 4. Fair active-FT comparison

The inaccessible conserved-bath example blocks full-joint target loading but does NOT block preservation of logical information by active FT. The unknown Z_B variables produce bounded local conditional fields J Z_M. With the same memory-only controls, resets, fresh ancillas, and bounded-duration gates, sufficiently weak J times a gate duration can fall within an appropriate local coherent-noise FT model; bath access is unnecessary for logical preservation. Known memory fields can be accounted for in controls. A specific threshold/resource claim still needs an explicit code, geometry, gate model, and schedule.

Conversely, the exact positive dimer loader requires bath control or a colder equilibration resource that ordinary memory-only FT does not have. A fair comparison must grant that same resource to active FT, and include the calibrated inverse-state synthesis and scratch/reset cost. No generic overhead superiority follows from the construction.

## Bottom line

Noncommutation itself does not forbid exact terminal-noise compensation: the anticommuting dimer calculation is a constructive counterexample. But full actual-joint loading requires BOTH channel-range positivity and physical access sufficient to establish the target bath populations/correlations. Neither is a consequence of logical fault tolerance, weak couplings, or locality. A general proposed theorem must separately prove these two conditions, quantify calibration accuracy versus system size, and establish the protected logical dynamics of the actual interacting Hamiltonian.

## 5. Reconciliation after reading the parent polymer-positivity mechanism

The parent's operator-polymer result, if its activity identification is proved, can establish positivity of the inverse-noise state while Section 2 still forbids its physical preparation. These are orthogonal obligations: a positive density operator need not belong to the reachable set of an actual control system.

A consequential next operation is an **indirect controllability audit**, not further extension of positivity alone. For one memory–bath dimer with full memory-qubit controls and calibrated drift J Z_M Z_B+b_x X_B+b_z Z_B, all J,b_x,b_z nonzero, the generated Lie algebra is su(4). Memory conjugation separates the bath drift and ZZ interaction; commutators of ZZ with the bath drift generate Z_M Y_B; commuting this with ZZ generates I_M X_B; subtraction from the original bath drift gives I_M Z_B. Full bath rotations and an entangling interaction follow. Thus direct bath drive is unnecessary in this restricted model. Operational synthesis still costs inverse weak interaction time, control amplitude/bandwidth, calibration, and accuracy. If b_z=0 the straightforward algebra is only ten-dimensional; do not assert full controllability from a transverse field alone.

## 6. Stronger operational opening after the parent proposes a reachable stationary ensemble

This section explicitly changes the target, rather than claiming to attain the canonical Gibbs state of Section 2.

If H=direct_sum_b H_b and bath sector probabilities p_b cannot change, the state

rho_reachable = sum_b p_b Gibbs_beta(H_b) tensor |b><b|

is stationary. Canonical weights are not necessary for stationarity or, potentially, a uniform-in-b memory argument. Whether the logical lifetime proof holds requires its own conditional estimates and logical-overwrite compatibility. Arbitrary conserved-sector weights are not canonical Gibbs weights.

The Section 2 dimers furnish an exact constructive sector-information interface:

1. Assume initially classical bath Z sectors, possibly arbitrarily correlated across dimers, and a supplied logical input independent of bath. Use an expendable memory probe initialized to |+>. Isolate/refocus the calibrated ZZ interaction; evolution for time pi/(4|J|) maps b=+/- to orthogonal +/-Y probe states. A Y measurement QND-reads the bath sector without changing its weight. Known memory terms require cancellation or a calibrated compiled interrogation sequence, with finite-bandwidth errors charged. If the actual memory spin holds logical data, a safe scratch/move/encoded-probe mechanism must be supplied; the protocol does not permit erasing it.
2. Conditional on b, let r_b=sqrt(h²+(g+Jb)²), t_b=tanh(beta r_b). Prepare the memory qubit in
   sigma_b=[I-(t_b/(lambda r_b))(hX+(g+Jb)Z)]/2.
3. This is positive when max_b t_b<=lambda. A known final memory depolarizer produces exactly Gibbs_beta(hX+(g+Jb)Z).
4. Performing these local operations retains the entire possibly correlated classical distribution p_b. The output is the full stationary reachable ensemble, including its memory–bath correlations, not a memory-only Gibbs approximation.

Required resources: calibrated J including sign, time O(1/|J|), memory-side coherent controls sufficient to isolate the interaction, measurement and entropy export, probe capacity compatible with preserving the supplied logical input, classical feed-forward, and preparation/readout accuracy adequate for global tolerance. Per-site error eta/N is a conservative sufficient budget. Unknown J can be estimated by memory-probe spectroscopy but sample/time/calibration costs must be charged; unknown nonclassical bath dynamics is not solved. Measuring initially coherent bath sectors dephases them, so a revised task must authorize/require that ensemble rather than claim preservation of unknown bath coherence.

This explicit conditional loader is the strongest immediate constructive opening I can establish: it supplies a real sector-readout-and-loading operation in a noncommuting model. Extending it to an interacting encoded code requires both an efficient conditional sampler and a logical-input-safe sector interface, which are not provided by the dimer calculation or by positivity.

## 7. Protected-code extension attempt and its decisive limits

An apparently stronger exactly solvable example is H=H_code(S)+sum_a[h_a X_{B_a}+J_a S_a Z_{B_a}]. Conditional bath partition functions do not depend on syndrome signs, so the known commuting-code syndrome loader remains applicable. A bath-side conditional thermalizer can then establish full correlations without changing syndromes. However this is a benign-coupling limiting example: all stabilizers, and the corresponding decoded logical observables, commute with the full Hamiltonian. Idle logical protection is therefore automatic on the whole Hilbert space. This does not earn protection against genuinely dangerous check-violating couplings such as X_j tensor B_j.

There is also a terminal-noise ordering issue: a bath thermalization stage *after* code terminal noise is additional controlled entropy export. It is valid only under an explicitly asymmetric noise model where this stage introduces no new code errors. If the stipulated generic physical-code error layer always comes last, pre-noise syndrome-conditioned bath preparation again leaves incorrect correlations. No free repositioning of the terminal layer is allowed.

Generic quantum belief propagation does not currently supply a constructive closure in this analysis. A global nonunitary transport filter has a condition-number/success-cost bound exponential in beta||V||, which is extensive for fixed local perturbation strength. Sequential local filters need a proved failure-repair or recycling operation that preserves prior thermal correlations and the supplied reference-entangled logical input. Ordinary FT recovery can change the desired noncommuting thermal state, so it cannot simply be inserted as that operation. An efficient Gibbs transport or phase channel with calibrated physical implementation, charged bath access and entropy export, and a proved logical-overwrite intertwining estimate would be a substantial additional assumption/result—not a consequence of the polymer positivity argument.

Final independent status: exact noncommuting dimer inverse-state preparation and an exact inaccessible-bath barrier are established; a restricted reachable-sector loader is explicit; the genuinely check-violating protected-code full-joint loader remains unearned. No end-to-end stretched-exponential passive-memory advantage is claimed.
