# Fresh independent audit of the nearest-neighbor LTI completeness proof

Date: 2026-11-05. Scope: `lti_gap_completeness_20261105/PROOF_CANDIDATE.md`, read at approximately 12:31 UTC. This audit did not consult the earlier review reports or import their numerical scripts/data. It does not review the projected-Y extension or establish priority/novelty.

## Finding

I found no fatal gap or counterexample to the restricted nearest-neighbor proper-parent claim for sufficiently large hierarchy levels. The trace/energy estimates, ideal stitching on the whole local code, and periodic-limit squeeze survived an independent algebraic check and a fresh numerical reconstruction.

One concrete domain clarification is needed if the definitions are read as including every positive integer level: explicitly restrict the nearest-neighbor hierarchy to **n >= 3**. At n=2, the adjacent anticommutator is absent and the claimed global lower-bound property is false. The draft already calls n=3 the minimal nearest-neighbor level, so this is a clarification rather than an asymptotic obstruction.

This is an internal adversarial mathematical audit, not external validation or a machine-checked proof. No conclusion is made for the weaker promise of merely having a unique injective-MPS infinite ground state.

## Exact counterexample to extending the hierarchy to level two

Take the spin-1 AKLT interaction

h = [(S_1 dot S_2)+2 I][(S_1 dot S_2)+I]/6.

It is a nonzero projector. Thus every level-two dual feasible rho satisfies Tr(rho h^2)=Tr(rho h)=1, and gamma_2=1. A four-site periodic AKLT chain has a nonzero vector with eigenvalue exactly 1/3. Therefore Delta_4 <= 1/3 < gamma_2, despite 4 >= 2*2.

`check_level_two.py` builds the interaction in exact rational arithmetic, verifies h^2=h, and verifies H_4 v=v/3 exactly. `level_two_counterexample.json` gives all integer coefficients of v and its squared norm 40. No floating-point eigenvalue comparison is required for this counterexample.

**Recommended change:** Add “For n >= 3” where the hierarchy is defined and qualify the lower-bound/monotonicity statements accordingly. Nothing else in the large-n proof needs changing for this issue.

## Independent trace and energy checks

1. **Moment preservation under ground compression.** Since h_i >= 0 and P_n projects onto the zero eigenspace of the sum, h_i P_n=P_n h_i=0 for every i. Consequently Q_n h_i h_j Q_n=h_i h_j, even when i and j overlap. Cyclicity of finite-dimensional trace then proves exact preservation of every required first and second moment by mu=Q_n rho Q_n. Ground/excited coherences do not contribute. The fact that mu is generally no longer LTI is harmless because no later use of LTI is made except through these already-preserved moments.

2. **Trace bound.** H_o >= g Q_n yields g Tr(mu) <= Tr(mu H_o)=n-1. There is no normalization-to-one step and no unnoticed inverse energy denominator.

3. **Contiguous-core estimate.** Writing r=m_c, the difference r v-Tr(mu H_c^2) is sum_{d<r} d b_d + r sum_{d>=r} b_d. For r>=2 the sole potentially negative term has coefficient one and is b_1 >= -2M. For r=1 the same coefficient-one assertion holds in the second sum. This establishes the claimed r v+2M bound without an O(r) negative correction.

4. **Repair cost and trace accounting.** The P-compressed seam-square bound contributes O(theta^(2 ell)) Tr(mu), hence O(m theta^(2 ell)/g). The bad-code part is bounded by local end-window energy, whose expectation is exactly 2 ell, hence O(ell/g). These are distinct contributions. The O(ell) term is not multiplied by Tr(mu) a second time. Equation (9) has the correct scaling and constants under the stated estimates.

5. **Core marginal and denominator.** A CPTP channel confined to the buffers preserves the entire core marginal, including arbitrary correlations inside it. Thus both core moments are preserved. Positivity of H_b implies Tr(nu H_per) >= m_c; no lower bound on a normalized excited-state weight is needed.

6. **Square expectation.** The weighted Hilbert-Schmidt triangle inequality is valid for unnormalized positive nu. It does not require H_c and H_b to commute. The finite-dimensional inequality H_per^2 >= Delta_n H_per holds even if nu has a ground-state component. Equations (11)-(12) therefore follow without orthogonalizing nu or assuming a dual optimizer exists.

7. **Nearly optimal sequence.** All constants are independent of rho. Also m_c v+2M >= 0 for each feasible rho by the core moment estimate. Passage to the infimum is continuous and legitimate, including the endpoint zero. The bound gamma_n <= 2M supplies the uniform upper bound needed in the final rearrangement.

## Independent stitching check

