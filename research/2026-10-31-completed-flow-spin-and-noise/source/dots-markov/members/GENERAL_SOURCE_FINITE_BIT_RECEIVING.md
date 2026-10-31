# General explicit Markov source: complete finite-bit receiving candidate

31 October 2026. Frozen candidate for joint independent review. This is a mathematical-existence construction, not an implemented simulator, practical gate advantage, black-box fast-forwarding result or novelty claim. It leaves the released independent-telegraph theorem unchanged.

## 0. Exact premises and local sources

Receive `PURE_STATIONARY_COMPLETION_AND_ACTIVITY_BOUND.md` (6,417 bytes, SHA256 e5bd50e302be281314e030c61a1cba8463223a2f8c71125e4fd7192fc3e716bf), with the accepted independent review and binding correction: c is the gap of C0 on psi-perp (additive reversibilization), not a complex eigenvalue gap of Q. Stationary acquisition, explicit source matrices and gap certification are paid. The local proofs used here are:

* `TWO_SECTOR_EXCURSION_COMPILER_CANDIDATE.md`, SHA256 55768c9659e6a02086044b242c976b9dbcfcd814a8f9ad8428d153fbf1c5a0d4: exact scalar path law, virtual-count bound, first-event envelopes.
* `FINITE_RESERVOIR_CONTRACTION_LEMMA.md`, SHA256 df29ee51740ea383f2b6225b9e6fb74b83d539933175761f45bf8ab445c6d402: normalization-one finite reservoir contraction synthesis, including coherent variable input. The independent arithmetic note SHA67618afa29a3b661849fbca283205db34e4c3fd00eb6657520c3eb9b6f7b30ea is a compatible alternative, not an extra oracle premise.
* The already reviewed finite-mode complete-isometry amplification and count-capped future comparison are received only at their algebraic scopes, with the new source/time errors explicitly priced below.

The local candidate files alone did not establish a whole compiler. This document supplies their joint circuit and error receiving conditions. The final whole receipt must bind this body and its source premises. In both pure-source exit-rate displays, the sum is over y!=x; an unrestricted row-generator sum would be zero. This notation correction changes no frozen source bytes.

## 1. Model, access and dimensionless quantities

Q is a known explicit finite irreducible generator on d>=2 states. Its stationary pi, psi=sqrt(pi), reservoir D0, jumps L_e^0 and C0 are available to certified finite precision. Use a known c>0 with C0>=c(I-|psi><psi|). All source acquisition and preparation are charged, including conditioning. The physical reservoir has jumps sqrt(lambda)L_e^0 and free generator lambda D0.

The centered coupling K satisfies PKP=0. A precision-capable controlled block encoding with normalization b>0 is supplied, or constructed with its actual LCU normalization paid. A bound ||K||<=b by itself is NOT access. Projectors onto ground/fast sectors and projected K blocks are implemented from the acquired source basis. A nonzero mean is included in H0, with its full physical action charged. The b=0 ground-source case is ordinary H0 evolution. The trivial one-state source is also handled directly.

Put

    mu=lambda*c*T, B=b^2*T/c, R=tr(C0)/c,
    D=||D0||/c, Pi=1/min(pi), H=alpha0*T.

Use normalized time x=t/T. Rescaling Q to Q/c, lambda to lambda*c and K to K/sqrt(c) leaves the physical model unchanged. In particular, c is not an arbitrary absolute unit granting free speed.

System instruments occur at p prescribed times, with their outcome records and arbitrary reference systems retained. They never inspect the reservoir or private event clocks. Their implementation costs are external or added separately. Adaptation based on their own accessible records is allowed. The reservoir is initialized once in psi and never reset between prescribed controls.

For mu<=64B, ordinary high-precision Lindblad simulation is a separate receiving branch: Hamiltonian/source action is bounded by H+64BD+8B and jump normalization action by64BR. Its precision-capable supplied encodings and ordinary simulator costs must be included; this is not a claim that low rate is free. The high-rate proof below is for mu>=64B. It supplies the genuinely new source/compiler operation.

## 2. Exact two-sector source and counts

In normalized time set

    g=sqrt(mu B), kappa=mu/2-g,
    omega=sqrt(kappa^2/4+g^2), s=omega-kappa/2,
    d_down=kappa+s, nu=s+d_down.

