# Expected private-event execution, separate from worst capped stages

This is a companion accounting consequence, not an alteration of the frozen baseline or a gate-count/practical-advantage claim. It applies only if the implementation actually measures the private first-event branches after complete amplification and executes the resulting classical loop until its next boundary. A statically padded coherent circuit still pays its full worst cap.

Let E(t)=Tr(H rho(t)). Under the acquired energy-form bounds

    |Tr i[K,H]rho|<=a_E E+2 r_E sqrt(E),
    G†H<=-kappa H,

and sqrt(lambda)>=2a_E/kappa, Young's inequality gives

    E'<=-lambda*kappa*E/4+4r_E²/kappa.

The exact physical dark-jump intensity is 2lambda E. Integrating and dropping nonnegative final energy yields

    E N(T)<=8E(0)/kappa+32r_E² T/kappa².

Prescribed system-only trace-preserving instruments leave the unconditional source energy unchanged. General source interventions add 8/kappa times their actual positive expected energy injections; no free control energy is assumed. Initial joint source/system/reference states are allowed, with E(0) paid.

For the exact capped process the number of first-event executions is bounded by Wcap+min(N,Mcap), with the harmless extra slots in the received call convention. Hence its expected padded kernel-slot proxy is at most

    d_A(K+1)[Wcap+8E(0)/kappa+32r_E² T/kappa²].

For the finite implementation retain ONLY its bounded integer execution counter in the existing count-augmented common-uniform hybrid. Do not compare full continuous and discrete timestamp records in TV. If this counter marginal has TV error at most epsilon_count and is bounded by Scap, its mean changes by at most Scap epsilon_count. The same numerical budgets can provide epsilon_count<=epsilon by retaining that counter as an output of the proof; the physical consumer need not receive it. Thus an explicit conservative implementation bound adds Scap epsilon to the square brackets. This counts executed padded words, not gates, and it is not a new worst-case complexity bound.

For the SAME localized weak-chain coupling with ||A||<=1, r_E²<=1 and kappa=19/39. Arbitrary initial source inputs have E(0)<=n. At T=1 and Wcap=258 the exact expected calls are at most

    258+8n*39/19+32*(39/19)².

The initial independent stationary classical law can instead be represented by the coherently prepared pure Gibbs state under the established adjoint-diagonal observable/control restriction; then E(0)=0. This is a paid representation of that particular classical task, NOT a replacement for arbitrary correlated CQ inputs or a claim about physical bath emission records.

The sharper bound is a familiar trajectory-style expected-runtime accounting. The lower actual call count does not remove the per-word LCHS, reversible arithmetic, operator encoding, or control costs. It also does not challenge the observed small dense/effective classical win. Any reported expected proxy must be labeled separately from the unchanged worst-cap table.
