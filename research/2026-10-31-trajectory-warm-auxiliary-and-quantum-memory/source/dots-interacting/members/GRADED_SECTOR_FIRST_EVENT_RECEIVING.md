# Interacting common-loss reservoirs: acquired sector compiler

31 October 2026. Whole receiving candidate for independent review. This is not an implementation, practical advantage or novelty claim. The precursor `TOTAL_EXCITATION_COMPILER_OPENING.md` remains frozen; its missing explicit Dyson phase is superseded here by (-i)^V for every retained virtual interaction insertion.

## 1. Model, compatibility and paid access

Let N=sum_i a_i^dagger a_i on r bosonic mode registers. The initial reservoir is vacuum. Define

    R_plus=sum_i F_i a_i^dagger, g=sqrt(sum_i f_i^2),
    H=H_f+R_plus+R_plus^dagger, J_i=2sqrt(lambda)a_i,

where lambda>0 is COMMON to all modes and each bounded system-only F_i has a supplied controlled block encoding of normalization f_i>=||F_i||. Their actual selection and precision costs are paid. Different F_i need not commute.

H_f is a compatible selfadjoint direct sum over total-excitation sectors, with [H_f,N]=0. Its restrictions to N<=L agree when L increases; unrelated matrices at different cutoffs are not admissible. Each finite restriction is bounded. A certified bound a_f(L)>=||H_f|_(N<=L)|| and an actual controlled implementation of exp(-it H_f) on that subspace, to any required precision, must be supplied or acquired. Denote its real cost by C_f(L,t,delta). No generic fast-forwarding or exponentially large matrix access is granted.

All physical modes remain in the model even if some F_i=0: H_f may move excitations into those modes and they can emit. Zero coefficients are omitted only from the coupling stack. If g=0 globally, N remains0 and the problem is the supplied H_f|_(N=0) evolution with system controls, not an immigration bridge.

Controls are normal system-only instruments at p prescribed times; arbitrary references and their outcome records are retained. They commute with N. Reservoir states, emission colors and private clocks remain inaccessible to the consumer. Instrument implementation costs are external or added separately.

Use a GLOBAL cutoff N<=L, not separate mode cutoffs as a dynamical boundary. Digital registers may each hold0..L; a coherent sum/predicate marks the valid total-number subspace. Define every arithmetic/unitary routine on the rest of the digital register as an explicit unitary extension or CPTP fallback. No good block normalizes an invalid branch.

## 2. Photon-removal circuit, not just its norm

On a configuration nvec of positive total n,

    V_minus|nvec>=sum_i sqrt(n_i/n)|i>|nvec-e_i>.

The mode index remains part of the output. This is an isometry: V_minus^dagger V_minus=I-P0, since sum a_i^dagger a_i=N. A separate vacuum flag supplies a contraction on the full space.

An actual circuit computes n=sum n_i, prepares the finite index distribution n_i/n from the occupation registers, and decrements the selected occupation. Scratch data concerning the OLD configuration are uncomputed by reconstructing it from the post-configuration and retained index i; old total equals post-total+1. No occupation or within-sector state is measured. The vacuum branch has its own orthogonal failure tag, so it cannot collide with an emitted-photon vacuum output. Conditional shifts have a defined unitary extension; exactly zero n_i receives zero accepted amplitude. Uniform absolute state-preparation errors are apportioned among O(r) rotations/arithmetic operations. This costs polynomial r,log(L+1),input/precision bits, not the number of configurations.

Let W/g be the acquired stacked system contraction

    psi -> sum_i |i> F_i psi/g.

Prepare amplitudes f_i/g, apply the supplied F_i/f_i block controlled by i, and KEEP i rather than unpreparing it. Its squared norm is sum F_i^dagger F_i/g^2<=I. All component success work is retained coherently. Zero f_i is handled directly; no division by zero occurs.

Apply the photon-removal unitary INVERSE to this stack, projecting only its designated index/flag-zero block at final success. On input sector n this implements

    O_plus Pi_n = R_plus Pi_n/[g sqrt(n+1)].

