# Operator order and connected strong-converse amplification

[Return guide](README.md) · [Main proof](package/new_consequence_work/control/endpoint_spectral_trace_theorem.md) · [Independent audit](package/new_consequence_work/bounded/planar_endpoint_independent_audit.md)

## A local channel tests a global ratio

For an involution `U=U^dagger`, `U^2=I`, a full-rank target has unique linear bit-flip preimage `((1-p)rho-p U rho U)/(1-2p)`. It is positive exactly when

```
p <= 1/(1+kappa)
kappa = ||rho^-1/2 U rho^1/2||^2
      = ||exp(beta H/2) U exp(-beta H/2)||^2
log kappa = D_max(U rho U || rho).
```

This is a state-specific physical-preimage test, not a physical inverse channel on arbitrary unknown inputs. Established precompensation and imaginary-time growth supply prior machinery. A positive single-site marginal or bounded average disturbance does not control the global operator-order ratio.

## An explicit positive, gapped, planar cell

The recursively embedded unit-edge tree has `n_h=3(4^h-2^h)` edges and `N_h=n_h+1` qubits, degree at most three and containing-square area `(4N_h-1)/3`. Its empty root-axis corridor supports later physical connectors.

With outward-oriented edges and `n_v=(I-Z_v)/2`,

```
H_h = sum_v n_v + (1/2) sum_(u->v) n_u (I+X_v).
```

Each term is positive, bounded by one and annihilates the vacuum. Since `H_h>=sum_v n_v`, the vacuum is the unique ground state and the gap is at least one. Terms do not commute; an onsite basis change makes the model stoquastic, so a sign problem is not required.

Parent-before-child activation histories, the rooted-tree hook formula and an explicit recurrence bound produce a normalized Perron-vector witness in the root-one sector. Its root-only amplitude is at least `A^-2n`, with `A=96 e sqrt(2)`. At `beta=12`, the resulting exact root-noise threshold shrinks exponentially with cell volume. The lower positivity bound does not synthesize the preimage.

## From a negative inverse direction to trace error near one

A normalized cell witness `O=(1-p)P-p X P X` has outcomes in an interval of length one and satisfies `Lambda_p^*(O)=(1-2p)P>=0`. Every physically obtainable output therefore has nonnegative witness mean. The Gibbs target has mean at most `-delta` for a sufficiently large cell. Partition-function estimates use eigenvalue min-max rather than a false operator-monotonicity claim for exponentials.

Cells are connected by actual fixed-strength positive diagonal nearest-neighbor wires and a common spine. The graph remains degree-three and the product ground state/gap survive. Conditional on the complete connector occupation record, cells are independent Gibbs states with a nonnegative extra root field; the same negative witness margin holds for every such record. Connector correlations are retained exactly.

On any obtainable output, successive witness measurements keep an unmeasured cell in the image of its final local root channel, even for arbitrary global upstream entanglement. Conditional concentration yields

```
inf_sigma D(output(sigma),rho_connected)
 >= 1-2 exp(-M delta^2/2).
```

That is the additional completion beyond exact inverse negativity: connected targets and approximation are covered simultaneously against every upstream state. The witness can be expensive to measure; no efficient certification experiment is claimed.

The source reports completed analytic proofs and independent checks, with geometric implementations covering 12,097 and 48,769 vertices. Small spectral tests supplement the proof; the low-temperature theorem rests on analytic inequalities rather than ill-conditioned floating inversion. [Recorded checks](package/new_consequence_work/results/planar_tree_checks.json) and [geometry receipt](package/new_consequence_work/bounded/planar_geometry_verification.json) are preserved without Capital replay.
