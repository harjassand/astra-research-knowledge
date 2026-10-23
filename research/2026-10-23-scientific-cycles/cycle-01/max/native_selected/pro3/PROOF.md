# Forward-KL control, cold-start failure, and safe initialization of local-global Monte Carlo

Producer: Astra PRO 3, 21 October 2026. This is an internally checked mathematical research checkpoint, not an externally refereed theorem or an observed application speedup.

## 0. Question, scope, and attribution

The question is whether the population forward error of a learned proposal is sufficient to control the cost of an exact-target Markov sampler, and whether adding an ordinary local Metropolis update preserves that control. This is distinct from the completed Gaussian conditional sampler and the closed SPARC inference operation.

The universal entropy-only exponential cost scale is already in Block and Polyanskiy, *The Sample Complexity of Approximate Rejection Sampling*, COLT 2023, using the corrected arXiv:2302.04658v3 (2024). Proposal-start independence-MH has strong existing finite-budget results, including Kurennoy, Yarullin and Reid, arXiv:2610.03480v1, and Shin, Pang and Jun, arXiv:2609.34639v1. The exact coefficient below is an explicit specialization/refinement of that framework; it is not presented as a new sampling principle. The general possibility that extra reversible updates delay mixing is also established (Holroyd, arXiv:1101.4690). Our distinct investigated boundary is fixed forward KL, proposal initialization, a three-state ordinary local-MH kernel, and matched global-proposal counts. Historical novelty of that precise boundary is not established by the focused search.

All results below have full arguments independent of unproved empirical fits. Numerical files check finite instances and implementation; they do not prove universal quantifiers. A population KL certificate is an assumption, not something a finite empirical training loss automatically supplies.

## 1. Definitions and access

Let pi and q be equivalent probability measures on a measurable space, with positive finite likelihood ratio W=dpi/dq q-almost surely. Natural logarithms and TV(mu,nu)=sup_A |mu(A)-nu(A)| are used. Set D(pi||q)=E_pi log W=E_q[W log W-W+1]. We assume D(pi||q)<=K, where K>0.

The independence Metropolis-Hastings kernel G proposes Y~q, accepts with min(1,W(Y)/W(X)), and otherwise stays. Initialization X_0~q is counted as one proposal draw. n transitions therefore use n+1 proposal draws and at most n+1 target/proposal evaluations if the current ratio is cached. An unnormalized target suffices because the normalizer cancels. G is reversible and invariant for pi; an invariant target is not an assertion of exact finite-time output.

For a pi-reversible local kernel L and 0<alpha<1 define H=alpha G+(1-alpha)L. Unless stated otherwise L is an actual fixed Markov kernel. State-dependent or history-dependent selection among invariant kernels is not automatically invariant.

## 2. Entropy tail lemma

For R>e, let A={W>R}, h=pi(A), a=q(A). Then a<=h/R. Binary data processing gives

    D(pi||q) >= h log(h/a)+(1-h) log((1-h)/(1-a))
              >= h log R+(1-h)log(1-h)
              >= h(log R-1).

The last inequality follows from (1-h)log(1-h)>=-h. Thus

    pi(W>R) <= K/(log R-1).                                      (2.1)

For a fixed pair of finite KL, log(R) pi(W>R)->0. Indeed the negative part of log W under pi has integral at most 1/e, so the positive part is integrable; its tail obeys t P(log W>t)->0.

An alternative useful clipped-excess estimate is

    E_q(W-R)_+ <= K/log R,  R>1.                                (2.2)

To prove it, put phi(w)=w log w-w+1. For w>=R, phi(w)-log(R)(w-R) has nonnegative derivative log(w/R) and value phi(R)>=0 at R. For w<R the right side is zero and phi(w)>=0. Integrate. The tail mass and clipped excess are different quantities and must not be interchanged.

## 3. Pure independence-MH: sharp entropy-only minimax asymptotic

Define

    R_K(n)=sup_{pi,q: D(pi||q)<=K} TV(qG^n,pi).

The supremum is over pairs separately for each n. Then

    lim_{n->infinity} log(n) R_K(n)=K.                            (3.1)

Equivalently, for the worst proposal-start mixing time T_K(epsilon),

    lim_{epsilon->0} epsilon log T_K(epsilon)=K.                  (3.2)

These are worst-case accuracy limits for this sampler (and, by candidate coverage, relevant selector classes), not universal hardness of sampling a target supplied in another representation.

### Upper bound

Couple X_0~q and Y_0~pi independently and use the same proposal and uniform acceptance variable at every step. Let C={W<=R}, h=pi(C^c). Initial failure of both states to lie in C has probability at most h+q(C^c)<=h(1+1/R).

