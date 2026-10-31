# Native dark-Lindblad source: complete first-event receiving construction

31 October 2026. Candidate for independent whole review. This receives a native generator, not a substituted collision process. It is a constructive circuit-existence statement; no implemented simulator, practical crossover, or novelty assertion is made.

## 1. Actual acquired inputs and output

Let P=|psi><psi| and Q=I-P on a finite, possibly succinctly encoded source. Supply precision-capable controlled preparation of psi (hence P/Q reflections), an acquired contraction block encoding of the rectangular stack L: v -> sum_a |a>L_a v with normalization alpha_L, and a Hermitian block encoding of H=(1/2)L†L with normalization alpha_H. The labels a are outputs of the stack, not an enumerated list. All these gates, inverses, work registers, and their requested-precision implementation costs are paid. A matrix norm bound is not an encoding. One may acquire H from the stack with alpha_H=alpha_L²/2. Separate better acquired encodings may instead be used.

The exact nominal operators satisfy L_a psi=0 and certified inequalities

    g Q <= H <= h Q,       G†H <= -kappa H,
    G=sum_a D[L_a],        g,h,kappa>0.

Supply system Hamiltonian H0 and Hermitian joint coupling K, with acquired block normalizations alpha_0 and b, and PKP=0. A known nonzero mean must instead be retained in H0 with its actual sqrt(lambda) action paid; scalar system identities may be removed under an explicit global-phase convention. The physical generator is

    lambda G - i[H0+sqrt(lambda)K,.].

The output guarantee is trace norm at most epsilon, uniformly on arbitrary joint system/source/reference input, for p prescribed common CPTP instruments, their retained outcome records and final joint source/system output. Instruments may act on the source. Their implementation costs are external or added explicitly. Their times are prescribed; the simulator's artificial jump colors and timestamps remain private. No identification with a classical stochastic source follows without a separate invariant-observable-algebra theorem.

All inputs are exact nominal acquired operators with refinable synthesis, certified rational/dyadic bounds and finite descriptions. For supplied real parameters one must have certified magnitude/precision access; exact sign/zero tests on unspecified reals are not assumed.

## 2. Scale normalization and previously checked receivers

Replace H,L,G,h,kappa by H/g,L/sqrt(g),G/g,h/g,kappa/g, and replace lambda,K,b by lambda*g,K/sqrt(g),b/sqrt(g). This leaves the physical model unchanged. In the remainder g=1. Set

    mu=lambda*T, B=b²*T, Hs=alpha_0*T, c0=sqrt(mu*B),

and use time in [0,1]. The normalized source still obeys Q<=H<=hQ and G†H<=-kappa H. Encoding normalizations below are the normalized ones. Raising h if necessary to max(h,alpha_L²/2) is allowed and makes all count bounds conservative; it does not magically improve alpha_L.

The count receiver is NATIVE_SOURCE_COUNT_LEMMA_CANDIDATE.md, SHA e2230beee7a7b2ba87f5aa9fe234cc9265724d36b8d4bd03327bd1c3afda0653, with NATIVE_COUNT_INDEPENDENT_REVIEW.md SHA 9c1d5645d993a4554f8b5bb5d5c6712ad6d61e9a14a72ea914d763838ae5de10. Its arbitrary-input and arbitrary-prescribed-instrument statement is used, not just its ground-input version.

The finite ordinary LCHS kernel is Sections 3–4 of ../pure_return_comparison_20261031/PRIMARY_COMPARISON_AND_ORDINARY_KERNEL.md, SHA 4360e7ccdb5fead0a34115eb8292d647c67755e3e0b7398f080d2883d59623d9, independently received by ORDINARY_KERNEL_INDEPENDENT_REVIEW.md SHA 897b1060111b655e1d36eee437cd23a832f30ea6e41022b1bf00e3bb69b74514. This is ordinary functional calculus with its real quadrature normalizer and slack amplification paid, not an exponential oracle.

