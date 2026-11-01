# Independent audit: consuming the force loop as a physical CNOT

## Verdict and scope

The direct CNOT recompilation in `phase8/root/CONSUMED_CNOT_AND_FULL_EXPOSURE.txt` is algebraically correct. The nominal loss channel has the stated local Pauli form, and the local pulse areas and calendar arithmetic are consistent. A receiver proof that already accepts an arbitrary faulty physical pair operation can consume this primitive without strengthening its input contract.

I have not independently rederived the inherited Phase 7 `7 x 7` receiver schedule in this audit. Its old-error plus new-error theorem is an explicitly inherited premise. The new primitive does not by itself prove the persistent-strong-defect CNOT extension.

## Exact gate and complete nominal channel

Use the same two closed force trajectories with commuting data operators `J_x=Z_c` and `J_y=Z_t`. The two causal closures give the complete product channel, on arbitrary correlated data/bus/reference inputs,

\[
\Lambda_{DM}
=\left(\mathcal U\circ\mathcal D_{Z_c}(p_x)
\circ\mathcal D_{Z_t}(p_y)\right)\otimes\mathcal E_{M},
\qquad U=e^{i\pi Z_cZ_t/4}.
\]

Orthogonal radiation displacement modes give independent nominal dephasing factors. Their weights are

\[
p_j=\frac{1-e^{-2(2n_b+1)G_j}}2.
\]

Here `J_x^2=J_y^2=I`, so the matched self phases are global. This avoids the gauge-phase qualification needed for the collective pair-parity construction. The root values `p_x≈6.13404e-6` and `p_y≈1.94035e-5` are consistent with the supplied nominal Gram matrix at `kappa=1e-4 g`, `n_b=.1`.

Let `S=diag(1,i)`. Directly in the computational basis,

\[
S_cS_t e^{i\pi Z_cZ_t/4}=e^{i\pi/4}CZ.
\]

Therefore the chronological sequence

\[
H_t,\quad U,\quad S_cS_t,\quad H_t
\]

equals `exp(i pi/4) CNOT`. The post-loop operation `H_t S_cS_t` takes `Z_c` to `Z_c` and `Z_t` to `X_t`. Thus the complete final data channel is CNOT followed by independent control-`Z` and target-`X` channels, tensor the free bus channel. Product-channel wording does not imply that an initially correlated data/bus state becomes a product state.

All gate radiation must remain discarded for this particular channel statement. An observed gate-field record requires a separate instrument-level argument.

## Real local slots and concurrent cooling

With Hamiltonian `h(t) n·sigma`, a pi rotation requires area `pi/2`. A `.04/g` pulse with `.005/g` sine-squared rise and fall has effective flat-area duration `.035/g`, so the Hadamard-axis pulse requires peak coefficient `44.8799 g`. The `S` pulse has half that area and requires `22.4399 g`. Both fit the declared `50 g` per-site norm cap. Three `.05/g` local slots plus the `1.84/g` loop give `1.99/g`.

The loop’s new shared-force peak is lower than that of the already analyzed pair-parity use. The proposed subsequent `4.472/g` passive bus-cooling interval can fit within a `10.984/g` recovery period. Reusing the stronger driven-readout moment barrier is legitimate if the same healthy-port bounds, envelopes, fresh-field assumptions, and all residual-coupling exposure are included. Opening the cooling port is a physical operation; its switch faults and controller exposure remain charged. A gross port failure is not a small calibration term.

The calendar sum is correct:

\[
1.99+8(10.984)+.1=89.962.
\]

Any actual outer decoding, routing, refresh, or waiting time remains additional. The proof cannot infer a controller throughput from this arithmetic.

## Old error and fresh fault

The complete nominal channel is valid on arbitrary inherited data/bus correlations. Therefore a bus error surviving from an earlier cycle does not by itself invalidate the ideal next-use action. A new fault during a particular interblock loop can act on at most that physical pair under the declared local interaction model. Local pulses before and after the loop preserve that pair support.

This matches a consumer contract allowing one arbitrary pair fault, including coherent fault maps. It does not justify counting an inherited data error as a fresh clean input or assigning independent error coins to successive cycles. The entire physical CNOT, both recoveries, waiting, and classical actuation must share the inherited theorem’s fault budget. A common physical event touching several pairs retains its first-order weight and larger support.

## Strong ordinary comparator: use the direct dirty-bus gate

The earlier dirty-bus time `pi+.4≈3.542` was for a fused pair-parity transaction with two simultaneous data-controlled interactions in each data stage. It should not be reused as the comparator time for this direct two-qubit CNOT.

A bounded dirty mediator has the ordinary controlled-Pauli commutator. For example let

\[
A=e^{-i\pi P_1^c X_M/2},
\qquad
B=e^{-i\pi P_1^t Z_M/2}.
\]

Chronological `A, B, A†, B†` gives `CZ_ct tensor I_M` exactly, for every mediator state and every data/mediator/reference correlation. For control values other than `(1,1)` the mediator operations cancel; for `(1,1)` the Pauli commutator is `-I`. The opposite signs in the inverse stages also cancel the conditional phase factors, so this formulation needs no extra data-`S` correction.

Under the previously chosen convention that the available coefficient of `P_1 tensor Pauli` is capped at `3g`, each of four single active interactions can supply area `pi/2` in `pi/(6g)`. The interaction-area total is `2pi/(3g)`, with the actual chosen finite ramps and controls added. The ordinary dirty `CZ` needs only target Hadamards before and after to become CNOT. An oscillator geometric `ZZ` gate needs the additional `S_cS_t` slot in the explicit root compilation.

This is a fair accounting correction within one declared native-Hamiltonian convention. It is not a universal coupling conversion: `P_1 tensor Pauli`, Pauli–Pauli, oscillator-force, and dispersive implementations have different actuator bounds and microscopic noise. Changing that convention can change the numerical comparison. The comparator still requires actual bounded control, local pulses, recovery, waiting, and receiver noise.

## Scientific conclusion

The new complete-history interface is now consumed by a real encoded-gate contract rather than stopping at an isolated parity primitive. That is a useful completeness check. The nominal CNOT itself and the no-reset dirty-mediator capability are ordinary mechanisms. The justified advance remains a physical admission and fault-history certificate for the retained oscillator under the stated model. The supplied summed lifetime ledger is candidly only a sufficient upper bound and does not certify the illustrative long-computation target or establish a device/resource advantage.