Indeed V_minus^dagger on |i> times a sector-n vector is a_i^dagger/sqrt(n+1). The physical state is not replaced by a sector label. Projection in this description means a block encoding, not an intermediate measurement. A fresh success register is used for every subsequent word factor.

The inverse block encoding supplies O_minus=O_plus^dagger. Consequently on sector n>0,

    O_minus Pi_n=R_plus^dagger Pi_n/[g sqrt(n)],
    ||R_plus^dagger Pi_n||<=g sqrt(n).

Taking its adjoint product gives the DIRECTION required later:

    R_plus R_plus^dagger <= g^2 N.

It is not an assertion about R_plus^dagger R_plus<=g^2 N. At the top cutoff an attempted raising operation is zero; at vacuum lowering is zero. All these flags are exact integer predicates.

## 3. Physical bounds and global-cutoff process

At any finite global cutoff, the number-shift identities hold for R_plus and the common loss. With V=z^N, the adjoint conjugated by V^-1/2 is the sum of

    -4lambda(1-1/z)N

and an interaction term proportional to i(R_plus-R_plus^dagger). Set Q=R_plus^dagger/g, so Q^dagger Q<=N. Replace the negative number term by the less negative -d Q^dagger Q and complete a square. This proves

    Tr(z^N rho(t))<=exp[Gamma*t*(z-1)/4], Gamma=g^2/lambda.

For the jump tilt with z=2e^theta-1 the same square gives

    E exp(theta J_T)<=exp[Gamma*T*(e^theta-1)].

H_f commutes with N, regardless of its cutoff norm. Nonselective system instruments with retained records preserve the number weight. No CCR at the cutoff or normalized-postselection bound is used.

The outgoing global-boundary Hamiltonian block is R_plus Pi_L, of norm at most g sqrt(L+1). Common lowering dissipators and compatible H_f restrictions agree on the embedded smaller subspace. Finite-to-finite Duhamel/trace Cauchy--Schwarz therefore gives vacuum controlled trace error

    2Tg sqrt(L+1) exp(Gamma*T/8) 2^(-L/2).

The independently checked uniform occupation bound may tighten this to

    2Tg sqrt(L+1) 2^(mu-L/2), mu=g^2/(4lambda^2).

Its source is `UNIFORM_OCCUPATION_BOUND_CANDIDATE.md`, SHA136e1cf32b06eac6dbfba53f1e7c4a91783c607233779f2cf7ce55fa234509dd, with receipt SHAa799f1564926c5d0033771cf174257470078eca5831a77d646b2ee369c384430. The uniform estimate is for normalized occupation moments, not for the unnormalized jump-tilted state; the activity cap still grows with Gamma*T.

Choose L>=1 by checking either valid bound, or their minimum, against epsilon/100. The older bound alone suffices for the resource claim, so no unfavorable inverse-small-lambda scale is forced by the optional uniform improvement.

The canonical infinite process is constructed exactly as in the accepted cutoff receiving: extend cutoff inputs by a CPTP projection/reset approximation, prove Cauchy convergence first on finite-number inputs and then extend by contractivity and density. The resulting normal CPTP maps compose and are strongly continuous. Their generators agree with the formal expression on finite-number test operators. H_f compatibility, not an arbitrary uniqueness claim for unbounded extensions, is binding.

For product identification, free exp(-itH_f) exists as its supplied compatible selfadjoint direct sum and preserves every number weight. The interaction R_plus+R_plus^dagger has the same raising bound and decreasing-weight estimate as before. During actual accumulated interaction time u<=U, use z(u)=1+2/(1+u/U); the weighted square bounds moments by exp(2Uu g^2) from vacuum. Free common damping decreases the weight and H_f preserves it. The boundary comparison is uniform in splitting count, so finite-cutoff Lie convergence and cutoff convergence interchange. No analytic-vector bound for arbitrarily growing H_f sector norms is assumed. This provides the canonical interacting process; it does not make H_f cheap to simulate.

## 4. One scalar bridge, quantum sector dynamics retained

