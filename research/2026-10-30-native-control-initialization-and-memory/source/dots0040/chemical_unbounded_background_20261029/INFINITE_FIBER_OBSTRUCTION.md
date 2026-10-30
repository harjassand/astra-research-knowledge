# A structural obstruction to finite-background continuation

29 October 2026. New exploratory extension; the reviewed finite-phase theorem is unchanged. No general two-population theorem or novelty claim.

Consider the weakly reversible directed rectangle, all rates one:

    0 -> p A -> p A+B -> B -> 0,  p>=1 integer.

Both populations are unbounded. At fixed A=a>=p, the frozen B generator is immigration-death with immigration lambda_a=(a)_p and per-particle death rate1. Its exact stationary law is Poisson(lambda_a). The reactions changing only A do not change this frozen B generator.

## Fixed truncation fails

For every fixed cutoff M, P(Poisson(lambda_a)<=M)->0 as a->infinity. Thus no finite fixed background retains a nonzero fraction of the frozen invariant mass. Enlarging a finite matrix once does not repair this.

## Adjacent physical count fibers are not close

An actual A-changing reaction moves A by p. The Hellinger affinity of the neighboring frozen laws is exactly

    H_a=exp[-(sqrt(lambda_(a+p))-sqrt(lambda_a))^2/2].

As a->infinity,

    log H_a ~ -(p^4/8) a^(p-2).

Hence for p>2 the affinity tends to zero and total variation tends to one. For p=2 the affinity tends to exp(-2), not one. The finite-mode proof's simultaneous fixed-shift ratios 1+O(1/a) are therefore not available in an invariant-law norm. This is not a bad constant in that proof; its representation loses uniformity.

At a fixed B=b, unnormalized fiber weights are lambda_a^b/b!, whose degree in a is p b. The degrees have no finite maximum as b ranges over the infinite background. Normalization introduces exp(-lambda_a); discarding that common factor changes the total mass from one to exp(lambda_a), which defeats an exp(-theta a) envelope when p>1. The finite-tree degree construction cannot be reused without a new summability argument.

## Why this is not a recurrence counterexample

The actual A-death rate is (a)_p B. At large a, a B-birth can trigger rapid A-deaths before B approaches its frozen mean. Thus stationary freezing is dynamically inappropriate precisely in the problematic region. An exact boundary corrector, derived separately, proves recurrence of this whole rectangle family without averaging. The example refutes this extrapolation mechanism, not the chemical recurrence conjecture.

## Primary overlap and scope

Two-species recurrence has already been publicly claimed by Agazzi, Anderson, Cappelletti, Laurence and Mattingly; ConStRAINeD still lists the full manuscript in preparation: https://constrained.polito.it/publications/ . Primary conference announcements date to 2023: https://informs-aps2023.event.univ-lorraine.fr/data/pages/book_of_abstracts.pdf . Therefore this example is a demanding mechanism test, not untouched priority territory.

The available primary paper https://arxiv.org/html/2610.31550v1 explicitly separates bulk estimates from compatible boundary estimates. https://arxiv.org/abs/2310.01949v3 explains stopping-time/Filonov criteria as a way to avoid gluing one-step Lyapunov functions. Those mechanisms are relevant prior art, not established consequences of Astra N33.
