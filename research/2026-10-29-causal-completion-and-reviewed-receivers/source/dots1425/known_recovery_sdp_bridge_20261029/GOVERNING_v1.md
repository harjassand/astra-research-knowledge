# Standard known-channel SDP bridge to additive-optimal opaque recovery
2026-10-29. Author theorem, receiving review pending. The optimization method is conventional, not a new SDP or new QEC criterion.

## Known finite optimization problem
Let C:k->d be the rational CPTP channel reconstructed in the accepted compressed-channel learner. Let its normalized Choi state use input-first tensor order. In column-vectorized recovery order (output k fastest), define
 W=(S C^T S†)/k,
where S permutes the Choi factors into that recovery ordering. Equivalently W=sum_l vec(K_l†)vec(K_l†)†/k² for ANY Kraus representation of C. This identity is representation independent and the matrix is computed directly from rational C, without extracting unknown source Kraus operators. W>=0, TrW=1/k, ||W||op<=1/k.

For recovery Choi J=sum_a vec(L_a)vec(L_a)†, entanglement fidelity is Tr(WJ), and its exact primal/dual SDPs are
 max Tr(WJ), J>=0, Tr_output_k J=I_d;
 min TrY, Y Hermitian, Y tensor I_k>=W.
The primal center J0=I_(kd)/k is strictly feasible, has smallest eigenvalue1/k and trace d. Feasible primal matrices have trace d and Frobenius norm<=d. The dual has strictly feasible Y=(1+1/k)I_d. Strong duality holds and the common optimum is F_opt(C). This is the standard optimum-recovery SDP of Fletcher–Shor–Win (quant-ph/0606035v1, SecIV), applied to a learned small channel rather than a supplied original ambient channel.

## Finite weak-SDP contract and exact repairs
For target0<zeta<1, set xi=zeta/(16d). Use a conventional rational weak-SDP algorithm to obtain rational Hermitian J,Y with
 Tr_output J=I_d EXACTLY,
 J>=-xi I,
 Y tensor I_k-W>=-xi I,
 TrY-Tr(WJ)<=zeta/4.
All inequalities are required certified conditions, not a floating solver stopping message. Exact affine TP is imposed by rational linear parameterization; PSD slack can be certified using rational matrix separation/eigenvalue enclosures. A proposed numerical solution which fails the checks is not accepted.

Repair by
 J'=(J+xi I)/(1+k xi),   Y'=Y+xi I_d.
Then J' is exactly PSD and TP, and Y' is exactly dual feasible. Since TrJ=d and each negative eigenvalue has magnitude<=xi, ||J||1<=d+2kd xi. Hence
 ||J'-J||1 <=[xi*kd+k xi(d+2kd xi)]/(1+k xi)=2kd xi.
The primal objective decreases by at most2d xi; the dual objective increases by d xi. Thus the certified primal/dual gap is at mostzeta/4+3d xi=7zeta/16<zeta. In particular J' implements an actual CPTP recovery whose known-channel fidelity is at least F_opt(C)-zeta. The exact repaired primal/dual certificate can be verified independently of the optimizer.

## Why the finite solver is a paid ordinary computation
This is a rational, bounded, strictly feasible SDP, not a black-box unknown-environment optimization oracle. A rational Hermitian basis of the TP affine slice is obtained by eliminating the linear partial-trace equations. With m<=2(kd)² real coordinates, one can use integer basis matrices of Frobenius norm at most2 and free coordinates bounded by2d. A conservative affine-coordinate interior radius is1/(4km) around J0, and an enclosing Euclidean radius is4md. k=1 is the trivial decoder and can be handled separately.

Rational PSD separation is polynomial bit complexity (e.g. symmetric elimination with exact rational negative-quadratic-form witnesses, or certified spectral bounds). The usual rational weak ellipsoid optimization for a well-bounded convex set therefore produces the above accuracy in polynomial(k,d,input-bit-length,log(1/zeta)) time. Objective slices near the optimum remain well-bounded after mixing an optimizer with J0 by an O(zeta) fraction; this supplies a radius polynomial in zeta, not an assumed unknown spectral gap. The dual can be restricted to TrY<=2 when seeking near optimum: dual feasibility implies Y>=0 and its optimum<=1; adding a small identity makes it strictly feasible with polynomial margin. Equivalent standard primal-dual weak-SDP algorithms are allowed.

