# Reconcile a late factory Pauli without assuming retired controllers
2026-10-30. Candidate controlled interface; not independently audited.

Suppose the factory boundary before feedforward is

    P_factory^dagger E_factory Enc(rho),

with P_factory the eventually computed Pauli from its measurement record. The unknown-coset buffer preserves this state up to a small relative Pauli e_buffer, while maintaining the original shared baseline. Thus, once P_factory is known, applying it yields

    (+/-) e_buffer E_factory Enc(rho).

Pauli conjugation does not enlarge support. On the factory's successful low-total-weight event and the buffer's global-energy event, this is inside the ordinary target-code correction radius. No knowledge of the true initial random syndrome is needed to assert this physical statement.

Live controllers require more than applying P_factory to bare DATA. Let F_old be the full-Hilbert frame for the old baseline program, and F_new the frame for zero baseline. Use the explicit controlled mode required by the earlier terminal readout, suppressing all incompatible dynamics. The intended finite-depth handoff is

    W=F_new (P_factory on DATA) F_old^dagger.

Between the inverse and forward frames, replace the old shared program by fresh zero program registers, retaining the old classical record as an environment if necessary. In the gauged representation, W applies only the desired DATA Pauli and leaves clock/lock/workspace coordinates unchanged. Consequently it does not assume every controller has retired, and does not simply restart a theorem on a measurement-conditioned clean controller state.

Both frames have bounded-depth bounded-range structure, and P_factory is a parallel one-site Pauli layer, even if its mask has extensive weight. Mode switching, new-program preparation, and gate faults must all be included in the controlled-stage noise model. Their local light cones give bounded-support bad events. The old marking/ancestor history must be retained across the interface; no faulty owner is declared newly pristine merely because the program changed.

The revised native instrument/mark proof must check the exact program-controlled gauges, good-range invariance, and late-ancestor bounds through this stage. This note identifies an actual constant-depth nominal circuit and a plausible charged seam; it does not certify those additional contracts or a fully autonomous mode switch.

After the handoff, continue ordinary zero-baseline protection. The classical computation can have taken a long time because the relative-coset buffer was active throughout. Its own computational correctness remains a separately charged classical probability, and the baseline record still had to be maintained reliably during that time.