Then kappa>=3g, s<=8B/3. The scalar endpoint majorant is exp([[0,g],[g,-kappa]]x). Sample its exact two-state Doob bridge with upward/downward rates s,d_down. Conditional on each fast interval of length ell, add an independent Poisson(g*ell) number of self-insertions, with ordered uniform relative positions. Apply actual projected K/b contractions, including K_QQ/b at these self-insertions. Preserve their chronological order and the free H0/fast-reservoir factors. This is the exact normalized Dyson law, not an approximation to a classical source path.

Uniformly over initial sector, its unconditioned total virtual count V has

    E 2^V <=4 exp(7s*x).

The proof uses a potential rate-s upward Poisson clock, at most two off-diagonal transitions per potential upward point plus one, and fast-visit self-insertion marks with E2^Z<=2. Marks can be drawn independently of the potential clock; accepted visits are a subset. Endpoint conditioning divides this bound by its actual endpoint probability only.

Use windows tau<=min(1,1/(16B)), W<=ceil(16B)+p+1. The accepted activity bound gives

    M=ceil(12B Pi^2+4Pi log(100/epsilon))+1,
    S=M+W+2.

M caps ACTUAL quantum jumps, not virtual insertions. No tail is assumed for the approximate compiler.

## 3. Complete first-event block, with actual jump outputs

A normalized fast interval is

    F(ell)=exp[mu(D_Q/c+I/2)ell], ||F(ell)||<=1.

Its scalar exp(-mu*ell/2) is already in the path measure. The finite reservoir contraction lemma evaluates and dilates F directly from its shifted dissipative matrix; no exponentially small ratio is formed. Each invocation has normalization ONE, avoiding dimension factors raised to the number of intervals. H0 intervals and all contractions have their controlled implementations paid.

No-event K0(tau) uses a uniform four-sector-pair inner LCU with normalization alpha0=4exp(s*tau). The physical word includes its input/output sector projections and maps the actual retained reservoir, whose fast sector has dimension d-1. Inner source words are unprepared after averaging; unknown system/reservoir inputs are not measured.

For edge e let ell_e=||L_e^0|| and rho_e=ell_e^2/c. The jump envelope in normalized time is

    alpha_e(x)^2=1024 rho_e exp(2s*tau)
                  [mu exp(-2kappa*x)+B].

Its inner uniform four-pair LCU has only FAST pre-jump endpoints, followed by the ACTUAL contraction L_e^0/ell_e. The final physical reservoir state is its actual output |y>, generally a superposition of ground and fast sectors. The endpoint label is pre-jump; projecting/resetting the output would be an incorrect instrument.

Since sum rho_e=R,

    alpha0^2+sum_e integral_0^tau alpha_e(x)^2 dx <4096(1+R).

Choose an enclosing integer power of two

    64sqrt(1+R)<=A<128sqrt(1+R).

Prepare the outer arms with probabilities alpha0^2/A^2, integral alpha_e^2/A^2, and the remaining zero good-block arm. CONDITIONAL on an event, its edge distribution is exactly rho_e/R, independent of its time. Its time density is the same truncated-exponential/uniform mixture for every edge. Thus rare edge probabilities never appear in a conditional time denominator.

For e=(x->y), cancel both its rate and source scale analytically:

    L_e^0/ell_e
      = |y>(<x|-sqrt(pi_x/pi_y)<y|)/sqrt(1+pi_x/pi_y).

This explicit rank-one contraction depends on stationary ratios, not inverse sqrt(q_xy). Zero edges are omitted. Prepare its bounded coefficients by certified finite arithmetic; source Pi and input lengths are paid.

The exact outer good block is V_first/A, where V_first is the complete first-event isometry (no event plus jump/time records). Its completeness holds on arbitrary physical reservoir inputs. All source, contraction and selection success ancillas remain coherent until COMPLETE-isometry amplification; no-event K0 alone is never amplified as an isometry.

## 4. Uniform block budget and outer-coordinate floor

Let

    e_step=epsilon/(100S), d_A=2A+1,
    beta=(e_step/(10^6 d_A^2))^4,
    sigma=(beta/[100A(E+1)])^4,

where E<=d(d-1) is the number of nonzero edges. Budget each of the finitely many error groups below at most beta/100; subdivision among its K or E elementary operations is explicit. Replacing the numerical100 by a larger fixed constant if an elementary norm convention requires it does not affect the input-dependent claim; no source-dependent constant is hidden in that replacement.

