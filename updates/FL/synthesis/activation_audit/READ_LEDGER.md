# Read and source ledger

Access date: 2026-10-14. Technical web checks used primary papers, primary project reports, official vendor material, or official metrology tables only.

## FL intake and capital context

- Read work/FL_WORKER_CONTRACT.txt, work/FL_PIN.json, the initial and supplemental FL intake manifests, work/astra-capital/00_START_HERE.txt, and work/astra-capital/AGENTS.md. Frozen byte copies are under source/.
- The pin records main revision ace0cfc4437fe91c20ccd24d69e0ee4bb335e871 and checkout/cumulative PR83 head 3c9c5564fc7f51cdbaa0a5a5b5b54ee9382dcd8d, plus the Ultra published ref. This workspace snapshot has no .git directory, so I relied on the supplied pin and did not independently resolve Git HEAD.
- work/FL-root was empty. The activation source's initial-manifest record is 25,794 bytes with SHA-256 7dfff79bddb5175067e4b90549b52c0c50fa5c9e5d9c2cc92f4e1a2f3b87d6ce. The owned source copy matches those exact bytes. The supplemental manifest explicitly corrects the provisional temporal filename/group to regenerative activation.
- Searched the frozen FL source inventory and source text for activation, hazard, recovery, unloading, molecule/rotor, scripts, and executable files. The activation packet contains the prose report only. work/FL-sources/global/verify_global_compatibility.py and its companion search code are for the separate global-compatibility stream and were not run or used here.
- Read current N777 and N783 dossiers and open capability/review gates. Both are source_derived_unreviewed; both review and capability gates remain open.
- For N777, copied the 535-line FA synthesis report and read its section 4 on the acquired full-configuration committor, arbitrary predictable switching with L^u q=0, almost-sure absorption, finite-time censoring, and the generator residual; also read the relevant open-gate/dossier statements. Source copy SHA-256: 4b6cddce0b5c881a53018f3cbc703f4658cb15011b3d1836afbe2cc77fd3e1ce.
- For N777 relative rare-yield scope, read the first 70 lines of FA synthesis review RELATIVE_ENDPOINT.md: its stated homogeneous finite-generator restriction, Doob/committor tilt, and need for an exponential moment. Full source copy SHA-256: 7686203cc231c4676836f050f694f93b4c79e529ddccdecea98249eb2ec70959.
- For N783, copied the 323-line FB reward report and read the no-chain terminal competing-hazard account, full active-state joint kernel, adaptive reward potential, reward horizon/reversal qualification, and termination/supply gates. Full source copy SHA-256: eae7bd7a8bd216e32a9db5e8775cc1fc90e08d839ec360df85a44fa3f0a07e7d.
- Read the N777/N783 dossier summaries and exact open gate questions. Dossier copy hashes are recorded in MANIFEST.json.

## Primary external sources

