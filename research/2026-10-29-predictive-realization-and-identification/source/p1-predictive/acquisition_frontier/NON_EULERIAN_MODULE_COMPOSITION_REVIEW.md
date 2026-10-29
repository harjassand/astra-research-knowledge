# Independent review: composition of modules with boundary flux imbalance

29 October 2026. This is a new scope proof for the directed completion
construction. It does not re-audit the completed acquisition or global
clock-ceiling proofs. All weights and cross-region stationary edge flows
below are supplied mathematical data.

## Result and precise scope

The root's extension is valid for a partition into regions with disjoint
retained port sets. A region need not be stationary or irreducible by
itself. Its local weighted Laplacian may have nonzero column sums at its
ports. What is needed locally is row balance, column balance at hidden
states, positive retained and hidden weights, and a transient hidden block.
The complete assembled trace must be irreducible and column balanced.

Each region may be completed independently by the earlier free-clock or
clock-capped channel construction. It must preserve that region's oriented
record and scalar c separately. Cross-region stationary edge flows are
reattached unchanged. The resulting full CTMC is stationary for the
preserved port weights and constructed hidden weights, and it preserves
the previously declared whole-region equilibrium-source mean hitting
times.

For clock ceilings, each port's spare departure budget subtracts all fixed
outgoing off-diagonal trace flow, including cross-region flow. If multiple
modules share a port instead of forming a region partition, the spare
budget must be allocated jointly among those modules; independently
spending the same budget twice is not justified by this result.

Every hidden state must be able to reach a retained port. A hidden closed
communicating component is excluded. In a finite CTMC this reachability
condition is equivalent to the hidden killed block being an invertible
M-matrix. Mere local row balance does not imply it.

## 1. Local identities do not require Eulerian ports

For one region, order its ports B before its hidden states I and write

    L = [[L_BB, L_BI], [L_IB, G]],  D=diag(w_I).

Assume L*1=0, and assume its hidden columns sum to zero:

    1_B^T L_BI + 1_I^T G = 0.                         (1)

No corresponding zero-column-sum assumption is made at B. Define

    S   = L_BB - L_BI G^-1 L_IB,
    v_R = -L_BI G^-1 w_I,
    v_L^T = -w_I^T G^-1 L_IB,
    c   = w_I^T G^-1 w_I,
    M   = L_BI G^-1 D G^-1 L_IB.                     (2)

The usual nonnegative off-diagonal rates and transient G make M, v_R,
v_L nonnegative. The hidden rows of L*1=0 give
G^-1 L_IB 1_B=-1_I, while (1) gives
1_B^T L_BI G^-1=-1_I^T. Consequently

    M 1_B = v_R,          1_B^T M = v_L^T,
    1_B^T v_R = 1_B^T v_L = 1_I^T w_I = V.          (3)

Thus all transportation margins used by the completion theorem survive
without stationary ports. Endpoint support also survives: if the local
trace flow F_ij=-S_ij is zero for i!=j, then M_ij=0. Both the direct
and hidden-mediated contributions to F_ij are nonnegative.

For the native second-moment identity, set A=-L_BI and E=-L_IB. The
hidden killed generator is -D^-1 G. Its endpoint-resolved first-duration
matrix is G^-1 D G^-1 E, so the entrance-flux weighted matrix is exactly M.
Its second-duration vector is 2 G^-1 D G^-1 w_I. Summing over entrance
fluxes and using 1_B^T A=1_I^T G gives

    sum_{entrance,endpoint} flux * E[sigma^2 | channel]
      = 2 * 1_B^T A G^-1 D G^-1 w_I
      = 2 w_I^T G^-1 w_I = 2c.                     (4)

These are local flux identities. They do not assert that the isolated
module, with those weights, is stationary. In particular, a port with
no local outgoing channel need not have a local departure experiment;
its associated entrance row is simply zero.

## 2. Exactly the needed boundary divergence is preserved

The Schur matrix is row zero even though it need not be column zero:

    S 1_B = 0,
    1_B^T S = 1_B^T L_BB + 1_I^T L_IB.              (5)

The right side of (5) is the original module's column-sum vector at its
ports, equivalently the vector of outgoing minus incoming stationary
flows. Therefore the off-diagonal trace channels already encode the
local port imbalance that the exterior must cancel.

The channel completion retains every local off-diagonal F_ij. Each
constructed hidden phase is individually flux balanced. A self-return
channel contributes equal incoming and outgoing flow at its port; an
off-diagonal channel contributes its prescribed F_ij from port i to j.
Thus the replacement has exactly the same boundary divergence (5).