A dimensionless upper generator bound, also valid up to a fixed universal factor for the exact count-augmented frozen process, is

    Lphys=1+2H+2mu D+2sqrt(mu B)+2mu R.

Use x_min=min(1,e_step/(100Lphys)); a remaining window below x_min is advanced to its fixed boundary by identity with the charged error. All other windows have tau>=x_min.

Exclude outer uniform endpoints and probability-threshold strips of width sigma. There are O(E+1) thresholds, so this removed measure is O((E+1)sigma); replacing the normalized contractions there by zero costs O(sqrt((E+1)sigma)) in the common-uniform L2 block, safely within beta/100. Numerical arm probabilities are computed to a corresponding absolute error smaller than sigma/[100(E+1)], with exact nonnegative clipping and normalization. Square-root amplitudes are synthesized with absolute vector errors budgeted to beta/100, not an unearned relative error on tiny probabilities.

A truncated exponential of rate a has quantile Q(u)=-log[1-u(1-exp(-a*tau))]/a. On u in[sigma,1-sigma], Q'<=tau/sigma and both endpoint distances are at least (sigma/2)min(tau,1/a). Uniform components have the simpler sigma*tau margin. Hence reserve

    t0=(sigma/4)*min(x_min,1/(1+2kappa)).

Both jump times and bridge durations are at least t0 on retained coordinates, after suitably small time errors. No-event durations are at least x_min. No minimum microscopic spacing is assumed outside the explicitly removed set.

The normalized jump amplitude derivative with respect to x is bounded by

    Lout=1+kappa+(1/32)sqrt(mu/B)
                   [H+mu D+sqrt(mu B)+mu R/2].

The positive B term in the common envelope supplies the denominator. Edge scales have already canceled. Choose outer representative-time error

    dx <= min(t0/10, beta/[100(1+Lout)], e_step/[100Lphys]).

Uniform discretization is coupled on the same outer uniforms; certified inverse exponential/log arithmetic needs only logarithmic precision in these bounds. Conditional mixture mass denominators are explicitly positive on tau>=x_min and B>0, and their logarithmic inverse is priced. Very small input B is paid through input precision, not a rejection loop proportional to1/B.

## 5. Explicit global virtual cap and near-tie cut

For t>=t0 the smallest two-state endpoint probability is P01(t). A computable uniform lower bound is

    p0=s*t0/(1+nu*t0),

because 1-exp(-z)>=z/(1+z), P10>=P01 and both diagonal probabilities are no smaller at the relevant minima. Put eta=beta/10^4 and

    K=ceil(log(4 exp(7s*tau_max)/(eta*p0))/log2),
    tau_max=min(1,1/(16B)).

Endpoint-conditioned virtual count overflow has probability at most eta. The source routine allocates K transition/mark slots plus one terminal flag, and maps any overflow to zero good block. K depends on log(1/p0), not1/p0. The pure zero-coupling case was removed in Section1, so s>0 here.

Let q=nu+g, an upper bound on total bridge-plus-self-event intensity before conditioning. Choose

    zeta <= min(t0/20, eta*p0/[100(1+q+q^2)]).

A dominating Poisson clock bounds the probability of an event within zeta of an endpoint, or of any event pair within zeta, by at most a fixed multiple of (q+q^2*tau_max)zeta. This includes the self-insertions and bridge transitions jointly. Divide once by the ORIGINAL endpoint probability p0. The resulting conditioned bad set is below eta. Subsequent recursive bounds do not multiply conditional endpoint inverses along a trajectory.

On the retained path every recursive bridge duration is at least zeta/2 after rounding. Put

    pz=s*(zeta/2)/(1+nu*zeta/2),
    Lker=16(1+q)^2/pz^2.

For the first-event density qi exp(-qi*u)P_flip,j(t-u)/Pij(t), direct differentiation bounds its integrated duration derivative, its moving-support strip and the no-event atom derivative by Lker. Here all transition derivatives are bounded by nu<=q and Pij>=pz. Thus first-event kernels at durations differing by h have TV discrepancy at most Lker*h. The same raw uniform selects the no-event atom or inverts the FULL event CDF; never divide by a possibly tiny event mass.

## 6. Coherent finite source: no large-mean Poisson oracle

Use source uniforms as finite uniform WORD registers, in coherent superposition. Deterministic capped arithmetic maps them, the endpoint labels and the time register to a path and work transcript. Overflow maps to a zero contraction with a distinct flag. SELECT preserves all source/work labels. Unpreparing the inner source gives the arithmetic average of its operator words, not a measured classical input or an assumed Kraus operator.

