# Sparse gamma clock: current derivation, 12 October 2026

Status: internally reconstructed probability identity and expected-cost argument.
The gamma-mixture identity is classical (Moschopoulos 1985 is the closest source
currently being inspected). Historical novelty of the random-access sparse
sampler and of its CRN application is UNKNOWN. No physical experiment, external
proof review, or finite-bit continuous-law implementation certificate exists.

## Exact interface

Input: integer k >= 1; an evaluable rate array lambda_i, i=0,...,k-1;
certified constants 0 < a <= lambda_i <= b. A query returns a chosen rate;
uniform random indexing is available. Rates, bounds, and index access are supplied
or their acquisition cost must be added. Output: a sample of

    H = sum_i X_i,     X_i independent Exp(rate=lambda_i).

The theorem uses an ideal random-real model with exact Gamma, Poisson, Uniform,
and geometric variates. Expected primitive count is not an every-execution cap.
A floating-point program is only a diagnostic implementation.

## Positive representation

Put q_i = 1-lambda_i/b and q_* = 1-a/b. For each i let
G_i be geometric on {0,1,...} with

    Pr(G_i=j) = (lambda_i/b) q_i^j.

If N=sum_i G_i, then Gamma(shape=k+N, rate=b) has the law of H.
Indeed, with z=b/(b+s), its Laplace transform is

    z^k product_i [(lambda_i/b)/(1-q_i z)]
      = product_i lambda_i/(lambda_i+s).

The log probability generating function of N is

    log E[z^N] = sum_i sum_{r>=1} (q_i^r/r)(z^r-1).

Therefore N is the total size of a Poisson point process of marks (i,r)
with intensities q_i^r/r. All intensities are nonnegative. No cancellation,
normalizing-product evaluation, or density evaluation is used in the sampler.

## Sparse marked-Poisson sampler

If a=b, return Gamma(k,b). Otherwise:

1. Set Lambda = k*(b/a-1).
2. Draw L ~ Pois(Lambda).
3. Initialize N=0. For each of the L candidate marks:
   - Draw I uniformly from {0,...,k-1}.
   - Draw R geometric on {1,2,...}, success probability a/b.
   - Query lambda_I.
   - Accept the mark with probability
     ((b-lambda_I)/(b-a))^R / R.
   - On acceptance, add R to N.
4. Return Gamma(k+N,b).

The candidate intensity at (i,r) is

    Lambda*(1/k)*(a/b)*q_*^(r-1).

Multiplication by the stated acceptance probability gives exactly q_i^r/r.
Poisson thinning proves the mark law, and the Laplace identity proves the output
law. In particular, the sampler queries at most L rates, with E[L]=Lambda.
If each exact rate query costs C_eval, expected query work is Lambda*C_eval.
Integer powers can be evaluated by repeated squaring; using R Bernoulli factors
instead charges E[L]*E[R] = Lambda*b/a factors. For bounded b/a this is the same
order. Exact arithmetic/variates must be charged separately from this query count.

The logarithmic-series alternative uses L~Pois(k*[-log(1-q_*)]),
R with mass q_*^r/(r*[-log(1-q_*)]), and acceptance (q_i/q_*)^R.
It has a smaller mean candidate count; the geometric version above avoids that
additional primitive and is enough for the CRN bound.

## Structured CRN clock

For fixed reaction order o and generativity g >= 0, consider

    lambda_i = c*binom(n+i*g,o),    i=0,...,k-1, c>0.

Assume n>=o. Rates are monotone, so a=lambda_0 and b=lambda_(k-1) are
certified by two evaluations. A chosen rate costs O(o) arithmetic operations;
rates have O(o log(n+kg)) bits when the common multiplier is rational of bounded
description. There is no enumeration of k rates.

For n>=2o and 1<=k<=n/o,

    b/a <= (1+(k-1)g/(n-o+1))^o,

and, by the mean value theorem,

    Lambda <= 2*o*g*(1+2g/o)^(o-1)*k*(k-1)/n.

