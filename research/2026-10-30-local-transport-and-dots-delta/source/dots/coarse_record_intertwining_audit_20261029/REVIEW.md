# Independent receiving: coarse-record intertwining and local reflections
2026-10-29. PASS the mathematical lemma with mandatory `INTERTWINING_BIN_AND_COEFFICIENT_CLARIFICATION.md`. This does not receive an approximate decoder or a physical implementation of the spectral-sign reflections.

## Isometry intertwining
In the IDEAL controlled-Hamiltonian circuit every target-coupling gate is a controlled exp(itB_j). For any target X, Duhamel bounds its commutator by |t| ||[B_j,X]||; the control projection has norm one. All other ideal gates, clean initializations and copied/dephased record dilations act on ancillas. Telescoping the full circuit, and then restricting its input ancillas to their initialized state, proves ||V_j X-(X tensor I)V_j||<=T_j||[B_j,X]||. This is a global isometry bound with references, not an averaged nonselective bound. Sequential telescoping is valid without commutation of different record operators.

From B_cd=(Delta_c Delta_d+Delta_d Delta_c)/2, the commutator with B_ab has four terms, each bounded by kappa times a response norm at most one, giving 2kappa. The sequential Delta and B intertwining constants kappa T_total and 2kappa T_total therefore follow. This argument applies to ideal Hamiltonian controls; actual program collisions are not silently treated as commuting gates. Their received complete-instrument simulation error is separate.

## Numerical record localization and required cyclic lift correction
The original phrase “representatives in [-3,3]” was insufficient: a cyclic bin can have two such numerical centers separated by four, and only the lift near the physical spectral interval gives the claimed good-event error. The required additive clarification selects the unique lifted interval meeting [-1-g_guard,1+g_guard], when any exists. With actual g_guard=nu^2 w/256<w/2 and w<=1, the window length is strictly less than the gap 4-w between distinct lifts, so uniqueness holds. If none exists, a bounded arbitrary representative is harmless. On the good event, the median is in that window, so the selected center is within w/2+g_guard<=w of b; on the bad event all centers are bounded and error is at most four. This is determined by the public parameters and copied bin, not the unknown eigenvalue.

Conditional on an eigenvector of B_j, retained bin probabilities and coherent uncompute give squared localization norm at most w^2+16beta. Distinct eigenvectors remain orthogonal on the target and distinct record labels are orthogonal, so this is an operator norm bound. The stated zeta0=w+4sqrt(beta) is conservative. Uncompute commutes with B_j and preserves bin probabilities.

For the sequential instrument, move B_j through preceding stages, paying 2kappa sum_(ell<j)T_ell, apply its own localization, and append later isometries; those commute with the retained g_j. Combining this input-side bound with full B_j intertwining gives ||(B_j-g_j)V||<=zeta0+4kappa T_total. No actual state is normalized on a selected record.

## Record-dependent coefficients
The pointwise l1 coefficient assertion alone would not justify moving record-dependent coefficients through a global operator norm. The additive clarification supplies the correct blockwise Cauchy--Schwarz proof. For each record r, sum_ab |v_a(r)u_b(r)|^2=1. Applying this to the nine ordered E_ab=B_ab-g_ab and summing record blocks gives norm squared at most sum_ab ||E_ab V psi||^2<=9zeta^2||psi||^2. Thus both the squared-axis and symmetrized two-axis bounds are indeed 3zeta. Duplicate symmetric entries are counted consistently.

A recorded matrix correction of operator norm eta changes v^T g u by at most eta, pointwise. Restricting V by a record projector gives a contraction W, not a postselected normalized state. The thresholds g_i>=h allow division by h^2 and yield the local defects delta=(3zeta+eta)/h^2 and 2delta. The operator norms of the programmed linear axes are bounded globally on those record blocks by sqrt3/h.

## Reflection replacement and propagated support
For real a, |sign(a)-a|<=|a^2-1| with sign(0)=+1; functional calculus therefore gives the vector inequality ||(sign(A)-A)psi||<=||(A^2-I)psi||. The same is true at zero eigenvalues and does not require a gap. R,S are exact Hermitian unitaries on the whole declared space.

A record-dependent coefficient is a scalar within each block and commutes with target operators. Expanding D(v)^2=sum_ab v_a v_b B_ab and D(u) gives ||[A^2,B]||<=3sqrt3 kappa/h^3. Here taking the supremum of a pointwise block-operator bound is legitimate and is different from the preceding V-weighted localization estimate.

The missing-support risk is correctly paid: (A^2-I)BW=B(A^2-I)W+[A^2,B]W. Thus ||(R-A)BW||<=sqrt3 delta/h+3sqrt3 kappa/h^3=delta_cross. The symmetric estimate holds for (S-B)AW. Since R and S have norm one,
(RS-AB)W=R(S-B)W+(R-A)BW,
and analogously for SR-BA. Adding these two bounds and ||{A,B}W||<=2delta yields ||{R,S}W||<=4delta+2delta_cross exactly as claimed. No invariance of ran(W) under A or B is assumed.

## Scope, corrections and evidence
This is a local algebra/intertwining theorem for the ideal finite-record Stinespring dilation. Received collision and known-control errors can be paid as channel errors for the acquisition, but this note does not magically transfer an operator-norm isometry statement to arbitrary physical dilations. Nor does it supply finite sample-based implementation of sign(A), sign(B), an Fopt upper certificate, nearby global Clifford representation, consistent third/chirality direction, or a complete approximate-central decoder. The author's unresolved-objective section remains governing.

Independent diagnostics checked 400 Hermitian axis pairs across dimensions 2,3,5,9, including the propagated BW replacement and final anticommutator inequality, and 1,968 canonical cyclic-bin lift configurations. All passed. These tests supplement the analytic proof and are not finite native-program or decoder runs. Source originals were not modified; the two identified proof-convention issues are resolved by the hash-bound additive clarification.
