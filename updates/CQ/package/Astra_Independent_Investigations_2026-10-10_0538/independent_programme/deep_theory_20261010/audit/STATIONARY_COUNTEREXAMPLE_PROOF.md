# Exact counterexamples to two stationary-averaging candidates

Date: 2026-10-10. Status: explicit finite constructions, checked with exact rational arithmetic. These are counterexamples to proposed auxiliary inequalities, **not** to Caccetta–Häggkvist or Seymour's conjecture.

## Conclusions

Let G be a finite strongly connected r-outregular oriented graph with no directed triangles. Let pi be the stationary distribution of its uniform outgoing random walk, d^-(v) its indegree, and s(v) its exact second out-neighborhood size (excluding itself and first neighbors).

1. The proposed inequality E_pi s >= r is false. An example has n=64, r=20, and
   E_pi s = 20 - 29/1186.
2. Even the weaker proposed repair E_pi(d^-+s) >= 2r is false. An example has n=160, r=52, and
   E_pi(d^-+s) = 104 - 2493/485524.
3. Both occur in one explicit family G_q, with
   n=48q+16, r=16q+4, n=3r+4.
   Every integer q>=1 violates the first candidate. Every integer q>=3 violates the joint candidate; q=3 is the first failing parameter in this family. No claim of global minimality is made.

## 1. The 16-vertex internal graph H

Partition the vertices into A={a0,a1,a2,a3}, B={b0,b1,b2}, C={c0,c1,c2,c3}, D={d0,d1,d2,d3}, and U={u}.

Insert all arcs in the four complete bipartite orientations

A -> B -> C -> D -> A.

Inside A insert a0->a1->a2->a3->a0. Finally insert u->a_i for all i. Insert no other arcs.

Every vertex has outdegree four. H has no loops, digons, or directed triangles. It is not strongly connected, because u is a source. Its exact local statistics are:

| Class | Size | Indegree in H | Second out-neighborhood size in H |
|---|---:|---:|---:|
| A | 4 | 6 | 5 |
| B | 3 | 4 | 4 |
| C | 4 | 3 | 4 |
| D | 4 | 4 | 3 |
| U | 1 | 0 | 3 |

For example, a vertex in A reaches one new A vertex and all four C vertices in exactly two steps. A vertex in D or U reaches precisely B as its new second neighborhood. Consequently sum_v s_H(v)=63, whereas sum_v d_H^+(v)=sum_v d_H^-(v)=64.

## 2. The strongly connected outregular triangle-free graph G_q

Fix an integer q>=1. Let K_q be the directed circulant on Z/(3q+1)Z with arcs i->i+j for j=1,...,q. Replace each macro vertex i by a copy H_i of H; preserve its internal arcs. For each arc i->j of K_q insert every arc from H_i to H_j.

This construction is a lexicographic substitution with all copies identical.

- n=16(3q+1).
- Each vertex has r=4+16q outgoing arcs.
- Strong connectivity follows because the macro step +1 is allowed, and every macro arc connects all vertices in the corresponding copies.
- The graph is oriented. The positive macro steps lie in [1,q], so opposite macro directions cannot both be present; H itself is oriented.
- A directed triangle with a cross-copy arc would have macro increments in {0,1,...,q}, at least one positive, whose sum is positive and at most 3q. It cannot equal zero modulo 3q+1. A triangle with no cross-copy arc would lie in H, which has none.

At any vertex v of internal type x,

  d^-_G(v)=16q+d^-_H(x),
  s_G(v)=16q+s_H(x).

For the second identity, the new macro endpoints are the q copies at offsets q+1,...,2q. Macro offsets 1,...,q are already first neighborhoods. Two-step paths that stay in one copy contribute exactly the internal second neighborhood. Mixed internal/external paths lead to copies already in the first neighborhood.

## 3. Exact stationary distribution

The stationary mass of every macro copy is 1/(3q+1) by macro translation symmetry and uniqueness. Let rho be the conditional stationary distribution within a copy; it is constant per vertex in each of A,B,C,D,U. Write these per-vertex probabilities as a,b,c,d,u respectively.

Since each of the q predecessor copies contributes its entire conditional mass equally to each target vertex, stationarity is equivalent to

  r a = q + a + 4d + u,
  r b = q + 4a,
  r c = q + 3b,
  r d = q + 4c,
  r u = q.

Normalization is 4a+3b+4c+4d+u=1. Equivalently,

  rho = (4/r) rho P_H + (16q/r) Uniform(H).

Thus rho is a uniformly restarted distribution on H, rather than H's own stationary distribution. This restart is the essential mechanism.

