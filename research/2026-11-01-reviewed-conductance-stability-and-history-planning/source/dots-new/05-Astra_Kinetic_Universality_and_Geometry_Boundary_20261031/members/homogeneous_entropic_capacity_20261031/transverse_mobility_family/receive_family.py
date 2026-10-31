"""Universally quantified unknown-transverse-mobility family receiving.
No actual physical model membership or inverse mobility is authenticated.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,importlib.util,json

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'finite_jensen_receiver'/'receive_jensen.py'
SOURCE_SHA='430d5e82d4ee782cd5fe8069635b4601c54c6b15426dc774ad3ac9f818b00769'
PROOF=HERE/'EXACT_MOBILITY_RANGE_CANDIDATE.md'
PROOF_SHA='ff8b132c42a37567f832a397ee53b64e7a34b3aabad39fe55aa327181ccd52c9'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA or hashlib.sha256(PROOF.read_bytes()).hexdigest()!=PROOF_SHA:
    raise RuntimeError('finite engine or family theorem source hash mismatch')
spec=importlib.util.spec_from_file_location('received_finite_engine',SOURCE)
engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)
base=engine.base;Unknown=engine.Unknown
FAMILY='all_fixed_transverse_SPD'


def family_descriptor():
    # Fresh nested data on every call, never a caller-mutable shared prototype.
    return {'quantifier':'for every constant finite symmetric positive-definite transverse matrix M',
            'longitudinal_mobility':'1','cross_mobility':'zero',
            'transverse_drift':'-v(y) M grad U(z)',
            'transverse_noise_covariance_per_time':'2 M / beta',
            'actual_physical_membership':'not authenticated',
            'matrix_entries_required':False,
            'excluded':['singular M','variable M','cross mobility','changed longitudinal mobility',
                        'nonreversible drift','time dependent control']}


def range_descriptor(m):
    return {'kind':'exact open attainable rate range characterization',
            'alpha':str(F(m,4)),
            'lower_endpoint':'k_parallel = integral_0^infinity t^(alpha-1)/R(t) dt / (beta MA Gamma(alpha))',
            'upper_endpoint':'k_free = 1/(beta MA R0)',
            'R_definition':'R(t) = integral_-1/2^1/2 exp(v(y)*t) dy',
            'MA_definition':'MA = integral_1/2^infinity v(y)^(-alpha) dy',
            'R0_definition':'R0 = integral_-1/2^1/2 v(y)^alpha dy',
            'endpoints_attained':False,
            'lower_endpoint_numerically_evaluated':False,
            'realizing_mobility_constructed':False,
            'path_statement':'for each fixed SPD shape B, gamma*B strictly continuously spans the open range'}


def certify(raw,*,family=FAMILY,full_ratio=None,**external_task):
    if type(family)is not str or family!=FAMILY:raise Unknown('unsupported universally quantified model family')
    out=engine.certify(raw,full_ratio=full_ratio,**external_task)
    out['schema']='homogeneous_unknown_mobility_family.v1'
    out['structural_method']='exact_transverse_SPD_open_range_with_finite_Jensen_outer_enclosure'
    out['finite_source_sha256']=SOURCE_SHA;out['range_proof_sha256']=PROOF_SHA
    out['family_task']=family;out['kinetic_family']=family_descriptor()
    out['exact_attainable_set']=range_descriptor(out['acquisition']['m'])
    out['observable']='for every declared M: cap_mu,M(A,B)/mu(A)'
    out['numerical_scope']='closed outer enclosure of the exact open attainable range; neither numerical endpoint claimed attained'
    out['uniform_rate_enclosure']=out.pop('full_rate')
    return out


def verify(raw,certificate,*,family=FAMILY,full_ratio=None,**external_task):
    expected=certify(raw,family=family,full_ratio=full_ratio,**external_task)
    if type(certificate)is not dict:raise Unknown('certificate record')
    for k in ['schema','structural_method','finite_source_sha256','range_proof_sha256','family_task','kinetic_family',
              'exact_attainable_set','numerical_scope','scalar_source_sha256','requested_full_ratio','full_ratio_exact',
              'task','b','observable','basins','N','T','tail_upper','precision_bits']:
        if not base.same_typed(certificate.get(k),expected[k]):raise Unknown('strict family/task/proof binding: '+k)
    if 'full_rate'in certificate or 'factor_upper'in certificate:raise Unknown('stale isotropic/radial scope field')
    got=certificate.get('acquisition')
    if type(got)is not dict or not base.same_typed({k:v for k,v in got.items() if k!='seconds'},
                                                {k:v for k,v in expected['acquisition'].items() if k!='seconds'}):
        raise Unknown('strict original raw acquisition binding')
    for k in ['mass','resistance','free_rate','jensen_resistance','structural_ratio','uniform_rate_enclosure']:
        if type(certificate.get(k))is not dict:raise Unknown('interval schema')
        for side in ['lower','upper']:
            if not base.same_typed(certificate[k].get(side),expected[k][side]):raise Unknown('exact interval binding')
    return {'status':'PASS','scope':'universal fixed-transverse-SPD family, exact open-range theorem and finite outer interval',
            'actual_physical_membership':'not authenticated','matrix_or_inverse_solver':'not supplied',
            'physical_m':expected['acquisition']['m'],'full_ratio_exact':expected['full_ratio_exact']}


def main():
    raw=base.fixture(512)
    cert=certify(raw,full_ratio=F(101,100),quad_relative=F(1,1000))
    Path('family_513D_certificate.json').write_text(json.dumps(cert,indent=2))
    print(json.dumps({'n':513,'interval':cert['uniform_rate_enclosure'],
                      'ratio_display':float(F(cert['full_ratio_exact'])),'matrix_entries_used':0},indent=2))
if __name__=='__main__':main()
