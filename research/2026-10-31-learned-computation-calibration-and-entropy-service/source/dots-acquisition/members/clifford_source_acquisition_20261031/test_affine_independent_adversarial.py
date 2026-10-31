"""Supplemental semantic verifier and independent affine realization checks."""
import copy,hashlib,json,random
from pathlib import Path
from compile_affine_source import (compile_affine,verify_affine,validate_affine,
                                  affine_action,inverse_matrix,linear,digest,nilpotence_index)
from acquire_clifford_source import acquire
from test_affine_source import dense_check

def refresh_actual(c):
    c=copy.deepcopy(c);p=c['source_program'];n=p['n'];mask=(1<<n)-1
    cs,offset=affine_action(p,p['env']);inv=inverse_matrix(cs)
    c['reverse_section_columns']=[v&mask for v in inv[:n]]
    c['reverse_fibre_columns']=[v&mask for v in inv[n:]]
    c['reverse_affine_offset']=linear(inv,offset)&mask
    c['nilpotence_horizon']=nilpotence_index(c['reverse_section_columns'])
    c['source_certificate']=acquire(p)
    return c

def run():
    raw={'n':2,'F_columns':[2,1],'G_columns':[1],'offset':0};cert=compile_affine(raw)
    same_law=0
    for off in [0,1]:
        for mask in range(4):
            changed=copy.deepcopy(raw);changed['offset']=off
            changed['F_columns']=[v^((mask>>j)&1) for j,v in enumerate(raw['F_columns'])]
            c=copy.deepcopy(cert);c['input_digest']=digest(changed)
            assert verify_affine(changed,c)
            dense_check(changed,c);same_law+=1
    # More/reordered redundant random bits: image uniformity, not raw coin identity.
    for noise in [[0,1],[1,1,0],[0,1,1,1],[1,0,0,1,1]]:
        changed=copy.deepcopy(raw);changed['G_columns']=noise
        c=copy.deepcopy(cert);c['input_digest']=digest(changed);c['original_noise_bits']=len(noise)
        assert verify_affine(changed,c);dense_check(changed,c);same_law+=1
    wrong=0
    for off in [2,3]:
        changed=copy.deepcopy(raw);changed['offset']=off
        c=copy.deepcopy(cert);c['input_digest']=digest(changed)
        assert not verify_affine(changed,c);wrong+=1
    # Reacquire source proofs and refresh all claimed actual inverse data.
    # X on the noise direction preserves the law; X on its quotient does not.
    for target,expected in [(0,True),(1,False)]:
        c=copy.deepcopy(cert);c['source_program']['gates'].append(['X',target]);c=refresh_actual(c)
        assert verify_affine(raw,c) is expected
        if expected:dense_check(raw,c)
        else:wrong+=1
    malformed=[None,[],0,'bad',{},dict(cert,source_program=None),dict(cert,source_program=[]),
               dict(cert,source_certificate=None),dict(cert,source_certificate=[]),
               dict(cert,source_program=dict(cert['source_program'],gates=None)),
               dict(cert,reachable_basis=[0]),dict(cert,equivalence_scope='all quantum processes'),
               dict(cert,original_coin_records_preserved=0),dict(cert,original_coin_records_preserved=True),
               dict(cert,arbitrary_original_quantum_dilation_preserved=True),dict(cert,nilpotence_horizon=0)]
    for c in malformed:assert verify_affine(raw,c) is False
    invalid=[None,[],{},dict(raw,n=True),dict(raw,n=0),dict(raw,F_columns=[2]),
             dict(raw,F_columns=[2,False]),dict(raw,G_columns=[-1]),dict(raw,G_columns=[4]),
             dict(raw,G_columns=()),dict(raw,offset=True),dict(raw,offset=4),dict(raw,extra=1)]
    for p in invalid:
        try:validate_affine(p)
        except ValueError:continue
        raise AssertionError('Malformed raw program accepted')
    outside=0
    for noise in [[],[0],[0,0,0]]:
        p=dict(raw,G_columns=noise)
        c=compile_affine(p)
        assert c['status']=='outside_controllable_uniform_class' and verify_affine(p,c)
        c['status']='synthesized_uniform_pure_return'
        assert not verify_affine(p,c)
        outside+=1
    rng=random.Random(883906);cases=admitted=0
    for n in [1,2,3]:
        for _ in range(30):
            gs=[rng.randrange(1<<n) for j in range(rng.randrange(0,5))]
            p={'n':n,'F_columns':[rng.randrange(1<<n) for j in range(n)],'G_columns':gs,'offset':rng.randrange(1<<n)}
            c=compile_affine(p);assert verify_affine(p,c);dense_check(p,c)
            cases+=1;admitted+=c['status']=='synthesized_uniform_pure_return'
    root=Path(__file__).parent
    record={'source_sha256':hashlib.sha256((root/'compile_affine_source.py').read_bytes()).hexdigest(),
            'same_law_quotient_and_redundant_noise_acceptances':same_law,
            'different_law_rejections_despite_refreshed_digest_or_source_proof':wrong,
            'fresh_source_proof_noise_direction_gate_change_accepted':True,
            'malformed_certificates_rejected':len(malformed),'malformed_programs_rejected':len(invalid),
            'empty_zero_noise_outside_class_cases':outside,'new_random_cases':cases,
            'new_random_admitted_dense_cases':admitted,'passed':True}
    path=root/'affine_independent_adversarial_checks.json';path.write_text(json.dumps(record,indent=2)+'\n');print(path.read_text())

if __name__=='__main__':run()
