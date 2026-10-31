# An ordinary Gaussian free-kernel implementation for the open chain

31 October2026. Root construction, pending independent review. This is a concrete implementation candidate for the source-only no-jump kernel, not a new integrability claim or a simulation of the entire coupled system. It is intended to replace a costly generic LCHS subroutine where existing quadratic-fermion machinery applies. The physical source generator and its actual jump stack are unchanged.

## 1. Exact parent operator in domain-wall coordinates

Use the open zero-field source of GEOMETRIC_GIBBS_NATIVE_COMPILER_BINDING.md. Let q_j=exp(2J_j)>0 for edges j=1,...,n-1. Map physical spins to a global first spin (qubit0) and domain-wall signs (qubits1,...,n-1) by reversible prefix XOR. The parent H=sum_i Pi_i is the symmetrized classical heat-bath generator.

At an interior physical spin, let L,R denote its adjacent domain walls and let J_L,J_R be the edge couplings. Define

 a=[tanh(J_L+J_R)+tanh(J_L-J_R)]/2,
 b=[tanh(J_L+J_R)-tanh(J_L-J_R)]/2,
 c=[sech(J_L+J_R)+sech(J_L-J_R)]/4,
 d=[sech(J_L+J_R)-sech(J_L-J_R)]/4.

The exact local parent term becomes

 H_i=I/2-(a Z_L+b Z_R)/2-c X_L X_R+d Y_L Y_R.

Proof: its diagonal heat-bath rate is [1-tanh(J_L Z_L+J_R Z_R)]/2. The odd function of two binary signs is exactly a Z_L+b Z_R. The magnitude of the simultaneous-flip offdiagonal is [2cosh(J_L Z_L+J_R Z_R)]^-1=c+d Z_L Z_R. Multiplying by -X_L X_R turns its second term into +d Y_L Y_R. No state-space enumeration is used.

The left boundary is

 H_1=I/2-(tanh J_1)Z_1/2-(sech J_1)X_0 X_1/2.

The right boundary is

 H_n=I/2-(tanh J_(n-1))Z_(n-1)/2-(sech J_(n-1))X_(n-1)/2.

All coefficients are rational or square roots of rationals for rational q. For example tanh J=(q-1)/(q+1), sech J=2sqrt(q)/(q+1), and the sum/difference formulas use q_L q_R or q_L/q_R.

## 2. One explicit work qubit removes the boundary linear term

Append qubit n in |+> and replace the last X_(n-1) by X_(n-1)X_n. Call the resulting nearest-neighbor XY operator H_ext. It commutes with X_n, and its restriction to X_n=+1 is exactly H in domain-wall coordinates. The X_n=-1 restriction is unitarily equivalent: conjugating all original n qubits by their product Z flips the sign of the right-boundary single-X term while preserving every Z field and two-spin XX/YY term. Thus H_ext is positive and has the same nonzero gap g as H, with a two-dimensional zero space. For n=1 the separate formula is H_ext=(I-X_0X_1)/2, with the same restriction statement.

The added qubit is a prepared computational work resource, not a changed physical source. Every successful source-kernel block returns it to |+>, and its preparation, projection flag, and gates are paid. Arbitrary physical source inputs are allowed. No theorem is asserted on an unprepared work-qubit domain.

## 3. Acquired quadratic normal form

For N=n+1 augmented qubits define Jordan-Wigner Majoranas c_(2j)=Z_0...Z_(j-1)X_j and c_(2j+1)=Z_0...Z_(j-1)Y_j. Then

 Z_j=-i c_(2j)c_(2j+1),
 X_jX_(j+1)=-i c_(2j+1)c_(2j+2),
 Y_jY_(j+1)= i c_(2j)c_(2j+3).

Consequently H_ext=nI/2+(i/4)c^T A c for an explicitly acquired real antisymmetric 2N-by-2N matrix A. It has O(n) nonzero entries; constructing it uses only the local input data. In this displayed Jordan-Wigner order, c_0 and c_(2N-1) never occur: the endpoint Z fields and endpoint YY couplings vanish. They provide two exact zero Majoranas before numerical diagonalization. The known positive gap implies there are no additional zero modes. Ordinary real orthogonal quadratic diagonalization of the remaining block yields

 U_G^dagger H_ext U_G = sum_k omega_k n_k,

with one zero fermionic frequency and all other omega_k>=g. The constant offset is zero because the parent is positive with a known zero state. A zero-mode orientation can correct the orthogonal determinant without changing H_ext. The auxiliary-sector equivalence and the known source gap establish the gap statement; floating-point eigenvalues are not used as certificates.

This uses standard Gaussian-circuit machinery. Jiang et al., Quantum Algorithms to Simulate Many-Body Physics of Correlated Fermions, arXiv1711.05395, Section IV and Appendix A, explicitly describe quadratic diagonalization and Gaussian-unitary construction: https://arxiv.org/pdf/1711.05395 . Their method is an ordinary component, not an Astra discovery. A conservative nearest-neighbor Majorana/Givens implementation has polynomial classical preprocessing and O(n^2) Gaussian rotations, with all angle synthesis and routing paid.

