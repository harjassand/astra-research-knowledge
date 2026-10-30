# Exact factorial extraction and the missing comparison principle

Status: new candidate representation; identities below elementary, global comparison unproved.

Fix a finite weakly reversible complex graph, rates k_e>0, and mass-action rates k_e x!/(x−y_e)!. Choose any strictly positive balanced complex edge flow a_e (sum finitely many directed cycles covering every edge). Then rates a_e have complex-balanced equilibrium c=1. In every residual layer z the reference edge flux under mu0(x)=1/x! is a_e/z!, so the same finite graph circulation is repeated exactly.

## Cycle-preserving finite volumes
An ordinary reflecting box destroys this identity at its boundary. Instead select finitely many residuals z, and retain each entire complex-graph linkage layer {z+y: y in that linkage}, with all its edges. The union is finite. On every communicating component the reference generator has invariant weights mu0, exactly, since each retained layer separately balances. Exhaust residual space to recover every original transition eventually. This is an honest approximation; it does not assume tightness of its stationary laws.

For arbitrary k_e, define conductance labels c_e(z)=k_e/z!. Let T_r be the directed spanning-tree sum rooted at r in a finite-volume communicating component, with each tree edge weighted by c_e(z), summing parallel labeled edges separately. The ordinary mass-action tree weight factors as

    product_(x≠r) x! * product_tree [k_e/z!].

The first product is (product_all_states x!)/r!. Hence the stationary law is exactly

    pi_N(r) = [T_r/r!] / sum_s [T_s/s!].

Thus the chemical stability problem can be recast as control of a positive tree density T_r on an overlapping graph of translated finite complex layers. No frozen infinite-background distribution, angular potential, or gradient integrability is used in this identity.

For the balanced reference a_e, T_r is constant on the component. For arbitrary fixed k_e, naive termwise comparison only yields

    max_r T_r/min_r T_r ≤ (max_e k_e/a_e / min_e k_e/a_e)^(|V_N|−1),

which is exponential in volume, not distance. Since |V_N| can scale as N^d, this bound loses against factorial confinement for d≥2. It is not a recurrence proof.

## The actual missing construction
A useful sufficient target is a volume-uniform relative tree bound

    T_x/T_o ≤ C exp(C|x|_1)

for a fixed accessible root o (or any bound with logarithm o(sum_i x_i log(x_i+2))), on canonical geometrically complete cycle-preserving finite volumes containing o (for example all layers whose complexes lie in a box). Arbitrary selected-layer volumes are insufficient: ARTIFICIAL_VOLUME_PUMP.md gives an exact mass-action counterexample. It would yield factorial tightness, finite moments of all polynomial jump rates, and a normalizable stationary limit. The reference cycles alone do not currently establish this estimate. N33 deterministic permanence does not supply it.

Connectivity/exhaustion must be handled per component: any fixed finite path to o is present eventually, but small truncations can have extra disconnected components. Normalize on the component containing o. Weak reversibility makes all included states closed under the finite-volume transition graph. Passing to a stationary limit requires the uniform tree bound or another independently proved tightness estimate; it must not be assumed.

This target is stronger than recurrence and is not claimed necessary. It may itself be false. The next construction/falsification tests must inspect the tree density, rather than assuming generic bounded-rate perturbations preserve positive recurrence.
