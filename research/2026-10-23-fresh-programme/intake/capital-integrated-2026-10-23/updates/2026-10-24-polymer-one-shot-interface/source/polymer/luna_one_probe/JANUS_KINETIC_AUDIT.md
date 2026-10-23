# Janus DA-to-thiol-M one-shot kinetic audit

This is a finite-state kinetic check, not a material-capability claim. No rates below are fitted to an experiment. The numerical values in the executable check are illustrative only.

## Model and exact formulas

Use transient states `D` (closed DA), `U` (opened/unlocked), and absorbing `L` (locked). The transitions are

```text
D --k_-→ U,     U --k_F→ D,     U --k_S→ L,
```

with nonnegative rates and `K = k_F + k_S`. Starting in `D`, the transient probabilities obey

```text
dD/dt = -k_- D + k_F U
dU/dt =  k_- D - K U
dL/dt =  k_S U.
```

The two decay rates are the nonnegative roots

```text
λ± = (k_- + K ± sqrt((k_- + K)^2 - 4 k_- k_S))/2,
```

and, for distinct roots, the exact probability of not yet locking by time `t`, conditional on starting in `D`, is

```text
S_D(t) = D(t)+U(t)
       = [λ+ exp(-λ- t) - λ- exp(-λ+ t)]/(λ+ - λ-).
```

When the roots coincide, the continuous limit is `S_D(t)=exp(-λt)(1+λt)`. This includes `k_F=0` and `k_-=k_S=λ`. If `k_-=0` or `k_S=0`, there is no path from the initial state to `L`, and `S_D(t)=1`.

From `U`, the probability that the *first* exit is locking within a contact interval `τ` (so this excludes a `U→D` return followed by reopening) is the competing-risks integral

```text
P(first exit is L by τ | start U)
  = ∫₀^τ k_S exp(-K t) dt
  = β(1-exp(-Kτ)),       β = k_S/K.
```

Thus a target direct-lock probability `p` is possible exactly when `β>p` and `Kτ ≥ -log(1-p/β)`. At fixed `k_S`, optimizing over `k_F≥0` cannot exceed `1-exp(-k_S τ)`: the expression is increasing in `β∈(0,1]`, and its maximum is at `k_F=0`, `β=1`. Consequently a necessary rate-capacity condition is `k_S τ ≥ -log(1-p)`.

## Storage/repair feasibility

For an intact seam stored for finite time `T_s`, the exact kinetic requirement for locking probability at most `ε` is

```text
1 - S_D(T_s; k_-^I,k_F^I,k_S^I) ≤ ε.
```

For a recontact interval `τ_R`, requiring direct lock probability at least `p` is

```text
β_R [1-exp(-K_R τ_R)] ≥ p,
β_R = k_S^R/(k_F^R+k_S^R),  K_R=k_F^R+k_S^R.
```

These two inequalities are a finite-time feasibility test; they involve separately measured intact and recontact rates. If the chemistry has the same `k_S` in both conditions, attaining branch fractions `β_I` and `β_R` requires the rate contrast

```text
k_F^I/k_F^R = [β_R/(1-β_R)]/[β_I/(1-β_I)].
```

The contrast can be attributed to a cage/access change only if that change independently alters the measured `k_F` (or another rate); the kinetic algebra does not establish such a change. With identical rates in intact and recontacted conditions, `β` is identical, so making direct first-exit locking likely also makes locking during storage more likely. In particular, as `τ_R→∞`, the repair probability tends to `β`; the same `β` controls the slow storage hazard when `k_-≪K`.

The exact storage survival also gives useful bounds. Put `A=λ+/(λ+−λ-)` for distinct roots. Then

```text
exp(-λ- T_s) ≤ S_D(T_s) ≤ A exp(-λ- T_s).
```

The left inequality is sufficient for low-risk design: `λ- T_s ≤ -log(1-ε)` implies storage locking risk at most `ε`. The right inequality gives a necessary condition `A exp(-λ- T_s) ≥ 1-ε`. When `k_-≪K`, `λ- = k_- β + O(k_-²/K)` and `A≈1`; after the fast `K^{-1}` transient, the approximate storage risk is `1-exp(-k_- β T_s)`. Use the exact `S_D` condition when checking a proposed rate set.

## Executable check

Run:

```sh
python3 work/next_unit/polymer/luna_one_probe/check_janus_kinetics.py
```

The script compares the eigenvalue expression against an independent RK4 integration, checks the repeated-root and no-lock boundaries, verifies the direct first-exit formula and an exact rational odds-contrast identity, and evaluates one explicitly illustrative finite storage/recontact pair. Its sample values give intact storage lock risk `9.9995e-05` over `100000` time units and recontact direct-lock probability `0.935903` over `20` time units. These are algebraic fixture outputs only, not evidence of a real chemistry meeting either target.
