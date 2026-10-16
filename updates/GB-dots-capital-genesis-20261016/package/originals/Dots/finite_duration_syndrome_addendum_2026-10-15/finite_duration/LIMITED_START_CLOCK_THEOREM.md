# Fixed-duration correction gadgets: a limited start-clock bridge

Status: reconstructed deterministic/probability interface, 2026-10-15. Conditional on the previously reconstructed memory proof and its named imports. Not a time-independent physical Lindbladian, noisy-clock theorem, hardware threshold, or novelty claim.

## Verdict

There is a sound reduction for fixed-duration, finitely many local gate gadgets, with clean-interval serializability as specified below. It uses the original independent START clocks, skipped-correction support births, individual bad gates, and finite-window block flags. It neither contracts an overlap component into one bounded fault nor asserts Poisson completion clocks after conflict selection. It never factors an arbitrary bad channel after the noninvertible completed correction.

A separate readout boundary contribution of order kappa*tau per guarded location is needed for arbitrary-time readout. Internal slab boundary strips can be avoided by global start-time serialization; a more conservative proof can charge them too. No claims are made about the actual intermediate states of clean gadgets being Pauli orbits.

## 1. Exact hypotheses and scope

At each correction location i (both CSS sectors included), independent exogenous Poisson starts have rate kappa. Every start s reserves a fixed finite patch P_i of data and local ancillas over [s,s+tau]. Each attempt has at most g gates, all supported inside P_i; aborting/skipping some or all gates is allowed only on a declared bad attempt. Gates, resets, and the controller's causal operations must obey this support statement. Conflict means overlapping time intervals at locations with intersecting reserved resources. Include i itself among its conflict neighbors; their number is at most D, uniformly in L.

Every actually clean attempt MUST receive fresh reset local ancillas, with previous correlations removed before its correction circuit begins. A guarantee only for a hypothetical fresh-ancilla input does not suffice. A clean completed attempt implements EXACTLY the completed correction C_i on its data, for arbitrary input entangled with exterior systems. Its private degrees of freedom can be discarded/reset. Crucially, operations outside its reserved resources during its interval commute with its gates: there are no unmodeled shared controllers, interacting baths, or records carrying dependencies into its execution. A product local circuit suffices. Merely knowing the reduced isolated map equals C_i, without this serializability condition, is not enough for the argument.

Optional external noise is independent Poisson local Pauli noise. Mark a gadget dirty if such an event touches its data or ancillas during execution. Ideal clean gates between noise events are required; continuous uncontrolled interactions are outside the model. Noise on ancillas is charged as a local primitive event as well. Let nu bound the aggregate noise-event rate per elementary counted noise location, and count every relevant data/ancilla noise location.

For horizon T, an attempt is bad if it conflicts with any attempt, is dirty, or has s<=T<s+tau. A bad gadget may execute arbitrary patch-local CPTP gates. Initial time has reset ancillas and no in-flight attempts. Existing in-flight attempts instead require an explicit startup strip charge and clean initialization; arbitrary unknown initialized ancilla corruption is not covered for free.

All start times and noise locations are exogenous. A physical protocol cannot use future starts to choose its actions; declaring bad retrospectively is only an analysis classification. An abort policy may use causal conflict detections. An isolated gadget that aborts for an uncharged unrelated reason violates the premise.

## 2. Deterministic gate-level serialization

Fix a finite start/noise schedule through T, including enough future clocks to determine overlaps if convenient. There are almost surely finitely many operations. Leave every bad gate at its original time. For each clean completed gadget, commute its gates past all intervening operations onto its original start, preserve its internal order, and replace its resulting channel by C_i. This is legal because any other gadget sharing its reserved resources during the interval would make it bad, and any touching noise event would make it dirty. Disjoint gates commute as channels on arbitrary entangled inputs. Two clean gadgets on intersecting patches have disjoint intervals and retain their original relative order. Thus this is an exact equality of endpoint channels, not an approximation in tau.

Pending gadgets at T are NOT completed fictitiously. Their executed prefix is retained as bad local gates, with unmeasured/reset ancillary outputs traced or retained as an auxiliary system. Skipped attempts remain reference starts at which no actual C_i occurs.

Expand each Kraus operator of each retained bad gate in data Paulis, with coefficients on its ancillary/auxiliary systems. Each term has data support within that gate's patch. Keep these events individually and in order. A long connected chain of conflicts can have unbounded union support; no step replaces it by a bounded-support channel. The same expansion works with ancillas retained between bad gates, provided all interactions with data remain in the stated individual patches and clean-gadget serializability holds.

After expansion, each operator term is a Pauli history with exact completed corrections at clean starts, arbitrary patch Paulis at bad-gate times, and omitted corrections at bad starts. Completed-correction projectors are scalar or zero on every definite-syndrome Pauli orbit. This is the existing universal Pauli-span transfer, not a physical random Pauli mixture.

## 3. Skipped corrections: the missing deterministic lemma

Let F_i be the original monotone old-state support-envelope update at start i. Let S_i include EVERY vertex whose envelope coordinate F_i can change, in both affected sectors as needed. Define sat_S eta to set S to one. Then, pointwise for every eta,

    sat_(S_i)(F_i(eta)) >= eta.

