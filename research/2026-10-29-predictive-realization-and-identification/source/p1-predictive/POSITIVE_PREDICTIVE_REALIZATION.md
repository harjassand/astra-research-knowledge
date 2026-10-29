# When predictive information admits positive dynamics

29 October 2026, Brisbane. Root construction. A short predictive record need not identify, or admit, a short underlying physical dynamics. The ordinary proof of the central transportation criterion and independent exact controls are preserved in `acquisition_frontier/DIRECTED_REALIZABILITY_TRANSPORT_REVIEW.md`. This root note develops its consequence interface, synthesis, and limits.

## 1. The new object and characterization

An oriented sufficient mean record on m labelled ports is
(S,w_B,b_R,b_L,c). S is an irreducible Eulerian Laplacian, w_B>0 are
calibrated port weights, and v_R=b_R-w_B, v_L=b_L-w_B are nonnegative
vectors with the same total V. For i!=j let F_ij=-S_ij. Set

    T={M>=0: M1=v_R, M^T1=v_L,
       M_ij=0 if i!=j and F_ij=0},
    J_*=min_{M in T} sum_{i!=j:F_ij>0} M_ij^2/F_ij.

Diagonal entries are allowed and unpenalized. For V>0, **a finite
irreducible positive CTMC realizes the record if and only if T is
nonempty and 2c>J_*.** Positive means nonnegative rates and positive
stationary weights, not strictly positive rates between every pair.
For V=0, c must be zero and the direct port chain suffices. Native port
holding rates are free design variables in this theorem.

Every realization using k hidden states satisfies

    2c >= (1+1/k)J_*,
    k >= J_*/(2c-J_*)  when J_*>0.

The proof identifies M as stationary hidden residence population jointly
labelled by entrance and exit port. Actual endpoint flux F and duration
sigma obey M_ij=F_ij E[sigma|i,j], row(M)=v_R, column(M)=v_L, and
sum F_ij E[sigma^2|i,j]=2c. A classical phase-type variance inequality
gives necessity. For sufficiency, choose an optimal transport, finite
diagonal return flux, and directed Erlang channels with the required
occupation masses; one explicit phase mixture adjusts the remaining
second moment. The complete proof covers arbitrary hidden cycles,
mixed entrance laws, and direct jumps with zero interior duration.

This is a **stationary network completion theorem for an incomplete
excursion-moment record**. Convex transport, scalar phase fitting and
Schur elimination remain conventional machinery. The proposed addition
is the exact equivalence between the stationary hidden-network problem
and this finite convex threshold. The targeted literature check found
no matching statement in the sources actually read; it does not prove
historical priority. See
`boundary_challenge/DIRECTED_TRANSPORT_LITERATURE_COLLISION.md`.

The directed record is sufficient, not claimed minimal. In particular,
scalar passive equilibrium means can be invariant under time reversal.

## 2. Consequences, and why the approximation metric is appropriate

With L=-diag(w)Q, interior block G=L_II, and labelled boundary B,

    S=L_BB-L_BI G^{-1}L_IB,
    b_R=w_B-L_BI G^{-1}w_I,
    b_L=w_B-L_IB^T G^{-T}w_I,
    c=w_I^T G^{-1}w_I.

For a passive exterior with reduced grounded matrix R, load z>=0,
residence c_ext>=0 and mass W_ext, all sharing the same calibration,

    T=[c+c_ext+(b_L+z)^T(S+R)^{-1}(b_R+z)]/(W+W_ext).

The assembled killed system must be transient. Every numerator term is
nonnegative. A construction with S,w_B,b_R,b_L exact and
c<=c_hat<=(1+epsilon)c therefore gives T<=T_hat<=(1+epsilon)T
simultaneously over all allowed exteriors. No bound on pointwise
survival alone would establish this guarantee. Boundary-started fields
are unchanged. Native port killing hazards use diag(w_B*kappa).

For 0<epsilon<=1 our positive construction uses at most
m+ceil(4/epsilon)m^2+1 states. It chooses diagonal flow with total
quadratic contribution epsilon*c/2, takes ceil(4/epsilon) Erlang phases
per positive transport entry, and raises any deficient second moment
with one extra phase mixture. Its initial scalar is at most
c(1+epsilon/4)^2<=(1+epsilon)c.

Whole-region transitions require separate records, with every cross-edge
endpoint retained. After deleting target regions A and assembling the
live boundary matrix, solve K_A h=b_R,live. For disjoint source union C,

    T_{C->A}=[sum_{j in C}c_j+sum_{j in C}b_L,j^T h_Bj]
             /sum_{j in C}W_j.

Perform the approximation region by region; preserving global c alone
does not preserve these queries. An exact counterexample to that shortcut
is in the directed realization review. Arbitrary hidden preparations,
unresolved separators and full survival laws are outside this statement.
For directed regions that are not stationary in isolation, preserve their
port flow imbalance and restore the fixed cross-region flows as proved
in `OPEN_MODULE_COMPLETION.md`; an isolated Eulerian hypothesis must not
be silently imposed on every region.

## 3. The regime change

Balanced v_R=v_L=v permits diagonal transport with J_*=0. Keep even a
directed Eulerian S and attach a bidirectional leaf of weight v_i at
each positive-v_i port, with conductance (V/c)v_i. This gives an exact
model on at most 2m states. Reversibility is sufficient, not necessary.
The earlier sharp 2m lower bound remains scoped to reversible competing
realizations with fixed labelled port weights.

For the two-port directed Erlang family, S has unit flow in both
directions, w_B=(1,1), v_R=(1,0), v_L=(0,1), and c_n=(1+1/n)/2.
The sole transport is M_01=1, so J_*=1 and the state bound gives k>=n,
attained by n serial phases. Its equilibrium mean to port 1 is only
5/4+1/(4n). A constant-size exact record can therefore require arbitrarily
many positive states without any large printed mean.

At fixed relative error, retaining all other coefficients exactly,
strong passive grounding isolates c and gives
k>=1/[epsilon+(1+epsilon)/n]. Conversely,
min(n,ceil(1/epsilon)) Erlang phases suffice with
c_n<=c_hat<=(1+epsilon)c_n. The large-n complexity of this family is
therefore order 1/epsilon. This is not a lower bound when arbitrary
simultaneous errors in all entries are allowed.

## 4. Acquisition and full cost remain separate

For native excursions, let s be the invariant event vector and lambda_i
the port departure rate. Then w_B,i=s_i/lambda_i,
F_ij=s_i P_ij and M_ij=s_i E_i[sigma 1{J=j}]. The right load uses
row sums of M; the left load uses column sums. Directed acquisition
therefore requires duration resolved jointly with the return endpoint.
Marginal duration means and frozen-fibre observations do not supply it.

This branch actually acquired two reversible synthetic records with
calibrated clocks, supplied tails and individual resets; it did not
execute a new directed statistical acquisition. Detailed-balance path
ratios cannot be reused for a directed event chain without a new proof.
Under Pr(sigma>t)<=C exp(-gamma t), the pending endpoint-marked duration
bias is C exp(-gamma H)(H+1/gamma), not the smaller bias of min(sigma,H).

The richer F,M-record construction preserves native total port clocks
using ceil(1/epsilon) phases per positive M entry. It must reject
F_ii>0,M_ii=0: instantaneous self jumps are not CTMC state changes.
All constructions retain clock, timestamp, source preparation, tail,
coefficient-precision and execution costs. A conventional small Schur
solve is the appropriate equally informed route for mean-only queries;
simulating the positive completion is not a demonstrated speedup.
