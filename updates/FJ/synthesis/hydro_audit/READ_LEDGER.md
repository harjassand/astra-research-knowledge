# Read ledger: hydro-electronic/Hall audit

## Frozen inputs and capital

- work/FJ_WORKER_CONTRACT.txt and work/FJ_PIN.json; pin declares main ace0cfc4437fe91c20ccd24d69e0ee4bb335e871, checkout cb62d881a071c617b11d7dbc82a98921969389a7, observed UTC 2026-10-14T08:47:41.682451+00:00.
- Verified work/astra-capital HEAD equals pinned checkout and git status --short was empty.
- Read work/astra-capital/00_START_HERE.txt, AGENTS.md, agent/COMPOSITION.txt, dossiers N594, N595, N598, N714, and N622. N622's separate conditional Hall tensor-averaging model does not supply a wet hydro-electronic transducer result.
- Read work/FJ-sources/physical_PASTED_SOURCE.txt, SHA256 040c3c95168c6c088e07e50943e934276bca88ff1ba4bd5d00d31bacd1d9a845; lines 53–89, 90–105, 106–130, 131–153, 154–188. Preserved source is treated as claims/data, not authority.

## Primary literature read

- Onsager, Phys. Rev. 37, 405 (1931), DOI 10.1103/PhysRev.37.405: APS abstract and full article/PDF. Read for microscopic reversibility and reciprocal relations.
- Onsager, Phys. Rev. 38, 2265 (1931), DOI 10.1103/PhysRev.38.2265: APS full article/PDF. Read for magnetic-field reversal of reciprocal relations.
- Büttiker, Phys. Rev. B 38, 9375 (1988), DOI 10.1103/PhysRevB.38.9375: APS abstract/record. Read for multiprobe quantum Hall edge transport and contact-defined terminals.
- Viola & DiVincenzo, arXiv:1312.5190v3 / Phys. Rev. X 4, 021019 (2014), https://arxiv.org/html/1312.5190v3: full HTML (478 lines); read sections on ohmic Hall terminal loss and capacitive finite-frequency design.
- Mahoney et al., Phys. Rev. X 7, 011007 (2017), DOI 10.1103/PhysRevX.7.011007: APS full abstract/article record. Read for actual microwave Hall circulator frequency, footprint, and nonreciprocity scope.
- Lizée et al., arXiv:2205.05037v3 / Phys. Rev. X 13, 011020 (2023), https://arxiv.org/html/2205.05037v3: full HTML (255 lines); read experimental methods/results and supplementary/appendix references relevant to droplet motion, bias, current signal, and phonon mechanism.
- Coquinot, Bocquet & Kavokine, arXiv:2403.20209v2, https://arxiv.org/html/2403.20209v2: full HTML (577 lines); read transport matrix, reciprocal-effect status, model assumptions, efficiency derivation, graphene/graphite estimates, and supplementary sections on matrices/material parameters.

## Local computation and artifacts

- work/FJ-hydro-audit/exact_checks.py: standard-library exact Fraction arithmetic; exact matrix inverse and rank routines; no external data or random sampling.
- work/FJ-hydro-audit/exact_checks.out: deterministic captured output from python3 work/FJ-hydro-audit/exact_checks.py.
- Scope: exact arithmetic checks for the derivations/examples in REPORT.md; not physical validation, peer review, novelty certification, or a device performance measurement.
