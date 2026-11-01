# Descent that removes a genuinely large coordinate

Author-derived, with no priority or independent-audit claim. This strengthens the geometric statement in `DESCENT_GEOMETRY.md`. The uncontrolled stochastic process is not replaced by these chosen words.

For each coordinate i let D_i consist of states x admitting an enabled reaction word to y<=x with y_i<x_i. Translation of the entire actual word shows D_i is upward closed. Dickson's lemma supplies a finite minimal basis B_i. Choose one witnessed word for each basis element. Across all nonempty B_i there are finite constants L and J bounding word length and total-count prefix overshoot. Both depend only on the raw reaction list, rather than a communication class or a growing inventory.

For any actual communicating class C,

    sup {x_i : x in C \ D_i} < infinity.                         (1)

To prove (1), otherwise choose a sequence in C\D_i with strictly increasing i-th coordinate. Dickson's lemma gives a comparable pair x<=z in that sequence, with x_i<z_i. Communication gives a word z->x, which witnesses z in D_i, a contradiction. If C\D_i is empty the assertion is immediate. No limiting stationary law is involved.

Consequently, outside a classwise finite box, choose a largest coordinate x_i. It exceeds the bound in (1), so an acquired basis word takes

    x -> x-delta,       delta>=0, delta_i>=1,

with length<=L and prefix total count<=|x|_1+J. Repeating such choices reaches a classwise finite head in at most |x|_1 words. All word-boundary counts decrease coordinatewise.

For the factorial energy E(x)=sum_i log(x_i!), each word decreases E by at least

    log x_i >= log(|x|_1/d),

whereas its prefix energy overshoot is at most J log(|x|_1+J). The first assertion uses the decrement of the chosen largest coordinate; the second uses at most J net positive particles in a prefix and the bound log(m!)−log(n!)<= (m−n)log m. If J was originally only a total-count overshoot, replace it here by the maximum sum of POSITIVE coordinate increments over every chosen word prefix. This is still a finite raw-list constant and controls factorial energy even when particles are converted between species.

Thus the actual class has finitely many translation templates giving a factorial-energy descent of order log |x|, with an energy barrier of order log |x| and linear total path length. This is substantially stronger than an arbitrary serpentine path of polynomial length. It remains a geometric statement: the process may execute competing reaction words with outward rewards.

The existence proof is valid for an abstract theorem. Acquiring every B_i and certifying completeness for a numerical compiler is a separate Petri-net problem. The explicit cubic diagnostic acquires axis words covering its whole orthant outside six states; it does not establish a general acquisition algorithm.