Indeed outside S_i the update is the identity, and inside S_i saturation dominates every binary value. Therefore at every BAD start the reference envelope may still perform F_i, immediately followed by saturation of S_i, although the actual history performs no correction. Its syndrome support remains contained. At each retained bad gate, saturate the syndrome corners of the whole allowed data patch. At a clean start apply the ordinary F_i. External Pauli events have their usual births.

This is a monotone envelope driven by ALL original independent starts, plus extra bounded births. The fake correction is only an envelope update, never an inserted quantum C_i. In particular no inverse of C_i or channel identity F_bad=E_after*C_i is asserted.

Actual homology changes only at actual good corrections, actual Pauli-expanded gate events, and physical noise. The old local-event homology argument applies to those actual events using their bounded patches. Virtual skipped-start envelope events do not change the physical error chain. Enlarge the required minimum L and constant patch neighborhoods accordingly.

## 4. Literal finite-window flags and their bounds

Keep the original slow-certificate and fast dependency-word flags, at the ORIGINAL start rate kappa. Set Delta=Cb/kappa. Fix the enlarged spatial guard needed for the previous all-input forcing proof and the enlarged birth supports above. Let N be an upper bound on the number of gadget locations whose skipped-start or any gate-birth patch can meet that guard. Let F count all elementary noise locations in the union of their patches and the direct guarded noise region. These are fixed O(guard volume) constants after b and geometry are chosen; include both sectors and all ancillas.

For slab [a,a+Delta], any bad-gadget birth in the guard comes from a start s in [a-tau,a+Delta]. Flag the slab if any such candidate start has a conflict partner with |s-s'|<tau; or if any relevant noise event lies in [a-tau,a+Delta+tau]; or if a start at one of these local candidate locations lies in the INTERSECTION [a-tau,a+Delta] intersect [T-tau,T] and is pending at T. The terminal event is empty for slabs whose candidate windows miss [T-tau,T]; an unrestricted global terminal event must not be reused in every slab. These flags may overcount harmless events.

Campbell's factorial moment formula, including distinct points of the SAME Poisson stream, gives the conservative overlap bound

    Pr(overlap flag) <= 2 D N kappa^2 tau (Delta+2tau).

No independence between the two starts of a pair, between selected attempts, or between neighboring flags is assumed. The ordered-pair count overcounts each pair and is an upper bound.

The guarded external-noise bound is

    Pr(noise flag) <= F nu (Delta+2tau).

This includes dirty-gadget effects; every relevant dirty start has its touching noise event in that interval and enlarged spatial guard. Thus no extra unproved noise-through-gadget factorization is needed.

For a readout boundary flag,

    Pr(pending-at-T flag) <= N kappa tau.

Only slabs intersecting the execution intervals of pending gadgets require this term, but taking it in every marginal is safe. Startup is free for clocks started at zero with no in-flight work. With stationary pre-zero starts and valid local initialization, a second strip of width tau costs at most another N kappa tau; one must define how their executed prefixes are initialized and charged.

Define delta_ideal to contain ONLY the original slow-certificate and fast-word terms, without its physical-noise birth term. Physical noise is counted in F nu below. Combining these terms,

    delta <= delta_ideal
             + 2DN kappa^2 tau (Delta+2tau)
             + F nu (Delta+2tau)
             + N kappa tau.

If one instead demands no gadgets cross deterministic slab boundaries, add at most two boundary strips, 2N kappa tau per slab. This simpler but worse route is not necessary for the global serialization argument.

Fix a coarse spatial packet radius q and the full spacetime dependency-degree bound BEFORE choosing b. A bounded fine patch has a uniformly bounded coarse enlargement for all b>=4; N and F can grow with the subsequently fixed b. One conservative full dependency degree for temporal offsets at most four is 9(4q+1)^4-1, with any sector factor included if represented separately. This is distinct from gadget conflict degree D.

All flags depend only on fixed spatial neighborhoods and clock windows contained in [a-2tau,a+Delta+tau], along with the stated noise window. For tau<=Delta the full spacetime dependency degree is uniformly bounded. Independent slabs are neither true nor required. Use the existing bounded-degree spacetime domination lemma, not a slabwise independence coupling. Spatial torus replay copies these full enlarged spacetime packets, including clocks crossing the copied slab boundaries. Enlarging the fixed neighborhood preserves the prospective-anchor method; the ancestor witness and its required primitive windows must both be included before copying. Copy each primitive stream once over the union of all witness windows, through their maximum right endpoint (possibly beyond the anchor layer endpoint), rather than independently resampling overlapping windows. For flags through transition n-1, [0,nDelta+tau] is a safe temporal range. The deterministic readout parameter T is identical in the original and copied flags.

The same enlarged-birth uniform-forcing argument applies: when a block has no extra flag, there are no bad-start saturations or bad-gate births in its guard. Outside births are handled by the original structural clock-chain exclusion, with the finite spatial patch margin increased. Saturations only create support; they introduce no additional propagation event that can cross a guard without either a guarded birth or a reference-clock chain.

