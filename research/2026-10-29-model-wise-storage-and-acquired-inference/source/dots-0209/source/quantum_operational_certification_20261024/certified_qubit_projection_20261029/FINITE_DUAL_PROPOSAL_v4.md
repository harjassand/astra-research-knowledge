# Four-variable finite weighted dual proposal

This proposal is not trusted. Only rational feasibility plus rational weak-duality gap certificates are acceptance evidence.

Let k_i=1/w_i. Neglecting the constant independent of L, minimize the convex function

f(L)=Tr L+sum_i ||(Y_i-k_i L/2)_+||_F^2/k_i.

Its Hermitian gradient in trace pairing is I-sum_i E_i where E_i=(Y_i-k_i L/2)_+. In the four Pauli coordinates the gradient is2 coeff(I-sum E_i). The generalized Hessian column for Pauli basis matrix P_j is sum_i k_i coeff(D_positive[A_i](P_j)), where A_i=Y_i-k_i L/2. In an eigenbasis of A, the positive-part Fréchet derivative is entrywise multiplication by divided differences of max(lambda,0). At an eigenvalue coincidence away from zero this is1 or0; at zero a generalized derivative is selected. The implementation uses a small regularizer, a least-squares Newton step, and damped sufficient-decrease search. None of this proves convergence at all inputs or on singular faces.

Before the numerical proposal, the equality-only projection is tried exactly:

L=2(sum_i Y_i-I)/(sum_i k_i), E_i=Y_i-k_i L/2.

If every E_i is PSD this is a valid cone-constrained optimum. A finite dual certificate still governs return. At moderate or very large K, the seen-only dual can provide another proposal, but its finite aggregate-weight term remains in the certificate. This distinguishes an allowed candidate mechanism from silently dropping the1/K objective.

The documented random stress family has58 successful exact certificates and2 fail-closed refusals. These inputs are retained; successful original-family/memory tests do not remove this algorithmic incompleteness. In particular, constant dual dimension does not alone imply a generic polynomial-time implemented solver. The accepted generic finite-convex-solver theorem and this concrete numerical factory have different scope.

## Cancellation diagnosis and separately saved v5 proposal

The two retained v4 failures were not large intrinsic optimization gaps: the limiting proposals had finite-K gaps1.14e-9 and2.79e-9, barely above the1e-9 request. The finite double proposals reconstructed sum-of-effects defects9.28e-9 and4.47e-8 because multiplying a double multiplier error by K≈10^9 loses primal accuracy. The final Dykstra fallback then refused with much larger gaps; diagnostics preserve the intermediate stages in failed_face_diagnostics_v4.json.

`high_precision_dual_v5.py` changes the arithmetic precision, not the objective. It evaluates the same qubit positive-part map and its four-coordinate derivative at100 decimal digits, then repairs a floating primal candidate but retains the high-precision rational dual multiplier. For a rank-one positive part, with r=||v|| and -r<a<r,

E=( (a+r)/2, (1+a/r)v/2 ).

Its Jacobian has J00=1/2, J0j=Jj0=v_j/(2r), and Jij=(1+a/r)delta_ij/2-a v_i v_j/(2r^3). The all-positive/negative faces give identity/zero. Exact certificates on both previously failed inputs now have gaps5.733e-17 and1.179e-32, below1e-9. These certificates are separately saved in repaired_face_certificates_v5.json; v4's58/60 result is not overwritten or relabelled60/60. Public v5 is a fail-closed fallback and still does not prove convergence on arbitrary rational centers. Independent review remains required. mpmath is an additional reproducibility dependency, not a physics oracle.
