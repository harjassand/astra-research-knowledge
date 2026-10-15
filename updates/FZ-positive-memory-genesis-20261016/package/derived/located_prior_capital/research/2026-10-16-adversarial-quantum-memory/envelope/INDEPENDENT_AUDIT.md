# Independent attack of the envelope and uniform forcing argument

Date: 16 October 2026. Investigator: Sol 2, envelope assignment.

## Result and exact scope

I found no invalid implication in Sections 1–2 of the pinned
`2026-10-15-autonomous-frontier-v2/THEOREM_AND_PROOF.md` or the corresponding
current `sweep/MONOTONE_ENVELOPE.md`. This is a scoped pass of the local
domination and primitive block construction. It does not independently
certify the imported cluster theorem, its torus adapter, or the decoder.
Those later implications are required for the full lifetime theorem.

The first false bound I located in the supplied older material is the
`6(2Rb+3)^4` face count in `adversary/ENVELOPE_BLOCK_AUDIT.md`, under its stated
union-of-coarse-cells guard convention. The canonical file already repairs
this to `6(((2R+5)b+3)^4)` for its radius-`R+2` primitive guard. That repair
changes only fixed constants and the allowed positive noise intensity; it
preserves the time-independent, cold-start, fixed positive density,
exponential-in-`L` target if all later proof steps hold.

I derived the statements below from the event formulas and the syndrome
cycle condition. Prior auditor verdicts are not premises. The supplied old
winding-ribbon and unpruned-genealogy countermodels were read and retain
their original scope: neither disproves this envelope construction.

Source hashes and all test counts are recorded in `RESULTS.json`.

## 1. One-event domination for every even syndrome

Use infection bits `eta=1`. At a clock `v`, the only decreasing output is
the center. If the physical syndrome has an incoming edge `(v-e_i,i)`,
its two endpoints are occupied, so `eta_v=eta_(v-e_i)=1`. The envelope
therefore cannot erase a physical syndrome vertex at the center. If no
incoming edge is present, even incident degree implies an even outgoing
degree. A legal correction pairs all outgoing directions and removes
every syndrome edge incident at `v`; the center may then be erased.

For each paired face, the adjacent vertices `v+e_i` and `v+e_j` already
belong to the physical input support. The only possibly new vertex is
`v+e_i+e_j`, and all three sources of its envelope AND were occupied.
With four outgoing edges, the two selected faces have distinct opposite
corners. They cannot recreate an incident edge at `v`; the argument works
for both faces at the same event. The envelope's other four potential
upper additions merely overcount. Unchanged coordinates preserve support.

This uses parity at vertices, not that the cycle is the boundary of a
particular small membrane. In particular it applies to winding cycles
whenever they occur in an allowed global syndrome. A face fault toggles
edges only on its four vertices, so setting all four envelope corners to
one covers both creation and cancellation.

Every output is an AND/OR expression in old bits. Thus it is monotone;
checking domination at the exact physical old support suffices for every
larger envelope. Induction over ordered primitive events proves pathwise
domination for continual births. On infinite space the assertion uses
the usual locally defined graphical process; the good-block proof below
has a finite causal dependency certificate and does not need to inspect
an infinite history. On the finite torus all event histories are locally
finite almost surely. Ties between distinct Poisson streams have
probability zero; a fixed tie order can also be stipulated.

The old-state convention is indispensable. Take the perimeter of a `2x2`
square in a coordinate plane. Its lower-left vertex `v` has two outgoing
edges; the inner opposite corner `v+e_1+e_2` is initially absent. The sweep
creates that opposite vertex. Clearing `eta_v` before evaluating the upper
addition would omit it and violate domination at one event. This is an
exact counterexample to a new-state implementation, not to the canonical
simultaneous formula.

The checks enumerate all 128 even patterns of the eight incident edges,
realizing each as a finite closed cycle, and all 131,072 cycles of the
embedded four-cube graph. Every one of the 2,097,152 cube clock transitions
passes, including 16,384 transitions with a two-face physical correction.
All 245,760 cover relations of the 15-input Boolean stencil are monotone.
These checks substantiate the local derivation; their finite size is not
evidence of an asymptotic lifetime.

## 2. Healthy halfspaces and genuinely permanent clearance

For an upper output `w=v+e_p+e_q` with `w_i>=0`, the required triple contains
a source with coordinate `w_i`: choose `v+e_i` if `i` is a paired direction,
and choose `v` otherwise. That source is zero in the healthy coordinate
halfspace. The old self is also zero. The center update cannot create a
one. Hence each coordinate halfspace is invariant, including its boundary.

For `h=sum_i x_i`, every source of an upper addition at `w` has height
`h(w)-1` or `h(w)-2`. Thus the lower healthy halfspace `h<=-sb` is invariant.
If all four immediate predecessors of `w` are permanently zero, every
upper addition into `w` has a permanently zero adjacent predecessor.
The next clock at `w` clears it and no subsequent clock can reinfect it.

The word *permanently* is essential. Here is an exact binary countermodel
to replacing it by first clearance. In one coordinate plane start with
occupied vertices

    (2,2), (1,1), (0,1), (0,2), (1,0), (2,0).

