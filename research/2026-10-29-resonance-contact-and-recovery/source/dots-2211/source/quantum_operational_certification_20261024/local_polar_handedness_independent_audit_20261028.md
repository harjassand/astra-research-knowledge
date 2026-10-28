# Independent review: nonsingular local channels with either determinant sign

28 October 2026. Reviewer `producer-workspace/review_effect_only_acquisition`. **PASS for the exact algebraic addendum and imperfect-observable error bound.** This does not broaden the earlier SPD finite-acquisition contract. Author source unchanged.

For T=OS with O orthogonal and S positive, D=diag(1,det O,1) makes O_eff=OD proper. A physical qubit unitary implements O_eff. Postcomposition by its inverse gives the genuine CPTP residual with Bloch matrix O_eff^T T=DS and translated vector O_eff^T t. DS need not be symmetric or positive; no operation implementing the improper reflection D alone has been invoked. The local-unitary source gauge sends O to W^T O and preserves det O, so the resulting V_eff is invariant under that stated gauge.

For an own-algebra-commuting positive factor R, the Gram calculation uses T^T T, not det T. Thus whitening produces B_(O e_j)R/sqrt(c). The positive factor and strict sign gap yield three orthogonal reflection axes A_j, even when their orientation is improper. Pauli multiplication gives A_X A_Z=-i(det O)A_Y; consequently i A_X A_Z=(det O)A_Y. Keeping X,Z and using this physical Y is exactly the proper orientation OD. The three-reflection extraction circuit only needs X,Z, so it does not need a separate estimated sign of det T. Its eventual finite certificates must target this modified exact pair explicitly.

Partial trace to an envelope containing the own algebra preserves the commutant identity as in the separately received polar proof. Strict R_J positivity still follows from nonsingular qubit channels and finite product structure, independently of determinant sign. Tr R_J=1, |F_j|=R_J/sqrt(c), and sqrt(G)=sqrt(c)S prove S=Tr|F_j|sqrt(G). An SPD residual formula is not valid after the handedness change without D.

For Hermitian reflection approximations S_X,S_Z, C=(i/2)(S_X S_Z-S_Z S_X) is Hermitian and has norm at most one. Relative to the exact Clifford pair, each product difference has norm at most e_X+e_Z; averaging the two ordered products yields ||C-iB_XB_Z||<=e_X+e_Z. The unsymmetrized iS_XS_Z is generally non-Hermitian and cannot silently be measured as a Hermitian observable. Contraction against a separately acquired shadow matrix remains a known-matrix calculation, not a free new physical measurement.

## Independent fixture

`local_polar_handedness_independent_check_20261028.py` uses a genuine anisotropic Pauli CPTP map with Bloch diagonal (1/5,3/10,-1/10), surrounded by nontrivial input/output rotations. Its determinant is negative and its right positive factor is non-diagonal. The corrected residual DS is explicitly nonsymmetric. The proper U_eff is constructed as an actual qubit unitary, and its postcomposed CPTP channel is checked against DS. A three-qubit source with CNOT mixer and nonflat spectator states checks the local two-qubit partial trace, Gram whitening, corrected Pauli axes and scalar normalization.

The independent numerical perturbation fixture tests 64 pairs of imperfect exact reflections. It checks the commutator is Hermitian, has norm<=1, and satisfies the stated sum-error bound; raw iS_XS_Z is non-Hermitian in these cases. These are symbolic source identities plus floating stress checks, not source draws, a finite-confidence learner, compiled hardware or evidence of practical advantage.

No unresolved gap found within this exact algebraic scope. Singular contrast, changing correlated factors, finite conditioning/control guards, actual acquisition rate and broader noise membership remain separate obligations. No transpose or antiunitary implementation is accepted.
