# Algorithmic clock damage: exact stress tests and a rejected monotone repair

Status: **new deterministic partial results, not a QCA threshold and not a counterexample to the paper's proved discrete theorem.** The physical compiler/service/cavity receipts remain intact and do not certify these semantic steps.

Primary comparator: Dünnweber–Styliaris–Trivedi, arXiv:2601.20818v3, VII.1–2, https://arxiv.org/html/2601.20818v3 . The continuous extension is explicitly an outline. Its finite synchronization neighborhoods have diameter M+ and clocks modulo q=2M+. The precise interface between overlapping neighborhoods and the local repair scheduler is not fully formalized there. The following tests use the literal *local* interpretation of its NE-twice/SW-inflation description, not two globally synchronized spatial sweeps.

## 1. Accepted hardware facts do not give algorithmic progress

A native SUCCESS completes an attempted channel. A rejected marching guard is a correct identity attempt. Each repair/update channel needs a separate attempt/service budget. A dirty native owner can heal while its algorithmic clock remains wrong indefinitely. Clean DATA-independent schedule laws do not extend to arbitrary dirty coherent prefix inputs.

The explicit gated-repair example and fair glider are in `check_clock_repair_literal.json` and `clock_repair_fair_glider.json`. They show respectively:

* repair must not be placed behind the same potentially deadlocked marching guard;
* fair counts of literal repair attempts do not imply deterministic clock erosion.

Neither says that a given infinite glider has positive probability under the actual random native schedule. Neither disproves the discrete QCA theorem.

## 2. A one-root sloped retiming cone

Use an open square of integer sites with the initially valid absolute clock field h(x,y)=x+y, represented without wrap modulo q. Let r=n−2 and take q=8n (equivalently a conservative fixed neighborhood diameter parameter M+=4n). Change only h(r,r) by +2. This is a single local clock corruption.

Now execute repair at all sites 1≤x,y≤r other than the root in decreasing x+y order, with north/east neighbors already treated when appropriate. A site's local NE repair is:

1. do nothing if its current value is within1 of both NE neighbors;
2. otherwise choose the greatest residue within1 of both; if none, use0;
3. repeat that local test once more, then apply the stated SW maximum inflation.

There is no wrap and no fallback-to0 in this chosen prefix. Direct induction gives

    new h(x,y) = x+y+2[1+min(r−x,r−y)] .                 (2.1)

For an edge of the square cone one NE neighbor has shift0 and the other shift2. The unique compatible value has shift2. In the interior the largest compatible value has shift2 plus the smaller of the two NE shifts, giving (2.1). The local NE operation is idempotent at fixed neighbors. The SW neighbors have not yet been treated and are lower, so inflation does nothing.

Thus one clock root permits a noiseless finite repair prefix that retimes r² sites, with maximum shift2r. The sum of unperformed clock increments is

    2 Σ_(a,b=0)^(r−1) [1+min(a,b)] = r(r+1)(2r+1)/3 . (2.2)

No corresponding DATA updates are included in these clock-repair operations. An arbitrary repair-only finite prefix can be extended to a fair schedule. Consequently a proposed deterministic damage theorem cannot replace these events by O(1) local DATA faults merely because every controller remained healthy or eventually received service.

The regression `check_sloped_retiming_cone.py` checks n=6,10,20,40 exactly. This is a **possible finite prefix**, not a probability lower bound uniform in n. The actual stochastic process may suppress particular prefixes. A positive threshold needs a probabilistic damage/cut argument if it relies on that suppression.

The example also shows why speeding up repair is not automatically beneficial. The literal repair fixes fully valid fields, but can transport a clock error across a steep, otherwise valid surface before ordinary updates relax it. Slowing repair may change this race; it does not by itself bound the DATA/buffer exposure while the wrong clock waits.

## 3. Primary Gács theorem actually read

The cited scan is archived as `primary_clock_sources/self-correcting-2d.pdf`, from https://cs-web.bu.edu/faculty/gacs/papers/self-correcting-2d.pdf . Section12.6 (printed pp271–272, PDF pp24–25) proves binary consensus for a synchronous rule R*, with a finite fault budget on a torus and a time bound depending on its side length and number of faults. Section15.2 applies the binary Vote' rule in parallel iterations. This is useful geometric machinery, but it is not itself an audited asynchronous modular-clock quantum-cut theorem. In particular, repeating a local idempotent NE correction twice at unchanged neighbors is not two parallel spatial sweeps.

