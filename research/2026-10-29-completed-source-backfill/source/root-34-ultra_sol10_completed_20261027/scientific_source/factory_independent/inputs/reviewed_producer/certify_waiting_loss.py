"""Directed dyadic acquisition of the entire unbounded factory PGF.

Imports the constructed compiler, not an independent proof audit. Small
Fraction results verify arithmetic enclosures; independent ordinary-chain
comparison is being performed separately by another assigned context.
"""
from fractions import Fraction as Q
import json,time,sys
from waiting_loss_factory import Acquisition,OUT,bs_probability
from dyadic_interval import Ball

class Certified(Acquisition):
    def __init__(self,memory,bits=512):
        Ball.configure(bits)
        # Do not call the mpmath constructor: every actual value is dyadic.
        self.memory=Q(memory);self.exact=False;self.precision=160
        self.cast=Ball.exact;self.lam=self.cast(self.memory)
        self.hcache={};self.kcache={};self.node_count=0;self.maximum_exponent=0
    def acquire(self,n):
        start=time.perf_counter();rows=self.H(n)
        total=sum(r[0] for r in rows);assert total.contains(1)
        mean=sum(k*r[0] for k,r in enumerate(rows))
        var=sum(k*k*r[0] for k,r in enumerate(rows))-mean**2
        source=sum(r[1] for r in rows);wall=sum(r[2] for r in rows)
        covtime=sum(k*r[2] for k,r in enumerate(rows))-mean*wall
        covsource=sum(k*r[1] for k,r in enumerate(rows))-mean*source
        result={'status':'DIRECTED_DYADIC_INTERVAL_ACQUISITION; model proof and code not independently reviewed',
                'n':n,'memory_survival_per_clock':str(self.memory),'precision_bits':Ball.BITS,
                'time_cutoff':None,'mean':mean.record(),'fano':(var/mean).record(),
                'expected_raw_source_attempts':source.record(),'expected_wall_clocks':wall.record(),
                'photon_wall_time_covariance':covtime.record(),'photon_source_cost_covariance':covsource.record(),
                'output_probabilities':[r[0].record() for r in rows],
                'total_probability_contains_one_exact':True,
                'PGF_nodes':self.node_count,'PGF_scalar_entries_including_derivatives':sum(3*len(v) for v in self.hcache.values()),
                'fusion_kernel_scalar_entries':sum(len(coeffrow) for matrix in self.kcache.values() for row in matrix for coeffrow in row),
                'cumulative_process_BS_probability_cache_entries':bs_probability.cache_info().currsize,
                'maximum_integer_exponent':self.maximum_exponent,
                'directed_interval_operations':Ball.operations,'max_stored_integer_bits':Ball.max_stored_bits,
                'max_intermediate_integer_bits':Ball.max_intermediate_bits,
                'maximum_output_probability_width':max((r[0].hi-r[0].lo)/Ball.SCALE for r in rows),
                'elapsed_seconds':time.perf_counter()-start}
        return result,rows

if __name__=='__main__':
    n=int(sys.argv[1]) if len(sys.argv)>1 else 16
    bits=int(sys.argv[2]) if len(sys.argv)>2 else 512
    memory=Q(sys.argv[3]) if len(sys.argv)>3 else Q(999,1000)
    if n==4:
        exact=Acquisition(memory,exact=True);expected=exact.H(4)
    model=Certified(memory,bits);result,rows=model.acquire(n)
    if n==4:
        assert all(rows[k][j].contains(expected[k][j]) for k in range(len(rows)) for j in range(3))
        result['all_exact_Fraction_components_enclosed']=True
    tag='' if memory==Q(999,1000) else f'_L{memory.numerator}over{memory.denominator}'
    (OUT/f'WAITING_LOSS_CERTIFIED_N{n}_{bits}bits{tag}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:({kk:vv for kk,vv in v.items() if kk in ['midpoint_float','width_float']} if isinstance(v,dict) else v)
                      for k,v in result.items() if k!='output_probabilities'},indent=2))
