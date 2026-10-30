# A graph-acquired same-episode occupation interface

30 October 2026. New unreviewed construction; no reviewed source is modified. This earns a broader local interface, NOT recurrence of a broader full network. It replaces an invalid direct-source clock transfer with a tagged-particle argument and a logarithmic good-set threshold.

## 1. Inputs and exact stopping

Use the raw module in GRAPH_ACQUIRED_DORMANT_RETURN_BOUND.md. The finite conversion generator Q is irreducible; distinguished residual species a=X_1; all conversions X_i+D -> X_j+D conserve D. The only linear D-consuming birth is a+D -> 2a. Nonlinear seeds 2a -> a+D and optionally 2a -> 2D compete with clearing at rates k_seed(a)_2 and k0(a)_2. The 2D -> a+D channel is required to have positive rate whenever the seed 2a -> 2D is present; otherwise it may be absent. This is a load-bearing fast-accessibility condition, not just a favorable optional term: without it a seed can remove the last two type molecules and create a fast-absorbing positive-D face. Total residual count n=sum X_i+D is conserved until clearing. At least one type molecule is required unless the optional 2D channel is enabled; states with no enabled fast path are not active inputs.

Physical A=a+a0, a0>=2, m=a0+2. Fix b>=q. Multiply fast rates by (A)_a0 (b)_q, as in the completed model. Stop sigma at the first clearing, D=0, or connector event. No connector is continued within this episode. Define the actual physical moments

    T=E sigma,   U=E integral_0^sigma A_t dt,
    V_m=E[(1+A_sigma)^(-m); D_sigma=0 is the stop].

For fixed graph/rates there are C,c,M such that, with x=1+a_in and every active positive-D input,

    T <= C U/x + C (b)_q^(-1) n^M exp(-c x),
    V_m <= C (b)_q U/x^2 + C n^M exp(-c x).

In particular, for n large and x>=C0[log(2+n)]^2,

    T/U <= C/x,       V_m/[(b)_q U] <= C/x^2.

The constants may be enlarged on bounded n. These inequalities concern the SAME first episode, including its actual dormant/connector stopping events.

## 2. Polynomial moment cost, earned independently

Let L be maximal shortest conversion distance to a and H=2L+3. With D>=1 and at least two type molecules, convert two chosen molecules to a along their paths (at most 2L jumps), then clear. With one type molecule, first convert it to a, then use a+D -> 2a: if D=1 this is already the dormant stop, otherwise clearing is possible. With zero types the positive optional 2D channel supplies a first type, unless the state is inactive and excluded. The stated paired-channel condition prevents entering such an excluded face from an active input. Thus a path of at most H enabled fast jumps reaches clearing or D=0.

Every required positive operational propensity is bounded below by a fixed positive constant; every total operational propensity is at most C n^2. Hence the conditional probability of such an exit within H jumps is at least c n^(-2H), from every nonabsorbed active state. The total operational jump rate is bounded below away from zero there. Conditional geometric-block domination therefore supplies, for every fixed integer j>=1,

    E (sigma_op)^j <= C_j n^(2Hj).

No independent blocks are required. Physical time is at most C sigma_op/(b)_q because (A)_a0 is uniformly positive. Adding the connector stop only shortens the episode. The common conversion clock u=integral D dt_op satisfies E u_sigma <= C n^(2H+1). These deliberately coarse polynomial costs are enough below; they are NOT a population-uniform fast-clearing claim.

## 3. Tagged original-a cohort

Tag the a_in initial a molecules. In the common D-clock, their conversion motions are independent Q-chains, until a seed removes a tag. Continue each removed tag as a fictitious independent Q-chain. The actual surviving tagged cohort is obtained by deleting tags from this reference cohort. The a+D birth preserves its original a tag; optional 2D adds particles; neither removes tags. A seed removes at most two. Clearing ends the episode.

There is a computable p>0 with

    inf_{u>=0} P_a(X_u=a) >= p.

