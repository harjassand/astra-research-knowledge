"""Separate exact receiver for the partition-free parallel-channel theorem.
The frozen radial consumer is reused only for raw acquisition/scalar integration.
Its original source and output files are never modified by this module.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,importlib.util,json
from time import perf_counter

SOURCE=Path(__file__).resolve().parent.parent/'acquired_quartic_consumer'/'compile.py'
SOURCE_SHA='45d75db5d0dac774df58070c66d11e9f7d0918bdd903489fdf71b61b9ea03fbf'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA:
    raise RuntimeError('frozen raw acquisition/scalar arithmetic source hash mismatch')
spec=importlib.util.spec_from_file_location('frozen_quartic_scalar',SOURCE)
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
Unknown=base.Unknown
TASK_KEYS={'beta','quad_relative','max_dimension','max_terms','max_coefficient_bits','max_grid',
           'max_points','max_cutoff','max_precision','max_power_bits'}


def certify(raw,**external_task):
    start=perf_counter()
    if not set(external_task)<=TASK_KEYS:raise Unknown('unknown external task parameter')
    out=base.certify(raw,**external_task)
    kappa=F(out['acquisition']['kappa'])
    square=(16+23*kappa)/(14*(1+kappa));p=out['precision_bits']
    if base.bits(square)+2*p>out['task']['max_power_bits']:
        raise Unknown('parallel factor root-shift budget')
    lo,hi=base.root_bounds(square,p,2)
    factor=F(hi,1<<p)
    free=F(out['free_rate']['lower']),F(out['free_rate']['upper'])
    out['schema']='homogeneous_parallel_capacity.v1'
    out['structural_method']='fixed_fiber_Cauchy_homogeneous_Gamma_Jensen_slab_contraction'
    out['scalar_source_sha256']=SOURCE_SHA
    out['factor_squared_exact']=base.rational_string(square)
    out['factor_upper']=base.rational_string(factor)
    out['full_rate']=base.interval((free[0]/factor,free[1]))
    out['seconds']=perf_counter()-start
    return out


def verify(raw,certificate,**external_task):
    expected=certify(raw,**external_task)
    if type(certificate)is not dict:raise Unknown('certificate record')
    for k in ['schema','structural_method','scalar_source_sha256','factor_squared_exact','task','b',
              'observable','basins','factor_upper','N','T','tail_upper','precision_bits']:
        if not base.same_typed(certificate.get(k),expected[k]):raise Unknown('strict task/proof binding: '+k)
    got=certificate.get('acquisition')
    if type(got)is not dict or not base.same_typed({k:v for k,v in got.items() if k!='seconds'},
                                                {k:v for k,v in expected['acquisition'].items() if k!='seconds'}):
        raise Unknown('strict raw polynomial/acquisition binding')
    for k in ['mass','resistance','free_rate','full_rate']:
        if type(certificate.get(k))is not dict:raise Unknown('interval schema')
        for side in ['lower','upper']:
            if not base.same_typed(certificate[k].get(side),expected[k][side]):raise Unknown('exact interval binding')
    return {'status':'PASS','scope':'raw coupled quartic parallel-channel full capacity/mass',
            'physical_m':expected['acquisition']['m']}


def main():
    out=[]
    for m in [2,3,4,16,64,128,256]:
        raw=base.fixture(m);cert=certify(raw);out.append({'m':m,'certificate':cert})
        print(json.dumps({'m':m,'rate_lower':cert['full_rate']['lower_display'],
                          'rate_upper':cert['full_rate']['upper_display'],'factor':float(F(cert['factor_upper'])),
                          'seconds':cert['seconds']}),flush=True)
    Path('parallel_results.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