## 5. Conditional memory conclusion

Choose fixed geometry, forcing constants, full spacetime dependency degree, and b so that delta_ideal is below the imported small-death budget. Then choose kappa*tau and nu/kappa sufficiently small for the displayed extra terms. For all sufficiently large compatible L and every T, the original common-decoder proof, applied to the serialized endpoint channel and its skipped-correction histories, gives

    || Dec_L Gamma_T Enc_L - Id ||_diamond
       <= min(2, A L^4 (1+kappa*T) exp(-cL)).

Here Gamma_T is the actual finite-duration gadget channel with local ancillary outputs discarded. An arbitrary untouched reference is allowed. The gate expansion requires the same universal correctability for every supported Pauli history, not an assumption about a typical Pauli path. The clean exact instruments and arbitrary local bad Kraus operators are covered by the existing Pauli-span quantum interface, with omission handled by Section 3 rather than the post-error-only theorem.

The bound concerns each arbitrary-time endpoint after ideal recovery. It does not prove that the raw memory remains in a Pauli orbit throughout a clean execution, or a simultaneous classical decoded-homology trajectory for all physical intermediate coherent states. Each T may have its own terminal bad-prefix classification; the decoder itself remains fixed.

## 6. Coupled physical rate-duration budget

Let x=kappa*tau<=1. Substituting Delta=Cb/kappa in the established bound yields

    delta-delta_ideal <= F(nu/kappa)(Cb+2x)
                        + N x [2D(Cb+2x)+1]
                     <= A0 nu/kappa + B0 kappa*tau,

where the explicit conservative constants are

    A0=F(Cb+2),   B0=N[2D(Cb+2)+1].

For data-only X/Y/Z noise in the original theorem, take nu=lambda_X+lambda_Y+lambda_Z. If sigma=max(lambda_X+lambda_Y,lambda_Z+lambda_Y), then nu<=2sigma, so one may use A_sigma=2A0 and the budget A_sigma*sigma/kappa+B0*kappa*tau. Ancilla noise must be added explicitly rather than inferred from that original sigma.

These constants are defined by the enlarged guard and actual conflict incidence, not fitted hardware constants. If an added startup strip is required, increase B0 by N. Other boundary conventions must be charged similarly.

For fixed physical nu and tau, the two terms cannot independently be tuned to zero by choosing kappa. Their unconstrained minimum over kappa>0 is

    2 sqrt(A0 B0 nu tau),

at kappa=sqrt(A0 nu/(B0 tau)). The x<=1 and any other admissibility conditions must still be checked. If the available flag budget is epsilon_star, the condition

    nu*tau < epsilon_star^2/(4 A0 B0)

is necessary for THIS conservative sufficient recipe to meet its budget (and with an admissible minimizing rate it is sufficient for that numerical inequality). Its failure proves no impossibility for the device, a sharper analysis, or another decoder. Increasing initiation rate reduces idle noise per correction but increases local execution conflicts.

## 7. Failure modes and what remains unproved

- Exact isolated reduced C without clean-interval serializability does not justify commuting gates. Shared interacting baths/controllers must be included in conflicts or separately analyzed.
- A suppressed start that is not charged as bad invalidates the retained-rate slow certificates. All skips and aborts must be covered by a bounded-window flag with the proved bound.
- Global/nonlocal ancilla resets, long unbounded gadget durations, uncontrolled memory interactions, noisy timers, adversarial start rates, or access to future starts are not covered.
- A busy resource cannot be assumed to maintain independent Poisson COMPLETIONS. Only attempted starts have that law here.
- Unboundedly many starts can occur during one execution window. The mathematical model allows arbitrary bad behavior within fixed patches; it does not by itself prove that a finite controller can realize that scheduling/reset convention. Dropping conflicting attempts is compatible if every such drop is charged and the circuit remains locally well-defined.
- Fixed g is sufficient to make gate-level histories locally finite; constants in the birth probability do not multiply by g because an entire bad attempt flags its guard once. The actual bounded gate supports and resets remain necessary premises.

## 8. Prior-art calibration

Herold et al., Cellular automaton decoders of topological quantum memories in the fault tolerant setting (2017), explicitly studies asynchronous local decoding and its Markovian-master-equation interpretation. Thus asynchronous local updates and dissipative interpretations are established prior art. Its reviewed primary text is not a proof of the finite-duration overlap/skip serialization lemma above.
https://eprints.whiterose.ac.uk/id/eprint/117725/1/Herold_2017_New_J._Phys._19_063012.pdf

Breuckmann et al., Local Decoders for the 2D and 4D Toric Code, explicitly includes finite-speed communication/computation in the Harrington decoder. This likewise prevents framing finite local decoder latency as a new concern.
https://arxiv.org/abs/1609.00510

No exhaustive priority or independent validation of this particular bridge was performed. The substantive mathematical dependencies remain the reconstructed support/forcing/domination/torus/quantum modules and the named Hartarsky-Toninelli/Toom-contour import in ../../coherent_memory_packet_2026-10-15/STATUS.md.
