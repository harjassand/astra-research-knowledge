# Finite-volume rest-parent transfer by global norm

Status: constructive transfer with explicit approximation mechanisms; requires independent audit of the polynomial relative-kernel bookkeeping. This deliberately allows volume-dependent finite interaction range. It does not strengthen the separate uniform-range half-space theorem.

## Inputs and exact comparison operator

Let F contain all far momenta below the static cutoff Lambda=1000M, with complete species, and Q=1-P_F. The compressed static family Q h_near(phi) Q has gap g>=M/4, as proved in COMPRESSED_REST_GAP_INTERFACE.md. The exact canonical construction on Q, with the appropriately doubled fast copies and correctly oriented decorations, gives a unique rest ground and algebraic gap Delta=min(g,1) in its chosen normalization. It does not require spatial locality for this algebraic statement.

Define H_dec=H_F+K_Q, acting on the target Fock factor and the complete rest/rotor factors. H_F is the explicit free far lattice-Weyl Hamiltonian and K_Q the exact canonical rest parent. After subtracting their ground energies, K_Q>=Delta(1-P_ground,Q). The actual physical Hamiltonian to be constructed keeps h_near literally, and approximates ONLY the rest counterterm and dressed-reset coefficients by finite-patch physical formulas.

To compute these coefficients without a projected-state oracle, extend the one-particle operator to

 h_tilde(phi)=Q h_near(phi) Q+mu P_F,

