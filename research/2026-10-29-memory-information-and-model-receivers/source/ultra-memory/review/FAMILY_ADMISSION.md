# Independent all-level admission check

29 October 2026. This supplements the whole review of A's
`RETRACTION_PROOF.md`; it is not another finite-level computation. The
governing physical family is the main alternating replacement family of
[arXiv:2605.10943v1](https://arxiv.org/html/2605.10943v1), Sections3.2--3.3,
with its actual five-qubit planar seed and its natural cancellation squares.

The reviewer verifies the following invariant package. It is stronger than
checking a few ranks, but does not extend admission to arbitrary LDPC Tanner
square complexes with arbitrary higher-overlap pairings.

1. Every qubit is incident to at least one check of each color.
2. Every nonzero X/Z check intersection has exactly two qubits, with its
   unique natural cancellation square.
3. For each check v of either color, the graph L_v=partial X_v is connected.

The main seed has X supports {0,1,2},{2,3,4} and Z supports
{0,2,3},{1,2,4}, up to labels. Its four intersections have size2. For
example L_X0 is the path 0--Z0--2--Z1--1; the other three check links have
the same path form. All qubits have both colors. Thus all three conditions
hold in the literal seed used by the exact consumer and in the primary
five-qubit surface seed.

## Cone and suspension structure

For an old X check x, every z vertex of L_x has degree2, by condition2.
Its two q neighbors are the shared qubits of x,z. Add a virtual diagonal
x--z inside their unique square; its two triangles show that X_x is a PL
cone on L_x. This is just a subdivision of the specified square, not a new
Hamiltonian check or a change of cancellation pairing.

The doubled Y_x is therefore a PL suspension of L_x, with the intervening
cylinder included. Since L_x is connected, has an edge and has no isolated
vertices, the link of EVERY vertex of a square subdivision of Y_x is
connected. At an apex the link is L_x. Away from the apices the local model
is an interval times a nonempty star, or the corresponding half-model;
punctured neighborhoods are connected. Subdivision preserves this fact.
In particular H1(Y_x;F2)=0, equivalently reduced H0(L_x)=0, as used in
the primary Lemma3.8. The local X-face pool consequently fills every tree
fundamental cycle used in A's degree-one homotopy.

## RX preserves size-two overlaps

The fine X checks are vertices of a Y_x. Fine qubits have two disjoint types:
X edges of a Y_x and Q vertices of a Y_q. Fine Z checks have three types.

* An X-face Z check intersects a vertex-X check in its two incident boundary
  edges, or not at all. Every face has four distinct vertices.
* A Q-edge Z check intersects a vertex-X check in the corresponding
  restriction X edge and its endpoint Q vertex, or not at all.
* A Z-point check intersects a vertex-X check only at a retained old z point;
  its Q-vertex intersection is exactly the old x,z intersection.

These exhaust the direct-sum degree-two bases. They prove condition2 at the
next level. In particular no new alternative pairing of a larger overlap
has been inserted by a finite-code constructor.

## RX preserves connected check links

For a fine X check at a vertex v of Y_x, the incident X-edge qubits and
X-face Z checks form the subdivided vertex link just discussed. It is
connected. A Q-vertex qubit present at v attaches to this graph through any
incident edge of its Y_q: that edge supplies a Q-edge check linking the Q
vertex to the corresponding restriction X edge. Such an edge exists because
old q has a Z neighbor. Extra Z-point checks attach between already present
Q vertices. Hence the full Tanner boundary graph of the fine X check is
connected.

For a fine Z check there are exactly three cases:

* An X-face check has a cyclic boundary link, with its four X-edge qubits
  alternating with the four endpoint X checks.
* A Q-edge check has two Q-vertex endpoint qubits. Each old X neighbor of q
  supplies a path between them through that neighbor's endpoint X checks
  and its restriction X-edge qubit. Thus its link is a union of parallel
  paths with common endpoints. There is at least one path by condition1.
* A retained Z-point check has the old Z boundary graph, with old q and x
  labels replaced by their fine Q-point and X-point copies. Condition2
  supplies precisely its old edges; condition3 makes it connected.

Every X-edge qubit has two X endpoint checks and belongs to a local face;
every Q-vertex qubit has an old X neighbor and an incident Q edge. Thus
condition1 also persists. All local cells remain incident to the face/check
pools counted in A's proof. In particular no naked isolated cell invalidates
the uniform vertex-count bound.

RZ is the degree-reversing transpose of RX with colors exchanged, so the
same argument applies. Induction proves admission at every replacement depth.

## Scope of this supplement

This is an analytic verification of the actual family's local hypotheses.
It does not independently prove the primary random Euclidean embedding,
its parameter choice, its Davies-memory theorem, or any physical device.
Those remain named external premises. For an arbitrary CSS square complex,
disconnected check links or larger intersections can invalidate precisely
the cone/suspension or p2 telescope used here. No generic admission theorem
for such inputs is asserted.
