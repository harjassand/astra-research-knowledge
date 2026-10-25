"""Record-only acquisition and replay. No native model or hidden states read."""
from pathlib import Path
from fractions import Fraction as F
from math import comb,log,sqrt
import json
import numpy as np
ROOT=Path(__file__).resolve().parent
AXES=[1,3,2]
CHAR=np.array([[1-2*(((d&1)*(p>>1)+(d>>1)*(p&1))&1) for p in AXES]
               for d in range(4)],dtype=np.int8)

def popcount(words):
    a=np.asarray(words,dtype='<u8')
    return np.unpackbits(a[...,None].view(np.uint8),axis=-1,bitorder='little').sum(axis=-1)

def contexts(words,length):
    bits=(popcount(words)>length//2).astype(np.uint8)
    return np.sum(bits*(1<<np.arange(6,dtype=np.uint8)),axis=1).astype(np.uint8)

def tail(eta,length):
    plus=(1+eta)/2
    return sum((F(comb(length,j))*plus**j*(1-plus)**(length-j)
                for j in range(length//2+1)),F())

def acquire(record,protocol):
    c=contexts(record['syndrome_words'],protocol['inner_read_length'])
    axis=record['axis'];standard=np.array(protocol['standard_policy'],dtype=np.uint8)
    assert np.array_equal(record['applied_repair'],standard[c])
    n=len(c);length=protocol['training_audit_length']
    score=(1-2*(popcount(record['pre_words'])>length//2).astype(np.int8))
    score*=1-2*(popcount(record['post_words'])>length//2).astype(np.int8)
    rawscore=score*CHAR[record['applied_repair'],axis]
    counts=np.bincount(c,minlength=64);totals=np.zeros((64,4),dtype=np.int64)
    for d in range(4):np.add.at(totals[:,d],c,rawscore*CHAR[d,axis])
    policy=totals.argmax(axis=1).astype(np.uint8)
    ties=totals[np.arange(64),standard]==totals.max(axis=1)
    policy[ties]=standard[ties]
    eta=F(protocol['eta']);gamma=(1-2*tail(eta,length))**2;delta=F(1,100)
    regret=(3/(2*float(gamma)))*sqrt(2*(64*log(4)+log(2/float(delta)))/n)
    wobs=(counts[:,None]+3*totals/float(gamma))/(4*n)
    return {'policy':policy.tolist(),'counts':counts.tolist(),'score_totals':totals.tolist(),
            'calibration_rounds':n,'paired_gain':str(gamma),
            'calibration_mixture_regret_bound_display':min(1,regret),
            'regret_failure_probability':'1/100',
            'regret_scope':'Actual calibration-memory history; no transfer to arbitrary future memory.',
            'observed_joint_task_weights_unprojected':wobs.tolist(),
            'changed_standard_contexts':int(np.count_nonzero(policy!=standard))}

def validate(record,protocol,acquisition):
    n=protocol['packet_length'];length=protocol['validation_audit_length']
    policy=np.asarray(acquisition['policy'],dtype=np.uint8)
    c=contexts(record['syndrome_words'],protocol['inner_read_length'])
    assert np.array_equal(record['applied_repair'],policy[c])
    positions=record['payload_positions'];packets=len(positions)
    assert len(c)==n*packets
    audit=np.ones((packets,n),bool);audit[np.arange(packets),positions]=False
    good=((popcount(record['pre_words'])>length//2)==(popcount(record['post_words'])>length//2))
    accepted=np.all(good.reshape(packets,n)|~audit,axis=1)
    assert np.array_equal(accepted,record['accepted'])
    eta=F(protocol['eta']);gamma=(1-2*tail(eta,length))**2
    a=(1+gamma)/2;b=(1-gamma/3)/2
    assert b/a<=F(1,2)
    beta=a**(n-1)/n
    return {'record_only':True,'hidden_model_or_errors_read':False,
            'payloads_attempted':packets,'payloads_accepted':int(accepted.sum()),
            'macro_calls':n*packets,'audited_macros':int(audit.sum()),
            'raw_native_CNOTs':protocol['native_CNOTs_per_macro']*n*packets,
            'forward_carriers':7*n*packets,
            'accepted_error_weight_upper_exact':str(F(1,n)),
            'sharp_accepted_error_weight_display':float(beta),
            'ideal_macro_acceptance_display':float(a**(n-1)),
            'conditioning_rule':'For independent payload/reference vs apparatus, divide weighted bound by actual acceptance probability; no fine-record posterior guarantee.',
            'physical_scope':'Local buffers/routing/full probes and private coordination are trusted/charged; all encoder/link/decoder faults are inside each unknown native macro.'}

def main():
    protocol=json.loads((ROOT/'transmission_protocol.json').read_text())
    with np.load(ROOT/'received_training.npz') as rec:acquisition=acquire(rec,protocol)
    with np.load(ROOT/'received_validation.npz') as rec:certificate=validate(rec,protocol,acquisition)
    (ROOT/'acquired_decoder.json').write_text(json.dumps(acquisition,indent=2)+'\n')
    (ROOT/'transmission_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print(json.dumps({'training_rounds':acquisition['calibration_rounds'],
                      'changed_standard_contexts':acquisition['changed_standard_contexts'],
                      'certificate':certificate},indent=2))

if __name__=='__main__':main()
