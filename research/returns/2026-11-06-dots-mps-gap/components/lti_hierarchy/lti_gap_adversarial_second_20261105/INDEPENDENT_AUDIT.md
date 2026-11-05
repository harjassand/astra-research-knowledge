# Second independent adversarial audit

Date: 2026-11-05. Auditor task: attack `lti_gap_completeness_20261105/PROOF_CANDIDATE.md`, independently of the existing review. The existing `INDEPENDENT_REVIEW.md` was not read. This is an internal mathematical audit, not external verification or a priority claim.

## Verdict

I did not find an actual counterexample or an omitted assumption in the precisely restricted theorem stated in the candidate. I independently rederived the energy moments, ground-space projection, duality, canonical Gram convention, whole-code stitching identity, and periodic spectral comparison. The candidate is substantially more than a numerical observation. However, it remains a proof candidate requiring expert scrutiny. The restrictions below must stay attached to the claim.

## Independent checks

1. **The spectral inequality is the right one.** For a positive frustration-free periodic Hamiltonian with first positive eigenvalue Delta_n, H² >= Delta_n H. This applies to every positive, unnormalized nu and does not require nu to be orthogonal to the ground space. Combining an upper bound for Tr(nu H²) with a positive lower bound for Tr(nu H) therefore gives the claimed upper bound for Delta_n. Ground-state weight cannot falsify this quotient. Replacing it by Tr(nu H)/Tr(nu), however, would be an invalid shortcut.

2. **Projection does not silently assume preserved LTI.** Since each positive local h_i annihilates the open-chain ground projector P on both sides, Q rho Q preserves h_i, h_i² and h_i h_j moments exactly. It need not preserve arbitrary marginal constraints. The proof only uses the preserved energy moments after this point. The open gap implies Tr(Q rho Q) <= (n-1)/g; this correctly controls otherwise unbounded ground-space mass.

3. **The core estimate is valid, including its sign-sensitive term.** Writing a=Tr(rho h_1²) and b_d=Tr(rho {h_1,h_{1+d}}), all b_d for d>=2 are nonnegative. The only potentially negative term is b_1 >= -2a >= -2M. Subtracting the core-square moment from m_c v gives coefficient one on b_1 when m_c>=2, and also gives the stated bound when m_c=1. Thus Tr(mu H_c²) <= m_c v+2M is valid. No uncontrolled extensive boundary subtraction is hidden here.

4. **The Gram orientation is correct in the stated convention.** For Gamma_L|a,b> having amplitudes (A_word)_{ab}, the entry G_L[(a,b),(c,d)] equals E^L(|d><b|)[c,a], with limit delta_ac sigma_bd. Hence G_infinity=I tensor sigma, not I tensor sigma^T. Primitive transfer with faithful sigma yields uniform invertibility for long blocks. Choosing theta strictly above the subleading spectral radius absorbs Jordan factors.

5. **The ideal stitch works on the entire two-window code, including reference entanglement.** Independently expanding arbitrary coefficients X_{a,c,d,b,ref}, decoding the two end buffers with S Gamma^+, retaining the two inner virtual factors, and encoding in cyclic order right buffer then left buffer produces amplitudes (A_t A_r A_l A_s)_{dc} times environment/reference coefficients. The retained sqrt(sigma) and inverse sqrt(sigma) cancel in the required order. No reversal of the order within either physical word is allowed. This establishes H_b K_0 P=0 as a whole-subspace identity, not just for one MPS vector.

6. **The repair cost does not secretly grow with the number of buffer bonds.** Actual and ideal outputs lie in the exact joined-buffer ground space. On those images all internal joined-buffer terms, including the periodic seam, vanish. Only two core/buffer seams act, with norm at most 2M. Consequently the boundary-square pullback is bounded by 4M² globally and is exponentially small on the two-window code. The positive-block domination step is valid by PSD Cauchy-Schwarz. Its failure-space weight is controlled by two open window Hamiltonians, costing O(ell), not O(n).

7. **The channel completion preserves the core marginal.** The success branch plus Q_0 X Q_0 trace-and-prepare failure branch is CPTP. Partial trace over the buffers removes P_0/Q_0 cross terms, so the sum leaves the entire core marginal unchanged. This remains true when the core is entangled with buffers or an external reference. The unprojected reference marginal would have been wrong; the candidate uses the projected failure marginal.

8. **SDP duality and nonattainment are handled.** The dual has the strictly feasible identity divided by Tr(h_1). For n>=3 the primal is feasible at delta=-M using the displayed coboundary and (h_1+h_2)²+(M h_1-h_1²)>=0; extra separated anticommutators are PSD. The dual is bounded below by the open-square moment estimate. Finite-dimensional SDP Slater duality therefore identifies values. All repair constants are independent of rho, so an approximating dual sequence is enough; no optimizing rho or limit repaired state is assumed.