Normalize time T to1 and put

    ell=lambda*T, v=g*T, G=g^2*T/lambda=v^2/ell,
    h_f=T*a_f(L).

Because [H_f,N]=0 and loss is common,

    exp[(-iH_f*T-2ell N)t]
       =exp(-it H_f*T) exp(-2ell Nt).

Expand only R_plus+R_plus^dagger. The scalar weights are those of ONE abstract ladder

    M=-2ell n+v(a+a^dagger).

The corresponding positive full kernel E(t) has the already earned normal-ordered finite endpoint formula, with alpha=v(1-e^-2ell t)/(2ell) and c=Gt/2-G(1-e^-2ell t)/(4ell). Its Doob bridge is immigration-death with immigration G/2 and per-particle death2ell. No exponentially large sector matrix is prepared.

Use the accepted direct marked-Poisson bridge (`THINNING_IMMIGRATION_DEATH_BRIDGE.md`, SHAbeb4cfb5a5ae77b096d712d12c7ebdbce1ad2a73de16ffebd1fab65bd444a458). A birth applies the actual O_plus, a death O_minus, with the actual H_f interval unitaries between events. SELECT ALSO applies (-i)^V for every retained virtual interaction insertion. Both birth and death contribute -i; discarded candidate immigrants and the final actual loss jump do not. Compute V modulo4 exactly. This supersedes the precursor's unstated Dyson phase.

A path crossing total L selects zero, without resampling. The inner average is the exact finite-L no-jump block; it does not scalarize the unknown state within a number sector. All occupation-label paths are virtual amplitude sources, not observed physical reservoir trajectories.

## 5. Explicit overlap between unequal-dimensional sectors

Let H_n be the actual joint system/reservoir total-number-n space. Its dimension may differ from H_m. For a scalar positive matrix E_mn and a row/column bound R0, define the accepted parts

    Rsrc: psi_n -> sum_m sqrt(E_mn/R0)|m,n>|psi_n>,
    Lsrc: phi_m -> sum_n sqrt(E_mn/R0)|m,n>|phi_m>.

To build them, coherently compute the physical total number, prepare a finite label list0..L with these probabilities plus failure, and retain the copied total label. They do not prepare any basis within H_n or H_m. Failure tags on the two sides are disjoint. The source labels and identical finite bridge seeds are left unchanged by SELECT.

For source endpoints n,m, the designated good word W_mn maps H_n into H_m. On that part, applying Lsrc^dagger to the physical output uncomputes the source labels using its ACTUAL output total m. Thus the good overlap is

    sum_m,n (E_mn/R0) W_mn Pi_n.

No matrix unit from an artificial scalar space replaces the physical sector-changing word. This formula remains valid when sector dimensions differ: it is a composition of explicit isometries and the acquired contraction block encodings, all with unitary extensions and success flags.

Uniform word errors are controlled by the direct-sum weighted Schur inequality. For input components psi_n, output component norms are at most sum_n E_mn ||psi_n|| times the word error; row/column sums bound the operator norm independently of dimensions. Absolute label-preparation errors instead telescope as isometry errors. No enumeration or union over all within-sector states is used.

## 6. Rectangular jump output and absence of a color normalization

The actual stacked loss isometry is

    Jstack= sum_i |i>J_i =2sqrt(lambda) V_minus sqrt(N).

Its squared norm on sector n is exactly4lambda*n. The retained color register is part of the physical Kraus OUTPUT, not inner source work. It must not be unprepared or projected onto a coherent color sum.

In normalized time define

    B_mn(t)=2sqrt(ell)*sqrt(m+1)*E_(m+1,n)(t), 0<=m<L,
    B_Ln(t)=0.

For right preparation on input H_n, sample post-jump total m with amplitude sqrt(B_mn/w); append the bridge ending at PRE-JUMP total m+1. Apply its word and then V_minus, which produces a vector in C^r_color tensor H_m. The left preparation on this output space acts as identity on color, computes total m, and prepares n with amplitude sqrt(B_mn/w) and the SAME bridge seed for n->m+1. Its inverse removes only the source labels/work, leaving the actual color and post-jump reservoir state.