All unlisted vertices, including the other two coordinates, are zero.
Clock `(2,2)` clears that target because its immediate predecessors are
zero. Subsequently clock `(0,1)`, then `(1,0)`, then `(1,1)`. The first two
create `(1,2)` and `(2,1)`. The final old-state triple creates `(2,2)` again.
This is allowed under a lower healthy halfspace. The canonical recursive
certificate has not certified those predecessors and makes no erroneous
permanence assertion.

For the no-birth lower-halfspace reference define `T_x=0` on `h(x)<=-sb`
and, on the finite predecessor cone of a target, define

    S_x = max_i T_(x-e_i),
    T_x = first arrival of the Poisson clock at x strictly after S_x.

The recursion is acyclic because height decreases on each predecessor
edge. Each cone is finite: a target of rank `r=h(x)+sb` has at most
`binomial(r+3,4)` noninitial cone vertices. By induction, `T_x` certifies
permanent zero status under *all continued no-birth clock updates*.

In fact, for the maximally infected reference above the plane, all sites
start infected until their certificate arrival, and upper additions cannot
reinfect a certified site. This reference has only actual deaths. For
arbitrary configurations initially below it, monotonicity gives the needed
upper bound without assuming their infection histories are monotone.

To justify the service variables, expose the entire finite clock DAG in
increasing height. `S_x` depends only on lower-site clocks, not on the
Poisson process at `x`. That process is independent of all previously
exposed clock processes. Therefore `E_x=T_x-S_x` is Exp(kappa), independent
of the previously exposed service variables. This proves mutual
independence by induction; it does not condition on an adaptively selected
actual syndrome component or actual clearance history.

The recursion becomes

    T_x = max_directed_paths sum_(y on path) E_y.

Every path from rank `r` to the plane has exactly `r` service sites and at
most `4^r` choices. Chernoff at `kappa/2` gives

    P(T_x>t) <= 4^r 2^r exp(-kappa t/2)
              = 8^r exp(-kappa t/2).

The displayed canonical `2*8^H` is conservative for `r<=H`. For target
cell `C_0`, `r<=sb+4(b-1)<(s+4)b`. Thus a union bound yields precisely the
advertised slow probability with harmless slack. The test explores all
1,338 reachable states and all 20,070 clock transitions in the full
15-site rank-three predecessor cone. This covers clock histories of
arbitrary length on that cone, including continued internal updates.

## 3. The clearance flag uses this slab only

The unrestricted `T_x` definition is convenient for its distribution,
but its event `T_x>Delta` has a literal current-slab implementation.
Initialize the base plane as certified. Scan only marks in `(0,Delta]`
within the finite cone. At a mark at `x`, certify `x` if all four
predecessors are already certified. A target is slow-bad iff uncertified
at the end. This scan agrees with `T_x<=Delta` and never requests the next
mark after the slab. An equivalent recursive truncated time is infinity
whenever a predecessor certificate or required local mark is unavailable
by `Delta`.

The cone lies within fine l1 distance `(s+4)b` of the target; `R>=s+5`
puts it in the fixed guard. Thus the slow flag depends solely on fresh
local clock increments. Permanent clearance is asserted for the reference
without future births; actual future slabs may of course contain births.
No permanence under future physical noise is needed or asserted.

## 4. Exact structural dependency words, including repeated clocks

For an output coordinate `w`, the possible event/input choices are

    clock w:            inputs w, w-e_1, ..., w-e_4;
    clock w-e_i-e_j:    inputs w, w-e_i, w-e_j, w-e_i-e_j, i<j.

There are exactly `5+6*4=29` structural choices, before removing redundant
or state-inactive choices. The canonical 35 overcount is safe. Each input
and clock center lies within one fine l_infinity unit of `w`, and within
two fine l1 units. A single mark's multiple outputs read the pre-event
configuration, so the next backward event time is strictly smaller.
There is no zero-time edge through another output of the same mark.

For a prescribed structural word of length `m`, even if some or all clock
locations repeat, let `N_word` count its strictly ordered distinct marks
in the slab. For each clock `v` used `r_v` times, the Poisson factorial
moment is `(kappa Delta)^(r_v)`. Integrating over the ordered time simplex
therefore gives

    E[N_word] = (kappa Delta)^m/m!.

Equivalently, conditional on counts `n_v`, random time ordering gives
`E[N_word | counts]=product_v (n_v)_(r_v)/m!`; averaging the falling
factorials gives the same formula. This second derivation is checked
exactly over 210 possible interleavings of counts `(3,2,2)`, for four
words with repetitions. Ordinary moments such as `E[N_v^m]` would be
wrong; the old-state strict ordering is exactly what permits factorial
moments here.

Union over `b^4` targets and at most `35^m` words gives

    P(fast-bad) <= b^4 (35 kappa Delta)^m/m!.

The terminal time is already arbitrary: the event counts any such tuple
in the entire slab. There is no additional observation-time union and
no factor for all output branches beyond the 29 (or 35) choices.

## 5. Uniform localization against arbitrary exterior histories

