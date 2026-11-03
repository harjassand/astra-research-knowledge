# Counterdiabatic electric coupling: explicit new regulator and acquisition gate

2026-11-03. This is a deliberately NONMINIMAL regulator. It does not inherit the zero-background conjugate purification at nonzero gauge field. The useful algebra, locality and self-adjointness can be paid for the actually acquired finite-device background domain; the desired uniform interacting mirror family is still absent.

## 1. Which background family is actually supplied?

For the finite-charge, finite-volume actual minimally gauged matrix h(A), the finite-box norm estimate in FINITE_TIME_QUANTUM_LINK_GATE.md proves a rank-one ground gap on

 D_epsilon={A: all principal plaquette curvatures |F_p|<epsilon},
 epsilon≤min(pi/(4S),Delta/(8SJ)).

Here S and J are the actual finite-box spanning-tree/charge constants. This is a derived domain, not an externally supplied admissibility oracle. Its threshold shrinks with the current volume-dependent resources. The unconditional local magnetic extension was withdrawn: discontinuous rotor cochains prevent importing its Schur comparison.

One CAN define a new gauge model with an infinite local plaquette barrier outside D_epsilon, and Dirichlet electric boundary conditions. That is an explicit hard-admissibility regulator, not ordinary Wilson dynamics. No claim that it approximates unrestricted gauge physics at fixed coupling/volume limit is made.

## 2. Actual response generators without a ground-projector oracle

On that domain let P(A) be the acquired unique ground projector. The actual vertices J_l(A)=∂_l h(A) are bounded finite-charge local terms. Choose an odd real-time spectral-flow kernel w whose transform is i/omega on all ground–excited energy differences |omega|≥delta, and smoothly regularized near zero, with rapid time decay. The family gap has delta≥3Delta/4. Define

 K_l(A)=∫w(t)e^(it h(A)) J_l(A)e^(−it h(A))dt.

This is computed from actual Hamiltonian dynamics and the known gap, not from a supplied eigenvector. It obeys

 ∂_lP=i[K_l,P],    ||K_l||≤C_w||J_l||/delta.

Matrix-element check: (K_l)_n0=i(J_l)_n0/(E_n−E_0), so i[K_l,P]_n0=−(J_l)_n0/(E_n−E_0), the correct derivative. The chosen zero-frequency kernel gives PK_lP=0. Derivative bounds follow by Duhamel with the first time moment of w, using actual first/second derivative norms.

Matter Lieb–Robinson plus the rapid filter gives spatially rapidly decaying tails centered at link l. It also gives JOINT link dependence: finite-time local dynamics can be truncated to a buffered finite patch whose input coefficients depend only on that patch's links. Exact exponential tails are not claimed after filtering. Uniformity needs uniform delta, local charges and interaction norms; the currently acquired finite-device sequence does not supply those constants independent of volume.

Gauge covariance is exact: h(A+dλ)=G_λ h(A)G_λ†, and the Abelian coordinate shift has unit Jacobian. Since G_λ is independent of A, J_l and K_l transform by the same conjugation. Thus the counterdiabatic terms preserve all Gauss constraints. They retain the actual same-chirality charges.

## 3. Self-adjoint Hamiltonian and exact invariant band

Define D_l=E_l−K_l(A). The identity above gives [D_l,P]=0. Use the CLOSED positive quadratic form

 H_CD=(κ_E/2)Σ_l D_l†D_l+H_B(A)+h(A)

on the gauge-invariant H¹_0(D_epsilon) form domain. Bounded K_l implies form equivalence with the electric Sobolev norm:

 ||K_l psi||²≤||K_l||²||psi||²,
 2|<E_lpsi,K_lpsi>|≤eta||E_lpsi||²+eta^(-1)||K_l||²||psi||².

Hence Friedrichs construction supplies a self-adjoint operator. No bare operator-norm-smallness of E is invoked. Smooth bounded P and ∂P preserve the Dirichlet form domain, and [D_l,P]=0 makes the two band subspaces reduce the closed form. Thus a prepared P-band state has exactly zero leakage for arbitrarily long time in this NEW model, despite unbounded electric bandwidth.