This rectangular overlap implements Jstack K0(t)/w(t). It does not enumerate r jump blocks and introduces no sqrt(r) normalization. The factor sqrt(m+1) is already in B_mn; V_minus is normalized and must not multiply it a second time. Top output row m=L is zero, since a pre-jump L+1 state is outside the physical cutoff.

The weighted Schur proof now uses input spaces H_n and output spaces C^r tensor H_m; it is unchanged. The known mode-label preparation cost in V_minus remains polynomial r and is paid even though it does not enlarge the scalar normalizer.

## 7. Scalar normalizers and complete first-event isometry

Choose windows tau<=1/[16G(L+1)]. The scalar row/column sums satisfy

    ||E(t)||_(row,col) <= exp(Gtau/2+sqrt(2G L tau))<2.

Use R0=2. Each local row/column is a finite O(L) list evaluated by the positive factorial formula; stable expm1/log arithmetic and absolute probability/rotation budgets are exactly those in the accepted bosonic receiver. There is only one abstract bridge.

The identity aE=e^-2ell t E a+alpha E bounds the stacked jump row/column normalizer by a fixed multiple of sqrt(ell(L+1))e^-2ell t+sqrt(G). The safe envelope

    w(t)=64sqrt(ell(L+1)e^-4ell t+G)

therefore suffices for B. Its total squared mass with the no-event arm is

    4+integral_0^tau w(t)^2dt
       <=4+1024(L+1)+4096Gtau.

Choose a power-of-two A with256sqrt(L+2)<=A<512sqrt(L+2), padding with a zero good-block arm. The outer event time is a known uniform/truncated-exponential mixture; the emission color is generated by V_minus INSIDE the event word, not by a scalar outer distribution depending on an unknown reservoir state.

The exact good block is the COMPLETE first-event isometry divided by A:

    [K0(tau); |t> Jstack K0(t)sqrt(dt)]/A.

Kraus completeness holds on arbitrary retained system/Fock inputs. Its event output includes color; the no-event output has a distinct arm and unused color flag. Keep outer arm/time/color records and all contraction flags coherent until full isometry amplification. Only inner bridge work is unprepared. Never amplify K0 alone as though it were an isometry.

## 8. Finite source, clock and amplification ledger

All following quantities are explicit paid bounds, not oracle promises. Select

    W=ceil(16G(L+1))+p+1,
    M=ceil(G(e-1)+log(100/epsilon))+1, S=M+W+2,
    e_step=epsilon/(1000S), d_A=2A+1,
    beta=(e_step/(10^6 d_A^2))^4, eta=beta/10^6,
    sigma=(beta/[100A(L+2)])^4.

Use finite-generator bounds

    Lambda=1+2h_f+4v sqrt(L+1)+8ell L,
    hE=h_f+2v sqrt(L+1)+2ell L.

Let t_min=min(1,e_step/(100Lambda)). Shorter remaining windows advance to their prescribed boundary by identity with charged error. On longer windows, remove outer-uniform tails and finite mixture-threshold strips of width sigma and set

    t0=(sigma/4)*min(t_min,1/(1+4ell)).

Their error is a COMMON-UNIFORM L2/square-root measure error, not timestamp TV. The normalized stacked event amplitude satisfies

    ||(Jstack K0/w)'|| <=sqrt(ell L)*hE/(32sqrt(G))+2ell.

Take the representative-time accuracy below t0/10, beta divided by100 times one plus this derivative bound, and e_step/(100Lambda). Positive G is binding; the global g=0 branch was handled separately.

For the direct bridge, candidate immigrant count is Poisson(U), U=Gt/2. Put

    Umax=G*tau_max/2, tau_max=min(1,1/[16G(L+1)]),
    Hcap=ceil(Umax*(e-1)+log(100/eta))+1,
    Kcap=2L+2Hcap.