The two-state bridge and complete-isometry amplification operations below are re-bound to the new source. The earlier full finite-bit pure-return receiver is SHA 1a097458af52e4b89746b2f5e38e8ba4ea9f8a835db731daef39b8e9ea71e032; its source generator and jump stack are NOT substituted for the present ones.

## 3. Acquired fast kernel with its factor two retained

Acquire A=H-Q/2 by LCU. A>=0, A P=0, and A Q>=Q/2; its normalization is at most alpha_A=alpha_H+1/2. Define

    F(s)=(1/2) Q exp(-s A) Q.

For s>=2 log(1/delta), replace F by zero, with error at most delta/2. Otherwise s is O(log(1/delta)). The received finite LCHS construction acquires exp(-sA)/2, followed by Q projections, with error delta and cost polynomial in alpha_A and log(1/delta). More explicitly its quadrature truncation is O(log²(1/eta)), finite positive Gauss panels and controlled Hamiltonian evolutions have polynomial action s*alpha_A and logarithmic precision; the real LCU normalizer is polynomial in log(1/eta), and slack singular-value amplification targets division by two. eta is tightened by that amplification's degree/normalizer. No exponential amplitude is ever computed. Time s is a coherent finite-bit input; actual controlled fixed-time Hamiltonian evolutions and their arithmetic are paid.

Consequently the exact free Q dwell is

    exp(-mu*u*H) Q = 2 exp(-mu*u/2) F(mu*u).

The kernel has norm <=1/2, and derivative norm <=(alpha_H+1/2)/2. Its numerical cutoff may be discontinuous: the approximation is uniformly close to this exact differentiable function, which is the function used in timing comparisons. The free P dwell is identity. H0 commutes with source projectors and the free source kernel; its unitary evolution is inserted chronologically. The factor two for EVERY Q dwell is retained below.

## 4. High branch, caps and positive sector majorant

For B>0 use the high branch when

    mu >= 4096 B max(1,h/kappa)^2.

This implies both the acquired count lemma's high condition and r>=8c0, where r=mu/2. Put

    delta=r-2c0, nu=sqrt(delta²+8c0²),
    s=(nu-delta)/2=2c0²/d, d=(nu+delta)/2.

Use the stable expression 2c0²/d for s. Then delta>=6c0, d>=delta, and s<=16B/3. Choose a certified dyadic tau_max within a factor two below min(1,1/(128B)). Thus s*tau_max<=1/24. Split at every prescribed instrument; the deterministic number of no-event windows is at most Wcap=ceil(1/tau_max)+p+1.

Let utheta=min(1,kappa/(16h)), theta=log(1+utheta). With tail budget epsilon/1000 take

    Mcap=ceil(((p+1)log2+log(1000/epsilon)
                  +32 utheta h² B/kappa²)/theta)+2,
    Scap=Mcap+Wcap+2.

Every numerical ceiling is computed from a certified upward interval, not an exact comparison to an irrational. The count lemma supplies this cap on the ACTUAL physical jumps, for arbitrary initial source and instruments.

In the H0 interaction picture expand only the coupling insertions. A P-to-P insertion is zero by centering. Every Q dwell contributes 2exp(-r*u) times F; projected K/b blocks are contractions. The complete scalar endpoint majorant is

    M=[[0,c0],[2c0,-r+2c0]],
    E(t)=exp(Mt) diag(1,2)=S exp(Msym*t) S,
    S=diag(1,sqrt2), Msym=[[0,sqrt2*c0],[sqrt2*c0,-delta]].

This follows by assigning the factor two to the initial Q sector and each insertion whose destination is Q. It prices all Q dwell factors, including consecutive QQ insertions, without an uncharged 2^word multiplier. Each virtual raising/lowering/QQ interaction contributes the scalar phase -i, so SELECT includes (-i)^V. Source occupations are sector labels only; the unknown actual source is never measured or reset.

