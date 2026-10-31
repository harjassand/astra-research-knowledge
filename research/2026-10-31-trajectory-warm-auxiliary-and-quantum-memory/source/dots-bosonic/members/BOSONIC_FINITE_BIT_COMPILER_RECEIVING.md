# Many retained damped bosonic modes: finite-bit compiler receiving

31 October 2026. Candidate for independent whole review. This is a constructive mathematical-existence claim only, not an implementation, practical crossover or novelty claim. Accepted infinite-domain/thermal files and previously delivered archives are unchanged.

## 0. Binding premises

Receive the normal infinite-Fock process and sharp controlled cutoff bound from `INFINITE_FOCK_CONTROLLED_LIMIT.md`, SHA256 a250c6ff320d19e86f28406d432c698c54f4ff71c9cab5dfaa0b2681f04501a2, and its domain/thermal receipt SHA256 1f88af1848bd3ad8587f5977da016a5c66e9ae746219c4a565146ecbd33f70ba. Thermal modes may first be doubled by `THERMAL_VACUUM_CONTROLLED_REDUCTION.md`, SHA256 61085d944aa7d27aaea552582fb13eb02f26b50d42f847e31bd34296373c2403, with the factor2nbar+1 paid. Virtual detector counts are not physical thermal heat/count records.

The direct bridge source is `THINNING_IMMIGRATION_DEATH_BRIDGE.md`, SHA256 beb4cfb5a5ae77b096d712d12c7ebdbce1ad2a73de16ffebd1fab65bd444a458. Its exact particle construction, stable posterior arithmetic, endpoint-independent count cap and conditional density bounds are used below. No bridge or Kraus oracle is assumed.

The complete-isometry attenuation/amplification identity and common-uniform private-clock hybrid are the algebraic primitives already proved in the finite-mode compiler. Their new bosonic normalizations, source bounds, phase errors and finite resource accounting are earned here explicitly.

## 1. Input model and normalized time

There are r retained vacuum modes with positive damping lambda_i and positive supplied coupling normalizations Gamma_i. Exactly zero-coupling vacuum modes are omitted: they remain vacuum under every system-only control. They are not passed through a vanishing endpoint bound. The thermal zero-temperature auxiliary is likewise omitted. The nontrivial physical interaction has coefficients sqrt(Gamma_i lambda_i)U_i, where U_i is a bounded, possibly non-Hermitian system contraction with an actual precision-capable controlled block encoding. U_i and U_j need not commute. Its adjoint is supplied by the inverse block encoding. All selection costs are paid; a norm inequality alone is not access.

Scale physical time T to1. Write

    b_i=Gamma_i*T, ell_i=lambda_i*T, omega_i=Omega_i*T,
    G=sum b_i, h=alpha_H0*T, g_i=sqrt(b_i*ell_i).

The finite model on occupations0..L has

    H_L=H0*T+sum omega_i n_i
          +sum g_i(U_i a_i^dagger+U_i^dagger a_i),
    J_i=2sqrt(ell_i)a_i.

Choose integer L>=1 by checking the accepted explicit bound

    2sqrt((L+1)sum b_i ell_i) exp(G/8) 2^(-L/2) <=epsilon/100.

This costs a logarithmic scalar test, with L=O(G+log(2+sum b_i ell_i)+log(1/epsilon)). For G=0 all retained modes disappear and only ordinary H0/control evolution remains. The joint Fock dimension (L+1)^r is never enumerated; use r registers of log(L+1) bits.

All guarantees below concern accessible systems, arbitrary references and records of p instruments at prescribed times. The physical reservoir and private jump times are inaccessible. Instrument gate costs are external or added separately. Thermal parameter acquisition and any continuum-bath fitting errors are separate inputs, not supplied by this compilation theorem.

## 2. Exact positive word representation

For each mode put

    M_i=-2ell_i n+g_i(a+a^dagger), E_i(t)=exp(M_i t).

Its Perron transform is the immigration-death chain with immigration nu_i=b_i/2 and per-particle death delta_i=2ell_i. The explicit bridge in the source file samples its endpoint-normalized positive Dyson paths. Distinct mode paths are independent before their event lists are merged. Sorting the union gives the exact chronological system word by the shuffle/Fubini identity; noncommuting U_i are not reordered.

