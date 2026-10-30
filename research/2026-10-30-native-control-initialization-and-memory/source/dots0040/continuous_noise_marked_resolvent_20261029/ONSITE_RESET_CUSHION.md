# Actual onsite reset cushion: an all-orders single-cluster norm bound

2026-10-29. New construction, not independently reviewed. Unlike the unmodified-generator first-reinsertion note, this changes the physical generator by an allowed onsite reset. It proves a single-cluster inclusive bound, not yet a full memory threshold.

## Physical change and its cost

At every hub site add the complete replacement generator

    mu (R_h - id),   R_h(rho)=|Q0,0><Q0,0|_h tensor Tr_h rho.

Use all basis-state Kraus jumps sqrt(mu)|Q0,0><a|. Their complete loss is mu I, so the replacement records are independent rate-mu Poisson clocks even for arbitrary entangled inputs. No external schedule or disabling is supplied. Existing locks are not released until the hub has been reset; normal Q cleanup follows. Thus reset-first isolation is preserved.

In the forest frame these replacements can apply a partial circuit to DATA when they strike an in-flight computation. They are NOT harmless ideal service. Charge every replacement as a bounded-support local DATA/controller fault at rate mu. Its output is good Q0, workspace0; it preserves all other good history sectors. Its conditional mask coherences remain quantum. The locality enlargement is the same bounded commuting-frame enlargement already proved. Thus the original Poisson theorem can tolerate this physical change alone when mu is below its (possibly extremely small) noise budget.

## Dimension-independent signed CP domination

For a bounded Hamiltonian H=g A, ||A||<=1,

    -i[H,.] = T_plus - T_minus,
    T_plus(rho) = (g/2)(I-iA)rho(I+iA),
    T_minus(rho)= (g/2)(I+iA)rho(I-iA).

The sum has effect g(I+A^2)<=2g I. Signs can be interchanged according to the Hamiltonian convention; the displayed difference has the stated -i commutator.

For a Lindblad jump L with ell=||L|| and B=L†L/ell^2,

    D[L] = T_plus - T_minus,
    T_plus(rho)=LrhoL† +(ell^2/4)(I-B)rho(I-B),
    T_minus(rho)=(ell^2/4)(I+B)rho(I+B).

Their sum effect is ell^2[B+(I+B^2)/2]<=2ell^2 I. Zero terms are omitted. These formulas hold with a retained bath and do not introduce bath resets or a bath-dimension factor. Each Kraus support is that of the original perturbation plus identity.

Let T_e=T_e,plus+T_e,minus and assume

    sum_(e: h in H_e) ||T_e*(I)|| <= a epsilon.

The cost convention uses Hamiltonian norms and squared Lindblad-operator norms; it is not asserted equal to the minimum generator diamond norm.

## Positive majorant of a seeded cluster

Use the exact routed mark lift from EXACT_MARKED_DUHAMEL.md. In each active set M:

1. Resum all exterior perturbations (H_e disjoint M) as actual CPTP evolution.
2. Omit incident perturbations from that baseline.
3. Route each incident T_e gain to M union H_e. This is a positive majorant of the signed routed expansion.
4. Route the actual independent replacement of marked h to M minus {h}. Nominal terminal/abort resets can also clear h and only improve the following bound.

The majorant is CP but generally not trace preserving. Its signed version sums exactly to the physical evolution. It involves no expansion of exterior spacetime volume.

For weight V(M)=q^|M| I, q>1, the adjoint of the majorant obeys, on a sector with m=|M|>0,

    A* V(M) <= m q^m [mu(q^(-1)-1) + a epsilon q^b] I.

Proof: exterior CPTP evolution preserves the scalar weight. Each marked replacement has scalar intensity mu and decreases its exponent by one. Each routed positive gain has effect bounded by its declared norm and adds at most b marks. Sum the incident budgets over marked owners; overcounting terms touching several owners is harmless. Other mark-clearing gains have nonpositive contribution to this inequality. At M empty no incident terms are expanded, and the full CPTP evolution is retained forever.

Consequently, if

    a epsilon q^b < mu(1-q^(-1)),

the total majorant mass, including absorbed empty-mark trajectories, is <=q^m for an initially normalized positive input in sector M. Equivalently its complete-instrument diamond norm is <=q^m. Composing an arbitrary seed insertion E contributes only ||E||diamond. This controls ALL orders of locally growing and merging dirty marks, without a factorial divergence and without exp(N epsilon T).

For q=2, epsilon < mu/(a 2^(b+1)) suffices. The same drift with a strict margin gives exponential decay of the still-active weighted mass: restrict the majorant to nonempty sectors (kill extinction gains), then m>=1 implies contraction at least mu/2-a epsilon 2^b. Thus pending-cluster output is explicitly bounded rather than dropped.

A fugacity z>=1 per routed reinsertion replaces a epsilon by z a epsilon in the same inequality. Whenever z a epsilon q^b < mu(1-q^(-1)), the sum of majorant masses of paths containing at least k reinsertion events is <=q^m z^(-k). Since every insertion enlarges support by at most b bounded local neighborhoods, this also controls genealogical cluster size. Independent replacement events are physical faults and must be included separately in the memory witness; the above does not erase their cost.

## Exact scope and remaining composition

This closes the all-orders SINGLE seeded inclusive influence cluster, under a real additional onsite reset noise floor mu. It is distinct from depolarizing-generator conversion: no joint data depolarizer, no finite bath dimension, and no claim that the original perturbation is a Poisson CPTP kick.

It does not by itself complete the full long-time SSF memory proof. One must organize multiple seeded clusters or fixed AGP masks so that (i) every dangerous witness is covered, (ii) overlapping clusters are not multiply charged with uncontrolled multiplicity, (iii) all unselected exterior terms remain CPTP, and (iv) the now-present physical replacement faults are included in the same connected spacetime envelope. The positive majorant is a norm tool, not the actual noise probability law. This remaining linked-cluster assembly must be proved, not assumed from the single-cluster drift.

The physical tradeoff is explicit: choose mu below the existing positive-kick memory threshold, then epsilon sufficiently smaller than mu. Whether resulting constants support a useful memory is unestablished.

### Retained-bath caution
The displayed CP norm identities remain valid on system plus a shared retained bath. Empty marks mean only that the system controller histories initially dirtied by this algebraic cluster have regenerated. They do NOT mean the seed's influence on the bath has vanished. A later bath interaction at another site is part of the resummed exterior background and can carry that information back. Therefore the result is not a bounded causal influence cone in a shared-bath model. A complete shared-bath threshold must use an inclusive fault-mask convention that charges those later system-bath interactions as noise locations, rather than inferring locality from bath-memory erasure. This is a substantive remaining assembly obligation.
