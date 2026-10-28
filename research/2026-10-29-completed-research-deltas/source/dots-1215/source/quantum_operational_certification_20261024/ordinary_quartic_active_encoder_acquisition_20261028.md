# Active ordinary acquisition of the exact-correctability quartic

28 October 2026. **New proof candidate; independent receiving pending.** This is a positive active-encoder theorem for a smaller decision invariant, not a proof of generic relative-optimal recovery. Its physically ordinary inputs use a collective receiver measurement on retained outputs. Independent pairwise swap tests are NOT an implementation of the estimator.

## 1. Decision invariant and imported local measurement

For the supplied four-real-coordinate quaternion encoder x in S^3, let J_x be the normalized qubit-input source Choi state, rho_x its output marginal, and let the physically ordinary six-state loss density be

    T_x = (2 rho_x tensor I_2 - J_x)/3.

One copy is prepared by choosing one of six Pauli pure states P uniformly, querying the encoded source once, and attaching the receiver-local qubit (I-P)^T. The classical P label is then discarded. All source calls count. No reference or encoder selector is coherent through the source.

Define

    D(x) = 24 Tr(rho_x^2) - 36 Tr(T_x^2)
         = 8 Tr(rho_x^2) - 4 Tr(J_x^2)
         = 12 Tr(T_x J_x).                                      (1)

Both T_x and J_x are positive trace-one matrices, so 0<=D(x)<=B with B=12. It is a homogeneous real quartic in four variables and has at most d=35 monomial coefficients. This is a representation of one scalar decision invariant, NOT a positive Choi-completion estimator.

Let K_ab(x)=E_x^c(|a><b|) for any Stinespring complement. Then

    D(x)=||K_00-K_11||_F^2 + 4||K_01||_F^2.                     (2)

Consequently D(x)=0 iff E_x is exactly correctable by a full CPTP receiver. The environment is not measured or supplied by (2).

The companion `ordinary_correctability_quartic_ustat_20261028_independent_audit.md` derives this ordinary-source collective-output estimator using the established quantum U-statistic/Casimir method. On n>=2 iid T_x copies, measure

    U_n = [24 sum_{a<b} Swap_B(a,b)
           -36 sum_{a<b} Swap_(BA)(a,b)] / binom(n,2).           (3)

The two Casimir sums commute. Nondemolition weak Schur measurements on the B systems and then BA systems yield (3); alternatively known-swap Hamiltonian simulation/phase estimation implements its spectral measurement. The source is never inverted or controlled. The receiver must retain all n output systems and local reference qubits. Gates, memory, swap control, arithmetic and measurement accuracy are paid. A direct implementation uses swaps on the physical outputs and does not need to learn a support basis or retain an encoder-dependent frame during this pilot.

The key bounds are

    E U_n=D(x),
    Var(U_n) <= 48 D(x)/n + 2016/[n(n-1)].                     (4)

Indeed the two-copy kernel H=24 Swap_B-36 Swap_(BA) has first contraction 12J_x>=0, and E H^2=1008 because Tr_B T_x=I_2/2. At D=0 the variance is exactly 2016/[n(n-1)], not a constant divided by n. This degeneracy is why ordinary signed independent-pair swaps would lose the rate.

The remainder of this note proves an ACTIVE GLOBAL encoder consequence of (4). It never assumes that fixed-anchor interpolation preserves near-boundary accuracy.

## 2. Finite quartic action list and known design

Fix 0<gamma<=1, 0<epsilon_D<=1, 0<beta<1. Choose a classical finite quaternion list X containing a chord-h net with

    h^2 <= epsilon_D/(4096 B).

Also include the 35 normalized vectors proportional to integer multi-indices alpha in N^4 with |alpha|=4. Their homogeneous-quartic evaluation matrix is nonsingular; these fixed rational-feature points give a known spanning set. For a normalized rational vector, every degree-four monomial is rational. Let a(x) in R^35 be its ordinary monomial vector, so D(x)=theta^T a(x) for unknown theta. No coefficient observation is assumed.

The list cardinality is polynomial in 1/epsilon_D. Its size appears only in classical scanning/design arithmetic and confidence logarithms, not as a source-query multiplier. Exact feature rank is 35; no small numerical singular value is discarded.

At a stage with known positive numbers u_x, choose a probability design pi with

    V=sum_x pi_x a(x)a(x)^T/u_x,
    a(x)^T V^{-1} a(x) <= L u_x,       L=4d=140.               (5)

