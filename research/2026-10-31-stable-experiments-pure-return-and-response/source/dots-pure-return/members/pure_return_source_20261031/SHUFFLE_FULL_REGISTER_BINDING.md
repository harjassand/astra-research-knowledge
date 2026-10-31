# Full-register binding for the acquired signed-shuffle example

31 October 2026. Concrete encoding qualification; does not modify the frozen abstract receiving theorem or claim whole acceptance before its receipt.

The signed-shuffle source uses n! valid permutation labels inside an ordinary binary register. The isometry/channel on the valid permutation subspace does NOT constrain an arbitrary extension on invalid bit strings. Extending it by the identity on those strings would invalidate the full-register operator return certificate with Q=I-|psi><psi|.

Let Pi_valid be the efficiently computable valid-permutation projector, and let psi_perm be the acquired uniform pure permutation state. Define an actual CPTP extension by

    Phi_ext(rho)
      = Phi_perm(Pi_valid rho Pi_valid)
        + Tr[(I-Pi_valid)rho] |psi_perm><psi_perm|.

The two branches have disjoint private environment flags, so valid/invalid cross terms are pinched. This is acquired without enumerating invalid states: compute validity coherently; on the valid branch run the acquired insertion isometry; on the invalid branch transfer the complete old source register into a private environment and prepare psi_perm. The old bits are retained, not reversibly erased. Preparation, validity computation, conditional transfer and the unitary extension/inverse are polynomial in n and precision with the actual supplied arithmetic circuits. The good-input environment vector c has only the valid flag.

For m>=1, the invalid branch has already returned to psi_perm. Therefore

    (Phi_ext^dagger)^m(I-P_perm)
      = Pi_valid (Phi_perm^dagger)^m(Pi_valid-P_perm) Pi_valid
      <= delta_m (Pi_valid-P_perm)
      <= delta_m (I-P_perm),

where P_perm=|psi_perm><psi_perm| and delta_m<=n exp(-m/n) is the symmetry-normalized valid-subspace return bound. This proves the required FULL-register inequality. The overlap A_ext=(<c| tensor I)W_ext annihilates invalid inputs, because their environment flag is orthogonal to c. Its valid restriction is the previously acquired overlap.

Add the independently reset fair sign qubit exactly as in `SIGNED_SHUFFLE_ACQUIRED_MODEL.md`. The full fixed state is psi=|+> tensor psi_perm. The product channel's m-step survival inequality remains <=delta_m Q_full: after one step the sign is |+>, and invalid permutation inputs are reset. One safe finite-arithmetic return horizon is

    m=n ceil(log_2(16n)),

which gives n exp(-m/n)<=1/16 and costs O(n log n). Using a smaller certified upward-rounded natural-log horizon is also valid.

Define the diagonal coupling to be zero on invalid permutation encodings. On valid labels it is the intended Z_sign tensor B_pi. Its norm and exact centering are unchanged. This qualification preserves the intended classical signed top-to-random process from the valid stationary preparation. It does not identify arbitrary quantum source interventions with classical controls.

Alternatively, one may formulate every operation on a rigorously invariant valid subspace and use Q=Pi_valid-P instead, but then every reflection, kernel and interface must consistently use that subspace. Mixing a subspace certificate with an arbitrary whole-register extension is not allowed.

Inputs received: `SIGNED_SHUFFLE_ACQUIRED_MODEL.md` and `markov_source_realization_20261031/ACQUIRED_SHUFFLE_MULTISTEP_RETURN.md`, together with their scoped local review. The abstract pure-return compiler assumes a full acquired certificate and does not itself repair invalid encodings.
