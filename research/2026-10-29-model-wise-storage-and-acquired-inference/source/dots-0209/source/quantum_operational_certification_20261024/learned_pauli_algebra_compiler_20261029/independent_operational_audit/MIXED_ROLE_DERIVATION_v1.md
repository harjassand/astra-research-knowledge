# Independent derivation: mixed-role cumulative resource error
2026-10-29. Governing-author theorem not yet received; this is a conditional independent derivation, not final acceptance.

## Model that suffices
At each call, after an actual classical history h, the source is a joint channel on current n-qubit physical input B and retained memory M, with joint Kraus operators

    V_a = sum_{v in S_*} P_v tensor A_{a,v}.

The same unknown binary linear subspace S_* applies at every time/history; time-dependent coefficients, arbitrary memory dimension, ancillary inputs and changing memory spaces are allowed. If an isometric representation is used, a labels a discarded environment basis. The symplectic algebra cost of S_* is at most a known g<n; hence dim S_*<=2g. Known Pauli tensor frame and trusted Clifford/Bell controls are required. Previously stored resources O may be entangled with M, but the source never acts on O or current reference R. All subsequent controls and storage preserve O except the final prescribed teleportation.

Conditional on h, the current fresh Bell pairs are independent of OM. The current compiler produces Clifford U_h such that S_h is contained in its g-qubit gauge-only Pauli subspace T_h; padding to g fixes k=n-g across all calls. Encode B by C_h=U_h dagger. Choose the private role after the source returns, independently of all pre-role state, with service probability q in (0,1).

For probe, apply conjugate C_h to R and perform Bell measurement RB in the known physical frame. The identity (C_h* tensor I)(I tensor P_v C_h)|Phi> = (I tensor P_v)|Phi> shows that the unnormalized post-outcome state on OM is sum_a (I_O tensor A_{a,v}) rho_OM (I_O tensor A_{a,v}) dagger. Thus its outcome probability p_h(v) is nonnegative and sums to one even when O and M are entangled. Update S_h by adjoining v. A probe innovation occurs precisely when v is outside S_h.

For service, decode B by U_h and discard both gauge halves. Store the remaining k reference-output Bell resource. The mixed-gauge partial-trace identity gives its marginal Bell fidelity sum_{v in T_h} p_h(v). This remains true with spectator O: trace O,M after projecting the new logical pair; gauge Hilbert-Schmidt orthogonality cancels coherent off-diagonal Pauli coefficients. The one-step service shortfall is

    ell_h = sum_{v notin T_h} p_h(v)
          <= a_h = sum_{v notin S_h} p_h(v).

This comparison is within the same actual mixed-role occupation h, not an all-probe counterfactual.

## Stopped J-service proof
Let A_t indicate that a call is still active before its new role coin is chosen; stop immediately after J services. It is predictable. Conditional expectation gives expected service shortfall on call t equal E[A_t q ell_t], while expected rank increment equals E[A_t (1-q) a_t]. Summing nonnegative quantities by Tonelli,

    E[sum service shortfalls] <= q/(1-q) E[sum probe rank increments]
                              <= q/(1-q) dim S_* <= 2g q/(1-q).

No iid source, minimum excitation, finite-memory assumption, or optional-stopping theorem is needed. The role coin itself ensures termination almost surely and expected call count J/q. Bound each shortfall by 1 if a displayed upper bound exceeds 1.

On every terminal classical branch, the J stored Bell projectors commute. The operator inequality I-product_j Q_j <= sum_j(I-Q_j) bounds joint resource Bell infidelity by the sum of marginal infidelities. Later trace-preserving actions on memory cannot change old resource marginals; conditioning on later records can change them, so the argument must average the final branch ensemble rather than assert equality branch by branch with the earlier conditional shortfalls. Taking expectation establishes joint infidelity <=2g q/(1-q).

Standard product teleportation of a fresh JOINT Jk-qubit payload through the completed correlated resource produces a possibly correlated global Pauli channel, with identity probability equal to joint resource Bell fidelity. The unconditional half-diamond error is exactly the nonidentity probability. Payload must enter only after acquisition; no environment access to stored references/outputs can be allowed. The result does not guarantee a future directly encoded source use.

For target error epsilon, q=epsilon/(2g+epsilon) gives expected calls J(2g+epsilon)/epsilon before ideal controls and storage errors. This is an explicit throughput cost, not a free cumulative guarantee.

## Challenges / boundaries
* Marginal channel support checked only along an all-probe trajectory does not justify this actual mixed-occupation theorem. The full joint Kraus-support promise is sufficient and must remain visible.
* If current reference access or role-dependent source action is allowed, the source can target service calls and defeat the argument. Post-return private role selection and isolation are essential.
* If the source later touches stored resources, preserving each resource at acquisition proves no joint final guarantee.
* Rare generators need never be completely discovered. The guarantee is on accumulated resources; no stopped future-stationary decoder claim follows.
* Algebra cost is not the same as rank. For g=1, S_*=span(Z2,X2+Z1) has rank2 and cost1. Starting with gauge on physical qubit1, learning Z2 can move gauge to qubit2, after which X2+Z1 remains an outside correction label. Two harmful innovations can occur, so a g bound cannot be substituted without another argument.
* Both service and probe physically use n Bell pairs. Service retains k pairs and discards g; acquisition includes reference storage, actual Clifford gates, Bell readout and the full random stopping-time storage lifetime.
