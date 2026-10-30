# Two-seed logarithmic occupation gap and exponential-weight route
Status: new personal derivation, unreviewed. Not part of the four frozen A=1 proof files. This is a concrete next mechanism test, not a claimed global theorem.

Take the multi-seed contract of INCOMING_MOMENT_MEMORY_LEMMA_CANDIDATE.md with a0=2, m>=3, v=m-2. Active states have A>=2. The source estimates give, for A<=epsilon N,

    c A N^v <= Q log A <= C A N^v,
    Q(1/A)<=-cN^v.

The second estimate follows from A-producing rate >=cA^2N^v times the negative 1/A increment of order A^-2; A-decreasing source terms have an extra A/N factor. Globally Q(1/A) is bounded above by CN^v; clearing dominates when A>=epsilon N. The positive killed supersolution C/[A N^v]+C/N^m therefore yields

    T(A)<=C/(A N^v)

uniformly over active starts (the N^-m term is smaller). More explicitly near low A its killed drift is <=-1; at high A the killing of C/(A N^v) is order N, dominating its possible order1 positive drift. Fixed bounded competing killing only improves this bound.

Choose K=floor(N^eta) with 0<eta<v/m. Before hitting A>=K, clearing-plus-bounded-competitor hazard is <=C(K^m+K+1). The unkilled mean hitting time from A>=2 is <=C/N^v by the 1/A drift. Hence killing before that hit has probability o(1). The overshoot is bounded by m.

For initial 2<=A<=sqrt(K), stop at the mesoscopic hit or killing. The terminal alive log A is at least log K on an event of probability1-o(1); subtracting initial log A gives a net expected logarithmic increase >=c log N. Cemetery log can be assigned0; its killing contribution in the stopped generator is NONPOSITIVE. Since Q log A<=C A N^v, Dynkin gives

    c log N <= C N^v E int_0^tau A_s ds,

so U>=c log N/N^v. Together with T<=C/(A N^v), this implies T/U<=C/log N on this lower region. Starting above sqrt(K), stop at killing or first crossing below sqrt(K). Before the crossing U_pre>=sqrt(K)T_pre; the landing lies in a bounded band below sqrt(K) and the preceding estimate applies. Strong Markov proves uniformly

    T/U <= C/log N.                                    (L2)

The same argument applies at fixed B=q with the actual bounded immigration/activation competitors. Clearing-first probability still tends to1 by the occupation-Holder estimate, and U>=cN^{-(m-1)} follows from the pointwise clearing/activation hazard comparison.

## Why the scalar worst-case reset formula is insufficient
Its later envelope p0~N^-v is too large relative to the crude opportunity floor N^{-(m-1)}. But the incoming-moment lemma suggests a sharper actual low-walk estimate: escape/bad probability <=C t, where t is the FIRST clearing's inverse-m-th moment, without later p0 cross terms.

Reason to test rigorously: before accumulating m low-phase immigrations or returning safely, there are only O(m+q) reset launches because each launch lowers the phase while immigration raises it. Every immigration race consumes one inverse-A power; the full family of incoming-moment bounds propagates each remaining inverse power across fast resets. Fast bad immigration itself has probability <=C(1+A_in)^-m from the incoming-dependent killed-time bound. Composing these positive kernels for the bounded number of launches should bound every bad/escape branch by C times the initial inverse-m-th moment. This requires exact full-processor moment control, not just one-clearing estimates; repeated activations increase A,N and therefore decrease the candidate incoming-moment supersolutions, which is favorable.

If that kernel statement is earned, t<=CT and (L2) give an actual up/down opportunity ratio O(1/log N). A factorial test weight has polynomial upward-shift amplification and is then too aggressive. Exponential phi_theta(r)=exp(theta r) has only a fixed shift multiplier; every fixed theta is compatible with a vanishing logarithmic gap. Its polynomially enlarged stopped values would still dominate polynomial boundary leakage and establish all exponential total-count moments by varying theta. Thus factorial growth is not a necessary capability supplied by the method.

Outstanding: complete the full-processor incoming-moment kernel argument including inactive outputs requiring up to two actual seeds, establish the coefficient-one section drift, then recheck both uncapped values with exponential rather than factorial contraction. No global two-seed recurrence conclusion is asserted here.