1. Timothy Y. Chen et al., “Direct observation of coherence transfer and rotational-to-vibrational energy exchange in optically centrifuged CO2 super-rotors,” *Nature Communications* 14, 3227 (2023), DOI 10.1038/s41467-023-38873-z. [Version of record](https://www.nature.com/articles/s41467-023-38873-z). Read the full publicly accessible article: abstract; experimental state-distribution results; broad distribution/J=364 tail statement; centrifugal-barrier note; field-free rotation-to-vibration timing; frequency-cut comparison; and discussion identifying moderate rather than fastest rotors as major inelastic-transfer contributors. Used only to scope what the experiment reports. It supplies no CO production, energy recovery, or population mean at 6.14 eV.

2. Sruthi Venkataramanababu et al., “Enhancing reactivity of SiO+ ions by controlled excitation to extreme rotational states,” *Nature Communications* 14, 4446 (2023), DOI 10.1038/s41467-023-40135-x. [Version of record](https://www.nature.com/articles/s41467-023-40135-x). Read the full publicly accessible article's abstract, optical pumping/ion-trap context, reaction-rate results, density, and discussion. Used to verify the reported factor-three enhancement and distinguish its ion-trap conditions from dense neutral CO2 conversion. No downloaded supplement or independent reanalysis of the data.

3. Ian MacPhail-Bartley et al., “Optical centrifuge as a probe of strong dissipative coupling between a molecular rotor and superfluid helium,” arXiv:2608.25161v1, submitted 25 Aug 2026. [arXiv record/PDF](https://arxiv.org/abs/2608.25161). Read the full 24-page PDF's abstract, introduction, and relevant experimental discussion/figure caption for accelerating and decelerating ultraslow centrifuges, alignment dynamics, thermalization, and dissipative bath coupling. The HTML endpoint timed out; PDF access succeeded. This source demonstrates a controlled field/alignment response in a strongly dissipative regime, not recovered work.

4. Institute for Sustainable Process Technology, *Next Level Solid Oxide Electrolysis: Upscaling Feasibility Study Report* (2023), [official report PDF](https://ispt.eu/media/2023-SOE-public-report_ISPT.pdf). Read its complete 33-page PDF at the relevant sections: Air Liquide CO basis of design and target purity/pressure; process-system schematic; thermoneutral and waste-heat assumptions; system electricity loads; Table 6 specific electricity consumption; cooling boundary; definition of complete plant; Table 12 AC/DC-adjusted values; CO2 feed-quality notes. The report is a modeled engineering use case, not full-scale operating data. Key inspected entries: >=96 mol% CO at 13 barg; 5,000 Nm3/h design capacity; 50% single-pass conversion; Table 6 3.2 kWh/kg CO (stack DC, feed/air heat, compression); Table 12 3.3 kWh/kg after a 97% AC/DC item; available high-quality liquefied CO2 and excess-heat assumptions; broader plant infrastructure not included in its modeled system boundary.

5. Topsoe, “Shared Learnings for Achieving High-Volume HTE Manufacturing” presentation hosted by the US DOE, 7 Mar 2022, [official DOE PDF](https://www.energy.gov/documents/shared-learnings-achieving-high-volume-hte-manufacturing-poul-georg-haldor-topsoe). Read the slide for the dry-CO2 electrolysis stack result: 14,000 h; 30,000 Nm3 (35.5 t) CO; 3.44 kWh/Nm3; 99 +/- 1% Faradaic efficiency. This is vendor-reported stack performance, not complete-plant energy.

6. Topsoe, “FAQ — Topsoe's eCOs plant,” [official product PDF](https://www.topsoe.com/hubfs/CAMPAIGNS/eCOs/FAQ_eCOs.pdf). Read the full one-page FAQ, including total-plant energy 6–8 kWh/Nm3 versus stack 3–3.5 kWh/Nm3, standard 99.0 vol% CO product purity, and CO2 feed/purge notes. These are vendor statements, separately sourced from the DOE stack-trial slide.

7. NIST, *CODATA Recommended Values of the Fundamental Physical Constants: 2022*, [official table](https://physics.nist.gov/cuu/pdf/wall_2022.pdf), and Commission on Isotopic Abundances and Atomic Weights, [2024 standard atomic weights](https://ciaaw.org/atomic-weights.htm). Read the tabulated exact electron-volt in joules and exact Avogadro constant, plus the C/O standard atomic-weight entries. The 28.010 g/mol CO mass is a nominal sum of 12.011 and 15.999, not an exact or universal isotopologue mass.

No third-party PDF was copied into the owned package. No outside source establishes performance or feasibility of the proposed regenerative molecular activation cycle.

## Owned source snapshots

- source/temporal_PASTED_SOURCE.txt preserves the 25,794-byte activation report; hash matches the intake manifest.
- source/FL_INTAKE_MANIFEST.json and source/FL_SUPPLEMENTAL_INTAKE_MANIFEST.json preserve the chronology and semantic filename correction.
- source/FL_PIN.json and source/FL_WORKER_CONTRACT.txt preserve the pin and operating contract.
- source/ASTRA_START_HERE.txt and source/ASTRA_AGENTS.md preserve the repository-start instructions consulted.
- source/N777_dossier.txt, source/N783_dossier.txt, source/N777_adaptive_proof_source.md, source/N777_relative_endpoint_source.md, and source/N783_reward_proof_source.md preserve relevant read context.
- No source or capital file was edited. Generated report, proof, checker, results, and this ledger are confined to work/FL-activation-audit/.
