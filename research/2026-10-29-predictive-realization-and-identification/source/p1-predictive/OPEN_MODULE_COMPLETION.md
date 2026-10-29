# Directed modules need not be stationary in isolation

29 October 2026, Brisbane. Root's scope completion for the use of the
positive-realization theorems in whole-region transition queries.

## 1. The distinction

An irreducible stationary global source can carry current through a
region. Removing its cross-region edges leaves a row-zero local
Laplacian whose column sums at retained ports need not be zero. The
closed-chain theorem cannot simply be applied to that local matrix as
though the prescribed weights were its isolated stationary law.

The construction nevertheless extends to these open modules. The
necessary information is already in the directed Schur matrix: its
column sums retain the boundary flow imbalance. No hidden cross-region
edge is permitted; every cross-edge endpoint must be a retained port.

## 2. Open-module hypotheses and identities

The regions here partition the states and have disjoint port sets. If
two modules share one physical port, their return flows must share a
jointly allocated departure budget; the independent budget formula below
must not be counted twice at that shared port.

Partition each region into ports B and interior I. Retain all known
cross-region stationary edge flows in a separate cross-edge Laplacian.
The local internal-edge Laplacian L_j has zero row sums. Its hidden
columns sum to zero because the original global stationary balance has
no cross-edge at a hidden state. Only port column sums can be nonzero.
Assume every hidden state reaches a retained port, so G=L_II is an
invertible M-matrix. Individual modules need not be irreducible.

Write A=-L_BI, B0=-L_IB and D=diag(w_I). Then

    G1=B0 1,  1^T G=1^T A,
    M=A G^{-1}D G^{-1}B0,
    M1=b_R-w_B, M^T1=b_L-w_B,
    c=w_I^T G^{-1}w_I.

Both excess-load totals equal the region's hidden mass. These identities
use balance only at hidden columns and therefore survive a nonzero
boundary current. The internal trace flow off diagonal is still
F_ij=-S_ij, and the local Schur matrix S has zero row sums. It need not
have zero column sums.

The boundary divergence is unchanged by eliminating hidden nodes:

    1_B^T S = 1_B^T L_BB + 1_I^T L_IB.

This follows by substituting 1_B^T L_BI G^{-1}=-1_I^T into the Schur
formula. The right side is exactly the original local column imbalance
at the boundary.

## 3. Completion preserves the imbalance that the exterior balances

Use the same residence transport and channel constructions locally.
Each hidden phase receives and sends equal stationary flux. Off-diagonal
trace flow is fixed to -S_ij; diagonal return channels have no net port
divergence. Hence the completed module has exactly the same boundary
column imbalance as its S, and therefore as its predecessor module.

After reattaching the unchanged cross-region edge flows, all these
imbalances cancel in exactly the original way. The complete Laplacian
is Eulerian, so the retained port weights and constructed hidden weights
form its stationary measure. If the assembled trace graph is
irreducible, so is the completed chain. Standalone stationarity of each
module is neither required nor asserted.

For a clock ceiling ell_i, calculate spare self-return flux using EVERY
fixed outgoing trace flow at that port, including cross-region edges:

    a_i=w_i ell_i-d_i,internal-d_i,cross.

Forbid hidden transport between regions, preserve each c_j separately,
and use this a_i in the local clock LP. The scalar envelope, support
conditions and variance adjustment proofs do not require balanced
boundary columns. Their assembled generator respects the port ceilings
and all hidden rate ceilings. The free-clock construction extends in
the same way. Empty hidden mass still requires c_j=0.

## 4. Whole-region consequence

Delete entire target regions A. With the remaining local Schur matrices
and unchanged cross edges, solve K_A h=b_R,live. For any disjoint source
union C, block elimination gives

    E_{w(.|C)}tau_A
      =[sum_{j in C}c_j+sum_{j in C}b_L,j^T h_Bj]
        /sum_{j in C}W_j.

The starting law is the GLOBAL stationary measure restricted to C; it
is not equilibrium of an isolated open module. Replacing each local
record exactly leaves this consequence unchanged. Keeping its other
entries exact and c_j<=c_hat_j<=(1+epsilon)c_j gives the same uniform
one-sided relative bound, because all source contributions are
nonnegative. This supplies the missing qualification for modulewise
use of the closed-chain completion theorems.

## 5. A small exact open-current example

Use four ports 0,1,2,3 and two hidden states a,b, with one directed
cycle of unit stationary flow

    0 -> a -> 1 -> 2 -> b -> 3 -> 0.

Port weights are one; hidden weights are 2 and 3. Region A consists of
0,a,1; region B consists of 2,b,3. Cross edges are 1->2 and 3->0.
Each local Schur matrix is [[1,-1],[0,0]], with nonzero column sums.
Their load pairs are b_R=(3,1),b_L=(1,3),c=4 for A and
b_R=(4,1),b_L=(1,4),c=9 for B.

All native port rates are capped by one. With hidden ceiling one, an
alternative A channel takes a direct jump with probability 1/3 and
three rate-one Erlang phases with probability 2/3. The B channel uses
a direct jump with probability 2/5 and five rate-one phases with
probability 3/5. The replacements preserve each mean record and the
unit trace flux; reassembly is stationary. All hidden rates are one,
although this common-rate realization uses more states than the original
slower exponential channels.

The two whole-region stationary-conditional means are 11/4 from A to B
and 18/5 from B to A. These follow directly from the displayed records
and can be compared against full killed equations. This is a supplied
mathematical construction, not an additional acquired source assay.

## 6. Executed controls and independent scope review

`check_open_modules.py` constructs both displayed generators directly,
checks hidden and global stationary balances, eliminates the two open
modules, and verifies both whole-region killed means as exact fractions.
The six-state source and twelve-state common-rate completion agree; every
prepared departure rate is exactly one. No source observations occur.

The separate ordinary review and checker in
`acquisition_frontier/NON_EULERIAN_MODULE_COMPOSITION_REVIEW.md` and
`check_non_eulerian_module_composition.py` verify a different nine-state
source and eleven-state completion, preserving distinct regional scalars
7 and 6. Its 15 boundary-target means and both whole-region means agree
exactly. The review explicitly checks transience, boundary divergence,
cross-flow charging and the disjoint-port budget hypothesis.
