# Read ledger — physical pivot audit

Access date: 2026-10-14. Primary-source pages were opened directly at the exact versions listed below. The copied producer ledger/source are preserved under `inputs/`; the producer script is copied but was not executed. No laboratory data, external contacts, or non-primary sources were used for the physical claims in this report.

## Primary sources

1. C. Bowness et al., “Laser-induced spectral diffusion and excited-state mixing of silicon T centres,” [arXiv:2504.09908v2](https://arxiv.org/html/2504.09908v2), 27 Nov 2025 according to the arXiv version header. Read the HTML main text, methods, and supplementary sections SVI–SX, including the RC-PLE linewidth, photon-rate, long-dark-time, and pair preparation model. The page has an internal author-date line of 24 Aug 2026 despite the arXiv v2 header date of 27 Nov 2025; that bibliographic inconsistency is recorded rather than silently resolved. The cited claims are tied to the exact v2 page and section names, not to an inferred revision chronology. The paper is also published as PRX Quantum 6, 030350 (2025).

2. X. Zhang et al., “Laser-induced spectral diffusion of T centers in silicon nanophotonic devices,” [arXiv:2504.08898v2](https://arxiv.org/html/2504.08898v2), published as PRX Quantum 6, 030351 (2025). Read the HTML main text and relevant check-probe, perturbation, off-resonant perturbation, and discussion sections. Used to establish that off-resonant pulses can reconfigure the local environment despite avoiding emitter excitation, and that dark retention alone does not imply protection during illuminated sequences.

3. C. Zhang et al., “Resolving and resetting the charge environment of single T-centers in silicon p–i–n waveguides,” [arXiv:2608.15993v1](https://arxiv.org/html/2608.15993v1), 17 Aug 2026. Read the HTML abstract, results, figures/captions, and methods. The arXiv PDF endpoint opened, but a subsequent PDF line-range retrieval timed out; the accessible HTML supplied the cited experimental details. No underlying raw dataset was available in the page; authors state data are available upon request. The paper is treated as prior work, not as an Astra invention.

4. F. Islam et al., “Surface passivation for narrowing optical linewidth of silicon T centers in nanophotonic devices,” [arXiv:2608.09904v2](https://arxiv.org/abs/2608.09904v2), 31 Aug 2026. Read the 16-page primary PDF. Used only in the early comparator screen: reported Al2O3 passivation, four same-emitter comparisons, and separate thickness cohort statistics. This is a preprint comparison and not a controlled head-to-head against the reset or RC-PLE studies.

5. Independent corroboration only: “Above-band illumination-induced charge stabilization of silicon T centers,” [arXiv:2607.28485](https://arxiv.org/abs/2607.28485). The primary abstract was read; its headline unheralded narrowing supports that above-band reset is an existing line of work. No detailed numerical comparison from this source is used.

## Independent calculation and execution record

- `derive_gate.py` is new code in this worker directory. It was run with the system Python 3 interpreter and uses only the standard library. It computes the two-state gate with exact rational arithmetic, an explicitly iid zero-failure binomial bound, and a scoped reconstruction of the source RC-PLE pair-throughput model.
- The calculation does not replay the source authors’ code, fit experimental data, or establish a device result. The pair model's detection and excitation factors are input parameters, not measured values from the cited experiment.
- The copied `inputs/PHYSICAL_OPERATION_AUDIT_CHECKS.py` was not executed. The source's physical prior conclusions were read only as context and are separately re-evaluated in this report.
