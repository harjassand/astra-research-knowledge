# W06 notation and abbreviation audit

Scope: `outputs/ASTRA_KNOWLEDGE/01_CORE.txt` and the standalone Astra cards. This is an ingestion-safety audit only; it proposes local metadata and token repairs, not changes to mathematical claims or proofs.

## Finding

Cards generally state their interface, but the global core and many compressed cards assume a reader already knows which local type each symbol has. Because Astra retrieves cards independently and can join several in one context, symbols need card-local declarations and machine-readable typed names. Do not infer cross-card identity from glyph equality.

Highest-risk collisions:

- `D`: hybrid memory dimension (`N07`), total sum of branch dimensions (`N22`), matrix/operator named `D` (`N71`), and defect count (`N27`, `delta, lambda` nearby). It is variously an integer, a positive operator, or a count.
- `r`: affine dimension or state parameter (`N07`, `N02`), number of input copies (`N18`), squeezing parameter (`N71`), graph threshold (`N27`), rank (`N87`), and density exponent (`W-frontier-analysis`).
- `eta` / `η`: error tolerance, loss/transmission parameter, phase-accuracy parameter, or a spectral eigenvalue. In `N18`, `eta=1/kappa`; in `N74`, `eta_i` are transmissions; in `N44`, `theta` is phase size; other cards use `eta` for accuracy. Unicode/ASCII normalization can silently merge or split them.
- `E`: energy scalar, POVM/effect operator, expectation symbol, event, or error label. `N18` uses `E` as an effect and `Q` as expected input cost; `N64` uses `E` for original mean photon number and `E0` for a derived bound; `N71` uses `E0` for energy and an effect-like `E` is elsewhere in the same corpus.
- `TV`: total-variation distance, but the card often fails to state the convention (sup event difference versus half the L1 norm), and nearby `T` can be a channel/contraction or trace distance. A model may treat them as interchangeable norms without checking sample spaces or conditioning.
- Memory “dimension” and “rate” are compressed together in `01_CORE`: `D`/`Q` dimensions, bits, classical capacity, and retained register count are distinct resources. E.g. `N07` has algebra dimension `D=sum d_j`, while `N22` separates largest branch `Q=max d_j` from total `D=sum d_j`; neither is automatically a bit rate.
- Expected versus strict energy: `01_CORE` juxtaposes “EXPECTED inputcost Q” (`N18/N19`) with hard spectral support budget (`N18`) and “hard SUPPORT energy” (`N32`, `N62`). “Energy” alone does not encode expected, per-use maximum, block maximum, or support constraint. `N71` expected resetcount and `N64` conditional tail/mean-energy bounds are other distinct quantities.
- Phase scope: `N64` says arbitrary phases for an energy theorem, while `N44` assumes a supplied local phase gauge and a small entrywise phase bound; `N42` positive-kernel sampling is yet another condition. A joined summary can falsely transfer the broad phase assumption to the sampler or robustness theorem.

## Five exact examples and minimally safe readings

1. `01_CORE.txt`, line beginning `N07`: “`e_D=Theta_Theta(D^(-2/s))`”; immediately nearby it defines `s=dim aff(Theta)` and says all retained data use `D=sum_j d_j`. This is one-draw reconstruction error versus memory *dimension*. Recommendation: expose as `tv_error_min(D_hybrid, Theta)` and `affine_dim(Theta)`; never label `D` “rate” or “bits”.

2. `cards/N22-pure-branch-memory.txt`: “`Q=max branchdimension ... D=sum branchdimensions chargesalllabels`”. This explicitly distinguishes max branch quantum dimension from total branch dimension, but token adjacency can drop the distinction. Recommendation: retain named fields `branch_dim_max_Q` and `branch_dim_sum_D`; encode classical-label accounting as a separate interface field.

3. `cards/N18-cost-detection.txt`: “`H>=0 ... E=Phi*(|v><v|) ... L=-lnE`” and later “`mean input costQ=Tr rho sum_i H_i`”; `01_CORE` summarizes this as “EXPECTED inputcost Q” while separately mentioning a hard spectral `Hsum-support budget`. `E` is an effect operator, not energy; `Q` is expected cost, not a hard cap. Recommendation: `effect_E`, `expected_cost_Q`, `support_energy_cap_Qmax`.