Every birth applies U_i and every death U_i^dagger in that word. Each such VIRTUAL interaction insertion also contributes -i from the Hamiltonian Dyson expansion, for both raising and lowering; SELECT therefore includes the exact scalar (-i)^V, where V counts retained virtual interaction events (not discarded candidate immigrants or padded slots). An actual damping jump J_i has no additional -i and is not counted in V. Scalar ladder factors sqrt(n+1),sqrt(n) and damping intervals are already included in the positive path weights. H0 evolutions occupy the intervals between sorted events. Known number frequencies give the scalar path phase

    exp[-i sum_i omega_i integral_0^t n_i(s)ds].

A path touching occupation L+1 selects zero good block at once, without resampling or normalizing survival. Thus the untruncated E_i remain positive majorants, while the averaged selected word is EXACTLY the finite-cutoff no-jump contraction. Paths may be killed before later returning to an allowed endpoint; zeroing their full word is essential.

The untruncated positive exponential is well defined (a displaced negative number operator plus a scalar). Its normal-ordered entries are

    alpha_i(t)=g_i(1-exp(-2ell_i t))/(2ell_i),
    c_i_exact(t)=b_i*t/2-b_i(1-exp(-2ell_i t))/(4ell_i),
    (E_i)mn=exp(c_i_exact) sqrt(m!n!)
       *sum_{k=0}^{min(m,n)}
           alpha_i^(m+n-2k) exp(-2ell_i*t*k)
             /[(m-k)!(n-k)!k!].

This finite positive sum computes each required endpoint entry m,n<=L; no joint-state matrix or cancellation-prone signed sum is needed.

## 3. Local row/column preparation and finite arithmetic

Use control-free windows tau<=1/[16rG(L+1)], split at prescribed controls. Define the enclosing local normalizers

    c_i=exp[b_i*tau/2+sqrt(2b_i*tau*L)], C=product c_i.

Rows and columns of the compressed E_i(t), t<=tau, are bounded by c_i, since normal ordering gives exp(c_i_exact+2alpha_i sqrt L). Consequently

    C<=exp[G*tau/2+sqrt(2rG*tau*L)]<2.

Use global no-event normalizer R=2. The right isometry on physical endpoint n prepares accepted amplitudes sqrt(E_mn/R), and the left on physical endpoint m prepares sqrt(E_mn/R) with the SAME endpoint workspace. Build these as products of local L+1-outcome preparations with probabilities E_i/c_i, local failure outcomes, and a global flag of probability C/R on both sides. Right and left failure spaces have distinct tags, and SELECT has zero good block there. Copying Fock basis labels is a reversible isometry preserving arbitrary superpositions, not a measurement of the reservoir.

Append to both sides IDENTICAL finite bridge seed registers and compute the same endpoint-conditioned path/transcript. SELECT preserves those labels and applies the chronological system word and phase. Inverse preparation removes the INNER source work. The overlap is the positive endpoint entry times its conditional word mean; hence the physical block is K0(t)/R. Independent seeds on the two sides would give the wrong operator and are forbidden.

Compute the local entries by the finite factorial sum. Factorials involve integers<=L; use exact products or guarded log arithmetic. For small x=2ell_i t evaluate (1-exp(-x))/x and1-(1-exp(-x))/x by stable series/expm1. For large x only nonpositive exponentials are evaluated. Individual negligible terms are discarded at an absolute entry-error allocation. Positive exponents c_i_exact are bounded by b_i*tau/2. All entry computations have polynomial L and bit complexity; no loop of ell_i*t is used.

To prepare a local probability vector with isometry error delta, compute its O(L) probabilities to absolute O(delta^2/poly(L)), clip/normalize to a genuine distribution, and synthesize its finite rotation chain. A residual branch below its absolute-error mass budget can be ignored; otherwise its normalization is bounded below by that budget. Product-isometry errors telescope over r factors. Choose local and global preparation errors totaling at most beta/100, with all arithmetic and gate costs charged.

For bridge errors, use the operator-valued weighted Schur bound: if every endpoint word mean has error<=eta, the entry errors are bounded by eta times the nonnegative kernel. Its row/column sums then give normalized block error<=eta. This avoids summing errors over (L+1)^(2r) endpoints. Absolute row-preparation errors are instead controlled by isometry telescoping, not assumed relative to tiny entries.

## 4. Actual first-jump row/column blocks

