# Independent challenge: periodic versus GNS gap

2026-11-05. Scope reviewed: `mps_gns_gap_extension_20261105/PROOF.md`, finite-range formulation, sections 1–6. This audit was performed without reading the other review file. The proof author was sent independently derived identities and one scope clarification. This is an internal audit, not external verification or a novelty endorsement.

## Verdict

I found no counterexample or missing mathematical hypothesis in the stated proper primitive-MPS parent class. The difficult reverse comparison, Delta_GNS <= Delta_N+O(sqrt(log N/N)), is supported by the explicit proof, rather than by an invalid interchange of a fixed-support limit with a growing-support operator. The argument appears complete conditional on the stated standard proper-parent gap facts and local form-core characterization. It does not extend as written to weak parents, nonprimitive tensors, arbitrary area-law states, or merely unique bulk MPS ground states.

## Independent derivation of the vulnerable steps

### Buffer projection and its energy

A first excited eigenvector can be chosen as a translation eigenvector since translation commutes with the periodic Hamiltonian. Its energy density is therefore exactly E/N. For the ell-site buffer's ground projector P, the uniform open gap gives q=||(I-P)psi||² <= (ell-r+1)E/(gN). Since P fixes the periodic ground vector, phi=Ppsi is exactly orthogonal to that vector.

The energy comparison must use the eigenvector equation. It gives

    <phi,H phi> = E(1-q) - <phi,H(I-P)psi>.

Only the at most 2(r-1) terms crossing the buffer cuts survive in P H(I-P). Hence their norm bound B_0=2(r-1)M gives the candidate's E+B_0 sqrt(q) upper bound. A generic low-energy vector would require a different estimate, with a possible extra factor two. The exact draft correctly uses an eigenvector.

### Uniformly bounded local preparation

Across core C and buffer B, the periodic ground coefficient matrix is

    Gamma_L F Gamma_ell^T / sqrt(Z_N),

where F swaps the virtual factors. Both block maps have uniformly bounded pseudoinverses once their lengths exceed a fixed threshold. Every phi supported in H_C tensor S_ell has matrix Y=X Gamma_ell^T. The candidate's

    O_C = sqrt(Z_N) X F Gamma_L^+

therefore gives (O_C tensor I)Omega_N=phi exactly. The transpose on Gamma_ell is correct for the coefficient matrix of a ket; it is not an adjoint. Its norm is bounded by sqrt(Z_N)||phi||||Gamma_ell^+||||Gamma_L^+||, independently of the core length.

An equivalent Schmidt check is useful: if mu=lambda_min(sigma)>0 and both block Grams are at least (mu/2)I, while Z_N<=2, all D² nonzero Schmidt coefficients are at least mu/(2 sqrt(2)). Thus a valid model-dependent uniform local-operator constant is K=2 sqrt(2)/mu after increasing the fixed block threshold. Conditioning can be terrible, but it does not grow with N for a fixed primitive tensor.

### Transfer convergence for support increasing to N

This is the main potential loophole, and it is closed explicitly. With b=N-k,

    W_b = F G_b^T F,
    W_infinity = sigma^T tensor I,
    rho_(k,N) = Gamma_k W_b Gamma_k^*/Z_N,
    rho_(k,infinity) = Gamma_k W_infinity Gamma_k^*.

Unitality gives ||Gamma_k||_HS²=D exactly, for every k. Also rho_(k,infinity) has trace one. Put epsilon_b=||G_b-I tensor sigma||. Then |Z_N-1|<=D epsilon_b and

    ||rho_(k,N)-rho_(k,infinity)||_1 <= 2D epsilon_b/Z_N.

For Z_N>=1/2 this is at most 4D epsilon_b, uniformly in k. This direct finite-virtual-space calculation avoids an observable-count or physical-dimension factor. It remains valid when k=N-O(log N). The candidate's Gram limit I tensor sigma and marginal metric sigma^T tensor I are both correct; confusing these two would break a generic complex-tensor implementation.

### Energy and normalization after transfer

The constructed O_N has uniformly bounded norm but support of length L=N-ell. Its norm and mean require only O(theta^ell) transfer error. The energy observable F_O=sum_(terms meeting C) O^*h_iO has support length L+2(r-1) and norm at most M(L+r-1)K². Thus the necessary energy error really is O(N theta^(ell-2(r-1))), not merely O(theta^ell). This N factor is included in the draft. Logarithmic buffers with the displayed coefficient make it negligible compared with sqrt(log N/N).

Centering O by its infinite-state mean does not change the energy. The variance lower bound tends to one, so there is no small-denominator or hidden normalization problem.

### The GNS variational principle

The reverse inequality limsup Delta_N<=Delta_GNS uses fixed local observables and ordinary transfer convergence. Local vectors form a form core for bounded finite-range interactions; equivalently, repeated local commutators yield analytic-vector bounds in this one-dimensional finite-range setting. The uniform periodic proper-parent gap, transferred to each fixed observable and then extended from this core, gives H_omega >= delta(I-|Omega><Omega|). Thus the variance denominator is appropriate and does not inadvertently exclude extra zero-energy GNS vectors.

Combining the inequalities gives existence of the periodic limit and its equality to the GNS gap, without borrowing existence from the LTI proof.

## Independent executable check