I reconstructed the tensor indices directly. For a spanning input whose left and right windows have coefficients (A_p A_s)_{a,c}(A_t A_q)_{d,b}, ideal decoding produces retained factors f and e-prime with amplitudes A_t[d,f] sqrt(R)[e-prime,e] A_s[e,c]. The joined encoder has coefficients (A_{joined})[f,z] sqrt(R)^(-1)[z,e-prime]. Its contraction cancels the two square-root factors, leaving

(A_t A_{joined} A_s)_{d,c}

with the original outer indices carried in the environment. This works coefficientwise, hence for the entire tensor-product code and every external reference. It does not require the original input to be a selected global MPS ground state or a product across the windows.

I independently verified the Gram convention:

G_L[(a,b),(c,d)] = E^L(|d><b|)[c,a] -> delta[a,c] sigma[b,d].

Thus R=sigma, not sigma transpose, for the stated flattening. The physical output order must be t, right buffer, left buffer, s, without reversing words within buffers. The stated order satisfies this requirement.

Both actual and ideal encoders have output in the joined S_{2 ell}. Therefore internal joined-buffer terms annihilate each output, and also their difference. Bounding H_b on these images by the two seam terms costs at most 2M, not O(ell M). Squaring costs at most 4M^2. This is sufficient for the claimed operator estimate, not merely an expectation estimate on one MPS.

## Fresh numerical falsification attempt

`check_stitching.py` independently generates three complex d=3, D=2 right-canonical tensors (seeds 1729, 2718, 3141), computes their invariant densities, builds Gamma and polar maps, and constructs actual and ideal Stinespring maps on an orthonormal basis of the full product of the two enlarged-window ground spaces. It imports none of the original scripts or data. Each sample passed the check that its three-site parent kernel has dimension D^2. This finite check is not itself a proof of the all-length proper-parent hypothesis.

For each seed I tested ell=2,3,4. Results:

- Maximum Stinespring isometry defect: 5.551e-15.
- Maximum ideal seam annihilation residual: 4.179e-15.
- Actual compressed seam-square norms for seed 1729: 0.0145196, 0.000885237, 0.0000870218.
- Corresponding norms for seed 2718: 0.0171760, 0.00418408, 0.000347624.
- Corresponding norms for seed 3141: 0.0520504, 0.0133983, 0.00388652.
- Every case satisfied ||H_b K|| <= 2 ||K-K_0|| within numerical tolerance (M=1).

The fresh random invariant densities are genuinely non-scalar and complex. The correct product-Gram error decreased; the transposed-metric error generally did not. The results are in `fresh_stitching_results.json`. These are whole-code-subspace tests, not tests solely on one periodic MPS. They support, but cannot prove, the general identities or asymptotic bounds.

## Periodic-limit inference

For every fixed valid level n, gamma_n <= Delta_N eventually in N. Hence L=sup_n gamma_n <= liminf_N Delta_N. Conversely, Delta_n <= gamma_n+e_n with e_n -> 0 yields limsup_n Delta_n <= L. These two inequalities prove both existence of the periodic-gap limit and equality with the hierarchy limit. There is no circular assumption that the periodic gaps already converge, and no illicit exchange of an n-dependent hierarchy level with the fixed-level lower-bound statement.

The inference does not identify the limit with a GNS gap; the draft correctly refrains from claiming that. It also uses the unrestricted hierarchy, not the projected-Y variant.

## Hidden assumptions that must remain visible

- A uniform open-chain gap for all sufficiently large intervals, not merely infinite-volume uniqueness.
- Exact eventual open-chain ground spaces S_L, not just containment of an MPS in the ground space.
- A primitive finite-dimensional canonical transfer channel with faithful invariant density, ensuring a positive limiting Gram matrix and uniform boundedness of inverse square roots.
- A fixed model: constants may deteriorate arbitrarily with its transfer spectrum, conditioning, injectivity threshold, and open gap. The rate is not uniform over all proper parents.
- The buffer-repair channel may jointly act on geometrically separated ends. This is permitted for a variational proof but is not a local hardware implementation.
- The theorem is an asymptotic completeness statement. It does not establish efficient polynomial-time numerical access to the resulting certificates: the SDP matrix dimension is d^n.

## Source definition check

I separately opened the primary Rai et al. source and confirmed that its Eq. (17) uses the objective sum j=2,...,n-1 and the LTI/energy-normalization constraints appearing in the candidate. The source's general-range formulas use different-looking index bounds; those are not grounds for silently changing the candidate's expressly nearest-neighbor Eq. (17) convention.

Source: https://arxiv.org/html/2411.03680v3

## Conclusion

Within the restricted nearest-neighbor, sufficiently-large-level, proper-parent scope, this fresh attempt did not find a central counterexample or proof gap. The exact n=2 counterexample supplies a small but concrete domain correction. External mathematical review, novelty assessment, effective constants, extensions, and equivalence to other infinite-volume gap definitions remain separate questions.
