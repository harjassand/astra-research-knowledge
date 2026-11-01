# A coupled activation family beyond every target-following episode

This is a diagnostic for the FULL programme, not a replacement endpoint or a recurrence counterexample. It has three free species and two mutually changing large inventories. It is outside the pinned-controller architecture and outside the new primary binary theorem.

Take the positive unit-rate weakly reversible ONE-linkage raw mass-action cycle

    0 -> A+B -> 2A+B+C -> 3A+2B+2C -> 0.                         (1)

Its complexes y0,y1,y2,y3 have degrees 0,2,4,7 and are componentwise ordered. The reaction increments are

    (1,1,0), (1,0,1), (1,1,1), (-3,-2,-2).

They span all three dimensions. None of A,B,C is a pinned phase or an imposed constant inventory.

## One genuine infinite class, not a ray across different classes

For every b>=1,c>=0 the actual word [0,1,1,3], using zero-based reaction indices in (1), gives

    (0,b,c) -> (1,b+1,c) -> (2,b+1,c+1)
      -> (3,b+1,c+2) -> (0,b−1,c).

For every b>=0,c>=1, the actual word [0,0,1,3] gives

    (0,b,c) -> (1,b+1,c) -> (2,b+2,c)
      -> (3,b+2,c+1) -> (0,b,c−1).

Each displayed propensity is positive under precisely the stated conditions. Repetition reaches (0,0,0). Weak reversibility gives enabled reverse communication paths for both words. Therefore ALL plane states (0,b,c) lie in the SAME actual class, as do their neutral complex lifts (0,b,c)+y_j. In particular z_n=(0,n,n) is a genuine fixed-class escaping residual sequence. A full complex cycle ending at y0=0 supplies the reachable carried mark 0 at each such state.

## The complete carried-target family fails here

At physical state z_n+y_j, every later source y_k, k>j, is disabled because its A count exceeds j. Every earlier enabled source y_k, k<j, is componentwise below y_j. Thus the residual increment of ANY non-target source is

    E(z_n+y_j−y_k)−E(z_n) >= 0.

Following the carried target costs zero. Consequently EVERY target-following episode, to EVERY terminal complex and with ANY number of target-following loops before its first source switch, has nonnegative total entropy reward on this escaping sequence. The failure is pointwise on every terminal branch, rather than a loose scalar bound. Any increasing transform of that reward has the same failure.

The actual target source probabilities also satisfy

    p_(z_n+y_j)(y_j) -> 1        for j=0,1,2,3.

Their leading degrees in n are respectively 0,1,2,4, and no later source is enabled. Hence no terminal rarity is available; the binary source's governing lemma is genuinely false here.

## The missed negative operation is real and actual

The first deletion word deliberately fires reaction 1 TWICE. The second use occurs with carried target y2 and source y1, so it borrows residual (1,0,1) and has positive entropy reward log(n+1). The subsequent actual reaction 3 has source y3 and repays that borrow while removing B, with reward -log(n(n+1)). The COMPLETE word has reward -log n. Stopping at its first source switch removes the essential repayment. Its probability is small, so a chosen path alone does not prove average inward drift.

The second deletion word similarly removes C by a non-target activation. Both words retain all real changes in B and C. A successful next representation must keep such borrowed inventories until repayment, and control all competing branches and the physical clock. A stationary fiber or supplied neighboring profile would bypass the very operation this family forces.

The ensuing actual A-return cycle calculation is developed in `UNPINNED_ACTIVATION_CYCLE.md`. Its stopped return/reward bounds are an operation on this obstruction, not an assertion that all boundary charts or the general recurrence theorem have been closed.
