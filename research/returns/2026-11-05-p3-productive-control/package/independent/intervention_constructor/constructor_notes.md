# Law-changing useful-work control: independent construction notes

This is a mathematical result for a declared finite-cycle interface. It is not a demonstrated physical protection device. The underlying Bellman and skip-free forward recursion are existing machinery; see the primary-source notes below. The specific assembly worth considering is a finite acquisition certificate valid for every catastrophe depth, with its statistical and hardware boundaries.

## 1. Operational model and objective

The true observable health state is `i in {0,...,N}`. State N is first catastrophe. At a safe state, an action a from a finite menu is selected. A complete physical cycle includes useful production, any maintenance, metrology, controller computation and settling. It has duration at most tau_max, energy at most E_max, and provides at least g_min>0 units of the required function. Its measured transition is up one with p_i^a, down one with q_i^a (clamped at zero), or unchanged with the remaining probability. Require p_i^a >= p_min>0 and p_i^a+q_i^a<=1. No additional jump or catastrophe channel is implicit.

The accumulated objective is expected total reward before first catastrophe. The reward r_i^a>0 can be raw useful work or a declared linear net benefit g_i^a-alpha*e_i^a-beta*tau_i^a, while raw useful output remains bounded below. A per-cycle energy/time cap and positive net reward are different from a hard total energy budget. The latter is NOT solved by this stationary theorem.

Reward is delivered before the end-of-cycle health update. If the actual machine can fail midway through a cycle before completing the promised output, its actual expected reward must be used; a uniform positive-reward contract cannot simply be assumed.

All randomized, history-dependent policies are allowed. A run is proper because N successive upward outcomes have conditional probability at least p_min^N. Consequently P(T_N>kN)<= (1-p_min^N)^k, uniformly over policies, so E T_N<=N/p_min^N.

## 2. Exact forward Bellman operation

Put d_{-1}=0 and, successively for i=0,...,N-1,

    d_i = max_a [r_i^a/p_i^a + (q_i^a/p_i^a)d_{i-1}].

Define V_i=sum_{j=i}^{N-1} d_j and V_N=0. Any action attaining the displayed maximum at state i is optimal simultaneously from every safe start, against every adaptive randomized policy.

Proof: V_{i+1}-V_i=-d_i and V_{i-1}-V_i=d_{i-1}. Therefore

    r_i^a + E_a[V(X_{t+1})-V(X_t)|X_t=i]
      = r_i^a-p_i^a d_i+q_i^a d_{i-1} <= 0,

with equality for a maximizing action. Sum this stopped supermartingale identity to time T_N wedge t; use bounded V and uniform absorption to pass to the limit. This gives the upper bound V for every policy and equality for the selected stationary one.

The formula is valid for arbitrary state-dependent rows. The action at state i depends only on rows at states <=i, not on catastrophe depth N beyond i. This is a direct operation for the useful-work decision; it does not require an absolute lifetime estimate.

For a stationary arbitrary policy pi, the exact loss identity is

    V*(x)-V^pi(x) = E_x^pi sum_{t<T_N}
       [p_{X_t}^{A_t}d_{X_t}-q_{X_t}^{A_t}d_{X_t-1}-r_{X_t}^{A_t}].

This is the ordinary undiscounted performance-difference / occupation identity. It exposes how small persistent policy errors can accumulate.

## 3. Homogeneous finite control description

If rows depend only on action, write c_a=r_a/p_a and rho_a=q_a/p_a. Let F(z)=max_a(c_a+rho_a z). Then d_i=F(d_{i-1}). The sequence d_i is increasing (F is increasing and d_0>0). Selected slopes can be chosen nondecreasing along the upper envelope. Each active affine line occupies one contiguous interval of damage levels; there are at most K-1 switches.

Suppose b uniquely maximizes rho, rho_b>1, and set

    D=max_{a!=b} ((c_a-c_b)_+)/(rho_b-rho_a).

For z>=D, b maximizes F. Since F(z)>=c_b+rho_b*z>z, that tail is invariant. Also

    d_{m-1} >= c_b*(rho_b^m-1)/(rho_b-1).

Thus one can take

    M=ceil(log(1+(rho_b-1)*D/c_b)/log(rho_b)),

with M=0 if D=0. The same mode b is optimal at every state >=M, for every N. Neither M nor the finite policy description depends on N.