Let X be the row-zero Laplacian of the unchanged cross-region edge
flows. With disjoint region port sets, the complete trace is

    K = X + direct_sum_j S_j.                        (6)

By assumption the source's K has zero column sums. Replacing each region
preserves every S_j, hence K, so the assembled replacement has balanced
hidden states and balanced ports. Dividing each outgoing edge flow by
its positive source-state weight defines an actual CTMC whose stationary
weights are exactly those specified or constructed. If K is irreducible,
all nonzero channel phases are reachable from and can reach its ports,
so the full replacement is irreducible. No isolated-module irreducibility
or isolated-module stationarity has been used.

## 3. The free-clock and rate-capped local tests still apply

The necessity arguments use (3)-(4), endpoint support, and channel moment
bounds; none uses port column balance. The sufficiency construction also
does not require it: its phase flow balance is internal to a channel,
and the known cross-region edge flows supply the missing port balance.

Therefore, for a positive local hidden mass V_j, the same local transport
polytope and free-clock criterion 2c_j>J_*j apply. Under a hidden ceiling
Lambda_j and port ceilings ell_i, the correct spare budget is

    a_i = w_B,i ell_i
          - sum_{k in B_j, k!=i} F^(j)_ik
          - sum_{k outside B_j} fixed_cross_flux_ik. (7)

It must be nonnegative. The module's diagonal channel is forbidden at
a_i=0, and the same capped criterion 2c_j>=J_cap,j then applies. The
off-diagonal channel transport is restricted to its own region. Regions
with V_j=0 must have c_j=0 and need no hidden completion. External edges
that are added after this assembled base network still require their own
remaining rate budget.

## 4. Whole-region means are preserved by the separate scalars and loads

Let A be a union of target regions and let C be a disjoint union of
source regions. Hidden states cannot cross region boundaries without
hitting a retained port. Therefore entrance into A occurs at an A port.
For each live region j, elimination of its hidden mean equation gives
the same local right load b_R,j=w_B,j+v_R,j. With K grounded at the target
ports, the retained mean field h_B is unchanged by the replacement.

The weighted sum of hitting times over one source region is

    c_j + b_L,j^T h_Bj,
    b_L,j = w_B,j + v_L,j.                           (8)

This follows directly by substituting
h_Ij=G_j^-1(w_Ij-L_IB,j h_Bj) into the population average. Its stationary
mass is mu_j=sum b_L,j=sum b_R,j. Hence

    E_{stationary conditioned on C} tau_A
      = [sum_{j in C}(c_j+b_L,j^T h_Bj)]
        / sum_{j in C} mu_j.                        (9)

Preserving only the total sum of the c_j would not establish (9) for all
source unions. Separate c_j and left population loads are indispensable
at this declared interface. No statement about arbitrary hidden initial
states, time distributions, or interventions follows from (9).

## 5. Exact control

The adjacent checker builds an original nine-state directed cycle with
four ports. Region A has the local directed path 0 -> hidden -> hidden -> 1;
its two hidden weights are 1 and 2. Region B has a three-hidden-state path
2 -> hidden -> hidden -> hidden -> 3 with all weights one. All edge flows
are one. Cross-region edges are 1 -> 2 and 3 -> 0. Port weights are one.

Both local Schur matrices are [[1,-1],[0,0]]: neither is Eulerian or
irreducible. Their left and right loads are respectively (1,4) and (4,1),
and their separate scalars are c_A=7 and c_B=6. The complete four-port
trace is the irreducible directed unit-flow cycle.

The replacement of A has direct 0 -> 1 flow 1/6 and a three-phase prefix
of flow 5/6, then exits with flow 1/3 or enters a fourth phase with flow
1/2. All hidden exit rates equal one; its weights are 5/6,5/6,5/6,1/2.
B retains its three unit phases. The completed network has eleven states,
the same port weights, and unchanged cross-region flows. Every port has
departure rate exactly one, leaving zero diagonal budget after all fixed
outgoing trace flows, including cross flows, are charged.

The checker verifies local non-Eulerian divergences, both exact oriented
records and transport matrices, assembled stationary balance and clock
ceilings. It compares all fifteen nonempty port-target means by full
killed-system solves and separately checks both whole-region transitions:

    stationary A -> whole B: 16/5,
    stationary B -> whole A: 3.

All calculations are exact fractions. This is supplied-data mathematical
validation; no source access, observation, or hardware preparation occurs.
