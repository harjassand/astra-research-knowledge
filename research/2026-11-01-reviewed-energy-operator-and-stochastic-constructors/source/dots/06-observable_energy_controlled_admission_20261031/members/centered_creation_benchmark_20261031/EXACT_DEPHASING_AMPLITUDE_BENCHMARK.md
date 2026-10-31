# Exact paid-resource benchmark for centered source creation

31 October 2026. Independent derivation by challenge_graph_profile_compiler at the parent's request. This is a two-qubit benchmark and an ordinary-method comparison, not a new fault-tolerance threshold, a quantum advantage, or a hardware claim. All previously reviewed author sources remain unchanged.

## 1. Model, exact reduction and normalization

A source qubit starts in |0>, its specified Markov field is initialized, and a data qubit is arbitrary, possibly entangled with a reference. During one interval [0,T],

    H=c X_source tensor Z_data,
    L=sqrt(lambda) sigma_minus_source tensor I_data,
    lambda>0, c>=0.

There are no additional controls, injection or hopping in this benchmark. Dissipators use D[L](rho)=L rho L* - {L*L,rho}/2. Thus the source's population loss rate is lambda and its X coherence decays at lambda/2, not lambda or 2lambda.

Data populations are unchanged. Let chi(t) be the source operator multiplying an initial data off-diagonal entry. It starts at |0><0| and satisfies

    chi'=-ic{X,chi}+lambda D[sigma_minus](chi).

Define f=Tr chi and x=Tr(X chi). Direct adjoint calculation gives

    f'=-2ic x,
    x'=-2ic f-(lambda/2)x.

Consequently

    f''+(lambda/2)f'+4c²f=0,
    f(0)=1, f'(0)=0.

The reduced data channel is exactly

    E_T(rho)=(1-p)rho+p ZrhoZ,  p=(1-f(T))/2.

Complete positivity ensures f is real and -1<=f<=1, hence 0<=p<=1. These are full channel identities, not a calculation for only one unentangled data state.

Writing a=lambda/4 and d²=a²-4c², the exact solution is

    f(t)=e^(-at)[cosh(dt)+(a/d)sinh(dt)].

At d=0 use f=e^(-at)(1+at); for d²<0 use the equivalent real trigonometric expression. There is no overdamped-only assumption in the ODE or subsequent bounds.

## 2. Explicit finite-rate probability bounds

Variation of constants yields

    f'(t)=-4c² integral_0^t e^[-lambda(t-s)/2] f(s) ds.

Put

    I(T)=2T/lambda-4(1-e^[-lambda T/2])/lambda²,
    p0(T)=2c² I(T)
         =4c²T/lambda-8c²(1-e^[-lambda T/2])/lambda².

Since |f(s)|<=1, |1-f(t)|<=4c² I(t)=2p0(t). The nonnegative function p0 is increasing. Inserting 1-2p0(T)<=f(s)<=1 into the double-integral formula for p gives the rigorous finite-rate bracket

    max(0,p0(1-2p0)) <= p <= min(1,p0).                (A)

The potentially negative lower expression is simply replaced by zero. No small-c or large-lambda approximation was used to establish (A).

A fully rational, somewhat weaker certificate is useful for exact executable checks. For rational lambda,c,T define

    U=4c²T/lambda,
    A=max(0,U-8c²/lambda²).

Then

    A max(0,1-2U) <= p <= min(1,U).                   (B)

For U<=1/2 this follows directly from the positive-kernel comparison f(s)>=1-2U; for U>1/2 the lower bound is zero. This avoids evaluating an exponential to certify the bracket.

In particular, under the explicit relaxation/small-error conditions

    lambda T>=4,  8c²T/lambda<=1/2,

we have A>=U/2 and 1-2U>=1/2, so

    c²T/lambda <= p <= 4c²T/lambda.                  (C)

The exact first-order coefficient is sharper: whenever lambda T tends to infinity and c²T/lambda tends to zero, (A) gives p~4c²T/lambda. At very short times instead, p~c²T². One must not apply the long-relaxation estimate uniformly through T=0.

The data-channel diamond distance from the identity, in the convention without a factor 1/2, is exactly 2p. The upper bound follows from E-I=p(Ad_Z-I), and the data input |+> attains trace-norm difference 2p.