The finite guarantee invoked is the conventional rational weak-SDP/ellipsoid guarantee, with explicit dimension/radius/slack data above. No generic solver was executed in this packet (cvxpy is unavailable); no claim of a new optimizer implementation is made. Vandenberghe–Boyd, *Semidefinite Programming*, SIAM Review38 (1996), Sec1, discusses polynomial-time separation/ellipsoid and interior-point methods: https://web.stanford.edu/~boyd/papers/pdf/semidef_prog.pdf .

## Physical known-matrix recovery
From the exact PSD Choi J', compute a known Kraus factorization and the Stinespring isometry with environment dimension at mostkd. Its total output dimension is at mostk²d; pad to qubits and complete this known isometry to a unitary. Standard finite two-level/Givens synthesis gives a polynomial(k,d,precision-bits) circuit and classical computation, with a declared channel-error budget gamma_rec. No source Stinespring, source inverse, coherent source access or supplied environment is used. Small eigenvalues of J' are not a source condition-number promise: the known PSD square root can be approximated to squared numerical tolerance, and the exact TP isometry has orthonormal columns. The compiler acts on the small randomized compressed payload, not on a classically reconstructed D-dimensional source.

## Additive-optimality transfer
Let N:k->D be stationary memoryless with rank N(I/k)<=d. Use the accepted reference-safe common-gauge compression and small-channel tomography. On the good estimation event, halfdiamond(C,A_U)<=delta, where A_U is the true small channel in its single common Haar gauge. Then for every CPTP recovery R, its entanglement fidelities on C and A_U differ by at mostdelta. Consequently
 |F_opt(C)-F_opt(N)|<=delta,
 Fe(R_J' A_U)>=F_opt(N)-2delta-zeta.
Include tomography failure beta and the full compression/synthesis channel budget gamma (including gamma_rec) to obtain
 Fe(implemented recovery of N)>=F_opt(N)-2delta-zeta-beta-gamma.
This is additive near-optimality in maximally mixed-reference entanglement fidelity, NOT diamond-near-optimality, quantum capacity, encoder search, or perfect recovery of an irreversible channel. The repaired dual/primal values also bound F_opt(N) within their zeta optimization interval plusdelta statistical error on the good event.

The same finite forward training-query budget as the compressed learner applies, with delta chosen proportional to the desired additive fidelity accuracy. No extra source queries are used for the SDP. All stored quantum training outputs and the later payload must share the common compression batch; a new standalone payload normally requires a fresh batch. The accepted Box–Muller common-design compiler replaces fixed-d GT enumeration and yields uniform theoretical polynomial(k,d,1/accuracy,logD) quantum/control cost with huge constants, provided its padded dimension d' is used consistently in tomography and design order.

## Scope, dependencies and example
Dependencies: compressed_mixed_encoder_recovery_20261029 and its low-support receiving extension; box_muller_design_compiler_audit_20261029/REVIEW_RECEIPT.json for uniform compiler; primary optimum-recovery SDP above. Their original scopes are preserved. The accepted Petz theorem remains valid independently and does not depend on this optimization upgrade.

AMPLITUDE_DAMPING_CERTIFICATE.md supplies exact rational matching primal/dual witnesses (optimal Fe81/100 versus Petz approximately0.710644 at a4/5). check_amplitude_certificate.py verifies12 such examples; these are exact analytic fixtures, not a generic SDP deployment. The general finite algorithm and physical synthesis are theoretical contracts. No historical novelty, universal quantum advantage, practical runtime, hardware implementation or arbitrary-memory claim is asserted.

## Closing the small-D polluted-encoder branch
The independently received controlled spectral-filter construction treats N_eta=(1-eta)V(rho tensor sigma)V†+eta I_D/D with supplied eta<=eta_U<1 and rank bound r. Its large-D branch already gives Fe>=F_opt(N_eta)-epsilon, while the previous small-D branch used only the squared-optimum Petz theorem. When D<256kr/[(1-eta_U)epsilon], D itself is polynomial in the supplied small parameters. Direct tomography of the full but now small channel, followed by this standard SDP and physical known-matrix compiler, gives Fe>=F_opt(N_eta)-epsilon there as well. Thus a NEW composed corollary covers both branches with additive optimality and polynomial source/control costs in k,r,1/(1-eta_U),1/epsilon,logD. The exact family optimum is1-eta+eta/k². This does not remove the irreducible depolarizing error or extend the family to arbitrary memory/noise. The earlier received filter theorem is unchanged; this last corollary depends on acceptance of the present SDP bridge.
