EVIDENCE-FOUNDED SCIENTIFIC OPPORTUNITY SELECTION
Date: 2026-11-05

Chosen question: Can independently determined reactive-interface laws compose
to predict and control full inorganic powder-synthesis trajectories in physical
time, including the creation and destruction of interfaces, without fitting
the new recipe? This is a supported choice for construction, not an achieved
interface theory, new synthesis, or civilization-changing discovery.

Read output/selection/reactive_interface_selection.pdf first. The previous
reflection-defect research is preserved separately and is not modified here.

MAIN REPRODUCTION (offline numerical inputs included)
Python dependencies: numpy, pandas, scipy, matplotlib, openpyxl.
  python opportunity_root/audit_thermodynamic_control.py
  python opportunity_materials/analyze_chen.py
  python opportunity_materials/analyze_precursor_genome.py
  python opportunity_physics/compare_measurements.py
  python opportunity_dynamics/audit_onsager_outlier.py
  python opportunity_root/build_selection_figures.py

Report generation additionally needs reportlab and Pillow:
  python opportunity_root/build_selection_report.py

GRANULAR REPRODUCTION
The raw selected coordinate files and our wrapper/results are included. The
original author's program is referenced separately, with an exact SHA-256:
  python opportunity_dynamics/fetch_author_analysis.py
  python opportunity_dynamics/reproduce_granular.py
The first command requires network access and only downloads/verifies. It does
not execute the downloaded program. The wrapper uses the analysis-function
prefix of that program. All 147 raw data blobs were checked against Git hashes.

PROVENANCE
Szymanski et al., Science Advances 2024, DOI 10.1126/sciadv.adp3309:
  The original phase-fraction XLSX is unchanged. Table S2 is explicitly
  transcribed in the audit script. Supplement acquired from the official
  Europe PMC service for PMC11221506.
Chen et al., Nature Synthesis 2024, DOI 10.1038/s44160-024-00502-y:
  Original source workbooks are unchanged. chen_target_tables.txt retains
  factual table rows extracted from the supplement, with labels inserted for
  deterministic parsing; it is not a facsimile of the full supplement.
  Numerical source coverage does not reconstruct all 224 reported syntheses.
Karan et al., Nature Materials 2026, DOI 10.1038/s41563-026-02596-5:
  Original source workbooks unchanged; acquired from Europe PMC PMC13421335.
  Original coefficient CSV: https://ndownloader.figshare.com/files/51681254
  Archive DOI: 10.6084/m9.figshare.28207292.v3.
  clock_diagnostic.json explicitly separates an ideal local-shell calculation
  from an experimental time or a complete simulator prediction.
Precursor Genome, Walters et al. 2026:
  https://github.com/lauren-walters/precursor-genome
  https://zenodo.org/records/21285546 (CC BY 4.0 data release).
  The ledger is unchanged; scans, alternative refinements and repeats are
  distinguished. Missing metadata and negative mass records are not repaired.
Lindeman, Soft Matter 2025, DOI 10.1039/D5SM00470E:
  https://github.com/cwlindeman/shear-cell-data/tree/v1.1
  https://zenodo.org/records/15367435
Bergstrom and McCloskey, ACS Energy Letters 2024,
  DOI 10.1021/acsenergylett.3c01662: explicitly transcribed Tables 1-2.

The reports and scripts cite all other primary comparisons. Full copyrighted
article texts are not redistributed. Original authors retain rights in their
source data and code; this package attributes numerical sources and provides
the selection analysis. Analysis notes from parallel audits retain their local
judgments, including cautions against over-interpreting endpoint collections.

SCOPE
No new laboratory experiment, diffraction re-refinement, DFT recalculation,
MD rerun or COMSOL rerun was performed. Reanalysis and exact conditional
calculations are labeled separately from observations and future hypotheses.
MANIFEST.json verifies the exact packaged bytes. Older acquisition manifests
may also refer to paper texts inspected during research but not redistributed.
