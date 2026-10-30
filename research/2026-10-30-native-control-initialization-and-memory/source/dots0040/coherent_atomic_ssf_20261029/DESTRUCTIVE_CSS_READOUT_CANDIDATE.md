# Controlled destructive CSS readout without quantum storage during classical decoding

2026-10-29. Constructive conditional readout architecture, not yet independently audited. This adds a controlled terminal measurement mode to the driven memory; it is NOT autonomous quantum-output retrieval and does not cover continuous coherent-Hamiltonian noise.

## 1. Readout mode and its actual added assumptions

At a specified memory observation time, use an explicitly controlled bounded-duration transition to a readout mode in which the unwanted native DATA-affecting evolution is disabled in the nominal model. Then implement the inverse forest frame F^dagger as a fixed-depth bounded-range qudit circuit, followed by a parallel CNOT copy of each DATA Z value into a fresh local pointer qubit initialized in |0>, and terminal Z observation of those pointers. DATA is then discarded. This implements simultaneous destructive DATA Z measurement. Logical X-basis readout is the analogous exchange of X and Z.

The nominal switching and gate schedule must actually be specified. A dissipative native generator cannot simply be inverted by declaring a frame change. If the hardware cannot suppress the native DATA-affecting drive, or if the switching process has uncontrolled coherent errors not in the stated model, this operational proposal is not certified.

Assume the controlled stage has duration τ_ro bounded independently of N, a bounded-depth local unitary/dilation description, and the same bounded-rate fixed-range exogenous CPTP kick model throughout. Local measurement/write faults must be represented in that declared bounded-depth readout instrument, e.g. by local noise on the measurement ancilla/premeasurement circuit before ideal pointer observation. Ideal projective observations are the terminal mathematical primitive; arbitrary unmodeled detector failures are not silently included.

The final forest inverse is identity only at initialization, not at arbitrary readout time. It acts on actual controllers/workspaces as well as DATA and must be implemented, including on malformed controller sectors. Its finite support and depth come from the full-Hilbert gauge, not from assuming all controllers retired.

After destructive measurement, DATA no longer needs to remain coherent during decoding. Store the N classical outcomes in a reliable classical subsystem and perform the specified classical algorithm offline. Rather than assuming unpriced perfect classical hardware, denote by p_cl a certified uniform probability that record storage/computation/output processing fails. A classical fault-tolerant implementation or an explicit trusted classical-processing assumption must supply this number. Its cost is not included in the quantum-memory theorem.

## 2. Exact decoding rule from a single product-basis measurement

Let x in {0,1}^N be the measured Z-basis string. Compute the Z-check syndrome

    s_Z=H_Z x.

Run the deterministic X-error SSF algorithm on this classical syndrome, updating it after each accepted X correction, and accumulate the correction mask c_X(s_Z). A full scan making no change terminates the algorithm. At most n_Z+1 scans are needed, where n_Z is the number of Z checks, because each accepted X correction lowers their integer syndrome weight.

For a fixed basis of logical Z operators with binary masks forming L_Z, output

    z_logical=L_Z [x XOR c_X(H_Z x)].                   (1)

A nonzero final syndrome can be flagged as decoding failure. On all certified safe histories it never occurs.

This is an exact quantum-measurement equivalence, not a Pauli-mixture argument. Applying an X correction before a product Z measurement merely flips the corresponding measured bits. Z corrections do not affect the measured Z values. Moreover the final logical observable in (1) is a function only of Z-check syndromes and logical Z parities, all of which commute with X stabilizer measurements. Thus inserting or deleting the unused X-syndrome measurement and Z-sector SSF processing does not change this logical classical-output POVM. One may analyze the full ideal terminal SSF decoder and then logical-Z measurement, while implementing only the measured bit string and its relevant-sector classical correction.

The equality holds on arbitrary joint DATA/reference/bath states as a classical-output channel after unobserved quantum registers are traced. Same-syndrome coherent faults are not twirled or assigned probabilities.

## 3. Concrete pointer-fault semantics and a bounded-support noise-only suffix

