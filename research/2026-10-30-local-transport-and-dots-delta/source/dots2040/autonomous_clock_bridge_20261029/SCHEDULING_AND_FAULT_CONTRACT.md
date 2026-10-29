# Autonomous correction: physical waiting times are not independent logical faults

2026-10-29. Root derivation, unreviewed. Purpose: test the load-bearing scheduling interface before importing an ideal autonomous-QEC threshold into a finite-rate physical implementation. No threshold theorem is claimed here.

Primary context: Dünnweber–Styliaris–Trivedi, arXiv:2601.20818v1, IV.1–IV.2, uses local marching-soldier counters and Poisson update attempts. Its continuous-noise statement concerns local unitary Poisson jumps; its Discussion explicitly leaves general nonunitary perturbations open. The model below isolates the noiseless counter schedule, not the entire quantum automaton.

## Exact directed last-passage representation

Let a bounded-degree graph have closed-neighborhood size at most z. Initially every site has update count0. A site may perform its next update only when its count is no larger than every neighbor's count. Attempts arrive from independent rate-one Poisson clocks. Let T(v,k) be completion of update k, T(v,0)=0.

After every closed neighbor has reached k−1, site v is eligible for update k and remains eligible until it fires. By the memoryless clock construction, its waiting time can be generated as an independent E(v,k)~Exp(1). Thus

    T(v,k)=max_{u in N[v]} T(u,k−1)+E(v,k).

This provides an equivalent deferred-clock construction; it is not a claim that every inter-success time is itself an independent exponential. In particular elapsed waiting includes neighbor delays.

Expanding the recurrence gives a maximum over at most z^(k−1) directed space-time paths of length k, with an independent exponential weight at each vertex on a fixed path. Different paths may overlap and are NOT independent.

For 0<lambda<1 and a>0, the union/Chernoff bound is

    Pr[T(v,k)>=a k+s]
    <=exp(-lambda s-k[lambda a+log(1-lambda)-log z]).

Taking lambda=1/2 and a=2 log(2 e z) yields

    Pr[T(v,k)>=a k+s] <= exp(-k-s/2).

The bound is uniform in total system size, albeit loose. A union over all sites costs log N in a global completion statement; a single-site expectation or positive mean update density does not remove that cost.

## A warning against the wrong fault contract

A single long first waiting time E(o,1)>s has probability exp(-s). Every site v at graph distance r then satisfies T(v,r+1)>s by a dependency path from (o,1). Thus one rare delay forces late updates on an entire growing spatial cone. For a d-dimensional grid, the number of forced late update locations within radius R is of order R^d, while choosing s proportional to R makes the witness probability exp(-O(R)).

Consequently a bound of the form Pr(all r selected UPDATE LOCATIONS are late)<=eta^r cannot hold uniformly for a fixed eta<1 when those selected locations span the delay cone and d>1. This does not prove the quantum memory fails: geometric delay clusters may be correctable and still give exponential lifetime in linear size. It does prove that a marginal O(p) noise probability between successful updates, or a mean update speed, is insufficient by itself to establish a product local-stochastic fault law in update-index coordinates.

The counterexample is about scheduling delays, not directly about quantum error events. Turning delay into damage requires specifying storage noise and its independence; no such step is silently assumed.

## Consequential next obligation

A microscopic damped-ancilla implementation needs a threshold-compatible joint fault contract. Options are (a) prove local fault bounds in physical space-time with the real asynchronous schedule retained, then show the automaton tolerates that model; or (b) construct a bounded-delay recovery/control mechanism that prevents a rare slow site from forcing an uncharged extended idle region. An average-speed argument is not either construction.

The desired capability is scalable autonomous quantum preservation using fixed local interactions and finite reset rates, not a global channel approximation whose error grows with volume*time. The supplied ideal-jump architecture and its restricted noise theorem remain a comparator, not an already-paid microscopic interface.
