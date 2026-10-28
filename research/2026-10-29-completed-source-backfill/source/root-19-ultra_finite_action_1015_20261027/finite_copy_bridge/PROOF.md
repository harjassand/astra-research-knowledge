# Finite-copy autonomous majority action: complete model derivation

Lead derivation, 2026-10-27. New arguments are not independently audited unless a separate receipt says so. This is an abstract finite-agent/reaction model; no physical chemistry, rate calibration, leader preparation or actuator is acquired. Established majority and delay primitives are ordinary comparators, not inventions.

## 1. Contract

Unknown nonnegative integer counts A,B must trigger exactly one irreversible YES action iff A>B, and NO otherwise, including ties. The controller uses local reactions and an input-independent prepared context. It has no external observer, reset or clock. A revisable limiting vote does not meet this contract: an early wrong vote may already consume the only payload.

For the constructive approximate operation supply volume V, population bound n_max, computation pair constants in [k_-,k_+], trigger constants at least g_->0, and an acquired unimolecular-clock rate interval. Prepare one neutral computation agent z and one leader L0. The actual computation population n=A+B+1 is unknown but satisfies 1<=n<=n_max. Input acquisition and the specified rate/initialization primitives are supplied interfaces with unacquired physical costs.

## 2. The five-reaction source and its finite-copy boundary

