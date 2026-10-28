"""Consume saved outputs and source hashes; freeze this owned research folder."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]

def main():
    source=json.loads((ROOT/'sources/ACQUISITION.json').read_text())
    assert source['revision']=='97970d87d04c7b0c932c69d3403b155d844acfc6'
    for item in source['files']:
        path=ROOT/'sources'/item['path']
        assert path.stat().st_size==item['bytes']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']
    primary=json.loads((ROOT/'sources/primary/receipts.json').read_text())
    for item in primary:
        if item['status']=='ACQUIRED':
            path=ROOT/'sources/primary'/item['file']
            assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']
            if path.suffix=='.pdf':assert path.read_bytes().startswith(b'%PDF-')
    for path in ROOT.rglob('*.json'):json.loads(path.read_text())
    r=json.loads((ROOT/'results/REDOX_TRANSPORT.json').read_text())
    strong=r['equally_informed_Levich_control']
    assert 1000<strong['Ga_ppm_at_anode_point2V']<r['Ga_leakage_rows'][4]['Ga_ppm']
    assert r['purity_potential_gates'][0]['largest_anode_V_fast_equilibrium_model']<0
    assert strong['purity_gates'][0]['max_anode_V']>0
    assert max(x['relative_error']for x in r['ordinary_independent_BVP_controls'])<5e-13
    assert not r['favorable_Ga_host_scenario']['dirty_scrap_to_host_admission_rate_acquired']
    receipt={
        'status':'PASS_SCOPED_OUTPUT_CONSUMER_AND_SOURCE_HASHES',
        'source_revision':source['revision'],
        'Levich_correction_changes_1ppm_window':True,
        'Ga_ppm_Levich_point2V':strong['Ga_ppm_at_anode_point2V'],
        'maximum_BVP_relative_error':max(x['relative_error']for x in r['ordinary_independent_BVP_controls']),
        'new_physical_capability':'NOT_ACQUIRED',
        'root_scientific_review':'Accepted internally at supplied-model scope; no primary-regime or physical validation.',
        'python_for_receipt':sys.version}
    (ROOT/'results/FINAL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    files={
        str(p.relative_to(ROOT)):{'bytes':p.stat().st_size,
            'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
        for p in sorted(ROOT.rglob('*'))if p.is_file()and p.name!='MANIFEST.json'}
    (ROOT/'MANIFEST.json').write_text(json.dumps({
        'status':'FROZEN_BOUNDED_AL_GA_CANDIDATE_FAILURE',
        'source_revision':source['revision'],'file_count':len(files),'files':files},
        indent=2)+'\n')
    for name,info in files.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==info['sha256']
    print(json.dumps({
        'status':'PASS','file_count':len(files),
        'bytes':sum(x['bytes']for x in files.values()),
        'proof_sha256':files['PROOF.md']['sha256'],
        'result_sha256':files['RESULT.md']['sha256']},indent=2))

if __name__=='__main__':main()
