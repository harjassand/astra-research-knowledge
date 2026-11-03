# Candidate proof: acquired bounded-patch charged Gaussian transport

2026-11-03. **For independent audit.** This proves/constructs a local endpoint-transfer operation from the paid Wilson endpoint estimates, not a collective rotor gap. It avoids the singular Kato denominator and acquires coefficients from a fixed local rule. Constants below are deliberately wasteful. Numerical tests are algebraic diagnostics, not simulations of the astronomical certified slab.

## A. Actual endpoint inputs and additional thickness cost

Use `index_bridge/WILSON_LOW_HIGH_LOCALIZER_TRANSFER.md`, with the compensating root/face orientation so free occupied charge is −s. Ha,Hb are the actual finite-range Wilson matrices, for one fixed bounded local rotor update; V=Ha−Hb is supported on the changed mass-template region S0. Set v=||V||1, bounded by rank(S0)||V||; W is a uniform bound on ||Hi|| from local hopping/onsite norms. These bounds depend on paid UV resolution and the local move, NOT lateral volume. Assume v>0. g=M/10, p is the certified full finite-slab Fermi gap (a fixed fraction of pmin). No interpolation gap is assumed.

The endpoint ledger gives near bare-block spectrum outside ±3M/8, high-block spectrum outside ±399M, free near/far hybridization plus mass coupling <=2M delta, delta=32 b_*^(L−1), b_*=(a Lambda)^2/2. The bare near gap follows already before the high Schur correction from the displayed localizer error bounds.

**Low far weight, operator norm rather than eigenvector-by-eigenvector counting.** Let Pi_low=1{|H|<g}. In the free near/far/high decomposition write X=P_near Pi_low, Y=P_far Pi_low, Z=Q_high Pi_low. Their intertwining equations with H restricted to Pi_low and a Sylvester bound (split positive/negative near spectra) imply

 x <= [2/(3M/8−g)](2M delta+M z),
 z <= [2/(399M−g)]M(x+delta),

where x=||X||, z=||Z|| and ||Y||<=1. Solving gives x+z<=32 delta with room. This uses the operator Sylvester bound ||A X−X B=C|| => ||X||<=2||C||/(G−g) when spec(A) is outside [−G,G], spec(B) inside [−g,g]; derive by splitting A's positive/negative subspaces and semigroup integration. No sqrt(number of low states) factor is introduced.

Here d>=1 is a NUMBER of layers (w=0,...,d-1), not the largest layer index. For a strip of the first d normal layers, the free far singular profiles have norm <=3 sqrt(d+1) b_*^(L−d), including their geometric-profile error. Consequently a conservative bound is

 ||chi_{0<=w<d} Pi_low|| <= eta_d := min(1,1100 sqrt(d+1) b_*^(L−d)),  L>d.

This bound is uniform in lateral volume and arbitrary rotor exterior. If final compiler support reaches depth r, **choose L>r plus the logarithmic buffer below**; the original endpoint-index thickness alone is NOT enough. L can be enlarged without worsening the near/high estimates.

## B. Direct difference acquisition: no full-volume trace error

P_i=1{H_i<0}, Delta=P_a−P_b. Resolvent identity gives

 Delta=(1/pi) integral_0^infinity Herm[(Ha−it)^−1 V (Hb−it)^−1] dt.

For endpoints with low spectral weight <=eta on S0 and full gap p, split each resolvent into |H|<g and |H|>=g. Products touching the low sector carry eta factors BEFORE a p denominator. Direct trace estimates give

 ||Delta||1 <= v[1/(2g)+(2eta/(pi g))(1+asinh(g/p))+eta²/(2p)].

Thus, after choosing eta<=p/[100(v+g)], B:=2+2v/g is a safe volume-independent trace bound. This is charged by v, not dim(slab).

Delete only the resolvent interval [0,tau]. Its error is at most

 E_low <= (v/pi)[tau/g²+(2eta/g)asinh(tau/p)+(pi eta²)/(2p)].

For an intended trace tolerance eta0 in (0,1), choose

 tau=min(g/4, pi eta0 g²/[100(v+g)]),
 eta_S0<=eta0 p/[100(v+g)].

Then E_low<eta0/10 using p<=g and p asinh(tau/p)<=tau. This is the explicit far-face suppression contract. The required extra thickness is logarithmic in p^-1 and eta0^-1, besides compiler depth.

For t>=tau there is no small-p issue. Truncate at T=max(2tau,100v/(pi eta0)); tail trace norm <=v/(pi T). Approximate the remaining integral using a mesh of maximum step h<=pi eta0 tau²/(100v). Since the integrand derivative has trace norm <=2v/t³, quadrature trace error <=h v/(pi tau²). Finite quadrature uses ONLY products Ra V Rb.

At each mesh t approximate R_t(H) by the explicit finite polynomial

 q_t,K(H)=(H+it)/(W²+t²) sum_{j=0}^K [(W²−H²)/(W²+t²)]^j.

