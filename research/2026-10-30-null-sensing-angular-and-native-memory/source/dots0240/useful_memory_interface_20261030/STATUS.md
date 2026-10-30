# Useful memory interface status
2026-10-30.

## Useful deliverables
1. **Encoded Bell switch:** a concrete encoded-to-encoded entanglement-swapping workload using the reviewed noisy terminal frame/readout stage plus transversal CNOT. Matched column grouping makes the Clifford operation onsite and preserves the deterministic support certificate. Recipients remain encoded through arbitrary classical decoding latency. Construction in ENCODED_BELL_SWITCH.md; independent scoped PASS in BELL_INTERFACE_AUDIT.md (audit SHA-256 d64e7ff0a2073b04e76b47dcc89520724150027562fdacd367e657da1890f60a). The construction explicitly adopts its controller-mode and analysis-block-boundary caveats.
2. **Exact bare-port boundary:** finite-rate first/last-depolarizing-event proof gives an N-independent error floor for loading/retrieving an unknown bare fixed-size quantum state. BARE_PORT_NO_GO.md. This explains why the natural high-reliability interface must remain encoded or end classically.
3. **Strongest measure-first comparator for one useful task:** delayed choice between logical X/Z measurements has quantum success near one, versus exact classical-memory optimum (1+2^{-k/2})/2, with an explicit optimal collective POVM. DELAYED_BASIS_GAME.md.
4. **Subthreshold access no-go:** the storage theorem itself makes any recipient coupling inside its protected perturbation class approximately input-independent. SUBTHRESHOLD_ACCESS_BOUNDARY.md. This is standard information-disturbance applied to the accepted scopes, not a new sensing/computing theorem.

5. **A consequential waiting resource calculation:** independent rare encoded-link arrivals with p_N=exp(-alpha N) can be synchronized in mean exp(alpha N) rounds rather than exp(2alpha N) without a quantum buffer, while retaining exponentially small storage error if alpha<c. WAITING_RESOURCE_CALCULATION.md. A conventional quantum buffer receives exactly the same benefit.

## Do not overclaim
Encoded link preparation is still an interface. The Bell switch deliberately reuses (and credits) the prior controlled destructive CSS readout; it does not solve the physical mode switch or noiseless classical control. The new workload is an encoded entanglement switch, not arbitrary universal computation. The ordinary scheduled quantum competitor gets all the same link/gate/readout resources and implements the same logical primitive. Only the reviewed unscheduled waiting guarantee distinguishes the architecture, with no numerical hardware advantage established.

## Preparation route rejected rather than silently imported
A product-state stabilizer projection yields a generally large random syndrome. Gu et al.'s single-shot Tanner QEC theorem controls sufficiently low initial reduced-weight data errors; it is not an arbitrary-syndrome preparation theorem. Primary source inspected: https://link.springer.com/article/10.1007/s00220-024-04951-6 (Theorems 1.2/1.3 and detailed setup). A noisy classical syndrome-to-correction computation can therefore not be declared a fault-tolerant encoder by invoking single-shot QEC alone.

An independently protected encoded-state factory, an audited autonomous preparation mechanism, or a restricted source already producing encoded states is the exact next prerequisite for an end-to-end quantum-link application. No claim that it is impossible is made.

## Primary preparation comparison and handoff
- PREPARATION_BASELINE_2411.md: Bergamaschi–Liu genuinely prepares encoded Bell states from product inputs with a physical residual error envelope. Exponential factory reliability costs O(N²) factory qubits at linear distance; instantaneous feedforward and general Pauli versus retained-bath CPTP scope remain operational gaps.
- PREPARATION_2609_BOUNDARY.md: the newer confinement-only theorem's ideal matched recovery does not establish native-basin initialization. Its soundness branch does provide an LS residual, under its own model.
- INITIAL_SEED_SLAB.md: explicit LS physical residuals can terminate the native positive-record backward proof at a paid initial layer; subnormalized good factory events are supported.
- CONTINUOUS_INITIALIZER_HANDOFF_AUDIT.md: independently scoped PASS on root's complementary LS-support-to-animal-moment/gentle-basin handoff, conditional on the stated Tanner simple-compiler theorem. This handles coherent conditional support faults without an ideal cleanup; it does not solve runtime factory feedforward.
- AUXILIARY_AUDIT.md independently checked the bare-port, delayed-basis, and subthreshold-access ordinary proofs.