An approximate normal form is sufficient. Compute an orthogonal transform, frequencies and a certified residual ||H_ext-H_tilde||<=xi using the small Majorana matrix. A sufficient explicit residual certificate is |n/2-sum_k omega_tilde,k/2|+(N/2)||A-O A_diag O^T||, using the spectral matrix norm. It includes the absolute scalar-offset discrepancy. In particular, if H_tilde is defined with zero vacuum energy, its constant is sum_k omega_tilde,k/2; the difference from the exact n/2 must be included in the certified residual, not discarded. The two exact zero Majoranas can be isolated without an uncertain eigenvalue test. Ordinary backward-stable/certified finite matrix arithmetic is paid. No inverse spacing between distinct positive frequencies is assumed: nearly degenerate positive modes may be treated as a cluster. Only the certified gap separating zero from positive frequencies is used to identify the zero subspace. The preprocessing must actually verify its residual; this note does not supply an exact eigenbasis oracle.

## 4. Complete contraction block, without generic LCHS

The previous native compiler needs, for s=lambda*t,

 F(s)=(1/2) Q exp[-s(H-gQ/2)] Q,

up to its stated normalization convention. In the Gaussian occupation basis let Q_ext project onto at least one occupied POSITIVE-frequency mode. Occupying the zero mode alone remains in the ground space. Reversibly identify the first occupied positive-frequency mode. If none exists, select a zero-output flag. Otherwise define a diagonal attenuation with factors

 exp[-s(omega_k-g/2)] for the marked occupied mode,
 exp[-s omega_k] for every other occupied positive mode,
 1 for unoccupied or zero-frequency modes.

Every exponent is nonnegative. Their successful product is exactly exp[-s(sum omega_k n_k-g/2)] on Q_ext. Implement each factor by an ordinary controlled one-qubit acceptance rotation with a fresh failure flag. These flags stay coherent; this is not normalized postselection. Uncompute the marker, reverse U_G, and project the work qubit back to |+>. Include the original domain-wall transform and its inverse. The successful compression onto the work-qubit input state is exactly Q exp[-s(H-gQ/2)]Q on the original source. A final factor-one-half attenuation gives F(s), so the existing factor-two majorant and its full output proof can be retained unchanged.

For s>=2 log(1/eta)/g, use the zero block instead, with norm error<=eta/2. All nontrivial kernels therefore have s bounded by O(log(1/eta)/g), irrespective of the microscopic rate. The time register, its conversion s=lambda*t and the cutoff comparison have their actual finite-bit cost.

## 5. Finite arithmetic and actual rotations

The filters need no online exponential oracle. For a finite binary time s=sum_l b_l Delta_s 2^l within the active range, precompute the acceptance coefficients exp[-omega_k Delta_s 2^l] and exp[-(omega_k-g/2)Delta_s 2^l]. Controlled on time bit b_l, mode occupation and the marker flag, multiply the appropriate contractions. Their product has the exact desired exponential for that represented time. Large coefficients are clipped only with the allocated absolute error, and very small acceptance amplitudes are not divided by. A straightforward implementation uses O(n B_time) filter rotations in addition to the Gaussian transforms and marker computation. It uses fresh success flags for products, rather than uncharged intermediate measurements or resets.

For 0<eta<1/4 choose the full normal-form residual xi<=min(g/8, eta*g/[100(1+log(1/eta))]); tighten the small-matrix residual by its displayed N/2 factor. The positive/zero spectral projectors differ by O(xi/g), and on the bounded active time range Duhamel bounds the semigroup change by O(s xi), after allowing the projector correction. Approximate frequencies are clipped to at least 3g/4 on the positive modes, while the known zero mode remains exactly zero; the induced matrix and scalar-offset changes remain inside the certified residual. Thus the marked attenuation omega_tilde-g/2 is at least g/4 and every filter remains a contraction. These facts give a uniform source-operator kernel error O(eta), not a dimension-amplified entrywise assertion. Gaussian unitary, coefficient arithmetic, individual rotation and work-qubit projection errors are subdivided across the explicit operation count. Taking smaller tolerances is allowed; all additional bits are paid.

The successful nominal block returns the work qubit unchanged even though intermediate Gaussian gates need not preserve its X eigenvalue. An approximate implementation may leak by its charged operator error. The final |+> projection is part of the block flag and may not be omitted. This is essential to the admitted source domain.

## 6. Evidence and limits

check_glauber_quadratic_kernel.py compares the restricted XY parent and the Majorana many-body spectrum for n=1,...,6, including signed weak bonds. Residuals are below 8e-15. A 258-by-258 Majorana matrix for n=128 is also formed without a 2^128 table; its numerical gap is diagnostic only. These tests are not an executed Gaussian circuit or a whole-simulator resource estimate.

The construction is specialized to the open zero-field one-dimensional heat-bath parent. It does not apply to arbitrary dark sources or replace their LCHS receiver. It does not make the entire system-plus-source interaction Gaussian: the noncommuting A_i and source interaction insertions remain. It does not by itself remove complete first-event amplification, word/clock sampling, actual jump-stack gates, or observation costs. It is a candidate use of stronger existing source-kernel machinery, not a practical-advantage or novelty claim.