The received determinant-increasing G-optimal design construction supplies (5), starting from the known uniform list and stopping with slack. This uses only known features and current classical envelopes. It does not query the source while scanning encoders.

Now COMPRESS this known covariance: solve the finite linear constraints

    sum_x w_x a(x)a(x)^T/u_x = V,
    sum_x w_x=1, w_x>=0.

A basic feasible solution has at most

    S=d(d+1)/2+1=631                                         (6)

nonzero weights. The covariance and every leverage inequality in (5) are unchanged. This is ordinary Caratheodory/linear-program support reduction in a fixed-dimensional real vector space, not compression of an unknown quantum state. The arithmetic is rational once the envelopes are rational. Only these <=S selected encoders receive physical queries at this stage.

## 3. Dyadic confidence-envelope algorithm

Set

    t=gamma epsilon_D/16,
    J=ceil(log_2(B/t)),  tau_j=B 2^{-j},
    U_x^0=B.

At stage j set u_x=U_x^{j-1}+tau_j and form/compress (5). At EACH support encoder x, take b independent batches, with b the SMALLEST odd integer satisfying

    b >= 8 log(2 S J/beta),
    n_j=max(2, ceil[2^18 L/tau_j]) copies per batch.           (7)

Each batch measures the collective observable (3). Let y_x be the median of its b outcomes. Form the raw linear estimate

    theta_hat = V^{-1} sum_{x in support} w_x a(x)y_x/u_x,
    Dhat_z=a(z)^T theta_hat  for ALL z in X.                  (8)

This estimate can be signed; it is not declared a physical state or nonnegative polynomial. Define e_z=(1/8)sqrt(tau_j u_z) and update

    U_z^j = min(B, max(tau_j, Dhat_z+e_z)).                   (9)

The exact-real display is for analysis. A finite rational variant is given below. Finally output a minimizer of the last raw Dhat on X.

### Conditional batch and interpolation proof

Suppose prior stages are good, so

    D_x<=U_x^{j-1}<=2D_x+2tau_{j-1}.

Then D_x<=u_x and u_x>=tau_j. Equation (4), n_j>=2^18 L/tau_j and n_j(n_j-1)>=n_j^2/2 give

    Var(U_(n_j)) <= tau_j u_x
          [48/(2^18 L)+4032/(2^36 L^2)].

At radius r_x=sqrt(tau_j u_x)/(16sqrt(L)), Chebyshev therefore gives a bad-batch probability at most

    48/1024 +4032/(2^28 L) <1/16.                            (10)

Independent-batch median amplification and (7) make

    |y_x-D_x| <= sqrt(tau_j u_x)/(16sqrt(L))                  (11)

simultaneous over all queried encoders and all adaptive stages except probability beta. This is a conditional argument on every previous good history; x, u, pi and the compressed support may all depend on earlier outcomes. A union bound over at most SJ support locations, not all decoder policies, is sufficient.

The deterministic weighted interpolation is the crucial step. For any z in X, (8), Cauchy-Schwarz and (5) imply

    |Dhat_z-D_z|
    <= sqrt(a(z)^T V^{-1} a(z))
       sqrt(sum_x w_x (y_x-D_x)^2/u_x)
    <= (1/16) sqrt(tau_j u_z).                              (12)

The support estimates therefore imply simultaneous whole-menu confidence without paying for every menu point or imposing a universal sup/average Bures inequality.

Since u_z<=2D_z+5tau_j, the update has

    D_z<=U_z^j<=2D_z+2tau_j.

For the upper bound, its excess is at most (3/16)sqrt(tau_j u_z), strictly smaller than the received (1/4)sqrt(2tau_j D_z+5tau_j^2) envelope allowance. This closes induction. The stronger raw constant 1/16 also implies the previously proved 1/8 final-error bound. Empirical minimization and Young's inequality give

    D(x_selected) <= (1+gamma/2) min_(x in X) D(x)
                         +tau_J/gamma.                     (13)

This imports only the final scalar inequality from the received nonnegative-design proof; the acquisition and variance argument here are different and explicitly proved above.

### Continuous-encoder comparator

