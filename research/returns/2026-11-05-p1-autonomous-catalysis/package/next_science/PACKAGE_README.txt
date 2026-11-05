AUTONOMOUS CATALYSIS RESEARCH — REPRODUCIBILITY PACKAGE
Prepared 2026-11-04. Read the main research report for conclusions and limits.
This archive preserves constructed science and unsuccessful attempts. It
does not certify a new physical mechanism or a demonstrated breakthrough.

CONTENTS AND STARTING POINTS
- research_report.txt or next_science/research_report.txt, when present:
  root scientific narrative. The build record identifies the included path.
- output/pdf/autonomous_catalysis_research.pdf, when available: final report.
- next_science/SELECTION_AND_QUESTION.txt: question selection and independent
  constructor routes; next_science/research_provenance.json pins Astra to
  d5ac5437c8f953fc515f931fbcb1ef80b4e96dd7 and records prior-artifact hashes.
- next_science/observation/: methane observational opening, positive source
  reconstructions, dual-isotope conditioning and retained negative results.
- next_science/observation2/: source-conditioned catalytic pulse and full
  renewal-cycle calculations, official SI and selected rendered SI figures.
- next_science/transfer/: finite acquisition/capacity alternative; full-cycle
  signed rewards, complete reversible model audits, rapid gross-adsorption
  stress cases, conditional thermal yet beneficial energy-routing example.
- next_science/invention/: initial independent concepts and prior-art
  challenges, exact capacity geometry/solver,72-state reversible catalyst,
  topology/thermal-projection counterexamples and exact rational witnesses.
- next_science/root_construction/catalysis/: final thermal-projection theory,
  nonlinear variational bounds, digitization and evidence figure scripts.
- prior_clocked_grid/clocked_grid_research.txt and clocked_grid_research.zip:
  unchanged earlier construction, including exact waveform/timing limits,
  source authors' causal account and the unsuccessful later-week replay.
- MANIFEST.sha256: hashes of every other archive member. PACKAGE_CONTENTS.json
  records source-relative paths, sizes, inclusion categories and omissions.
  BUILD_ENVIRONMENT.json reports the build environment, not a lockfile.
  THIRD_PARTY_ATTRIBUTIONS.txt distinguishes measurement licenses.

BUILDING AND VERIFYING THE ARCHIVE
From the extracted project root:
  python next_science/package_research.py
prints a read-only summary of what would be included. It creates no archive.
After the final report is ready:
  python next_science/package_research.py --build
writes output/autonomous_catalysis_research.zip. Optional --require-report
requires both the report and final PDF. --list prints all inclusion paths.
--workspace PATH and --output PATH override locations. The script checks the
old grid TXT/ZIP against their recorded SHA256 before packaging. On a fresh
extraction it finds them under prior_clocked_grid. It never alters scientific
source files, downloads data, runs experiments, uploads or publishes.
The manifest excludes only its own checksum to avoid circular hashing.
Verify after extraction, before rerunning scripts that overwrite outputs:
  sha256sum --check MANIFEST.sha256
The ZIP is constructed via a temporary file and then replaced atomically.
It is not a promise of byte-identical ZIPs across Python/zlib versions; member
content hashes, exact rational outputs and stated numeric tolerances govern.

REQUIREMENTS
Python 3.11+; the present calculations were executed under Python 3.12.
Core own-code dependencies:
  python -m pip install numpy scipy mpmath openpyxl matplotlib pillow
The exact capacity and rational topology computations also use Python's
standard-library fractions module. PDF rebuilding may additionally require
reportlab and the renderer dependencies documented by any included PDF
builder. No GPU or external service is required to rerun the included own
calculations. They are conditional synthetic models unless explicitly marked
as computations from public measurements. Scripts write their JSON/CSV/figure
outputs beside themselves; work on a copy to preserve the original hashes.

CORE CATALYSIS REPRODUCTION (from archive root)
  python next_science/observation2/catalytic_pulse_construction.py
  python next_science/observation2/full_cycle_renewal.py
  python next_science/observation2/reversible_impulse_response.py
  python next_science/observation2/pulse_resource_bounds.py
  python next_science/invention/catalytic_cycle72.py
  python next_science/transfer/catalytic_cycle_response.py
  python next_science/transfer/catalytic_poisson_audit.py
  python next_science/transfer/reversible_source_stress.py
  python next_science/transfer/thermal_recycling_counterexample.py
  python next_science/root_construction/catalysis/check_thermal_projection.py
  python next_science/root_construction/catalysis/variational_gate_bound.py
  python next_science/root_construction/catalysis/thermal_competition.py
  python next_science/root_construction/catalysis/full_cycle_figure.py
The72-state programs use arbitrary precision and can take longer than the
small closed-form examples. A complete script run reproduces its conditional
model, not the original authors' atomistic simulation or an empirical fit.
No scientific calculations are rerun by the packaging script.

EXACT WITNESSES AND ALTERNATIVES
  python next_science/invention/projection_exact_witnesses.py
  python next_science/invention/projection_two_cycle_witness.py