The exact entries are

    E00=(d/nu)e^(st)+(s/nu)e^(-dt),
    E01=E10=(2c0/nu)(e^(st)-e^(-dt)),
    E11=2[(s/nu)e^(st)+(d/nu)e^(-dt)].

In particular Eji<=2e^(st), E10<=2(c0/delta)e^(st), and

    E11<=2e^(-delta*t)+4(c0/delta)^2 e^(st),
    E1i<=2e^(s*tau)[e^(-delta*t)+c0/delta].

The latter uses c0/delta<=1/6. These are positive word sums, not probabilities of physical jumps.

## 5. Complete first-event isometry and actual jump output

Let K0(t) be the exact no-physical-jump propagator with normalized-time generator -i(T*H0+c0*K/b)-mu*H. Here K/b is the supplied normalized coupling after the source scale change. The exact stack of physical jumps is J=sqrt(mu)L. It annihilates P, but its output is arbitrary retained source plus its actual color, not a reset to psi.

For K0(t), prepare four uniform initial/final sector arms, each containing its endpoint-conditioned positive virtual path; accept its scalar coefficient Eji(t)/(2e^(s*tau)). SELECT contains |j><i| sector transitions realized by projected operator blocks on the actual source, not a literal rank-one reset. The resulting block has normalization

    alpha_no=8e^(s*tau).

For JK0(t), only pre-jump sector Q contributes. Use two uniform initial-sector arms and append the acquired L/alpha_L. A safe pointwise normalization is

    alpha_jump(t)^2 = 256 alpha_L² e^(2s*tau)
                              [mu e^(-2delta*t)+4B].

Indeed the required amplitude is at most 2alpha_L sqrt(mu) E1i. Squaring the preceding bound and using mu*c0²/delta²<=64B/9 gives the stated slack. The color and post-jump source of L are output registers of this instrument and survive to continuation.

The integrated proposal mass is independent of the rapid rate:

    Z=alpha_no²+integral_0^tau alpha_jump(t)^2 dt
     <=e^(2s*tau)[64+256alpha_L²(4/3+1/32)]
     <256(1+2alpha_L²).

Here mu/(2delta)<=4/3 and 4B*tau<=1/32. Choose a padded integer

    Aamp=32 * 2^ceil(log_4(1+2alpha_L²)).

Then Aamp²>=1024(1+2alpha_L²)>Z and Aamp=O(1+alpha_L). The zero remainder is an explicit zero-output contraction arm with distinct failure flags. Outer branch weights are alpha_no² and the two nonnegative integrals in alpha_jump²; sample the event component as truncated exponential of rate 2delta or uniform. No probability division by a small physical jump probability occurs.

For fixed outer event time t, UNPREPARE the inner endpoint/path random seed after SELECT to obtain the mean no-jump word. Do NOT unprepare the outer event-type/uniform-coordinate/color registers. All block-encoding failures remain coherent until complete-isometry amplification.

Exact Kraus completeness is

    K0(tau)†K0(tau)+integral_0^tau K0(t)†J†J K0(t)dt=I.

It follows by differentiating K0†K0; it holds on the FULL source/system Hilbert space, with external references. Therefore the good block of the complete outer construction is V/Aamp for an isometry V. It is legitimate to amplify this complete block, not the no-jump contraction alone.

For integer Aamp set dA=2Aamp+1 and attenuate by cA=Aamp*sin(pi/(4Aamp+2)). Aamp oblivious Grover iterations give exact amplitude one on the ideal isometry. A perturbation beta in the base block gives good-block error <=dA² beta and leakage O(dA sqrt(beta)). This follows from the noncommutative Chebyshev recurrence on the selfadjoint dilation of a rectangular block, not a scalar derivative argument. The O(Aamp) base calls, attenuation and phase synthesis are all paid.

## 6. Exact conditional virtual source

