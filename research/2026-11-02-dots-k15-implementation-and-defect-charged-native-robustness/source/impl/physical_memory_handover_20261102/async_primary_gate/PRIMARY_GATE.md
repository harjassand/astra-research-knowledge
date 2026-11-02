# Asynchronous classical synchronizer: primary gate

2 November 2026. No outreach or paywall bypass.

## Verified source interface (compact)

Cook–Gács–Winfree, *Self-stabilizing synchronization in 3 dimensions* (20 October 2008 draft), https://www.cs.bu.edu/faculty/gacs/papers/3Dasync.pdf .

Definitions 2.11–2.12 permit lattice/torus products and specify independent unit-rate Poisson update clocks. Proposition 2.7 gives constants gamma,delta>0 such that a blame path of length <=m and elapsed time >gamma*m has probability <exp(-delta*m).

Theorem 4.1 concerns a fault-free repair cylinder following initial localized damage. It assumes `Slack(L,G)`: defects lie in a cube of side L, and surrounding lifted clock differences satisfy a slope bound. Repair takes c1*L+c2*G with failure <=exp(-d*L). Introduction and Section 4.3 explicitly leave a stochastic bound on Slack failure unresolved. This is not a continuing-fault asynchronous threshold or a uniform service-time theorem.

Wang, FOCS 1991, DOI https://doi.org/10.1109/SFCS.1991.185379 , has a primary abstract asserting reliable homogeneous asynchronous computation. Full-text timing/fault hypotheses were not retrieved. The thesis is linked by arXiv:2601.20818v3 to ProQuest document 304019330.

## Access status

- Cook–Gács–Winfree author-hosted 36-page PDF read successfully, especially pp. 1–2, 10–11, 18–21.
- IEEE Wang page produced a JavaScript bot-verification screen; DBLP produced an access-denied bot screen. No challenge bypass was attempted.
- The thesis's existing primary-reference link returned HTTP 403 at ProQuest. No retry without new evidence; no authentication or alternate protected endpoint attempted.
- Ordinary public searches found citations and abstracts, not an authorized accessible Wang theorem text. The Wang hypotheses therefore remain **unverified**, not disproved.

## Own deduction: exact service lemma that a candidate must actually discharge

A finite local state space alone proves no progress. For example, adding one `stalled` state that is absorbing under all intended update channels leaves a finite-state process with infinite service delay after a single fault. Likewise, a finite spatial neighborhood is not a closed finite-state chain when an uncontrolled boundary can keep its updates disabled.

Here is a sufficient stronger condition. Fix a bounded local contact patch B with at most b update types, each having rate in [lambda_min,lambda_max], and additional fault-attempt intensity at most nu per site. Suppose there are constants m and tau, independent of total system size, such that from **every** classical patch state and every allowed exterior history, one can choose at most m intended contact updates whose ordered occurrence completes the next required operation. The word must remain executable despite arbitrary events outside B; irrelevant events within B are excluded during this witness interval. All intermediate quantum operations must additionally obey the intended causal contract—progress alone does not imply correctness.

Partition a time interval tau into m equal slots. A particular useful update can be required exactly once in its slot, with no other patch events and no patch faults anywhere in the interval. Independent Poisson attempts then give a conditional success probability at least

    v >= exp[-(b*lambda_max + |B|*nu)*tau]
         * min(1, lambda_min*tau/m)^m > 0.

When a useful word has fewer than m symbols, pad using silent slots; constants can be reduced uniformly over the finitely many possibilities. Choosing a word based on the patch state at the interval's beginning is legitimate because the lower bound holds uniformly over that state and all past history.

The conditional lower bound yields

    Pr[T_service > k*tau | arbitrary past] <= (1-v)^k,
    E[T_service | arbitrary past] <= tau/v.

This is a physical-time bound, with all repair and waiting included. It accommodates continued stochastic contact faults because the witness event pays for a fault-free interval; it does not assume faults stop forever. The finite-rate noise constants affect v but do not grow with system volume.

For local fault-set domination, further evidence is needed: witness patches/events for different requested operations must have bounded overlap or an equivalent causal factorization. Marginal exponential tails alone do not imply a product bound for many operations. Coherent/non-Markovian perturbations require a superoperator fault-path estimate, not a replacement by classical probabilities.

## Quantum lift still required

The classical scheme may copy current and previous classical controls; it cannot copy unknown quantum data. A valid use in quantum brickwork must implement each quantum gate exactly once after all causal predecessors, use disjoint or atomically interlocked gate supports, and identify a recoverable quantum state at asynchronous cuts. A repair that resets a clock cannot silently replay or skip an unknown quantum gate. The parent should test this causal contract separately from the service lemma above.

**Decision:** no inspected primary theorem presently closes the required robust asynchronous quantum-contact interface. The author-hosted draft provides a concrete local repair ingredient and explicitly exposes its extra Slack hypothesis; Wang remains an access-limited unverified candidate.
