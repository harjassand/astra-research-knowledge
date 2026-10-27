# Conditional-hopping retargeting and acquisition: independent audit

Published capital pin: `1dc593a750b447be6536bafcf0be156d27767dfe`. Analytic audit only: no principal scripts, residual searches, hardware, helper, or live workspace used.

## Verdict

**The exact local balance repair is valid for the stated conditional nearest-neighbor hopping class.** N747's residual algebra and N765's diagonal-control derivative identities extend. The inherited thermodynamic identification extends with the actual current covariance replacing `t²/2`. A parametric rational witness, support-complete isolation, and explicit statistical/calibration budgets are essential. Existing numerical regret bounds do not transfer automatically.

The ordinary three-axis process-tomography/log acquisition is valid with the small-error cap and bias allocation below. It has conservative `epsilon^-2` shot scaling per setting, unlike the weaker short-time-slope assay's `epsilon^-4`. Neither is a new invention of tomography or an acquired physical interface.

## 1. Exact balance and locality

Let

`H_a=-sum_i a_i(n_env)(sigma_i^+ sigma_(i+1)^-+h.c.)+H_diag`,

where `a_i` is real, translation invariant and finite range, depends only on sites outside its hopping pair, and `0<a_min<=a_i<=a_max`. Let `H_diag` be bounded, translation invariant, finite range and real diagonal. Write `A_a=-i[H_a,.]` and let `P` be occupation dephasing. Nominal hopping is constant `t0>0`.

Define `E_i f` literally as the matrix-element projection retaining only off-diagonal pairs `xi=eta^(i,i+1)` with unequal pair occupations. Different nearest-neighbor edges define disjoint coherence sets on sufficiently large periodic rings. Set

`f_a=f0+sum_i(t0/a_i-1)E_i f0`.

On an edge coherence, `f_a,eta xi=(t0/a_i(env))f0,eta xi`. Because the environment excludes the pair, this multiplier is real and equal at both endpoints. Odd Hermitian parity is preserved. Other coherences remain unchanged.

Each population commutator entry is a sum over these edges. Edgewise,

`H_a,eta xi f_a,xi eta=(-a_i)(t0/a_i)f0,xi eta=H_0,eta xi f0,xi eta`,

and the other product agrees as well. Diagonal Hamiltonians contribute nothing to the diagonal of any commutator. Thus

**`P A_a f_a=P A_0 f0=0` exactly.**

This is a configuration-edge flux rescaling, with no population inverse. It does not construct an accurate witness from scratch.

For an extensive sum of local densities, `E_i` removes all off-pair coherences and retains the neutral exchange component on the pair. Its Pauli implementation therefore preserves locality. `1/a_i` is a diagonal function on the same finite environment, with a finite projector/Walsh expansion; multiplication enlarges the support by that environment. Translation covariance survives. All full commutator outputs must be included in the final footprint `W` before applying large-ring stabilization. A general environment table can require exponentially many entries in its range, and small `a_min` increases coefficients and precision costs. Finite support does not establish economical complexity.

## 2. Residuals and diagonal-control jets

The Hamiltonian remains real and number conserving. It therefore preserves the parity structure used in N765: `RS=SR`, `RA_a=-A_aR`, `(RB)^*=RB`, and `Rj_a=j_a`, where `B=S+A_a`. The N747 balanced two-sided formulas and N765 corrected residual identity apply to `f_a` and an admitted even trial `g`. Exact balance leaves only the regularized population residual `lambda P g`, whose normalized norm tends to zero. No population residual is discarded by `S^+`.

Assume amplitudes are independent of design control `V`, `H_diag(V)` is affine diagonal, and each nominal polynomial trial coefficient is balanced. Then `f_a(V)` remains polynomial in `V`, rational in the positive amplitude parameters. The diagonal perturbation `A1` annihilates populations and creates no population output, so

`||(S+lambda)^(-1/2) A1 (S+lambda)^(-1/2)||<=4J_*(H1)/d`

and the complete response-error derivative bounds survive in form. The residual's full extra polynomial order must be retained.

Finite-shot acquisition yields amplitude intervals, not exact amplitudes. **A midpoint retargeting `t0/a_hat` is generally not balanced for the actual `a`.** The valid method is the symbolic rational witness `f(a)`, whose identity holds at every point of the acquired positive box, with complete residual/derivative bounds uniform on that box. Arbitrary rounding also requires an exact reconstruction preserving the identity.

If physical `V` changes hopping or current, the omitted derivatives must be included and bounded; the diagonal-control theorem alone does not cover them. The rate `S_odd>=d` applies on the number-neutral/even-X/Y sector containing the current and exact solution. Trials with single-X/Y components require their actual `S^+` rates rather than an incorrect blanket rate `d`.

## 3. Actual current and thermodynamic extension

The diagonal coefficient commutes with all densities, so the exact continuity equation has current

`j_i=(a_i/2)(X_iY_(i+1)-Y_iX_(i+1))`.

It is local, centered, odd, number neutral and obeys `S j_i=d j_i`. Under product trace, currents on different edges have different flip patterns and hence zero cross-edge inner product, including when diagonal environments overlap. Exclusion of the hopping pair from `a_i` gives exactly

**`b_J:=||j_a||_#²=(1/2)E_tr,env[a_i²]<=a_max²/2`.**

Use this actual covariance everywhere the constant-hopping source used `t²/2`. The susceptibility remains `chi=1/4`.

Positive amplitudes make every nearest-neighbor swap available. Each fixed-number configuration graph is connected, so finite-volume fixed points remain functions of total number. The same dissipation argument excludes other undamped imaginary eigenmodes; contractivity excludes zero Jordan blocks. The current is orthogonal to all fixed points.