The symmetric Metzler kernel is a Doob transform of a two-state chain with up rate s and down rate d. Given its endpoints, the positive off-diagonal paths have exactly this chain's bridge law. On every fast-sector residence of duration ell independently add a Poisson(2c0*ell) number of QQ insertions, uniform in that residence, then sort. This restores the +2c0 fast diagonal in the original M. The endpoint S factors are already in E.

There is an explicit logarithmic endpoint-conditioned count cap. Potential up events are dominated by a Poisson(s*tau) clock. A full fast visit is bounded by an independent Exp(d) residence; with gself=2c0 and gself/d<=1/3, its self-count Z obeys E2^Z=d/(d-gself)<=2. Assign full independent residence marks even to unused potential up events. The possible initial fast visit contributes at most one down event and its self-count. Thus, before conditioning,

    E 2^V <=4 exp(7s*tau).

For durations t>=t0, all four endpoint probabilities of the Doob chain are bounded below by

    p0=s*t0/(1+nu*t0).

This uses P01(t)=(s/nu)(1-e^(-nu*t))>=s*t/(1+nu*t), P10>=P01 and diagonal minima >=s/nu. Dividing the MGF once by the ORIGINAL endpoint probability gives a uniform conditional cap

    Kcap=ceil(log(4exp(7s*tau_max)/(eta*p0))/log2)+2.

Its numerical dependence is logarithmic in 1/p0. No sampler performs 1/p0 trials.

At current state i, endpoint j and remaining time t, the first-event survival is e^(-q_i*u) Pij(t-u)/Pij(t), density q_i e^(-q_i*u) P_(1-i),j(t-u)/Pij(t). There is a no-event atom only for i=j. Use the SAME raw uniform to choose the atom and otherwise invert the UNCONDITIONED event CDF; never renormalize by a possibly tiny event mass. Closed two-state matrix formulas use stable nonpositive exponential expressions. Recursive inverse-CDF bisection is capped by Kcap. Self Poisson counts are sampled by a finite CDF scan up to the remaining cap; all overflow selects zero, without resampling. Thus this is a concrete acquired source rather than a conditional bridge oracle.

## 7. Fully specified numerical budgets

Put

    e_step=epsilon/(1000Scap),
    beta=(e_step/(10^6 dA²))^4,
    sigma=(beta/(100Aamp))^4,
    eta=beta/10^4.

Use certified positive dyadic lower bounds within a factor two for p0 and all subsequent lower bounds, and upward bounds for rates/derivatives. These replacements are made BEFORE choosing dependent budgets. Elementary ceilings may be increased by two. No exact transcendental comparison is required.

A conservative norm bound on the normalized physical generator and its counter-augmented frozen version is

    Lphys=1+2Hs+2c0+2mu*alpha_L².

Set x_min=min(1,e_step/(100Lphys)). A remaining window shorter than x_min is advanced by identity to its fixed boundary. Every other first-event call has tau>=x_min. Remove outer uniform-coordinate endpoint strips of width sigma. Square-root removed mass, not its probability alone, is charged to the outer isometry. Give outer probability weights total absolute error much less than beta², including midpoint end bins.

Retained truncated-exponential/uniform times satisfy t,tau-t>=t0 with

    t0=(sigma/4)min(x_min,1/(1+2delta)).

The truncated exponential inverse is -log(1-v(1-e^(-2delta*tau)))/(2delta), evaluated by stable log1p/expm1 and its uniform limit. On the retained uniform interval its derivative is <=tau/sigma. A safe derivative bound for the normalized event operator JK0(t)/alpha_jump(t) is

    Lout=1+delta+sqrt(mu/B)(Hs+c0+mu*h).