While the chains differ and both lie in C, a proposal with weight above R is accepted by both and couples them. For a proposal of weight at most R, both accept whenever U<=W(Y)/R. Thus until coupling neither state can exit C, and the per-step probability of coupling is at least

    E_q min(1,W/R) >= (1-h)/R.

Consequently

    TV(qG^n,pi) <= h(1+1/R)+exp[-n(1-h)/R].                      (3.3)

When b=K/(log R-1)<1 one may replace h by b. Take R=n/(log n)^2. The exponential term is negligible relative to 1/log n, and the first term times log n tends to K. This proves the upper half of (3.1).

### Lower bound and sharp constant

On two states take pi(1)=p and q(1)=r=p exp(-K/p). The other masses are complements. Then

    D(pi||q)=K+(1-p)log[(1-p)/(1-r)] < K.

Direct diagonalization of the two-state kernel yields

    TV(qG^n,pi)=(p-r)(1-r/p)^n=p(1-exp(-K/p))^(n+1).             (3.4)

For large n choose p=K/[log n+2 log log n]. Then n exp(-K/p)=1/(log n)^2, so the last factor tends to one, and p log n tends to K. This proves (3.1). Monotonicity of TV under a fixed Markov kernel gives (3.2) by sandwiching the envelope between (K-eta)/log n and (K+eta)/log n.

For each fixed finite-KL pair, (3.3) and the stronger fixed-pair tail statement show log(n)TV(qG^n,pi)->0. There is no contradiction: the worst pair changes with n. K=0 is the separate trivial case pi=q.

## 4. Fixed-KL cold-start obstruction for ordinary local-global MH

Fix K>0 and 0<alpha<1. Write c=K/4 and b=1-exp(-c). For

    0<p<=min(1/4, exp(-c)b),
    s=p exp(-2c/p),  r=p exp(-c/p),
    pi=(p,s,1-p-s),  q=(r,b,1-b-r),                             (4.1)

label the three states A,B,C in path order. All masses are positive. We have s<=b and q_C=exp(-c)-r>=exp(-2c). Hence

    D(pi||q)=c+s log(s/b)+pi_C log(pi_C/q_C)<=c+0+2c=3K/4.       (4.2)

This is a finite inequality, not just a limiting assertion. As p->0, the actual divergence tends to K/2.

Use the same symmetric local proposal for every p:

    Q=[[1/2,1/2,0],[1/2,0,1/2],[0,1/2,1/2]].

Apply ordinary MH acceptance min(1,pi_j/pi_i). This gives an irreducible reversible local kernel with

    L_BA=L_BC=1/2,
    L_AB=s/(2p)=exp(-2c/p)/2,
    L_CB=s/(2pi_C).

All remaining mass stays at the current state. A has the largest global importance weight. Its global and local exit probabilities are respectively

    h_G=(1-p)exp(-c/p),  h_L=exp(-2c/p)/2.                       (4.3)

Starting from q, the first mixture update puts at least d=b(1-alpha)/2 in A, by selecting L at B and proposing A. Retaining only paths that then remain in A gives, for n>=1,

    TV(qH^n,pi) >= d(1-h)^(n-1)-p,
    h=alpha h_G+(1-alpha)h_L.                                  (4.4)

For every fixed n the right side tends to d>0 as p->0. Therefore for every fixed 0<epsilon<d,

    sup_{(4.1)} min{n: TV(qH^n,pi)<=epsilon}=infinity,            (4.5)

despite D(pi||q)<=K and a finite uniform pure-IMH bound. Each individual finite chain is irreducible and converges. This is a lack of a uniform guarantee over the admitted class, not nonconvergence of a fixed chain.

### Matched global-call schedules

The row-vector product LG means local first, then global; GL means the reverse. Each cycle uses one global and one local update.

For LG, the first cycle reaches A with mass at least (b/2)(1-h_G). Staying in A for each further cycle has probability at least (1-h_L)(1-h_G). Thus

    TV(q(LG)^n,pi) >= (b/2)(1-h_G)[(1-h_L)(1-h_G)]^(n-1)-p.

For GL, starting in B, the global proposal can propose B (probability b) and remain there, after which the local step goes to A with probability 1/2. The first-cycle lower mass is b^2/2, giving

    TV(q(GL)^n,pi) >= (b^2/2)[(1-h_L)(1-h_G)]^(n-1)-p.

These limits are positive. Matching the number of expensive global calls therefore does not remove the obstruction. Local steps cost additional proposal and ratio evaluations.

### Why standard comparisons do not settle this example

