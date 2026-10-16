# Coupled total-count/dispersion route: exact generators and a minimal-family obstruction

## Result

A genuine coupled statistic removes the PREVIOUS sparse-product factor-isolation argument. Nevertheless, the minimal static exponential family

    g(t,n)=exp[lambda(1-t)+theta(120-S(n))+eta*C(n)],
    S=sum_i n_i, C=8 sum_i n_i^2-S^2,
    theta>=0, eta>=0,

cannot certify an initial probability below one on the actual eight-site model. An exact inequality at the uniform state (60,...,60) suffices; it is not a synthetic replacement model. General time-dependent F(t,S,C), other parameter signs with separately verified boundary conditions, or other coupled representations remain unexcluded.

I also obtain a rigorous residual-separation interface for general positive F(t,S,C). It requires no closed moment dynamics and preserves the actual first-hit target, but no useful F or certified rare probability has been acquired here.

## Exact unbounded-generator identities

Use the rates and open 2-by-4 graph established in the preceding audit. Let E denote its ten undirected edges, d_i the degree, D=8.2207, and F_k=sum_i (n_i)_k the falling-factorial sums. Write B=sum_i b(n_i), A=sum_i a(n_i). Then

    Q S = B-A
        = -.040 F_3 + 2.676 F_2 -37.881 S +864.816.

For F_2=sum_i n_i(n_i-1), a birth changes it by 2n_i, a death by -2(n_i-1), and a directed diffusion i->j by 2(n_j-n_i+1). Hence

    Q F_2 = -.080 F_4 +5.192 F_3 -65.058 F_2 +216.204 S
              +2D[sum_i d_i n_i - sum_{ij in E}(n_i-n_j)^2].

Thus diffusion conserves S and dissipates graph dispersion, with a positive discrete-jump correction. It is NOT simply negative: at a uniform positive configuration the diffusion contribution to QF_2 is positive.

Since C=8(F_2+S)-S^2 and Q(S^2)=2S Q S+B+A,

    Q C = 8 Q F_2 +(8-2S) Q S -(B+A).

Equivalently, the actual jump increments are

    birth at i: Delta S=1, Delta C=16n_i-2S+7;
    death at i: Delta S=-1, Delta C=-16n_i+2S+7;
    diffusion i->j: Delta S=0, Delta C=16(n_j-n_i+1).

The diffusion contribution to QC is exactly

    16D[sum_i d_i n_i - sum_{ij in E}(n_i-n_j)^2].

These identities describe the original generator, or retained states whose jumps do not overflow. In the capped probability problem, transitions to count 163 must instead use the specified failure payoff. One cannot apply these polynomial formulas to a killed statistic with payoff zero at overflow without adding the boundary correction. On target states the process is stopped. The residual interface below treats these distinctions explicitly.

`check.py` derives the jump generator directly and verifies these identities with exact fractions on seven heterogeneous and uniform states, including a state at count 162 for the UNBOUNDED identities. These checks accompany the displayed algebra, not a claim that seven samples prove a universal identity.

## No two-dimensional Markov closure

S and C do not determine the rates of their own transitions or even their drifts. For example, the continuation configurations

    x=(20,0,3,3,0,0,0,0),
    y=(20,1,1,4,0,0,0,0)

have the same S and C (also the same F2), but F3(y)-F3(x)=12, so QS(y)-QS(x)=-12/25. This discrepancy is verified exactly.

Even full permutation-invariant moments do not determine the graph term: placing one count 16 at a corner or at a degree-three vertex gives identical S and C but different QF2. Both configurations are continuation states. Thus replacing the process by a closed two-statistic chain would be unjustified.

## Why the minimal coupled family fails

C is nonnegative by Cauchy-Schwarz. Every actual target state has S<=120, so V(n)=exp[theta(120-S)+eta C]>=1 there when theta,eta>=0. At the initial all-50 state, S=400 and C=0, so V(initial)=exp(-280theta). This is a valid target MAJORIZATION; it does not equate the target with S<=120.

At the actual continuation state n=(60,...,60), S=480 and C=0. There are no immediate target or overflow transitions. Every birth and death increases C by 7; every diffusion jump increases C by 16. Therefore the exact residual ratio is

    QV/V = 8{b(60)[exp(-theta+7eta)-1]
                  +a(60)[exp(theta+7eta)-1]}
             +20D*60[exp(16eta)-1].

Using exp(x)>=1+x for every real x gives

    QV/V >= 8[a(60)-b(60)]theta
                 +{56[a(60)+b(60)]+320D*60}eta
            = (904518/125)theta +(160197294/125)eta.