Use the specified nominal readout unitary U_copy F^dagger, where U_copy is the parallel local CNOT copying DATA Z into fresh |0> pointers. Defer the ideal pointer observations until the end. Any local measurement/write error before that observation is modeled as an actual local CPTP kick on DATA, pointers, controllers and bath. Arbitrary unmodeled pointer-detection errors are excluded; subsequent classical record errors are charged through p_cl.

Push frame-stage faults forward through the remaining nominal F^dagger circuit, and copy-stage faults backward through the preceding copy circuit. The resulting channel is the ideal F^dagger, followed by an ordered sequence of conjugated local CPTP kick channels, followed by ideal U_copy and pointer observation. Conjugation preserves CPTP and enlarges support only by a constant-depth light cone. Common bath action is retained. This manipulation does not invert a measurement or a dissipative native evolution.

Now expand each local joint DATA/pointer Kraus operator in Paulis on those two finite-dimensional local factors, leaving arbitrary controller/bath coefficients. Before U_copy, the accumulated pointer Pauli sends the fresh pointer state to a computational basis string a, up to phase. The measured pointer string is the DATA Z string XOR a. Therefore the pointer-X component acts as an additional observed-bit X mask on the associated DATA coordinates; pointer-Z phases and DATA-Z components can be retained in the coefficient/output-environment factors. Each insertion contributes a bounded effective observed-bit mask, and its mapped support lies in the same constant-radius light cone. No probability is assigned to these Pauli terms.

There is NO SSF feedback during this quantum readout suffix. Hence these effective observed-bit masks can be accumulated as Pauli bad events and fed into the virtual classical SSF correction of the final measurement string. One must not claim that an arbitrary pointer fault is literally a DATA-only channel preserving the entire logical quantum state: the conclusion here is a classical-measurement-compatible Pauli history, which is sufficient.

Enlarge G to include every effective readout support clique, mapping each pointer position to its associated DATA site. The degree remains bounded. If s_ro bounds the effective support and ν_ro bounds incidence of primitive readout locations touching W, then

    Q_ro(W)<=s_ro N_ro(W),
    N_ro(W) is dominated by Poisson(ε ν_ro τ_ro |W|).

The coefficientwise expansion does not require a factor exponential in all faults. On a safe physical location record, the deterministic certificate corrects EVERY effective Pauli mask branch simultaneously.

### Measurement-compatible span and the final norm step

Let x be a fine pointer result and let f(x) be the fixed classical output rule (1). For each safe Pauli-expanded branch, its Kraus restriction annihilates every logical Z-basis state except |f(x)>: correctness of that branch means an encoded logical basis input z can give x only when z=f(x). Thus

    K_x Enc = B_x <f(x)|_L

with an output/controller/bath operator B_x, and the same form survives coherent summation over safe branches. After tracing the fixed initial ancillary state and grouping x by z, the safe classical-output map has effects a_z |z><z|, with 0<=a_z<=1. It need not be a scalar times the entire ideal measurement.

If the bad-record CP instrument has uniform diamond norm δ, trace preservation gives 0<=I-sum_z a_z|z><z|<=δI. The difference between the ideal measurement and the safe map is itself CP of norm at most δ. Adding the bad map proves classical-output channel distance at most 2δ, including any entangled reference. This establishes the needed norm conversion without falsely claiming full quantum-state recovery after pointer faults.

## 4. One D0-only root block avoids a false service assumption

Combine the finite noisy readout stage and the ENTIRE subsequent ideal classical SSF computation into one final analysis suffix. D0 is an unconditional finite-work bound, independent of how many noiseless SSF scans are performed. Its root component satisfies

    |K|<=C_seed [|R_in intersect K|+Q_ro(K)].            (2)