Set `m=floor(Rb/2)`. All the first `m` sites and clock centers of a backward
word are within distance `2m<=Rb` in l1 of its target; the stronger actual
l_infinity bound is `m`. Therefore the event “an m-word exists” is a
finite function of clocks in the fixed guard. It is defined from all
structural choices, not from the actual input or actual support.

Compare an arbitrary initial input healthy on `A_j` to the corresponding
no-birth infinite-halfspace reference. They are ordered throughout the
radius-`R` forced-input guard initially: for `A_5`, writing `x=bz+r` with
`r_i>=0` gives `h(x)<=-sb => sum z_i<=-s`. The coordinate alternatives
follow immediately from `x_i>=0 => z_i>=0`.

If the comparison fails at a target at any time in the slab, trace a
violating old input backward. Monotonicity says some old input must
violate the order whenever a clock output does. If there is an m-event
prefix, fast-bad occurs. Otherwise the trace remains within the input
guard and reaches the initial time or a physical birth there. The
initial order and the guarded no-birth condition exclude both. Hence
arbitrary exterior initial bits, exterior births, exterior clock speeds,
and their acceptance histories cannot spoil the target conclusion on
the same good event. This proves the forcing simultaneously for all
inputs and all five alternatives. Its use does not assert a synchronous
fine-lattice round.

On the torus, take `M` larger than the fixed guard diameter so that every
guard has an injective lift; for example `M>2R+7` safely accommodates the
radius-`R+3` primitive support. The theorem already quantifies over
sufficiently large `M`. The infinite halfspace is only a local reference
after this lift, never a globally ordered torus halfspace.

## 6. Constants, eroder geometry, and the older false count

For `b>=4`, `Rb>=4` implies `m>=Rb/4`. With the stated
`R>=ceil(280 e C)+10`,

    35 e C b/m <= 140 e C/R < 1/2.

Thus Stirling's lower bound `m!>=(m/e)^m` proves
`delta_fast<=b^4 2^(-m)`. For `s=1` and `C=10 log(8)+2`, the slow exponent
is exactly `-b`; the factors `2b^4` do not affect its limit. `C` and `R`
are fixed before increasing `b`.

For a cubic vertex guard of side `N`, the exact number of positively
based faces whose vertices meet it is

    6 N^2 (N+1)^2.

For each orientation its two in-plane base coordinates have `N+1`
possibilities and its other coordinates have `N`. The historical
radius-`R` coarse guard has `N=(2R+1)b`. At `R=1,b=4` the exact count is
146,016, while `6(2Rb+3)^4` gives 87,846. More generally the old count fails
for every `b>=3` under that literal convention. This is a real numerical
counterexample, though its effect is only a fixed-factor threshold repair.

The canonical radius-`R+2` primitive guard has `N=(2R+5)b`; its
`6(N+3)^4` count exceeds the exact count. A face base meeting that guard
lies at most one fine unit outside it, so all birth streams lie within
coarse radius `R+3`. Slow cones and m-prefix clocks lie there too. The
coarse dependence radius is consequently fixed independently of `b`.

For a finite coarse zero island, every zero output must have a zero
parent in each forcing set. The four coordinate alternatives imply that
each coordinate maximum cannot rise. The fifth implies that minimum
height rises by at least `s`. Initially
`sum_i M_i-min h <=4 diam_infinity`, so extinction is in at most
`1+4 diam_infinity/s` steps. Locality keeps intermediate islands finite.
This proves the eroder assertion directly.

Choose the imported small bad-field target `delta_*` only after fixing
`C,R` and the coarse rule. Increasing fixed `b` makes both clock terms
arbitrarily small. Taking

    sigma_0/kappa = delta_* / [18 C b (((2R+5)b+3)^4)]

makes the noise term at most `delta_*/3`. All these constants are positive
and independent of `L` and time. No usable numerical threshold follows
without quantitative later imported bounds. This is the exact
noncircular fixed-density quantifier order needed by the claimed theorem.

## 7. Between-sample forcing consequence

For an occupied target at any slab time, follow an occupied old input
backward. An own-site AND output has occupied old self. An upper OR
output either retains occupied old self or has all three occupied
sources. If the target's primitive bad flag is absent, fewer than `m`
clock steps reach an occupied initial site in the input guard; encountering
a guarded birth or reaching `m` steps would contradict goodness.

Thus whole-slab infection is assigned either to an initial infected
nearby cell, or to a current bad flag. The latter forces the comparison
bit to zero at the next layer even when the actual endpoint cell is
healthy. A birth on one plaquette followed by clocks at its base, two
adjacent corners, and opposite corner gives an explicit slab that is
empty at both samples but occupied in between. The primitive birth flag
covers it. No birth-between-samples counterexample survives that flag.

I did not use a finite-torus cluster tail or final decoder conclusion
in obtaining this statement. They remain later independent requirements.

## Reproduction

From the repository root:

    python3 research/2026-10-16-adversarial-quantum-memory/envelope/check_envelope.py

The script uses only Python's standard library. It emits hashes of the
audited sources together with all counts. `RESULTS.json` is the saved
output from this invocation. The exact counterhistories are regression
tests against weaker formulations, explicitly distinguished from
counterexamples to the canonical model.
