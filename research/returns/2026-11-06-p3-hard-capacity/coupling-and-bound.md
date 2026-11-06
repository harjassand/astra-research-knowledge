# Observable coupling, rejection cost and finite-time guarantees

These are the [complete return's reported claims](P3_HARD_CAPACITY_20261106_RETURN.txt), without a new Capital proof check. Primitive meaning is strong: each binary coordinate flips at `a+γu_i`, `γ=b−a>0`, independently of its state/exterior configuration when the command is held. Hidden interacting rates and common shocks are outside the generator. HIGH consumes one unit of enabled capacity. Supplied rational state/jump reward tables and actual observations/command execution remain assumptions.

Partition into patches`B`, volume`k_B`, maximum`k`. Retain fully interior additive rewards, with omitted crossing predictable reward in`[L∂,U∂]`, `D∂=U∂−L∂`. The accepted predecessor marginal occupation/flux construction and joint rate-cost contract give a mean-capacity patch-LP relaxation`Vrel`, with `J*≤Vrel+U∂` for global hard-capacity controllers. This is an upper bound until admission and physical tracking are constructed.

Decompose finite rational patch occupations into mixtures of deterministic endpoint policies. Draw a policy label independently per patch and initialize its **internal reference state** in that policy's stationary law. These are controller-memory draws, not equilibrium preparation of the physical plant. Reference patches are independent, while bits/demand within each patch and across time may be strongly correlated. Rational stationary solves, initialization and precision are paid.

For reference requests`c_i∈{0,1}`, select `d≤c` with `Σd=min(M,Σc)` and issue`d`. Rejected demand is `O=(Σc−M)_+`. The command vector always satisfies the integer cap. Arbitrary actuator failure to obey LOW is outside that conclusion and needs a separate safety mechanism.

The reference must track observed plant events, rather than run as an unrelated simulation. The reported joint-coordinate rates are:

| Plant/reference bits | Real-only flip | Both flip | Reference-only flip |
|---|---:|---:|---:|
| Equal | 0 | `a+γd_i` | `γ(c_i−d_i)` |
| Different | `a` | `γd_i` | `a+γ(c_i−d_i)` |

The plant marginal is`a+γd_i`; the reference marginal is`a+γc_i`. When unequal, an observed plant flip can be followed by the reference with private coin probability `γd_i/(a+γd_i)`; no hidden microscopic channel needs to be identified. The reference's projected generator remains patch-local, preserving its independent patch laws despite global admission.

For Hamming disagreement`D=d_H(X,Z)`, the joint generator satisfies `L D≤γO−2aD`, hence

`2a∫₀ᵀ E D_t dt≤E D₀+γ∫₀ᵀ E O_t dt`.

If retained rewards obey `r₀(z,c)−r₀(x,d)≤K_x d_H(x,z)+K_uΣ(c−d)`, rejected requests cost at most

`K_x E D₀/(2a)+C∫₀ᵀ E O_t dt`, with `C=K_u+γK_x/(2a)`.

This charges coordinate disagreement directly rather than waiting for whole-patch synchronization or dividing by an unknown global mixing gap. The baseline factor`1/(2a)` is still a real cost and can be large.

Patch demand`D_B∈[0,k_B]` has total mean≤`M`. Independence **between patches**, not temporal/within-patch independence, gives

`E O≤(1/4)√(Σ_B k_B²)≤(1/4)√(nk)`.

Combining rejection and boundary costs proves the stated long-run intensive loss. With `Γ_P=(1/4)√(Σk_B²)` and Bellman upper-certificate span sum`S`, every initial physical state and horizon`T` obeys delivered lower `E R_T/T≥Vrel+L∂−CΓ_P−K_x E D₀/(2aT)` and global adaptive upper `supπ E R_T/T≤Vrel+U∂+S/T`. Thus intensive finite-time regret is at most

`D∂/n+CΓ_P/n+[S+K_x E D₀/(2a)]/(nT)`.

Since`D₀≤n`, no physical stationary initialization is required. Spans remain paid transients. Deleting requests is legal for this nonnegative enabled-HIGH constraint, so no slack below`M` is needed here; arbitrary mean-resource sets retain their predecessor feasibility-margin requirements.

A retained failure establishes why the observable coupling matters: a blindly copied independent one-bit reference has reward`3/4`, while its physical follower gets`1/2`, even with zero rejected requests. This refutes that shortcut, not the conditional plant/reference construction or all virtual-advice methods. The source's finite checks support exact rate marginals/disagreement/cap algebra in a four-component case; Capital has not obtained or replayed its code.