Physical interaction costs are explicit: relative to bare electric energy, add

 −(κ_E/2)Σ_l{E_l,K_l}+(κ_E/2)Σ_lK_l².

The first term is unbounded but relatively form bounded, the second bounded/quasilocal. These are designed momentum-dependent many-body interactions, not ordinary minimal gauging. Their strength uses J_l/delta and the filter's locality scale.

## 4. What survives in the low band?

With psi=f(A)Omega(A), PK_lP=0 and [D_l,P]=0 imply

 D_l[fOmega]=Omega[−i∂_lf+mathcal A_l f],
 mathcal A_l=−i<Omega,∂_lOmega>.

Therefore the exact P-band operator is

 (κ_E/2)Σ_l(−i∂_l+mathcal A_l)²+H_B+E0(A).

The Berry connection remains. The positive Born–Huang scalar from BARE electric projection is canceled by this particular off-diagonal counterdiabatic modification; it must not be retained twice or silently claimed unchanged. Changing diagonal parts of K changes the intraband connection and is a further physical regulator choice.

Exact band invariance alone does NOT prove that the P band is the lowest physical sector with a uniform excitation threshold. Its gauge kinetic/Berry ground energy can differ from that in Q. A pointwise h(A) rest gap does not compare the gauge zero-point energies of the two connection bundles. A finite-box bound can pay those differences, but an extensive subtraction without proof would repeat the earlier vacuum-energy error. This is a separate spectral gate.

## 5. Finite-range implementation and error

Restrict the actual dynamics in the filter to a finite patch and truncate the time integral. Complete gauge-invariant local terms can be retained in that patch, so gauge covariance is exact. LR/filter estimates give ||K_l−K_l^(R)||≤eta_R and similarly a derivative tail, with rapid decay and computable constants. Replacing K by K^(R) produces a strictly finite-range nonminimal electric coupling.

Band invariance is then approximate, not exact. The kinetic difference contains E_l(K_l−K_l^(R)), so there is no uniform operator-norm error over the infinite electric spectrum. On a charged finite-energy experiment, the same energy-relative commutator/residual method as in FINITE_TIME_QUANTUM_LINK_GATE.md controls the error by eta_R times electric second moments plus derivative tails. Range must be chosen for the stated time/energy accuracy. It is incorrect to apply the bounded-matter stability theorem directly to this unbounded cross term.

## 6. Why this does not yet close the chiral-gauge gate

The actual missing input is a gauge-covariant LOCAL interacting mirror band with a uniform background domain and gap while the desired chiral face is gapless. The supplied rank-one family is for the whole gapped finite device; it cannot be substituted for a mirror projector in a gapless slab. A low-total-energy band cut at a dense target spectrum may have tiny level spacing and nonlocal spectral-flow generators. An abstract rest tensor factor at A=0 does not solve this at A≠0, particularly after the conjugate-copy charge mismatch.

Nor are the nonminimal counterterms automatically irrelevant in a continuum limit. K_l can be orderJ_l/delta; with both J_l and delta at the matter UV scale, their ratio need not vanish. Projected Berry curvature, E0(A), canceled Born–Huang terms and induced gauge counterterms require explicit response matching. The construction is promising as a designed regulator only if these locality, band-ordering and continuum-matching gates are earned.

## Established comparison

Space-adiabatic perturbation theory already constructs almost invariant bands and effective Berry dynamics when its isolated-band and regularity hypotheses hold: Panati–Spohn–Teufel, https://arxiv.org/abs/math-ph/0201055 and https://arxiv.org/abs/quant-ph/0201123 . Local counterdiabatic approximations are established machinery, e.g. Sels–Polkovnikov, https://pmc.ncbi.nlm.nih.gov/articles/PMC5441767/ . The scientific novelty sought here cannot be the formal covariant derivative or generic adiabatic lemma. It would be acquisition of the actual local interacting chiral-mirror family and a paid physical gauge-response match. Those remain open in this construction.