`check_uniform_constants.py` imports no candidate code. It generates three generic complex d=3,D=2 unital tensors and evaluates the exact finite-virtual-space formulas. Sixty cases vary buffer lengths 2,4,8,12 and core supports 2,5,20,100,1000. All passed the trace-norm comparison, infinite-marginal normalization, and Schmidt lower bound. Maximum observed trace-distance/bound ratio was 0.34117. Results are in `uniform_constants_results.json`.

These tests target increasing-support constants, not the full spectral theorem. They are floating-point diagnostics and are not certified inequalities or a substitute for the algebraic proof.

## Exact prior result checked

Bachmann, Dybalski and Naaijkens, *Lieb–Robinson Bounds, Arveson Spectrum and Haag–Ruelle Scattering Theory for Gapped Quantum Spin Systems*, Annales Henri Poincare 17, 1737–1791 (2016), Proposition 5.4. It proves that a fixed spectral interval missing from all sufficiently large finite-volume Hamiltonians is also missing from the limiting GNS Hamiltonian. This is the familiar finite-volume-to-GNS lower-gap implication. It does not supply the reverse comparison or equality used here.

- https://arxiv.org/pdf/1412.2970
- https://doi.org/10.1007/s00023-015-0440-y
- Saved primary PDF: `BDN_1412_2970.pdf`; extracted proposition is near line 1487 of the accompanying text.
- PDF SHA-256: 3edeb48a167b9ae6a26d6d885ccde03b068423d432176a256eb0a4ee42a14126.

Targeted searches did not identify a precise earlier theorem asserting this exact proper-primitive-MPS periodic/GNS equality with this quantitative route. That is not evidence of novelty strong enough for a priority claim. The normal-parent gap theory itself is classical (Fannes–Nachtergaele–Werner and subsequent martingale work). Exact equality could be known or implicit in literature not checked here.

## Remaining qualifications

1. Keep the proper-parent finite-interval kernel equality. Bulk-state uniqueness alone does not establish the needed buffer support or projection bound.
2. Keep fixed finite bond dimension, primitivity, faithful sigma, and a uniform open gap. Nonprimitive sectors or extra boundary zero modes require a different argument.
3. This proves an asymptotic statement, not efficient finite-size convergence in practice; constants can diverge as sigma becomes poorly conditioned or transfer mixing slows.
4. The computability consequence in section 6 additionally needs computably specified interaction/tensor data and effective certification, not arbitrary uncomputable real coefficients. This clarification was sent to the author.
5. Proof review and literature priority remain separate. No proof defect found is not equivalent to a published theorem or a confirmed new result.

## Final revision check

The author added the analytic-vector argument for the local form core and restricted the eventual-termination consequence to exact rational/algebraic data, with no claim to decide the proper-parent promise or implement exact certification. I inspected those edits and found them consistent. The computability clarification above is therefore addressed in the reviewed final version. The reviewed proof hash is recorded separately in `REVIEWED_PROOF_SHA256`.

## Addendum, 2026-11-05 13:35 UTC: sharper positive-seam estimate

The author proposed replacing the square-root projection estimate with a positivity argument. I independently checked it and found it valid under the same hypotheses.

Write H=H_B+H_C+V, where V is the sum of the b=2(r-1) terms crossing the two cuts. Let B_0=bM, phi=Ppsi, chi=(I-P)psi, and q=||chi||². Each summand is positive, H_B P=0, and H_C commutes with P. Consequently

    E >= <phi,H_C phi> + <psi,Vpsi>.

Translation covariance of the selected excitation gives e_V=<psi,Vpsi>=bE/N. Since phi=psi-chi,

    <phi,H phi>
      <= E + <phi,Vphi> - e_V
      <= E + 2 sqrt(e_V <chi,Vchi>) + <chi,Vchi>
      <= E + 2 sqrt(e_V B_0 q) + B_0 q.

This uses positivity of V and Cauchy-Schwarz in its quadratic form. It does not apply a full-Hamiltonian operator-norm bound. With q<=ell E/(gN), the excess is bounded by

    (E/N) [2 sqrt(b B_0 ell/g) + B_0 ell/g],

which is O(ell/N), uniformly for E<=rM. The variance denominator differs from one by O(ell/N), while the previously audited transfer error remains O(N theta^ell). Therefore logarithmic buffers improve the GNS/periodic comparison to

    Delta_GNS <= Delta_N + O(log N/N).

This sharpening concerns the separate GNS extension only; it does not change the original LTI hierarchy convergence rate. The revised full file still needs to be reread after the author integrates it.

An optional independently derived refinement is also valid: if mu=lambda_min(sigma) and epsilon_b=||W_b-W_infinity||<mu, then W_b>=(1-epsilon_b/mu)W_infinity. Thus for every positive observable F supported outside the b-site buffer,

    omega_infinity(F) <= [Z_N/(1-epsilon_b/mu)] omega_N(F).

Applied to positive F_O, this replaces the absolute O(N theta^ell) energy comparison by a relative O(theta^ell) factor. It is unnecessary for the O(log N/N) conclusion and was sent to the author as an optional separate refinement, not silently substituted into the reviewed draft.

### Integrated sharper-rate revision accepted

At 2026-11-05 13:37 UTC I reread the integrated sections 3–4 and checked the revised statement and conclusion in `PROOF.md`. Equation (10), the explicit bound on R_(N,ell), and the unchanged variance/absolute-transfer estimates consistently prove O(log N/N). No additional hypothesis or proof defect was found. The author did not include the optional multiplicative-transfer refinement, so it remains separate from the reviewed theorem. The updated full-file hash is in `REVIEWED_PROOF_SHA256`.
