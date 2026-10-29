# Independent whole review of root's storage composition

29 October 2026. **ACCEPTED at its stated model-wise exact-Gaussian scope.**

Whole-read file: `../root_quantum_receiver/STORAGE_THEOREM.md`, Sections 1--5.
The separate `THEOREM.md` was derived from the accepted three modules before
reading root's composition. No numerical example or producer code was used.

I checked the following load-bearing points independently.

1. With c0=ln2/2, a=[c0/(2chi rho)]^(1/3) and
   R=floor(a2^(k/3))-1, the positive support-volume exponent is at most
   c0 2^k/2. Eventually R>=a2^(k/3)/2 and covers native supports. Hence the
   claimed p_k=4e exp(-c0 2^k/2) is valid on a common good sector.
2. sqrt(p_k)=2sqrt(e)exp(-c0 2^k/4). The native Hamiltonian defect bound,
   the 3n sampler clock, the coherent local factor 6, dissipative local
   factor 3, and all four truncation cross/tail terms are present.
3. For R>=1 the Gaussian R² tail is bounded by the chosen linear-R tail.
   Root's C_T=2B0+4D0+2D0² is safe, and its b includes both the local static
   exponent and radius-reduced coherent-tail exponent.
4. C_D=2sqrt(e)(2nu v+27)+3C_T and
   C_E=3beta nu v sqrt(e) have the correct factors. They give
   Fe(I/2) infidelity <=(3/4)n(C_E+C_D t)e^(-b2^(k/3)).
5. The stated onset, followed by t<=e^(b2^(k/3)/4), gives the claimed
   Fe error e^(-b2^(k/3)/2). The centered-Kraus conversion gives EVERY
   purified-input infidelity <=2e^(-b2^(k/3)/2) and diamond error
   <=2sqrt(2)e^(-b2^(k/3)/4). No Pauli-diagonal-channel hypothesis enters.
6. The source family has nonempty checks and Y_x edges covered by faces.
   The displayed g bound and n_k<=5g^(2k) are therefore safe. The exponent
   alpha=ln2/(6ln g) and c=(b/4)5^(-alpha) have the correct directions.
7. Constants/onset can be uniform over the perturbation class by using a
   single vbar and its uniform computable zetabar, rather than an unspecified
   actual incidence charge varying with k. This is an explicit formulation
   in my theorem, not a correction to root's intended uniform bounds.

No missing factor, stationarity assumption, or change of generator class was
identified. Root explicitly retains the H-adaptation, thermal ancilla and
physical-access limitations; that scope is essential to this acceptance.