Uniform resolvent error is bounded by

 ||q_t,K−R_t|| <= sqrt(W²+T²)/tau² * [W²/(W²+tau²)]^(K+1).

Choose it <= e=min(1/tau, pi eta0 tau/[100vT]). Product trace error is bounded by v(2e/tau+e²), integrated over length <=T. Thus with the allocations above the resulting Hermitian matrix M satisfies

 ||Delta−M||1 <= eta0.

All constants can be tightened, but no bound multiplies a separate projector error by the full slab dimension. Each q_t,K has degree 2K+1, and every q_a V q_b is supported inside that hopping neighborhood of S0. Hence M has finite physical support R and coefficients depending only on a fixed finite rotor stencil. The computation is independent of the actual exterior. R is known before choosing final L; enlarge L to exceed its normal depth and the buffer required in section E. There is no global eigenprojector oracle.

## C. Earned exceptional cutoff, including +/-1 charge modes

Fix desired amplitude error epsilon in (0,1/10). Set

 t=epsilon²/(100B), rmax=ceil((B+1)/t),
 gamma0=t/[4(rmax+1)], eta0=epsilon gamma0/[10^4(rmax+1)].

Acquire M to this eta0 by section B. Its trace norm <=B+eta0. Therefore it has at most rmax eigenvalues with |lambda|>=t. Among the intervals obtained by inserting all computed |lambda(M)| in [t,2t], identify an empty interval of at least the counting-guaranteed width and choose a deterministic FIRST CERTIFIED interval at half that width (scan a rational grid in increasing order, refining arithmetic as needed); choose its midpoint c. Its certified distance to every |lambda(M)| is >=gamma0. Explicit finite rule: scan predetermined centers c_j in [t+gamma0,2t−gamma0] on mesh gamma0/4; compute all |lambda(M)| to certified error <=gamma0/8; select the first center whose approximate distances all exceed 5gamma0/4. A true gap of width4gamma0 guarantees acceptance; actual margin exceeds gamma0. This needs bounded finite precision, not equality/tie decisions. Threshold choice uses M alone, NOT global spectral data.

Let S_R=1{|M|>=c}. Its rank r<=rmax, and it lies inside the physical patch. Since ||Delta−M||<=eta0<<gamma0, the corresponding true spectral projection S=1{|Delta|>=c} has the same rank and a uniform gap at c. Split the positive and negative spectral tails directly: Sylvester separation yields ||S−S_R||<=4 eta0/gamma0 and a finite-rank direct rotation taking S to S_R. Do NOT invoke operator-Lipschitz continuity of absolute value. The independent audit proves these constants. Crucially, NO gap at lambda=+/-1 is required.

Projection algebra gives [P_a,Delta²]=[P_b,Delta²]=0. Thus S reduces both P's. It contains every +/-1 eigenvector, including all unmatched occupied modes. Outside S,

 ||Delta_(Sperp)||HS² <=2t ||Delta||1 <=2tB.

The ranks on Sperp agree. In the principal-angle decomposition the residual Slater overlap is product cos(theta_j), and is >=1−sum sin²(theta_j)>=1−tB. This is where small angles are discarded, with a SUM bound rather than a dimension-times-maximum bound.

## D. Construct the finite charged partial map, with no Kato inverse

Acquire the finite compressed matrices A_i=S_R^* P_i S_R to operator accuracy zeta<=eta0 (section E). They are within O(eta0/gamma0+zeta) of the exact projections obtained by rotating S to S_R. Round each finite matrix at 1/2. Its eigenvalues are near 0 or1; this rounding gap is earned from the subspace estimate, not assumed. Occupied ranks r_a,r_b agree with the true restricted ranks, so r_b−r_a=Tr(P_b−P_a)=−delta s.

Choose deterministic orthonormal occupied and empty bases for each rounded projection. Let Ua,Ub take the standard first r_a or r_b occupied modes to these bases. On the finite Fock space define

 T_R = Gamma(Ub) C_(r_a->r_b) Gamma(Ua)^dagger,

where C explicitly annihilates the unmatched standard occupied modes if r_a>r_b, or creates the missing ones if r_b>r_a. It is a norm-one partial operator, not an invertible transporter. It has EXACT physical free axial charge r_b−r_a. Every orbital is inside R.

The finite-rank rotation used for analysis changes at most 2r modes. Its second-quantized operator differs from identity by O(r eta0/gamma0); rounded finite Slater vectors have the same finite-dimensional error bound. Therefore

 |<Psi_b|T_R|Psi_a>| >=1−tB−C' r(eta0/gamma0+zeta) >=1−epsilon

