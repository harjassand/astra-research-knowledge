# Independent root product-forcing review

30 October 2026. Frozen root note SHA256 bb211c7b7d0b8b8ffac258e0b62386e74ee171468fd48c13edbd4111172d4816. Three-source manifest `PRODUCT_SOURCE_SHA256.txt`; copies in `product_sources/`.

**Verdict: accept PF1-PF4 as a persistent-label local theorem with the binding progress-allocation precision below.** This restores the n T^L lower-tail power without independence of actual labels. No stopped Green, seed repair or global theorem is included in this receipt.

## Essential generator allocation

Interpret 'actual positive rate splitting' as a decomposition of the generator into per-label progress subgenerators, safe events and bounded-participation adverse events. No physical event intensity may be counted more than once across progress subgenerators. Each event allocated to label i reduces its positive rank by at least one; all collateral changes must be safe. Rank-zero allocated progress events can be taken null or safe. This is enough even when destinations depend on retained state/history.

Without that allocation the theorem is false: one common clock of rate q reducing EVERY label simultaneously would look like rate q progress to each label if double-counted. Starting all labels at rank L, their successes are identical and have probability P(Pois(qT)>=L), not a population-concentrated count. This is excluded by a genuine decomposition. Also a progress event with adverse collateral changes cannot be credited for free; its adverse action must satisfy a valid decomposition/participation accounting.

## Exact algebra

The backward time derivative of each factor is a phi'_r. For a one-step allocated progress event its generator factor is -a q(phi_(r-1)-phi_r), divided by f_r in the product. These cancel and leave -beta F sum_i a phi_i/f_i. At rank zero, phi'_0=-beta phi_0 and no progress is needed. Larger designated drops and safe collateral changes only decrease the after-product, so the same upper bound holds.

For an adverse set A, each new factor is at most one. With z_i=a phi_i/f_i>=0, the relative increase is bounded by product(1+z_i)-1. Telescoping and 1/f_i<=1/(1-a) give at most (1-a)^(-(k-1)) sum z_i. Summing actual intensities uses precisely the per-label participation bound b, which is canceled by beta. This is a generator inequality for a product observable, not a factorization of path laws.

The bounded positive test and the stated Dynkin/localization assumption yield E F(T)<=F(0). Since phi_r(T)>=phi_L(T), PF3 follows for every initial rank vector. At terminal time F(T)=(1-a)^A. With a=1/2, Markov at A<=np/4 gives exponent -(1/2-log(2)/4)np, stronger than -np/4. The stated Poisson mass lower bound supplies c T^L on 0<T<=1. The dependence on fixed k is explicit; a collective event touching all n labels does not retain population-independent constants when k=n.

## Regression audit

The supplied script was read and rerun from the frozen copy; its output is byte-identical to the supplied JSON. Five hundred pointwise randomized tests verify the derivative/progress identity and worst-output adverse bound. The finite three-label CTMC includes an actual correlated reset of all three labels at fixed k=3 and checks the product mgf at four times. Maximum numerical positive drift residual is approximately 9.6e-16. These are regression/falsification aids, not the proof of uniformity; the symbolic inequalities above establish it.

The ghost paragraph remains only a deterministic containment device. Extinction, physical holding time, replenishment, births/deletions, terminal rewards and full Green/cycle arguments require their own hypotheses and proofs. Separate author completions are not silently incorporated into this root-lemma verdict.
