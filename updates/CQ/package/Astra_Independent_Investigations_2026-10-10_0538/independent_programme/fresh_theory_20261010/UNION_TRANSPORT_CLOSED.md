# Closure-native upward transport: falsified and already known

Status: independent rediscovery of a known counterexample, not a new result and not progress on Frankl's conjecture.

Candidate: for every nontrivial finite union-closed family F, some coordinate e admits an injection from the sets omitting e to sets containing e, with A contained in its image.

Exact counterexample: take F to be all unions of edges of the cycle C5, including the empty union. F has 17 members: empty, the five edges, the five three-vertex paths, all five four-sets, and the full set. Every coordinate occurs in 10 sets. For e=0 on the standard cycle 0-1-2-3-4-0, the four absent sets {2,3}, {1,2,3}, {2,3,4}, {1,2,3,4} have only the three present supersets {0,1,2,3}, {0,2,3,4}, {0,1,2,3,4}. Rotation gives the obstruction at each coordinate. This is a 4-to-3 Hall violation, including for fractional transport.

The seeded search in transport_search.py independently found an isomorphic C5 family after 6,280 tests; counterexample_raw.json preserves its original labels. Random search is not a proof of minimality.

Generalization proved directly: for C_n with n>=5, F_n is the family of all unions of edges, equivalently vertex sets whose induced subgraph has no isolated vertices, together with empty. Fix e and put B=V minus {e and its two neighbors}. B is a path with n-3>=2 vertices. Each of the four sets obtained by optionally adjoining e's two neighbors lies in F_n and omits e. Among their possible e-containing supersets, exactly B union {e} is forbidden, because e is isolated. Thus the same 4-to-3 Hall obstruction holds for every coordinate of every F_n.

A bounded-deletion repair cannot have a universal coordinate-count bound: replace each vertex of C5 by t inseparable copies and replace every family member by the union of its copied blocks. If fewer than t elements may be deleted, the allowed relation is still upward at block level, so the same Hall obstruction survives. This observation is not presented as novelty.

## Primary literature verification

Alec Edgington gave exactly the symmetric 17-set C5 counterexample in the February 13, 2016 discussion of Gil Kalai's upward-injection conjecture:
https://gowers.wordpress.com/2016/02/13/func3-further-strengthenings-and-variants/
Find the Edgington comment dated February 13, 2016, 8:10 pm. The follow-on discussion already studies cyclic interval unions.

The natural repair by isotone nonnegative weights was already discussed as weighted FUNC by Gowers and Edgington in February 2016:
https://gowers.wordpress.com/2016/02/22/func4-further-variants/
This route is closed here rather than relabeling that known conjecture as an acquired primitive.

Current entropy developments checked for avoidance of duplicate work, not independently audited: Yunjiang Jiang, Entropy bounds and global couplings for union-closed families, arXiv:2609.08291v1, September 8, 2026. It claims a 0.38288525 bound and uses inverse-union-multiplicity balancing. No claim about the current proved best constant is made here.
https://arxiv.org/html/2609.08291v1