These use the retained positive-search output as input; the prior search
script is also preserved but need not be rerun to verify its exact witness.
For capacity demonstration options:
  python next_science/invention/capacity_geometry_exact.py --help
The archived result preserves the full rational enclosures and checks. A
capacity result is not substituted for arbitrary-basin mean passage time;
read transfer/construction_checkpoint.txt and the root Poisson/access notes.

METHANE MEASUREMENT COMPUTATIONS
  python next_science/observation/analyze_methane.py
  python next_science/observation/analyze_dual_isotope.py
The first uses isotope_source_4.xlsx and5.xlsx;4–7 are retained as the selected
published source-data set. The second reads all six workbooks at their EXACT
script-relative paths:
 next_science/observation/dD_GlobMean/
 Riddell-Young_2025_dD_GlobMean/output/GlobMean_dD_iterations*.xlsx
Each contains the authors' archived ensemble, not a new reconstruction by us.
The NOAA annual, monthly and growth text downloads and their original headers
are preserved, along with URL/hash manifests. Recorded downloads are versioned
snapshots; current live data may have been revised.

UPSTREAM DATA/PIPELINES NOT INCLUDED
To rerun the AUTHORS' upstream global-isotope reconstruction, download
Riddell-Young_2025_dD_GlobMean.zip(88,160,857bytes) from
 https://zenodo.org/records/17238656
 https://zenodo.org/api/records/17238656/files/Riddell-Young_2025_dD_GlobMean.zip/content
and consult the recorded author workflow in dual_isotope_zenodo_manifest.json.
For their mass-balance figures/inversion also download the separate
Riddell-Young_2025_MassBalancePackage.zip(~1.97GB) from the same record.
Their workflow includes station inputs, NOAA smoothing code, gridded source
maps and dependencies such as xarray,cartopy,shapely and geopandas. Neither
upstream pipeline was rerun here. Only the six archived ensembles needed by
our covariance/GLS computation are bundled. Other author intermediate and
ensemble outputs are deliberately omitted as redundant for our calculation.
Original isotope source-data URLs are in isotope_source_manifest.json:
 https://doi.org/10.1038/s41467-026-74777-4
The optional optical-feedback-trap comparison can be revisited from
 https://doi.org/10.5281/zenodo.6680673 (measurement data)
 https://doi.org/10.5281/zenodo.6680638 (SKIPPER author code).
Their manifests are retained, but author code/data copies are omitted because
none is required by our included computational scripts. Their public CC BY 4.0
license was recorded; omission is a scope/size choice, not a claim of a ban.

ASTRA AND GOVERNING SOURCES
Exact repository-relative governing source locations, pinned revision,
conditions and corrections are recorded in our construction notes. Raw
repository files are not redistributed because a repository-wide reuse
license was not established. To inspect the originals, use the pinned commit:
 https://github.com/harjassand/astra-research-knowledge/tree/d5ac5437c8f953fc515f931fbcb1ef80b4e96dd7
Read its 00_START_HERE.txt, AGENTS.md and agent/ACCESS.txt before task-first packet
retrieval. This archive does not claim that every neighboring Astra theorem
applies to these newly constructed tasks.

ATTRIBUTION, CHANGES AND EXCLUSIONS
The methane ensemble data are Benjamin Riddell-Young (2025), Zenodo 17238656,
CC BY 4.0. The isotope source spreadsheets are Youmi Oh and coauthors (2026),
'Isotopic constraints in methane inversions reveal larger trends in wetland
emissions with improved linkage to terrestrial water storage',Nature
Communications,DOI10.1038/s41467-026-74777-4,CC BY 4.0. Workbooks are unchanged.
NOAA GML data retain their original citation/use headers; URLs and recorded
SHA256 are included. Do not describe provisional/revised records as immutable.
The official catalyst SI is Chenjia Liang, Jun Yao, Xiaoxia Hou and coauthors,
'Dynamic Vibration-Coupled Energy Transfer for Boosting ORR Catalysts in Fuel
Cells',DOI10.1021/jacs.5c15936.s001,ACS Figshare31199023,CC BY-NC 4.0.
The PDF is unchanged; vcet_SI.txt is an extracted-text rendition andsi-*.png
are rendered pages. Numeric digitization and its geometric uncertainty are
our derivatives, not author-supplied numeric data or experimental intervals.
 https://creativecommons.org/licenses/by/4.0/
 https://creativecommons.org/licenses/by-nc/4.0/
These third-party conditions remain applicable; this package does not issue
a single blanket license over all material, nor imply author endorsement.
The prior grid archive is preserved as received with its existing contents
and notices; it is not repackaged or relicensed internally.

Excluded: __pycache__ and compiled Python; downloaded research-paper PDFs,
HTML, XML and extracted full text; raw Astra source copies; the large upstream
methane archives and unused author intermediates; optional author repository
code/data; transient render caches. Source URL/hash manifests and our own
notes/proofs/results—including failed routes, unfavorable comparisons and
limitations—are preserved. The licensed SI is an explicit exception to the
paper-full text exclusion because it is an empirical source needed for the
reported digitization and source-condition analysis.