Set T=256q^3+240q^2+84q+13. Solving the five equations gives

  a = (2q+1)(16q^2+9q+2)/(2T),
  b = (64q^3+60q^2+23q+4)/(4T),
  c = (256q^3+224q^2+73q+12)/(16T),
  d = (8q+3)(128q^3+104q^2+31q+4)/(16(4q+1)T),
  u = q/(4(4q+1)).

All are positive. The probability of any individual vertex of G_q is its corresponding value divided by 3q+1.

## 4. Exact expectations and signs

The internal second-neighborhood deficit is +1 on A, 0 on B and C, and -1 on D and U. Therefore

  E_pi s - r = 4a - 4d - u
               = -(2q-1)(16q^2+11q+2)/(2T).

This is strictly negative for every integer q>=1.

The internal indegree surplus gives

  E_pi d^- - r = 24a + 12b + 12c + 16d - 4
                 = (576q^3+524q^2+163q+20)/(4(4q+1)T).

This remains strictly positive, consistent with the stationary entropy inequality.

Adding yields

  E_pi(d^-+s) - 2r
    = -(256q^4-464q^3-568q^2-193q-24)/(4(4q+1)T).

At q=1 and q=2 this quantity is positive. At q=3 it is negative. For all q>=3, write q=z+3, z>=0; the numerator polynomial becomes

  256z^4 + 2608z^3 + 9080z^2 + 11519z + 2493,

which is positive. Hence all integer q>=3 violate the joint candidate. As q tends to infinity, the second-neighborhood deficit tends to -1/16, the indegree surplus tends to zero, and the joint deficit tends to -1/16.

Specific values:

| q | n | r | E_pi s-r | E_pi d^--r | E_pi(d^-+s)-2r |
|---:|---:|---:|---:|---:|---:|
| 1 | 64 | 20 | -29/1186 | 1283/11860 | 993/11860 |
| 2 | 112 | 36 | -44/1063 | 1175/19134 | 383/19134 |
| 3 | 160 | 52 | -895/18674 | 20777/485524 | -2493/485524 |

For q=3 the conditional per-vertex stationary probabilities are

  a=1211/18674,
  b=2341/37348,
  c=9159/149392,
  d=121203/1942096,
  u=3/52.

Divide each by ten for the full 160-vertex stationary probabilities.

## 5. Scope and significance

These constructions invalidate a universal stationary second-neighborhood inequality, including its proposed joint indegree repair. They do not rule out a substantially different inequality or a statement restricted to a hypothetical CH-counterexample density regime. In fact n=3r+4 in every G_q, so the directed-triangle CH bound n>=3r+1 is respected.

The failure explains why a proof for simple cycles of homogeneous regular blocks can be misleading: each H is outregular but internally non-Eulerian, and external uniformly distributed arrivals change its conditional stationary weighting. Dilution makes this weighting approach the uniform measure, under which H has total second-neighborhood deficit one.

## 6. Exact verification and artifacts

Run:

  python independent_programme/deep_theory_20261010/audit/verify_counterexample_family.py

The verifier uses only standard-library sets and fractions.Fraction, constructs full adjacency lists, checks all vertex degrees, absence of loops/digons/directed triangles, forward and reverse reachability, positivity and normalization of pi, every stationarity equation, every exact second-neighborhood cardinality, and all expectation formulas. It verified q=1,...,5 successfully.

Primary certificates:

- counterexample_q1_n64_r20.json
- counterexample_q3_n160_r52.json

Each contains the complete adjacency list, exact stationary probabilities, indegrees, second-neighborhood sizes, and exact expectation gaps.

The initial independent annealing run tested 524,489 proposed mutations across 108 runs and found no failure. That negative heuristic result is superseded by the explicit counterexamples, not evidence for either inequality.

## 7. Relevant prior literature, without claiming prior occurrence of this candidate

Sullivan's 2006 survey states the unweighted average second-neighborhood conjecture for Eulerian oriented graphs as Conjecture 6.15 on page 8, attributed to Seymour and/or Jackson:

https://aimath.org/WWN/caccetta/caccetta.pdf

Cary's accepted 2019 paper discusses that conjecture explicitly on page 766:

https://arxiv.org/abs/1711.01189

Seacrest's arc-weighted version defines a different weighted second neighborhood and proves equivalence to Seymour's conjecture; it does not supply the stationary-weighted average candidate considered here:

https://arxiv.org/abs/1212.1883

I did not locate a primary source stating this exact stationary-weighted candidate. This is a limited search outcome, not a novelty claim. The graphs above are non-Eulerian, so they do not refute the Eulerian average conjecture.
