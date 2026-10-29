# Scoped receiving review of the coupled-transport consequence

30 October 2026. Actual inputs and the imported support builder were read. Exact snapshots are retained beside this review.

| Input | SHA-256 |
|---|---|
| `COUPLED_TRANSPORT_WITHOUT_KINETIC_IDENTIFICATION.md` | `2888431d94a8f0b6777460208ada2b3f06e3252bca9d93e8c6e17dba93ed6114` |
| `check_coupled_transport.py` | `a95541eaf71852a2b7994f8b98aa3fee2ebd58ab82d761452acad63012f5bfa7` |
| `COUPLED_TRANSPORT_CHECK.json` | `da7d39384597fc655e7474b25bfb8f05e4a14c582dc05303fdf6c870dec3e953` |
| Imported `check_event_memory.py` | `67aae0769abe185d3b0a2ed8c6e6d15a86f2bbb0f4641206d127419272c8831d` |

**Disposition: accepted at the stated gate, force, and fault interfaces.** No substantive mathematical correction is required. The executed fixture was inspected, including its actual imported builder; it was not expanded or rerun. This is an application of established tight-coupling and stochastic-network machinery with a supplied selective gate, not acceptance of a new thermodynamic principle or a physical implementation.

## 1. The support coboundary is exact

With `epsilon_1=1`, `epsilon_2=-1`, allowed selected events satisfy `epsilon_a delta=u_before` and flip the bit. For `g(u)=-u/2`, their current difference and potential increment are both `u_before`. Unselected events have zero marked increments and preserve the bit, so the equality holds on those edges too. Summing gives `J_1-J_2=g(u_t)-g(u_0)` for every finite actual path. Nonexplosion extends it to every finite physical time, without a stationary or Markov assumption on the timing law.

The result concerns the two declared marked currents. Unselected particle displacement cannot be discarded from a different density or complete-displacement observable. The actual file preserves this distinction. A zero gate rate is a support premise and is not certified by a finite confidence interval for a small positive rate.

## 2. Force sign, entropy factor, and exact stall law

Baseline marked detailed balance gives

\[
\frac{q_h(x,y,a)}{q_h(y,x,a)}
=\frac{\mu_0(y)}{\mu_0(x)}e^{2(h_1d_1+h_2d_2)}.
\]

The factor two in the force affinity is therefore correct for the supplied convention `q_h=q_0 exp(h dot d)`. In stationarity the gradient contribution of `log(pi_h/mu_0)` sums to zero. Pairing directed marked edges gives the nonnegative entropy production and exactly `sigma=2(h_1 I_1+h_2 I_2)`. The bounded coboundary gives `I_1=I_2`, hence the displayed `2(h_1+h_2)I`.

At `h_1=h`, `h_2=-h`, the force increment is `h[g(y)-g(x)]`. Direct multiplication gives

\[
\mu_h(x)q_h(x,y,a)
\propto\mu_0(x)q_0(x,y,a)e^{h[g(x)+g(y)]},
\]

which is unchanged under reversal. Thus the sign `mu_h proportional mu_0 exp(-hu)` is correct. In a product baseline with a fair bit this reweighting preserves the visible marginal. It supplies an invariant law, not a prepared initial law or convergence-time bound. Restriction and renormalization on an individual communicating class is understood when the support is reducible.

The isothermal power ratio has the correct load sign and the same factor two. It is valid only with the declared physical force interpretation and inclusion of every affinity. It does not pay for an unmodeled actuator or establish a complete apparatus efficiency.

## 3. Productive-cycle strictness

Every closed marked path has `J_1=J_2=k`. Its force affinity is `2(h_1+h_2)k`, since the baseline potential terms telescope. A productive cycle with `k!=0`, present with positive rates in the finite class, excludes **marked-edge** detailed balance when `h_1+h_2!=0`. Strict positivity of the stationary distribution in that class then makes the paired entropy sum strictly positive. The claimed current sign follows from its entropy identity.

The marked qualifier matters in a general multigraph: aggregate state-transition balance could conceal oppositely marked channel fluxes. The file defines rates, reversals and entropy at the marked level, so this issue is already handled. Absence of a productive cycle can block conversion, and a small common positive rate scale can make its power arbitrarily small. The proof does not assert a kinetics-independent power lower bound.

I checked the eight displayed transitions against the oriented triangles and unselected chords. All satisfy the gate and occupancy support, and their signed sum is `(-3,-3)`. The reverse is allowed. The builder supplies exactly the 20 occupancy/bit states, and its reciprocal support plus the reported reachability witness establish the stated connected support for this fixture.

## 4. Executed population check

The checker uses `build(1., 'opposed', 1.)`, so closed-gate edges are absent and all permitted selected rates are positive. It multiplies each unordered marked reverse pair by the same random reciprocal factor; unselected pairs receive the same treatment. Its force multiplication is `exp(h dot d)` with reverse increments checked explicitly. The generator uses row sums zero and solves the transposed stationary system with normalization.

The recorded 15 cases correspond to three reciprocal-prefactor choices and five force pairs. They check equal currents, stall, strict current sign away from stall, and the marked entropy identity. The largest recorded entropy-identity error is `4.08006961549745e-15`, consistent with the manuscript's rounded statement. The report's embedded checker hash matches the actual checker. The imported builder's hash is pinned separately above, since the embedded checker hash alone would not identify that dependency.

These floating-generator residuals are population checks. The exact path/cycle algebra and the proof for arbitrary reversible kinetics do not depend on their numerical tolerances.

## 5. Error counts and their exact scope

For the two fault types introduced in Section 5, the identity is correct. A selected wrong-sign event that still flips the bit has residual

`(d_1-d_2)-Delta g = -2u_before`,

while an isolated extra bit flip has residual `-u_before`. Summing signed residuals and then applying the triangle inequality gives `|J_1-J_2|<=1+2N_wrong+N_extra_bit`.

This count bound retains the atomic update on each selected event except for the explicitly counted isolated flips. It is not a bound for arbitrary missed selected-event updates, as the following paragraph already says require a separate supplier/model. For example, two correct-sign channel-1 events while the bit fails to update give current difference two with both displayed fault counts zero. If missed updates are admitted, they need their own mismatch count. The current theorem is accepted with this specified-fault interpretation, not an unrestricted fault-tolerance interpretation of the phrase 'every recorded actual path'.

## 6. Predecessor and selection boundary

The primary Lipowsky–Liepelt network paper and Utsumi's actual CJoin-with-memory model were opened during this scoped review. Utsumi's minimal model explicitly correlates transfers through a one-bit internal state, switches the input/output roles after firing, and distinguishes a paid reset protocol. This supports the root's narrowed interpretation and its refusal to inherit a hardware realization or exact-zero gate by analogy. No additional opportunity survey was undertaken.

The retained consequence is useful: a supplied opposed gate imposes exact current locking and a kinetic-independent stall condition without learning arbitrary reciprocal prefactors. The main selected result remains the nonlocal physical path law, compatible hidden kinetics, and the zero-external-clock receiver. No claim of new tight-coupling thermodynamics, apparatus feasibility, finite-data certification, or practical superiority is accepted here.
