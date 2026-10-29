"""One fixed same-target full-velocity comparison plus two finite-word paths.

No rerun-until-pass, source/time grid, empirical1e-12 accuracy or literal
fair-bit claim. The source's small anisotropy is not statistically resolved.
"""
from pathlib import Path
from dataclasses import asdict
import importlib.util,json,math,random,time
from nonradial_query import Query,D,DELTA,DEFF,ZBETA,phi,initial_h,source_a,norm2


class WordQuery(Query):
    def __init__(self,kind):
        super().__init__(202610299501,trace=True);self.kind=kind;self.wait_word=iter([.001,1e6,1e6])
    def wait_exp(self):
        self.counts.exponentials+=1;return next(self.wait_word)
    def top_uniform(self,pg,pl):
        self.counts.uniforms+=1;return pg/2 if self.kind=='gain' else pg+pl/2
    def thin_uniform(self):
        self.counts.uniforms+=1;return .1


class CountedRandom(random.Random):
    def __init__(self,seed):
        super().__init__(seed);self.uniform_calls=0;self.exponential_calls=0;self.normal_calls=0
    def random(self):self.uniform_calls+=1;return super().random()
    def expovariate(self,lambd=1.):
        self.exponential_calls+=1;return -math.log(1-self.random())/lambd
    def native_normal(self):
        self.normal_calls+=1
        return math.sqrt(2*self.expovariate())*math.cos(2*math.pi*self.random())
    def sphere(self):
        z=2*self.random()-1;angle=2*math.pi*self.random();r=math.sqrt(max(0.,1-z*z))
        return (r*math.cos(angle),r*math.sin(angle),z)


class Source:
    energy=3.
    def __init__(self):self.proposals=0;self.rejections=0
    def draw(self,rng,a,tilted=False):
        while True:
            self.proposals+=1
            if not tilted or rng.random()<a/(a+3):v=tuple(rng.native_normal() for _ in range(3))
            else:
                r=math.sqrt(rng.native_normal()**2+2*rng.expovariate()+2*rng.expovariate())
                v=tuple(r*x for x in rng.sphere())
            if rng.random()<(1+DELTA*source_a(v))/(1+DELTA):return v
            self.rejections+=1


def main():
    root=Path(__file__).parent;start=time.perf_counter();paths=[]
    for kind in ('gain','loss'):
        q=WordQuery(kind);v=(2.,1.,.5);out=q.query(v,1.)
        assert len(q.trace)==1 and q.counts.nodes==3 and q.counts.terminal_exits==2
        child0,child1=q.trace[0]['children']
        expected=D*phi(v)*(initial_h(child0)/D)*(initial_h(child1)/D)*(1 if kind=='gain' else -1)
        assert abs(out-expected)<1e-16
        paths.append({'kind':kind,'scope':'prescribed event/clock word; native random partner+elastic directions; NOT iid',
                      'value':out,'independent_leaf_product':expected,'events':q.trace,'counts':q.receipt()})
    q=Query(202610299510);tick=time.perf_counter()
    outputs=[q.continuous(1.) for _ in range(128)]
    newtime=time.perf_counter()-tick
    new={'method':'positive clipped bounded-query continuous consumer','time':1.,'n':128,'seed':202610299510,
         'outputs':outputs,'seconds':newtime,'counts':q.receipt(),
         'ideal_real_TV_contract':'<=1e-12 uniformly in time; sharper Gaussian bound in STATIC_CERTIFICATE',
         'float_arithmetic_or_PRNG_TV_certified':False}
    (root/'CONSUMER_PARTIAL.json').write_text(json.dumps({'native_paths':paths,'new':new},indent=2)+'\n')
    # Read-only reuse of the established full-law currency implementation.
    path=root.parent/'t_velocity_rate/hard_sphere.py'
    spec=importlib.util.spec_from_file_location('ordinary_hard_sphere',path)
    ordinary=importlib.util.module_from_spec(spec)
    import sys
    sys.modules[spec.name]=ordinary;spec.loader.exec_module(ordinary)
    source=Source();solver=ordinary.HardSphere(source,a=3.,seed=202610299511)
    solver.rng=CountedRandom(202610299511);counts=ordinary.Counts()
    tick=time.perf_counter();base=[solver.physical(1.,counts) for _ in range(128)]
    basetime=time.perf_counter()-tick
    old={'method':'normalized full hard-sphere currency lineage','time':1.,'n':128,'seed':202610299511,
         'outputs':base,'seconds':basetime,'counts':asdict(counts),
         'source_proposals':source.proposals,'source_rejections':source.rejections,
         'all_uniform_calls':solver.rng.uniform_calls,
         'all_exponential_calls':solver.rng.exponential_calls,'all_source_normal_calls':solver.rng.normal_calls,
         'ideal_real_contract':'exact normalized f_t, hence same1e-12 target',
         'Gaussian_source_termination_extension':'ORDINARY_COMPARATOR.md',
         'float_arithmetic_or_PRNG_TV_certified':False}
    # Same explicit admitted error is given to a much cheaper ordinary Gaussian
    # route. At t1 it does not certify the requested1e-12, no failure inferred.
    rng=CountedRandom(202610299512);tick=time.perf_counter()
    gaussian=[tuple(rng.native_normal() for _ in range(3)) for _ in range(128)]
    gaussian_time=time.perf_counter()-tick
    tv=DEFF*ZBETA/2;rate=2*math.sqrt(2/math.pi)/400
    out={'status':'EXECUTED_FLOAT_DIAGNOSTIC_ONLY','source':'N14 anisotropic f_delta, delta2^-14',
         'native_paths':paths,'new':new,'ordinary_exact_lineage':old,
         'ordinary_Gaussian':{'outputs':gaussian,'seconds':gaussian_time,
                              'paid_TV_at_t1':tv*math.exp(-rate),
                              'requested_TV':1e-12,'requested_accuracy_paid_at_t1':False,
                              'future_time_qualifying_requested_TV':math.log(tv/1e-12)/rate},
         'new_observed_negative_clippings':q.counts.negative_clippings,
         'tiny_anisotropy_statistically_resolved':False,
         'practical_or_all_solver_advantage_claim':False,
         'elapsed_seconds':time.perf_counter()-start}
    (root/'CONSUMER.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'new_seconds':newtime,'ordinary_exact_seconds':basetime,
                      'ordinary_Gaussian_seconds':gaussian_time,'new_nodes':q.counts.nodes,
                      'new_factory_coins':q.counts.factory_coins,
                      'ordinary_source_draws':counts.source_draws,
                      'new_nonlinear_proposals':q.counts.nonlinear_gain_proposals+q.counts.nonlinear_loss_proposals,
                      'new_negative_clippings':q.counts.negative_clippings,
                      'seconds_total':out['elapsed_seconds']},indent=2))


if __name__=='__main__':main()