The exact values b(60)=4790571/500 and a(60)=524283/50 and all coefficients are independently checked. A supercaloric static-prefactor envelope must satisfy lambda>=QV/V, hence

    log g(0,(50,...,50))
      = lambda-280theta
      >= (869518/125)theta +(160197294/125)eta >=0.

The bound is strictly above one unless theta=eta=0 and the prefactor is also zero. It remains valid if the target boundary is overwritten to one, because the diagnostic state has no target-entering jumps. Overflow conventions cannot repair this row either.

This family genuinely contains pair coupling: C includes -2 sum_{i<j}n_i n_j, so it is not a product of local factors. At sparse configurations, subsequent arrivals change C and are priced by the potential. The earlier factor-isolation proof no longer applies. The obstruction here instead comes from downward reaction drift at a uniform high state plus positive jump-induced dispersion. It does not exclude eta<0 with a different target normalization, nonlinear total-count potentials, or genuinely time-dependent coupled functions.

## Rigorous residual interface for general F(t,S,C)

Let F be a supplied positive function and define its envelope on continuation states by F(t,S(n),C(n)). Require F>=1 on every ACTUAL target statistic pair, a nonnegative terminal function, and failure payoff zero. One may overwrite the target by one. For an upper residual bound, it is sufficient to retain the native F value on target-entering transitions when that value is >=1; this only raises the residual. This preserves first-hit semantics and does not replace the target by a total-count event.

Fix t,S,C and let Q2=(C+S^2)/8. The residual QF/F decomposes into eight unary and ten pair terms at these fixed statistics:

    U(a) = b(a)[R_+(a)-1]+a_rate(a)[R_-(a)-1],
    R_+(a)=F(t,S+1,C+16a-2S+7)/F(t,S,C),
    R_-(a)=F(t,S-1,C-16a+2S+7)/F(t,S,C),

with R_+(162)=0 for overflow; the death term at a=0 is omitted.

For an undirected edge with counts a,b,

    E(a,b)=D*a[R_to_b(a,b)-1]+D*b[R_to_a(a,b)-1],
    R_to_b(a,b)=F(t,S,C+16(b-a+1))/F(t,S,C),

and the reverse ratio exchanges a and b. A ratio into a destination already at162 is zero, and a source-zero term is omitted. These prescriptions implement killed overflow exactly, including diffusion overflow.

For ANY chosen finite real (or rational) multipliers alpha,beta,

    max_{actual n: sum n_i=S, sum n_i^2=Q2, max n_i>15} QF/F
      <= alpha*S+beta*Q2
           +max_{0<=n_i<=162, max n_i>15}
                 [sum_i {U(n_i)-alpha*n_i-beta*n_i^2}
                       +sum_{ij in E}E(n_i,n_j)].

The inequality follows simply by adding and subtracting the fixed moment constraints. No duality equality, moment closure or probabilistic approximation is assumed. The right-hand inner maximum is an ordinary width-two grid max-sum calculation with a Boolean flag for whether any count exceeds15. Two successive one-coordinate contractions per column cost O(163^3), rather than enumerating 163^8. Fixed multipliers already give a valid upper bound; optimizing them within any chosen bounded search box can improve it without being required for validity. For a rational F table and rational multipliers the residual entries can be verified exactly; upward rational rounding followed by exact integer max-sum gives a conservative certificate. Analytic or interval control is still needed over time if F varies continuously.

The sufficient supercaloric test is partial_t log F plus this upper bound <=0 at every feasible (t,S,C). Off-fiber evaluations introduced by the relaxation need a consistently defined positive extension of F; otherwise one must omit unattainable local terms only with a proved constraint argument. In particular, negative/impossible C arguments cannot silently receive arbitrary probability values.

This is a concrete low-dimensional OUTER certificate interface, not an acquired efficient solver: S ranges from 0 to1296, C has many feasible integer values up to419904, each tested fiber requires a graph contraction, and time/roundoff/dual-relaxation slack remain charged. No claim of affordable full coverage follows from the formal reduction. The max-sum principle is established variable elimination, not a novelty claim.

## Total-count-only comparison and stopping point

All-low implies S<=120, so a certified bound on first hitting S<=120 upper-bounds the actual target event, but the reverse implication is false (for example (16,0,...,0)). It may lose a great deal of information. The naive exponential total-count certificate is the eta=0 subfamily and is already ruled out by the uniform-60 inequality above. This does not rule out all nonlinear or time-dependent total-count majorants.

The acquired inputs suffice for exact generator identities, closure counterexamples, the minimal coupled-family obstruction, and the rigorous residual interface. They do NOT supply a useful coupled F, a certified low-dimensional first-hit probability, or a small useful interior upper bound. Further work would require constructing a nontrivial dynamic/nonlinear majorant and certifying all its residuals; no such object is asserted here.