This follows from ||J||<=sqrt(mu)alpha_L, ||K0'||<=Hs+c0+mu*h, alpha_jump>=32alpha_L sqrt(B), and logarithmic proposal derivative <=delta. In particular the acquired alpha_L cancels rather than causing an inverse physical jump norm. Choose outer time accuracy

    du<=min(t0/10, beta/[100(1+Lout)], e_step/[100Lphys]).

Only log(1/B), not inverse B repetitions, enters precision. B>0 has an explicit finite description; its zero case is handled separately below.

For the virtual source let qrate=nu+gself and choose

    zeta<=min(t0/20, eta*p0/[100(1+qrate+qrate²)]).

A dominating rate-qrate Poisson clock bounds events near either endpoint and event pairs within zeta by an absolute constant times (qrate+qrate²*tau_max)zeta. This includes the QQ points. Divide once by the original endpoint probability p0. Remove these paths together with total virtual overflow. The conditional removed mass is O(eta). Remaining recursive durations after rounding are >=zeta/2. Put

    pz=s(zeta/2)/(1+nu*zeta/2),
    Lker=16(1+qrate)²/pz².

Differentiating the explicit first-event density, atom and moving endpoint bounds its TV change under a remaining-duration change by Lker times that change. Transition derivatives are <=nu, and denominators are >=pz. This bound is used through logarithmic precision, not as an operation count.

Finite coherent seed words drive a fixed-depth reversible bisection. If its depth is J, at most 2^(J+1) possible thresholds occur. Remove raw-uniform strips of width eta/[100(Kcap+1)2^(J+3)] around all thresholds; the circuit performs J comparisons, not 2^J. Required arithmetic precision is O(J+log(Kcap/eta)). Source registers are uncomputed only after SELECT so their averaged word is the good block.

For each residence, its Poisson mean z=gself*ell can be numerically large. Compute probabilities through the remaining Kcap via log p_n=-z+n log z-log(n!), with z=0 separate, and clip values below their allocated absolute tolerance. If all retained probabilities are tiny, almost all mass goes to overflow; this does not require z iterations. n! involves n<=Kcap only. Allocate per-entry CDF error eta/[100(Kcap+1)^2], and sample/sort the accepted uniform relative positions. Fixed scan, capped sort and reversible arithmetic have polynomial bit cost in Kcap and input/precision bit lengths.

Choose inner time accuracy

    h_time<=min(zeta/[100(Kcap+1)],
                eta/[100(1+Lker+gself)(Kcap+1)^2],
                beta/[100(1+Hs+mu*(alpha_H+1))(Kcap+1)^2]).

Across recursion, remaining durations differ by at most O(Kcap*h_time). The total kernel/count mismatch is O((Lker+gself)Kcap² h_time). Poisson means have TV Lipschitz constant gself; conditional on coupled counts use the SAME relative uniforms. There is no multiplicative inverse-quantile stability iteration. The operator word timing error is O((Hs+mu*(alpha_H+1))(Kcap+1)^2 h_time). This explicitly charges the new fast-kernel derivative; omitting it would be incorrect.

All kernel, projected coupling, jump-stack, source reflection, acceptance, rotation and interval simulation errors are at most beta divided by 10^4 times the capped total number of operations. Kernel LCHS/SVA internals tighten their own tolerance accordingly. Every virtual insertion includes (-i); its elementary phase is exact or receives this budget.

A B_time-bit H0 interval in [0,tau] is implemented by B_time controlled fixed-time evolutions with durations tau/2^j. Their errors are subdivided. Charge every one of the Kcap+1 padded interval slots at its worst-case tau cost, not an unproved sum-of-realized-path-cost shortcut. The same principle applies inside acquired kernel Hamiltonian simulation. No free variable-time oracle or exponentially large preprocessing table is used.

## 8. Whole isometry, private-time and count conjunction

Each capped inner mean block differs from the ideal word mean by <=beta/10 with the preceding subdivisions. Removed probabilities bound operator-mean errors linearly because selected words are contractions. If a coherent source-state norm comparison is used instead, pay the square-root bad-mass bound.

