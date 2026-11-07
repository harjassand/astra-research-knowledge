from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'principal'
def take(text,start,end=None):
 a=text.index(start);b=text.index(end,a) if end else len(text);return text[a:b]
head='''# Constructed collective information for new preparations and drives

Research dossier, 7 November 2026. **The broad requested breakthrough remains OPEN / NOT ACHIEVED.** No historical priority, physical validation or practical advantage is asserted.

## 1. Strongest result actually achieved

We obtained an acquired collective predictor for a specified class of interacting block populations, including nonconvex collective energies and very slow phase switching. Its error can be bounded without the inverse macroscopic relaxation gap. Positive kinetic estimates plus a mass-metric repair allow reliable predictions at all frozen-control horizons without calibration precision proportional to an exponentially rare transition rate. The predictive object contains count-resolved positive rates and equilibrium weights, rather than an unknown many-body functional. Within the explicit access model it is constructed once and evaluated for new permitted preparations and drives without performing their target experiment or solving the microscopic state again.

The scientific principle established at this scope is: **retain the slow collective sector; control discarded kinetic fluctuations relative to collective dissipation; acquire positive conditional rates and masses; then propagate a finite stochastic law with the appropriate common-metric, mass-metric or finite-horizon certificate.** The relative-energy certificate is derived for the physical class, not simply postulated for arbitrary matter.

This does NOT establish a general representation-discovery theorem or a new law of generic interacting matter. The successful class has supplied count coordinates, controlled internal mixing and strong local calibration rights. Strong collective interactions are allowed; arbitrary strongly interacting discarded sectors are not proved tractable. The retained spatial field can itself remain hard to evaluate. The strongest equal-information incumbent can use established conditional averaging, reversible-network methods and coarse kinetic Monte Carlo. Superiority over that incumbent has not been shown.

The main complete theorem is Part A below, with its exact physical, preparation, noise, source-warmness and control assumptions. Part B repairs estimated stationary weights. Part C derives interacting-shell conditional acquisition and its resource bounds. Part D expands thermodynamic drives and constructs noisy preparation. Part E proves numerical evaluation costs. These contracts are distinct: one must not combine their conclusions while dropping their additional hypotheses.

### The resulting operation

For N binary sites in B blocks, the acquired descriptor is a finite positive mobility/conditional-rate table, count-shell weights or their ratios, geometry, and calibrated uncertainty bounds. A query supplies a computable permitted collective energy, kinetic protocol, initial count law/source certificate and bounded count observable. It returns an expectation interval (or a probability interval for an effect), clipped to its physical range. A single acquisition event covers adaptive selection of numerical queries satisfying the budgets; this does not grant arbitrary measurement-feedback control of the physical dynamics. Monte Carlo evaluation adds its own per-query failure budget; physical fluctuations are separate from epistemic uncertainty.

At a fixed number of blocks, q=product_r(m_r+1) is polynomial in N, so frozen-generator evaluation is polynomial in q, log(T+1), input bits and requested numerical precision. At growing B the full count grid is exponential. Ordinary sparse coarse trajectories are polynomial in T, not log T. The theorem does not conceal a large coarse solve inside the word collective.

For all residual W_r identically zero, known energies and a common equilibrium law, if z=sqrt(C_c/gamma)<1 and the learned positive mobility table has relative error eta<1, every bounded retained readout from an ideal source of L2 Gibbs warmness W has error at most

W[z/(2sqrt(1-z))+eta/(2sqrt(1-eta))]+2 zeta_source+epsilon_eval.

This holds for all horizons and arbitrary prescribed kinetic protocols preserving that law. The explicit derived C_c is independent of total block number and block sizes; gamma is the physical conditional swap gap. Changing thermodynamic fields has a bounded-action theorem, or a separate finite-horizon/arbitrary-source theorem. Unknown empirical masses use the autonomous repair in Part B; they do not automatically inherit arbitrary switched common-metric control.

An additional relative mean-lifetime theorem handles a count target from Gibbs conditioned on its ENTIRE transient complement. It can certify an exponentially large mean with polynomial kinetic precision. It does not turn TV-only preparation error into relative accuracy of an unbounded hitting observable. Part D supplies the stronger noisy-source repair and charges its growing pin energies.

### Scientific status

- PROVED at stated finite-state assumptions: relative-energy and mass-metric lemmas, volume-independent fluctuation bound, exact count-rate synthesis, finite-noisy table acquisition, finite-horizon reuse, thermodynamic-action reuse, noisy pin writer, killed Schur and relative mean-lifetime comparison, stochastic numerical evaluation.
- CONDITIONAL ON AN ACTUAL QUANTITATIVE GAP/APPARATUS CERTIFICATE: efficient interacting-shell acquisition beyond the uniform-shell model. The primary high-temperature Kawasaki theorem supplies a class; it does not supply generic low-temperature mixing.
- OPEN: discover sufficient variables for general short-range strongly interacting matter; obtain generic efficient conditional kinetics; preserve efficient accuracy under extensive changing fields and growing independent controls; efficiently evaluate a growing noncontractive collective field at rare-event horizons.
- UNKNOWN: historical novelty of the particular composition and estimates. NOT ESTABLISHED: consequential matched practical advantage or the larger foundational capability.
- Physical experiments performed: zero. All numerical records below are synthetic checks supplementing analytic proofs.

Earlier Gibbs, thermal-memory and P1/P2/P3 capital remains intact at its recorded scope. No theorem from it is a load-bearing premise here. The Astra retrieval connector was unavailable; local pinned records and primary literature were used. This dossier is a research return, not a manuscript or publication instruction.

## 2. Reading and dependency map

The main mathematical dependence is finite reversible Markov dynamics -> conditional count projection -> a derived local fluctuation inequality -> gap-free evolution comparison. Known exclusions supply the actual conditional graph gap. Statistical calibration supplies positive kinetic coefficients. Estimated masses require the separate contour proof. No Mori–Zwanzig closure, a learned neural functional or an unspecified orthogonal propagator is imported as a computational oracle.

Full derivations and independent challenges are retained in the supporting record. Parts A–E reproduce the load-bearing proof developments. Independent alternatives, exact primary-source review, obstructions and the unresolved frontier follow them. The initial reports are preserved without retroactive editing; a brief principal-result description reached the constructor before its written freeze, after it reports having formulated its own route. This boundary is disclosed in the record and is not described as four sealed written returns.

'''
a=(p/'RELATIVE_ENERGY_CONSTRUCTION.md').read_text()
a=a[a.index('## 1. Nonautonomous'):]
a=a.replace('Caputo-Liggett-Richthammer, Theorem 1.1 and section 4.1.1 (0906.1238v3)','Caputo-Liggett-Richthammer, Theorem 1.2, Corollary 1.3 and section 1.2.3 (0906.1238v3)')
b=(p/'MASS_METRIC_REPAIR.md').read_text().split('\n',2)[2]
b=b.replace('candidate proof for independent checking; not frozen initial. No priority claim.','proof independently checked by the three reviewers; not part of the frozen initial. No priority claim.')
b=b.replace('Proposed gap-free bound:','Checked gap-free bound:')
b=b.replace('this integral is <1 (e.g. 1/r<=1 for r>=1 yields bound 2exp(-.5)>1, so need split or use direct value <.56).','this integral is <1: split at 2 to obtain at most 2exp(-1/2)-exp(-1)<1.')
c=(root/'machinery/FOLLOWUP.md').read_text();c=take(c,'## 3. Residual microscopic interactions','## 7. Scientific status')
d=(root/'auditor/REVIEW_RELATIVE_ENERGY.md').read_text();d=take(d,'## 6. New constructive extension','## 9. Physical and computational accounting')
e=(p/'EVALUATION_AND_PREPARATION.md').read_text();e=take(e,'## Positive scaling','## Preparation note')
parts=[head,'# Part A. Main explicit construction and proofs\n\n',a,'\n# Part B. Estimated stationary masses: autonomous repair\n\n',b,'\n# Part C. Interacting conditional shells and acquired weights\n\n',c,'\n# Part D. Thermodynamic controls and physically specified noisy preparation\n\n',d,'\n# Part E. Certified numerical evaluation\n\n',e]
parts += ['\n', (p/'OVERVIEW_SUPPORT.md').read_text(), '\n# Part H. A genuinely local constitutive operation\n\n', (root/'constructor/FOLLOWUP.md').read_text(), '\n# Part I. Certified adaptive primal-dual compilation\n\n', (root/'constructor/DUAL_ADAPTIVE_BRACKET.md').read_text(), '\n', (p/'TRANSPORT_PRIORITY.md').read_text(), '\n', (p/'EVIDENCE_AND_FRONTIER.md').read_text()]
(p/'DOSSIER_DRAFT.md').write_text(''.join(parts))
print((p/'DOSSIER_DRAFT.md').stat().st_size)
