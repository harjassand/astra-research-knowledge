# Directed constraint envelope for the valid-cut clock model

Status: exact candidate adapter between the explicit event-poset clock model and the envelope/fill computation. This avoids incorrectly importing an undirected1-Lipschitz extension into a clock model with oriented causal constraints. No full purge theorem is claimed.

## 1. Directed difference constraints

There are L ordered brickwork layer types. For an overlapping pair g→h with g earlier than h, valid event counters obey

    0≤n_g−n_h≤1.

Equivalently, put two directed constraint arcs:

    g→h has cost0; h→g has cost1,
    n_y≤n_x+w_(x,y) on each arc x→y.              (1.1)

Every zero-cost path strictly increases layer type, so its length is at most L−1. A path of total cost c can therefore be chosen with at most L(c+1)−1 edges. Reverse arcs have cost at most1. Let d(x,y) be the directed shortest-path cost. Balls in this cost metric have bounded physical radius, at most the edge interaction range times L(R+1).

## 2. Maximal ordinary relaxation

Freeze a set F with values c_v and suppose the current outside counters are feasible on all constraints not entirely inside F. Every outside component must have an attached frozen boundary. With paths restricted to the outside until their initial departure from F, set

    u(x)=min_(v∈F accessible) [c_v+d_out(v,x)].     (2.1)

This is the greatest feasible outside counter field. It preserves both directions of every boundary constraint, because the existing feasible field is below u and supplies the reverse-boundary lower bound.

If h<u somewhere, a legal unit increment exists. A blocked positive-deficit vertex x has a saturated incoming constraint h_x=h_y+w_(y,x). The blocking vertex y also has positive deficit; otherwise u_x≤u_y+w=h_x. Follow blockers. Values never increase, and a cycle would have total cost0, impossible because zero-cost arcs are acyclic. The path therefore ends at an unblocked positive-deficit vertex. Increment it, preserving feasibility and h≤u. Termination takes exactly the total integer deficit, as in the undirected proof.

## 3. A directed-distance sphere has a feasible boundary

Choose o∈F and let a=max_(v∈F)d(o,v). Let the frozen values accessible from the outside components have span D_c=c_max−c_min. For x with d(o,x)=R>a, (2.1) satisfies

    c_min+R−a ≤ u(x) ≤ c_max+R.                   (3.1)

The lower bound is the directed triangle inequality. For the upper bound, take a minimum-cost path from o to x and retain its suffix after the LAST visit to F. That suffix is an allowed outside path of cost≤R. Thus boundary values on S_R={x:d(o,x)=R} have spread at most W=D_c+a.

Take

    R > a + L(W+1).                              (3.2)

For x,y∈S_R, if d(x,y)≥W, the spread bound implies u(y)≤u(x)+d(x,y). If d(x,y)<W, choose a minimum-cost path of at most L(W+1)−1 edges. Any vertex z on that path obeys

    d(o,z) ≥ d(o,x)−d(z,x) ≥ R−path_length > a,

because the reverse of the path prefix costs at most its number of edges. The whole path avoids F, so exterior feasibility yields the same inequality. Therefore u|S_R satisfies every FULL directed-metric difference constraint, including shortcuts through the hole.

The directed McShane extension

    U(z)=min_(x∈S_R) [u(x)+d(x,z)]                (3.3)

agrees with u on S_R and satisfies (1.1) everywhere. This supplies a genuine oriented-causal fill, not merely undirected clock agreement.

For a finite graph the relevant sphere/ball must exist; if the entire component lies within the bounded radius, it is itself the bounded repair domain. Physical boundaries and multiple outside components are handled using their actual graph metric and all accessible boundary values, not an assumed periodic identification.

## 4. Local dirty-auxiliary computation

Use bounded-hop tuples (v,d_hop) exactly as in the bounded-hop flushing lemma, but an arc of cost w proposes

    (v_neighbor+w, d_hop,neighbor+1).

Hop count still increases by1 on every propagation, even on a cost0 arc. Thus forged minima flush after D_hop+1 sweeps. After another D_hop sweeps, shortest-cost paths with the minimal-hop tie-break have propagated. The legitimate value span is at most D_c+D_hop because w∈{0,1}; the same Q>2(D_c+D_hop+1) cyclic-order bound applies.

Fresh current snapshots, actual frozen boundary sources, a finite hop cap and the physical timing/service obligations are unchanged. Zero-cost arcs do not license resetting the hop certificate to0. This is the exact adapter to `VALID_CLOCK_CUT_SPLICE.md`.