Bridge event times use fixed-depth bisection of the full CDF. If J levels are required, at most2^(J+1) possible grid thresholds per step exist. Excluding a raw uniform strip of width xi around all possible thresholds has probability at most2^(J+2)xi. Allocate xi<=eta/[100(K+1)2^(J+3)] and round the source uniform to finer accuracy. This costs O(J+log(K/eta)) bits, not2^J operations. All evaluated exponentials have nonpositive arguments or are combined stably; never form exp(+nu*t) as an intermediate.

Self-insertions require only a FINITE Poisson CDF scan through the remaining global cap. For a fast interval ell set z=g*ell. Compute

    p_n=exp(-z+n log z-log(n!)), 0<=n<=K_remaining,

and assign the rest of the mass to overflow. For z=0 return0. If z is below the allocated sampler error, return0 with that charged error. Otherwise logarithms have a priced finite input range. Evaluate each log p_n with absolute guard precision, clipping probabilities below the error/K threshold to0 and clipping tiny positive log errors to probability1. Since n<=K, log(n!) can be computed by at mostK elementary log/sum operations or exact integer factorial plus log. Even when z is huge, the arithmetic integer part uses O(log(2+z)) bits; an exponentially small p_n is discarded, not resolved relatively. No loop runs to z, no rejection waits for a rare event, and no full uncapped Poisson count is generated.

Use certified cumulative probabilities to absolute error <=eta/[100(K+1)^2], and a finite uniform word fine enough to charge the K+1 threshold strips. Allocate eta/[100(K+1)] to each interval's count sampler, so all intervals together cost at most eta/100. The scan reproduces the capped Poisson law; its overflow mass is already included in the global virtual-tail bound, not charged as a new unbounded event.

When a count n<=K_remaining is obtained, generate n independent uniform relative positions in that fast interval and sort them reversibly. All loops pad to K and zero-fill unused slots. A comparison-based reversible sorting network of polynomial size suffices. The global near-tie cut includes these marks and guarantees stable ordering with the neighboring bridge events. Exact coincident endpoints have measure zero in the reference; numerical zero intervals are treated deterministically, with discrepancies charged through the cut and duration coupling.

## 7. Additive duration, count and operator errors

Choose an inner time-grid error h satisfying

    h <= min(zeta/[100(K+1)],
             eta/[100(1+Lker+g)(K+1)^2],
             beta/[100(1+H+mu(D+1))(K+1)^2]).

The finite bridge kernel is compared with the exact kernel at its own rounded remaining duration. Across K steps, accumulated duration mismatches are at most O(Kh), and summed kernel discrepancies at most O(Lker*K^2*h). This is an additive coupling, not an iterated inverse-CDF Lipschitz product.