Along any great circle, D is a trigonometric polynomial of degree at most four, with frequencies 0, +/-2, +/-4. Every Fourier coefficient has modulus <=B, so |D''|<=40B. At a global minimum on S^3 the tangent first derivative vanishes. A chord-h nearby grid point has angle <=2h (h<=1), hence

    min_X D <= min_(S^3) D +80B h^2
            <= D_* +5epsilon_D/256.                        (14)

Combining (13), tau_J<=t, gamma<=1 and (14) yields, with ample slack,

    D(x_selected) <= (1+gamma)D_* +epsilon_D.                (15)

No strong convexity, isolated minimizer, eigenvalue gap, or quadratic stability of a global interpolation is assumed. Flat valleys and weak quartic selectors are included. SOS Gram uniqueness is not required.

## 4. Deterministic source cap and finite processing

There are at most SJ distinct stage support locations, with b homogeneous collective batches each. Since tau_J>=t/2 and sum_j 1/tau_j<2/tau_J,

    N_pilot <= S b [J+2^20 L/t]
            <= S b [J+2^24 L/(gamma epsilon_D)]
            = O_tilde(1/(gamma epsilon_D)).                 (16)

Here d=35, S=631 and L=140 are fixed constants. They are large, and the displayed constants are deliberately conservative. Equation (16) counts EVERY source call, not only favorable receiver outcomes. The number of selected encoder locations is O(log(1/(gamma epsilon_D))); b supplies the stated confidence amplification. This is a theorem about the quartic estimator, NOT a bound on the number of full loss-state Bures matrix queries.

Finite rational implementation does not require a favorable unknown source condition number. Clip envelopes to [tau_j,B] on every history, and round them upward to mesh tau_j/64. In (9), use a rational upper approximation to e_z within tau_j/64, then round the resulting envelope upward once to that mesh. The two upward errors total at most tau_j/32. With raw error (12), the total upper excess is at most

    (3/16)sqrt(tau_j u_z)+tau_j/32
       <=(7/32)sqrt(tau_j u_z),

still below the 1/4 invariant allowance. The lower bound is preserved by clipping because D<=B. The exact raw estimate (8) is rational when ideal Casimir eigenvalues are read: they are integer contents combinations divided by binom(n,2). Current u has polynomial bit length; it is not a recursively accumulating irrational estimate.

The fixed 35 spanning anchors bound the uniform-design minimum eigenvalue below by c/(B|X|) for a known fixed c>0. Determinant updates retain a polynomial fraction of the initial weight after O(d log|X|) steps. Their inverse conditioning is consequently polynomial in |X| and 1/t on ALL clipped histories. LP support reduction preserves the same V exactly. Rational basic solutions have polynomial bit length because the equality dimension is fixed. Scanning, inverses, LP reduction, envelope rounding, and final selection are polynomial in 1/epsilon_D, 1/gamma, log(1/beta), plus paid physical controls.

For FINAL probability beta, run the ideal statistics at beta/2 and budget the WHOLE adaptive physical/measurement transcript discrepancy at unhalved diamond <=beta (TV<=beta/2). Finite eigenvalue readout, known swap/Casimir measurement, ordinary preparation and encoder controls, seed generation, reset error and stored-output memory belong in this ledger. A phase-estimation misidentification budget can instead be allocated directly across the deterministic number of batches. The maximum simultaneous bank is n_J physical outputs plus local qubits and actual implementation workspace. The gate/memory statement is theoretical polynomial scaling, not practical constants or a count-only experiment.

## 5. What this gives for actual full-CPTP recovery

