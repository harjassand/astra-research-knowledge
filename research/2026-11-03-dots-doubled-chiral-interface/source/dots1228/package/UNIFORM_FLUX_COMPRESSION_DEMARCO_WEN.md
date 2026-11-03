# Uniform flat-flux compression of the completed DeMarco–Wen rotor Hall model

## Result
For the completed 2+1D rotor model of DeMarco–Wen, a finite physical angular-momentum compression can preserve the entire finite-volume ground-state line bundle over flat U(1) twists. It preserves exact onsite charge, spatial locality, a uniform positive gap, and Chern number n^T K m. It gives up exact commuting-projector structure. The cutoff grows with volume. This does not establish a fixed-local-dimension thermodynamic regulator, nor the separate 4+1D free-fermion/rotor interface.

Primary text actually checked: https://arxiv.org/html/2102.13057 , Eq.(5), Eqs.(12)–(18), Appendix A Eqs.(19)–(24), and Appendix C. The paper gives the exact rotor model and transition functions; I did not find this finite noncommuting compression theorem stated there. It explicitly discusses difficulty retaining symmetry AND commuting projectors after finite truncation. The argument below is a consequence/extension, not a novelty claim.

## 1. Actual flux family, not a gap assumption from theta=0
Take a finite triangular torus sufficiently large that each local projector star is contractible. The normalized wavefunction is multiplication by a unit-modulus phase of the form

    Ω_theta(phi)=exp[-2pi i Σ_{I<=J} k_IJ Σ_triangles (dphi_I+a_I(theta))
                                                   floor(dphi_J+a_J(theta))],

with the oriented cup-product contraction and seam/ghost-variable prescription in the paper. Here theta=(theta_x,theta_y), with twists n_I theta_x and m_I theta_y. This schematic cochain formula is implemented specifically by the paper's boundary replacements and Appendix A; do not replace the seam prescription by an unrelated gauge coupling.

Let D_theta be multiplication by this phase on the physical rotor L2 space, and p_i the onsite projector onto zero angular momentum in all species at vertex i. Define the positive shifted Hamiltonian

    H(theta)=Σ_i [1-D_theta p_i D_theta†].

The phase ratio for changing only phi_i includes only triangles touching i; therefore these are the paper's local projector kernels with the stated boundary twists. D_theta is a unitary bounded multiplication operator even though its phase is discontinuous. It follows for EVERY theta, rather than merely at zero flux, that H(theta) has unique ground state Ω_theta, gap1, and norm<=v, where v is the number of sites/projectors. No unbounded kinetic operator is used in this step.

## 2. Genuine physical twists commute with compression
For each contractible star X_i choose a local lift of the flat boundary twists. This assigns ordinary onsite angular offsets alpha_j(theta) on that star. In the local kernel the twist amounts precisely to replacing phi_j by phi_j+alpha_j(theta); all phase factors from triangles not touching the updated site cancel between bra and ket. Haar integration in p_i is invariant under the corresponding translation. Consequently

    h_i(theta)=R_Xi(alpha(theta)) h_i(0) R_Xi(alpha(theta))†,

where R_Xi is the product of physical onsite U(1) rotations, with the standard seam prescription. Different local lifts differ by a constant symmetry rotation on the star, leaving its symmetric kernel unchanged.

Let P_N=Π_{i,I} 1_{|L_{i,I}|<=N}. Since P_N commutes with EVERY onsite rotation, not merely the total symmetry,

    P_N h_i(theta) P_N
       =R_Xi,N(alpha(theta)) [P_N h_i(0) P_N] R_Xi,N(alpha(theta))†.

Thus H_N(theta)=P_N H(theta)P_N on Ran P_N is the ORDINARY physical flat-twist family of the single finite-qudit Hamiltonian H_N(0). It is not an arbitrary artificial parameter family. Its matrix elements are finite trigonometric polynomials in theta, because local charges are bounded integers. It is therefore smooth, even though the original infinite-dimensional phase multipliers need not be norm-continuous as operators.

## 3. Uniform vector-valued Fourier tails from the actual phase
Use theta in the compact fundamental square [0,1]^2 and phi coordinates in [0,1). Twisting only changes the offsets of the floor hyperplanes, not their rotor-coordinate slopes. The smooth phase coefficients stay bounded because theta and fixed n,m are bounded. Thus the slice proof in FINITE_ROTOR_REGULATORS.md is UNIFORM in theta.

