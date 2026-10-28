# Ordinary labelled access for reusable operator-norm acquisition

2026-10-27. Separate access reduction for the received clipped-operator reusable receivers. No joint sender/receiver Choi measurement is needed.

Let E have qutrit input and output dimension s, normalized Choi J, d=3s, and supplied bound ||J||<=L. Define omega=I_A/3 tensor E(I_3/3). A normalized qutrit projective2-design gives the receiver-local mixed program
T=E_j[|psi_j^*><psi_j^*|_A tensor E(|psi_j><psi_j|)] = (J+3omega)/4.
The sender prepares the known unentangled probe psi_j and sends its classical label. The receiver locally prepares psi_j^* and combines it with the received output. Discarding labels gives an iid sample of T from exactly one original source call. Similarly, sending I_3/3 and preparing I_A/3 locally gives one omega sample per call. These are the already received labelled-sample preparations; no shared entangled training reference is assumed.

Since J<=L I_AB, partial trace gives E(I_3/3)=Tr_A J<=3L I_B. Thus omega<=L I_AB and T<=L I_AB. Both are density matrices with the same known norm upper bound and dimension as J.

The generic clipped debiased-Keyl batch estimator in reusable_low_rank_choi_contrast_receiver.md estimates either state to operator error epsilon L/7, with failure probability beta/2, using a fixed sample cap of order
(d/(L epsilon^2))log(d/beta)
with only an absolute constant-factor overhead. Use independent labelled T samples and omega samples. Form the CLASSICAL Hermitian estimate
Jtilde=4Ttilde-3omegatilde.
With probability at least1-beta, ||Jtilde-J||<=epsilon L. No positivity claim is needed for Jtilde; all downstream received spectral-rounding or background-thresholding arguments start from a Hermitian operator estimate and produce a density explicitly.

Therefore canonical_reusable_quadratic_receiver.md, reusable_low_rank_choi_contrast_receiver.md, and reusable_known_positive_background_receiver.md retain their sample exponents with ordinary labelled unentangled source probes and receiver-local collective training measurements. The exact quantum measurement may remain difficult; no gate/computation efficiency claim is made.

For the canonical flat grid family, omega=I_(9D)/(9D) is exactly known. Only T needs to be estimated, to error epsilon/(4D), before setting Jtilde=4Ttilde-3omega. One explicit cap is n0=100D^2 per batch and
k=ceil(64(4/epsilon)^2 ln(18D/beta)),
with N=n0 k labelled source calls. The original downstream epsilon=nu/4000 and confidence choices can be retained. This is a factor16 sample overhead in the leading batch count, not a change in rank/signal exponent.

For the known all-real-p extra-sector dilution, apply the already received known-sector filtering/retry cap to labelled T samples. The extra-sector outcome is independent of the preparation label and U, and conditioned on a base-sector outcome leaves the exact base T. The classical labels and rejected source calls remain fully charged.

This reduction applies to these operator-norm-based constructions, not automatically to arbitrary fidelity-only Choi tomography algorithms. It does not grant physical Choi copies or a universal deterministic simulation of coherent unknown-input queries from labelled samples.