## 3. Optimizing the ideal environment does not remove the amplitude scale

Let V be any pure initialized Stinespring isometry for this exact channel, with the source and emitted field retained as part of its environment. Because data basis populations never change,

    V|0>=|0>|e0>,  V|1>=|1>|e1>,
    ||e0||=||e1||=1,  <e1|e0>=f=1-2p.

Any environment unitary changes both vectors together and preserves this overlap. For an arbitrary unit ideal environment output |e>, define V_id|z>=|z>|e>. Then

    ||V-V_id|| = max(||e0-e||,||e1-e||).

The average of the two squared distances is at least

    2-||e0+e1||=2-2sqrt(1-p).

For p<1, choosing the normalized bisector of e0 and e1 makes the distances equal and attains that lower bound. At p=1, the same limiting value is attained by a phase-orthogonal choice. Therefore the EXACT optimized initialized-isometry distance is

    d_min = sqrt(2-2sqrt(1-p)),
    sqrt(p) <= d_min <= sqrt(2p).                    (D)

The ideal environment must be independent of the data input. Allowing it to encode the data would no longer be an ideal identity-channel dilation.

For p<=1/2, even optimizing over a data unitary cannot improve (D). Apply the isometries to a maximally entangled data-reference input. The noisy reduced state has eigenvalues 1-p and p on two orthogonal Bell states. Its overlap with any pure ideal-unitary Choi state is at most 1-p. The joint-vector overlap with any ideal environment is thus at most sqrt(1-p), proving the same lower bound; the identity/bisector construction attains it.

Combining (C) and (D),

    d_min >= c sqrt(T/lambda),
    d_min <= sqrt(8) c sqrt(T/lambda)

in the stated finite-rate window. More sharply, in its small-error asymptotic regime d_min~2c sqrt(T/lambda).

For the one selected interval in the actual common jump-history dilation, the inclusive fault operator is W(c)-W(0). The zero-coupling evolution leaves the cold source and its field in a fixed environment state and acts identically on data. Hence

    ||W(c)-W(0)|| >= d_min >= sqrt(p).

This lower bound holds regardless of whether that particular zero-coupling environment state is the optimal bisector. It does NOT assert equality between a physical common-history fault amplitude and sqrt(p), nor identify fault amplitudes with probabilities. A universal claim that this one-location amplitude is O(c²T/lambda) would fail in the small-error window.

This one-location witness is sufficient to obstruct a uniformly better per-location amplitude scaling. It does not prove a new threshold, an optimal constant in the all-selected-set upper bound, or a lower bound on the performance of a code with active correction.

## 4. Fixed diffusion and paid resources

For c=sqrt(lambda)b with fixed b,T>0, the exact roots show

    f(T) -> e^(-8b²T),
    p -> (1-e^(-8b²T))/2.

Thus raising lambda does not make the physical disturbance vanish. For b²T small, p~4b²T and d_min~2b sqrt(T). At fixed c, by contrast, increasing lambda suppresses the disturbance with the scale above.

Within (C), a target initialized-isometry/fault-amplitude upper eta forces the necessary condition lambda>=c²T/eta². A data-channel diamond-error target epsilon is a DIFFERENT resource requirement, involving p rather than sqrt(p). These statements hold only for this unchanged apparatus, time interval and task; arbitrary active decoupling, error correction, alternate targets or altered couplings are not ruled out.

## 5. Ordinary exact and effective comparators

This benchmark has an especially strong ordinary alternative. Its logical process is exactly a symmetric telegraph Hamiltonian c xi(t) Z with flip rate lambda/4 and stationary initial sign, under system-only interventions. Indeed the reduced operator pair

    r=Tr_source rho,  y=Tr_source(X rho)

obeys r'=-ic[Z,y] and y'=-ic[Z,r]-(lambda/2)y, the same closed two-moment hierarchy as that classical process, with y(0)=0. System-only operations act identically on both components. This does not identify raw quantum source outputs or allow arbitrary source controls. A scalar ODE or constant-size channel calculation already solves the present benchmark; it is not a computational advantage example.

