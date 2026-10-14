# Proof and checker record

This note records the independent argument and the finite checks used in `REPORT.md`. It does not elevate finite replay to a general proof or external validation.

## Exact source comparison

For a reversible heat-bath edge `x <-> y` with reference masses `m0x,m0y`, common edge attempt `a0`, and true endpoint masses proportional to `m0x wx,m0y wy`, the symmetric conductance is proportional to

`(a/a0) * (m0x+m0y) wx wy / (m0x wx + m0y wy)`

relative to the reference conductance. The bracketed mass ratio is at least one because

`(m0x+m0y)wxwy - (m0xwx+m0ywy) = m0x wx(wy-1)+m0y wy(wx-1) >= 0`.

It is at most `Rm` because

`Rm(m0xwx+m0ywy) - (m0x+m0y)wxwy = m0xwx(Rm-wy)+m0ywy(Rm-wx) >= 0`.

Multiplying by `a/a0 in [1,Rk]` gives `[1,Rm Rk]`. A reaction conductance with fixed reaction coefficient scales by `w`, hence is in `[1,Rm]`. Adding these forms proves `C <= A <= R C` for this model. The comparison presupposes the same positive support and the stated pointwise envelopes; it does not infer either envelope from transcripts.

With `r=w-Av`, symmetry gives

`<w,A^-1 w> - (2<w,v>-<v,Av>) = <r,A^-1r> >= 0`.

If `C >= alpha I` and `C <= A`, the remainder is at most `||r||^2/alpha`. For two source vectors, bilinearity gives the corresponding cross remainder `<r1,A^-1r2>`. The contraction `||2 alpha A^-1-I|| <= 1` yields center `<r1,r2>/(2alpha)` and radius `||r1||||r2||/(2alpha)`. All norms/square roots in the independent rational fixtures were bounded outward.

## Finite exact fixtures

`independent_check.py` builds an explicit 16-state pairwise reversible model with positive degree-two clock coefficients, a one-site reaction, and an independently constructed local-product reference. It checks detailed balance, the mass/source normalization, pointwise mass and clock ratios, every flip/reaction conductance, exact rational semidefinite form positivity, exact inverse mean, residual brackets, and a point-source cross certificate. PSD checks use exact rational symmetric elimination with positive pivots; there is no float eigenvalue claim in the result.

The result has `Rm=9/4`, `Rk=10/7`, `R=45/14`, `alpha=7544/32931`, and `Z=145/92`. The exact mean is `1193860868651309676743490382851080680889/381256366133273907987612643025618850087`. The exact mean lies in the independently recomputed equilibrium residual interval. The exact point-source response lies in the two-solve interval. The degree-two recovery checks all eight Boolean contexts from seven sampled contexts.

`reverse_query_check.py` reparses both A/B source transcripts using exact rational arithmetic. It independently reconstructs 172 pairwise energy observations, all 2,772 downhill rates per model, every reverse conversion, all degree-two coefficients, preparation flags, and `a/2 <= d <= a`. Recovered support tables are fully enumerated only for the observed small supports (maximum 3 in B); this is not a general dense-support algorithm.

`finite_response_check.py` solves the normalization-plus-response correction equations exactly for the four-rate example and verifies exact equality of every response and positivity of all old weights. Its proof extension for any finite set of positive shifts uses invertibility of the Cauchy/normalization matrix and bounded corrections as the hidden rate tends to zero.

`countermodels.py` exactly compares a baseline and a cubic-modified clock law; degree-0/1/2 context observations and all energy readings agree. It also checks the two preparation-clock models with the same prepared downhill observation and different free means. Both examples deliberately violate a premise needed by the conditional acquisition result.

## Owned producer-copy checks

Selected producer code and fixtures were copied to `source_copy/`; the original packet is untouched. The copy used an explicit `allow_pickle=False` on NumPy archive loads. The four 16-/64-state fixtures passed the listed exact checks. Full A/B/tensor transcript-only replays preserved the stored lower endpoints. Because SciPy was unavailable on this host, only the floating proposal step used NumPy in place of SciPy; exact rational certification was retained. The new positive-vector witnesses gave slightly different upper strings but each new exact interval passed the copied checker.

The owned test results are finite independent arithmetic, not proof-assistant output, external review, or physical evidence.
