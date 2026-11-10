Rare-event power comparison for conversion segments
and an actual stationary transfer on a scalar birth/death class
10 November 2026 UTC / 11 November Brisbane

1. Precise inherited setting.

Use the actual-binding reference construction of the completed elementary return and ROOT_BIMOLECULAR_CONVERSION_SEGMENT_ENTROPY_20261110.txt. Start reference and actual processes at the SAME fine state. Internal binding/release intensities agree. Conversion intensities are b_e(z) and r_e b_e(z), with fixed r_e in [1-eta,1+eta], 0<eta<1. Stop at the first conversion sigma and retain the entire marked path, holding times and final mark. All null/parallel firings are distinguished and charged. On an enabled decoded fibre the earlier constant-length activation argument proves sigma finite with polynomial population-dependent time/firing moments.

Put b=sum_e b_e and H=integral_0^sigma b(Z_s)ds. Under the reference law H is a unit exponential random variable: it is the independent aggregate conversion clock's integrated-hazard threshold. This is not an exponential assertion about physical time sigma. The path density L=dP_actual/dP_ref is

 L=r_final exp[-integral_0^sigma sum_e(r_e-1)b_e(Z_s)ds],

so pointwise

 (1-eta)exp(-eta H)<=L<=(1+eta)exp(eta H).

The earlier entropy/TV estimate loses information about rare events. The pointwise likelihood bound retains it.

2. Eventwise power bounds, including arbitrarily rare events.

Let E be ANY measurable event of the stopped segment, p=P_ref(E), and A_eta=(1+eta)/(1-eta). Then

 A_eta^-1 p^(1+eta) <= P_actual(E) <= A_eta p^(1-eta).        (1)

This is uniform over initial fine states, decoded population, binding speed and the number of internal firings. The same bound applies to any next-conversion mark/state/decoded-state event by projection.

Proof. For a unit exponential H, among all events of probability p, the largest integral of exp(eta H) is its upper-tail integral. Layer cake proves this without assuming independence between E and H:

 E[1_E exp(eta H)]
 <=integral_0^infinity min(p,P(exp(eta H)>t))dt
 =p^(1-eta)/(1-eta).

Likewise the smallest integral of exp(-eta H) is the integral over H>=-log p:

 E[1_E exp(-eta H)] >= p^(1+eta)/(1+eta).

For example the second inequality follows by integrating the lower bound
P(E intersect {exp(-eta H)>t})>=max(0,p-P(exp(-eta H)<=t)).
Combine these with the pointwise bounds on L. The cases p=0 and p=1 follow directly or by continuity. This proves (1).

Thus a polynomially rare reference event cannot become an arbitrary small additive constant under a fixed small relative conversion-rate perturbation. Its polynomial exponent changes by at most a relative eta, up to A_eta. This is stronger than uniform row TV or two-sided entropy alone. It is still not a universal invariant-law theorem on a general infinite graph.

3. A restricted but complete positive stationary consequence.

Consider a GENUINE scalar birth/death Markov event kernel on N0. Let

 pi_n=exp(-1)/n!,
 d_0=0, d_n=(n+1)^(-2), n>=1,
 p_n=1/[(n+1)(n+2)^2], n>=0,
 q_n=1-d_n-p_n.

The p_n are upward probabilities and d_n downward probabilities; q_n are marked self-events. Direct balance pi_n p_n=pi_(n+1)d_(n+1) proves the Poisson reference law. Give every marked event an independent unit-rate exponential holding time. All firings, including self-events, then have mean count T by time T and the population is pathwise <=n0+Poisson(T).

Assume an actual birth/death kernel on the SAME graph has every row event subject to (1). This assumption retains more structure than merely small segment TV/KL. Applying (1) to upward and downward marks gives

 A_eta^-2 (n+1)^(-1-eta)(n+2)^(-4eta)
 <= p'_n/d'_(n+1)
 <= A_eta^2 (n+1)^(-1+eta)(n+2)^(4eta).                    (2)

For eta<1/5, the upper ratio is <=A_eta^2 2^(4eta)(n+1)^(-1+5eta). The unnormalized invariant weights therefore have a summable factorial-power bound. All fixed stationary moments exist, and the unit-clock actual process is nonexplosive and positive recurrent. The old additive-row perturbation counterexample has p'_n>=eta²/[4(n+2)], which eventually violates (1); it cannot occur under this stronger segment structure.

There is also an explicit accuracy estimate. For eta<=1/10 let unnormalized weights be w_0=pi_0 and w_(n+1)/w_n=p'_n/d'_(n+1). Dividing (2) by the Poisson ratio 1/(n+1) gives

 |log[(w_(n+1)/pi_(n+1))/(w_n/pi_n)]|
 <=2log A_eta+4eta log2+5eta log(n+1)
 <=eta[7+5log(n+1)].

The constant7 is valid since 2log A_eta<=4eta/(1-eta²) and log2<7/10. Hence, with

 R(n)=7n+5log(n!),
 w_n=pi_n exp(s_n), |s_n|<=eta R(n).

For each fixed integer j>=0 define the finite, computable constants

 M_j=sum_n pi_n(n+1)^j,
 K_j=sum_n pi_n(n+1)^j R(n) exp(R(n)/10).

Finiteness is explicit: pi_n exp(R(n)/10)=exp(-1)exp(7n/10)/sqrt(n!). The weighted term has a ratio tending to zero, so a finite prefix and geometric tail compute a certified upper bound. A rational/algebraic majorant is

 (n+1)^j(7n+5n²)3^n/sqrt(n!),

whose successive ratio for n>=1 is <=9(3/2)^j/sqrt(n+1). Thus a cutoff n+1>=[18(3/2)^j]^2 gives a tail ratio<=1/2. No stationary-law, normalizer or exact-real oracle is being assumed in these constants.

Using |exp(s)-1|<=|s|exp(|s|),

 sum_n(n+1)^j |w_n-pi_n|<=eta K_j.

If eta<=min(1/10,1/(2K_0)), the normalization Z'=sum w_n satisfies |Z'-1|<=eta K_0 and Z'>=1/2. The actual invariant probability pi'_n=w_n/Z' therefore obeys

 sum_n(n+1)^j |pi'_n-pi_n|
 <=2eta(K_j+K_0 M_j).                                    (3)

In particular stationary whole-law TV and every fixed absolute-moment error are O(eta), with explicitly computable constants. This proves a real time-uniform stationary transfer in this scalar class, not just the existence of one-step likelihood bounds. The unit-clock convention is part of this example; a nonconstant physical occupation clock requires its own weighted control.

4. Exact scope of the new interface.

Equation(1) is a general consequence of the admitted relative CONVERSION intensity structure after binding errors have been absorbed. Equations(2)--(3) are a restricted positive example that uses a genuine scalar birth/death event kernel, Poisson reference ratios and a constant physical event clock. They do not prove that the arbitrary decoded process in the elementary compiler is Markov, birth/death, reversible or unit-clock. Hidden postconversion states and occupation rewards cannot be discarded. General weakly reversible reaction graphs and simultaneous stationary population/cost bounds remain unresolved.

The operation this note adds is control of rare transition probabilities through exponent perturbation, plus a complete factorial-tail stationary transfer where the kernel geometry is available. It identifies mathematical information discarded by an entropy-only argument and excludes the particular additive-row counterexample at the right scope. It does not impose a network, method, fallback objective or additional condition on the FULL original elementary-compiler endpoint. No scientific calculation, sampling, extra model, installation, physical experiment or source recovery was used to derive it.