4. `cards/N71-spectral-passive-loss.txt`: “`0<=r_j<=rmax`” (squeezing), “`nu_j=s_j(T)^2 POWER transmissions`”, “`TV(P_T,Q_T)<=...`”, and “`expected resetcount<=E0`”; later the proof line defines `D=XR^-1X-R` as a matrix. This card alone uses `r`, `D`, `TV`, and `E0` with different types. Recommendation: names `squeeze_r_j`, `power_transmission_nu_j`, `tv_distance_output_law`, `expected_reset_count`, and `matrix_defect_D`.

5. Phase transfer across `cards/N64-all-gaussian-herald-tails.txt` and `cards/N44-positive-phase-robustness.txt`: N64’s “`ANY physical finite-mode Gaussian input, arbitrary phases`” supports an energy/tail theorem; its own caveat says it “does NOT remove ... positive-kernel SAMPLING prerequisite.” N44 instead requires “`AFTER SUPPLIED local phase gauge`” and `|theta_ij|<=theta`, with RHS `<1`. Recommendation: type assumptions as `phase_scope=arbitrary_for_energy_bound` versus `phase_scope=supplied_gauge_entrywise_bound(theta)` and attach each only to its conclusion.

## Compact card-local dictionary / typed interface

Add a short header to each card, with only symbols actually used there:

```text
SYMBOLS: D_hybrid:int>=1=sum_j d_j; s_aff:int>=1=dim_aff(Theta);
         e_tv:[0,1]=inf_encoder,decoder sup_theta TV(output,theta);
DISTANCE: TV=0.5*L1 on the named output sample space; conditional/unconditional stated explicitly.
COST: cost_kind in {expected, per_use_max, block_max, support_cap}; unit and block length required.
ASSUMPTIONS: phase_scope=...; energy_scope=...; input_scope=...; shared_registers=...
```

For individual cards, do not force these exact glyphs; give stable semantic names and preserve original notation as aliases. Minimal field set for machine-first ingestion:

```text
symbols: [{glyph, ascii_aliases, semantic_name, type, unit, domain, definition}]
metrics: [{name, norm_or_distance, sample_space, conditional_on, bound}]
resources: [{name, kind, expected_or_worst_case, scope, unit}]
assumptions: [{name, value, applies_to_conclusion}]
```

Type distinctions that should be explicit: `Dimension` vs `BitCount` vs `Rate`; `ExpectedCost` vs `SupportCap`; `EffectOperator` vs `EnergyScalar`; `ProbabilityLaw` vs `Distance`; `PhaseBound` vs `ArbitraryPhase`; `MatrixDefect` vs `IntegerCount`.

## Minimal machine-first glossary

```text
Dimension := positive integer, with object named (Hilbert, algebra, branch-max, branch-sum).
BitCount := number of encoded classical bits; do not derive from Dimension without a stated code.
Rate := asymptotic bits/cost or bits/use with limit and cost convention stated.
ExpectedCost := E[cost] under specified input/randomness and block.
SupportCap := almost-sure spectral/support constraint; not implied by ExpectedCost.
EnergyScalar := numeric first moment in named units; EnergyOperator := self-adjoint H.
EffectOperator := operator 0 <= E <= I; never alias to EnergyScalar E.
TVDistance(P,Q) := 0.5 * sum_x |P(x)-Q(x)| on declared discrete space (or corresponding measure norm); state conditional status.
PhaseBound(theta) := supplied gauge plus per-entry |phase| <= theta; not synonymous with arbitrary phase.
SqueezeParameter(r) := Gaussian squeezing; Transmission(nu) := power transmission; distinct dimensions/types.
```

## Compact-token hazards

The concatenated prose (e.g. `EXPECTEDinputcostQ`, `UNIFORMTV`, `HARDsupport`, `AFTERSUPPLIEDlocalphasegauge`, `NOinverseheraldprob`) is readable to a domain expert but is a poor token interface: segmentation is inferred rather than encoded, and a model can attach an adjective to the wrong claim. Preserve compact display text if needed, but add structured sentence boundaries or semicolon-delimited fields: `COST_KIND=expected; COST_SYMBOL=Q; COST_DEF=Tr(...)`. Keep Greek and ASCII aliases together (`η|eta`, `θ|theta`, `ε|epsilon`) and never use a raw symbol as a database key.