## 4. Robust cone: rows may vary independently with state

Suppose actual c_i^a, rho_i^a lie in action envelopes [c_a^-,c_a^+] and [rho_a^-,rho_a^+] for all safe states. These envelopes must be supplied by validated structure or acquired at all states; shallow observations alone cannot establish arbitrary tail rows.

For a candidate tail mode b, assume

    rho_b^- >= 1,
    rho_b^- > rho_a^+ for all a!=b,
    c_b^- >0.

Define

    D_box=max_{a!=b} ((c_a^+-c_b^-)_+)/(rho_b^- -rho_a^+).

If a certified prefix gives a lower bound d_{m-1}>=D_box, b is optimal for all later states, for every state-dependent model in the envelopes. Its next increment is at least c_b^-+rho_b^-d_{m-1}, which remains above the threshold.

Prefix certification is elementary interval arithmetic. Start [L_-1,U_-1]=[0,0]. At state i each action score lies in [c_a^-+rho_a^-L_{i-1}, c_a^++rho_a^+U_{i-1}]. If one lower endpoint exceeds every competing upper endpoint, that action is certified. Propagate its interval. If the tail condition fires, stop; never evaluate all N values. With strict finite-prefix margins and a strict tail slope gap, sufficiently accurate local estimates always certify the finite policy.

This gives pointwise exact optimality for each stationary model in the box. It does not automatically say this policy is optimal in a nonstationary model whose future rows are allowed to depend on time or hidden history. A separate robust mission bound below does survive conditional drift within the boxes.

## 5. Explicit nontrivial family

Two modes, with per-cycle useful reward r_A=3 and r_B=2:

    A: p=.1, q=.2; c=30, rho=2.
    B: p=.2, q=.7; c=10, rho=3.5.

The exact policy is A at state 0 and B at every positive safe state, for every N. The increment sequence and optimal work are

    d_i=34*(3.5)^i-4,
    V_0=13.6*((3.5)^N-1)-4N.

Always-A yields 60*(2^N-1)-30N. Always-B yields 5.6*((3.5)^N-1)-4N. Thus the selected policy is not obtained by blindly choosing the largest repair rate everywhere.

The same exact policy is certified uniformly on

    p_A in [.09,.11], q_A in [.19,.21],
    p_B in [.19,.21], q_B in [.69,.71].

Indeed c_A^- = 3/.11=27.2727..., c_B^+=2/.19=10.5263..., and

    D_box=(3/.09-2/.21)/(.69/.21-.21/.09)=25,

so the state-0 winner A is strict and d_0>=27.2727...>D_box. This also certifies the policy for arbitrary state-dependent rows in those envelopes, not merely homogeneous ones.

To avoid giving the winner in advance, the acquisition problem can start from a broad parameter set (or a union with regions where the two command kernels are swapped while their rewards stay fixed). The algorithm measures the command kernels and returns only when its intervals certify the policy. On any compact separated region it terminates with a number of samples independent of N. A box whose winner is already known is a mathematical robustness certificate, not by itself a nontrivial statistical acquisition problem.

## 6. Acquisition and resources

For a homogeneous actual interface, elementary tests at state 1 produce three categorical outcomes and identify p_a and q_a. For m independent trials per action, Hoeffding plus a union bound gives simultaneous probability accuracy h with failure probability <=4K exp(-2m h^2). Hence

    m >= (1/(2h^2))*log(4K/delta).

This is a count of elementary transitions, not free physical tests. One possible admissible assay contract is: an auditable healthy reset, a reusable repair/reset port with stated time/energy/parts cost, and an actual machine with N>=3. From reset state 0, operate until the first up transition (mean <=1/p_min cycles), then apply one test action at state 1, observe the outcome in {0,1,2}, and repair/reset. There is no exposure to N during that one test, but the reset primitive is an additional physical capability that must be earned, paid or explicitly assumed. Replacing each assay by a fresh initialized faithful unit is a different cost model, costing O(Km) units. Neither arbitrary deep-state initialization nor a faithful-copy simulator is supplied by this theorem.

If homogeneity is not structurally established and no uniform row envelope is supplied, one must acquire each needed row. An alleged shallow assay certificate for arbitrary deep rows is invalid.