For an explicit conservative count, let D be the maximum number of phase triangles touching one site, κ the number of rotor species, K1=Σ_{I<=J}|k_IJ|, and Q=1+max_I(|n_I|+|m_I|). A safe bound is

    B=4pi D K1(Q+2),    R=1+2D κ².

Indeed a floor argument along any coordinate slice has slope 0,+1 or -1 and crosses at most two rounding thresholds over one period, regardless of its theta-dependent offset. Its magnitude is bounded by Q+1. Between cuts only the unfloored edge factor differentiates, giving the displayed phase-derivative bound. Count the periodic endpoint as an extra jump. The vector-valued argument applies without any internal-component multiplicity factor.

Writing d=κv, with Γ=B+2R,

    sup_theta ||(1-P_N)Ω_theta||² <= d Γ²/(2pi² N) =: τ_N.

Moving cut surfaces and their intersections do not invalidate this estimate: it is an almost-everywhere slice estimate followed by Fubini and Parseval. There is no claim of finite bare angular-momentum second moment.

For local continuity in theta, the set swept by the finitely many moving floor hyperplanes has measure O(|δtheta|), while the phase varies smoothly elsewhere. Bounded convergence therefore gives L2-continuity of local wavefunction sections. The scalar patch transitions given below take care of global topology. Continuous line bundles are sufficient; derivatives of the original discontinuous phase are not needed.

## 4. Uniform gap and exact bundle preservation
Let Π(theta)=|Ω_theta><Ω_theta|. Uniformly in theta,

    λ0(H_N(theta)) <= δ_N := v τ_N/(1-τ_N),
    λ1(H_N(theta)) >= 1,
    gap(H_N(theta)) >= 1-δ_N.

These follow from the compressed exact-ground trial vector and minmax, exactly as at zero flux. If δ_N<1, the finite ground line has nonzero overlap with the exact line. If Π_N(theta) is its spectral projection (embedded in the full physical rotor space), then

    ||Π_N(theta)-Π(theta)|| <= sqrt(δ_N) < 1.

The continuous nonvanishing fiber map Π_N(theta):Ran Π(theta)->Ran Π_N(theta) is a line-bundle isomorphism. This is stronger and safer than trying to control an ill-defined derivative of the infinite-rotor phase.

The actual DeMarco–Wen transition law is

    Ω_(theta+ell)=exp[-2pi i Σ_{I<=J}k_IJ
          (n_I theta_x m_J ell_y - m_I theta_y n_J ell_x)] Ω_theta.

Since both P_N and Π_N are fixed/periodic physical operators, the local sections Π_N(theta)Ω_theta obey exactly the SAME scalar transition functions. In the paper's convenient scalar gauge the y-edge gluing is exp[-2pi i (n^T K m)theta_x], and the x-edge gluing is trivial. Hence the finite compressed Hamiltonian's ground-state Chern number is exactly n^T K m, with the paper's orientation convention.

A concrete sufficient choice is τ_N<=1/(4v+1), giving δ_N<=1/4 and gap>=3/4. For requested ground-projector error epsilon and gap>=1/2, require τ_N<=min(1/(2v+1),epsilon²/(v+epsilon²)). Therefore N=O(v d Γ²/epsilon²) suffices, with constants explicitly above. For fixed κ,K,n,m and bounded-degree triangulations, v,d~volume and N~volume²/epsilon². Each physical site has dimension (2N+1)^κ. Full many-body storage remains exponential in volume; no efficient classical simulation follows.

## 5. What this does and does not close
This closes a finite-volume PHYSICAL resource interface for the completed 2+1D rotor Hall example: a symmetry-preserving local finite-qudit regulator has a uniform flux gap and the correct integer ground-bundle invariant. It does not evade any finite-dimensional commuting-projector theorem, because compression destroys commutativity and projector identities. Nor does it rely on replacing U(1) by Z_n.

The result fixes the integrated topological Chern response. It does NOT assert uniform convergence of Berry curvature pointwise, finite-frequency current response, all dynamical correlations, or an infinite-volume Hall coefficient at a fixed finite cutoff. Those demand additional estimates. A generic low-energy sector of the original flat CP Hamiltonian remains infinite dimensional, so the earlier obstruction to uniform arbitrary-state truncation remains intact.

The 4+1D swindle/fermion-decoration construction, any higher-dimensional twist invariant, gauged dynamical links, and the absent symmetric free-fermion/rotor interface each require separate checks. The argument here is not a license to infer their gaps from anomaly matching.
