# A certified operational reset without resetting the true environment

28 October 2026. New construction candidate; independent review pending. This imports the received trace-class complete-quotient primitive, not an unproved physical realization or reset oracle. It removes ongoing environment-reset demands CONDITIONAL on an already valid acquired core. Cold-start acquisition without reset remains a separate obligation.

## 1. Actual operation and certificate inputs

Use the stationary finite accessible quantum-port and honest finite observable-rank-r contract of TRACE_CLASS_COMPLETE_QUOTIENT_EXTENSION.md. The true hidden memory may be infinite-dimensional. A valid r-core supplies raw physical prefixes tau_j, empty prefix first, trace row m_j=Tr(tau_j), m_1=1, 0<=m_j<=1, and predictive coordinates Pi with complete positive-state bound ||Pi(Omega)||_Sigma<=K Tr(Omega). Unknown core values need not be supplied exactly: simultaneous valid intervals from a prior paid acquisition suffice.

Choose a finite physically executed memory-only word R. It prepares declared accessible inputs, runs native operations and discards all accessible outputs/outcomes at its end; any local ancillas are freshly initialized each repetition. Thus its ACTUAL memory map Psi is CPTP and preserves the reachable algebraic span and its invisible subspace. No outcome postselection or retained reset-record controller is silently inserted. Let C be its true r-by-r coordinate matrix, so Pi Psi=C Pi and mC=m. The word's full call, preparation, discarded-readout, duration and control costs are charged every repetition.

Acquire C from the shifted raw table H_R,ij=Tr[F_i Psi(tau_j)] using the same valid core interval inversion as the signed predictor. These are actual joint prefix/reset-word/future probabilities. They include all failed prefix trials and marginalize reset outputs. Acquisition of these tables is NOT free from an arbitrary current hidden state; see Section6.

## 2. Eliminate the unknown trace coordinate stably

Let E select coordinates2,...,r and define

    W_m y = (-sum_(j=2)^r m_j y_j, y_2,...,y_r).

Then m W_m=0, E W_m=I, and every tuple x with m x=0 equals W_m E x. On the amplified block trace norm, ||E||<=1 and ||W_m||<=2 because 0<=m_j<=1. This holds with operator-valued Hermitian coordinates and arbitrary finite reference dimensions, not only scalar probability vectors.

Define

    a=E C e_1, D=E C W_m.

On the trace-one affine hyperplane y=E x evolves as y'=a+D y. On trace-zero tuples, C W_m=W_m D because mC=m. If the computable certificate below gives

    ||D||_(1->1) <= c <1,                                  (1)

then every amplified trace-zero block contracts: ||D^t y||_Sigma<=c^t||y||_Sigma. This uses only the sum of absolute matrix coefficients, so no unspecified completely bounded norm optimization is hidden.

The affine fixed point is y_*=(I-D)^(-1)a and v=e_1+W_m y_*. Starting from physical rho_0, C^t e_1 converges to v. Since every such physical state has coordinate norm<=K, ||v||_1<=K and ||y_*||_1<=K. This does NOT assert convergence of the actual memory state in trace norm or existence of a physical stationary trace-class memory state.

For r=1, the quotient is already operationally independent of memory: take v=1 and zero reset cost. No empty-matrix norm ambiguity is required.

## 3. Decoupling an actual record or reference

Let Omega_MR be any positive normalized finite-history joint state whose memory blocks belong to the reachable algebraic span; R can contain retained classical calibration records and finite quantum registers. Put x=Pi(Omega), so ||x||_Sigma<=K and m x=Omega_R. Since E(x-v tensor Omega_R) has norm<=2K,

    ||C^t x - v tensor Omega_R||_Sigma
      <= ||W_m|| c^t ||E x-y_* tensor Omega_R||_Sigma
      <=4K c^t.                                           (2)

The actual operation Psi acts only on memory through its accessible word; it does not inspect R. Thus (2) is an operational forgetting certificate for initially correlated records, not merely a convergence statement from one fixed state.

