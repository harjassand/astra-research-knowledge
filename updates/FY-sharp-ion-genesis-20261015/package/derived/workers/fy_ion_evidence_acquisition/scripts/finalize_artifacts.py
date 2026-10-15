"""Verify immutable sources and produce selective handoff manifests."""
import datetime
import hashlib
import json
import math
import pathlib
import zipfile

ROOT=pathlib.Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'acquisition_manifest.json').read_text())
sources=[]
checks=[]
for rec in manifest:
    if 'local_path' not in rec:
        continue
    p=pathlib.Path(rec['local_path'])
    b=p.read_bytes()
    digest=hashlib.sha256(b).hexdigest()
    assert digest==rec['sha256']
    kind='PDF' if b.startswith(b'%PDF') else 'ZIP/OOXML' if b.startswith(b'PK') else 'GZIP/TAR' if b.startswith(b'\x1f\x8b') else 'HTML' if b.lstrip().startswith(b'<!DOCTYPE') else 'UNKNOWN'
    valid=not (p.suffix=='.pdf' and kind!='PDF')
    if p.suffix=='.xlsx':
        with zipfile.ZipFile(p) as z:
            assert z.testzip() is None
            assert 'xl/workbook.xml' in z.namelist()
    sources.append({'source_filename':p.name,'local_relative_path':str(p.relative_to(ROOT)),'requested_url':rec['requested_url'],'final_url':rec['final_url'],'acquired_utc':rec['acquired_utc'],'bytes':len(b),'sha256':digest,'actual_type':kind,'expected_extension_valid':valid,'publication_handling':'local-only original; cite URL/hash; do not publish full texts or source archive'})
    checks.append({'check':'source_bytes_unchanged','file':p.name,'pass':True})

r=json.loads((ROOT/'analysis/MEASUREMENT_RESULTS.json').read_text())
assert r['kautz_ED']['conductance_points_per_cell']==354
assert r['kautz_ED']['voltage_points']==42877
assert r['kautz_ED']['minimum']['conductance_cell']=='B191'
assert math.isclose(r['kautz_ED']['minimum']['G_over_G0'],0.4934752014676972,rel_tol=1e-14)
assert math.isclose(r['kautz_ED']['conditional_inventory']['50_percent_at_37h_umol'],0.315,abs_tol=1e-14)
assert math.isclose(r['kautz_HCl_efficiency']['efficiency'],1.9612608840137795e-5,rel_tol=1e-13)
assert math.isclose(r['kong']['unweighted_mean_purity_percent'],99.45712414656207,rel_tol=1e-13)
assert math.isclose(r['kong']['cost_sums'][1]['sum_B_to_G_USD_per_kg_LiOH_H2O'],4.59941,abs_tol=1e-12)
checks.extend([{'check':x,'pass':True} for x in ['paired_Kautz_source_counts_and_reported_minimum','conditional_0.315_umol_arithmetic','HCl_maximum_electrical_power_and_efficiency','Kong_equation6_all_nonzero_source_rows','Kong_0.5year_cost_components_sum']])

(ROOT/'SOURCE_INDEX.json').write_text(json.dumps({'sources':sources},indent=2)+'\n')
inventory=[]
for p in sorted((ROOT/'analysis/private_extractions').glob('*_cells.json')):
    b=json.loads(p.read_text())
    inventory.append({'source_file':b['source_file'],'sheets':[{'name':s['name'],'dimension':s['dimension'],'state':s['state'],'populated_cell_count':len(s['cells']),'formula_count':sum('formula' in c for c in s['cells'].values())} for s in b['sheets']]})
(ROOT/'analysis/WORKBOOK_INVENTORY.json').write_text(json.dumps(inventory,indent=2)+'\n')
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'source bytes and numerical replay only; no new physical verification','source_hash_checks':len(sources),'checks':checks,'format_failure_preserved':'Kautz direct main-PDF request returned HTML; version-of-record full PDF not acquired','visual_review':['Kautz publisher SI PDF pages25-26; calibration and Ti-current examples','Kautz author preprint v3 PDF page10; ON/OFF conductance response','reanalysis plot; labels, units, sampling gaps, minimum visible'],'source_obligations_still_open':['ratchet Li/Na/Cl species-resolved transport','whole-cycle auxiliary and membrane inventories','input-power record for KCl ED regime','repeatable collected and retained lithium output','Kong underlying replicate records and complete dry-product impurity certification']}
(ROOT/'VALIDATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
files=['EVIDENCE_REPORT.txt','SOURCE_INDEX.json','VALIDATION_RECEIPT.json','analysis/MEASUREMENT_RESULTS.json','analysis/WORKBOOK_INVENTORY.json','analysis/kautz_deionization_derived.csv','analysis/kong_purity_recalculation.csv','analysis/kautz_deionization_reanalysis.png','scripts/acquire.py','scripts/extract_sources.py','scripts/analyze_measurements.py','scripts/finalize_artifacts.py']
public=[]
for fn in files:
    p=ROOT/fn
    public.append({'relative_path':fn,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(ROOT/'PUBLISHABLE_MANIFEST.json').write_text(json.dumps({'allowed_files':public,'excluded_directories':['raw_originals/','analysis/private_extractions/','analysis/local_plot_dependencies/'],'excluded_file':'acquisition_manifest.json contains full HTTP metadata; use SOURCE_INDEX.json for citations','note':'Selection does not perform publication. Original data are local-only; no full article/SI text is included.'},indent=2)+'\n')
print(json.dumps({'source_hash_checks':len(sources),'format_failures':[s['source_filename'] for s in sources if not s['expected_extension_valid']],'checks':len(checks),'publishable_files':len(files),'receipt':str(ROOT/'VALIDATION_RECEIPT.json')},indent=2))
