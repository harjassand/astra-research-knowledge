"""Package the evidence audit, numerical inputs and reproducible calculations."""
from pathlib import Path
import hashlib,json,zipfile

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'output'/'selection'
paths=[]
def take(folder,names):
    for n in names:paths.append(ROOT/folder/n)
take('opportunity_root',[
 'audit_thermodynamic_control.py','build_selection_figures.py','build_selection_report.py',
 'build_selection_archive.py','thermodynamic_audit.json','table_s2_transcribed.json',
 'onset_sensitivity.json','onset_sensitivity_by_reaction.json','phase_trajectories.json',
 'clock_diagnostic.json','local_shell_clock_diagnostic.csv','phase_data/adp3309_data_s1.xlsx',
 *[f'41563_2026_2596_MOESM{i}_ESM.xlsx' for i in range(2,7)]])
take('opportunity_materials',[
 'analyze_chen.py','analyze_precursor_genome.py','chen_target_tables.txt','chen_fig4c.csv',
 'chen_extracted_temperature_rows.csv','chen_matched_temperatures.csv','chen_reanalysis_summary.json',
 'precursor_genome_ledger.json','precursor_genome_summary.json','materials_evidence_audit.md',
 'source_downloads.json','audit_manifest.json',
 *[f'44160_2024_502_MOESM{i}_ESM.xlsx' for i in range(7,10)]])
take('opportunity_dynamics',[
 'assessment.md','source_manifest.json','reproduce_granular.py','reproduction_results.json',
 'reproduction_summary.csv','granular_reproduction.png','audit_onsager_outlier.py',
 'onsager_outlier_note.md','onsager_outlier_countercheck.json','BTO_Transport_Coefficients.csv'])
paths.extend(sorted((ROOT/'opportunity_dynamics'/'raw').rglob('*.csv')))
take('opportunity_physics',[
 'compare_measurements.py','comparison_results.json','bergstrom2024_tables.json',
 'bergstrom2024_tables.csv','electrolyte_opportunity_audit.md','redox_synthesis_prior_art_check.md'])
take('output/selection',['reactive_interface_selection.pdf','synthesis_evidence.png','synthesis_clock.png'])

# The external author's analysis program is a separate dependency, with its
# exact inspected bytes pinned. This archive redistributes our wrapper/results,
# not the third-party program or full research papers.
author=ROOT/'opportunity_dynamics'/'trackParticlesAndStrains.py'
author_sha=hashlib.sha256(author.read_bytes()).hexdigest()
fetch='''"""Fetch the externally maintained author-analysis dependency, verify, then save.
This script downloads only; it does not execute the downloaded program.
"""
from pathlib import Path
import hashlib,urllib.request
url='https://raw.githubusercontent.com/cwlindeman/shear-cell-data/master/trackParticlesAndStrains.py'
expected=%r
with urllib.request.urlopen(url,timeout=45) as r:data=r.read()
if hashlib.sha256(data).hexdigest()!=expected:
    raise RuntimeError('Author source changed; recover the recorded revision before reproduction.')
p=Path(__file__).resolve().parent/'trackParticlesAndStrains.py'
p.write_bytes(data)
print(p)
''' % author_sha
(ROOT/'opportunity_dynamics'/'fetch_author_analysis.py').write_text(fetch)
paths.append(ROOT/'opportunity_dynamics'/'fetch_author_analysis.py')

readme='''EVIDENCE-FOUNDED SCIENTIFIC OPPORTUNITY SELECTION
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
'''
(OUT/'README_selection.txt').write_text(readme)
manifest={'date':'2026-11-05','files':[],'external_author_program_sha256':author_sha}
for p in paths:
    if not p.is_file():raise FileNotFoundError(p)
    manifest['files'].append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,
                             'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
mf=json.dumps(manifest,indent=2)
(OUT/'selection_manifest.json').write_text(mf)
dst=OUT/'scientific_selection_record.zip'
with zipfile.ZipFile(dst,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    z.writestr('README.txt',readme);z.writestr('MANIFEST.json',mf)
    for p in paths:z.write(p,str(p.relative_to(ROOT)))
with zipfile.ZipFile(dst) as z:
    assert z.testzip() is None
    for entry in manifest['files']:
        assert hashlib.sha256(z.read(entry['path'])).hexdigest()==entry['sha256']
print(json.dumps({'path':str(dst),'bytes':dst.stat().st_size,'verified_files':len(paths),
                  'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()},indent=2))