For any subsequent finite allowed coherent/adaptive controller retaining R, the final accessible-output map on predictive tuples has norm at most one: realize a signed tuple by Lambda(x)=sum_j tau_j tensor x_j, execute the ACTUAL complete CPTP future controller, then trace hidden memory. Lambda has norm<=1; complete CPTP processing and partial trace contract Hermitian trace norm. Invisible-kernel invariance makes this representation exact on reached states. Consequently the half trace distance between the actual post-reset future output and its operational-limit reference is at most

    epsilon_reset(t)=min(1,2K c^t).                         (3)

The reference defined by v is a physical accessible process at every finite horizon: it is the limit of the processes obtained by actual reset repetitions from rho_0. Each finite Choi channel is CPTP and that cone is closed. Consistent limits give a compatible finite-horizon family. We do not construct a finite hidden CP realization or assume that v has a positive Lambda representative.

The comparison is uniform over finite future controllers and finite reference dimensions at the actual ports. It is not a full hidden-memory diamond-norm reset. Hidden counters or inaccessible degrees of freedom can continue recording the entire past.

## 4. A finite interval test, including the trace row

Let valid simultaneous bounds give |C-Chat|<=F and |m-mhat|<=d, with m_1=mhat_1=1. All matrices/bounds can be rational. For row l>=2 and column j>=2 define

    Dhat_lj=Chat_lj-Chat_l1 mhat_j,
    B_lj=F_lj+F_l1+|Chat_l1| d_j.

Indeed D_lj=C_lj-C_l1 m_j, and |m_j|<=1 yields |D-Dhat|<=B. Therefore

    c_cert=max_(j>=2) sum_(l>=2) (|Dhat_lj|+B_lj)             (4)

is a certified amplified contraction constant. Accept ONLY if c_cert<1. This is a sufficient certificate, not a test characterizing all mixing sources; a poorly chosen core/norm can fail despite true mixing. Invalid or uninformative intervals cause ABSTAIN. Data-dependent word selection is permitted only under a simultaneous confidence event covering the declared finite word pool; arbitrary post-selection of unbudgeted words is not included.

Choose the smallest integer t such that 2K c_cert^t<=epsilon. Rational repeated powering suffices, with actual word length L_R giving t L_R native calls. For c_cert=0 one repetition suffices; for c_cert in(0,1) this is logarithmic in1/epsilon with the explicitly acquired conditioning/mixing constants. Confidence failure beta and physical WHOLE reset-word implementation distance nu_t are added once. Repetition of inaccurate controls needs an actual complete process bound, e.g. t times a certified per-word norm error; ideal contraction alone does not certify the hardware.

No empirical trace row is set to all ones. Trace-row uncertainty enters (4) and is essential: the stable trace-zero hyperplane depends on the actual raw prefix masses.

## 5. What it enables, and what it does not

After a valid core and reset certificate have been acquired, later calibration/service episodes can begin with this paid operational burn-in rather than a full environmental reset. Approximate starting-law errors must enter probability intervals and whole-process performance budgets; repeated episodes are not thereby literally independent.

For N reset-separated experiments whose conditional starting operational law is within epsilon_reset of the same limit, conditional event means differ from the corresponding limit-law probabilities by at most epsilon_reset. Classical martingale concentration can therefore use radius epsilon_reset plus its stochastic deviation, rather than falsely applying an exact iid model. A joint whole-record comparison can alternatively pay at most N epsilon_reset by a hybrid. Which accounting is appropriate depends on the downstream theorem; it must be stated.

This also supplies a potential interface for retiring calibration records before a record-averaged recovery protocol: the memory is operationally decorrelated from those records to (3). It does NOT itself prove cancellation of decoder estimation errors, a fast1/N learning rate, or a guarantee after records remain accessible to the final evaluator. Those are separate constructions.

The strongest conventional baseline is a known mixing/burn-in or Doeblin-style condition followed by ordinary identification. The addition here is an acquired sufficient contraction witness on the complete observable quotient, with trace-row uncertainty and a possibly infinite nonmixing actual environment. No historical novelty or practical speed advantage is claimed.

## 6. Bootstrap boundary