## 4. An actual bounded-footprint alternative and its earned cost invariant

Let a finite graph carry classical clocks. Let

    B(k)=#{edges uv : k_u−k_v is not 0,±1 modulo q}.

Fix a local repair interior S and its one-edge collar. Its attempted channel reads that full footprint. If there is at least one currently invalid edge incident on S and a replacement of clocks in S making **every edge incident on S valid**, choose such a replacement by a fixed finite table. Leave exterior clocks unchanged. Optionally erase DATA in S and reset its classical current/old buffers, so no false assertion of quantum rewind is made. If the test has no solution, act as identity. The entire finite channel can be compiled by the accepted native full-footprint Stinespring/rollback mechanism; nominal resets remain onsite.

Every nontrivial such repair removes at least one invalid edge and creates none. Every ordinary marching update which tests validity on its full incident set also creates no invalid edge. Hence, for a classical record with arbitrary fault insertions,

    number of nontrivial repairs ≤ B(initial)+Σ_j b_j, (4.1)

where b_j bounds the number of edge predicates that fault j can alter. For bounded footprint/degree, b_j is a fixed constant. This is a deterministic **retiming-event** budget, independent of how many identity attempts or clean ordinary updates occur. It does not prove that all defects disappear, that the quantum cut is valid, or that storage exposure is bounded. Under coherent noise this classical identity is only a structural starting point; one still needs an actual observable or a valid cavity expansion, not a fictitious fault record.

## 5. Exact deadlock/extension obstruction to the monotone repair

Even the closest-change local CSP version can stall after one root. The following one-dimensional fixture embeds as a strip; it is an obstruction to this repair class, not to all possible controllers.

Take an initially valid nonwrapping slope h_i=i (add a common positive offset if desired). Allowed repair interiors are integer intervals of radius r, i.e. length2r+1. Corrupt only h_0 to b=4r+3. First repair the interval S={1,…,2r+1}, holding boundary values h_0=b and h_(2r+2)=2r+2 fixed. Every feasible solution must obey h_i≥b−i. The minimum-total-change solution is

    h_i=b−i,  1≤i≤2r+1 .                            (5.1)

It makes all S-incident edges valid and removes the right invalid edge. The remaining invalid edge is (−1,0).

Consider ANY radius-r interval [a,a+2r] containing both endpoints of that edge: −2r≤a≤−1. Its outside boundary values are a−1 on the left and b−(a+2r+1) on the right. Their difference is

    b−2a−2r ≥ 2r+5,

but there are only2r+2 edges between those boundaries. No1-Lipschitz replacement exists. Intervals containing only one endpoint cannot repair the bad edge either: the analogous boundary gap is still too large. Taking q sufficiently larger than b and the window length excludes a wrapped shortcut.

Thus a root plus one perfectly nominal closest-change repair can leave an invalid edge unrepairable by every allowed local interval. With boundaries held fixed, the defect persists. Allowing outside ordinary updates changes the problem; it does not make the missing bound free. Such a process can have a finite retiming budget and still have unbounded stalled-QEC exposure.

## 6. Required next theorem, not assumed

A useful continuous compiler needs a root-cost estimate covering all three quantities:

1. unsafe or repeated/omitted DATA-channel actions;
2. retimed current/old classical buffers and the resulting quantum causal cut;
3. duration/geometry of unprotected storage or stalled correction.

The constants must not consume an O(M²) fraction of the very code gadget used to correct a root. A finite-state hitting bound with constants depending arbitrarily on M proves eventual service but does not close the renormalization exponent. Nor is a whole-neighborhood clock reset a local DATA repair just because M is fixed in N.

The current native service and CP cavity theorems solve physical timing/noise instrumentation. The algorithmic damage/cut theorem remains OPEN. A genuinely local purge/heal construction or a stochastic defect-cost theorem is required; a classical self-stabilization theorem alone does not supply the quantum interface.
