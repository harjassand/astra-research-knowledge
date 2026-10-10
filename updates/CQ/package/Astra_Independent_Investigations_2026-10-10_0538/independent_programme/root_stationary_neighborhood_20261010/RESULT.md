# A scoped counterexample to stationary-weighted Seymour expansion

The broad statement E_pi |N2(v)| >= E_pi d+(v), for the stationary law of the uniform-outneighbor walk on every strongly connected oriented graph, is false.

Take vertices0,1,2,3 and arcs0->1,0->3,1->2,2->0,3->1,3->2. The exact stationary distribution is(4,3,4,2)/13: multiplying by the uniform-outneighbor transition matrix gives this same row vector. The first outdegrees are(2,1,1,2); exact second outneighborhood sizes, excluding self and first neighbors, are(1,1,2,1). Hence E_pi d+=19/13 while E_pi |N2|=17/13, a deficit2/13.

The graph has directed triangles and variable outdegree. This DOES NOT refute the row-regular triangle-free stationary inequality being investigated in deep_theory_20261010, and does not refute Seymour's existential conjecture (vertex2 satisfies it). It only prevents importing an unrestricted stationary-weighted theorem without proof. No novelty claim.

Reproduce numerical discovery with test.py (seed171010; first witness n4/trial3), found.json. The exact fractions and identities above establish the counterexample independently of floating-point computation. The initial process attempt failed before execution; retry succeeded after checking the environment. No failed attempt is counted as a result.

## Triangle-free variable-degree counterexample

Use four cyclically ordered blocks, each with two vertices u_i,v_i. Put u_i->v_i inside each block and all four arcs from block i to block i+1 mod4. There are no directed cycles of length1,2,3: within a block edges are acyclic, and a cycle crossing blocks must advance through all four blocks.

Every u_i has outdegree3 and every v_i outdegree2. Every vertex's exact second neighborhood consists precisely of the two vertices in block i+2, hence has size2. The exact stationary weights are pi(u_i)=3/28 and pi(v_i)=4/28. Each u_i receives3/28 from the previous block, and each v_i receives that plus1/28 from u_i. Thus E_pi d+=17/7 while E_pi |N2|=2. Triangle-freeness alone does not rescue the broad weighted-outdegree statement.

This does NOT refute E_pi |N2|>=minimum outdegree (here equality2), nor the regular triangle-free target. It explains why row-regular pruning and its stationary law cannot be replaced by a variable-degree weighted average. This is a specialization of the transitive cyclic-block architecture already being studied, not a novelty claim.