Thus k=O(sqrt(n)) gives O(1) expected candidate marks for fixed o,g. The case
g=0 is exactly Gamma(k,a). The common physical rate multiplier c changes only
the output time scale.

For the collision-free batch length K used by uniformly reactive CRN schedulers,

    Pr(K>=k) = product_(j=0)^(k-1)
                binom(n-o*j,o)/binom(n+g*j,o)
             <= exp(-o^2*k*(k-1)/(2n)).

Hence E[K^2]=O(n) and the sparse clock also has O(1) unconditional expected mark
count when K is sampled independently of the waiting-time randomness. A batch
length selected using the waiting times does not satisfy this independence.
Collision timing, the exact stopping-time endpoint, and the transformed scheduler's
common rate multiplier require an explicit integration proof; that proof is a
separate gate, currently assigned by root to an independent reviewer.

## Primary target and exact source locations

Joshua Petrack and David Doty, *Exactly simulating stochastic chemical reaction
networks in sub-constant time per reaction*, arXiv:2508.04079v2, 12 February 2026:

- https://arxiv.org/html/2508.04079v2#S5.Thmtheorem5.1 : Theorem 5.1 and its
  two-term continuous-time bound. HTML lines 533-548 in the tool view.
- Section 5.1, especially equation (2) and the paragraph after coefficient
  construction: hypoexponential density evaluation and adaptive rejection
  sampling. HTML lines 549-577.
- Section 5.2: overshoot and conditional rejection sampling. Lines 578-584.
- Algorithm 6 and Lemmas 5.2-5.3: full continuous-time integration and its
  amortized cost. Lines 585-636.
- Section 5.4: moment-matched gamma approximation in the implementation;
  lines 637-672. This is an approximation, whereas the shape mixture above
  reproduces the full ideal law.
- Section 7: exact timestamp sampling named as an efficiency question;
  lines 983-989.

Read-depth receipt: abstract; Sections 1.1-1.3, 2.1-2.4, 4.4 including its
coupling proof and cost, 5.1-5.4 including the clock calculations, 6.3.1-6.3.2,
and 7 were inspected via the primary arXiv HTML. Source evidence is source-
reported, not an independent validation of every theorem in that paper.

## Initial representation and pivot

The initial proposed operation was to sum entire connected interaction components
instead of stopping at the first repeated molecule. For a fixed batch m, schedules
whose simple interaction graph consists only of isolated vertices, edges, and
two-edge paths have counts z (paths), y=m-2z (edges), x=n-2m+z (isolates), with
unnormalized weight proportional to

    1/[x! y! z! 2^(m-z)].

Its adjacent ratio is 2*y*(y-1)/[(x+1)(z+1)], giving log concavity and a potentially
fast conditional sampler. That conditional law is not the whole scheduler law:
the exceptional component probability and conditional exceptional branch are
unresolved. Simply rejecting full schedules until an exceptional branch is found
can erase the proposed saving. This was a useful failure, not a completed primitive.
The change to a positive gamma-shape representation attacks the distinct exact
clock obstruction and closes its latent dimension through sparse Poisson marks.

## Counterexamples and limits to retain

- If all lambda_i=a and b=2a, the chosen envelope is unnecessarily loose and
  Lambda=k; the exact target is Gamma(k,a). Tight supplied/certified bounds matter.
- If one unknown rate among k is changed from a to 2a, a sampler claiming exact
  access-independent operation cannot simply ignore every rate query. Aggregate
  mean/variance matching is not a full-law argument.
- A gamma matching the first two moments is generally not the sum law: for two
  unequal rates a,b its third cumulant is 2(a^-3+b^-3); a moment-matched gamma has
  third cumulant 2*(a^-2+b^-2)^2/(a^-1+b^-1), unequal unless a=b.
- The sampler does not acquire chemical rate constants, justify mass-action
  kinetics, remove passive-reaction slowdown, or solve arbitrary network stiffness.
- No deterministic cap, exact floating output law, total-variation claim for
  rounded real outputs, global reaction simulation bound, or historical priority
  follows solely from the expected mark bound.
