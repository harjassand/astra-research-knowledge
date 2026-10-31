"""Finite full-rate accuracy from one extra exact scalar resistance integral."""
from pathlib import Path
from fractions import Fraction as F
from time import perf_counter
import hashlib,importlib.util,json

SOURCE=Path(__file__).resolve().parent.parent/'acquired_quartic_consumer'/'compile.py'
SOURCE_SHA='45d75db5d0dac774df58070c66d11e9f7d0918bdd903489fdf71b61b9ea03fbf'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA:
    raise RuntimeError('frozen raw/scalar source hash mismatch')
spec=importlib.util.spec_from_file_location('frozen_jensen_scalar',SOURCE)
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
Unknown=base.Unknown
TASK_KEYS={'beta','quad_relative','max_dimension','max_terms','max_coefficient_bits','max_grid',
           'max_points','max_cutoff','max_precision','max_power_bits'}

class PlusIntegrator(base.Integrator):
    def point(self,y):
        if y in self.cache:return self.cache[y]
        if len(self.cache)>=self.max_points:raise Unknown('total scalar evaluation budget exhausted by extra resistance')
        if not F(0)<=y<=F(1,2):raise Unknown('Jensen scalar evaluation outside proven monotone slab')
        a=1+self.kappa;v=1+self.kappa*(1-y*y)**2
        r=a*a/(2*a-v);power=self.power(r,self.m)
        out=(0,0),base.root_bounds(power,self.p)
        self.cache[y]=out;return out

def certify(raw,full_ratio=None,**external_task):
    start=perf_counter()
    if full_ratio is not None and (type(full_ratio)is not F or full_ratio<=1):
        raise Unknown('requested full ratio must be an exact Fraction >1 or None')
    if not set(external_task)<=TASK_KEYS:raise Unknown('unknown external task parameter')
    # Base validates every task/budget before raw work; extension input-size check
    # is also done before acquisition using the same effective coefficient budget.
    cb=external_task.get('max_coefficient_bits',65536)
    if type(cb)is not int or cb<=0:raise Unknown('strict coefficient budget')
    if full_ratio is not None and base.bits(full_ratio)>cb:raise Unknown('requested ratio input bit budget')
    out=base.certify(raw,**external_task)
    remaining=out['task']['max_points']-out['point_evaluations']
    if remaining<=0:raise Unknown('no paid evaluations remain for extra scalar integral')
    m=out['acquisition']['m'];kappa=F(out['acquisition']['kappa']);p=out['precision_bits']
    ii=PlusIntegrator(m,kappa,p,remaining,out['task']['max_power_bits'])
    lo,hi=ii.integrate(F(0),F(1,2),out['N'],1);plus=2*lo,2*hi
    mass=F(out['mass']['lower']),F(out['mass']['upper'])
    rr=F(out['resistance']['lower']),F(out['resistance']['upper'])
    beta=F(out['task']['beta'])
    if plus[0]<=0:raise Unknown('extra resistance unresolved at fixed precision')
    full=1/(beta*mass[1]*plus[1]),1/(beta*mass[0]*rr[0])
    ratio=full[1]/full[0]
    if full_ratio is not None and ratio>full_ratio:
        raise Unknown('computed finite Jensen bracket does not meet requested full ratio; tighter quadrature or this structural method may be insufficient')
    out['schema']='homogeneous_finite_jensen_capacity.v1'
    out['structural_method']='fixed_fiber_Cauchy_homogeneous_Gamma_Jensen_exact_extra_resistance'
    out['scalar_source_sha256']=SOURCE_SHA
    out['requested_full_ratio']=None if full_ratio is None else base.rational_string(full_ratio)
    out['jensen_resistance']=base.interval(plus)
    out['structural_ratio']=base.interval((max(F(1),plus[0]/rr[1]),plus[1]/rr[0]))
    out['full_rate']=base.interval(full)
    out['full_ratio_exact']=base.rational_string(ratio)
    # No old radial factor is used as a receiving premise or advertised factor.
    del out['factor_upper']
    out['additional_point_evaluations']=len(ii.cache)
    out['total_scalar_evaluations']=out['point_evaluations']+len(ii.cache)
    out['additional_power_calls']=ii.power_calls
    out['additional_max_power_integer_bits']=ii.max_power_integer_bits
    out['seconds']=perf_counter()-start
    return out

def verify(raw,certificate,full_ratio=None,**external_task):
    expected=certify(raw,full_ratio=full_ratio,**external_task)
    if type(certificate)is not dict:raise Unknown('certificate record')
    for k in ['schema','structural_method','scalar_source_sha256','requested_full_ratio','full_ratio_exact',
              'task','b','observable','basins','N','T','tail_upper','precision_bits']:
        if not base.same_typed(certificate.get(k),expected[k]):raise Unknown('strict task/proof binding: '+k)
    if 'factor_upper' in certificate:raise Unknown('stale radial factor field')
    got=certificate.get('acquisition')
    if type(got)is not dict or not base.same_typed({k:v for k,v in got.items() if k!='seconds'},
                                                {k:v for k,v in expected['acquisition'].items() if k!='seconds'}):
        raise Unknown('strict raw polynomial/acquisition binding')
    for k in ['mass','resistance','free_rate','jensen_resistance','structural_ratio','full_rate']:
        if type(certificate.get(k))is not dict:raise Unknown('interval schema')
        for side in ['lower','upper']:
            if not base.same_typed(certificate[k].get(side),expected[k][side]):raise Unknown('exact interval binding')
    return {'status':'PASS','scope':'finite Jensen raw coupled quartic full capacity/mass',
            'physical_m':expected['acquisition']['m'],'full_ratio_exact':expected['full_ratio_exact']}

def main():
    out=[]
    for m,delta,target in [(2,F(1,100),None),(4,F(1,100),None),(16,F(1,100),None),
                            (64,F(1,100),None),(128,F(1,200),None),(256,F(1,200),F(103,100)),
                            (512,F(1,1000),F(101,100))]:
        raw=base.fixture(m);cert=certify(raw,quad_relative=delta,full_ratio=target)
        out.append({'m':m,'quad_relative':str(delta),'requested_full_ratio':None if target is None else str(target),'certificate':cert})
        print(json.dumps({'m':m,'lower':cert['full_rate']['lower_display'],'upper':cert['full_rate']['upper_display'],
                          'full_ratio':float(F(cert['full_ratio_exact'])),'evaluations':cert['total_scalar_evaluations'],
                          'seconds':cert['seconds']}),flush=True)
    Path('finite_results.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