Per deployment, the policy requires only the finite set of certified damage thresholds; control storage need not grow with N if a real threshold sensor is supplied. The plant must still embody the capacity N. Per-cycle output >=g_min and duration <=tau_max guarantee useful output rate >=g_min/tau_max until failure. Energy and parts consumed over k completed cycles are at most k E_max and k R_max, so energy/part use per delivered work is bounded by E_max/g_min and R_max/g_min. An exponential total work claim consumes an exponential total supply of those resources; it does not mean exponential output from fixed fuel or spares.

The statistics can be reused for multiple N and multiple deployments on the same validated interface: the one confidence event already certifies all N. Drift outside the certified envelope, new unmodelled common modes and altered hardware invalidate that reuse. A real audit/test schedule has its own cost and failure probability.

## 7. Same-access forecast lower bound

Keep p_A=.1, q_A=.2, p_B=.2 and rewards fixed; let q_B=q0 or q0+h/N with q0=.7 and fixed h>0. For sufficiently large N both models remain in the same robust policy region, so the optimal policy is identical. Writing rho=q_B/.2,

    V_N(q_B)=(30+10/(rho-1))*(rho^N-1)/(rho-1)-10N/(rho-1).

Consequently V_N(q0+h/N)/V_N(q0) -> exp(h/q0). Choose h so that this exceeds (1+epsilon)/(1-epsilon). A constant-relative epsilon estimate therefore distinguishes these two worlds.

Under the same actual elementary transition access, a B trial at a positive state has outcome vector (.2,q, .8-q). Its one-step KL against the alternate world is O(h^2/N^2); A trials are identical. Even if the experimenter adaptively chooses actions and initial safe states, chain rule gives transcript KL <= C h^2 E[n]/N^2. Binary testing then requires

    E[n] >= (N^2/(C h^2))*kl(1-delta,delta)
          = Omega(N^2 log(1/delta)).

This includes direct lifetime sampling, full-model estimation and any other predictor using only this interface. It does not include an additional analog instrument that directly reads q with arbitrarily high precision at no charged cost. Estimating all relevant probabilities to O(epsilon/N) gives the matching N^2 scaling, up to constants/logarithms, in a compact interior parameter family.

The policy certificate itself requires only fixed parameter precision as long as the cone and prefix margins are fixed, and therefore O(log(1/delta)) observations per mode independent of N. The advantage is over an absolute forecast task. Ordinary skip-free dynamic programming equipped with the same intervals obtains exactly the same policy certificate; there is no advantage over the strongest equally informed same-decision method.

There is no universal direct-decision advantage: if two candidate repair slopes differ by Theta(1/N), exact best-policy identification can itself require Omega(N^2 log(1/delta)) local samples (swap the two slopes between hypotheses). Claiming a constant-factor near-optimality lower bound for unrestricted online policies needs a separate proof: useful operation can continue while collecting data, and the very long lifetime may make exploration inexpensive in lost useful work.

## 8. Robust finite mission guarantee

Fix a deployed policy and deterministic valid conditional bounds p_i<=p_i^+ and q_i>=q_i^- at every cycle. They may vary with history. Set b_0=1 and

    b_i=(q_i^-/p_i^+)b_{i-1} for i>=1,
    H(0)=0, H(i)=sum_{k=0}^{i-1}b_k.

At safe i>=1, E[Delta H|history] <= p_i^+ b_i-q_i^- b_{i-1}=0. At 0, the increment is at most p_0^+. Stopping at N and summing gives

    P_x(T_N<=t) <= [H(x)+t p_0^+]/H(N).

For a finite prefix followed by q^- /p^+=R>1, H(N) grows geometrically like R^N. If raw useful work per cycle is >=g_min, then

    P_x(work before catastrophe <W)
       <= [H(x)+ceil(W/g_min) p_0^+]/H(N).

This yields a constructive finite-mission design with N=O(log(W/delta)) from a prepared low-damage state, without knowing the absolute rare mean. It is a guarantee for the selected policy, not a claim that the expected-work optimum also maximizes finite-horizon success probability.

For the example A at zero and B thereafter, R=q_B^-/p_B^+ and H(N)=(R^N-1)/(R-1). Starting from healthy state 0,

    P(T_N<=t) <= t p_A^+ (R-1)/(R^N-1).

