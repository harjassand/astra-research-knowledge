# Finite-operation and precision budget for the acquired pair-Pauli route

27 October2026. Local post-cutoff addendum; independent receiving requested. The received ideal pair-Pauli theorem remains unchanged. This supplies a finite-operation variant with statistical slack, not an efficient implementation of the collective Keyl POVM.

Use the original known input parameters0<t<=1,beta and known measurement-only padded dimension D<2d. All decoder optimization and physical partial-trace constraints remain on the original d=3s space after compression. Supplied numerical parameters have finite rational descriptions; conservative rational lower regularizations and upper copy counts can be used.

## 1. Deterministic finite arithmetic replaces exact diagonalization

At a pilot scale u let the stored Hermitian estimate be rho_bar and define the known target G0=rho_bar+uI (G0=I initially). Compute a unitary basis U and positive rational numbers g_i with a CERTIFIED operator residual

 Gtilde=U diag(g_i)U*, ||Gtilde-G0||<=u/100.           (1)

The quantum measurement target is the explicitly described U basis, not an unknown source eigenbasis. Abort unless u/2<=g_i<=4. No square-root/inverse of the unknown state is computed.

On a preceding successful pilot history,

 .74(rho+uI)<=Gtilde<=1.26(rho+uI),
 rho<=2Gtilde, lambda_minGtilde>=u/2.                (2)

The .74 and1.26 bounds follow from the previous3/4 and5/4 bounds and uI<=rho+uI. Successful histories pass the stated spectral guard with slack.

Use the same actual pair-Pauli estimator in this known basis, but increase the stage count to

 n_u=ceil[(16384D²/u) ln(8DK/beta)],

where K is the total pilot stage count down to u_*=t/4. The moment bounds12D²/u and centered norm12D/u remain valid by(2). Matrix Bernstein at whitened deviation1/20 has exponent at least n_u u/(10000D²), paying failure beta/(4K).

The EXACT raw empirical mean in the U basis, rotated back, has relative statistical error at most(1.26/20)(rho+uI). Store a Hermitian approximation to this raw mean with certified operator error at most u/100. The stored estimate therefore has relative error at most

 1.26/20+1/100=.073<1/8.                             (3)

This closes the pilot induction. The measurement/control basis is allowed to depend on all preceding classical observations. First-failure conditioning, not an assumption about bad histories, gives pilot failure at most beta/4.

IMPORTANT: full whitening followed by dewhitening cancels on the sample mean. The algorithm simply accumulates the RAW unbiased pair-Pauli estimators. The whitening map is used only in the proof of concentration; no numerical inverse-whitening computation is necessary.

## 2. Final basis and raw contrast acquisition

After the T-only pilot form G0=4T_bar+tI. Compute another certified basis Gtilde_A with residual at most t/100. On the pilot event,

 .865(A+tI)<=Gtilde_A<=1.135(A+tI)<=(5/4)(A+tI).

Abort unless its computed eigenvalues lie in[t/2,6]; good histories pass. Both actual states T and omega satisfy rho<=2Gtilde_A. Use independent single-copy pairs in this known basis, with

 n_c=ceil[(2048D²/t) ln(8D/beta)].

The exact filtered contrast has variance156D² and centered norm60D/sqrt t as before. Bernstein at deviation sqrt t/2 pays failure at most beta/4. Thus its exact empirical filtered error E0 has norm at most sqrt t/2.

There is again an exact cancellation: inverse Sylvester applied to the empirical filtered mean gives the RAW empirical contrast4Y_T_bar-6Y_omega_bar. The algorithm stores this raw contrast, rotated back and compressed to the physical space, to certified operator error at most t/100. It need not numerically apply a Sylvester inverse or square root to data.

For analysis only, undoing the known Sylvester map and Douglas factorization give

 Hhat-H=sqrt(A)Z+Z*sqrt(A)+R,
 ||Z||²<=(5/16)t,
 ||R||<=[sqrt(5)/2+1/100]t.                         (4)

The t/100 term includes raw-contrast reconstruction error. The received exact-source localization therefore gives a constant below25rt+2kappa, and the robust two-comparator localization gives a constant below85rt+2kappa. In particular the previously used conservative bounds140rt+2kappa and3L_*+300rt+2kappa remain valid, with no downstream change of exponents or promises.

The known deterministic source cap is

 N_cap=sum_pilot_scales n_u+2n_c=O((D²/t)polylogs).   (5)

All stored averages can be accumulated from integer outcome counts and rational estimator coefficients in the measured basis. Interval matrix multiplication controls the final basis rotations of these averages. Their norms and all reciprocal regularizations are polynomially bounded in D and1/t, so the requested u/100 andt/100 tolerances require only polynomially many bits and operations in the stated parameters and input bit lengths. No sampled probability needs to be computed.

## 3. Gap-free certified basis computation

A spectral gap is NOT needed for(1). One explicit method is classical complex Jacobi diagonalization of the known Hermitian G0. Each exact two-level rotation removes one chosen off-diagonal entry and decreases the squared off-diagonal Frobenius norm by twice that entry's squared modulus. Choosing a largest entry decreases this norm by a fixed fraction at least2/[D(D-1)] per step. Therefore O(D² log(D||G0||/u)) steps suffice for residual much smaller than u/100, without any eigenvalue separation.