Let ell_opt(x) be optimal entanglement infidelity over ALL CPTP decoders at x, and let R bound encoded Choi rank. Use ROOT fidelity f(A,B)=||sqrt(A)sqrt(B)||_1; Bell/entanglement fidelity is its SQUARE in the decoupling identity below. The established recovery/complement duality is due to Uhlmann-type purification arguments; see Bény and Oreshkov, [General conditions for approximate quantum error correction and near-optimal recovery channels](https://arxiv.org/abs/0907.5391). That paper proves a stronger worst-case channel theorem. Here only the following fixed maximally entangled input specialization is needed, and its constants are derived explicitly.

Take a Stinespring dilation and its pure half-Bell state |Psi>_ABE. Put Omega_AE=Tr_B|Psi><Psi| and sigma_E=Tr_A Omega. Uhlmann's theorem gives

    1-ell_opt = max_(sigma'_E density) f(Omega_AE,
                                      I_A/2 tensor sigma'_E)^2.

Indeed a decoder isometry B->A'F followed by discarding F is a full CPTP decoder. Its Bell overlap is the squared norm of the projection onto |Phi>_AA'; equivalently maximize its squared overlap with |Phi>_AA' tensor |xi>_EF over unit |xi>. Reversing these two maxima and applying Uhlmann yields the displayed identity, with an arbitrarily enlarged known decoder ancilla if required. It proves receiver EXISTENCE only; the final ordinary learner below acquires that receiver without accessing E.

Define Delta=Omega-I_A/2 tensor sigma_E. In complementary blocks,

    Delta=(1/4)[[K00-K11, 2K01], [2K10, K11-K00]],
    ||Delta||_F^2=D/8.

Omega is supported on A tensor supp(sigma_E), whose dimension is at most 2R. Thus ||Delta||_1<=sqrt(2R)||Delta||_F=sqrt(RD)/2. Choosing sigma'=sigma_E in Uhlmann and using 1-f<=||Delta||_1/2 gives ell_opt<=1-f^2<=||Delta||_1.

For the converse, choose an optimizing sigma' and write Delta'=Omega-I_A/2 tensor sigma'. The map P(X)=X-I_A/2 tensor Tr_A X is an ORTHOGONAL projection in Hilbert–Schmidt inner product, and P(Delta')=Delta. Hence

    D=8||Delta||_F^2 <=8||Delta'||_1^2<=32 ell_opt.

The last inequality is the usual purification/trace-distance bound ||A-B||_1<=2sqrt(1-f(A,B)^2). Together these prove

    D(x)/32 <= ell_opt(x) <= sqrt(R D(x))/2.                 (17)

The lower constant is a safe trace/Frobenius bound, not an equivalence of relative objectives.

For the conditioned estimate assume sigma_E has positive eigenvalues at least mu. Restrict everything to A tensor supp(sigma_E), so tau=I_A/2 tensor sigma_E is strictly positive with lambda_min(tau)>=mu/2. Let Q=sqrt(Omega)-sqrt(tau). The Sylvester identity

    sqrt(Omega) Q + Q sqrt(tau)=Delta

has singular-value denominator at least sqrt(mu/2) in the left/right eigenbases, so ||Q||_F^2<=2||Delta||_F^2/mu. Since f(Omega,tau)>=Tr(sqrt(Omega)sqrt(tau)), we have 1-f<=||Q||_F^2/2. Consequently

    ell_opt <=1-f^2<=2(1-f)<=D/(4mu).                        (18)

This is an explicit elementary bound, so no unproved noncommutative chi-square inequality or squaredproducer-workspace/root-fidelity convention is hidden.

The relevant marginal is sigma_E=E_x^c(I_2/2), whose positive eigenvalues are exactly those of J_x. It is NOT the output marginal rho_x. A uniform positive floor on a connected encoder sphere forces constant Choi rank by continuity; rank-changing families are excluded, and the floor is not a harmless technical assumption. Restriction to its support handles zeros; the entire complementary Choi state lies in A tensor supp(sigma_E).

A genuine conditioned zero-optimum consequence follows. Assume:

1. Some encoder is perfectly correctable, so min_x ell_opt(x)=D_*=0.
2. For EVERY candidate encoder, every positive eigenvalue of J_x is at least a KNOWN mu. A generic rank bound alone does not imply this.

Run (15) with gamma=1 and epsilon_D=mu epsilon/2. On its good event, the selected encoder has ell_opt<=epsilon/8. A fresh fixed-encoder ordinary Bures/full-CPTP learner at that encoder then produces the actual receiver; it is not inferred merely from small D. Its source cost is O_tilde(R^2/epsilon), with the received same-frame finite-horizon convention. Total calibration scales as

    O_tilde(1/(mu epsilon) + R^2/epsilon).                  (19)

Thus mu^{-1}=O(R^2) gives the desired rank-squared exponent in this explicitly conditioned PERFECT-ENCODER subclass. If mu is of order 1/R, the encoder pilot is smaller than the final receiver acquisition. A known exact decoder or a known optimal encoder is not supplied.

For an entirely clean averaged operational corollary, give the pilot failure budget epsilon/8. On good records ell_opt<=epsilon/8; on bad records ell_opt<=1. Hence E ell_opt<=epsilon/4. Use the received fixed-encoder learner with relative factor 2 and additive epsilon/4, yielding averaged loss <=3epsilon/4; reserve epsilon/4 for the full finite-operation discrepancy. One future payload uses the selected encoder and the actual learned retained-frame decoder. The pilot can discard its own stored quantum banks after measurement. No classical description of a virtual decoder is applied to an unaligned payload.

Without the eigenvalue-floor promise, (17) still gives a scoped zero-optimum construction: take epsilon_D=epsilon^2/(64R), which ensures ell_opt<=epsilon/16 on the good event, at pilot cost O_tilde(R/epsilon^2), plus O_tilde(R^2/epsilon) final receiver calls. This removes the physical encoder-grid multiplier but does NOT attain the requested generic epsilon exponent.

For a nonzero comparator ell_*, minimizing D cannot simply be promoted to a (1+gamma)ell_*+epsilon theorem. Bounds (17)-(18) do not preserve that comparator, and no acquired spectral floor or favorable rank profile is assumed. The generic relative-risk acquisition target remains OPEN. The square-root conversion loss is real: for a qubit erasure channel with erasure probability p, D=6p^2 while ell_opt=3p/4. Its intrinsic flag supplies a faster task-relevant ordinary route than inferring p from a uniform additive D estimate. The scalar invariant is not automatically the best acquisition target for rare flagged sectors.

### Nontrivial constant-rank/floor example

Use the ordinary Bell-sector realization V_x|psi>=|x> tensor |psi> in C^4 tensor C^2. Let S be an unknown real symmetric orthogonal 4-by-4 involution with both positive and negative eigenspaces. Let W be an unknown output unitary. The stationary source is

    N(omega)=W [omega+(S tensor Z) omega (S tensor Z)] W^*/2.

For every x the two encoded normalized Choi vectors are orthogonal: their inner product is (x^T S x) Tr(Z)/2=0. Thus every J_x has EXACTLY two eigenvalues 1/2, including all perfect encoder locations; R=2 and mu=1/2 uniformly. Nevertheless

    D(x)=2(x^T S x)^2,

so perfect encoding requires the unknown balance condition x^T S x=0. At an eigenvector of S the encoded logical channel is uncorrectable dephasing. A balanced vector makes the two error sectors orthogonal and permits a perfect full-CPTP decoder, but the unknown W means that decoder is not supplied. This is a genuine unknown unflagged recovery family, not auxiliary-only information with a common known perfect receiver. An equally informed conventional learner can of course use the same invariant or learn S/W by another paid method.

## 6. Comparison and exact scope

Quantum U-statistic degeneration, transposition-sum observables, and efficient weak-Schur measurement are established ingredients, not inventions here. In particular, Badescu, O'Donnell and Wright, [Quantum state certification (2017)](https://www.cs.utexas.edu/~wright/papers/state-certification.pdf), Sections 7.2–7.3 (Proposition 7.9 and Theorems 7.10, 7.13), develop commuting-transposition-sum measurements and a variance bound of the form n^-2 plus squared Hilbert–Schmidt distance/n. The present scoped derivation is the inaccessible-complement correctability defect expressed on the physically ordinary loss density, its positive contraction 12J, and its composition with the explicitly paid encoder design. This citation is not a priority claim for that composition.

The strongest equally informed conventional learner may use this SAME ordinary preparation, collective Casimir/U-statistic measurement, adaptive quartic design and final recovery SDP. The construction is itself such a conventional active learner; no quantum-versus-conventional sample advantage is asserted. It improves the internal statistical mechanism over independent pairwise swap estimation, not over an equally capable collective-output baseline.

The sparse-kernel matrix-confidence obstruction in `ordinary_sparse_kernel_matrix_query_obstruction_20261028.md` remains consistent: that fixture has D=0 at EVERY encoder and is solved immediately at the policy level. This quartic learner does not reconstruct its irrelevant auxiliary state family or require uniform confidence for deliberately bad decoders.

**Established in this candidate note:** an explicit logarithmic-count active encoder design and O_tilde(1/(gamma epsilon_D)) ordinary source cap for the nonnegative quartic D; a conditioned zero-optimum full-CPTP recovery corollary; and an unconditioned zero-optimum fallback at O_tilde(R/epsilon^2+R^2/epsilon).

**Not established:** generic relative-optimal recovery at R^2/(gamma epsilon), a learned/automatic Choi spectral floor, hardware execution, small-memory receiver, count-only measurements, or an advantage over the equally informed adaptive conventional method. No external publication or push occurred.
