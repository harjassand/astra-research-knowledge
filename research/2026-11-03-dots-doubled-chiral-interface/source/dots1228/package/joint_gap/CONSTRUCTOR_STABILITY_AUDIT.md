# Constructor audit of the direct product-frame stability bridge

Audited 2026-11-03 against PRODUCT_FRAME_STABILITY_AND_SYMMETRIC_TRUNCATION.md and the actual parent input. Assessment: positive at proof-bridge level; no range/threshold circularity found.

1. The signs are consistent. With omega=E_m-E_n and D_mn=i(1-fhat(omega))V_mn/omega, one has V+i[H,D]=B. For S'=iDS, d(S†HS)/ds=S†BS. Ground/excited entries give P'=i[D,P]. The explicit w(t)=sign(t)/2-integral_0^t f(u)du has w'=delta-f and, for the exp(i omega t) Fourier convention, what=i(1-fhat)/omega. Thus the spectral flow and low-pass derivative use the SAME compatible filter.

2. Since the low-pass support lies strictly below the bootstrap gap, EACH B_x commutes with the rank-one instantaneous projector. Conjugating by S and subtracting its scalar vacuum expectation makes EACH term annihilate the fixed product vacuum. This is the essential stronger property; merely knowing the total perturbation annihilates that vacuum would not suffice.

3. Product-vector conditional expectations preserve this annihilation exactly. Self-adjoint local shells O_X satisfy O_X=(1-P_X)O_X(1-P_X), whence absolute quadratic-form bound ||O_X|| sum_(x in X)q_x. Local Hilbert dimension is irrelevant. Support-count polynomial moments must be included; the draft includes them and the initial-radius labels.

4. Fixed bootstrap gap and fixed weighted interaction class give uniform filtered-dynamics and spectral-flow locality constants. The unperturbed K is allowed to have exponential tails, and the input perturbation is small in a fixed weighted norm. Consequently the constants do NOT vary with the final truncation radius. The first-gap-crossing argument is valid in each finite volume; bounded isolated-eigenvalue perturbation theory starts it even with infinite-dimensional rotor sites. Improved lower gap 3/4 excludes first crossing at1/2. This fixes the earlier Yarotsky cutoff-threshold circularity rather than hiding it.

5. The actual stronger parent supplies the required coercivity, not only a gap. ACTUAL_FAST_PARENT_AND_COERCIVITY.md gives cN<=K<=CN. Section1b of the stability draft gives an independent shorter route using Kref symmetry and the quasilocal vacuum-preserving R_beta excitation-number comparison.

6. EXPLICIT_JOINT_POLYNOMIAL_LOCALITY.md supplies the missing JOINT locality premise: grouped binomial polynomial terms for sign(h) have exponential operator-norm error AND finite rotor support, with only polynomial counting losses. The E0 counterterm is similarly acquired per-site. Thus this is not a stability theorem applied to a fiberwise-local but rotor-nonlocal oracle.

7. Scope: the theorem gives a symmetric strictly finite-range truncation for the uniformly gapped two-face/half-space boundary construction. It does not by itself prove that deleting a remote face mass leaves the near interface unaffected in a FULL finite-volume spectral sense: the intended remote chiral surface is gapless, so one cannot retain the previous global gap claim after that deletion. The half-space interface statement and a finite device with a desired remote chiral surface must be distinguished. Finite rotor charge cutoff also remains a separate scope restriction.

Primary machinery checked directly: Michalakis–Zwolak arXiv:1109.1588v3 SectionV Lemma1 (termwise filtered ground-projector commutation), and Nachtergaele–Sims–Young arXiv:1810.02428v2 Theorems6.3/6.4/6.14, Corollaries6.15/6.16 (spectral flow and locality for bounded interactions, allowing arbitrary onsite Hilbert spaces). The specialized product-vacuum coercive bootstrap is the team's deduction, not quoted as a theorem from those sources.