with the deliberately large 10^4 safety factor above for the elementary finite-rank estimates (the independent audit gives C'<=200). This avoids an inverse square root of I−Delta² entirely; orthogonal principal pairs and rank-changing modes are retained and handled by finite Fock preparation.

The deterministic eigensolver may pick arbitrary bases INSIDE an occupied subspace: those choices change a Slater ray by a phase, but not the norm-one map property or the amplitude bound. All computation is on M and finite compressed data. No conditioning hypothesis on individual occupied eigenvectors is needed.

## E. Acquiring compressed P data and the full support/thickness ledger

Only the r-dimensional compression in D is needed. For smooth Fermi function

 F_sigma(x)=1/2−arctan(x/sigma)/pi,

one has |P(x)−F_sigma(x)|<=sigma/(pi g) on |x|>=g, and <=1 on the remaining low spectrum. If the whole physical support of S_R lies in the first d_R normal layers,

 ||S_R^*(P−F_sigma(H))S_R|| <=sigma/(pi g)+eta_dR².

Choose sigma<=g zeta/4 and eta_dR²<=zeta/4. Approximate F_sigma uniformly by a real finite polynomial to error <=zeta/2, for example via the same finite resolvent-quadrature/geometric-polynomial construction. This is an OPERATOR bound only on the retained finite compression; no full-volume trace conversion occurs. Matrix entries of that polynomial on R depend only on a finite additional hopping buffer. That buffer affects coefficient locality and computational cost; the operator T_R itself remains supported on R.

A sufficient final normal thickness is

 L >= d_R + ceil[log(1100 sqrt(d_R+1)/eta_target)/log(1/b_*)] +1,
 eta_target=min(sqrt(zeta)/2, eta0 p/[100(v+g)]).

This pays both the original changed-support low-frequency response and the entire exceptional-mode support. Because p decreases with lateral size, the thickness has an explicit log(p^-1) addition. The physical support/rotor coefficient stencil remain volume-independent; the far face is kept outside the operator support. The scheme is catastrophically expensive: v itself scales with the astronomical UV volume of one coarse move; K scales at least like (W/tau)^2 times logs, retained-mode count like B²/epsilon², finite Fock operations can be exponential in retained patch dimension. These are FINITE existence resources, not a practical simulation claim. All extra range, body order, precision and slab layers must remain in the final ledger.

## F. Actual decoration, exact symmetries, and real structure

The pairing changes on a bounded closed local Majorana patch. Products of pairing projectors Pdec_a,Pdec_b are rank-one there. Search the finite local Majorana-monomial basis for a nonzero Pdec_b Gamma Pdec_a; completeness guarantees one exists with the needed parity. Normalize this partial rank-one map by its locally computed singular value to norm one. This is an actual decoration computation, not an inverse-decoration oracle. It maps the local paired ground states with unit magnitude and carries axial charge delta s. Multiply it by T_R; total operator is even and exactly axial-neutral.

Apply the unchanged-neighbor anchored rule in `ANCHORED_ACTUAL_SLAB_KERNEL.md` to the whole finite compiler. Integer free vector charges and the explicit barycentric mass covariance make the resulting coefficient rule exactly vector-covariant and individually rotor-periodic. All thresholds/bases are computed in the canonical local slice, so tie choices do not break covariance. The rule is common to every exterior matching its finite stencil, and the amplitude guarantee is uniform under the same endpoint/normal-weight bounds.

The root's fixed real structure for the actual Wilson family permits all difference/compressed matrices and finite surgery to be chosen real in a fixed local Takagi basis. Hermitian real resolvent quadrature or a final real-structure symmetrization preserves error/locality. Anchored vector rotations respect that real structure. Thus the free transfer phase can be reduced to a sign. This does NOT establish cancellation of the decoration sign around closed rotor-move loops.

## G. Executed algebraic test and exact remaining gate

`principal_surgery.py` constructs rank-6 and rank-5 projectors with exact orthogonal principal pairs, a rank-changing unmatched mode, near-orthogonal pairs, and a discarded angle10^-4. It mixes the patch basis generically and then tests controlled leakage outside the patch. The direct Kato denominator has minimum singular magnitude about10^-16. The finite partial surgery nevertheless has norm1 and amplitude .999999995 without leakage, .99999690 at leakage rotation10^-3, and .99976428 at10^-2. These are finite algebraic checks, not Wilson-slab simulations.

Remaining audit targets: operator low-far Sylvester constants against the precise endpoint decomposition; cutoff perturbation constants C,C'; precision termination for deterministic spectral margins; the stated finite projector-rank preservation. The argument's structural inputs and costs are now explicit and locally acquired. Even if all pass, it proves only uniformly nonzero local ENDPOINT transfer. It does not prove that the fluctuating rotor Hamiltonian has a unique symmetric gapped ground, nor remove real sign holonomy, nor justify a global-volume-norm Schrieffer–Wolff argument.

## Independent audit update
See AUDIT_LOCAL_PARTIAL_TRANSPORT.md. Layer-count convention and finite-precision deterministic cutoff selection corrected; C′<=200 verified. A separately audited two-massed-face slab has a true uniform gap M/3, eliminating the one-face low-far suppression machinery if BOTH rotor/decoration faces are retained. It does not automatically give a single-face chiral regulator.
