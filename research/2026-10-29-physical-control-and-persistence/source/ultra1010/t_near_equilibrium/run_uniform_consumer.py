"""Fixed 128-observation executions at0,1,10^6; no time/seed retries.

Plus one prescribed native nonlinear path and the paid ordinary Gaussian
observation baseline. Finite statistics cannot resolve the tiny deviation.
"""
from fractions import Fraction as F
from pathlib import Path
import json,math,random,time
from radial_query import Query,Counts,D,DELTA,ZBETA,initial_h,nu


class TapeQuery(Query):
    def __init__(self):
        super().__init__(0)
        self.tape=iter([.1,2**-20,.1,.5,.25,.5,.5,.1,.25,.5,1-2**-40,1-2**-40])
        self.used=0
    def u(self):
        self.used+=1;self.counts.uniforms+=1
        return next(self.tape)


def main():
    started=time.perf_counter();root=Path(__file__).parent
    tape=TapeQuery();mark=tape.query(2.,1.)
    child=math.sqrt((4+2*math.log(2)/.75)/2)
    expected=initial_h(child)**2/D
    assert tape.counts.nonlinear_events==1 and tape.counts.nodes==3
    assert tape.counts.terminal_exits==2 and tape.used==12
    assert abs(mark-expected)<1e-15
    path={'scope':'prescribed finite random-word native gain path, not an iid sample',
          'mark':mark,'independent_expected_product':expected,'uniforms':tape.used,'counts':tape.receipt()}
    rows=[]
    for index,t in enumerate((0.,1.,1e6)):
        query=Query(202610299100+index);tick=time.perf_counter();outputs=[]
        for _ in range(128):outputs.append(query.observation(t))
        elapsed=time.perf_counter()-tick
        counts=[outputs.count(i) for i in range(3)]
        rows.append({'time':t,'n':128,'seed':202610299100+index,'cell_outputs':outputs,
                     'cell_counts':counts,'seconds':elapsed,'counts':query.receipt()})
        print('new',t,'seconds',elapsed,'nodes',query.counts.nodes,'factory coins',query.counts.factory_coins,flush=True)
        (root/'UNIFORM_CONSUMER_PARTIAL.json').write_text(json.dumps({'rows':rows,'native_path':path},indent=2)+'\n')
    # All-time paid ordinary approximation, deliberately different accuracy contract.
    query=Query(1);rng=random.Random(202610299110);ordinary=[]
    tick=time.perf_counter()
    for _ in range(128):
        u=rng.random();total=0.
        for i,p in enumerate(query.mass):
            total+=p
            if u<total:ordinary.append(i);break
    ordinary_seconds=time.perf_counter()-tick
    r_mass=[41/1512,1-41/1512,0]
    initial_exact=[(1-DELTA)*a+DELTA*r for a,r in zip(query.mass,r_mass)]
    result={'status':'EXECUTED_FLOATING_DIAGNOSTIC_not_exact_bit_output',
            'input':'actual isotropic hard spheres, f_delta=(1-delta)M+delta r, delta2^-14',
            'D':'1/3200','target':'exact normalized three radial cell law in ideal-real model',
            'cells':['[0,1]','(1,2]','(2,infinity)'],'native_nonlinear_path':path,
            'rows':rows,'initial_exact_cell_probabilities':initial_exact,
            'ordinary':{'method':'known Maxwellian cell law','n':128,'seed':202610299110,
                        'outputs':ordinary,'seconds':ordinary_seconds,
                        'accuracy_contract':'TV<=D Z_beta exp(-nu0 t/200)/2; not exact transient law',
                        'all_time_TV_bound':D*ZBETA/2},
            'elapsed_seconds_total':time.perf_counter()-started,
            'small_transient_signal_statistically_resolved':False,
            'continuous_full_velocity_law_acquired':False,
            'practical_advantage_over_LVDSMC_or_isotropic_solver_claim':False}
    (root/'UNIFORM_CONSUMER.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'seconds_total':result['elapsed_seconds_total'],'ordinary_seconds':ordinary_seconds,
                      'nonlinear_events':[r['counts']['nonlinear_events'] for r in rows]},indent=2))


if __name__=='__main__':main()