Overflow probability is uniformly <=eta/100 WITHOUT endpoint conditioning penalties. Stable finite survivor-posterior lists, finite Poisson CDF scans, direct truncated-exponential times and candidate lifetime tests supply a fixed polynomial source circuit. The acquired source receipt, not a generic CTMC bridge oracle, supplies these operations.

Set a global boundary/tie/retention cut

    zeta<=min(t0/10,
          eta/[100(Kcap+1)^2(1+2ell+1/t0)]).

Source uniforms are trimmed only with a total probability budget eta/poly(Kcap). All categorical/CDF lists are certified/clipped/normalized; each list and threshold gets its subdivided eta budget. Initial-death and surviving-birth quantiles are1-Lipschitz in duration. Candidate lifetime and retention errors have the stated independent-uniform strip bounds. All draws use the SAME finite outer duration; there is no recursive endpoint denominator.

Choose internal time accuracy

    h_time<=min(zeta/[100(Kcap+1)],
        beta/[100(1+h_f)(Kcap+1)^2]).

There is no separate number-phase oracle now: the actual H_f evolution carries ALL within-sector dynamics, including free frequencies and interactions. Its timing derivative is bounded by h_f. Chronological order, total-cutoff flags and (-i)^V are stable on the retained set. Off it, changing a contraction word costs at most twice bad probability in the INNER operator mean.

Allocate O(beta/(Kcap+1)) aggregate operator error among each O_plus/O_minus implementation, the final V_minus if present, and each H_f interval. Each stack/removal routine further divides its budget among actual component encodings and polynomial arithmetic operations. Failure work remains coherent; a scalar norm bound is not substituted for these circuits.

For B-bit variable duration, a safe implementation uses B controlled fixed-time evolutions exp(-iH_f*T/2^k), allocating interval error across B. Charge all of them in C_f, separately for each of Kcap+1 slots. There is no free2^B lookup table and no automatic optimized additive time cost from the sum of path durations.

After forming the complete block, attenuate by A sin(pi/(4A+2)) and use A ordinary oblivious Grover iterations. The noncommutative Chebyshev/dilation proof gives good-block error O(d_A^2 beta) and leakage O(d_A sqrt(beta)); synthesis and every O(A) base call are paid. The displayed small beta leaves these below e_step.

Read or retain private event/time/color only AFTER amplification. Preserve the reservoir on every branch. Compare against the EXACT finite-L process with a count register frozen at M. Its generator norm has the same Lambda bound up to a fixed constant, independently of count-space dimension. A backward hybrid across at most S calls prices representative-time changes by Lambda times their error, plus local isometry and tiny-window errors. Later prescribed instruments contract. The exact activity bound pays count truncation; no MGF is assumed for the approximate algorithm. All capped/failure branches have unconditional CPTP fallbacks, not normalized successful postselection.

Adding the checked global Fock cutoff and initialization budgets gives error epsilon after fixed universal safety allocations. Inner mean errors and outer L2 errors are not interchanged.

## 9. Honest conditional resource statement

The scalar cutoff, source lists, source/event caps and amplification are polynomial in L,G,p, encoded input lengths, log(2+lambda*T) and log(1/epsilon). Physical registers use r log(L+1) bits plus system and polynomial work. Stacks/removal add polynomial r arithmetic and the actual F_i encoding/selection costs. No sector is enumerated and no source event loop is proportional to lambda*T.

This overhead multiplies the REAL controlled H_f implementation cost, conservatively for every binary-duration slot and amplification call. Precision bits also include log(2+T*a_f(L)). A formal [H_f,N]=0 identity does not provide a circuit. If a_f(L) or C_f grows badly with L, the resulting complete cost can also grow badly. This is not hidden under a general polynomial claim about arbitrary interacting Hamiltonians.

For explicit subclasses with polynomial-L acquired access, the construction is genuinely a polynomial-overhead common-rapid-loss compiler. The next section supplies such a subclass. Inverse tiny coefficient scales used only in numerical precision are charged through finite input descriptions, not through an inverse-rate loop.