Calabrese, Doty and Latifi, [arXiv:2506.06590v1](https://arxiv.org/html/2506.06590v1), Lemma13, use

    A+N -> A+Y; B+Y -> B+N; A+B -> waste;
    C+Y -> C+N; 3C -> waste.

Give these positive constants a,b,c,r,s, respectively. Stochastic propensities are a*A*N/V, b*B*Y/V, c*A*B/V, r*C*Y/V and s*C(C-1)(C-2)/V^2. The last convention gives fluid drift d[C]/dt=-3s[C]^3; a 1/6 factorial convention only rescales s. Reporters Y+N=M are conserved. The source's definition concerns limiting concentrations, not finite-copy irreversible actions.

**Family proposition.** No fixed integer initial clock count makes these five reactions an exact finite-copy majority decider over all integer inputs and positive rates.

If rho=C(0) mod3 is positive and d=A(0)-B(0)>0, upstream events eventually leave A=d,B=0,C=rho. Each reporter keeps switching with N->Y rate ad/V and Y->N rate r*rho/V. Its stationary YES probability is p=ad/(ad+r*rho)<1; the M-reporter stationary law is Binomial(M,p). Permanent correct consensus is absent. If rho=0, choose a nonempty tie. A finite enabled event sequence can remove the clock first, create or retain a YES reporter, then consume the last A,B pair. The wrong reporter freezes. This sequence has positive probability for every positive set of constants. This proves the proposition, not a no-go for all chemical controllers or a refutation of the continuous paper.

`bridge.py` computes exact limiting single-reporter probabilities by a two-state recursion at each upstream state (j,C), where j=min(A,B). Let u=aA/V, v=(bB+rC)/V, q=cAB/V and z=s*C(C-1)(C-2)/V^2. The values f0,f1 satisfy

    (q+z+u)f0-u*f1=q*f0(j-1,C)+z*f0(j,C-3),
    -v*f0+(q+z+v)f1=q*f1(j-1,C)+z*f1(j,C-3).

At a final upstream state the values both equal u/(u+v), or are(0,1) if no catalyst remains. Fraction arithmetic replays both equations exactly. For A=B=1,C=3,V=1 and unit constants, f0=20/63,f1=34/63. This explanatory count example is not the source's canonical context. Canonical source scaling A=B=V/2,C=M=V gives terminal mean wrong-voter fractions about0.303159,0.207522,0.153829,0.119465 for V=6,12,18,24. The M-reporter mean equals the single-reporter marginal; their transient joint law is not asserted independent.

Error can decrease with volume. There is no claim that the two iterated error limits disagree or that approximate finite-copy computation is impossible.

The continuous majority primitive has an independent proof: A-B is conserved. For positive difference, A approaches that difference while B,C vanish, so Y'=aA-(aA+bB+rC)Y gives Y->1; negative difference gives Y->0. In a tie, A=B=x/(1+cx*t) and C=C0/sqrt(1+6s*C0^2*t). For p=aA+bB+rC and h=aA/p, integral(p)=infinity and h->0. The tracking lemma f'=p(h-f), integral(p)=infinity,h->L implies f->L: after a time T with |h-L|<=eta, integration bounds |f-L| by |f(T)-L|exp(-integral_T^t p)+eta. This avoids the false general pointwise estimates recorded separately in SOURCE_PROOF_FAILURE.md. The complete source paper is not audited here.

## 3. Ordinary six-state replacement

The primary comparator is Gasieniec etal., [OPODIS2016, Section2/Figure2](https://doi.org/10.4230/LIPIcs.OPODIS.2016.14). The PDF table was visually checked. Strong states P,N,Z have weights+1,-1,0; weak p,n,z have weight0. Nonidentity rules are

    P+N -> 2Z;
    P+Z -> P+p; N+Z -> N+n;
    P+n -> P+p; P+z -> P+p;
    N+p -> N+n; N+z -> N+n;
    Z+p -> Z+z; Z+n -> Z+z.

Inputs A,B initialize P,N. Prepared neutral context is weak z, an explicit initialization choice. Binary YES voters are P,p; all others vote NO. Total n and P-N are invariant. Strong cancellation leaves one sign or neither. A surviving P/N demotes Z and converts every weak agent to its sign. In a tie the last P+N event leaves at least two Z, which cannot then be removed and convert weak p,n to z. Empty input with prepared z is already NO. All relevant rates are positive. These paths from every state, finite state space, and absorbing correct consensus prove almost-sure eventual correctness for every positive rate assignment.

Full reachable-count graph checks verify invariants, reachability of correct consensus from every state and closure of that consensus. A first run used P+N->Z+z; after reading the primary table it was corrected to2Z and rerun. Historical variant outputs remain clearly named and are not the primary comparator.

## 4. Finite-time consensus certificate

Put m=min(A,B), d=|A-B|. Strong cancellation is a pure-death process with independent holding rates at least lambda_j=k_-*j(j+d)/V, j=1,...,m. For theta=k_-(d+1)/(2V),

    E exp(theta*T_ann) <= product_j lambda_j/(lambda_j-theta).

Thus t_ann=[sum_j -log(1-theta/lambda_j)+log(3/delta)]/theta has tail at most delta/3; take0 when m=0. After cancellation, clearing Z and then wrong weak opinions are each dominated by n exponential clocks of rate alpha=k_-*max(1,d)/V. In a tie only one phase is needed, but using two is conservative. Each phase has tail <=n*exp(-alpha*t). Consequently

    P(T_stable > t_ann+2*log(3n/delta)/alpha) <=delta.

For unknown inputs use worst d=0,m=floor(n_max/2),n=n_max. This is T_comp=O((V/k_-)(log n_max+log1/delta)). A promise excluding ties with |A-B|>=d_min permits the smaller d_min bound; it is explicitly separate from the all-input contract.

Also E[T_stable]<=sum_j V/[k_-*j(j+d)]+2V*H_n/[k_-*max(1,d)]. Nine channels have total nonidentity propensity at most q_max=9*k_+*n_max^2/V. The expected update count before any integrable stopping time is at most q_max times its expected time. Identity collisions and physical encounter dissipation are not silently included as zero-cost chemistry.

## 5. Autonomous irreversible commitment

Add one leader and the unimolecular chain L0->L1->...->Lh. Every step has its own unknown constant in [lambda_-,lambda_+]. At Lh, six local rules Lh+v->ACTION_bit(v)+v sample a computation agent, preserving its state. The only ready leader is consumed, so exactly one action occurs. Total trigger hazard is >=g_-*n/V>=g_-/V.

Use delta=epsilon/4 for T_comp. Choose

    h=ceil(log(4/epsilon)/(log2-1/2)),
    lambda_+=h/(2T_comp), R=lambda_+/lambda_-.

Coupling exponential holding times and their elementary Chernoff bounds gives

    P(T_clock<T_comp)<=exp[-h(log2-1/2)]<=epsilon/4,
    P(T_clock>2h/lambda_-)<=exp[-h(1-log2)]<=epsilon/4.

The upper clock deadline is4R*T_comp; mean clock time is at most2R*T_comp. Trigger allowance (V/g_-)*log(4/epsilon) fails with probability at most epsilon/4. A wrong or late action requires at least one of: computation fails to stabilize by T_comp; clock finishes early; clock finishes late; trigger finishes late. The union bound, without assuming independence of these bad events, yields

    P(correct action by4R*T_comp+(V/g_-)*log(4/epsilon))>=1-epsilon.

The leader has no effect on computation before readout. The argument covers heterogeneous clock constants throughout the acquired interval, not only equal endpoint examples.

Resources: at most n_max computation agents plus one leader; h+9 abstract species; h+15 channels; exactly h clock updates and one action update. Mean action time is at most h/lambda_-+V/g_-. Mean computation updates before action are bounded by q_max times that mean. Chemical free energy per update, leak/reversibility, mixing, preparation, readout/actuator chemistry and absolute-rate acquisition remain UNKNOWN.

A selectable slow clock rate is a real extra interface. With a fixed lambda_+ instead, choose h at least both2lambda_+*T_comp and the confidence bound: reliability survives by paying a potentially large stage/species/update cost. Its clock deadline is2h/lambda_-, rather than substituting4R*T_comp after integer rounding. Both regimes are serialized. The construction claims neither a free long timer from dense initialization nor a fixed network working uniformly for arbitrary population sizes and unbounded rate ratios. Displayed deadlines are floating evaluations of these analytic formulas, not interval-certified laboratory clocks.

`GENERATED_ACTION_CRN.json` gives the actual abstract network for n_max=9,V=9,epsilon=.05:23 stages,32 species,38 channels, prepared z=1,L0=1 and unknown P+N<=8. Full finite-count positive/negative/tie calculations run. For a computation generator Q the ready distribution is h applications of lambda*(lambda I-Q^T)^-1; the local trigger uses the ordinary killed-process equation (rI-Q)b=r*w. An independently assembled full computation/clock generator agrees with this reduced phase-type calculation. These standard resolvents are reference tools, not a new law.

## 6. Exact-N ordinary census and the unknown-N boundary

If exact N fresh tokens is supplied, a leader L_(j,d) can consume tokens without replacement. Fresh A,B,neutral S increment j and change d by+1,-1,0; each becomes SPENT. At j=N the leader commits YES iff d>0. The signed-sum invariant proves zero logical error for all positive constants. There are N^2 transient leader states, two terminal states, four token states,3N^2 channels and exactly N updates. With pair constants at least k_-,

    E[T]<=(V/k_-)*H_N; P(T>t)<=N*exp(-k_-*t/V).

For N=V=9 the unit-rate mean is exactly7129/280, about25.4607, with nine updates and87 species. The exact recursion and generated network are in CENSUS_RESULTS.json. This stronger comparator pays for exact N; it is not assigned that information for free in an upper-bound-only problem.

For standard CRNs without inhibitors, finite reachability is monotone under adding input molecules. If an unknown-population controller on A=1,B=0 commits YES along a finite firing sequence, add two B molecules with the prepared context unchanged. The same sequence remains enabled and has positive probability, but its irreversible YES is now wrong. A population upper bound admitting both inputs does not remove this obstruction, even if all rates are known. Exact-N promises, absence/cover-time information, inhibiting access or nonzero error change the contract. Revisable consensus is not an irreversible action and is not ruled out.

## 7. Consequence

The completed bridge is an abstract finite-copy unknown-input-to-action operation with explicit reliability, latency, clock, state and update costs. It repairs an operational handoff the continuous primitive does not supply. The strongest equal-information ordinary implementation is the same six-state consensus plus the same Erlang clock, so no new capability or advantage is established. The exact-N census and an external calibrated timer are additional strong controls when their extra access is acquired.

The next hard attack must change an operational frontier: acquire a physical sparse leader, clock/readout primitive and justified rate bounds, then improve error/time/species/energy against these controls. More fixtures or tighter constants alone would not change the present decision. No physical device, chemistry advantage, novelty or publication readiness follows.