For event i define its local positive matrix

    B_i(t)mn=2sqrt(ell_i)*sqrt(m+1)*(E_i(t))_(m+1,n),
          0<=m<L, 0<=n<=L,
    B_i(t)Ln=0.

The virtual bridge endpoint on this mode is PRE-JUMP occupation m+1. The physical output is m. Other mode endpoints are unchanged. Both preparation sides compute the same pre-jump string; on the zero row m=L the source selects zero. The physical ladder lowering factor is in B_i, not dropped from the operator amplitude.

The identity aE_i=exp(-2ell_i t)E_i a+alpha_i E_i, applied as an upper bound on the compressed nonnegative blocks, gives local row/column bound

    c_i[2sqrt(ell_i L)exp(-2ell_i t)+sqrt(b_i)].

Choose local event normalization

    d_i(t)=8c_i sqrt(ell_i(L+1)exp(-4ell_i t)+b_i),

and global event envelope

    w_i(t)=64sqrt(ell_i(L+1)exp(-4ell_i t)+b_i).

The event product normalization is d_i product_{j!=i}c_j=8C sqrt(...), less than w_i/4. Product left/right isometries, with the corresponding global flags and identical bridge seeds, therefore implement J_iK0(t)/w_i(t). The physical Fock output is retained, not reset to vacuum.

The complete first-event isometry has no-event arm K0(tau) and event arms J_iK0(t)sqrt(dt). Its normalization mass is bounded by

    R^2+sum_i integral_0^tau w_i(t)^2 dt
       <=4+1024r(L+1)+4096G*tau.

Choose a fixed enclosing integer power of two A with

    256sqrt(r(L+1)+1)<=A<512sqrt(r(L+1)+1).

Pad by a zero good-block arm to exactly A. This is a deliberately conservative polynomial normalization, not an optimized constant.

Prepare outer arm/type uniforms coherently with weights R^2/A^2, integral w_i^2/A^2 and the remaining zero mass. Conditional event times are a mixture of uniform on[0,tau] and truncated exponential of rate4ell_i. All integrals use stable expm1 and positive sums. Retain outer type/component/uniform/time labels through amplification; unprepare only the INNER bridge words. Their common-uniform Kraus norm is exactly1/A before approximation. No no-jump contraction is normalized as if it were an isometry.

## 5. Global caps and finite budgets

The accepted finite-cutoff jump bound is E exp(N)<=exp[G(e-1)]. Let

    W=ceil(16rG(L+1))+p+1,
    M=ceil(G(e-1)+log(100/epsilon))+1,
    S=M+W+2, e_step=epsilon/(1000S),
    d_A=2A+1,
    beta=(e_step/(10^6 d_A^2))^4,
    eta=beta/10^6,
    sigma=(beta/[100A(r+1)(L+1)])^4.

M counts ACTUAL reservoir jumps; virtual bridge counts have a separate cap. Every error group below is allocated a fixed fraction of beta or e_step as specified; polynomially many suboperations divide that group budget rather than each receiving it in full.

A dimensionless finite physical generator bound is

    Lambda=1+2h+2L sum_i|omega_i|
             +4sqrt(L)sum_i sqrt(b_i ell_i)+8L sum_i ell_i.

The no-jump generator norm is bounded by

    hE=h+L sum_i|omega_i|
          +2sqrt(L)sum_i sqrt(b_i ell_i)+2L sum_i ell_i.

Set t_min=min(1,e_step/(100Lambda)). Remaining windows shorter than this are advanced to their prescribed boundary by identity with a charged error. Otherwise tau>=t_min.

Remove outer uniform tails and finite arm/component threshold strips of width sigma. Their measure is O((r+1)sigma) and their common-uniform L2 block cost is its square root. Set

    t0=(sigma/4)*min(t_min,1/(1+4sum_i ell_i)).

Both event-time endpoint distances exceed a safe multiple of t0 on retained uniforms; no-event durations are at least t_min. Finite probability/rotation arithmetic is budgeted so these inequalities retain slack. There is no assumption of a global minimum physical waiting time.

For the normalized event amplitude Fi=J_iK0/w_i, a bound is

    ||Fi'|| <= sqrt(ell_i L)*hE/(32sqrt(b_i))+2ell_i.

