"""Join independently verified finite cases against the frozen author manifest.

Scientific interval work is in separate prospectively bounded receipts. This
join checks hashes, exact case coverage, operation totals and source disposition;
it does not silently promote an INCOMPLETE source to complete-range success.
"""
from pathlib import Path
import datetime,hashlib,json,time

ROOT=Path(__file__).resolve().parents[4]
OWN=Path(__file__).parent
MANIFEST=ROOT/'work/cycle6/c07_s02/phase2/OPTIMAL_PREFIX_MANIFEST.json'
MANIFEST_SHA256='43af483d98e4a92c36e5ee11ed5a758475b570a25e6fdeae9b59a03da2694874'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    started=time.perf_counter()
    outpath=OWN/'optimal_prefix_independent_complete_manifest_check.json'
    if outpath.exists():raise SystemExit('Preserving previous joined receipt.')
    assert sha(MANIFEST)==MANIFEST_SHA256
    manifest=json.loads(MANIFEST.read_text())
    assert manifest['delta_bar']=='138629437/100000000'
    assert manifest['certified_N_range']==[3,199]
    sources_checked={}
    for path,digest in manifest['sources'].items():
        assert sha(ROOT/path)==digest
        sources_checked[path]=digest
    all_cases=[];totals={};receipts=[]
    for chunk in manifest['chunks']:
        source=ROOT/chunk['path']
        assert source.stat().st_size==chunk['bytes']
        assert sha(source)==chunk['sha256']
        suffix=('_completed_N170_independent_integer_G64.json' if chunk['file_status']=='INCOMPLETE'
                else '_independent_integer_G64.json')
        path=OWN/(source.stem+suffix);receipt=json.loads(path.read_text())
        assert receipt['status'].startswith('PASS independent exact inputs/congruences/LDL')
        assert receipt['source_sha256']==chunk['sha256']
        assert receipt['guard_bits']==64
        assert receipt['precision_bits']==chunk['precision_bits']
        assert receipt['declared_total_wall_cap_seconds']==60
        assert 0<=receipt['wall_seconds']<60
        assert receipt['completed_cases']==chunk['accepted_cases']
        assert receipt['checker_sha256']==sha(OWN/'optimal_prefix_independent_integer_verifier.py')
        if chunk['file_status']=='INCOMPLETE':
            assert chunk['accepted_cases']==[170]
            assert receipt['source_file_status']=='INCOMPLETE'
            assert receipt['source_requested_N_range']==[170,199]
            assert receipt['accepted_source_cases']==[170]
            assert 'uncertified pivot N=171' in receipt['source_failure_preserved']
            assert receipt['partial_wrapper_sha256']==sha(OWN/'optimal_prefix_partial_completed_verifier.py')
        else:
            assert chunk['file_status']=='PASS all requested finite cases strictly positive'
        assert chunk['acquisition_wall_seconds']<chunk['declared_cap_seconds']<=60
        all_cases.extend(receipt['completed_cases'])
        for key,count in receipt['verified_counts'].items():totals[key]=totals.get(key,0)+count
        receipts.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path),
                         'accepted_cases':receipt['completed_cases'],'verification_wall_seconds':receipt['wall_seconds'],
                         'source_sha256':receipt['source_sha256'],'source_file_status':chunk['file_status']})
    assert all_cases==list(range(3,200))
    assert len(set(all_cases))==197==manifest['coverage_count']
    assert totals['contained_q_enclosures']==manifest['counts']['population_intervals']==20094
    assert totals['certified_blocks']==manifest['counts']['congruence_blocks']==491
    assert totals['positive_pivots']==manifest['counts']['positive_pivots']==15045
    assert totals['cross_multiplied_L_entries']==manifest['counts']['strict_lower_entries']==328350
    assert sum(c['bytes'] for c in manifest['chunks'])==manifest['total_evidence_bytes']
    assert abs(sum(c['acquisition_wall_seconds'] for c in manifest['chunks'])-
               manifest['total_acquisition_wall_seconds_including_failed_run'])<1e-8
    receipt={'status':'PASS complete independent exact finite-prefix certificate verification',
             'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'delta_bar':manifest['delta_bar'],
             'target_delta':'2log2 strictly smaller, proved by exact positive log2 series enclosure',
             'certified_N_range':[3,199],'coverage_count':len(all_cases),'verified_counts':totals,
             'independent_inputs':'positive Taylor exp(+y), geometric tail, reciprocal and squaring; different from author alternating exp(-y)',
             'independent_operations':'owned integer outward recurrence and exact endpoint quotient cross multiplication; no imported author arithmetic',
             'manifest':str(MANIFEST.relative_to(ROOT)),'manifest_sha256':MANIFEST_SHA256,
             'source_code_and_proof_hashes_checked':sources_checked,'receipts':receipts,
             'total_verification_wall_seconds':sum(r['verification_wall_seconds'] for r in receipts),
             'author_acquisition_wall_seconds_including_failed_run':manifest['total_acquisition_wall_seconds_including_failed_run'],
             'author_evidence_bytes':manifest['total_evidence_bytes'],
             'partial_source_disposition':'Only N170 is accepted from retained INCOMPLETE P1024 file; N171..199 are independently checked from frozen P1536 replacements.',
             'limits':['Finite certificates prove a finite prefix, not an unbounded-N extrapolation.',
                       'Analytic tail must be joined separately for N>=200.',
                       'N2 endpoint is singular and separately handled; not tested above endpoint.',
                       'No moment atom acquisition, finite-bit sampler, priority or external validation is implied.']}
    receipt['join_wall_seconds']=time.perf_counter()-started
    receipt['join_checker_sha256']=sha(Path(__file__))
    outpath.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('receipts','source_code_and_proof_hashes_checked')},indent=2))

if __name__=='__main__':main()
