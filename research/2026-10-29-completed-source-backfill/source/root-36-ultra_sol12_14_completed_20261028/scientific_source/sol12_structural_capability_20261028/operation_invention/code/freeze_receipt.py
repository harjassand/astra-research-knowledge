"""Verify exact source receipts/result consumption and freeze this owned folder."""
from pathlib import Path
import hashlib,json
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
REVISION='8d51d60762b3ee28c10aaaa56e1b92da119dc1cc'

def main():
    for receipt in ('sources/ACQUISITION.json','sources/powder_source_receipts.json'):
        data=json.loads((ROOT/receipt).read_text())
        assert data['revision']==REVISION
        for item in data['files']:
            local=ROOT/'sources'/item['path']
            if not local.exists():local=ROOT/'sources'/Path(item['path']).name
            assert local.stat().st_size==item['bytes']
            assert hashlib.sha256(local.read_bytes()).hexdigest()==item['sha256']
    for path in ROOT.rglob('*.json'):json.loads(path.read_text())
    common=json.loads((ROOT/'results/common_sideband.json').read_text())
    shell=json.loads((ROOT/'results/shell_and_loss_witness.json').read_text())
    assert common['ordinary_and_lockin_same_noisy_statistic']
    assert common['ordinary_joint_regression_rank']==729
    linear=shell['sharper_reciprocal_linear_bound']
    assert Fraction(linear['rigorous_normalized_response_upper'])<Fraction(100,99)
    assert Fraction(linear['true_void_fraction_lower'])>Fraction(49,100)
    assert linear['reciprocity_general_symmetric_two_site_identity']=='PASS_EXACT'
    receipt={
        'status':'PASS_SOURCE_HASHES_JSON_AND_EXACT_RESULT_CONSUMER',
        'source_revision':REVISION,'ordinary_same_statistic':True,
        'linear_gate_upper':linear['rigorous_normalized_response_upper'],
        'linear_void_lower':linear['true_void_fraction_lower'],
        'independent_scientific_review':
            'Root theorem-level challenge as recorded; this consumer is producer-authored.'}
    (ROOT/'results/final_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    files={
        str(p.relative_to(ROOT)):{
            'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
            'bytes':p.stat().st_size}
        for p in sorted(ROOT.rglob('*'))if p.is_file()and p.name!='MANIFEST.json'}
    manifest={
        'status':'FROZEN_BOUNDED_OPERATION','file_count':len(files),
        'source_revision':REVISION,'files':files}
    (ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    for name,item in files.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==item['sha256']
    print(json.dumps({
        'status':'PASS','frozen_files':len(files),
        'total_bytes':sum(v['bytes']for v in files.values()),
        'proof_sha256':files['PROOF.md']['sha256'],
        'loss_proof_sha256':files['FAILED_LOSS_BRIDGE.md']['sha256']},indent=2))

if __name__=='__main__':main()
