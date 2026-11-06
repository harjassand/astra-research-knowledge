# Exact repair and recovery inside a fixed-depth window

For a local circuit of fixed depth `h`, let mutable flag `p_g` control each gate, define layer products `W_ℓ(p)=∏_(g in layerℓ) U_g^p_g` on disjoint supports, and `W(p)=W_h(p)…W_1(p)`. Different layers may not commute. The controlled unitary is `V=Σ_p |p><p|⊗W(p)`.

Replace each controller change `p→p′` with a physical CPTP attempt that also applies `W(p′)W(p)†`. Any control history telescopes exactly to `W(p_m)W(p_0)†`, including reversals and repeated/out-of-order changes. All-zero to all-one flags therefore produce the intended circuit without measuring/copying the unknown input; arbitrary untouched references remain. An `H₀`, CNOT₀→₁, `T₁` example includes the backtracking sequence `000→010→110→100→101→001→111`. Compensation is installed in the physical generator, not assigned to a reliable outside controller.

Recovery must transform too. With `𝒱=Ad_V`, conjugate separate-factor time-independent controller/data generators together:

`Lphys=𝒱 (LC⊗id+id⊗LM) 𝒱⁻¹`.

Every actual controller attempt `Φ_i` becomes `𝒱(Φ_i⊗id)𝒱⁻¹`, and every data recovery `R_j` becomes `𝒱(id⊗R_j)𝒱⁻¹`. They remain CPTP with fixed attempt rates. On classical flags, recovery is `Ad_W(p) R_j Ad_W(p)†`, following the partial gate. The transformed controller and recovery commute because the original separate-factor operations commute. Different recoveries need not commute, and retain the original data-dynamics order.

This earns compatibility of repair, noncommuting work and concurrent recovery **within the window**. It does not construct a scalable autonomous memory `LM` or noisy-progress controller `LC`. Assuming either would leave the full processor unfinished. Unchanged recovery during a partial shared gate can act on the wrong intermediate code, even if logical command order is correct.

For actual physical burst CPTP faults `F_j` supported on installed registers in `B(z_j,R_j)` with a shared adversarial environment `E`, use `(𝒱⁻¹⊗id_E) F_j (𝒱⊗id_E)`. This retains shared-environment correlations, adaptivity and coherent clock/program corruption. With gate range at most `a`, conservative enlargement is `ℓ=ha`, so transformed fault support lies in `B(z_j,R_j+ℓ)`. Full chronological channels satisfy `Cphys=𝒱 Cframe 𝒱⁻¹` for actual attempts, including no-op branches, without conditioning on a successful trace or random completion time.

Minimum radius1 gives `R+ℓ≤cR`, `c=1+ℓ`. A comparison Pareto source of intensity `λ′=λc^α` contains among radius≥`c` marks a process of intensity`λ` with radii`cR`; transformed faults fit their corresponding marks, and extra marks can act as identities. The exponent`α` and `r=α−d` remain, while intensity budget worsens explicitly. No independent effective-noise assumption appears. This is a **fixed-h** source assignment, not the missing joint protection/progress event.

| Component cost | Established scope |
|---|---|
| Local support diameter | `b→b+2ha` |
| Flags/program selectors | Bounded per gate, `O(h)` registers per data site at bounded gate density |
| Local dimension | Fixed only for fixed`h`, potentially large constants |
| Attempt rates/overlap | Per-term rate retained; constant overlap, charged constant slowdown for fixed total-rate cap |
| Wiring | `O(N)` for installed registers, range-dependent constants |
| All-installed register-time | `Nt`, including controller and idle hardware |
| Reset/other attempts | `O(Nt)` expected at bounded rates |
| Source budget | `λ(1+ha)^α`, with rate slowdown also charged |
| Startup/acquisition/receiver | Not constructed or removed |

These are component costs, not an end-to-end processor upper bound. All claims and finite-check descriptions come from the [complete return](P2_FIXED_DEPTH_CONTROL_20261106_RETURN.txt); the linked code TXT was not delivered or executed.