These checks reproduce the comparison Delta_n <= gamma_n+O(sqrt(log(n)/n)) under the stated assumptions. The sandwich with gamma_n <= Delta_N for N>=2n then establishes existence of the periodic gap limit and equality with the hierarchy limit.

## Separate executable test

`check_independent_stitch.py` was written from scratch and imports none of the candidate implementation. It samples three complex d=3,D=2 unital tensors, computes their faithful fixed-point density matrices, builds all MPS words explicitly, and tests ell=2,3. The test spans the complete tensor product of the two (ell+1)-site code spaces and retains both discarded virtual factors as an environment. It checks the ideal seam identity, actual success-isometry identity, and the compressed boundary-square operator inequality.

All six tests passed. Ideal seam Frobenius residuals were 5.10e-15 to 7.83e-15; isometry residuals were 7.02e-15 to 1.48e-14. Fixed-point eigenvalues included (0.17138,0.82862), so these are not flat-Gram special cases. Exact numerical records are in `independent_stitch_results.json`. This tests the indispensable algebraic operation, not the entire theorem or global proper-parent hypotheses. Floating-point tests are not proofs.

## Scope that cannot be dropped

- The open ground space must eventually equal the fixed normal-MPS boundary space, not merely contain it. A unique product or injective-MPS bulk ground state does not establish this finite-interval hypothesis. PVBS-type extra boundary zero modes are an obstruction to that inference, not a demonstrated counterexample to the hierarchy's broader completeness.
- The open-chain uniform gap and primitive faithful canonical transfer are used essentially in this proof. Standard proper-parent theorems provide the gap; alternatively keep it explicit.
- The proof is for Rai's unrestricted Hermitian coboundary Y, equivalently Eq. (17). It does not by itself establish the projected-Y Appendix D variant. I did not audit any separate extension document.
- The limit is the periodic finite-size spectral-gap limit. Equality to a specified infinite-volume/GNS gap needs its own theorem and hypotheses.
- This is a fixed-model asymptotic convergence argument. It has no model-uniform constants and does not yield polynomial computational complexity. In particular, the level-n SDP has a d^n-dimensional PSD variable, and the constants can deteriorate with small sigma eigenvalues, small open gap, or slow transfer mixing. Inverting the error rate gives n of order epsilon^-2 times a logarithm, with model-dependent factors, before the exponential-in-n SDP cost is paid.
- The finite-range extension note and projected hierarchy are outside this audit's established claim.

## Closest checked literature and novelty boundary

1. Rai et al., *A Hierarchy of Spectral Gap Certificates for Frustration-Free Spin Systems*, Quantum 10, 2065 (2026), arXiv:2411.03680v3. Eq. (17) is precisely the dual used here: positive rho, equal end partial traces, and Tr(rho h_1)=1. The discussion explicitly leaves hierarchy completeness and exact-gap convergence unresolved, including the general one-dimensional frustration-free problem. The candidate would resolve a restricted proper-normal-MPS parent subclass, not that full question.
   https://arxiv.org/html/2411.03680v3
   https://doi.org/10.22331/q-2026-04-13-2065

2. Rozman, Molnar and Schuch, *Lower Bounds on Spectral Gaps of Parent Hamiltonians via Tensor Networks*, arXiv:2607.19078v1. This is the strongest close baseline, not just the older qualitative martingale theorem. Its blocking method yields computable lower bounds, proves positivity for normal/block-normal parent Hamiltonians, and states that its Lemma 2 bounds converge to the asymptotic open-boundary gap. It also explicitly distinguishes weak parents from proper parents and gives a finite-block ground-space criterion. The proposed theorem must be advertised as convergence of the particular Rai LTI hierarchy to the periodic limit, not the first convergent or constructive MPS gap-bound method. The actual practical compute comparison is not settled by the proof.
   https://arxiv.org/html/2607.19078v1

3. Rao, arXiv:2510.08427v2, a different hierarchy using enveloping algebras/second exterior powers, establishes finite-system completeness at a level depending on the number of qubits. This is not a thermodynamic fixed-window convergence theorem for Rai's dual.
   https://arxiv.org/html/2510.08427v2

Targeted web searches through 2026-11-05 did not locate an earlier proof of the exact restricted Rai hierarchy statement or this whole-code boundary repair argument. This search result is not sufficient to establish novelty. A careful expert literature review, including unpublished work, remains necessary.
