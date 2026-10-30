# Active-phase credit: a structural trace beyond finite head fixtures
Status: NEW PERSONAL DERIVATION, unreviewed. Proves a proposed capped trace estimate in arbitrary composition dimension under the explicit fast-graph contract. Global recurrence in that dimension is NOT claimed.

## Contract
Composition species X_1=A,X_2,...,X_d with d>=2, total N. Retain connector 0->A+B->3A+4B->0 with fixed positive constants. Fast reactions are a finite strongly connected graph of cubic composition complexes, all catalysed by 4B, and include every pure triple 3X_i. Fixed positive constants may be arbitrary.

Let I(x) be one iff at least one fast composition reaction is enabled. Fast state-level weak reversibility implies I is unchanged by EVERY fast jump: an enabled fast jump has an enabled complex return path, so its target is not inactive. Adding molecules of A cannot turn I off. If A>=1, activation adds two A and therefore lands in I=1 because 3A is a fast complex. If I=0, every X_i<=2, hence N<=2d.

Define the integer credit residual

    r=B-N-I(x).

Its exact increments are:
- Fast reaction:0.
- Immigration:0 or -1; it is -1 precisely when an inactive state becomes active.
- Activation from an inactive state:0.
- Activation from an active state:+1.
- Clearing: -1 if its target stays active,0 if its target becomes inactive.

Thus a genuine upward residual move can occur ONLY through activation during an active fast excursion. The troublesome activation at an inactive hole is exactly cancelled by the activity credit. This is a derived state predicate, not a stationary phase approximation.

## Earned active absorption bound
At any active composition, choose an enabled complex y and follow a complex path to3A, then clear. Keeping the composition residual x-y fixed makes every step feasible. Path length is bounded by a constant depending only on the finite fast graph, not N. After dividing the common (B)_4 factor, all total rates are <=C(1+N)^3 and every desired enabled rate is >=c. Bounded-jump blocks therefore give

    sup_active E tau_clear <= C(1+N)^ell/(B)_4

for some fixed finite ell. This requires neither mixing nor a drift profile. It applies to all active states, including classes with conserved residue labels. Inactive states are not falsely included.

Use the actual cap N<=L(r)=floor((log r)^p), with p>0 fixed, and stop at its actual exit or a low-r threshold. While r is neutral and the state active, B=r+N+1. The chance of ANY competing birth before the next clearing is at most

    C r^-3 (1+L(r))^(ell+1) = r^(-3+o(1)),

and its mean duration is r^(-4+o(1)). Activation is an upward exit; immigration is a neutral restart unless it exits the cap. If N>2d+3, the first clearing necessarily lands active (its new total exceeds2d) and is a DOWNWARD residual exit. Thus the apparently infinite composition tail already exits down with probability1-r^(-3+o(1)).

## Uniform bounded-attempt argument on the remaining head
At an inactive state A>=1, prescribe activation before immigration. Its probability is >=1-C/r. Activation is residual-neutral and lands active. Prescribe the next clearing before any birth; probability is1-O(r^-3) on this fixed head. If it lands active, residual goes down and we stop. Otherwise it is neutral and the inactive total N has decreased by one. Repeating at most2d times reaches an inactive A=0 state or a downward exit. Starting in an active bounded head, first prescribe clearing; it either exits down or lands in the same inactive head.

From an inactive A=0 state, prescribe successive immigrations until activity turns on. At most three are needed because A=3 is active. The first immigration occurs at its positive constant rate. The second and third, if still needed, each beat activation with probability at least c/r. The immigration that turns on activity is a DOWNWARD residual exit. Thus this part succeeds with probability at least c/r^2.

Define a block to abort and restart at the first failure of a prescribed choice, or stop at residual/cap exit. It uses at most a fixed number of active absorption episodes and inactive waiting times. Its mean duration is bounded by a constant. Its upward-exit probability is at most r^(-3+o(1)), since only activation during an active episode can be upward. Its downward-exit probability is at least c/r^2, uniformly over every capped starting state: large active states use the direct-clearing alternative above, while all inactive states belong to the fixed head. Prescribed head paths fit inside the cap for sufficiently large r.

The residual stays EXACTLY fixed between blocks. Positive renewal therefore gives

    P(first residual exit is up and remains alive) <= r^(-1+o(1)),
    E(time to residual exit OR cap exit) <= C r^2.           (1)

No truncated domain is assumed invariant. Neutral intervals at fixed r have finitely many capped states, so their nonexplosion is immediate; the weighted trace argument controls the concatenation of intervals.

## Actual stopped-cost consequence
For any fixed 0<alpha<1, and phi(r)=Gamma(r+1)^alpha times a subexponential cap-compatible tilt, (1) yields contraction

    E[phi(r_next)1_alive]/phi(r)
       <= r^(alpha-1+o(1))+O(r^-alpha) ->0.

Multiplying by any fixed polynomial preserves it. The actual stopped value W=E integral phi(r_t)dt is finite, <=C(1+r)^2 phi(r), and satisfies LW=-phi(r) inside the cap. The choice of tilt must still be matched to the quantitative outer collar; for the polylog cap exp[(log r)^(1+p/2)] is the earlier compatible choice.

## Remaining global obligations
Since B-r=N+I, the factorial resource gap on a growing-cap collar remains linear in N. However immigration can change I and therefore r by -1, and clearing can change r by -1 or0; all actual cap entries must be rechecked, rather than borrowed from the older residual without calculation.

More importantly, for d>=3 the old F+W_r entropy sum has a genuine off-cone mismatch. At A/N near0, the other d-1 populations can still have entropy near log(d-1). A radial N!-based W_r may then overwhelm F even in its negative cone. The earlier two-composition choice of one exponential damping constant does not automatically extend. This trace lemma does not resolve that global selection issue and does not prove arbitrary-dimensional chemical recurrence.

## Actual cap-entry check
Fast jumps preserve r,N. Immigration has delta r<=0 and delta N=1, so cannot enter the increasing cap from above. Inactive activation has delta r=0, delta N=2; active activation has delta r=1, delta N=2, while L(r+1)-L(r)<=1; neither can enter. Clearing has delta N=-3 and delta r in{-1,0}, and is therefore the only possible large-r cap entrance. Its exterior source lies in L(r)<N<=L(r)+3. Threshold entrances have bounded r and bounded target N, hence finite support. On the collar B-r=N+I>=N, so the same factorial B!/r! separation absorbs any earned polynomial-profile forcing. This checks the real cap rather than assuming it invariant.
