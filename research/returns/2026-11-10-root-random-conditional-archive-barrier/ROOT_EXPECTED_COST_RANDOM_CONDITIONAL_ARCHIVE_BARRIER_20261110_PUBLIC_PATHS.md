ROOT: EXPECTED SOURCE-COST OBSTRUCTION FOR RANDOM-SIZE CONDITIONALLY EXACT ARCHIVES
10 November 2026 Brisbane. A restricted-model expected-cost theorem composed with P1 614571. It is NOT a lower bound for all algorithms in the full batch problem.

MODEL OF THIS LEMMA.
There are m actual original iid P rows. Choose an a.s. finite integer K>=0 independently of the ENTIRE P sample stream, including those original rows. K may use independent bits or Q-only information. Draw and PAY for K fresh P labels, forming n=m+K iid P records. Other Q calls and computation are unrestricted.
Assume the algorithm is universally exact CONDITIONAL ON K: for every fixed P,Q and every k with positive probability, L(Y|K=k)=Q^m. This extra condition holds for independently randomized fixed-size exact archive matchers. It is not part of the original full problem.
Costs here count the actual K newly drawn P labels; unused random budgets cannot be charged as if they were actual calls. Conditioning on K does not truncate an arbitrary adaptive P stopping time.

THEOREM.
At P=Q=Unif[d], write C=E K. Every such algorithm has
 E changed_fraction >= (1-1/d)/(2 sqrt(1+3(d-1)(m+C)/d^2)).
Thus a TV-plus-eta guarantee with 0<eta<=1/8 entails
 m+C >= (d-1)/(12 eta^2)-d^2/[3(d-1)] >= (d-1)/(16 eta^2).
This remains true for unbounded heavy-tailed independent archive sizes when C is finite. No deterministic source cap, Q cap or exponential-moment assumption is used.

PROOF.
Fix k and Q. The n=m+k P records are iid, even conditional on K=k, and their ordering conditional on their complete histogram A is uniform and independent of the numerical P. Extra Q information, bits and algorithmic decisions have a P-independent conditional kernel after this conditioning. Universal conditional exactness gives the multinomial Bernstein identity
 sum_{|a|=n} Multinomial(n,a)*p^a*K_{a,k}(y)=Q^m(y).
Uniqueness of homogeneous multinomial Bernstein coefficients forces K_{a,k}(y)=Q^m(y). Hence Y conditional on A,K has lawQ^m, whereas each designated original X_j conditional on A,K has marginal A/n. The coupling inequality implies
 E changed_fraction |K=k >= E_{A~Mult(n,P)} TV(A/n,Q).
At both uniform this is phi_(d,n)=d/(2n) E|Z-n/d|, Z~Bin(n,1/d).

Put sigma^2=n p(1-p), p=1/d. The exact centered fourth moment satisfies E(Z-np)^4<=sigma^2+3sigma^4. Holder interpolation yields
 E|Z-np| >= sigma^3/sqrt(E(Z-np)^4) >= sigma^2/sqrt(1+3sigma^2).
Therefore
 phi_(d,n)>=(1-1/d)/(2 sqrt(1+3n(d-1)/d^2)).
The right side is convex as a function of n>=0. Jensen over K proves the displayed expected-cost bound.
Rearrangement gives (d-1)/(12eta^2)-d^2/[3(d-1)]. Since d^2/(d-1)^2<=4 and eta<=1/8, the subtracted term is at most one quarter of the first term. The final bound follows. Infinite C already has infinite source cost.

CONSEQUENCE AND LIMITS.
Randomizing the length of an independently acquired archive while retaining exact Q^m at EACH length does not avoid the empirical-estimation source cost, even if its length has rare long tails. This excludes a broad purported expected-cost shortcut for m well below d/eta^2.
It does not exclude general adaptive mixed P/Q stopping, kernels whose exactness arises only AFTER mixing over stopping events, or jointly generated outputs. P1's accepted one-row expected O(d/eta) coupler remains valid and lies outside the asserted independent-size/conditional-exactness representation. No new all-regime expected lower bound, sharp minimax formula or critical-batch positive algorithm follows.
The proof uses the entire exact product law; correct row marginals alone are not an equivalent contract. Old m acquisition/storage and every fresh archive row must still be charged in applications.

RELATED COMPLETE CHECK.
P1's adaptive two-size counterexample was independently derived by ROOT with the original uniform histogram ties. On the X=1,Z1=0 branch, Pr(Y1=1)=q(1-p/2); on X=0,Z1=1 it is q+(1-q)(1-p)/2; the X=Z1=1 branch contributes pq. Summing gives q+q(1-q)(p-1/2). At p=7/10,q=3/10 this is171/500, not3/10. This analytic check is not a new scientific score, implementation test suite or proof of failure of every adaptive archive.
Original source: P1_XI_614571_BATCH_REUSE_RETURN.md13793UTF8/SHA56165639184386e083602fa1c150a67d3bf3c5544e1223e9cd8ae483c0b0a7ef. Its zero-P optimality and deterministic-P-cap Bernstein proof are accepted at their stated scopes. The old expected-stopping lower bound and exact cost-m threshold remain unchanged.
All known/unknown source/access/transfer/resource/Sol/Dots holds persist. No source recovery, extra worker, model, API, index probe or experiment was used.