For the outer map attach a private uniform remainder to each finite midpoint bin. Exact and approximate amplitudes then occupy the SAME uniform-coordinate Hilbert space. Their L² difference is bounded by square-root removed mass, weight/synthesis error, the inner block error, and Lout*du. This gives base good-block error <=beta. Continuous and finite timestamps themselves have TV distance one in general; no such comparison is claimed.

Complete-isometry amplification has good error <=dA²beta and leakage O(dA sqrt(beta)), below e_step. Divide an additional e_step/100 among all O(Aamp) attenuation/phase/base calls. Failure flags are retained or mapped to a fixed CPTP output, never normalized after postselection.

Privately read/store the first-event arm/time after amplification. A no-event arm reaches the fixed window end. A jump arm retains the actual L output/color and recurses on the remaining duration. Do NOT reset the source. Source interventions occur only at the prescribed window boundaries.

For a global proof augment the EXACT process with a counter and freeze it on reaching Mcap. Its generator norm is bounded by a fixed absolute multiple of Lphys, independently of counter/source dimension. Its future joint channel is Lipschitz in remaining time, even with later fixed instruments and arbitrary references. A backward hybrid over at most Scap calls charges e_step, O(Lphys*du), and O(Lphys*x_min). Thus private representative times are compared through their actual future channel, not disclosed records. The count cap's exact bad effect is <=epsilon/1000 uniformly by the received tilted-MGF bound; replacing this CP tail by fixed continuation costs at most twice its probability in complete trace norm. No approximate-process MGF or exceptional-path mean is assumed. Fixed caps and unconditional overflow handling define a finite CPTP circuit on EVERY input. Enlarging the displayed numerical safety factors by a universal constant, if needed for a diamond-versus-Stinespring convention, makes the sum <=epsilon; no input-dependent constant is hidden.

## 9. Degeneracies and a constructive ordinary low-rate branch

T=0 executes only zero-time prescribed instruments. lambda=0 gives ordinary H0 evolution with the source retained. A one-dimensional Q=0 source is trivial after centering. Zero coupling is not zero source dynamics on arbitrary inputs.

For B=0 and mu>0 use K0=e^(-iH0*t)(P+e^(-mu*H*t)Q) directly, without Doob endpoint formulas. One Q kernel F suffices. Use alpha_no=8, alpha_jump²=256 alpha_L² mu e^(-mu*t), and a constant-size padded isometry normalizer as above. The normalized event block has the exact cancellation

    J K0(t)/alpha_jump(t)=(L/alpha_L)F(mu*t)e^(-iH0*t)/8.

Its derivative is O(Hs+mu*(alpha_H+1)), with no division by B. Truncated exponential source, common-uniform comparison, private-time hybrid and arbitrary-input count cap apply exactly as above. There are no virtual interaction events. Windows are bounded by one and controls. Arbitrary source excitation may emit; it is not reset or ignored.

When B>0 but mu<4096B max(1,h/kappa)^2, ordinary high-precision simulation is enough. For completeness it can be obtained here without a separate source oracle. Set

    D=-i(H0*T+c0 K/b)-mu H,
    d0=Hs+c0+mu*alpha_H,
    tau_low<=1/[32(1+d0+mu*alpha_L²)].

Acquire D/d0 by the supplied Hamiltonian/H/K encodings and LCU (handle d0=0 separately). The Taylor LCU for e^(tD) uses terms d0^j t^j/j! and SELECT (D/d0)^j. On each window d0*t<=1/32, its normalization is <=e; truncate at O(log(S_low/epsilon)) with the usual factorial tail. This prepares the no-event block, not a normalized no-event state. Append sqrt(mu)L for a jump, use a UNIFORM outer time with normalization e sqrt(mu)alpha_L, and combine with the no-event arm. Integrated squared mass <=e²(1+mu*alpha_L²*tau_low)<16, so pad to an integer8 and amplify the COMPLETE first-event isometry. Taylor source counts use a finite CDF scan of a bounded mean; all primitive errors, timing and failures have the same finite complete-isometry treatment.