Unequal damping with noncommuting mode mixing is excluded: exp[-iH_f t-2sum lambda_i n_i t] would no longer split into scalar total-number damping and the acquired unitary. Generic number-changing H_f, arbitrary nonlinear thermal equilibrium preparations, publicly accessible private bath clocks and adaptive intervention times are not received by this proof.

## 10. Explicit interacting Hamiltonian access

A consequential concrete family is number-conserving Bose--Hubbard plus known self/cross-Kerr terms,

    H_f=H_sys+sum_i Omega_i n_i
        +sum_(i<j)(J_ij a_i^dagger a_j+J_ij* a_j^dagger a_i)
        +sum_i U_i n_i(n_i-1)/2
        +sum_(i<j) V_ij n_i n_j.

Coefficients are finite-description numbers (Omega,U,V real) with their acquisition/precision paid. H_sys is system-only and has supplied block access. These are compatible restrictions of a selfadjoint direct sum. The bath is genuinely interacting/non-Gaussian when Kerr terms matter; the receiver does not replace its within-sector evolution by a scalar.

On the occupation registers, a_i^dagger a_j/(L+1) is an acquired contraction: reversibly calculate sqrt((n_i+1)n_j)/(L+1), prepare its success amplitude, and update the two occupations, with exact zero branches at forbidden shifts. The same construction works coherently on all configurations. Diagonal n_i/L and n_i n_j/L^2 are direct arithmetic-amplitude encodings. Products n_i(n_i-1) are similar. Mode-pair SELECT can scan the explicit O(r^2) list; this cost is paid. On the valid total-number subspace these maps are the desired untruncated operators, since a forbidden per-mode overflow has zero physical hopping coefficient there.

A conservative explicit LCU normalization is

    alpha_f(L)=alpha_sys+L sum_i|Omega_i|
        +2(L+1)sum_(i<j)|J_ij|
        +L^2[sum_i|U_i|+sum_(i<j)|V_ij|].

It bounds the actual restriction and supplies its block encoding, rather than merely a numerical norm estimate. Standard controlled qubitization then supplies exp(-itH_f) with O(alpha_f(L)*|t|+log(1/delta)) queries to that acquired encoding, with the ordinary coefficient preparation/arithmetic and phase-synthesis costs paid. This ordinary ingredient is credited to Low--Chuang, *Hamiltonian Simulation by Qubitization*, primary abstract and normalized block-input formulation: https://arxiv.org/abs/1610.06546 . The theorem is not attributed to this construction.

Thus the concrete whole cost is polynomial in the acquired coefficients' ordinary action scales, r,L and target precision, and only polylogarithmic in the separate common damping scale through L and bit work when those other physical resources are fixed. It is NOT automatically logarithmic in arbitrary large hopping/Kerr/frequency coefficients.

There is a stronger SPECIAL diagonal case. If J_ij=0 and the bath part is a known diagonal polynomial in occupation, it commutes with H_sys. Compute its value on the occupation registers, multiply by the binary duration, reduce modulo2pi and apply a finite phase rotation. This costs polynomial r,log(L+1),coefficient magnitude/input bits and log(1/delta), plus ordinary H_sys simulation. Large known diagonal Kerr or number frequencies then enter only logarithmically. Adding noncommuting hopping invalidates that simple factorization; the safe general qubitization bound above pays alpha_f action. A better interaction-picture treatment would require its own earned interface, not an assumed fast-forwarding theorem.

## 11. Limited organizing corollary

The algebra uses an integer grading, compatible grade-preserving H_f, acquired raising blocks with norm g sqrt(n+1), and an acquired lowering isometry V with V^dagger V=I-P0 and stacked jump2sqrt(lambda)V sqrt(N). CCR and Gaussianity are not used in the scalar bridge or weighted square. A different efficiently acquired graded model satisfying these EXACT interfaces can receive the same compiler overhead. This is conditional access, not a claim that operator norms construct a circuit. Concrete bosonic stack/removal operations and the explicit interacting subclass above remain the proved central model; additional hard-core or other realizations require their own interface check.

The original precursor and all previously reviewed source archives are preserved. Whole acceptance of this receiving conjunction requires a separate independent read.
