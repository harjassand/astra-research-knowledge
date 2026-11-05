# Ordered-fault-tuple cover for a fixed minimum-weight decoder

## Result and assumptions

On a finite graph with positive integer edge costs, independent rational edge-error probabilities, two rough boundary sets, and a fixed exact minimum-weight decoder/canonical residual path selector, the construction below gives independent Bernoulli trials with mean `P(failure)/Z`. The rational normalizer `Z` is certified by a finite positive supersolution, not estimated from samples. There is no walk-length truncation. Arithmetic implementation details are in `SAMPLER.md`.

The operation collapses clean-route multiplicity by proposing only the ordered oriented faulty edges of a canonical witness. It does not remove all witness overlap. A repetition-line counterexample below proves exponential worst-case inefficiency even with exact gap distances and unique clean routes. The demonstrated finite normalizer gains must not be called a general FPRAS, an all-distance polynomial algorithm, or a speed advantage over unexecuted competitors.

## Canonical fault tuple and coverage

For an error configuration E that the fixed decoder fails to correct, let C(E) be its minimum-weight correction. The fixed canonical selector chooses a simple left-to-right path P in E XOR C(E). Record, in path order and orientation, precisely those edges of P that belong to E. Write this tuple as F=((u_1,v_1,e_1),...,(u_k,v_k,e_k)). Underlying edge IDs are distinct; adjacent faulty edges may share vertices.

Minimum-weight optimality implies the faulty-edge cost on P is at least the clean-edge cost. Otherwise replacing C(E) by its symmetric difference with P would produce a lower-cost correction with the same syndrome. Since costs are positive, k is nonzero.

Let d_L(u) and d_R(v) be lower bounds for clean-path cost from the left boundary to u and from v to the right boundary. Let g(v,u) lower-bound every clean segment between those vertices. These bounds may allow paths that are incompatible with the eventual tuple; that enlarges the cover but cannot remove a canonical tuple. Define

    S(F) = sum_j c(e_j) - d_L(u_1)
           - sum_{j<k} g(v_j,u_{j+1}) - d_R(v_k).

Then S(F)>=0 for every canonical tuple. Current instances use exact uncapped boundary distances and internal g=min(graph distance,64). Fault starts/ends are restricted only where rough-boundary leaves cannot occur internally on a simple witness.

## Positive folded proposal

Fix an integer modulus N. A state is (last head vertex v, accumulated-score residue r). Its nonnegative continuation weight to the next fault (x,y,e) is

    q_e * 2^(c_e-g(v,x)),

with residue shifted by c_e-g(v,x). The terminal weight is

    t(v,r) = 2^(-d_R(v)) * 2^(-((r-d_R(v)) mod N)).

The first-fault weight is q_e*2^(c_e-d_L(u)); it enters residue (c_e-d_L(u)) mod N. Let T be the continuation matrix. A finite positive rational table H satisfying H>=t+T H defines a killed Markov proposal: stop with t/H, make each transition with T_ij H_j/H_i, and assign leftover probability to a null result. Root choices are proportional to their first-fault weight times H at the next state, with total Z.

For any stopped ordered sequence F, multiplication telescopes. Writing r_final=S(F) mod N, its proposal mass before final filtering is

    (product_{e in F} q_e) * 2^(S(F)-r_final) / Z.

Reject immediately if an underlying edge ID repeats. This removes only tuples that cannot be canonical, and bounds the number of distinct proposed faults by the graph edge count. Do not reject shared endpoints. Reject S(F)<0. For nonnegative score, accept the final score filter with probability 2^(-(S(F)-r_final)). Its exponent is a nonnegative multiple of N. The remaining tuple mass is exactly product q_e / Z.

The implementation may use a rounded-up terminal term when CERTIFYING H, but the runtime stop weight must be the exact t above. Similarly, the folded distance kernel must retain its residue-dependent shifts: a scalar positive near/far decomposition does not generally remain a positive folded decomposition. The current sampler uses each actual capped distance explicitly.

## Full-error completion and exact acceptance identity

Given a surviving distinct-edge tuple F, force its edges faulty and draw every other edge independently with its q_e. For any compatible full E, the joint mass is

    (product_{e in F} q_e)/Z * product_{e not in F} q_e^E_e (1-q_e)^(1-E_e)
    = P_q(E)/Z.

No clean-edge factor is missing: the proposal never selected or conditioned a clean gap route. Finally accept if and only if the canonical ordered ORIENTED faulty-edge tuple of E is exactly F. Every failing E has exactly one such tuple; every nonfailing E has none. Summing gives acceptance probability P_q(failure)/Z. Thus independent ideal-bit trials produce an ordinary binomial count.

An exactly checked outward fixed-shot Clopper-Pearson interval for this count, multiplied by exact Z and expanded by the explicit input-conversion total-variation bound, covers the original stated graph law at the specified confidence. It is not an optional-stopping interval. Python PRNG output is reproducible pseudorandomness, not a mathematical source of independent ideal bits or a hardware-noise certification.

## Concrete certificate

The current d13 and d21 instances use N=D=64, q denominator 2^64 and H-grid 2^-56. `build.py` and `certify_tuple.cpp` use upward rounding at every positive distance term and a final all-row recheck. The runtime uses unrounded exact weights; certificate slack is null probability. A separate four-limb audit instead reconstructed every row at a full common denominator, requiring 185-bit row arithmetic, and checked graph-distance lower bounds by all local edge potential inequalities. See `../qec_fault_tuple_audit_20261105/AUDIT.md`.

The compact H table does not imply small total storage or preprocessing: internal distances and near-pair kernels are largely dense at the measured sizes. All such arrays, construction work, decoder allocations, confidence computation and process startup must be charged.

## Exponential obstruction even without route multiplicity

Take a repetition line of 2m unit-cost edges with independent error probability p<1/2 and the standard minimum-weight decoder, with any fixed tie rule. Every monotonically ordered m-edge subset is an admissible fault tuple. Its total clean-gap distance is m, so S=0 and it contributes p^m to the exact cover. Therefore

    Z >= binom(2m,m) p^m.

The failure probability is no larger than Pr[Bin(2m,p)>=m]. For the successive binomial terms starting at m, their ratio is at most p/(1-p). Hence

    P(failure) <= binom(2m,m) [p(1-p)]^m * (1-p)/(1-2p),

and consequently

    acceptance <= (1-p)^(m+1)/(1-2p).

This decreases exponentially with m for every fixed p>0. Ties only lower the upper bound, while nonmonotone tuples, score folding and supersolution slack can only increase Z. The obstruction survives exact, uncapped gap distances, a unique geometric clean route, and no score aliasing. Its source is the relaxation that does not condition omitted line edges clean. It is a limitation of this cover, not an impossibility theorem for rare-event estimation or repetition-code analysis.

## Independent validation

The finite audit exhausts all errors and all distinct-edge ordered tuples on a weighted cyclic graph for score moduli 1,2,4 and exact/capped distances. It checks the actual killed Markov law, including null mass, repeated-edge rejection and boundary shifts, and recovers Z*acceptance=62229/156250000 exactly in all six cases. Deliberately rejecting shared endpoints introduces bias. Concrete checks reconstruct both large tables and verify the floating-CDF proposal accelerations by outward integer tests; these accelerations cannot affect the law when their stated arithmetic assumptions hold.
