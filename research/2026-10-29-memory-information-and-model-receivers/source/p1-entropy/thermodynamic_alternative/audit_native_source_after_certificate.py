"""Post-certificate source-factory audit. Does not execute or redraw producer."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext
import hashlib,json
import numpy as np
from check_thermodynamic_completion import zero,gen,dec,convert

BASE=Path(__file__).resolve().parent.parent/'native_entropy'
RUN=BASE/'run'
HERE=Path(__file__).resolve().parent


def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    public_audit_path=HERE/'NATIVE_RECORD_PUBLIC_AUDIT.json'
    public=json.loads(public_audit_path.read_text())
    assert public['status']=='PASS' and public['private_source_reads']==0
    receipt=json.loads((RUN/'PRODUCER_RECEIPT.json').read_text())
    truth=json.loads((RUN/'PRIVATE_SOURCE.json').read_text())
    raw=np.load(RUN/'native_record.npz',allow_pickle=False)
    N=len(raw['start_port']); scale=1<<20
    assert receipt['individual_native_trials']==receipt['individual_reset_preparations']==N
    assert receipt['individual_native_jumps']==2*N
    assert receipt['source_scalar_random_variates']==6*N
    assert receipt['native_record_sha256']==public['raw_record_sha256']==digest(RUN/'native_record.npz')
    assert receipt['native_record_bytes']==(RUN/'native_record.npz').stat().st_size
    assert receipt['producer_sha256']==digest(BASE/'produce_native_entropy.py')
    observed_self=int(np.sum(raw['start_port']==raw['end_port']))
    assert receipt['observed_self_returns']==observed_self==122733
    def total_interval(array):
        a=[int(v) for v in array]
        return F(sum(max(0,v-1) for v in a),scale),F(sum(a),scale)
    h_lo,h_hi=total_interval(raw['native_hold_upper_ticks'])
    t_lo,t_hi=total_interval(raw['interior_duration_upper_ticks'])
    h=F(str(receipt['native_port_clock_units']))
    t=F(str(receipt['native_interior_clock_units']))
    total=F(str(receipt['total_native_clock_units']))
    assert h_lo<=h<=h_hi and t_lo<=t<=t_hi
    assert h_lo+t_lo<=total<=h_hi+t_hi
    max_tau=F(str(receipt['maximum_native_interior_time']))
    umax=int(raw['interior_duration_upper_ticks'].max())
    assert F(umax-1,scale)<=max_tau<=F(umax,scale)
    # Construct the fixed microscopic source independently from exact private
    # parameters only AFTER the public certificate audit has been frozen.
    p=F(truth['p']); q=F(truth['q']); wx=F(truth['hidden_weight'])
    assert p==F(5,8) and q==F(3,8) and p+q==1
    assert wx==F(16,15)
    weights=[F(1)]*5+[wx]*10; flows=zero(15)
    for e in range(5):
        i,j=e,(e+1)%5
        for orient in [0,1]:
            x=5+2*e+orient; a=p if orient==0 else q
            flows[i][x]=wx*a; flows[j][x]=wx*(1-a)
            flows[x][i]=wx*(1-a); flows[x][j]=wx*a
    Q=gen(flows,weights)
    assert [-Q[i][i] for i in range(5)]==[F(32,15)]*5
    assert [-Q[i][i] for i in range(5,15)]==[F(1)]*10
    assert all(Q[i][j]==0 for i in range(5,15) for j in range(5,15) if i!=j)
    # Factory equivalence: choose either incident edge with probability 1/2,
    # then primary star with p; its return-to-start probability is q.
    expected_self=p*q+q*p; expected_neighbor=(p*p+q*q)/2
    assert expected_self==F(15,32) and expected_neighbor==F(17,64)
    for i in range(5):
        paths={j:F(0) for j in range(5)}
        for x in range(5,15):
            for j in range(5): paths[j]+=Q[i][x]/F(32,15)*Q[x][j]
        assert paths[i]==expected_self
        assert paths[(i-1)%5]==paths[(i+1)%5]==expected_neighbor
        assert sum(paths.values())==1
    assert sum(weights)==F(truth['total_stationary_weight'])==F(47,3)
    R=sum(weights[i]*(-Q[i][i]) for i in range(5))
    assert R==F(truth['total_departure_flux'])==F(32,3)
    # Same abstract generator admits a different odd-state reversal. This
    # comparison is not a physical implementation or certificate premise.
    parity=list(range(5))+[5+(x^1) for x in range(10)]
    assert all(weights[i]==weights[parity[i]] for i in range(15))
    assert all(flows[i][j]==flows[parity[j]][parity[i]] for i in range(15) for j in range(15))
    with localcontext() as ctx:
        ctx.prec=80
        log_ratio=dec(F(5,3)).ln()
        E=dec(F(16,3))*log_ratio
        per_departure=log_ratio/2
        per_time=dec(F(16,47))*log_ratio
        assert dec(F(public['reused_entropy_per_departure']))<per_departure
        assert dec(F(public['reused_entropy_rate']))<per_time
        assert dec(F(public['window_entropy_rate']))<per_time
        population_linear=dec(F(8,47))
        assert population_linear<per_time
    data=dict(status='PASS',phase='POST PUBLIC-CERTIFICATE FREEZE: factory and truth comparison',
        public_audit_sha256=digest(public_audit_path),source_redraws=0,producer_executions=0,
        private_truth_reads_for_comparison=1,individual_trials=N,resets=N,native_jumps=2*N,
        scalar_random_variates=6*N,observed_self_returns=observed_self,
        reported_elapsed_native_time=receipt['total_native_clock_units'],
        raw_elapsed_interval=[h_lo+t_lo,h_hi+t_hi],source_states=15,hidden_states=10,
        factory_matches_exact_generator=True,ideal_interior_duration='Exp(1)',
        conservative_tail_contract_valid='Exp(1) tail <= exp(-t/2)',
        source_entropy_per_departure=per_departure,source_entropy_per_time=per_time,
        conventional_population_star_optimum_per_time=per_time,
        copositive_full_endpoint_population_bound_per_time=population_linear,
        ordinary_reversal_scope='all states even; positive entropy',
        alternate_parity_scope='paired hidden stars swapped, ports fixed; generalized detailed balance; not a native physical claim',
        instrument_scope='Raw timestamp intervals validated against aggregate receipt; original unrounded arrays not retained and RNG not replayed',
        statistical_scope='No complete floating RNG law proof or physical calibration validation',
        private_source_sha256=digest(RUN/'PRIVATE_SOURCE.json'),
        producer_sha256=digest(BASE/'produce_native_entropy.py'),
        audit_script_sha256=digest(Path(__file__)))
    (HERE/'NATIVE_SOURCE_POSTCERTIFICATE_AUDIT.json').write_text(json.dumps(convert(data),indent=2)+'\n')
    print(json.dumps(convert({k:data[k] for k in ['status','source_redraws','factory_matches_exact_generator','individual_trials','native_jumps','reported_elapsed_native_time','source_entropy_per_time','conventional_population_star_optimum_per_time']}),indent=2))


if __name__=='__main__': main()
