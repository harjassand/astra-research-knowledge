# Assemble the complete local residual before taking absolute values

28 October 2026. **Small analytic/diagnostic refinement; not independently received.** The frozen full-core, low-rank and trace-class sources are unchanged. This gives a potentially tighter admissible epsilon for their already proved CP-suffix mechanism, not a new recovery theorem or a generic advantage claim.

Let Chat_z=Hhat^-1 Hhat_z and C^f_z be the actual fitted physical candidate's coordinates. The acquired inverse certificate M gives the STATISTICAL-only coefficient error

    |C_z-Chat_z|<=E^stat_z=M[D_z+D_H|Chat_z|].

For action a and core column j, assemble the Hermiticity-preserving map from input A_a to the direct sum of output-coordinate/native-outcome blocks (i,o):

    Dhat_(a,j)(X)_(i,o)
      =sum_(u,v) (Chat_(a,u,o,v)-C^f_(a,u,o,v))[i,j]
                    B_(a,v) Tr(D_(a,u) X).

Its UNNORMALIZED Choi matrix is block diagonal in (i,o), with blocks

    J_(a,j,i,o)=sum_(u,v) (Chat_z-C^f_z)[i,j] D_(a,u)^T tensor B_(a,v).

Choose a certified bound b_(a,j)>=||Dhat_(a,j)||diamond. Then the complete tuple-map residual has the valid bound

    epsilon_new=max_(a,j) { b_(a,j)
        +sum_(i,o,u,v)||D_(a,u)||op ||B_(a,v)||_1 E^stat_z[i,j] }.

Proof: split true-minus-fit into true-minus-empirical and empirical-minus-fit. The first term has the existing IC dual bound. For the second, the tuple input norm is the SUM of the block trace norms, so the complete induced norm is bounded by the maximum single-column diamond norm. Combining the two costs columnwise proves the formula, including arbitrary references. Neither empirical coordinates nor their Choi matrices are required to be positive.

A simple certified choice is

    b_(a,j)=sum_(i,o)||J_(a,j,i,o)||_1,

since the diamond norm is bounded by the unnormalized Choi nuclear norm. An even cheaper rational upper bound replaces each nuclear norm by the sum over matrix entries of |Re entry|+|Im entry|. Alternatively the standard Hermitian diamond epigraph SDP can certify the local norm: Z>=+/-J and Tr_output Z<=t I, minimize t. These coordinate maps are generally NOT differences of channels and may have norm greater than two, so there is NO universal t<=2 constraint. A known Choi-norm upper bound can furnish a finite cap instead. No new SDP identity or compiler is claimed.

The improvement is taking cancellations INSIDE a complete local map before absolute values. Only the statistical uncertainty still uses an entrywise frame-weighted worst case. The matrices have one-port dimensions and no horizon tensor power. The artificial coordinate direct sum is a norm representation, not a physical memory register or a CP quotient section. The new bound can be worse than the original dual triangle bound, so min(epsilon_old,epsilon_new) is always an available safe choice.

## Exact fixture result and scope

`local_complete_residual_refinement_check.py/.json` reuses the frozen full-core author fixture in an ISOLATED temporary copy, explicitly not as new independent evidence. It forms the complete empirical-minus-fit Choi blocks and uses only the certified entrywise nuclear-norm upper bound; no SDP is executed. Synthetic statistical widths and the raw mass debit remain paid.

In that fixture, epsilon falls from approximately 0.00003098948908 to 0.00001070009562 (factor 2.896188), and horizon-three eta from approximately 0.003952576525 to 0.001365678859. The statistical-only contribution is at most approximately 1.53988 times 10^-10. All comparisons are exact rational; decimals are display. The bound remains conservative relative to the underlying endpoint error. There is no general numerical gain or practical superiority over direct service tomography, and no source samples, hardware, generic fitting, solver or compiler execution.