Bounded finite-range dynamics and local currents give fixed-time thermodynamic current correlations. Contractivity yields `|C_n(t)|<=b_J`. The number-neutral parity Schur operator retains lower bound `d`. Hence the source's regularizer argument gives

`kappa(lambda)<=b_J/(d+lambda)`,

`regularizer comparison error<=lambda b_J/d²`,

and rescaled spectral tail bound `2b_J/(R d)`.

The positive current spectral measure, Stieltjes uniqueness, continuity equation and the same order of limits then identify

**`D_a=4 kappa_a(0+)`**

as the actual infinite-system second-moment coefficient. No global population-gap lower bound is needed. This does not establish Gaussian hydrodynamics or a physical-time convergence rate.

For diagonal `V` control, the local complex resolvent disk persists with `b0=b_J/d`. On a finite positive amplitude box, use a uniform upper bound for `b_J`, common `d_min>0`, fixed finite range and bounded coefficients. Normal-family convergence transfers control derivatives and complete finite residual identities to the actual thermodynamic scalar. New residual quality, curvature, global exclusion and policy bounds are still needed for a useful uniform regret certificate; the old numerical tables are not automatically valid.

## 4. Three-axis tomography and principal logarithm

Under support-complete isolation and a fixed prepared Z environment, the logical pair obeys

`H_pair=-aX+(Delta/2)Z`,

with coherence dephasing `d`. Its Bloch generator is

`K=[[-d,-Delta,0],[Delta,-d,2a],[0,-2a,0]]`.

Set `L=2a_max+Delta_max+d_max`, so `||K||_2<=L`, and choose `tau=1/(4L)`. Moreover `K+K^T=-2diag(d,d,0)<=0`, hence `||exp(tK)||_2<=1`. For `M=exp(tau K)`,

`||M-I||_2<=tau||K||_2<=1/4`.

Preparing each positive Bloch axis and measuring each axis gives nine transition means per environment pattern. If every entry of `Mhat` has **total** error at most `delta`, then `||Mhat-M||_2<=3delta`. Choose

**`delta_total<=min(tau epsilon/3,1/24)`.**

Then `R=max(||M-I||,||Mhat-I||)<=3/8<1/2`. The principal log is given by its convergent near-identity power series, and `log M=tau K`. Telescoping the noncommuting matrix powers proves

`||log M-log Mhat||<=||M-Mhat||/(1-R)<=6delta_total`.

Extract `a_hat=(log Mhat)_(2,3)/(2tau)` with one-based indexing. It follows that

**`|a_hat-a|<=3delta_total/tau<=epsilon`.**

No commutation between `M` and `Mhat` is assumed in the Lipschitz argument. `Mhat` need not be a physical channel: the near-identity bound ensures its real principal log exists. Finite arithmetic/truncation error in evaluating the log must be allocated in the total budget.

For `Q` environment patterns, independent bounded-outcome Hoeffding with statistical radius `delta_stat` gives a sufficient count per setting

`N>=2 delta_stat^(-2) log(18Q/failure)`.

The factor accounts for all `9Q` means. This radius is statistical, not the entire error when nonzero systematic bias remains. For example require total preparation/switching/readout/numerical bias at most `delta_total/2`, use `delta_stat=delta_total/2`, and take

`N>=8 delta_total^(-2) log(18Q/failure)`.

Thus fixed coarse bounds give conservative `epsilon^-2` repetitions per setting, with `9Q` settings, all coherent preparations, reset, switching, calibration and classical log computation charged. The physical access is stronger than the one-contrast assay and is established process-tomography methodology, not a new metrology primitive.

## 5. Short-time slope fallback

Starting instead at logical `+Y` and measuring Z, the Bloch equations give `z'(0)=-2a` and

`|z''(t)|<=B:=2a_max(Delta_max+2a_max+d_max)`.

With observation mean bias at most `b`, independent N-shot mean `Zbar` at time `h` obeys, with probability at least `1-delta`,

`|-Zbar/(2h)-a|<=Bh/4+b/(2h)+sqrt[2log(2/delta)/N]/(2h)`.

Taking `h=epsilon/B`, `b<=epsilon²/(2B)`, and `N>=2B² epsilon^-4 log(2/delta)` yields an interval of radius epsilon. This validates the proposed conservative fourth-power count under the weaker readout contract. Fixed nonzero bias has floor `sqrt(Bb/2)` after optimizing h; the count must not hide the required `b=O(epsilon²)` improvement.

## 6. Isolation and scope

Isolation must disable every other hopping term whose **full support** distinguishes the probed configurations, including remote bonds whose conditional coefficient depends on a probed occupation. Every environment occupation affecting `a_i` or detuning must stay frozen. Merely preparing a Z pattern and turning off adjacent bonds is insufficient. Fixed range makes the switching region finite; it does not acquire it physically. Switching-induced diagonal changes, timing and noise changes belong in the bias budget.

The extension covers real positive finite-range conditional nearest-neighbor hopping, with the specified trace, symmetry and Markovian contracts. It does not cover complex phases, extra transitions, particle nonconservation, arbitrary spatial defects, finite-temperature response or nonunital/memory noise. Model-class acquisition, small residuals, ordinary-method superiority and useful full-cycle cost remain separate tasks.

Governing corpus passages: N747 `updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/research_note.md`, lines 100–116,118–181,183–242; N765 `updates/EX/package/frontier_residual/recovered/astra_frontier_residual_response/research_note.md`, lines 66–120,122–185,187–235. The new deduction is the local parametric flow retargeting and its specific extension of those interfaces, not a reclassification of archived source status or a physical validation.
