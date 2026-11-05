# Exact compiler, positive lift and the scope of the supplied checks

This is a navigation map for the supplied [complete manuscript](package/MANUSCRIPT.md), not an additional Capital proof audit. The governing theorem and physical-model scope are on the [main result page](README.md).

## Effective finite model

Appendix A compiles the machine/input into a finite labelled Wang set whose finite nonzero-edge components are accepting rectangles with one marked anchor. A finite accepting component exists exactly when the machine halts. A folded radius-one update and explicit finite row automata avoid assuming a cleanup trajectory or importing noisy computation.

For t tile types, choose finite binary group G with enough characters for edge labels, `C0=10000(t+1)` and multiplicity `D=C0+t`. Two physical spins s,r, stored group-edge variables and a multiplicity variable give site alphabet `4D|G|^2`. The local factor uses `F=sum_z Chi_z I_z`, with I_z enforcing spin equality only at a marked anchor. Multiplicity energy is 0 or 1 according to the explicit threshold `b<=C0+F`; each Ising layer has mismatch cost 6.

At beta=1, summing multiplicities gives `C(1+aF)`, where `C=C0+t exp(-1)` and `a=(1-exp(-1))/C`. This factor comes from finite integer energies, not a prescribed noninteger coupling. The bounds `at<1e-4` and `16 exp(2)ta<.012` give the stated auxiliary mixing/polymer margins.

Appendices B–C establish the exact finite Fourier identity: free dangling-edge integration yields a positive hard-core gas of accepting rectangles with activities `a^|gamma|` and equality indicators at anchors. Invalid tableaux have zero summed Fourier contribution. Infinite dual supports are not simply asserted absent.

## The all-state argument is essential

Appendix D uses uniformly mixing conditioned group variables and local partition ratios to identify **every physical Gibbs spin marginal** with the induced summable interaction and to construct its canonical positive lift. Appendix E supplies pressure comparison and entropy-preserving recoloring of infinite FK components, then uses the precisely stated equilibrium-to-Gibbs direction. This yields the needed conditional bond domination for original translation-invariant laws; ordinary finite-volume FK bounds with fixed opposite colours would not suffice.

Appendix F supplies common lower percolation, the accepting-anchor merger, and exact finite disagreement-component swaps. It controls exchange-odd correlations with constants independent of how late the first accepting rectangle appears. The nonhalting branch has an empty finite-polymer family and exactly the two uncoupled Ising spin specifications. These analytic steps, rather than extrapolation of small examples, support the infinite-volume conclusion.

## Recorded evidence, without replay

| Supplied receipt | Stated scope |
|---|---|
| [Tableau grammar](package/checks/explicit_tableau_grammar_results.json) | 84 width/height cases over seven example machines; small-box assembly/status-pattern and ancillary identities |
| [Independent folded-machine oracle](package/checks/folded_machine_results.json) | 160 random two-symbol three-state machines, 923 trajectories and 21,532 exact state/tape comparisons, with bounded 120-step prefixes |
| [Final constants](package/checks/final_constants_results.json) | Exact rational margins, including the analytic all-integer-distance bound `10(0.03)^R`; not merely a finite distance sweep |
| [FK/merger algebra](package/checks/fk_merger_algebra_results.json) | Finite partition identity, 6,144 horizontal conditionals, 1,536 insertion ratios and 5,632 component swaps; no independent infinite-volume certification |

The original [runner](package/run_checks.py) and four scripts remain available with their saved outputs. Capital did not run them. Internal review completion is credited as reported in the [README](package/README.md) and manuscript status section; no separate external referee or machine-proof artifact is invented. Source transport hashes establish preserved files, not a new scientific audit. [Original package and provenance](SOURCES.json).