H has Dirichlet form at least alpha times G's, so this is compatible with ordinary spectral-gap comparison. Those comparisons do not bound the projection of this changing nonstationary initialization onto slow modes. Peskun-type asymptotic variance comparisons likewise do not imply monotonic finite-time TV from q. Existing local-global guarantees with drift, weight-moment or warm-start assumptions remain valid; their required constants are not bounded by (4.2). For example chi-square(pi||q) contains p exp(c/p), which diverges.

The finite-state construction is a rigorous performance obstruction, not a proposed physical dataset or an application benchmark. These explicit three-state probabilities are directly sampleable; there is no claim that all algorithms must pay the displayed MH cost.

## 5. Constructive initialization certificate

We now give an implementable way to remove the uncontrolled starting-density issue before applying a warm-start theorem. This is an ordinary resampling construction with a new self-contained accounting here, not a claimed new resampling algorithm.

Draw N iid q candidates X_i and choose one with probability W_i/sum_j W_j (SIR). Only unnormalized positive weights are needed. Let

    M=exp(2K+1),  delta_N=exp[-N/(16M)].

By (2.2), E min(W,M)>=1-K/log M>1/2. The independent variables V_i=min(W_i,M) lie in [0,M]. The bounded multiplicative Chernoff inequality gives

    P(sum_i V_i<N/4)<=exp[-N/(16M)].                            (5.1)

For completeness, the Chernoff inequality follows by applying e^(-t x)<=1+(e^(-t)-1)x for x in [0,1], multiplying expectations, and choosing the standard half-mean deviation; exp(-mean/8) suffices. Here the normalized total mean is at least N/(2M).

Let E be the good event in (5.1). Since sum W_i>=sum V_i, for every measurable A the output's good-event submeasure satisfies

    mu_good(A)=E[1_E sum_i W_i 1_A(X_i)/sum_j W_j]
             <=(4/N) E sum_i W_i 1_A(X_i)=4 pi(A).              (5.2)

Thus mu_N=mu_good+mu_bad, where mu_bad has mass beta<=delta_N and mu_good<=4pi. Equivalently,

    E_4(mu_N||pi)=sup_A[mu_N(A)-4pi(A)]<=delta_N,
    mu_N=(1-beta)nu+beta eta,  nu<=B pi, B=4/(1-beta).           (5.3)

The proof-only event E and the normalized ratio W need not be evaluated by the algorithm. If H is pi-invariant and a valid theorem gives TV(nu H^t,pi)<=F_B(t) for all B-warm nu, then

    TV(mu_N H^t,pi)<=beta+(1-beta)F_B(t).                        (5.4)

Approximate warmness alone does not supply F_B; it must be justified separately. Any overall pi-invariant transition preserves the good-submeasure domination and bad-mass decomposition.

### Strongest matched-budget initializer

Kurennoy et al. (2026), Theorem 1, proves that proposal-start independence-MH after N candidates has no larger convex f-divergence from pi than ordinary SIR at the same N, on finite positive state spaces. Taking f(u)=(u-4)_+ transfers (5.3) to ordinary IMH. Therefore our executable finite-state comparison uses pure IMH as the strongest matched-budget initializer. SIR remains the transparent proof device; no SIR advantage is claimed. The direct SIR theorem above is valid on the general measurable space without needing that cited finite-space comparison.

## 6. A self-contained warm-start bound for arbitrary reversible local moves

This section is derived by the principal investigator. It supplies a conservative F_B under explicit assumptions, showing that the initialization correction can produce a finite uniform guarantee. It is not asserted to be the best numerical rate.

Make the mixture lazy: C=(I+H)/2. It is pi-reversible and has spectrum in [0,1]. Suppose 0<=f=dnu/dpi<=B, with B>=1. For R>e set h=pi(W>R), and let r_n=exp[-alpha n/(2R)]. Then

    TV(nu C^(2n),pi)
    <=sqrt([r_n(B-1)+h B^2][r_n/4+h]).                         (6.1)

The same bound plus beta applies after (5.3), with its corresponding B.

### Proof of the weak inequality used in (6.1)

For a bounded g, use the reversible independence-MH form

    E_G(g,g)=1/2 integral pi(dx)pi(dy)
                       [g(x)-g(y)]^2/max(W(x),W(y)).

On C_R x C_R the reciprocal maximum is at least 1/R. The complementary pair mass is 2h-h^2. Therefore

    Var_pi(g)<=R E_G(g,g)+h Osc(g)^2
              <=(2R/alpha) E_C(g,g)+h Osc(g)^2.                (6.2)

