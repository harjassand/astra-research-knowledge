# Compressed stabilizer-character contacts: asymmetric two-species KP repair

2026-11-02. Derived with root's multiscale adjoint idea. **Exact pairing identity and quantitative contact estimates**, conditional only on the declared decoder lift/charge bounds and actual local filling theorem. This resolves the polynomial-filling-volume KP obstruction for scalar stabilizer-character sources; it does not alone prove the full time-dependent source gas.

## 1. Exact character without expanding a filling

Let B be the data Pauli word of a spatially small closed source. Strip its scalar phase so B acts as +I on the code space; by distance, it is then a stabilizer. Let tau be a valid defect polymer syndrome. The canonical correction has the exact decomposition

  D(tau)=c_pre(tau)+sum_{i=0}^{r-1} J^1_{0:i} c_i(tau)
                     +J^1_{0:r} c_terminal(tau),

with fixed common lift maps, and syndrome(D(tau))=tau. Use the appropriate binary symplectic pairing (or opposite CSS dot product). Then the syndrome character is exactly

  chi_B(tau)=(-1)^[B,D(tau)]
    =(-1)^{[B,c_pre(tau)]+sum_i [B_i,c_i(tau)]},
  B_i=(J^1_{0:i})^* B.                                  (C1)

Here star means the adjoint for the chosen pairing, not necessarily the bare transpose in a nonstandard cochain basis. In standard opposite CSS coordinates it is the transpose map. The prepass and terminal terms are included, not dropped.

Proof: D(tau) maps the vacuum syndrome sector to tau. Conjugating B through D(tau) gives its eigenvalue in that sector. Bilinearity and the decoder decomposition give (C1). This uses no chosen physical stabilizer filling.

## 2. Honest adjoint growth constant

If the row-weight norm of each complete macrostep lift is at most K_adj, then

  |supp B_i|<=C |supp B| K_adj^i.

The existing physical correction lift bound usually controls COLUMN weight, not row weight. Do not silently identify K_adj with K_lift. Bounded forward/reverse fixed dependency multiplicity supplies a finite uniform K_adj, but its actual value must be admitted. This distinction changes constants, not the summability below.

For a source containing m bounded-support labels, |supp B|<=b_D m. Intermediate macrostep layers and the bounded physical prepass change only fixed constants.

## 3. Thermal roots at height i are exponentially rarer

Let a defect polymer gamma have base mass M and activity z_gamma=e^{-B_th M}. A nonzero correction coordinate at level i requires a nonzero input in its charged component. Componentwise macrostep contraction and ancestor closure imply

  M >= c_h 2^i-C_h.                                    (C2)

Only actual nonzero correction coordinates count. A zero halo vertex at height i is NOT enough; using (C1) automatically excludes it. Fixed offsets for intermediate layers and the terminal bag are absorbed into c_h,C_h.

The exact trace-polymer gas gives at most A^M labeled polymers of mass M through a fixed ambient vertex. For a charge a_D M and B_th>a_D+log A, therefore

  sum_{gamma: c_i(gamma)[x] nonzero} z_gamma e^{a_D M}
     <= C exp[-c 2^i].                                (C3)

This is a rooted high-level density estimate, not an assumed spatial correlation bound.

## 4. Source-to-defect KP row is linear in SOURCE mass

Let the pair factor be h(B,gamma)=chi_B(tau_gamma), so |h|=1 and |h-1| is 0 or 2. If h differs from 1, at least one nonzero pairing contact in (C1) occurs. Mark one such contact and use a union bound. Equations (C2)-(C3) yield

  sum_gamma z_gamma e^{a_D M} |h(B,gamma)-1|
    <= C m sum_{i>=0} K_adj^i exp[-c 2^i]
    =: L(c,K_adj) m.                                  (C4)

The sum is finite for every c>0 and every fixed K_adj. Moreover L tends to zero as B_th grows, with local constants fixed. Thus it can fit a linear source charge a_S m at sufficiently low temperature.

This replaces the incorrect source-row estimate proportional to defect density times a polynomial filling volume m^p.

## 5. Defect-to-source KP row uses the OLD filling bound

For this reverse row, do NOT invert the high-level lift. Use the actual local filling theorem: a closed stabilizer word supported on a connected m-label cluster has a check filling inside a polynomial-radius neighborhood of that cluster. If chi_B(tau_gamma) differs from 1, this filling meets some occupied BASE check of gamma.

Fix one such base check y and source mass m. Bounded physical geometry and the polynomial filling radius put the source's canonical physical anchor within a polynomial(m) neighborhood of y. At each anchor, bounded-degree connected-label counting gives at most C_S^m possible label clusters (including their finite local decorations). Hence, for source activity majorant q^m and source charge a_S m,

  sum_sources |z_S| e^{a_S m} |h(S,gamma)-1|
    <= C M sum_{m>=1} poly(m) [C_S q e^{a_S}]^m.        (C5)

This fits a linear defect charge a_D M for sufficiently small q. Polynomial filling is harmless in THIS row because it is summed against q^m. It was not harmless in the source row.

If the local filling theorem is phrased in physical radius rather than label mass, connectedness of the used-label cluster gives radius O(m); the bounded-dimensional physical geometry converts the polynomial radius into the polynomial anchor count used above. Bath-only and identity data words have trivial h and need no such count.

## 6. Same exact interaction, different majorants

There is no requirement to estimate both KP rows using the same contact footprint. The exact pair factor h=chi_B(tau) is defined once. Formula (C1) supplies the upper-row multiscale contact cover; the local filling supplies a different cover for the reverse row. Both are valid implications of h!=1. Their asymmetry is the point of the construction.

With defect hard-core incompatibility already paid by part of a_D M, and source hard-core/source-clock interactions separately budgeted, (C4)-(C5) give a genuine two-species KP admission for scalar character sources. No exp(c m^p) external-background penalty is introduced.

## 7. What remains before claiming the annealed perturbation gain

A normalized quantum source representation must still supply scalar activities with the annealed beta-v bound and show that every remaining defect interaction is exactly the character factor above (or additional interactions with independently controlled rows). Time-dependent syndrome switching, source-owned holes, endpoint clock pins, and source-induced changes of canonical trace components cannot simply be dropped. This lemma fixes one formerly fatal normalization obstacle; it is not the whole normalized mixed-gas theorem.
