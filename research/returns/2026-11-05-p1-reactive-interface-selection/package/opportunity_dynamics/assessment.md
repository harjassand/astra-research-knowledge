# Mechanics opportunity assessment

## Decision

Reject this branch as the main discovery target in the present assignment. The acquired data make a strong, reproducible case that granular mechanical memory depends on deformation direction and path. This is already the central finding and interpretation of the primary paper. The measurements do not identify a transferable stress constitutive law or a new control operation. A second lead, slow cyclic aging across disordered solids, also has a recent geometric interaction model that already explains the reported behavior.

This is a grounded rejection of these two openings, not a claim that general constitutive prediction of disordered solids has been solved.

## Exact acquired object and provenance

The main object is a set of particle and boundary coordinates from low-friction, two-dimensional hydrogel sphere packings subjected to cyclic strains along two independently controlled directions. The public dataset is Chloe W. Lindeman's `shear-cell-data`, tag `v1.1`, archived as DOI 10.5281/zenodo.15367435.

- Repository: https://github.com/cwlindeman/shear-cell-data/tree/v1.1
- Archive: https://zenodo.org/records/15367435
- Primary article: Chloe W. Lindeman, *Multi-dimensional memory in low-friction granular materials*, Soft Matter 21 (2025), 4890–4897, DOI https://doi.org/10.1039/D5SM00470E
- Downloaded full preprint: *Multi-dimensional memory in sheared granular materials*, https://arxiv.org/abs/2407.14966 ; the downloaded PDF is the July 2024 v1 and therefore is not a byte-equivalent substitute for the final 2025 article.

I downloaded 147 raw CSVs, totaling 5,557,461 bytes, and the author's analysis script. The manifest records the selected preparations and source Git blob hashes. All 147 raw files match the manifest hashes; independent SHA-256 hashes are recorded in `reproduction_results.json`. All 27 selected preparations analyzed successfully. The script executes the relevant functions from the author's code, then computes descriptive preparation-level summaries.

The reported displacement is the mean Euclidean nonaffine particle displacement, divided by box size. Although an internal variable is called RMS, the implementation averages displacement norms rather than their squares. The analysis corrects affine box deformation by the fitted boundary matrix and subtracts global translation.

## Decisive quantitative comparison

The cleanest comparison is SB readout after SB training, SA training, or no training. Each group contains five independently prepared packings. The two trained groups received almost the same measured peak strain: mean 0.05173 for SB and 0.05160 for SA. Their readout cycle-3 peak strains were 0.05135 and 0.05050, respectively; control readout mean was 0.05061.

| Preparation | Number | Cycle-3 mean nonaffine displacement / box size | Ratio to matched training |
|---|---:|---:|---:|
| SB training, SB readout | 5 | 0.00109140 | 1.000 |
| SA training, SB readout | 5 | 0.00644784 | 5.908 |
| No training, SB readout | 5 | 0.01153572 | 10.570 |

Every matched-training preparation has a lower cycle-3 displacement than every orthogonal-training preparation and every control preparation. An exploratory exact Mann–Whitney comparison gives two-sided p = 0.00794 for either comparison. This is descriptive evidence across a small, protocol-blocked collection, not a fully randomized causal effect estimate.

The full curves and preparation-level values are in `reproduction_results.json`, with a compact CSV and `granular_reproduction.png`. The effect decisively defeats a scalar maximum-amplitude-only description of the state. It does not defeat models that already track anisotropy, plastic rearrangement state, or deformation paths.

## Why the apparent gap does not survive

The article explicitly interprets its experiments as learning trajectories in multidimensional strain/configuration space. In the 2024 preprint, alternating training and loop training/readout show that the response depends on the path rather than merely on the final strain direction or a maximum amplitude. Calling this discovery a noncommutative mechanical memory representation would rename the reported phenomenon without providing a stronger mechanism or construction.

The strongest explanation available in this experiment is its own learned-path/limit-cycle account, together with the existing interacting rearrangement and cyclic training literature. This is more demanding than a scalar-amplitude baseline. We have not established a quantitative model beating those physical accounts.

One must distinguish protocol versions. The downloaded March 2025 alternating-training records have mixed readout and a different training amplitude from the mixed-loop group. They must not be interpreted as a clean equal-amplitude replication of the alternating-training/SB-readout experiment depicted in the July 2024 preprint. Two mixed-loop preparations contain only six stroboscopic boundary frames, from which cycle peak strain cannot be recovered. The script reports those peaks as missing rather than inferring them.

