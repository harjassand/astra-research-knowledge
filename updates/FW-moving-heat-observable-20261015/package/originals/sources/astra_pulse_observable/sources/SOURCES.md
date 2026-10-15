# Primary-source ledger

These sources informed selection, prior-art checks, and input interpretation. None of their manuscript text or software implementation is redistributed here. Only the stated original measurement row is retained.

## Scientific inputs

Rüther, Schamel, Plank, Schomburg, Röder and Danzer. *Cell-to-Cell-Variations of a Panasonic NCR18650B*. Zenodo record 8369275. https://zenodo.org/records/8369275 . Associated paper: *Cell-to-cell variation beyond parameter analysis — Identification and correlation of processes in Lithium-Ion Batteries using a combined distribution of relaxation times analysis*, Journal of Power Sources 587 (2023), 233677. https://doi.org/10.1016/j.jpowsour.2023.233677 . See provenance.json for extraction and unacquired inputs.

## Load-bearing prior-art boundaries

1. Yury Grabovsky. *Reconstructing Stieltjes functions from their approximate values: a search for a needle in a haystack*. SIAM Journal on Applied Mathematics 82(4), 1135–1166 (2022); arXiv:2101.02775. https://arxiv.org/abs/2101.02775 . Certified reconstruction and uncertainty for EIS already exist. The abstract was inspected; this session did not independently audit the whole proof or execute its Fortran implementation.
2. Scott Lawrence. *Model-free spectral reconstruction via Lagrange duality*. arXiv:2408.11766. https://arxiv.org/html/2408.11766v1 . Positivity-constrained bounds on spectral linear functionals and finite-dimensional dual formulations are established machinery. HTML sections on formulation and duality were inspected; no theorem is imported with additional unverified hypotheses.
3. Huang et al. *How reliable is distribution of relaxation times (DRT) analysis? A dual regression-classification perspective on DRT estimation, interpretation, and accuracy*. Electrochimica Acta 443, 141879 (2023). https://www.sciencedirect.com/science/article/pii/S001346862300066X . Referenced by the upstream implementation; no claim of having reproduced its hierarchical model.
4. Huang et al. *Rapid mapping of electrochemical processes in energy-conversion devices*. Joule 8(7), 2049–2072 (2024). https://doi.org/10.1016/j.joule.2024.05.003 . Joint time/frequency-domain acquisition is an incumbent, not a new proposal here.
5. hybrid-drt original source. https://github.com/jdhuang-csm/hybrid-drt/blob/e01dba1bf5f02fa6b63c82169c0652a5a695344d/hybdrt/models/drt1d.py . Fitting core and prediction interface inspected, not executed. This package's NNLS comparator is NOT a reproduction of hybrid-drt.
6. Goldammer et al. *Determination of the Distribution of Relaxation Times by Means of Pulse Evaluation for Offline and Online Diagnosis of Lithium-Ion Batteries*. Batteries 7(2), 36 (2021). https://www.mdpi.com/2313-0105/7/2/36 . Time-domain pulse analysis is established prior art.

## Opportunity scan, not reproduced benchmarks

- Cantera. *Ignition delay time using the Redlich–Kwong real gas model*. https://cantera.org/stable/examples/python/reactors/non_ideal_shock_tube.html . Accessible governing model and ignition-delay example.
- *KinetiX: A performance portable code generator for chemical kinetics and transport properties*. https://arxiv.org/html/2411.02640v2 . Existing kinetics-performance competition.
- *FEAT: Free energy Estimators with Adaptive Transport*. https://arxiv.org/html/2504.11516v2 . Learned transport, escorted free-energy estimators, and explicit sampling prerequisites.
- *Scalable Global Optimization for AC-OPF via Quadratic Convex Relaxation and Branch-and-Bound*. https://arxiv.org/html/2505.18435v1 . Existing global-bounding competitor and public-grid test environment.
- *Nonlinear Landau Collisions Without Collision Tensors*. https://arxiv.org/html/2606.31035v1 . Existing low-storage collision representation; not executed.
- *A fast spectral particle method for the Landau equation*. https://arxiv.org/html/2609.23086v1 . Existing fast collision computation; not executed.

## Research-memory use

Astra's current inventory and OpenAI/math's README were inspected for orientation and claim-status limitations. Neither supplies a theorem assumed in this work. No claim of exhaustively reading either repository is made.
