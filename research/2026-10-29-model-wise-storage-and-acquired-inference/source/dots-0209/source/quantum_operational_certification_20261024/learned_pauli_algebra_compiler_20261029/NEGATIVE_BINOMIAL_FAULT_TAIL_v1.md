# Candidate negative-binomial fault tail for the keyed payload comb
2026-10-29. New refinement, independent review pending. Applies to the actual PRIVATE_PAD_PAYLOAD_INSTRUMENT comb, not automatically to unkeyed Bell-resource service.

Let p=1-q be the probe probability. At each actual call the exact keyed instrument permits the following equivalent generative order, conditional on the full latent previous history: first draw the common physical Pauli label v and its memory-instrument branch; then draw the independent private role coin. On a probe the physical label is revealed and span updated; on a service the corresponding logical Pauli acts on the next payload slot. The conditional memory instrument is the same in both roles. This reordered mathematical description is justified by the exact instrument identity, not by performing a virtual Bell measurement on unkeyed service resources.

Call a round an opportunity if v lies outside the span S_t of actual previous probe labels. Its being an opportunity is determined before its current role coin. At each opportunity a probe occurs with probability p and increments binary rank; a service occurs with probability q and may create a logical fault. A service logical fault implies an opportunity, although some opportunities may act harmlessly on the chosen gauge envelope.

By optional skipping of independent coins at selection events determined before their own coin, the role sequence along successive opportunities is iid Bernoulli(p). Selection can depend arbitrarily on all previous roles, labels, memory branches and time; no stationarity or minimum event probability is used. If opportunities cease before m*=dimS* probe successes, extend the selected sequence with fresh artificial coins. Artificial opportunities only increase the number of service opportunities before m* probe successes. There cannot be a real opportunity after m* actual probe innovations, because then S_t=S* and all later labels lie in it. Thus for any fixed service target, finite source-call cap, or entire indefinitely extended process,

  number of actual faulty service blocks <=_st NB(m*,p),

where NB counts failures before m* successes. The same domination holds with the known bound m=2g>=m*. For m=0 there are no faults and the following formula is replaced by zero.

For integer t>=0,

  Pr[faulty service blocks>t]
    <= Pr[Binomial(m+t,p)<=m-1]
     = sum_{j=0}^{m-1} binom(m+t,j)p^j(1-p)^(m+t-j).       (NB)

This is a distribution-free tail under the common-algebra/private-role instrument promise. It is stronger than the first-moment bound mq/[p(t+1)]. In particular, if

  p(m+t)>=max(2m,8 ln(1/epsilon)),

then the right side is at mostepsilon by the lower-tail binomial Chernoff bound. This gives t=O((m+log(1/epsilon))/p), without any1/epsilon factor in the outer code's correctable-error budget. Constants are conservative; exact finite binomial tails can be used.

An outer code correcting t service-block errors, or t groups of consecutive service blocks (a bad group requires a bad service), therefore has direct reduced half-diamond error at most(NB), plus a separately charged source-call/probe-budget cap failure. The outer code still requires lengthB>4t for the explicit received GRS construction. With m=Theta(n), this does not provide a free finite-size throughput claim; storage/control/keys and probe joint access remain paid.

## Proof obligations and falsification checks
The selected-coin argument requires that current opportunity selection be independent of its current role coin conditional on full past, which follows here from the exact padded joint-memory instrument and no key/role leakage. It would fail if the source knew the current role and injected new errors only on services. It also fails if one substitutes an artificial classical fault label for a coherent unkeyed service without proving an instrument identity. The theorem is not an iid noise claim: only the trusted role coins are iid. Stopping afterJ services or at a finite cap truncates the opportunity sequence and cannot add faults. Hidden Kraus/Pauli branches can be conditioned in the proof because their weights are input-independent for the full fresh payload initially independent of source memory.
