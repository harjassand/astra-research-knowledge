# Coordinatewise deletion words: a representation of the whole class

This is an author-derived use of monotone reachability and Dickson's lemma. Its historical novelty is not established. It is a geometric construction, not yet the physical-clock recurrence theorem.

For a finite raw reaction list define D to be the set of count states x from which an enabled finite word reaches y<=x, y!=x. The inequality is coordinatewise. D is upward closed: the same word translated by z>=0 takes x+z to y+z. Therefore D has a finite minimal basis B. For each b in B choose one actual deletion word w_b, ending at b-delta_b with delta_b>=0 nonzero. There are finitely many words, so their maximum length L and maximum prefix count overshoot J are finite and depend only on the raw list.

Let C be ANY actual communicating class. Then C\D is finite. Otherwise Dickson's lemma gives two distinct states x<=y in that infinite set. Communication supplies an enabled word y->x, so y is in D, a contradiction. This step uses actual communication, not an asserted stationary law.

Thus every state of C outside the finite set H_C=C\D dominates a basis vector b and has an acquired word

    x -> x-delta_b,

whose terminal counts ALL decrease or stay fixed. Iterating such words reduces the integer total count at least once per word and reaches H_C in at most |x|_1 words. The total length is at most L|x|_1. Every prefix stays below |x|_1+J because word-boundary counts decrease. This is a linear-length descent path with a constant count overshoot, not a serpentine path of length |x|^d.

For a weakly reversible network the word stays in the same closed communication class by translated complex return paths. The statement does not assume a conserved total or freeze any low coordinate. A finite conserved class simply lies entirely in its finite head if no deletion is possible. A conserved enzyme pool forces deletion words to return its actual phase, so several evolving inventories and bounded phase coordinates are retained in the representation.

This gives a genuine alternative to transporting one Green profile between neighboring inventories: the global geometry is encoded by finitely many monotone deletion templates and a classwise finite terminal set. It does NOT mean the uncontrolled Markov process follows those templates. Their physical success probabilities and competing exits still have to be controlled.

## Acquisition boundary

Existence of the finite basis follows from a proved well-quasi-order lemma, which is legitimate for an existence theorem. A numerical raw-list compiler must find its basis, witnesses and a completeness certificate. Enumeration of a few successful deletion words is not such a certificate. For a concrete hard family one can instead exhibit words whose upward cones cover the whole orthant outside an explicit finite head; that is an actual complete certificate for that family. The accompanying code pursues this concrete acquisition before any general numerical-compiler claim.

The equally informed ordinary machinery is Petri-net reachability/coverability. The property x->y<x is a reachability property with a linked initial/final comparison, not merely the ordinary upward coverability target used in `coverability_clock.py`. A complete general acquisition cannot silently replace it by that easier algorithm.