The raw core and shifted-word intervals imported in Section1 need a valid acquisition law. If they were obtained using independent paid starts, the theorem replaces FUTURE starts only; it does not retroactively eliminate that initial resource. If an independently justified approximate operational reset bound is supplied, its bias may be included in initial intervals and then sharpened by (4). That is a separate physical premise, not a reset discovered from no information.

A single uncontrolled trajectory does not automatically provide the same raw tables as independently started prefix/future experiments. Replacing those acquisition means by observed transition frequencies would be circular. Finite observations also do not certify a missing rank promise: a delayed hidden mode can reproduce all tested short behavior and later retain old records. This note neither proves a cold-start impossibility under every honest rank/control promise nor closes that cold-start problem.

The next substantive obligation is therefore a noncircular bootstrap mechanism, or a precise application where a finite initial reset bank is available but repeated long-term resets are the dominant obstacle. This conditional theorem is useful only at that actual scope.

## 7. Conditional compilation of a restart-based learner

Suppose a separately established learner/protocol uses N fresh operational starts for calibration, one further fresh start before a finite service, and has record-retired final-channel error r_N under that reference law. It may use the entire calibration record to choose its decoder, but finally retires that record as specified by its own theorem. Replace EACH of those N+1 starts by t actual reset-word repetitions. The bound (3) includes correlation with all previously acquired records and caller registers, so a sequential hybrid gives a whole-protocol difference at most (N+1) epsilon_reset(t). Therefore

    actual final-channel error <= r_N +(N+1) epsilon_reset(t)
                                 +beta+nu_all.              (5)

Here beta is the failure probability of the initial core/reset certificate, and nu_all is the complete implementation debit for the entire compiled protocol. The ideal reference law is the SAME operational-limit source. A theorem for a different physical initial state cannot simply be reused.

If a separately proved reference learner has r_N<=C/N, taking epsilon_reset<=C/[N(N+1)] preserves an O(1/N) final-channel guarantee with O(N log N) reset-word repetitions at fixed acquired c<1,K. This is a conditional compiler consequence, not a new proof of that learner's1/N rate. A single reset AFTER a correlated calibration run would only remove memory/program correlation; it would not repair biased or nonsymmetric calibration statistics. Every start required by the reference theorem is replaced and paid.

The initial valid core/reset bank remains an extra resource. Reusing it across later many-service sessions is where this mechanism could be useful. The following fixture demonstrates operational rather than microscopic forgetting, but does not resolve initial acquisition.

## 8. Exact rank-two fixture with an environment that never resets

Let memory consist of a classical pointer bit and an inaccessible unilateral-shift counter. One native action emits the current pointer as a classical output, flips the pointer with probability q=1/4, and increments the counter. A deterministic reset word is one such action with its output discarded. Start with pointer0 and counter0.

Use empty prefix tau1 and the first outcome0 prefix tau2. Both have mass one; their pointer distributions are (1,0) and(3/4,1/4). With empty future and a next-output1 test,

    H=[[1,1],[0,1/4]], m=(1,1), K=sum|H^-1|=9,
    C=[[0,-1/2],[1,3/2]], D=1/2,
    v=(-1,2).

The signed coordinate v represents the stationary POINTER distribution(1/2,1/2), not a positive mixture of the two core prefixes. The actual counter keeps shifting. States with different counter values remain orthogonal; there is no stationary normal density on the unilateral-shift counter and no full-memory trace-norm reset.

All future accessible effects ignore the counter and depend only on pointer populations, so the complete observable quotient is exactly rank2. For a pointer initially perfectly classically correlated with a retained reference bit, t discarded reset actions leave actual half-distance 2^(-t-1) from the product pointer/reference state. The general certificate gives the looser2K(1/2)^t. The independent reference dimension is not used in the proof, though this finite fixture only illustrates a classical correlation.

The accompanying exact rational program checks20 horizons, trace preservation, the signed fixed coordinate, and all8 corners of a conservative interval contraction certificate with entry/trace widths1/1000, producing c_cert=503/1000. It uses no RNG, source draws or hardware. Infinite counter scope is proved analytically, not by a finite truncation.