Actual jump intensity <=mu*alpha_L² gives a Poisson count cap O(mu*alpha_L²+log(1/epsilon)); the number of deterministic windows is O(1+d0+mu*alpha_L²+p). This bounds S_low by a polynomial in the stated low-branch parameters. Generator/time derivatives and Taylor precision cost only logarithmic bits, whereas the physical action d0 and mu*alpha_L² are genuinely paid. This is ordinary small-window Lindblad/trajectory simulation, not a fast-forwarding assertion. It also gives an explicit ordinary comparator.

## 10. Resource scope and what this conjunction does not acquire

After scaling g to one, overhead is polynomial in

    1+Hs+B+p, h, kappa^-1, alpha_H, alpha_L,
    source/system/register and parameter input bit lengths,
    log(2+mu), log(1/epsilon),

multiplied by actual precision-capable encoding/preparation costs. Positive-parameter logarithms used in precision are part of their input descriptions. Restore original variables using Section 2; in particular B=original b²T/g, mu=original lambda*g*T, h=original h/g and kappa=original kappa/g. The low branch has mu polynomially bounded in these parameters. The high branch has polynomial Scap, O(1+alpha_L) amplification, and only logarithmic rate dependence in the virtual cap and numerical clocks. No explicit source dimension, pi_min, Kraus-label enumeration or free inverse probability sampling appears.

The proof does not acquire psi, a spectral gap, the Lyapunov drift, jump-stack access or coupling from arbitrary matrix data. It does not certify a learned model, expose microscopic jump records, infer physical heat statistics, support consumer-chosen interventions at private jump times, or bypass the action of a noncentered mean. Native source G is retained exactly; there is no precision-dependent replacement by a collision generator. General system and source instruments remain paid operations. Existing LCHS, block encoding, bridge sampling, Hamiltonian simulation and dissipative preparation are strong ordinary ingredients; the claimed contribution here is only this explicitly checked receiving conjunction, pending whole review.

## 11. Finite branch decisions and low-branch budget binding

A sufficient clean parameter interface is nonnegative rational lambda,T, an exactly zero or supplied positive rational/dyadic encoding normalization b, and positive rational certified g,h,kappa,alpha_H,alpha_L. No test of whether an unknown encoded operator is zero is needed: any acquired positive normalization can be used even for a zero operator. The B=0 shortcut is used only from certified zero data; otherwise use that positive normalization and pay its B. T=0 and lambda=0 shortcuts have the same exact-data convention.

For a refinable nonrational parameter interface, branch using an overlap instead of an exact real comparison. The high proof applies above C B and the low proof remains valid below 2 C B, where C=4096max(1,h/kappa)^2. Refine certified parameter intervals until either the high lower test or the low upper test is certified. The overlap makes equality at either original threshold harmless. When positivity itself has not been certified, an upper bound may instead certify that the whole source-plus-coupling action mu*alpha_L²+sqrt(mu*B) is below the allocated error; then simulate H0 alone with that Duhamel error paid. Refinable access and its arithmetic cost are assumptions, not free exact-real tests. Acquired normalizations and certified upper bounds, rather than unavailable exact operator norms, are used in every test.

In Section 9's low branch recompute the count/window call cap S_low, and instantiate e_step, beta, sigma and primitive error subdivisions using S_low and Aamp=8. The high-branch MGF cap is not used there. The uniform-event normalized operator is (L/alpha_L)K0(t)/e, whose derivative norm is at most d0/e; this cancels sqrt(mu) exactly and introduces no inverse-rate normalization. The short-window and private-time hybrid use the same Lphys bound. These observations make the low branch a fully ordinary finite-action alternative with the same retained-input/output convention.