Apply the root argument to the relevant X sector for Z readout (or Z sector for X readout), using the effective observed-bit masks above. If all enlarged components in this suffix are smaller than ℓ, the final no-change scan must have zero relevant syndrome by the good-component progress theorem. The remaining effective bit-flip error is a stabilizer in that sector, and the logical measurement is correct. Using the two-sector union bound below is conservative; it is not an assertion that pointer faults preserve the entire logical quantum state. Thus a measurement-decoding failure implies a cutoff-bad connected component in this suffix or in an earlier memory block.

Do NOT apply D1 to the noise-only quantum readout interval: it has no SSF service and would have an order-one missed-opportunity parameter. Instead root at the whole suffix using (2). If Q_ro is not already dense, take the target in R_in and continue the established backward chain only through earlier genuine memory blocks. If Q_ro is dense, it is the terminal fresh event and has a direct Poisson tail. This is why no quantum storage is charged during the offline polynomial-time algorithm and no fictitious good-service window is inserted.

For example put a_root=1/(2C_seed), α_ro=a_root/s_ro and u_ro=ε ν_ro τ_ro. For u_ro<α_ro,

    P[Q_ro(W)>=a_root |W|]
      <= r_ro^|W|,
    r_ro=(e u_ro/α_ro)^α_ro.                           (3)

Let r_mem be the per-terminal-set base r0 in the audited transactional memory corollary, and replace it by max(r_mem,r_ro) in the spacetime-animal calculation. All later constants K_vol,A_st and the two-sector union proceed as before. Writing

    r=A_st max(r_mem,r_ro)^(1/K_vol)<1,

one obtains the conservative classical-output channel bound, for L completed memory blocks plus the controlled readout suffix,

    ||M_actual - M_ideal_logical-Z||_diamond
      <=2 min{1,2(L+1)R N r^ℓ/(1-r)} + 2p_cl,          (4)

capped by two if desired. The X-basis version is identical. The displayed factor uses the already available conservative two-sector memory union; the readout suffix itself needs only the relevant measurement sector. A measurement-specific one-sector bound could improve constants but is not needed.

This is a comparison of the full logical classical-output channel, including an arbitrary entangled reference, not only a marginal bit-error rate. A full noisy terminal instrument and the common-span proof are needed for that interpretation.

## 5. Operation and resource accounting

* Mode switching: one explicitly controlled stage of bounded duration; nominal suppression of incompatible native dynamics and its noise model are additional hardware assumptions.
* Forest inverse: O(N) bounded-support qudit gates in constant graph-local depth, assuming the reviewed bounded-degree full-Hilbert frame construction. Actual gate durations contribute to τ_ro.
* Destructive observation: N single-qubit measurements in one parallel basis-measurement stage (with the declared finite-depth local measurement implementation).
* Raw classical storage: N outcome bits, plus O(N) syndrome/correction workspace; reliability is quantified by p_cl rather than assumed from quantum storage.
* Offline relevant-sector SSF: at most n_Z+1 complete hub scans, O(N n_Z)=O(N^2) elementary bounded-degree classical work in a naive implementation. Stabilizer parities initially cost O(N) at bounded check weight. Computing k logical parities costs O(kN), at most O(N^2), for an explicitly provided logical-operator basis.
* Classical decoder latency does not demand quantum DATA storage after destructive measurement. It still demands reliable classical storage and computation and does not prove low-latency classical processing.

The locality is the declared bounded-degree interaction graph. Embedding it into fixed-dimensional geometric hardware and routing readout controls are separate charged resources. A precomputed logical-operator basis has polynomial description/preprocessing cost; it is not a minimum-weight decoding oracle.

## 6. Exact remaining gap

This adds a plausible controlled destructive logical-Z/X measurement mode under explicit finite-depth switching/readout semantics and the same Poisson-CPTP noise class. It does not provide general quantum state retrieval, arbitrary logical measurement bases, a noise-free freeze of live data, a continuously autonomous readout mode, or an implementation of reliable classical processing. Nor does it extend the memory proof to generic continuous coherent Hamiltonian perturbations.

The appended-noiseless-SSF mathematical decoder and the readout-dilation fault propagation should receive independent audit before (4) is treated as established. The frozen transactional memory corollary is not altered by this candidate.