For a fast interval, Poisson(g*ell) and Poisson(g*ell') have TV distance at most g|ell-ell'| by adding an independent increment. When counts agree, use identical uniform relative positions. Their absolute location changes by at most the endpoint displacements plus the interval-length error. Thus all count/position coupling discrepancies cost O(g*K^2*h) plus the separately allocated finite sampler errors. Sorting preserves the noncommuting word order off the priced tie set.

Both the free system and normalized fast-reservoir factors are contractions. Their timing derivative bounds are H and mu||D_Q/c+I/2||<=mu(D+1), respectively. Telescoping the actual word therefore bounds its timing error by

    O([H+mu(D+1)](K+1)^2 h).

This fast-reservoir term is mandatory. Using only the H0 derivative would leave a rate-dependent gap.

Give each of at mostK+1 free fast contractions and H0 evolutions error at most beta/[10^4(K+1)], and each of at mostK projected coupling/jump encodings the same budget. Source basis/preparation errors and finite edge contractions have a corresponding subdivision. Dense contraction arithmetic is performed reversibly on the duration words, applies the finite rotation circuit, and uncomputes its parameters. It uses no table of all time words. Every contraction has fresh success work; all success flags remain coherent through the global amplification.

Variable-duration H0 evolutions use binary decomposition into controlled fixed-time evolutions. Charge every slot separately, conservatively at the enclosing window/time bound with all precision overhead. No optimized additive action cost follows merely from the sum of selected path durations.

Combining the overflow/cut probabilities (operator mean cost at most twice their probability), additive source distribution errors, word timing and operator synthesis gives uniform inner-block error below a fixed fraction of beta after the stated subdivisions. Uniformity is over all endpoint pairs, all retained times and all physical system/reservoir/reference inputs. Four-pair LCU coefficients have their scalar majorant normalization already paid; no sum over d-dimensional reservoir basis words multiplies these errors exponentially.

## 8. Complete isometry, amplification and the physical clock

Outer finite amplitudes, inner blocks and time coordinates use independent work roles. The inner word sources are unprepared; outer private type/color/component/uniform records survive. Compare the exact and finite outer maps on the SAME uniform-coordinate Hilbert space. Their L2 Kraus-vector discrepancy is bounded by the amplitude/source budgets, the removed-coordinate square-root cost, and Lout*dx. This proves a base-block perturbation at most beta after allocation. It does not assert TV closeness of continuous and discrete timestamp outputs.

Pad to the exact normalizer A and attenuate by c_A=A sin(pi/(4A+2))<1. A ordinary Grover iterations give exact unit amplitude for the ideal first-event isometry. For the finite rectangular block, selfadjoint dilation and the noncommutative Chebyshev difference bound give amplified good-block error <=d_A^2*beta. Unitarity bounds leakage by O(d_A sqrt(beta)); attenuation/phase synthesis is allocated correspondingly among O(A) calls. With the displayed beta these errors are well below e_step. No normalization of a postselected nonunitary K0 is used.

After this complete amplification, privately read or retain the event label and its representative time, update the remaining window, and iterate. The actual reservoir is retained after EVERY branch. It is never re-prepared in psi. Prescribed consumer operations act only on accessible systems and records.

For the global comparison, augment the EXACT physical Lindblad process by a count register and freeze it after M jumps. Its generator norm is at most a fixed multiple of Lphys, independent of the count dimension. Its future channel is therefore Lipschitz in the remaining duration by that bound, also with later prescribed instruments, references and records. A backward hybrid across at most S calls charges the per-call isometry discrepancy and Lphys*dx; tiny-window identity advances cost Lphys*x_min. This compares the private-time algorithm to the exact future at the perturbed remaining time, rather than exposing rounded times to an arbitrary consumer.

The exact source activity tail bounds the event of reaching the count cap by epsilon/100. An exact instrument coupling before that event bounds its discarded/frozen contribution by a constant times this probability. The finite approximate process need not satisfy an independent jump MGF. Initial psi/basis preparation is given an additional epsilon/100 budget and handled by channel contractivity, not by reusing an activity bound for a possibly wrong initial reservoir.

The sum of these allocated errors is below epsilon after fixed universal safety factors. Fixed caps and all failure flags define an unconditional CPTP circuit on every input. No favorable outcome is normalized after postselection, and no exceptional physical duration mean is assumed.

## 9. Resources and exact exclusion boundary

All inner caps and precision requirements are logarithmic in endpoint/tie probabilities and polynomial in the displayed scale-invariant inputs. The normalized fast matrix argument is mu*(D_Q/c+I/2)*ell; its dense finite arithmetic has polynomial dependence on d, source norm/input bits and log(2+mu), not a loop of length mu. The capped Poisson scan has polynomial K work, independent of its potentially large uncapped mean. Every source/arithmetic branch is padded to a uniform bound, so superposed endpoints and times are valid.

Calls are bounded by S=O(B Pi^2+Pi log(1/epsilon)+B+p+1), complete amplification by O(sqrt(1+R)) base calls per call, with polynomial source preparation/sorting/arithmetic, K operator selections, K+1 separately charged fast/H0 interval implementations, and uncomputation. A selected coupling encoding is the supplied actual interface; if assembled from components, its component SELECT costs are included. Reservoir/state acquisition and consumer-instrument costs are explicitly additional, not bounded by p alone.

Consequently the candidate high-rate overhead is polynomial in d,1+H+B+p,R,D,Pi,input lengths,log(2+mu),log(1/epsilon), with operator encoding costs included. The low-rate branch pays its ordinary source-conditioned Lindblad normalization as stated. Source conditioning may be very expensive. This is not efficient access to an unknown or succinct exponentially large source, not uniform over unbounded postselection, not a public path/timestamp simulator, not a nonstationary-source theorem, and not an optimal or practical resource claim.

Whole acceptance must follow joint review of this finite-bit body and its exact local/source premises. It does not follow merely from small physical jump count.
