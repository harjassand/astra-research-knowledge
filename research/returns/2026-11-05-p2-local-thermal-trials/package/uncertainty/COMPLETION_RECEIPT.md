# Independent selection construction C: completed receipt

## Completed

The constructive question was whether a forced response can determine exact
maximum preparation uncertainty even when it does not identify the hidden
realization. The answer is yes for the declared collocated contraction-bath
mechanical class. The theorem supplies a conservative completion attaining the
entire uncertainty set, a response-derived Gram kernel, exact conditioned
minimax intervals, and a derivative-free position-box implementation with
finite acquired-response error.

The physical initial-energy norm, known M/Gamma/mu, collocation, retained plant,
and existing response-acquisition certificate are substantive premises. This
is not a general consequence of passivity alone or a free response oracle.

## Files and execution

* `FIRST_PRINCIPLES_DERIVATION.md`: initial constructive derivation.
* `MAXIMAL_PREPARATION_KERNEL_THEOREM.md`: theorem, proofs, finite-error
  continuation, resource ledger, comparison and limits.
* `completion_kernel_checks.py` and its JSON: floating diagnostics of the
  conservative identity and larger preparation uncertainty for the same
  low-order dissipative response.
* `acquired_box_kernel.py` and its JSON: exact rational construction from the
  preserved response table, retaining its actual error and confidence contract.

Reproduction from the workspace root:

    python output/selection_independent_principle/completion_kernel_checks.py
    python output/selection_independent_principle/acquired_box_kernel.py

Both ran successfully. No prior source or accepted result was altered.

## Decisive comparisons

The finite computation is real, but the inherited response error 0.0562185 is
too coarse for this particular robust Gram inflation to improve the elementary
energy radius on width-0.1 boxes. Its bound is 4.8732 versus 1.0, so the
operational decision is to retain the elementary bound. A useful small-radius
application must pay a new, substantially smaller response-error certificate;
it cannot silently reuse an exact response or free derivative.

Classical conservative realization, de Branges--Rovnyak functional models and
Hilbert optimal recovery already supply the strongest abstraction and match
the information access. Accepted Astra N997 likewise explicitly compares
retained exact/uncertain operator histories to equally informed optimal
recovery. No major historical novelty or operational advantage over those
comparators has been established here. The strongest selection conclusion is
a completed structural companion and precision boundary, not a new flagship
capability.

The actual mathematical distinction is preserved: a third-order rational
forced response can have an infinite-rank maximum preparation kernel. This
does not assert infinite finite-accuracy cost; it excludes inferring an exact
small preparation state from forced-response order alone.
