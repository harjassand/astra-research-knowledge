# Unknown drift budget: finite full-information master
2026-10-29. New author construction; receiving review pending. This removes the declared-budget input of TRACKING_CORE_DRAFT.md, not its source privacy/predictability assumptions.

## Finite controller bank, fixed before data
Let T>=2, L=ceil(log2 T), J=ceil(L/4). Use the following finite bank, identically for each star edge:
- net radii epsilon_j=2^(−j),0<=j<=J, with rational-quaternion gridm=5*2^j;
- shares alpha in {0} union {2^(−k):1<=k<=L+1};
- learning rates eta_l=p*2^(−l−1),0<=l<=L+1.
There are H=O(log³ T) base learners. Each is the exact fixed-share learner in the core draft, with its own net and fixed parameters. All bases receive the SAME actual probe records. They are not separately deployed quantum experiments or counterfactual source histories.

At an active time, baseb has predictable candidate distributionw_{b,t}. Maintain a separate ordinary rational multiplicative-weight masterv_t over theH bases. Its action distribution is
 pi_t(C)=sum_b v_t(b)w_{b,t}(C),
with duplicate net rotations treated as distinct labels if convenient. Sample one candidate from this mixture on each star edge; arbitrary independent star rotations still define a consistent global frame by setting root frameI and site framesC_i.

## Shared unbiased master feedback
A real probe suppliesfhat_t(C) in[0,1] for every candidate on every net. For each base compute the exact rational weighted estimate
 fhat_{b,t}=sum_C w_{b,t}(C) fhat_t(C),
using weights from BEFORE the current feedback. It remains in[0,1]. Update every base with its ordinary importance-weighted probe record. Update the master with ell^master_t(b)=1_probe fhat_{b,t}/p, using rational eta0<=p/2. Its conditional mean is the base's predicted true shifted loss along the SAME actual physical history. Thus the ordinary MW bound gives expected true-delta regret to any FIXED baseb of at most
 R_master=45[lnH/eta0+eta0 T/p].
Choose eta0 within factor2 ofmin(p/2,sqrt(p lnH/T)) using the available rational grid. Then R_master=O(sqrt(T logH/p)+logH/p).

Each base's pathwise fixed-share inequality bounds its predicted loss against every predictable net path, regardless of whether its own candidate was actually deployed. This is legitimate full-information feedback: the loss process is induced by the actual master, and all virtual base predictions are evaluated on that single process. It is NOT a comparison with the memories that separate base policies would have generated.

## Oracle bound without a supplied variation budget
For any deterministic envelopePbar bounding the actual predictable frame variation, set
 S_b=min(T−1,ceil(Pbar/epsilon_b)).
For alpha_b=0 regard the following bound as available only forS_b=0. For every otherbaseb the core theorem and master bound imply
 E total selected star loss
 <= (n−1)R_master
    + min_b {18(n−1)T epsilon_b²
       +45(n−1)[K(S_b,alpha_b)/eta_b+eta_b T/p]}. (M1)
The minimizing base is a deterministic proof choice based onT,Pbar, not a hindsight choice based on probe outcomes. The implemented controller never receivesPbar. The inequality is valid for every such deterministic envelope, separately, with one and the same controller.

The bank contains a radius within a constant factor ofmax(T^(−1/4),(Pbar/T)^(1/5)), a share within a factor2 of the budget-tuned optimum whenS_b>0, and a learning rate within a factor2 of the relevant optimum. The resulting entropy complexity satisfiesK/T→0 wheneverPbar/T→0; alpha=0 covers the static case. The extra master term hasR_master/T→0. Therefore the selected average loss tends to zero for every predictable hidden-frame family with a deterministic sublinear variation envelope, WITHOUT knowing that envelope. A high-probability statement for retrospectively observed variation, or arbitrary hindsight paths, is not asserted.

The same construction can use the robust square-root comparator defect term instead of18(n−1)T epsilon² when there is additional predictable current-frame defect. The rate then depends on BOTH variation and defect budgets. No unrestricted rapidly changing source guarantee follows.

## Exact arithmetic and the crucial sampler order
Base integer weights have the polynomial bit bounds in the core draft. For the master, each fhat_b is rational with denominator dividing the common probe-loss denominator times the base weight sumQ_b. At each update clear allH denominators using their product (an LCM is optional). The logarithm of this common denominator is the sum ofH polynomial bit lengths. Accumulating these integer update factors forT rounds remains polynomial: a deliberately loose bound is O(H T² logG_base) master-weight bits, plus fixed parameter denominators. H is polylogarithmic and the largest net isO(T^(3/4)); all exact arithmetic is finite, but this is not a practical runtime claim.

A candidate sampler chosen only AFTER sampling its master base can have base-dependent cap probability, biasing the intended mixture. Avoid that error. For EACH star edge, pre-sample one prospective candidate from EVERY base and the master base choice, checking all capped samplers before any role/source call. Conditional on past weights, every accepted index is independent of its rejection count, so the joint cap event is independent of the complete vector of proposed candidates and master choices. Deploy only the prospective candidate of the selected base. Retire unused candidate keys privately. This costs H+1 candidate/master draws per edge per round, not additional quantum source calls.

Also pre-sample all role-specific probe/matching/permutation keys under FINITE_SAMPLER_SCHEDULING_CLARIFICATION.md. Their laws and cap ranges must not depend on the freshly selected candidate/base. Role coins have their neutral independent count/output implementation. Charge all attempted samplers in the union bound. After a neutral stop, zero every true/estimated loss; the proof can continue virtual fixed-share updates without any physical source calls.

## Operational meaning
Substitute(M1) in the same arbitrary-memory guard readiness formula. Under sublinear predictable frame variation, the fixed-port concatenated compiler gives readiness tending to one and its conditional source-exposure rate, with model-free accepted soundness unchanged. All controls, buffers, finite code generation and actual learner costs remain paid. This changes the fixed-frame hypothesis to a slowly drifting frame without demanding that the learner uniquely identify it. It is neither future-frame prediction nor an established practical advantage over an equally informed adaptive full-path conventional controller.
