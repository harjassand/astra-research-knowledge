#!/usr/bin/env python3
"""Local source build; does not upload, mutate originals, or run old science."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from io import BytesIO
import hashlib,json,shutil,datetime
HERE=Path(__file__).resolve().parent
WORKSPACE=HERE.parents[1]
NAME='Astra_Amplification_Cycle11_ULTRA_20261023'
OUT=WORKSPACE/'outputs'/NAME
def ident(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def copy(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
def main():
    if OUT.exists():raise RuntimeError('Refuse to replace prepared source; choose explicit correction workflow')
    OUT.mkdir(parents=True)
    for p in HERE.iterdir():
        if p.is_file() and p.suffix in ('.txt','.json','.py') and p.name!='build_packet.py':copy(p,OUT/p.name)
    copy(HERE/'build_packet.py',OUT/'provenance/build_packet_local.py')
    for src,dst in [('converse','converse'),('prior_challenge','receiving'),
                    ('search','search'),('breeding_lemma','breeding')]:
        shutil.copytree(HERE/src,OUT/'studies'/dst)
    shutil.copytree(HERE/'references',OUT/'references')
    shutil.copytree(HERE/'provenance/drafts',OUT/'provenance/drafts')
    prev=WORKSPACE/'outputs/Astra_Amplification_Cycle10_ULTRA_20261023.zip'
    assert ident(prev)==dict(bytes=10721967,sha256='893b52944c4a9cb693404a0c99da5c0af57f4fac5cdfff5b4b0b29b4f3f66b49')
    copy(prev,OUT/'source_chain'/prev.name)
    for n in ['CYCLE10_ULTRA_NORMAL_WORKSPACE_CLARIFICATION.txt','CYCLE10_ULTRA_NORMAL_WORKSPACE_AUDIT.txt']:
        copy(WORKSPACE/'outputs'/n,OUT/'source_chain'/n)
    z=ZipFile(prev);assert z.testzip() is None
    pr=z.read('PROOF.txt');assert hashlib.sha256(pr).hexdigest()=='41776adc6c19232d2db53adf4e628c680f61f6b7cf08b6ddd24c612db3cb633c'
    chain=[];r1=None
    for depth in range(16):
        names=[n for n in z.namelist() if n.endswith('.zip')]
        target=next((n for n in names if 'R1_OWNER_SOURCE' in n),None)
        if target:
            b=z.read(target);chain.append(target)
            r1=dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),nested_member_chain=chain)
            assert r1['sha256']=='8b813c9f267e3079225219fb2e857cd3e4c18451f82471e3c5ee72be73136676'
            zr=ZipFile(BytesIO(b));m='R1_finite_reuse/source_packet/seeds/R1_MODEL_AND_PROOF.txt';bm=zr.read(m)
            r1['model_member']=m;r1['model_bytes']=len(bm);r1['model_sha256']=hashlib.sha256(bm).hexdigest()
            assert r1['model_sha256']=='ae58a46f5d2c4c56a9904259ef1b2ee532da6056087be62bff08b39c4b83548e'
            # Direct exact small load-bearing seed, full native reservoir/replays remain in chain.
            p=OUT/'source_chain/R1_MODEL_AND_PROOF_UNCHANGED.txt';p.write_bytes(bm)
            break
        n=next((n for n in names if 'ULTRA' in n),names[0]);chain.append(n);z=ZipFile(BytesIO(z.read(n)))
    assert r1
    write(OUT/'provenance/SOURCE_PRESERVATION.json',dict(
        current_native=ident(prev),governing_predecessor_proof=dict(bytes=len(pr),sha256=hashlib.sha256(pr).hexdigest()),
        preserved_R1_native=r1,scope='Byte identity/ZIP CRC/source continuity only; no historical science rerun',
        parked_programmes='Full historical native chain unchanged; R1/molecular/thermal/TPV closures preserved'))
    common=HERE/'intake/Astra_Scientific_Amplification_Cycle11_20261023'
    selected=['START_HERE.txt','REPORT.txt','protocol/AGENT_HANDOFF.txt','prompts/04_ULTRA_CONTINUATION.txt',
              'reviews/quantum_review.md','ORIGINAL_SOURCE_ROUTES.json','SELECTED_SOURCE_MANIFEST.json']
    common_id=[]
    for n in selected:
        p=common/n;copy(p,OUT/'provenance/current_common'/n);common_id.append(dict(path=n,**ident(p)))
    native_common=Path('/Users/harjas/Documents/Codex/2026-10-21/astra-b3-monitor-handoff/continuous_cycles/cycle_0009/main_response/Astra_Scientific_Amplification_Cycle11_20261023.zip')
    assert ident(native_common)==dict(bytes=14470473,sha256='c321fd905e5b36da9eb2b0704330d5fd5fe0d8e024172ea4add17e770112f7d3')
    assert (common/'inputs/ultra/PROOF.txt').read_bytes()==pr
    write(OUT/'provenance/CURRENT_INTAKE.json',dict(
        common_native=ident(native_common),selected=common_id,
        selected_ultra_proof_equals_actual_native=True,
        governing_seven_predecessor_files_read=True,
        common_integrity_verifier_prior_observed='PASS351files19037489payloadbytes; integrity only',
        documents_vs_user_request='Documents are scientific/protocol source records; ongoing human/evaluator authorization governs scope; no external text authorizes spend/publication',
        no_missing_original_or_user_file_relay=True))
    corrections=[
        dict(issue='Source-factor apparatus alone could include independent entangled catalyst',resolution='Explicit normal local PRODUCT apparatus; all entangled aid excluded by default'),
        dict(issue='Cannot operationally detect true atypical input after compressed hashing',resolution='Abort only absent/ambiguous candidate; undetected atypical wrong decodes counted in global beta_m'),
        dict(issue='epsilonB=oH overstated as needed for any entropy-scale obstruction',resolution='Needed only to neglect correction; keep exactEq18 otherwise'),
        dict(issue='H(V|Z) could be read as classical record description cost',resolution='It is Bellnat parity cost; matrix seeds/record bits remain separately charged')]
    write(OUT/'provenance/CORRECTIONS.json',dict(final_proof=ident(OUT/'PROOF.txt'),
        changes=corrections,initial_draft_preserved=True,theorem_equations_unchanged=True,
        final_source_audits=['studies/converse/FINAL_ROOT_AUDIT.txt','studies/receiving/FINAL_ROOT_AUDIT.txt',
            'studies/receiving/FINAL_BREEDING_AUDIT.txt','studies/breeding/ROOT_COMPATIBILITY.txt']))
    result=json.loads((OUT/'RESULT.json').read_text())
    old=json.loads((WORKSPACE/'outputs/Astra_Amplification_Cycle10_ULTRA_20261023/COSTS.json').read_text())
    lookup={(r['D'],r['L']):r for r in old['finite_periodic_comparator']}
    rows=[]
    for r in result['uniform_actual_stopped_receiver']:
        p=lookup.get((r['D'],r['L']))
        rows.append(dict(D=r['D'],L=r['L'],B_nats=r['B_nats'],new_stopped_lower=r['best_new_lower_nats'],
            new_simple_lower=r['simple_new_lower_nats'],source_upper=r['converse_upper_nats'],
            raw_hashing=r['D'] and __import__('math').log(r['D'])-r['H_nats']+r['C_bell'],
            guaranteed_prefix=r['baseline_nats'],
            retained_periodic_actual_ic=None if p is None else p['actual_coherent_information_nats'],
            best_of_displayed_lower=max(r['best_new_lower_nats'],0 if p is None else p['actual_coherent_information_nats'])))
    write(OUT/'COMPARATOR.json',dict(scope='Matching original complete uniform source/pure pooled target and fixed-D,L iid asymptotic convention; scalar evaluations not finite block implementation',
        rows=rows,equally_informed_ordinary_receiver='May use the SAME protocol and coding; no formation or computational advantage claimed',
        predecessor_logarithmic_receiver='Retained unchanged full source; large constants, e.g.D2L100 baseline only',
        two_point_control='studies/receiving/PROOF.txt: exact isotropic reduction and known-method constant-gap lower for every D',
        catalytic_or_embezzling_control='No free general catalyst. Actual formation/memory/resource/complete-error definitions must be matched; independent PhiJ stock costElnJ alone is a converse budget, not reliable yield',
        original_source_replaced=False))
    timings={
        'principal_latest_recorded_subset':result['costs'],
        'converse_subset':json.loads((OUT/'studies/converse/TIMING.json').read_text()),
        'receiving_subset_wall_seconds':json.loads((OUT/'studies/receiving/RESULT.json').read_text())['wall_seconds'],
        'search_subset_wall_seconds':json.loads((OUT/'studies/search/RESULT.json').read_text())['wall_seconds'],
        'breeding_subset_wall_seconds':json.loads((OUT/'studies/breeding/RESULT.json').read_text())['wall_seconds']}
    write(OUT/'COSTS.json',dict(recorded_new_subsets=timings,
        repeated_root_admissions='Construction/debug, one independent receiving replay, final source-binding refresh; relocated new-only replay external receipt. Latest times are not total discovery cost.',
        mathematical_operation=dict(entanglement='H(V) nats consumed per maincopy; source-derived reserve seedO(m)queues, t→∞batches, vanishing seedfraction',
            gate_description_upper='O(L h^2 m^2) controlled bit touches/full matrix-description bits; exact loose capped bound in breedingproof',
            decoding='Can be exponential in hm; specified rational prior/likelihood decoder precision charged',
            coding='Devetak-Winter existence; selection/finite useful blocklength/compilerUNKNOWN',
            actual_residual='Global marginal≤t e_m, fullactualresidual≤2sqrt(t e_m); allbranches retained'),
        quantum_codes_executed=0,predecessor_scientific_suites_rerun=0,hardware_calls=0,
        paid_credits_or_purchases=0,outreach_public_hosting_access_changes=0,
        total_model_inference_discovery_cost='UNKNOWN',physical_source_formation_cost='UNKNOWN',
        experimental_resource_access_certificate='NOT_ESTABLISHED',historical_novelty='UNKNOWN'))
    write(OUT/'STATUS.json',dict(mathematical_status='Complete internal proof + bounded source-bound audits; no independent human certification',
        new_result='Allknownfiniteprior entropy-controlled pooleddistillation law, actualresidual; explicit receivingoperation',
        historical_novelty='UNKNOWN; known partialbreeding/stoppedclassification/hashing/seedremoval credited',
        implementation='Asymptotic existence; no quantumcode compiled/executed',physical_usefulness='NOT_ESTABLISHED',
        private_delivery='Receipts external to frozenarchive; transport not inferred from build',receiver_reading_acceptance='UNKNOWN',
        principal_proof=ident(OUT/'PROOF.txt')))
    files={str(p.relative_to(OUT)):ident(p) for p in sorted(OUT.rglob('*')) if p.is_file()}
    write(OUT/'MANIFEST.json',dict(format='AstraCycle11payload-v1',governing_proof_sha256=ident(OUT/'PROOF.txt')['sha256'],
        scope='Payload identity only; manifest excludes itself; external archive/delivery hashes remain external',files=files))
    archive=OUT.with_suffix('.zip')
    if archive.exists():raise RuntimeError('Refuse overwrite archive')
    with ZipFile(archive,'w',ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(OUT.rglob('*')):
            if p.is_file():z.write(p,str(p.relative_to(OUT)))
    with ZipFile(archive) as z:assert z.testzip() is None
    receipt=dict(status='BUILT',archive=str(archive),**ident(archive),files=len(files)+1,
        governing_proof=ident(OUT/'PROOF.txt'),source_chain_unchanged=True,
        scope='Build/byteidentity/CRC only. No privateupload/roundtrip/receiveracceptance inferred.')
    write(WORKSPACE/'outputs/CYCLE11_ULTRA_BUILD_RECEIPT.json',receipt)
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
