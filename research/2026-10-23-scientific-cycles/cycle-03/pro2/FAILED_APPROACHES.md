# Failures that changed the construction

## Recursive orthogonal frames do not compose

The first constructive ansatz used five directions. At each fan apex v, choose
the child path's three periodic orthonormal frame rows in the orthogonal
complement of the row at v and the row at its parent apex. Those orthogonal
readings isolate certain diagonals and spokes. They do not control a parent
path edge globally.

Take a root triangle and attach N child three-row frames at each endpoint u,v
of its path edge. Set the parent edge coefficient to one. At each endpoint,
distribute cancellation of the opposite endpoint's query row over the N frames.
The parent action cancels, while all remaining child actions have total square
2/N. A matrix entry remains one, so the inverse ratio is at least sqrt(N/2).
This holds for every independent rotation of those local orthonormal frames.
It is a whole-ansatz failure; it does not by itself exclude arbitrary dense
graph-adapted designs. notes/fan_port_lemma.md proves the statement and gives
the precise design assumptions. checks/check_fan_ports.py records exact N=1,
16 and256 examples; the largest has1539 vertices and squared action1/128.

The separate interface challenge found the same global mechanism from a
block-action viewpoint: eliminating children can cancel a parent coefficient
through many small spokes. A locally invertible triangular block system has
no uniform global inverse merely because each diagonal block is well behaved.
Its five exact diagnostic cases and costs are retained separately.

## Protecting three parent functionals removes necessary local rank

A proposed repair protects all three independent rows needed for a parent
triangle by putting child rows in their common orthogonal complement in R^5.
This leaves dimension at most two for the child path. Including the apex gives
at most three effective child directions; long fans retain the accepted
three-query obstruction. The contradiction has precisely those three-function
independence and orthogonality hypotheses. It is not used as a universal
five-query lower theorem.

These failures suggested the covariance dichotomy: too few independent child
directions preserve a local obstruction; sufficiently many child directions
allow cheap cancellation of the root action. PROOF.md turns that mechanism
into an argument that covers every dense design, rather than only these frames.

## A rooted bad graph cannot replace a cone without paying for its edges

An initial temptation after the fan-tree lower result was to use an arbitrary
rooted bad graph as the next child and iterate. This is invalid. The high-rank
branch places cancellation coefficients from the root anchor to all child
vertices represented in its covariance. If some of those pairs are nonedges,
the witness is outside the permitted support. Iterating that shortcut at fixed
treewidth would even contradict the established six-query upper bound at
treewidth two.

The final proof explicitly requires a universal apex and supplies a separate
coning lemma. The cone creates exactly the needed allowed spokes and raises
treewidth by one. Coefficients across k+1 child copies cancel k apex-action
constraints exactly. This is the load-bearing repair, not a relaxation of
the support contract. The cone over a branching tree need not be an ordinary
fan, so the original fan-tree conclusion is proved separately in Section7.

## Projection alone would certify the wrong input

Projecting a child query block to dimension h makes an inherited obstruction
available. It does not make its action small on the actual input by equality.
The final proof charges ||D DeltaX||_F<=||D||_2||DeltaX||_F. The saved
low_projection_actual_input.json has a nonzero perturbation action and verifies
this bridge exactly. Its independently checked input hash covers the actual X.
No retuning to erase that error, or claim for an unconnected surrogate, is used.

## Earlier exclusions and stops remain scoped

The unchanged Cycle2 archive preserves fixed-palette compression and independent
recovery of all row-color aggregates failing in their stated classes. Neither
one was rerun or relabeled as the all-design theorem. The exact unit-row path
formula remains distinct from the false capped-row version and its n=4
counterexample. The separator theorem and both incoming q3 obstructions retain
their precise assumptions, analytic rates and separate executable tent bounds.

No original NIST completion, scalar-moment, molecular, GUIDE, thermal, TPV,
desalination or half-cell campaign was reopened. The new structural theorem
does not defeat the original dense numerical incumbent. Other owners' protected
programmes are not transferred or reviewed by this capsule.

## Method decision

The selected global five-direction fan-tree question is closed negatively
within its exact contract. The broader sharp treewidth theorem makes another
fixed-palette search there unproductive. The new question in CONTINUATION.txt
restricts maximum degree to four, excluding the high-degree operation that now
has a proof. No experiment on that next question was added to this checkpoint.