with mu in[g,R_h]. It is uniformly gapped and bounded. Its purification generator splits into a Q part and a CONSTANT F part. In every rotor-reset kernel W_tilde(phi) W_tilde(phi')^*, the F part cancels exactly. Its F ground-energy contribution is also a constant and is subtracted. Thus full-space formulas compute exactly the desired Q parent tensored with identity on F.

## Sign polynomial and global tail budget

Choose R>=max_phi ||h_tilde(phi)||,||h_near(phi)|| and A=h_near/R, A_tilde=h_tilde/R. Put q=1-g²/R². Use

 p_k(A)=sum_{j=0}^k c_j A(1-A²)^j, c_j=binom(2j,j)/4^j.

For the GAPPED A_tilde, the uniform sign error is <=q^(k+1)/(1-q). For the possibly GAPLESS physical A, no sign approximation is asserted; nevertheless ||p_k(A)||<=1 by the scalar partial-binomial identity. Both1-A² and1-A_tilde² are contractions.

Let n be the TOTAL one-particle mode count, including the canonical copies, and n_rot the number of reset centers. Choosing

 eta=q^(k+1)/(1-q) <= epsilon/[C n(R+n_rot+1)]

bounds the total finite-volume reset and energy-counterterm polynomial truncation error by a prescribed fraction of epsilon. This pays the full Fock amplification: second-quantizing a one-particle error eta costs at most 4n eta, and there are n_rot reset terms. Thus k=O((R/g)² log[n(R+n_rot+1)/epsilon]) with the already paid local constants. No infinite bath or rotor trace is used.

## Replacing projected polynomial data by physical data near the interface

For a coordinate patch S at depth at most d, the explicit geometric profiles give

 ||P_F P_S||<=sqrt(dim S) b_*^(L-1-d).

The difference A_tilde-A is a bounded sum of terms containing P_F. A telescoping identity on a near column gives

 ||[p_k(A_tilde)-p_k(A)]P_S||
 <=C(k+1)² sqrt(dim S_expanded) b_*^(L-1-d-2k-2),

where S_expanded is the physical hopping neighborhood of radius2k+2. This has NO exponential binomial-coefficient cost: telescope A(1-A²)^j as a grouped product and use that both quadratic factors are contractions. Physical powers have exact finite walk support.

For reset kernels one needs relative, rather than absolute, Gaussian unitaries. If phi and phi' differ at one rotor, the physical polynomial generator difference has support in a patch of radius O(k) around that rotor. Its rank and trace norm are polynomial in k and the fixed local orbital count. Apply the same grouped telescoping identities to this generator difference and to its finite-time interaction-picture evolution. Every discrepancy term contains a P_F adjoining a finite physical walk from that patch. Trace norm costs the rank of the expanded patch, not the whole Fock dimension. The resulting bound is a computable polynomial in k, propagation order J and patch orbital count, multiplied by b_*^(L-1-d-CkJ).

The scalar counterterm must be compared AFTER subtracting a fixed-texture reference. Far contributions independent of phi then cancel. Telescoping between phi and that reference anchors each trace difference at the physical near mass; cyclicity and the same grouped-product bounds give a polynomial(k) times near-strip volume times the same geometric leakage factor. The reference contributes only an irrelevant scalar, not an energy oracle.

## Explicit finite-patch Gaussian computation

The physical polynomial generator has one-particle norm bounded by a constant and range O(k). Its relative reset generator is supported in an O(k) patch. Finite-time Gaussian propagation can be restricted to a patch of radius

 R_patch=C k(J+1)

with trace-norm error bounded by C d_patch times C0^J/J!, by the matrix-exponential Taylor remainder and finite walk support. Duhamel transfers this trace-norm error to the norm of the second-quantized relative unitary. Choose J=O(log[n_rot/epsilon]) conservatively. Each reset kernel is now obtained from finite fermionic matrices and the rotor coordinates in that finite stencil. No inverse, Gibbs state or interface response is supplied.

The counterterm uses finite polynomial traces and has radius O(k). Exact symmetry twirling, as already acquired, does not increase approximation norm and enlarges support only by the fixed symmetry-circuit radius. Keep the original free hopping and near mass EXACT.

A conservative range ledger is R_patch=O(log²[n/epsilon]) times the fixed gap/norm constants, not an unproved O(log n) claim. This is finite range for every finite device, but not uniform in volume.

## Global norm and slab thickness

There are O(n_rot) bounded reset terms and O(N R_patch) anchored scalar densities. Let C_poly(k,J) be the explicit polynomial prefactor obtained by the finite telescoping/rank count above, including local orbital multiplicities. Choose all polynomial/tail budgets to sum to at most epsilon/2, and impose

 C_poly(k,J) N b_*^(L-1-R_patch) +2r b_*^L/a <= epsilon/2.

The second term is the already audited full-Fock free leakage. Thus a sufficient separation is

 L >= R_patch+1+O(log[C_poly(k,J)N(1+r/a)/epsilon]/|log b_*|).

The finite-matrix algorithms and finite sums make C_poly certifiable; its precise constant bookkeeping remains the independent audit point. The scaling is polylogarithmic thickness/range for fixed physical endpoint resources. No local-stability theorem on a non-tensor Q algebra is invoked.

The resulting actual physical Hamiltonian H_phys obeys the global bound

 ||H_phys-(H_F+K_Q)||<=epsilon.

This is the desired rest-gap transfer if the coefficient bookkeeping is certified. All rotor factors can remain infinite dimensional because the construction and errors concern bounded operator kernels. Finite rotor dimension is a separate paid step.

## Low-energy consequence, with correct multiplicity language

Take epsilon<Delta/8. After ground-energy alignment, the only comparison states below Delta are free Fock excitations of H_F tensored with the unique rest ground. The actual spectrum lies within epsilon of that comparison spectrum before alignment (within2epsilon after aligning ground energies).

For any energy cutoff E_cut<Delta-epsilon whose distance from the comparison spectrum exceeds epsilon, the actual spectral projection below E_cut has the SAME rank as the free-Fock target projection, by the gap-preserving bounded-perturbation homotopy. This remains meaningful with infinite rotor Hilbert factors: the comparison subspace below Delta is finite dimensional because F has finitely many fermionic modes. It proves absence of additional low rest states at the charged resolution.

Do not promise a gap between every free many-body level. Resolving exponentially dense target-Fock levels may demand exponentially small epsilon; the stated resource formulas then charge log(1/epsilon). Enumerating all2^r target states is not a polynomial classical computation.

The actual canonical device has two same-chirality fast copies, so its exposed species multiplicity is doubled relative to the original four-Weyl construction. No copy removal or gauged-continuum claim follows.

## Explicit replacement for the unspecified coefficient prefactor

A crude monomial ledger avoids needing the sharper polynomial(k,J) estimate above. It is a bound for proof certification, not an instruction to enumerate exponentially many walks.

Let n include every fast-copy one-particle mode, n_rot every reset center, and R>=1 bound the normalized-energy scale. Choose k so

 q^(k+1)/(1-q)<=epsilon/[1000n(n_rot+R+1)].

Set B=4^(k+2); this safely bounds the monomial coefficient l1 norm of the canonical one-particle Gaussian generator built as(pi/4) times the off-diagonal p_k(A) sign/covariance block, including its fixed copy matrices. Its OPERATOR norm is still bounded by a fixed constant (at mostpi/4), since ||p_k(A)||<=1. Choose J>=1 so

 8 exp(2pi) (2pi)^(J+1)/(J+1)! <=epsilon/[1000n(n_rot+1)].

Define D=2(2k+1)(J+1), plus the fixed input interaction/texture stencil radius where applicable.

For each rotor reset, use the truncated relative one-particle kernel

 I+T_J(G_phi)T_J(-G_phi')-T_J(G_phi)T_J(-G_phi),
 T_J(G)=sum_{j=0}^J G^j/j!.

Subtracting the equal-configuration baseline is essential. Every remaining monomial contains the local difference of the underlying mass matrices. The degree is at mostD, and coefficient l1 norm is bounded by4(J+1)^2 B^(2J). The exact relative Gaussian unitary differs from this expression by the displayed factorial tail, uniformly on the one-particle space.

A physical patch containing every D-step walk from the changed rotor stencil gives EXACTLY the same truncated relative expression as the full physical matrix, extended by identity outside. Therefore the exact full physical relative unitary and exact finite-patch relative unitary differ only by twice the factorial tail. Passing to Fock space multiplies the one-particle norm error by at most4n, using the principal-log Gaussian-lift argument below (or the sharper exterior-product bound for number-conserving blocks). No second quantization of a nonunitary Taylor polynomial is performed.

For projected versus physical relative polynomials, take a mixed telescoping difference: each discrepancy contains both a near mass change and at least one P_F. Select the P_F nearest that near insertion in the telescoping order. The intervening physical contractions have walk length at mostD; every other factor has norm at most1. The profile bound then supplies at mostC sqrt(n)b_*^(L-1-D) per discrepancy, with at mostC(D+1)^2 insertion choices. The same mixed telescoping works for the counterterm AFTER its fixed-texture scalar subtraction; cyclicity anchors its trace at the near insertion. One trace/Fock conversion costs at most another factorn.

A deliberately oversized explicit common amplification is

 A_cert=10000(n+n_rot+1)^4(R+1)(D+1)^4(J+1)^4 B^(2J+2).

It covers term counting, mixed telescoping, local rank, trace/Fock amplification and the scalar energy coefficient. Require

 A_cert b_*^(L-1-D) <=epsilon/4,
 2r b_*^L/a<=epsilon/4.

Together with the sign and factorial budgets this yields the requested global comparison norm <=epsilon, with the displayed factor10000 covering the fixed canonical-copy and Gaussian-lift constants. Here n counts all physical fermionic modes, including decoration and canonical copies, and the Majorana dimension is2n.

Although A_cert can be quasipolynomial in volume, log A_cert=O(kJ+log n+log R). It is used ONLY to select thickness and arithmetic precision. The actual finite-patch formulas use polynomial evaluation and finite Gaussian matrix exponentials, never monomial enumeration. Consequently the paid radius and thickness remain O(log²(n/epsilon)) with fixed endpoint norm/gap constants. The implicit n=O(NL) dependence can be resolved by increasing an explicit trial L until the displayed elementary inequalities hold, or by a conservative squared-log upper bound; this is a deterministic scalar resource check, not a physical-state oracle.

### Numerical size of the inherited constants

The asymptotic squared-log range must not conceal the existing UV constants. With aM=10^-6, R_h=10/a+M and compressed gap g=M/4, one has R_h/g about4*10^7. The elementary binomial sign degree is therefore approximately1.6*10^15 times log[n(R+n_rot+1)/epsilon], before the additional Gaussian Taylor order multiplies the patch radius. This is an existence-scale finite construction, not a practical solver or device specification. No numerical dense simulation is proposed.

Energy-zero clarification: the implemented scalar counterterm approximates the reference-subtracted function E0(phi)-E0(phi_ref). The exact reference E0(phi_ref) need not be computed or supplied. Accordingly the global norm comparison is understood after adding one rotor-independent scalar C_ref to H_F+K_Q. This scalar changes neither dynamics nor gaps nor relative low-energy counts. It is not an unimplemented state-dependent counterterm or a ground-energy oracle.


## Gaussian-lift phase certificate (including superconducting decorations)

The exterior-tensor bound applies directly only to number-conserving blocks. For the general Majorana/BdG canonical parent, use the actual canonical one-body generator K=(pi/4) times its off-diagonal sign/covariance matrix. Every exact, polynomial and physical-patch generator has norm<=pi/4 because the exact sign and the partial polynomial both have norm<=1.

The relative path O(t)=exp(t K_phi)exp(-t K_phi_prime),0<=t<=1, has one-body eigenangles of absolute value at mostpi/2 by its operator-norm path length. It stays in the principal-log neighborhood of SO, never touching eigenvalue-1. The exponential-defined many-body Spin lift therefore agrees with the continuous principal-log lift starting at identity. This fixes the double-cover sign even across discontinuous changes of rotor configuration: t parametrizes the explicit Gaussian products, not a path in rotor space.

For O,O_prime in that neighborhood, the principal-log integral gives

 ||log O-log O_prime||
 <=||O-O_prime|| integral_0^infinity ds/(1+s²)
 =(pi/2)||O-O_prime||.

Indeed each normal matrix O has spectrum on the unit circle with nonnegative real part, so ||(O+sI)^-1||<=1/sqrt(1+s²). The quadratic Majorana lift of an antisymmetric logarithm has norm bounded conservatively by its Majorana dimension times the logarithm norm. Since there are2n Majoranas, unitary Duhamel yields a many-body lift difference <=pi n||O-O_prime||, safely<=4n times the one-body error. The explicit error budgets and A_cert above include this factor.

No scalar Berry phase, Spin sign, or second quantization of a nonunitary truncated exponential is left as an oracle.

Canonical-copy compatibility: for the rest-parent construction, the removed momentum ball includes both k and-k and complete spin/flavor multiplets. The second canonical copy uses the conjugate/onsite-real-structure transported projector, and the Nambu/Majorana extension includes the corresponding conjugate hole subspace. Thus Q is a valid fixed CAR/BdG subspace for the canonical doubling and all F factors cancel consistently. An arbitrary nonsymmetric probe band may still be used in the response-only lemma, but it is not substituted unchanged into this rest-parent construction.

Dummy-gap convention: the formula +mu P_F is written in the number-conserving Wilson block. In a redundant BdG matrix it means the compatible particle/hole pair diag(+mu P_F,-mu P_F^*), or the equivalent fixed Majorana complex structure on F, not an identity shift that violates particle-hole symmetry. The block is independent of phi, has magnitude mu, and its canonical factor cancels from relative reset kernels. All norm/profile estimates are unchanged.

Fast-gap normalization: if decoration blocks are included in the common sign polynomial, use g_fast=min(M/4,Delta_dec), where Delta_dec is their actual static gap, and enlarge R to include their norm. All q, k and Delta formulas use this g_fast; M/4 alone is the Wilson-rest gap. Equivalently the finite local decoration generator may be handled exactly and separately. The quoted R_h/g≈4*10^7 example assumes the decoration does not lower the chosen common gap; otherwise the displayed general formulas charge the larger ratio.

Additional fast-term leakage (independent audit correction): the actual fast matrix is h_free+V_near, whereas the comparison fast matrix is h_F+Q(h_free+V_near)Q. Besides the free residual2r b_*^L/a, one must include V_near-QV_nearQ. Since V_near is physically supported on the near boundary and ||V_near||<=M,

 ||dGamma(V_near-QV_nearQ)||<=3 n^(3/2) M b_*^(L-1).

This conservative bound uses ||P_F P_boundary||<=sqrt(n)b_*^(L-1) and the full-Fock trace-norm factor n. It is explicitly included in A_cert b_*^(L-1-D), since R>=M, D>=0 and the displayed A_cert dominates3n^(3/2)M. Thus the total fast comparison is the sum of this near-mass leakage and the separately displayed free residual; it is not the free residual alone.

Independent audit has checked the outward mixed telescoping, anchored reference-subtracted scalar trace, and principal-log Spin-lift repair. The mixed telescope starts by replacing Q Delta A Q by Delta A, then replaces factors nearest that insertion outward, ensuring the segment between each P_F and the local mass change is a physical finite walk.

Finite-device ground uniqueness is a separate precision choice: the free far band has smallest excitation p_min,lattice>0 under the AP spin structure. Global comparison gives a unique device ground and gap at least min(Delta,p_min,lattice)-2epsilon only when epsilon<min(Delta,p_min,lattice)/2; choosing one quarter is a safe margin. No volume-independent full-device gap is claimed. The weaker epsilon<Delta/8 condition controls absence of additional rest states without resolving every small far-band level.

Lift normalization: the canonical generator is the explicitly fixed pure quadratic off-copy generator, with no independently chosen phi-dependent scalar phase. Its off-copy one-body matrix has zero trace, so the number-conserving normal-ordering scalar vanishes. The Majorana version is its specified bilinear exponential. The principal-log argument compares these canonical lifts; it would not justify arbitrary Gaussian implementers multiplied by unknown scalar phases.

Final audit status: AUDIT_GLOBAL_NORM_REST_TRANSFER.md passes the corrected finite-volume construction. Its former integration warning is addressed by the separately derived NEW rest-gap/Fourier-cutoff comparison in FINITE_AUXILIARY_CHIRAL_DEVICE_INTEGRATION.md and FINITE_AUXILIARY_REST_COMPATIBILITY.md; no unchanged-old-spectrum assertion is made.
