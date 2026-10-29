# A stronger equally informed exact ordinary route

The first small-model Gaussian rejection baseline beat CFTP. Before promoting a
practical advance, grant it the SAME harmonic projection that the coupling proof
uses. This produces a much stronger positive independent proposal, rather than
another CFTP parameter sweep.

Let P=B^T L_0^(-1)B and tau_e=P_ee. For fixed q and r, sample INDEPENDENT conductance
bits from the exactly known tilted priors

    ptilde_e/(1-ptilde_e) = [p_e/(1-p_e)] q^(-r tau_e/2).

Given X, put D_X=det(L_X)/det(L_0). Accept the proposal with probability

    a_X = q^((r/2) sum tau_e X_e) D_X^(-r/2).             (L1)

It lies in (0,1] by the same chord inequality used in REJECTION_BOUND. Multiplying
the product proposal density by (L1) cancels the tilt exactly, leaving a constant
times the desired conductance weight. On acceptance draw its conditional Gaussian
field with the SAME certified quantization engine. This is an ordinary positive
rejection sampler for the IDENTICAL normalized output, with no target-density,
normalizing-constant or mixing oracle. Rational determinants and computable scalar
powers are enough. No frame fitting or use of sampled CFTP outputs chooses the tilt.

The guarantee improves the Gaussian-proposal exponential rate. For lambda in[0,1],

    0 <= log(1+(q-1)lambda)-lambda logq <= d_q,
    d_q = log[(q-1)/logq]-1+logq/(q-1),                  (L2)

with continuous value d_1=0. There are k=n-1 nonzero eigenvalues, hence

    a_X >= exp[-r k d_q/2]  for EVERY proposal.           (L3)

At q=2, d_q is about .05966. This can make the exact ordinary route useful well
beyond the small example where untitled Gaussian rejection already wins. It still
has an exponential bound for fixed contrast and unbounded size; no all-size
polynomial guarantee follows from (L3). The CFTP theorem supplies that missing
worst-case guarantee. A fixed-attempt capped rejection followed by an independent
exact CFTP fallback remains exact, since every accepted proposal has the target law
and the independent fallback has the same law. This hybrid needs no estimate of
acceptance probability. Its actual total cost must include both algorithms.

These are standard determinant chords, leverage preconditioning and rejection
sampling ingredients. Historical priority of their combination here is UNKNOWN;
they must not be presented as an invented general sampling principle. This is the
stronger ordinary comparator that was missing from the initial performance story.
The additional comparator protocol is declared separately before execution and
uses ONLY already executed source cases/output targets, with no CFTP rerun.