The local cycle-3 cusp contrast, (D2+D4)/2-D3, has broad preparation-level 95% t intervals that include zero in the selected small groups. This does not refute the qualitative path-memory result; it prevents claiming a precisely established universal cusp law from this subset. The large matched-versus-orthogonal displacement contrast is the robust numerical result.

## Relevant limitations

The system has 34–37 particles, roughly five training cycles, and destructive readout at sufficiently large amplitudes. There are no measured force or stress trajectories in this selected dataset. It cannot identify a general stress constitutive closure, durability law, or physical-time optimal control policy. Rate effects are explicitly outside the preprint's scope; hydrogel friction can relax and particles can dry over laboratory time.

The apparatus itself exhibits memory and finite residual boundary strain. These are acknowledged and investigated in the article. They should not be asserted to explain away all particle memory: the analysis removes affine boundary deformation, and the authors report particle memory in cases without the same box-memory signature. Nevertheless, apparatus and friction state must be part of any future transferable quantitative account.

Particle correspondence is nearest-neighbor based. The implementation does not impose a global one-to-one assignment, although the author reports near-complete tracking fidelity. We did not manufacture a new tracking correction or treat a possible tracking problem as established evidence against the experiment.

## Second lead: cyclic aging is already mechanistically addressed

The second primary study is Dor Shohat, Paul Baconnier, Itamar Procaccia, Martin van Hecke and Yoav Lahini, *Aging of amorphous materials under cyclic strain*, PNAS 123(8) (2026), e2515075123, DOI https://doi.org/10.1073/pnas.2515075123 . Full sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC12933069/ and https://arxiv.org/abs/2506.08779 . Its replication archive is https://zenodo.org/records/18314148 .

The full preprint and archive metadata were acquired; the 197 MB replication ZIP was not downloaded because the paper's explicit model comparison already rejects the proposed novelty. Across crumpled Mylar, steel-fiber assemblies, and Nitinol, the paper studies long-time phase-dependent logarithmic aging and dissipation changes under repeated cycles. It compares simpler relaxation/hysteron accounts with a full geometric network of bistable elastic elements. The latter is reported to reproduce the collection of experimental signatures; nonlinear geometric and nonpairwise interactions are central. Repackaging slow cyclic aging as an unexplained failure of pairwise hysterons would ignore this strongest competitor.

## Reproduction

From the shared workspace, run:

```bash
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 opportunity_dynamics/reproduce_granular.py
```

Inputs are the downloaded raw files, source manifest, and the author script. Outputs are regenerated JSON, CSV, and PNG. No proprietary solver, paid external computation, or new experiment was used.

## Adversarial implications for the synthesis branch

Comparing first-product identities with maximum thermodynamic driving force is enough to select a problem worth investigating. It is not enough to establish that transferable physical-time planning is achievable from the available measurements. That comparison only rejects the tested thermodynamic ranking; it does not reject the stronger family of mechanisms involving nucleation, diffusion, interface contact, and evolving morphology.

A sharper constructive target is: Can a library of local reactive-interface response operators, calibrated once on lower-order systems and expressed in physical units, be composed to predict full phase-fraction time courses and successful heating schedules for previously unseen multicomponent recipes, without refitting to the new recipe or filtering possible phases by the desired product?

This earns a broad operation only if transfer is tested across a genuinely new interaction setting. Holding out another trajectory of the same recipe is weaker than holding out a new precursor combination or microstructure while preserving an independently calibrated operator library. The benchmark must include measured thermal histories and initial particle/contact geometry or explicitly quantify uncertainty over those inputs. Operators must describe both reaction and the creation/destruction of future interfaces, otherwise simple rate composition is not closed.

First-phase identity data alone do not identify reaction rate constants or the contact/transport state. Even complete bulk phase fractions may admit several different kinetic networks with incompatible control predictions. A decisive next calculation should first expose whether the existing time-resolved measurements identify the operator under the intended interventions. If they do not, report the nonidentifiability or robust prediction set rather than assigning a physically suggestive name to an unconstrained fit.

The synthesis branch currently has the stronger empirical route to a complete operation because it includes time-resolved phase measurements and an identifiable competitive simulator. Its continuation should turn on an auditable transfer test against that strongest simulator, not the general statement that kinetics matters. A demonstrated composition rule or a precise obstruction to one would be substantive; the presently reproduced first-product discrepancy is not itself the discovery.