All retained b_i are positive. Choose outer representative-time error

    dt <= min(t0/10,
              beta/[100(1+sum_i||Fi'||)],
              e_step/[100Lambda]).

At fixed outer uniform, the truncated-exponential quantile has derivative at most tau/sigma. Evaluate finite words and logs to meet dt. This prices small b_i and large rates/frequencies through their input and precision logarithms, not through a number of microscopic events. Exact zero-coupling modes were removed instead of dividing by zero.

## 6. Uniform direct-bridge caps and rounding

For any outer time t>=t0 and all endpoint strings, total candidate immigrant count is Poisson(U), U=G*t/2. Use

    Umax=G*tau_max/2, tau_max=min(1,1/[16rG(L+1)]),
    Hcap=ceil(Umax*(e-1)+log(100/eta))+1,
    Kcap=2rL+2Hcap.

The exact conditional bridge has at most Kcap events except on candidate-count overflow of probability<=eta/100, uniformly in endpoint strings. No endpoint-probability divisor appears. Candidate counts are sampled by finite Poisson CDF scans, with a global Hcap counter; overflow selects zero good block.

Posterior initial survivor lists are evaluated by the source's relative log weights and log-sum-exp. Compute each list with TV error<=eta/[100(r+1)], and similarly allocate all Poisson CDF and source-uniform threshold errors. Finite lists are certified/clipped/normalized. Both preparation sides use the same arithmetic. There is no runtime search for a rare endpoint and no enumeration of all endpoint strings.

Let delta_max=2max ell_i. On the capped draws, the source density bounds give a single global boundary/tie/retention cut. Take

    zeta <= min(t0/10,
        eta/[100(Kcap+1)^2(1+delta_max+1/t0)]).

This union includes cross-mode pairs and the correlated birth/death pair of each candidate; the latter is bounded using its lifetime density. All draws already have the exact conditioned law, so no later multiplication by tiny endpoint inverses occurs.

There are O(Kcap+r) source uniform words. Remove tails of width at most eta/[100(Kcap+r+1)] for each where needed by inverse-log precision. This costs at most a fixed fraction of eta. Truncated-exponential time quantiles have derivative<=t/sigma_inner on the retained uniforms and duration derivative in[0,1]. Candidate birth times are linear in their uniforms. Candidate lifetimes are first tested against the endpoint using the independent survival uniform; rejected candidates need not have large lifetimes represented. Test-threshold strips and finite log errors are charged explicitly to the source budget.

Choose an inner time error h_time satisfying

    h_time<=min(zeta/[100(Kcap+1)],
       beta/[100(1+h+max_i|omega_i|)(Kcap+1)^2]).

All time arithmetic is direct at the SAME finite outer duration. There is no recursive first-event duration whose denominator could deteriorate. Finite source distributions are coupled at that duration; changing the external duration is handled by the outer amplitude/future comparison, with the source lemma's explicit duration coupling available as an independent check.

Sort the at most Kcap events reversibly with padded slots. On the retained set, order and cutoff-crossing flags are stable. On its complement SELECT may produce any contraction or zero, costing at most twice the bad probability in the INNER operator mean. Count/time overflow flags are kept distinct and never postselected away.

## 7. Word phases, operator synthesis and coherent variable duration

The total scalar phase is (-i)^V times the number-evolution phase. Compute (-i)^V exactly from V modulo4 and apply its controlled phase in SELECT; this has constant phase precision cost and its integer counting is included. Omitting it changes the no-jump map already at first order. The number phase is computed from integers and times:

    integral_0^t n_i(s)ds
       =n_final,i*t-sum_(events j of i)sign_j*t_j.

Here n_final is the VIRTUAL BRIDGE endpoint: in an actual first-jump arm it is the pre-jump occupation m+1 on the jumping mode, not the physical post-jump m. The jump itself occurs after the no-jump interval and contributes no extra free-evolution duration. Using the post-jump occupation in this formula would introduce an erroneous frequency phase.

Uniform event-time error h_time changes its argument by at most O(Kcap*max|omega_i|*h_time), safely below the conservative timing budget. This explicitly prices high-frequency phase sensitivity. Compute the phase modulo2pi with certified arithmetic to its allocated error; large known omega_i contribute logarithmic magnitude/precision bits. A known diagonal number rotation is not a generic fast-forwarding oracle.

H0 interval errors telescope through contraction words. A conservative O((Kcap+1)^2 h_time*h) bound suffices for timing. Allocate each of Kcap system insertions and Kcap+1 H0 intervals synthesis/block error at most beta/[10^4(Kcap+1)], and apportion row/column preparation, phase arithmetic and source-basis work to their beta/100 groups. If only separate U_i encodings are given, selected-color operations may scan all r encodings; pay their sum rather than assuming a free SELECT.

Each B-bit duration uses B controlled fixed-time H0 evolutions via binary decomposition, with error divided among the pieces. Charge each slot at a known enclosing time bound, including all B controls and precision work. No table of2^B durations and no optimized additive action cost is assumed. Reservoir ladder shifts and occupancy/cutoff tests are exact finite-register arithmetic; source weights already include their sqrt(n) factors.

Uniform endpoint-wise source and word errors give a uniform normalized block error through the weighted Schur estimate. Uniform control-input errors in each local arithmetic/preparation circuit give the same operator bound on coherent endpoint/time superpositions. Work is computed reversibly, retained through SELECT and uncomputed afterward. Only inner work is erased; actual reservoir memory is never erased.

## 8. Isometry amplification and exact capped-future hybrid

The complete ideal good block is B=V_first/A, with B^*B=I/A^2 on arbitrary physical system/Fock inputs. Attenuate it by c_A=A sin(pi/(4A+2))<1 and use A standard oblivious Grover iterations. The ideal amplitude becomes exactly1.

For a rectangular block, the selfadjoint dilation and noncommutative Chebyshev difference identity bound good-block perturbation by d_A^2*beta. Unitarity bounds failure leakage by O(d_A sqrt(beta)). The displayed beta, with finite-group allocations, makes these smaller than e_step. Attenuation/phase synthesis and all O(A) calls are separately charged. No scalar singular-value derivative is substituted for operator robustness, and no successful branch is normalized by postselection.

Only after COMPLETE amplification may the private type/time record be read or retained for iteration. The actual post-jump Fock state, all no-event Fock coherences and system/reference correlations survive. The consumer receives neither the source path nor the private time.

Compare to the exact finite-L process augmented by a count register and frozen after M jumps. Its generator norm is bounded by a fixed multiple of Lambda, independently of the counter dimension. Hence its exact future channel is Lipschitz in the remaining duration of the current control-free window. Later prescribed instruments contract trace distance. A backward hybrid through at most S calls charges each isometry error, Lambda*dt, and Lambda*t_min for a skipped tiny window. Outer continuous and finite timestamps are compared on a retained common-uniform L2 space, never by a false TV/diamond comparison exposing the timestamps.

The exact finite-L MGF pays the count cap. No MGF is assumed for the approximate implementation. Every overflow/failure branch and the deterministic call cap has an unconditional CPTP fallback, with the preceding error bounds; no exceptional-path expected duration is invoked. Adding the accepted infinite-Fock cutoff error and finite initialization/synthesis budgets gives controlled-output trace error at most epsilon after fixed universal safety constants.

## 9. Resource statement and exclusions

The selected cutoff L, window/call bounds, candidate/event caps, finite lists and precision words are all polynomial in

    r, 1+G+h+p, supplied encoding/input lengths,
    log(2+sum ell_i), log(2+sum |omega_i|), log(1/epsilon),

with physical couplings/thermal factor2nbar+1 included in G and small positive parameter scales paid through their encoded lengths. Source preparation uses r local O(L)-sized lists and polynomial capped marked-event arithmetic. It does not enumerate (L+1)^r states or draw a number of events proportional to rapid damping/frequency. Amplification has A=O(sqrt(r(L+1)+1)); all its base calls, inverses and source work are included.

Supplied system operator encodings, actual H0 simulation and consumer instruments are paid. Dense large-system matrices are never exponentiated. This is an existence-level polynomial resource statement, not an explicit elementary-gate count, optimized exponent or practical advantage. It assumes known finite damped modes and their parameters; general continuum spectral fitting and physical bath acquisition are not free.

The accepted target is the canonical infinite-Fock process, initialized in vacuum or the exactly received finite thermal product state, with private reservoir memory and prescribed-time system controls. No public bath trajectory, thermal heat-count statistics, arbitrary adaptive intervention times, unpriced nonstationary infinite-energy preparation, or normalized rare-postselection guarantee is supplied. Whole compiler acceptance requires independent binding of this body and its source/domain premises.
