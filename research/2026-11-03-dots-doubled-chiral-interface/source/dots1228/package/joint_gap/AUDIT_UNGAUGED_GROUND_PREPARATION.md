# Independent audit: explicit ungauged ground acquisition

2026-11-03. Audited `POLYNOMIAL_UNGAUGED_GROUND_PREPARATION.md`.

Verdict: the state-acquisition mechanism passes for the specified finite-volume gapped regulator, with the compiled-Hamiltonian eigenvector error now separately budgeted.

The vector Fourier-quadrature telescope is correct. In every difference term, apply the differing coordinate FIRST to the raw normalized amplitude, use its uniform slice-BV error, then apply the remaining continuous/discrete Fourier maps as contractions in the corresponding mixed normalized L2 spaces. This avoids both the exponential tensor-dimension factor and the invalid L-infinity-BV shortcut for moving walls. The bound sqrt(2N+1) sum_j(V_j+2pi N)/S is valid.

The phase-grid state is acquired by a controlled GLOBAL Gaussian circuit from onsite Bell pairs and uniform rotor grids; its cost is polynomial in the actual one-body dimension, not the Fock dimension. Exact integer shears and the corrected output-order D dagger give the sampled final amplitude. Canonical Gaussian phases, rather than covariance-only synthesis, must be retained. The previously audited product-formula implementation does retain them.

Cutoff and total-charge postselection are contractions. Their accepted unnormalized vector differs from P_N Omega by at most rho, giving the stated success probability (sqrt(1-tau_N)-rho)^2 and normalized-state error <=2rho/sqrt(1-tau_N). Thus success is constant, not exponentially small. This is a total matter-charge projection, not a dynamical Gauss-law state-preparation result.

The known ground bracket and excited lower bound put Delta/2 strictly between ground and excitations of H_alg. The conservative trial-overlap bound is valid. Fixed-resolution QPE with a known norm/phase rescaling and repeated median discrimination supplies a ground filter with logarithmic false-acceptance overhead. It requires no unknown interacting ground energy when that positive-parent bracket is actually available.

A needed correction was identified and incorporated: filtering H_alg prepares its ground, not automatically the original compressed Hamiltonian's ground to the same requested accuracy. The additional eigenvector angle is bounded by epsilon_H/(g_target-epsilon_H). Choosing epsilon_H<=epsilon_out g_target/16, or explicitly adding this error to the output guarantee, closes that link. Merely epsilon_H<=Delta/16 would only establish separation, not arbitrary target-state accuracy.

The final algorithm is polynomial at fixed microscopic resources because it has an acquired high-overlap trial and certified gap. This is a property of the engineered parent, not an algorithm for arbitrary interacting ground states. It does not imply practical constants, classical wavefunction access, or gauge-field ground preparation.

For an exposed device, use the actual full finite-size gap min(Delta_rest,p_min) and acquire/restore the reference-energy scalar before reusing a QPE threshold. A rest-only threshold does not isolate the far-band ground. The corrected note explicitly preserves this distinction.
