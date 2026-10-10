# Primary boundary for the unary finite-determination candidate

Inspected 2026-10-09. This is a scoped comparison, not a claim of exhaustive novelty clearance.

## The precise problem

A specified rational initial vector a, a single polynomial update F over Q, and a polynomial output h define u_t=h(F^t(a)). The target is to decide whether u_t=0 for EVERY t>=0, by bounding a finite initial zero block. It is not the question of whether some u_t is zero. A bound uniform in dimension is distinguished from bounds only for each fixed dimension.

## Closest unary status statement

Clemente, *The commutativity problem for effective varieties of formal series, and applications*, arXiv:2503.21697v2 (2025), Section III-F2, explicitly says univariate polynomial-recursive zeroness/equivalence is decidable using an Ackermann complexity bound and that an elementary algorithm remains open. This is specifically about univariate polyrec, not merely multiletter automata.

https://arxiv.org/html/2503.21697v2#S3.SS6.SSS2

## Generic field closure does not solve specialization

Clemente, Donten-Bury, Mazowiecki, Pilipczuk, *On Rational Recursive Sequences*, STACS 2023, Theorem 6 and Section 4.3: symbolic independent initial coordinates admit a scalar rational recurrence of bounded order, m<=k+k^3 log(kD). The derived recurrence may be undefined after substituting a particular rational initial state. Their falling-factorial example has d initial zeros despite a generic second-order rational relation. Conjecture 17 asks for an elementary bound on the initial zero block in terms of dimension and degree. The paper also gives a PSPACE lower bound. The proposed return-domain construction addresses specified initial points without denominators; its dimension-dependent tower would not settle the stronger elementary conjecture.

https://drops.dagstuhl.de/storage/00lipics/lipics-vol254-stacs2023/LIPIcs.STACS.2023.24/LIPIcs.STACS.2023.24.pdf

## Discrete Risler bound: same endpoint, additional hypothesis

Novikov and Yakovenko, *Trajectories of polynomial vector fields and ascending chains of polynomial ideals*, Ann. Inst. Fourier 49(2), 1999, Theorems 3 and 5, Sections 1.3 and 3.4, bound consecutive zeros along each chosen polynomial orbit by a tower of height n with base 1+d^n. Their explicit hypothesis is that the map preserves the dimension of every semialgebraic variety. It is stronger than dominance and is absent from the proposed candidate. Theorem 5 separately states unrestricted eventual stabilization by Noetherianity, then imposes dimension preservation for the primitive-recursive length bound. Thus the unrestricted claim is not already the stated Theorem 3/5.

https://www.wisdom.weizmann.ac.il/~dnovikov/Papers/annalif-99.pdf

## Effective difference elimination: related mechanism, different quantifier

Ovchinnikov, Pogudin, Scanlon, *Effective difference elimination and Nullstellensatz*, arXiv:1712.01412v3 (2019), Theorem 3.1/Corollary 3.2, bounds how long a partial solution must exist to imply that SOME infinite sequence solution exists. Their Section 6 uses dimension/degree recurrences and cyclic trains, with a cubic curve case in Proposition 6.24. This is substantial prior methodological overlap.

Their Theorem 3.4 guarantees a bounded-order NONTRIVIAL elimination consequence, not every consequence or a recurrence valid at every specialized point. Remarks 3.3/3.5 and Section 5 give coefficient-dependent obstructions to unrestricted strong statements. The explicit example uses a relation whose y-coordinate is not specified by a globally polynomial update; it does not directly refute the candidate.

A fixed-point condition cannot simply be appended as a shift-invariant equation: x=a would constrain every time, not just time zero. Likewise, taking one safe cyclic train somewhere in the relation does not certify that the specified orbit enters it. The return-device argument supplies its own bounded-access-or-exit alternative. No direct application of the published main statements currently yields that alternative. Whether a known corollary or other later theorem already gives the same unrestricted bound remains an open priority question.

https://arxiv.org/html/1712.01412v3

## Current assessment

The candidate is not claimed to be an established Ackermann-to-primitive-recursive advance. The inspected statements leave a genuine-looking gap at unrestricted specified-orbit finite determination. Full priority and independent/formal validation remain unresolved.

## Exact OPS strong-theorem obstruction

The inspected Section 5.2 example fixes a positive integer M and uses the equations

sigma(x)=x+1/M,
x [y(x-1)-1]=0.

The target consequence y(x-1)-1 holds for all full sequence solutions, while suitable finite solutions beginning at x=0 violate it for arbitrarily long M-dependent windows. There is no globally specified polynomial y-update in this system. A rational attempt to propagate the required y-values meets the exceptional denominator at x=1. This is an actual counterexample to a coefficient-independent strong theorem for arbitrary difference relations. It neither proves nor refutes the more restricted globally polynomial, deterministic candidate.

The candidate therefore cannot be justified by casually invoking a strong version of Corollary 3.2: that extension is expressly false. Its entire burden is the separate coherent-return proof. Conversely, the existence of some safe orbit elsewhere in V makes existential consistency uninformative about the given orbit; fixing a time-zero point is not the same as adding an equation and all of its shifts.
