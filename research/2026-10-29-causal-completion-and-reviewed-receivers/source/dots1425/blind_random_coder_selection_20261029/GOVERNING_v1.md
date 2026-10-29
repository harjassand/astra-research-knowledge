# Blind rank-and-code selection by complete-block validation
2026-10-29. Author construction; independent receiving review required. This combines established random coding and conventional holdout testing with the received forward-query physical decoder. It is not a new decoupling law or a practical high-rate coding claim.

## Physical task and candidate channels
Fix a stationary memoryless CPTP channel N:C^D -> C^Dout, D=2^n. The controller receives the logical input BEFORE encoding and has trusted preparation, endpoint gates, quantum buffers, and Bell tests. Logical dimension k=2^ell<=D is specified. N is fixed independently of all code seeds; arbitrary seed-responsive or memoryful noise is excluded. No rank is supplied.

At stage j=0,1,... set R_j=2^j and L_j=(j+1)^2. Each of L_j trials draws a NEW known random Clifford k-code E_s, and defines a complete finite candidate channel M_(j,s): fresh training through N E_s, joint compression with the later encoded payload, learned small-channel physical recovery, and all abort/default completions. Its rank parameter is min(Dout,kR_j), with the received padding rules. Use the received Petz construction with total fidelity overhead tau<=epsilon/32. The conventional SDP alternative is allowed if its own overhead is paid. Every validation and every service run starts a FRESH complete training block; only the classical code seed and controller parameters are retained after selection.

Apply an independent uniform logical Pauli before the known encoder and undo it after decoding. Retire the key, and include every internal outcome in the averaged CPTP channel. Write ell_(j,s)=1-F_e(M_(j,s)); this is unchanged by padding. The reduced padded channel has half-diamond distance exactly ell_(j,s). This is not a joint-output guarantee with a released pad key, and does not apply to a task where an already encoded payload is supplied without pre-encoding control.

Finite Clifford sampling uses the received bounded integer sampler. Its predeclared failure completion is included in the seed distribution; choose its failure probability so its contribution to the SEED-AVERAGE fidelity loss is at most epsilon/64. Equivalently one may repeat the exact sampler almost surely; the bounded version is the governing finite interface here. Candidate-specific decoders remain complete CPTP channels, even on that fallback seed.

## Exact acceptance schedule
Take rational 0<epsilon<1 and 0<delta<1. For trial a=1,...,L_j, let
 delta_(j,a)=delta 2^(-j-1)/L_j,
 b_(j,a)=LEAST integer b with 2^(-b)<=delta_(j,a),
 m_(j,a)=ceil(32 b_(j,a)/epsilon).
Run m independent whole-candidate Bell tests using sacrificial logical halves and fresh training blocks. Accept this seed/rank pair iff its failure fraction is <=3epsilon/4. Otherwise try the next fresh seed; after L_j failures increase j. The real payload is not consumed during selection. A validation block costs the full training-query count q_j plus one encoded Bell-payload source call. No saved gauge-dependent program from validation is reused.

Trusted measurement, seed and synthesis errors must either be implemented within the received candidate budget or explicitly debited. The theorem's acceptance statistics assume ideal trusted Bell tests; a bounded test error requires correspondingly shifted thresholds. Actual seed and gate algorithms are finite mathematical interfaces, not claims of executed hardware.

## Model-free statistical soundness
For ANY fixed N, conditional on a proposed seed and all preceding search history, its complete fresh-block failure bits are IID Bernoulli(ell_(j,s)). If ell_(j,s)>epsilon, Chernoff gives false acceptance <=exp(-m epsilon/32)<=delta_(j,a). Union bound over the countable schedule gives
 Pr[ever accept a candidate with halfdiamond(M_(j,s),id)>epsilon] <=delta.
The bound is on the fresh-service AVERAGED channel conditional on the accepted classical seed/parameters and validation transcript. It is not a guarantee for every internal training realization. The independence of future whole blocks makes this an operational service statement, not postselection on the actual payload. A pass does not establish a Kraus-rank bound. For unpromised sources the search need not terminate.