For example choose t0=1. Prescribed finite paths and final no-jump events give min_i P_i(X_t0=a)>=p1>0. For u>=t0 apply the Markov property at u-t0; for u<=t0 use the no-jump probability exp(-q_a t0). Take p=min(p1,exp(-q_a t0)). Constants use only finite graph/rate data.

At deterministic u the reference count Y_u is binomial with a_in trials and success probability at least p. Consequently P(Y_u<=p a_in/2)<=C exp(-c0 a_in). To extend this to a finite interval, a first downward crossing of this level must be a conversion jump from a state with Y already at most p a_in/2+1. The total reference jump intensity is at most C a_in. Its compensator and the same binomial estimate give

    P(inf_{0<=u<=R} Y_u < p a_in/2)
       <= C(1+a_in R) exp(-c0 a_in).

There is no conditional-independence claim after survival or at a stopping time.

The number of nonlinear seed marks before clearing has a geometric tail, since their common (a)_2 clock is independently marked as seed versus clear with fixed probabilities. The additional connector/dormant stops only shorten this count. Thus the probability that seeds remove more than p a_in/4 tags is at most C exp(-c1 a_in).

Choose the deterministic reference horizon

    R=n^(2H+1) exp(c0 a_in/4).

Markov's inequality for the earned common-clock mean gives P(u_sigma>R)<=C exp(-c0 a_in/4). Combining the horizon, reference-cohort crossing, and seed-count estimates yields

    P(E_bad) <= C n^M exp(-c a_in),

where E_bad is the event that a_t<p a_in/4 at some t<sigma. Small a_in can be absorbed into constants. This argument retains the actual stopped law; it never treats the surviving reference tags as conditionally independent.

## 4. Same-episode inequalities

On E_bad's complement, A_t>=c x throughout, so sigma<=C x^(-1) integral A_t dt. On E_bad, Cauchy-Schwarz and the independently earned physical second moment give

    E[sigma; E_bad] <= C (b)_q^(-1) n^M exp(-c x).

This proves the displayed T bound.

For V_m, use its exact terminal-jump compensator. Only a+D -> 2a with D=1 can produce the dormant stop. Before the first low-cohort crossing, its physical rate times outgoing reward is

    (b)_q (A)_a0 k a 1_{D=1} (2+A)^(-m)
        <= C (b)_q A^(-1)
        <= C (b)_q x^(-2) A.

The pre-crossing indicator is predictable, so integration bounds the dormant reward before that crossing by C(b)_q x^(-2) U. Dormant entries after the crossing have reward at most one and probability at most P(E_bad). This proves the V_m bound without multiplying a compensator by a nonpredictable future-survival event.

Finally the initial physical holding time gives

    U >= c x /[(b)_q (1+n)^(a0+2)].

Indeed all fast propensities are at most C(b)_q (1+n)^(a0+2), and the fixed connector rates i+tAb are bounded by the same expression for b>=q. The first holding interval is part of the episode. Dividing the error terms by this lower bound, x>=C0 log^2(2+n) makes every fixed polynomial error smaller than x^(-2) for large n. Hence both normalized inequalities follow.

## 5. Consequence, comparator, remaining gap

This is an actual finite-graph acquisition: shortest paths give the coarse absorption cost and p; tagged conversion chains give exponential depletion control; the same episode's compensator gives the weighted dormant reward. It does not assume a direct a-producing source at each face and survives the two-edge Erlang obstruction to O(1/n) clocks.

The ingredients are ordinary finite-state path bounds, labeled-particle coupling, Chernoff bounds, and stopped compensators. The useful change of construction is a logarithmic good set: polynomial cost times exp(-c a_in) is negligible there. It is not a claim of novelty over multistep Foster theory, and it does not replace the required bad-face Green or full signed-cycle source.

In particular, this note does NOT earn a uniform polynomially small clearing-output inverse-A profile from every seeded input, a full seed-phase continuation for arbitrary conversion graphs, or the associated two-block correction. Those remain required before any broader recurrence statement. The accepted four-species theorem remains the completed frozen 17-source bundle only.
