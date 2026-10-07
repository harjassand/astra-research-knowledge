"""Root-centroid downstream certificate with charged held-out calibration.

All issued upper bounds use Fraction intervals and integer square roots.
Fixtures are fixed-tape software diagnostics, not evidence of a physical iid
source, Gaussian output sampling, or the probability theorem itself.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import random
import time

from entropy_table_certificate import log_interval, sqrt_interval


def root_coefficient_upper(v,bits=55):
    v=F(v)
    if v<1:
        raise ValueError('admitted r/gamma must be >=1')
    if v==1:
        return F(2)
    ln,_=log_interval(v,F(1,1<<bits))
    return min((2*v*v*ln[1]-v*v+1)/(v-1)**2,2+2*ln[1])


def certify(training, validation, modes, labels_count, r, ridge, confidence_delta,
            domination, requests, scale_window, epsilon, bits=55):
    r,ridge,delta,C,epsilon=map(F,(r,ridge,confidence_delta,domination,epsilon))
    t0,t1=map(F,scale_window)
    if not 0<ridge<=r or not 0<delta<1 or C<1 or requests<1 or not 0<t0<t1:
        raise ValueError('invalid acquisition contract')
    if modes<1 or labels_count<1 or not validation or not 0<epsilon<1:
        raise ValueError('invalid dimensionality/records/tolerance')
    sums=[[F(0)]*modes for _ in range(labels_count)]
    counts=[0]*labels_count
    for label,row in training:
        row=list(map(F,row))
        if not 0<=label<labels_count or len(row)!=modes or not all(0<=x<=r for x in row):
            raise ValueError('training field violates supplied range')
        counts[label]+=1
        for i,x in enumerate(row): sums[label][i]+=x
    codebook=[[sums[j][i]/counts[j]+ridge if counts[j] else ridge
               for i in range(modes)] for j in range(labels_count)]
    assert all(ridge<=x<=r+ridge for row in codebook for x in row)
    losses=[]
    for label,row in validation:
        row=list(map(F,row))
        if not 0<=label<labels_count or len(row)!=modes or not all(0<=x<=r for x in row):
            raise ValueError('validation field violates supplied range')
        losses.append(sum((x-q)**2 for x,q in zip(row,codebook[label])))
    W=modes*(r+ridge)**2
    assert all(0<=x<=W for x in losses)
    N=len(losses)
    mean_loss=sum(losses)/N
    log_confidence,_=log_interval(1/delta,F(1,1<<bits))
    root_radius=sqrt_interval(log_confidence[1]/(2*N),bits)[1]
    loss_upper=mean_loss+W*root_radius
    coefficient=root_coefficient_upper(r/ridge,bits)
    risk_upper=coefficient*loss_upper
    scale_normalization=1/t0-1/t1
    cw=1/scale_normalization
    tv2=F(requests)*C*cw*risk_upper/4
    status='CERTIFIED_UNDER_IID_AND_MODEL_CONTRACT' if tv2<=epsilon*epsilon else 'UNKNOWN'
    record_data={'training':[[j,[str(F(x)) for x in row]] for j,row in training],
                 'validation':[[j,[str(F(x)) for x in row]] for j,row in validation]}
    return {'status':status,'m':modes,'D':labels_count,'archive_bits':max(0,(labels_count-1).bit_length()),
            'training_source_draws':len(training),'held_out_source_draws':N,
            'scalar_field_values_read':(len(training)+N)*modes,
            'r':str(r),'ridge':str(ridge),'codebook_roots':[[str(x) for x in row] for row in codebook],
            'codebook_covariances':[[str(x*x) for x in row] for row in codebook],
            'training_cell_counts':counts,'loss_range_upper':str(W),
            'empirical_loss':str(mean_loss),'confidence_radius_upper':str(W*root_radius),
            'mean_loss_upper':str(loss_upper),'root_coefficient_upper':str(coefficient),
            'reference_divergence_risk_upper':str(risk_upper),'confidence_delta':str(delta),
            'domination_C':str(C),'requested_observations':requests,'scale_window':[str(t0),str(t1)],
            'scale_density_envelope_cw':str(cw),'target_epsilon':str(epsilon),
            'TV_squared_upper_rational':str(tv2),'TV_upper_float_display_only':float(tv2)**.5,
            'record_sha256':hashlib.sha256(json.dumps(record_data,sort_keys=True).encode()).hexdigest(),
            'precision_bits':bits,
            'scope':'Valid under supplied PSD field range, iid source/evaluator, frozen classifier/codebook, reference domination and ideal Gaussian/scale decoder contracts. Issued bound rational; no physical sampler or continuous-TV digital claim.'}


def main():
    start=time.perf_counter()
    fields=[[F(1,16),F(1,8)],[F(3,16),F(1,4)]]
    # The classifier is FIXED and exactly reads the known finite state label.
    # Separate seeded tapes exercise record handling; no statistical validity
    # is inferred from pseudorandomness or this observed fixed-tape run.
    train_rng=random.Random(6002)
    valid_rng=random.Random(6003)
    training=[]
    validation=[]
    for _ in range(32):
        j=train_rng.randrange(2);training.append((j,fields[j]))
    for _ in range(1024):
        j=valid_rng.randrange(2);validation.append((j,fields[j]))
    args=dict(training=training,validation=validation,modes=2,labels_count=2,r=F(1,4),
              ridge=F(1,64),confidence_delta=F(1,10),domination=F(2),requests=3,
              scale_window=(F(1),F(2)))
    reports=[certify(**args,epsilon=eps) for eps in (F(1,3),F(1,10))]
    assert all(x>0 for x in reports[0]['training_cell_counts'])
    assert reports[0]['status']=='CERTIFIED_UNDER_IID_AND_MODEL_CONTRACT'
    assert reports[1]['status']=='UNKNOWN'
    codebook=[[F(x) for x in row] for row in reports[0]['codebook_roots']]
    exact_population_loss=sum(sum((x-q)**2 for x,q in zip(row,code)) for row,code in zip(fields,codebook))/2
    assert exact_population_loss==F(2,64*64)
    assert exact_population_loss<=F(reports[0]['mean_loss_upper'])
    result={'status':'PASS_EXACT_DIAGONAL_CALIBRATION_DIAGNOSTIC','reports':reports,
            'fixture_reference_probabilities':['1/2','1/2'],'fixture_root_fields':[[str(x) for x in row] for row in fields],
            'exact_fixture_population_loss':str(exact_population_loss),
            'elapsed_seconds':time.perf_counter()-start,
            'evidence_boundary':'Records are fixed pseudorandom-tape fixtures; iid/range/domination hypotheses are admitted, not acquired from this diagnostic. Gaussian output primitive is not implemented. Failure at tighter epsilon is preserved as UNKNOWN.'}
    out=Path(__file__).with_name('root_calibration_checks.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'training':32,'validation':1024,
                      'acceptance_statuses':[r['status'] for r in reports],
                      'TV_upper_display_only':reports[0]['TV_upper_float_display_only'],
                      'elapsed_seconds':result['elapsed_seconds'],'output':str(out)},indent=2))


if __name__=='__main__':main()
