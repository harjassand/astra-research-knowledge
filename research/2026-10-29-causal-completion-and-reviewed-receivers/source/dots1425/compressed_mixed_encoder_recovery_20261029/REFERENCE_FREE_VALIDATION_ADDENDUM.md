# Whole-block validation without a Bell-reference link (qubit instance)

2026-10-29. Root additive construction, receiving review requested. Training-reference removal alone does not remove the Bell resource of the previously received blind selector; this note replaces that TEST explicitly.

For a fixed complete candidate algorithm (fresh training, current encoded payload call, joint compression and physical decoder), let M be its averaged logical qubit CPTP channel. Choose one of four tetrahedral qubit pure states with two uniform fair bits. Their Bloch vectors are(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1), each divided bysqrt3. These states form an exact pure-state2-design. Prepare the selected state, run the ENTIRE candidate, and measure survival in that same state using the inverse of its known preparation unitary. The failure bit is actual and nonnegative.

The complete candidate must not use the current test-state label before returning its logical output. The label is used only in terminal survival readout. Otherwise an input-aware replacement strategy could spoof the test and the fidelity identity would not apply. Training input labels remain available as specified; the hidden current payload-test label is a different item.

The standard average-fidelity identity gives
 q_fail=(2/3)[1-F_e(M)].
Thus to certify logical Bell loss<=epsilon, test the Bernoulli threshold alpha_test=2epsilon/3. In the already received rare-error validation rule, use
 m=ceil[32 log2(1/delta)/alpha_test]=ceil[48 log2(1/delta)/epsilon],
and accept if empirical failure<=3alpha_test/4=epsilon/2. A true Bell loss>epsilon is falsely accepted with probability<=delta; Bell loss<=epsilon/4 has true test rate<=alpha_test/4 and inherits the same good-candidate rejection bound. Fresh independent entire blocks remain the validation unit. All training/source calls are multiplied bym and must be counted.

After selection, the actual service uses a fresh independent block with the SAME selected classical code/rank/algorithm, not the old training gauge. If the sender can pad the logical payload before encoding and the decoder can undo/retire that key, the received Pauli-twirl transfer gives reduced-channel half-diamond error<=epsilon on the valid selection event. This does not add a retroactive input pad to an already-encoded unknown payload.

For a remote sender/decoder, send the prepared training/test systems through the actual channel and supply their necessary classical labels through a declared classical communication interface. The test label can be withheld until the logical output is fixed. No entangled Choi reference or joint Bell measurement is used in this explicit qubit training+validation variant. Decoder-side coherent storage of large outputs and all trusted local controls remain. If private roles/settings are needed for the separate memoryful guard, its stronger side-channel restrictions still apply.

The tetrahedral rotations are known but generally non-Clifford. Their finite synthesis errors must be included in the total instrument error allowance; exact ideal gate descriptions are not a hardware accuracy certificate. The general logical-k state2design version has coefficientk/(k+1) but needs its own finite sampling/preparation budget. This note fully specifies only the qubit finite-outcome choice.
