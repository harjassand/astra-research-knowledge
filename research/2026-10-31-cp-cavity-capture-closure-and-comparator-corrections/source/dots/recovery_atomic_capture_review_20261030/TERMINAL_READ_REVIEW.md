# Separate review of finite terminal copy-out
30 October 2026. Frozen source: FINITE_NOISY_TERMINAL_READ.md beside this review. This receipt is separate from the main record theorem.

**PASS at its stated physical-qubit output scope.** The source specifies actual target reset, a finite terminal pause of storage service, and parallel bounded-strength two-site CNOT copying. Its result is a joint Z-error bound on the physical output targets, not a protected macroscopic detector or external software output.

The reset law and port law hold on the same actual joint state because the port theorem is uniform in the retained bath and admits target-only reset operations. They are not independent. The commuting-projector Cauchy--Schwarz bound yields p^(|A|/2)r^(|B|/2), so expanding the XOR upper bound correctly gives q_w=sqrt(p)+sqrt(r). The square-root loss is retained.

In the copy interaction picture, the pullback of a target's wrong-Z projector is exactly the initial port/target XOR projector. Different output projectors commute and have disjoint bounded ideal cones. The explicit service pause removes nominal majority flips during that interval; target resets must also stop or be included as part of the explicitly analyzed ideal layer. Other QND port controls commute these tests. Finite-depth conjugation of the stipulated perturbations gives the accepted positive subset-moment inequality with a constant lightcone/incident inflation, not a volume factor.

The warm exponential moment follows by expanding product_j[1+(e^theta-1)B_j] and applying the joint XOR law. Exponential Markov then gives R2 exactly. Choosing e^(-theta)=(a C eta tau_c)^(1/a) when at most1 sets the extra exponential to e^(1/a), and bounding the warm bracket by q_w+e^(-theta) proves R3. At eta=0 the direct theta limit gives q_w. Displayed parameters may be capped at1.

The read interval is terminal: this does not establish that the paused storage subsequently resumes its earlier protected phase/moment state. The new output qubits also need a separate retention theorem if stored afterward. Detector errors require their actual instrument/noise interface. Those limitations are stated rather than silently imported.
