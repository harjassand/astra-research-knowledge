# Rank-adaptive selection of a fresh-block quantum decoder
2026-10-29. Author theorem draft; independent receiving review required. The statistical method is conventional holdout validation. Its purpose is to remove a supplied-rank assumption without selecting on the real payload or reconstructing the environment.

## Candidate interface
Fix a stationary memoryless CPTP source N:Ck->CD and trusted preparation/readout/control. Candidate j has rank parameter R_j=2^j. It is a fully specified finite physical decoder algorithm: it makes at most q_j forward training calls, then consumes one independently encoded payload, and outputs a k-dimensional state. All internal outcomes, random choices and abort completions are INCLUDED in a CPTP logical channel M_j. The compressed-encoding construction gives candidates with the following completeness property: for every exactly correctable mixed encoding of junk rank r, whenever R_j>=r, its chosen accuracy/control budget ensures 1-F_e(M_j)<=alpha/4. Output padding is allowed if kR_j>D; it is known padding, not extra source access. No such performance promise is needed for soundness.

Every validation run and every later service run starts the ENTIRE candidate from fresh source calls and fresh controller states. Learned gauge-dependent parameters/programs from a sacrificial validation run are not reused for service. In particular the common-Haar gauge introduced by joint Schur compression is regenerated inside each complete block. The encoded real payload is not touched during rank search.

## Finite acceptance rule
Given desired0<epsilon<1 and0<delta<1, set alpha=epsilon²/k² and delta_j=delta*2^(-j-1). Choose integer b_j>=log2(1/delta_j), by rational integer comparisons, and m_j=ceil(32 b_j/alpha). Perform m_j independent sacrificial runs of candidate j, using a maximally entangled logical test input and its retained trusted test reference: encode its payload half by N, run the candidate decoder, then measure the known maximally entangled projector with the retained test reference. Record a failure bit X in{0,1}. Its mean is ell_j=1-F_e(M_j).

Accept j exactly when the number of failures divided by m_j is at most3alpha/4. Otherwise increment j. No optimization oracle or rank estimator is used. The validation source-call cost is at most m_j(q_j+1) at stage j, including sacrificial encoded payload calls. Future service pays its own q_j fresh training calls; it does not inherit a free program.

## Soundness for any stationary memoryless CPTP source
If ell_j>alpha, the multiplicative Bernoulli lower-tail bound gives
 Pr[accept j] <= exp(-m_j alpha/32) <=2^(-b_j)<=delta_j.
Fresh source blocks make the same bound hold conditional on reaching stage j. Union bound gives probability at most sum_j delta_j=delta of ever accepting a candidate whose true averaged logical infidelity exceeds alpha. On the complementary event, any accepted j has
 (1/2)||M_j-identity||diamond <= k sqrt(1-F_e(M_j)) <=epsilon.
This is a guarantee on the fresh-service AVERAGED channel, including arbitrary payload/reference inputs, not a claim that every internal realization is close to identity. Conditional on the offline validation transcript, service still implements M_j because its entire training block is fresh and N is stationary memoryless. This independence is why validation can certify a later channel here; it is not postselection on the service outcome.

The guarantee is model-free over such CPTP sources: a pass does not prove a rank bound or exact correctability. If N is not recoverable, the search may never accept. Trusted Bell-test error must be explicitly bounded or absorbed in the thresholds; arbitrary source memory/drift invalidates the IID transfer and is not covered.

## Completeness and stopping cost under the mixed-encoding promise
Let j*=ceil(log2 r). For all j>=j*, completeness gives ell_j<=alpha/4. With Chernoff parameter ln3, the probability of rejecting at threshold3alpha/4 is at most
 exp[m_j alpha(1/2-(3/4)ln3)] <=exp(-m_j alpha/4)<=delta_j^8,
using ln3>1. Thus the probability of not stopping by j* is at most delta_(j*)^8 (unless it stopped earlier, which only helps availability). The probability of continuing forever is zero: conditional rejection probabilities at all later good stages are bounded by delta_j^8.

If q_j is bounded by C 2^(p j) times a fixed polynomial in j and1/epsilon, the expected total query cost is finite and polynomial in r and1/epsilon, with constants depending on that fixed exponent p. Indeed the probability of reaching j*+s is at most product_(l=0)^(s-1) delta_(j*+l)^8, which decreases quadratically exponentially in s and dominates any2^(p s) query growth. The high-probability budget through j* is the explicit finite sum sum_(j=0)^j* m_j(q_j+1), even though the controller is not told r. This is not a uniform finite worst-case stopping bound over arbitrary unpromised N.

The candidate theorem's query complexity and control-runtime scope must remain separate. Fixed-rank Schur/GT implementations need not be jointly polynomial in rank; this selection proof does not upgrade their gate complexity. A common-design compiler may strengthen that separately.


## Finite checks and dependencies
`check_selection.py/json` verifies18 acceptance/miss bounds by exact binomial summation with rational arithmetic, and9 expected-cost tail fixtures. Integer comparisons choose b_j and the rational failure threshold, with no transcendental sampling oracle. The candidate completeness dependency is `compressed_mixed_encoder_recovery_20261029`; its receiving status and gate-runtime qualifications must be carried separately. The model-free soundness theorem does not require its correctness, but completeness does. No claim of universal positive yield for arbitrary channels or correlated/drifting sources is made.
