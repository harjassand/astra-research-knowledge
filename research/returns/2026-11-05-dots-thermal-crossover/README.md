# Finite-size crossover without a computable general stopping bound

This supplied addendum is **conditional on the provisional base proof** of [fixed-temperature exchange-odd undecidability](../2026-11-05-dots-thermal-fourier/README.md). It reports a completed independent internal audit of its boundary, averaged-DLR, quantifier, nonuniqueness and pressure arguments, with no fatal issue found. It does not independently verify the base theorem or claim external peer review/formal verification.

Read the complete [note](package/NOTE.md), [source/assumption record](package/SOURCES.md), [original ZIP](original/thermal_crossover_addendum_20261105.zip), [visible return](DOTS_THERMAL_CROSSOVER_ADDENDUM_20261105_RETURN.txt), [other corollaries](other-corollaries.md) and [provenance](SOURCES.json). Its recorded base-manuscript SHA256 is `42b57bfe3212e57db34803dc4f6af6875d5d8a6d3e38f9244958c38a31f0dc0c`; the supplied base ZIP contains manuscript hash `825b1bfc2cfa7984c23bae25770355bbf309ae88d5478111c50be70f97dd1b89`. Both supplied packages are preserved unchanged. Exact base-version identity is not established, and no unprovided version or equivalence is reconstructed.

## Specified finite equilibrium experiment

In an L by L square, fix exterior layer spins to plus/minus, include site factors centred inside the square, and **sum dangling group edges freely**. No exterior-centred tile factors are included. A fixed-width collar embeds this open/mixed-boundary gas in the full physical configuration space. It is not silently identified with a full fixed-exterior DLR kernel on exactly that square; full physical DLR equations hold for interior update sets away from the collar.

Let `m_M(L)=L^-2 sum_v E[(s_v-r_v)/2]`. It is a uniformly computable finite partition-sum statistic, without an efficiency claim. If no accepting rectangle fits, the **entire finite spin marginal** is exactly two independent low-temperature Ising boxes with opposite boundaries. It is not a claim that all auxiliary variables or Hamiltonian descriptions are indistinguishable.

The supplied conclusions are:

- Nonhalting gives `m_M(L)>.9999999` at every size.
- A halting input has `m_M(L)->0`, though it has the same exact high-order plateau until an accepting rectangle fits.
- If the machine halts after T transitions, the first possible fitting side is at least `max(2,T+1)`; tape width can require more.
- No **total computable function of the compiled description** can bound the eventual crossover index for all halting inputs, or even their first crossing below 1/4.

The zero limit uses translation-averaged finite-box measures: every subsequential limit is a translation-invariant physical Gibbs state, with collar error vanishing as boundary/volume. It does not assume a centred boundary-state limit is translation invariant or m_M(L) is monotone.

## Computability quantifiers and costs

The proposed bound must be total on all compiled inputs; its guarantee is required on halting inputs. Partial procedures allowed to run forever for nonhalting machines are not excluded. A total bound would permit either finite partition-sum discrimination with a fixed numerical gap or finite accepting-tableau search, deciding halting. No exact eventual-tail index or its partial computability is asserted.

Alphabet size and description grow with the programme. At a **fixed** alphabet and bounded energy/support tables, finitely many instances have a finite maximum crossover. The theorem excludes a computable envelope as descriptions grow, not arbitrary delays inside one fixed alphabet. Busy-Beaver reindexing must retain compiler-size overhead.

The machine-independent infinite-volume odd bound `10(0.03)^distance` therefore does not give a computable finite-size stopping certificate for this boundary experiment. It does not prove a Monte Carlo mixing-time law, physical preparation/sample-complexity bound, arbitrary-boundary strong spatial mixing or arbitrary-perturbation robustness. It supplies no finite-observation hypercomputer or laboratory material prediction.

[Saved checks](package/numerical_checks.json) certify rational contour inequalities/decision margins and enumerate single-layer plus-boundary Ising squares of sides 1–4 with floating sums. They do not establish the base theorem, halting behaviour or asymptotic crossover numerically. Earlier quantum size-driven transitions and uncomputable phase diagrams are credited; the general idea of finite-size deception is not renamed new. No programme, new audit or large retrieval build was run for publication.