Because C is positive semidefinite, I-C^2>=(I-C). Put v_j=Var_pi(C^j g). Markov contraction of oscillation and (6.2) yield

    v_(j+1)<= (1-alpha/(2R))v_j
                +alpha h Osc(g)^2/(2R).

Hence v_n<=r_n Var_pi(g)+h Osc(g)^2. Apply this once to f (Var f<=B-1 and Osc f<=B) and once to each indicator 1_A (variance<=1/4, oscillation<=1). Self-adjointness and Cauchy-Schwarz give

    |<f-1,C^(2n)(1_A-pi(A))>|
    =|<C^n(f-1),C^n(1_A-pi(A))>|
    <=sqrt([r_n(B-1)+h B^2][r_n/4+h]).

Taking the supremum proves (6.1).

### Explicit finite budget

For desired epsilon in (0,1/2], take

    N>=16 exp(2K+1) log(3/epsilon),
    B=6, h_0=epsilon/18,
    R=exp(1+18K/epsilon),
    n>= (2R/alpha) log(18/epsilon).

Then beta<=epsilon/3, the normalized good density is at most 4/(1-epsilon/3)<=4.8<6, and (2.1) gives h<=h_0. Also r_n<=h_0. The square root in (6.1) is at most 2B h_0=2epsilon/3, so the total TV is at most epsilon.

This finite guarantee is intentionally reported with its complete cost: N initialization candidates and 2n lazy hybrid applications. Expected later global updates are alpha*n, and expected local updates are (1-alpha)*n; each underlying update has its own implementation cost. The bound scales exponentially in K/epsilon with a very poor constant and does not beat the pure-IMH entropy-only baseline. It is a validity certificate and a route for substituting stronger application-specific warm-start bounds, not evidence of computational acceleration.

## 7. What is and is not established

Established internally with full proofs: the sharp pure-IMH entropy envelope; an explicit fixed-KL failure of unrestricted cold-start hybridization, including matched global-call schedules; a population-KL-to-approximate-warmness construction; and a conservative arbitrary-reversible-local guarantee after initialization and laziness.

Inherited: independence-MH, common-proposal coupling, rejection/importance sampling, the general entropy cost scale, the fact that extra updates may delay mixing, convex-divergence comparison of IMH and SIR, and weak-Poincare/Dirichlet proof techniques. This work does not claim those as new.

Not established: historical priority of the specific hybrid construction; a practical speedup on a scientific workload; a way to verify a global population KL bound from finite training data without extra assumptions; a uniform claim for adaptive state-dependent kernel choice; or a lower bound for every possible sampler. No physical experiment or original Gaussian-operation transfer is claimed.

## 8. Chosen next scientific question

Keep this line active. Determine the sharp proposal-start hybrid convergence envelope when BOTH D(pi||q)<=K and D(q||pi)<=J are bounded, with fixed alpha and arbitrary pi-reversible local kernel (using laziness where required). The present funnel has diverging reverse KL, so it does not settle that class. Entropy truncation followed by Section 6 supplies a conservative finite bound, but its nested exponential dependence may be far from sharp. The next obligation is a matching construction or a sharper comparison theorem; more toy demonstrations of the already-proved one-sided obstruction are not the next task.

## Primary references

* Block and Polyanskiy (2023; corrected 2024), https://arxiv.org/abs/2302.04658v3 and https://proceedings.mlr.press/v195/block23a.html . The corrected v3 explicitly repairs the COLT proof of Lemma 27; the old tail lemma must not be used uncorrected.
* Kurennoy, Yarullin and Reid (2026), https://arxiv.org/abs/2610.03480v1 . Finite-space convex-divergence dominance, priority representation and clipped-tail bounds.
* Shin, Pang and Jun (2026), https://arxiv.org/abs/2609.34639v1 . Uniform-race approximate sampling and simultaneous clipping guarantees.
* Daeijavad and Asoodeh (2026), https://arxiv.org/abs/2606.03033v1 . Local/core-tail contraction under explicit warm-start assumptions.
* Wang (2022; preprint v6 2021), https://arxiv.org/abs/2008.02455v6 . Exact independence-MH convergence tied to bounded likelihood ratios and initialization.
* Holroyd (2011), https://arxiv.org/abs/1101.4690 . General examples in which extra updates delay mixing.
* Peres and Winkler (2013), https://arxiv.org/abs/1112.0603 . No-delay/censoring theorems with specific monotonicity and starting-density hypotheses.
* Samsonov et al. (2022), Local-Global MCMC kernels: the best of both worlds; precise source and assumptions in literature_boundary.md. Their drift/level-set/chi-square assumptions are stronger than forward KL alone.
