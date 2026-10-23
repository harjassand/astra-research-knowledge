# Coherent decoding against an actual response class: primary gentle-measurement comparator

## Primary source and exact scope

A. Winter, “Coding Theorem and Strong Converse for Quantum Channels,” *IEEE Transactions on Information Theory* 45(7) (1999), 2481–2485, §V (“On Good Measurements”), Lemma 9. The author-posted paper is [arXiv:1409.2536](https://arxiv.org/abs/1409.2536) (the version is the 1999 article). Lemma 9 states: for a quantum state \(\rho\), an effect \(0\leq X\leq I\), and \(1-\operatorname{Tr}(\rho X)\leq\lambda\leq1\),
\[
\left\|\rho-\sqrt X\rho\sqrt X\right\|_1\leq\sqrt{8\lambda}.
\]
The postmeasurement state here is **subnormalized**. The result concerns the entire state \(\rho\), so an arbitrary side/reference register can be included in its Hilbert space, with \(X\) acting only on the measured subsystem. It therefore supports a reference-stable disturbance estimate. The theorem itself is stated for one effect and does not state a multi-outcome coherent decoder or a postselected branch guarantee.

The version’s §II describes finite-dimensional algebras, while noting the argument works equally in the general case; the finite-tensor implementation here is within its stated setting. The lemma and proof are at PDF p. 3 (journal p. 2484). In the proof, the disturbance is bounded before tracing out any register, which is what lets a later fixed operation act on the full correlated state. A common subsequent CPTP instrument, retaining its outcome and environment registers, cannot increase trace distance. Conditioning on an accepted outcome is not itself covered by that contraction statement; postselection may amplify error, so a branch-vector estimate needs its own argument.

## Exact coherent-vector comparison for a decoded class

The source is a close conventional prior for the disturbance mechanism, but the sharper \(\sqrt{2e}\) vector bound used by the current construction is a direct coherent-decoding calculation, not Lemma 9’s stated constant. Let the actual class \(K\) be stored in an orthogonal reference register, with projectors \(P_k\), and let Bob’s supplied decoder POVM be \(\{D_k\}\). Assume its average success on the actual premeasurement joint state \(|\psi\rangle\) is
\[
\sum_k\langle\psi|P_k\otimes D_k|\psi\rangle\geq1-e.
\]
Coherently dilate the decoder by the local isometry
\[
V=\sum_k\sqrt{D_k}\otimes|k\rangle_G,
\]
and compare it to the ideal reference-copying isometry \(W=\sum_kP_k\otimes|k\rangle_G\). Since \(P_k\) and \(D_k\) act on different registers and \(\sqrt{D_k}\geq D_k\),
\[
\operatorname{Re}\langle V\psi|W\psi\rangle
=\sum_k\langle\psi|P_k\otimes\sqrt{D_k}|\psi\rangle
\geq1-e.
\]
Both outputs are unit vectors, so
\[
\|V|\psi\rangle-W|\psi\rangle\|^2
=2-2\operatorname{Re}\langle V\psi|W\psi\rangle\leq2e.
\]
Apply the **same** Stinespring dilation of Bob’s original fine instrument and the same local transformation controlled by \(G\) to both vectors. The norm difference remains at most \(\sqrt{2e}\); projecting onto the accepted subspace can only reduce it. This comparison retains the whole side/reference system and the original instrument. Its hypothesis is an externally supplied POVM that decodes the actual class with error \(e\) on the unconditioned premeasurement state. It does not infer such a decoder from a measured posterior, and by itself gives no error control after normalizing on a low-probability acceptance event.

Thus Winter (1999) is the primary source for the generic gentle-measurement state estimate; the actual multi-outcome coherent-copy inequality above is a short, source-compatible operator calculation. No novelty or priority claim is implied.
