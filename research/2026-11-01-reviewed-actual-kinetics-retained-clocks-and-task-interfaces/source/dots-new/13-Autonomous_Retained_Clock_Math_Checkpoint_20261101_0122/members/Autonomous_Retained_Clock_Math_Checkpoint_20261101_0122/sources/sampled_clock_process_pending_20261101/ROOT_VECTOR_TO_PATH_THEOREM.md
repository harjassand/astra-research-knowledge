# Root construction: from one slow vector to an actual sampled binary process

Status: new conditional theorem, independent audit pending. Ordinary Markov conditional expectation, relative-entropy chain rule and Pinsker are components, not novelty claims.

Let P_t be an actual positive Markov semigroup preserving probability pi. Let Z be an actual measurable +/-1 label on the entire state space. For each deterministic interval Delta_i>0 receive r_i in [0,1), and a proved error

  ||P_Delta_i Z-r_i Z||_(L2 pi) <= d_i.

Let actual initial law nu have density f0<=R relative to pi. Positivity and invariance preserve this density upper bound at every deterministic time. Observe the SAME continuing physical trajectory at deterministic times t0=0,t1,...,tn, with intervals Delta_i. No hidden-state reset is performed.

Compare with the two-state Markov chain having the SAME initial label distribution as nu, and each step transition Q_i(z,z')=(1+r_i z z')/2. Then

  KL(actual joint label law || Q joint law)
      <= R sum_i d_i^2/(1-r_i^2),
  TV(actual joint label law, Q joint law)
      <= min(1, sqrt((R/2) sum_i d_i^2/(1-r_i^2))).

Proof. Given the actual entire observed label history through i-1, the next-label positive probability is p_i=E[(1+P_Delta_i Z(X_ti-1))/2 | history]. The comparison probability is q_i=(1+r_i Z(X_ti-1))/2, since current Z is observed. Thus p_i-q_i is the conditional expectation of e_i(X)=(P_Delta_i Z-r_i Z)/2. Jensen and the actual deterministic-time marginal bound imply E(p_i-q_i)^2 <= R ||e_i||_2^2. Bernoulli relative entropy is at most (p-q)^2/[q(1-q)], by KL<=chi-square. Both comparison labels have q_i(1-q_i)=(1-r_i^2)/4. Apply the entropy chain rule along ACTUAL histories, then Pinsker (natural logarithms). No union over the 2^n words, hidden-state conditional mixing, or iid waiting assumption is used.

A weaker bound requiring only ||f0||_2<=sqrt(D) is TV <= min(1,(sqrt(D)/2) sum_i d_i), using conditional total variation and L2 contraction of the adjoint density. This does not supply the stronger KL bound under the same weaker premise.

## Acquiring the slow vector from trial/current forms

For a reversible actual semigroup P_t=exp(-tK), a mean-zero trial psi with N=||psi||_2^2 and finite inverse form admits a spectral measure. Suppose a received rate k satisfies E(psi)/N<=k and k<psi,K^-1 psi>/N<=1+epsilon. The accepted elementary scalar moment lemma gives

 exp(-kt) <= C(t)=<psi,P_t psi>/N <= exp(-kt)+epsilon.

Self-adjointness and the semigroup identity then give

 ||P_t psi-exp(-kt)psi||_2^2
 =N[C(2t)-2exp(-kt)C(t)+exp(-2kt)] <=N epsilon.

Consequently an actual binary label Z with ||Z-psi||_2<=eta has

 d_i <= sqrt(N epsilon)+(1+r_i)eta, r_i=exp(-k Delta_i).

If psi equals Z outside a transition slab of pi-mass s and both lie in [-1,1], eta<=2sqrt(s). Sharper pointwise construction may improve this. A label must be defined inside the slab; one cannot omit states and still claim a binary sampled process.

## Scope and cost

This is finite sampled-path accuracy, hence applies to EVERY event/function of the same finite label record. It is not exact continuous first-hit renewals, independent residence times, relative rare-event probability accuracy, or arbitrary adaptively selected observation times. As Delta->0, the factor 1-r^2 is charged and the estimate may fail. Acquiring the actual global model, trial, inverse-form source current, initial density bound, and numerical exponential enclosures remains necessary. Computing the comparison chain costs O(n) for Markov-additive events with bounded accumulator, but arbitrary record predicates can themselves be computationally difficult; no universal cheap event-query oracle is promised.

The basic process theorem needs no reversibility once the actual vector bounds are independently received. The trial-to-vector argument DOES use reversibility and cannot be silently applied to the earlier time-dependent neutral-processing scalar correlation theorem. Nonautonomous controls/feedback need their own vector/interface proof. Exact Gibbs|A provides R=1/pi(A); actual preparation is still a separate obligation.