The damped-qubit second-order mechanism itself is established. Zanardi, Marshall and Campos Venuti, Proposition 3 and Eq. (5), give an effective dissipator 4g² tau D[L] from coherently coupled amplitude-damped qubits. Here g=c, tau=1/lambda and L=Z, giving 4c²/lambda D[Z], exactly the coefficient checked above. Their Proposition 1 supplies a scaled effective-semigroup estimate on the steady-state subspace. The cited result is not itself an every-selected-location common-dilation amplitude certificate. [Primary text](https://arxiv.org/html/1506.04311).

Reiter and Sørensen's effective-operator formula likewise gives L_eff=L H_NH^(-1)V_+. With H_NH=-i lambda Q/2 in this fixture, it yields an effective jump of magnitude 2c/sqrt(lambda) times Z and zero effective Hamiltonian, up to a physically irrelevant jump phase. That is ordinary weak-drive elimination, not a new derivation of the scale. Its stated reduced-master-equation approximation does not alone establish a uniform all-order fault-path bound for an arbitrarily long controlled network. [Primary text, Eqs. (3)–(5)](https://arxiv.org/html/1112.2806).

Popkov et al. explicitly retain weak effective dissipation in the strong-dissipation/Zeno regime; the projected dynamics is not generally frozen. Their stated preparation/finite-system asymptotic scope must not be promoted to our all-selected-set interface. This reinforces the interpretation that nonvanishing second-order noise is expected, rather than a failure of elimination theory. [Primary text, Section II](https://arxiv.org/html/1806.10422).

## 6. What leverage remains against microscopic fault-tolerance priors?

Ng and Preskill's Gaussian theorem already derives local fault-amplitude control from a two-point correlation integral, with epsilon²=2e times a maximum location-versus-whole-computation integral. For exponentially decaying local covariance of size c² and correlation time O(1/lambda), it already gives the scale c sqrt(tau/lambda), not c tau. However its Wick/free-field hypothesis is substantive. A source-qubit X observable has <X²>=<X⁴>=1 in the cold state, whereas a centered Gaussian variable with variance one has fourth moment three. Merely measuring the same two-point decay cannot license applying that theorem to arbitrary qubit networks. [Primary text, Section III and Wick-dependent derivation](https://arxiv.org/html/0810.4953).

Preskill's non-Gaussian correlated-Hamiltonian result already uses the inclusive norm premise ||E(I_r)||<=epsilon^r and controls collective interactions by summed operator norms. It permits very general bath states/dynamics. Directly inserting this benchmark's system-bath coupling yields a local instantaneous-norm quantity of order c tau; rapid source relaxation does not automatically shrink that norm. A stronger application would have to earn a transformed interaction or all-order correlation bound, not silently insert an effective reduced-channel rate. [Primary text, Section 2/Theorem 1](https://arxiv.org/html/1207.6131).

The meaningful scoped delta of the accepted clamped-weight work is therefore an explicit sufficient finite-rate all-selected-set initialized-dilation amplitude certificate for its restricted dissipative source structure, with arbitrary finite initial source correlations and all real outside creating interactions retained; its source-derived extension also pays D/kappa and actual local matrix/circuit support certificates. This is not a new threshold or a new Zeno/elimination mechanism. It is not proved superior to an equally informed stronger microscopic analysis. Gaussian methods can be stronger where their hypotheses truly hold; exact small-system or telegraph calculations plainly win this benchmark.

A global reduced-channel error bound of size delta does not by itself imply epsilon^k for every selected set of k locations, especially with a retained source, arbitrary gaps and outside interactions on. That missing local high-order interface is the precise obstruction to treating the cited elimination theorem as an automatic full replacement. Conversely, absence of such an explicit interface in these inspected results is not proof of historical novelty or of impossibility of deriving it with ordinary methods.

## 7. Executed evidence and its limits

`check_benchmark.py` performs exact SymPy verification of the closed equations, exact rational isometry geometry, and rational finite-rate certificates; it also compares the closed ODE with a full 16-dimensional two-qubit Liouvillian in 45 floating-point cases. All 146 checks pass. The dense numerical comparisons are diagnostics, not certified approximations to the exact channel. The finite-rate bounds themselves follow from the analytical inequalities and exact rational arithmetic. No experimental or gate-execution claim is made.

The primary texts above were actually opened at the indicated equations/sections. No denied full text or alternate-copy bypass was used. This is a focused strongest-route comparison, not an exhaustive priority survey.