Finite computations can select an entry within a fixed fraction of the maximum while the residual exceeds the target, and approximate each two-level rotation with error smaller than an inverse polynomial in D,1/u and the known norm bound. For example choose step errors small enough that their total matrix perturbation is below u/1000 and each step's decrease before termination loses at most half its exact guaranteed decrease. This requires only inverse-polynomial absolute accuracy (one may use a bound proportional to u²/[D^4(1+||G0||)^2] per step, additionally divided by the known step cap). Verify the final residual by interval arithmetic before accepting the basis. Rational rounding of diagonal entries is included in(1).

All paths have a known norm bound: a raw pair-Pauli sample has norm O(D), so stored pilot means and G0 have norm O(D); final contrast means have norm O(D). Bad histories may abort but cannot create an unbounded arithmetic workload. Strict success margins ensure that sufficiently accurate certified arithmetic does not introduce aborts on good histories. Near-degenerate eigenvalues affect neither the residual certificate nor the statistical proof.

## 4. Finite universal gates and adaptive transcript error

Each known D-dimensional basis unitary can be decomposed into a polynomial number of explicitly known two-level rotations (dense synthesis uses O(D²); retaining the Jacobi product costs only an additional logarithmic factor). The matching basis requires O(D) more two-level rotations. Classical matching/settings/probe labels are sampled from finite distributions; bounded-bit approximate sampling can be charged in total variation.

Known two-level gates can be reduced to one-qubit rotations and controlled gates on log2D qubits using standard constructions; see [Barenco et al., Elementary gates for quantum computation](https://arxiv.org/abs/quant-ph/9503016). Fixed finite universal-gate approximation with polylogarithmic accuracy overhead is supplied by [Dawson--Nielsen, The Solovay--Kitaev algorithm](https://arxiv.org/abs/quant-ph/0505030). These are imported circuit-compilation tools, not claims about efficient Keyl measurement. Their primary source descriptions were checked27 October2026.

Let G_max be a deterministic polynomial upper bound on the number of target elementary gates in any ONE training preparation/measurement circuit. Choose per-gate operator approximation error at most

 beta/[32 N_cap G_max].

The resulting per-trial measurement-channel diamond error is at most beta/(16N_cap). Bound the settings/matching/probe-label sampling variation by the same amount per trial; O(log(D²N_cap/beta)) random bits per bounded integer draw suffice with conservative modulo/rounding bounds. These budgets include local known probe/reference preparation, basis rotation and standard readout.

Adaptive transcript coupling is valid: whenever previous classical histories match, the two procedures choose the same target next measurement, whose conditional outcome-channel error has the stated uniform bound. Telescoping over at most N_cap queries bounds the whole transcript discrepancy by at most beta/4. Source CPTP calls cannot amplify a preceding known-operation error. There is no continuity assumption on how an eigenbasis is chosen as a function of the observed history.

The exact-target finite-classical algorithm has statistical failure at most beta/2 by Sections1--2. The compiled physical protocol therefore succeeds with probability at least1-beta after the charged transcript budget. Classical interval/residual certificates are deterministic and are not treated as an unobservable probabilistic success event.

The number of known gates and classical bit operations is polynomial in D,N_cap,1/t, input bit length and log(1/beta). It is NOT polynomial in log D alone, and this is not a practical-speed claim. Quantum storage is one physical output plus known local/embedding/work registers, rather than an n0-copy collective measurement. The source's own unknown internal gate cost is not bounded by a query theorem.

## 5. A concrete finite decoder and verification composition

To avoid any uncharged SDP implementation primitive, use the separately received top-r projector decoder alternative if desired. Approximately diagonalize the stored PHYSICAL Hhat with residual zeta<=t/100, select the at-most-r positive diagonal entries, and let P be their projector in that explicitly represented unitary basis. It is an ACTUAL projector. Its score gap is at most2r zeta<rt, because both the true top-r projector and P have trace at most r. Thus kappa<=rt is paid without an eigenvalue-gap assumption. Do not substitute an arbitrary approximate effect for this projector.

Implement the nine known Weyl-conjugate projective tests by known basis rotations, a reversible selected-index flag, and unrotation after rejection; retain all registers as required by the received sequential decoder. Approximate circuit implementation contributes its separately assigned complete per-deployment diamond error xi_dep by the ordinary hybrid bound. This budget does not require a source-dependent purification or inverse.

For one fully specified safe choice, take t=nu²p0/(10^9r), kappa<=rt and xi_dep<=nu²p0/10^7. The ideal spectral decoder has delta<=142rt, b<=243delta and acceptance within243delta of p. Adding the deployment error still leaves a>=3p/4 and b/a<nu²/6144 with wide slack. Hence the SAME compiled decoder can be tested by the received learned-throughput holdout at target nu and acceptance floor p0/2. Holdout known preparations/tests may likewise be compiled using its deterministic source cap and a separate transcript confidence budget. The holdout tests the ACTUAL fixed compiled decoder, not an idealized unimplemented one.

No source-copy or accuracy exponent changes: training is O(s²r/(p0nu²)polylogs), with explicit single-copy known-gate operations and the previously charged holdout cost. The collectiveO(sr/(p0nu²)) route remains separate and potentially more query-efficient. Neither rate is asserted to beat every ordinary baseline when r is large. No unitary-covariance/averaged-nu^-1 conclusion is transferred to this discrete estimator, and no matching accuracy lower, hidden-source certification or nonstationary-future guarantee is inferred.
