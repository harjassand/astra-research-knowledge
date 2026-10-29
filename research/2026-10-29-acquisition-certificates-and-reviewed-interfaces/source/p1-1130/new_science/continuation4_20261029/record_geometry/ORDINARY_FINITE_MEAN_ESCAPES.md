# Strong ordinary alternatives and their actual additional access

29 October 2026. Astra P1, existing record-geometry complementary role.

The four-state obstruction rules out one universal visible-only exact
finite-mean procedure at the declared unknown-kernel interface. It does not
rule out the following concrete procedures. These alternatives must remain
visible when assessing a preparation construction.

## 1. Independent baseline rejection

If an actual procedure supplies a new specimen state with law mu conditional
on the entire preceding rejected history, accept the current specimen with
probability W(Y)/M, M=max W. One trial has accepted measure W mu/M. Thus
the successful state has exact law nu=W mu/mu(W), with expected trial count
M/mu(W). Preparation, sensing, randomization and discarded trials retain
their actual costs.

A single baseline specimen also gives this exact law conditional on the
first acceptance, with success probability mu(W)/M. That is a heralded
success law. Its rejection branch has not supplied unconditional preparation.
Repeated calls of an arbitrary unknown stationary kernel do not produce the
conditional baseline refresh needed to repeat this argument.

## 2. Exact label closure makes first-label feedback sufficient

Let P be stationary for mu, with finite visible labels Y. Suppose the
time-reversed kernel P* is strongly lumpable on those labels:

    P*1_{Y=b}(x)=q_(Y(x),b).                         (1)

For a reversible source this is simply exact invariance of the visible
indicator span under P. It is a structural promise; finite data alone do
not prove an unrestricted exact identity.

**Receiving lemma.** From X_0~mu, the endpoint law of every almost surely
finite visible-only stopping time has density relative to mu depending
only on its endpoint label.

To prove it, fix a finite visible word a_0,...,a_t and an endpoint x with
Y(x)=a_t. Under the stationary law, the conditional past visible-word
probability is the product of reverse label transitions from (1), independent
of hidden coordinates inside the endpoint label. Multiply by the controller's
conditional stopping probability for that word and sum over words and t.
Nonnegative summation yields an endpoint density constant on each label.

Draw D independently with probability

    q_D=W(D)mu(Y=D)/mu(W),

then stop when the current visible label first equals D. Conditional on D,
the receiving lemma gives mu(.|Y=D); combining labels gives the full nu.
If the finite visible chain is irreducible, the stopping time has finite
mean. No microscopic copying or knowledge of its transition probabilities
is required to execute the rule. A numerical cost certificate does require
an actual hitting-time bound.

The four-state family violates (1) as soon as a swap component couples the
bits. Its exactly computed first-label failure demonstrates why this premise
cannot be omitted. For connected injective smoothing operations with sharp
labels, the preserved finite-closure obstruction remains relevant.

## 3. Entirely frozen disorder with a common visible baseline

Another useful sufficient class has full state (H,Y), with H frozen and
with a finite visible chain P_H in each sector. Suppose the baseline is
mu(dh,dy)=xi(dh)pi(dy), with the same known visible pi in every sector.
There is no additional evolving microscopic coordinate within (H,Y).

Draw D with q(d)=W(d)pi(d)/pi(W), independently of H, and wait for Y=D.
When the hitting time is finite almost surely in every relevant sector,
the final state is exactly (H,D): H retains its original xi distribution
and D was drawn independently. The full target xi times q is therefore
prepared exactly, even though the hidden variable never mixes and the
visible rates can depend arbitrarily on H.

The mean cost is the actual xi-average of the sector hitting times. It can
be finite or infinite; finite mean in every individual sector does not
imply a finite prior-averaged mean. For an unknown symmetric binary flip
probability p(H), this procedure has mean

    E tau = (1/2) E_xi[1/p(H)]

when zero-call stopping is allowed, because the initial fair visible label
disagrees with the independent target half of the time. This is an honest
finite-mean escape when the reciprocal-rate expectation is warranted.

The common visible baseline is essential. The preceding continuation's
sector-weight counterexample shows that aggregate baseline masses alone
do not provide it.

## 4. Full finite microscopic state recognition

Lovasz and Winkler's unknown finite-chain stationary stopping algorithm
observes which microscopic state has been reached, collects designated
exits from every state, and tests an auxiliary directed assignment for a
spanning tree. It stops at the actual current state with the stationary
law and has finite expected cost for every finite irreducible native chain.
The transition matrix need not be known. This is a strong ordinary incumbent,
not a hypothetical matrix-based substitute.

For a finite, irreducible physical kernel K whose stationary law is the
desired nu, the same algorithm applies to actual K calls. In the explicit
four-state family, the binary compiler gives a strictly positive K, so
irreducibility and finite mean hold. Full microscopic state recognition
would therefore turn the same specimen into an exact finite-mean sampler.
Only observing Y does not reveal whether two visits with that label were
the same microscopic state, and does not supply this algorithm's inputs.

This comparison explains the boundary sharply: hidden observation access,
conditional regeneration, or exact reverse label closure can change the
answer. Mere native stationarity and known visible masses cannot.