No equilibrium preparation is used. Known low damage/reset is still a required preparation resource. An arbitrary initial state near N cannot enjoy the same small risk.

## 9. Interface errors and near-optimality

Fixed numerical uncertainty in p,q can coexist with exact optimal policy certification; the value itself may vary exponentially across the same box. Physical mistakes cannot simply be union-bounded away over exponentially long operation.

If a wrong-mode event only changes the actual local transition law, include it in the actual measured command kernel and compare against controllers with that same actuator. A fixed error rate can leave the robust cone and geometric mission guarantee intact. This is different from claiming the imperfect implementation matches an ideal error-free optimum.

For example, under ideal B in the tail, independently applying A instead with probability eta changes

    p_eff=.2-.1 eta, q_eff=.7-.5 eta,
    rho_eff=(.7-.5 eta)/(.2-.1 eta).

Relative to the ideal policy its expected work has a leading ratio (rho_eff/3.5)^N, and log(rho_eff/3.5)=-(3/14)eta+O(eta^2). Constant-relative ideal performance therefore generally requires eta=O(1/N), although exponential safety remains if rho_eff>1. A coarse robust certificate may still identify the exact optimal requested control for the imperfect actuator if those actual kernels are what it measures.

If there is an extra independent catastrophic interface hazard eta per cycle, a run has mean length <=1/eta and expected useful work <=g_max/eta. The finite-mission bound acquires an additional term at most t eta. To retain an exp(cN) lifetime or an exp(-cN) per-cycle hazard guarantee, the interface hazard must be comparably protected and its actual hardware, energy and calibration cost included. The theorem does not supply that protection.

Unobserved health-state errors change the problem to partially observed control. They are not automatically absorbed by a command-kernel calibration. A verified physical state/threshold readout, or a separate POMDP analysis, is necessary.

## 10. Prior art and strongest comparison

1. Jacob Wijngaard and Shaler Stidham, Jr., **Forward Recursion for Markov Decision Processes with Skip-Free-to-the-Right Transitions, Part I: Theory and Algorithm**, Mathematics of Operations Research 11(2):295-308, May 1986, DOI 10.1287/moor.11.2.295. Primary publisher URL: https://pubsonline.informs.org/doi/10.1287/moor.11.2.295 . Its abstract explicitly identifies forward recursion for maximal expected reward from 0 to i. This is directly relevant, stronger prior art than a generic Bellman citation.

2. **Optimal control of random walks, birth and death processes, and queues**, Advances in Applied Probability, primary URL: https://www.cambridge.org/core/journals/advances-in-applied-probability/article/abs/optimal-control-of-random-walks-birth-and-death-processes-and-queues/CF6CACA2D553B8766F1B31EB6E447708 . Establishes classical optimal-control/monotone-policy context. Bibliographic authors/year should be read from the actual page before final citation.

3. Andrea Zanette, Mykel J. Kochenderfer and Emma Brunskill, **Almost Horizon-Free Structure-Aware Best Policy Identification with a Generative Model**, NeurIPS 2019, primary URL: https://papers.neurips.cc/paper_files/paper/2019/hash/a724b9124acc7b5058ed75a31a9c2919-Abstract.html . It directly studies using instance structure and action gaps to reduce policy identification complexity in discounted MDPs. Do not claim the general principle that a policy can be easier to identify than its numerical value is new.

4. Liyu Chen, Andrea Tirinzoni, Matteo Pirotta, Alessandro Lazaric, **Reaching Goals is Hard: Settling the Sample Complexity of the Stochastic Shortest Path**, ALT 2023, https://proceedings.mlr.press/v201/chen23a.html . Relevant sample-complexity and access limitations; the usual minimum-cost SSP task is not automatically identical to the present maximum-positive-work task.

5. **Robust Markov Decision Processes**, Mathematics of Operations Research, DOI 10.1287/moor.1120.0566, https://pubsonline.informs.org/doi/10.1287/moor.1120.0566 . Robust confidence-region control is existing machinery. The claimed pointwise all-model policy certificate is stronger than merely maximizing worst-case value, but follows from explicit inequalities here.

The core elementary operation is established prior art. The finite row-box cone, law-changing useful-work acquisition/forecast separation, and mission/interface boundary are the specific synthesis to evaluate; novelty is not established by this note. There is no demonstrated civilization-changing physical capability.