## Completeness for an unknown finite rank
Suppose the actual Kraus rank is r, and set j*=ceil(log2 r). Assume the quantitative random-coding regime
 A=r sqrt(k/D)<=epsilon/128,
 equivalently D>=16384 k r^2/epsilon^2.
The received random-code/Petz theorem gives exact-uniform-seed average loss <=2A+tau<=3epsilon/64. The finite seed-sampler fallback contributes at most epsilon/64, so the actual finite seed distribution has average loss <=epsilon/16. This holds at EVERY j>=j*, not merely at the first adequate guess. Markov implies at least3/4 of seeds have ell_(j,s)<=epsilon/4.

For any such good seed, the same elementary upper-tail calculation as the received rank-selection theorem yields rejection probability <=exp(-m epsilon/4)<=delta_(j,a)^8. Since delta_(j,a)<1/2, it is at most1/256. Hence the conditional probability of a failed trial, for every reached j>=j*, is at most1/4+1/256<1/2. All fresh seeds and blocks are independent of past source calls; bad earlier trials do not alter N. Consequently
 Pr[stage j fails | stage j reached] <=2^(-L_j).
A successful trial may also be a statistically false acceptance; this only helps stopping and is accounted separately by the delta soundness budget.

Thus the search stops almost surely under the stated promise. The probability of reaching j*+s is at most
 2^(-sum_(i=j*)^(j*+s-1) (i+1)^2), s>=1.
The explicit cost through stage J is sum_(j=0)^J L_j m_j(q_j+1), including seed generation/control separately. The probability of not stopping by j* is at most2^(-(j*+1)^2). A larger desired readiness confidence can be obtained by reading the displayed tail and extending the finite cap; no uncharged stopping oracle is needed.

## Expected cost and why multiple seeds matter
Suppose the received implementation bounds each trial cost by C 2^(p j) times a fixed polynomial in j,1/epsilon,log(1/delta),k,logD,logDout. This applies to query costs, and separately to the uniform finite-design theoretical gate/bit compiler, with its own large constants. The least-integer choice of b ensures b=O(j+log(j+1)+log(1/delta)).

Before j*, the geometric cost sum is polynomial in r. For stages j*+s afterward, multiply the stage cost by the reach bound above. Since sum_(i=j*)^(j*+s-1)(i+1)^2 >=s(s+1)/2, the tail is bounded by a fixed polynomial times sum_s 2^(p s-s(s+1)/2), finite with constants depending only on the fixed implementation exponent p. Therefore expected total search cost and expected subsequent selected-candidate service cost are polynomial in r,k,1/epsilon,log(1/delta),logD,logDout at the received theoretical compiler scope. This is not a uniform worst-case finite runtime on arbitrary N.

Using just ONE fresh seed per stage would provide only a constant-probability success and a geometric tail; that need not dominate 2^(p j) costs. The increasing trial count is load-bearing, not cosmetic. The stronger cubic tail supplied by L_j=(j+1)^2 is more than needed but explicit.

## Scope and dependencies
This removes the supplied rank and supplied useful encoder from the low-rank unknown-noise interface, conditional on sufficient ambient input dimension and memoryless seed-oblivious noise. It preserves all quantum training storage and endpoint-control costs. Complexity is polynomial in k, not in log k: no efficient high-logical-rate architecture or quantum-capacity algorithm follows. No environmental tomography, source inverse, Stinespring oracle or opaque optimizer is introduced.

Dependencies: random_code_learned_decoder_20261029/GOVERNING_DRAFT.md and FINITE_SEED_AND_ENCODER_COST.md (receiving status must be supplied); rank_adaptive_decoder_selection_20261029 (received schedule/statistics); compressed_mixed_encoder_recovery_20261029 and received low-support extension; box_muller_design_compiler_audit_20261029 receipt (uniform theoretical control). Known-recovery SDP is an optional received improvement, not required for these constants. This draft does not confer acceptance on a dependency still under review.
