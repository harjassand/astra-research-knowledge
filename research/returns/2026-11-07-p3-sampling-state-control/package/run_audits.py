"""Bounded digital audits; no physical experiment or acquired calibration."""
from __future__ import annotations
import json, math, random
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import numpy as np
from scipy.linalg import expm
from threadpoolctl import threadpool_limits

from sampling_control import (compile_plan, bounded_commands, native_bracket,
    native_population, physical_budget, exact_weight, query_lower_bounds,
    exact_query_upper, compile_fair_bit_plan, bounded_commands_with_source_bits)
from exact_factory import Counts, exact_command

ROOT = Path(__file__).resolve().parent


def save(name, value):
    (ROOT/name).write_text(json.dumps(value, indent=2)+"\n")


def expect_binomial(p, n, function):
    return sum((F(math.comb(n, s))*p**s*(1-p)**(n-s)*function(s)
                for s in range(n+1)), F(0))


def rational_approximation(cold, hot, q, n, bits, rounds, contrast=F(1),offset=F(0)):
    scale = 1 << bits
    dy = lambda z: F((scale*z.numerator)//z.denominator, scale)
    qd = dy(q)
    ac = (1-qd)*expect_binomial(hot, n,
             lambda s: dy(max(F(0), 1-F(n-s, n)/(1-q))))
    ah = qd*expect_binomial(cold, n,
             lambda s: dy(max(F(0), 1-F(s, n)/q)))
    total = ac+ah
    success = 1-(1-total)**rounds
    weight = success*ah/total  # timeout returns cold, unconditionally
    output = cold+(hot-cold)*weight
    dc = expect_binomial(1-hot, n, lambda s: max(F(0), F(s,n)-(1-q)))
    dh = expect_binomial(cold, n, lambda s: max(F(0), F(s,n)-q))
    bound = (dc+dh)/contrast+(1-(hot-cold))**rounds+F(2*rounds, scale)
    physical_output=(output-offset)/contrast
    physical_target=(q-offset)/contrast
    error=abs(physical_output-physical_target)
    assert error <= bound
    return {
        "n": n, "bits": bits, "rounds": rounds,
        "cold_accept_mass": str(ac), "hot_accept_mass": str(ah),
        "unconditional_hot_weight": str(weight), "output_population": str(physical_output),
        "calibrated_contrast":str(contrast),"calibrated_offset":str(offset),
        "population_error": str(error), "certified_bound": str(bound),
        "error_float": float(error), "bound_float": float(bound),
        "assertion": True,
    }


def kron_all(mats):
    result = np.array([[1.0]], complex)
    for m in mats:
        result = np.kron(result, m)
    return result


def lindblad(j):
    eye = np.eye(len(j))
    k = j.conj().T@j
    return np.kron(j.conj(), j)-0.5*np.kron(eye, k)-0.5*np.kron(k.T, eye)


def apply_local(rho, channel, site, total_qubits):
    t = rho.reshape([2]*(2*total_qubits))
    out = np.zeros_like(t)
    for a,b,c,d in product(range(2), repeat=4):
        dst = [slice(None)]*(2*total_qubits)
        src = dst.copy()
        dst[site], dst[total_qubits+site] = a,b
        src[site], src[total_qubits+site] = c,d
        out[tuple(dst)] += channel[a+2*b,c+2*d]*t[tuple(src)]
    return out.reshape(rho.shape)


def trace_distance(a, b):
    return float(np.abs(np.linalg.eigvalsh((a-b+(a-b).conj().T)/2)).sum()/2)


def quantum_fixture():
    n, q = 3, F(1,4)
    cold, hot, weight = F(3,16), F(21,52), F(13,45)
    X = np.array([[0,1],[1,0]], complex)
    down = np.array([[0,1],[0,0]], complex)
    lam, e = 1.0, 0.1
    generators = [lam*lindblad(X)+a*(lindblad(down)+e*lindblad(X)) for a in [5.0,0.5]]
    t = 24.0
    channel = (1-float(weight))*expm(t*generators[0])+float(weight)*expm(t*generators[1])
    H = np.array([[1,1],[1,-1]], complex)/math.sqrt(2)
    U = kron_all([H]*n)
    for i in range(n-1):
        phase = np.ones(1<<n)
        for v in range(1<<n):
            if ((v>>(n-1-i))&1) and ((v>>(n-2-i))&1):
                phase[v] = -1
        U = np.diag(phase)@U
    dim = 1<<n
    tau = np.diag([1-float(q),float(q)])
    sigma = U@kron_all([tau]*n)@U.conj().T
    omega = np.eye(dim).reshape(dim*dim)/math.sqrt(dim)
    rho = np.outer(omega,omega)
    dressed = np.kron(U,np.eye(dim))
    rho = dressed.conj().T@rho@dressed
    for i in range(n):
        rho = apply_local(rho,channel,i,2*n)
    rho = dressed@rho@dressed.conj().T
    goal = np.kron(sigma,np.eye(dim)/dim)
    observed = trace_distance(rho, goal)
    bound = 2*n*math.exp(-0.25*t)
    assert observed <= bound+1e-12
    # A held classical label makes each conditional component stationary.
    residues=[]
    for p,g in zip([cold,hot],generators):
        residues.append(float(np.linalg.norm(g@np.diag([1-float(p),float(p)]).reshape(-1,order='F'))))
    average_amplitude = (1-weight)*F(5)+weight*F(1,2)
    average_population = native_population(F(1),F(1,10),average_amplitude)
    shared_label_tv = 2*weight*(1-weight)*(hot-cold)**2
    assert shared_label_tv == F(1,52)
    return dict(qubits=n, target_population=str(q), native_amplitudes=[5.0,0.5],
                cold_population=str(cold), hot_population=str(hot),
                exact_hot_weight=str(weight), time=t,
                max_entangled_reference_trace_error=observed,
                analytic_complete_output_bound=bound,
                fixture_is_not_a_diamond_norm_computation=True,
                conditional_stationarity_residuals=residues,
                target_minimum_eigenvalue=float(np.linalg.eigvalsh(sigma).min()),
                output_trace_residual=float(abs(np.trace(rho)-1)),
                mean_amplitude=str(average_amplitude),
                mean_generator_stationary_population=str(average_population),
                reused_label_two_output_trace_error=str(shared_label_tv))


def run():
    bracket = native_bracket(F(9,10), F(11,10), F(2,25), F(3,25),
                             F(5), F(1,2), F(5))
    q, pc, ph = F(1,4), F(3,16), F(21,52)
    offset, contrast = F(1,20), F(9,10)
    observed = lambda p: offset+contrast*p
    xq, xc, xh = observed(q), observed(pc), observed(ph)
    xc_upper, xh_lower = observed(bracket['cold_upper']), observed(bracket['hot_lower'])
    algebra = []
    for lam in [F(9,10),F(1),F(11,10)]:
        for e in [F(2,25),F(1,10),F(3,25)]:
            c = native_population(lam,e,F(5))
            h = native_population(lam,e,F(1,2))
            w = exact_weight(c,h,q)
            assert (1-w)*c+w*h == q
            assert exact_weight(observed(c),observed(h),xq) == w
            algebra.append(dict(lam=str(lam),e=str(e),cold=str(c),hot=str(h),hot_weight=str(w)))
    save("EXACT_INTERPOLATION.json", dict(bracket={k:str(v) for k,v in bracket.items()},
         target=str(q), rate_cap="5", rational_cases=algebra,
         calibrated_readout=dict(offset=str(offset),contrast=str(contrast),
              observed_target=str(xq),observed_cold_upper=str(xc_upper),observed_hot_lower=str(xh_lower)),
         lower_bounds=query_lower_bounds(xc,xh,xq),
         exact_emitter_source_query_upper_per_command=str(exact_query_upper(xc_upper,xh_lower,xq))))
    finite = [rational_approximation(F(1,10),F(2,5),q,n,bits,rounds)
              for n,bits,rounds in [(8,8,5),(16,12,10),(32,16,20)]]
    finite.append(rational_approximation(xc,xh,xq,16,12,20,contrast,offset))
    save("EXACT_BOUNDED_DISTRIBUTIONS.json",finite)
    table=[]
    for N in [100,10000,1000000]:
        for mode in ['global','per_cell']:
            p=compile_plan(N,xq,xc_upper,xh_lower,
                           F(1,1000),F(1,1000),F(1,1000),mode,contrast)
            row=p.certificate()
            fair=compile_fair_bit_plan(p,observed(bracket['cold_lower']),xc_upper,F(1,1000))
            phys=physical_budget(p,bracket['restoration_rate_lower'],F(1,1000),F(1,1000),fair['source_query_cap'])
            row.update(physical=phys,fair_source=fair)
            if mode=='per_cell':
                local_queries=p.n*p.rounds_per_cell+2*fair['pair_cap_per_cell']
                source_time=local_queries*F(phys['probe_relaxation_time'])
                out_time=F(phys['output_relaxation_time'])
                row['fully_parallel_relaxation_time_only']=str(source_time+out_time)
                row['fully_serial_relaxation_time_only']=str(N*source_time+out_time)
                row['fully_parallel_all_cell_activity_upper']=str(N*bracket['maximum_activity_per_cell']*(source_time+out_time))
                row['fully_serial_all_cell_activity_upper']=str(N*bracket['maximum_activity_per_cell']*(N*source_time+out_time))
                row['timing_note']='Readout, digital control, routing, acquisition and old-output holding add to these relaxation-only times; no physical seconds or joules are assigned.'
            table.append(row)
    save("FINITE_RESOURCE_CERTIFICATES.json",table)

    # Exact algorithm: seeded pseudorandom fixtures, never physical data.
    rng=random.Random(7310607)
    counts=Counts(rng.getrandbits)
    cold_source=lambda: int(rng.random()<float(xc))
    hot_source=lambda: int(rng.random()<float(xh))
    trials=2500
    hot_count=sum(exact_command(cold_source,hot_source,xq,xc_upper,xh_lower,counts)
                  for _ in range(trials))
    exact_run=dict(trials=trials,hot_commands=hot_count,
                   predicted_hot_probability=str(exact_weight(pc,ph,q)),
                   observed_hot_frequency=hot_count/trials,
                   unknown_source_outcomes=counts.unknown_coins,
                   source_outcomes_per_command=counts.unknown_coins/trials,
                   fair_bits=counts.fair_bits,rational_coins=counts.rational_coins,
                   maximum_integer_bits=counts.maximum_integer_bits,rescalings=counts.rescalings,
                   note='Seeded simulation only. Frequency agreement is not an exactness proof; the proof uses the original factory theorem and the algebraic mixture identity.')
    save("EXACT_FACTORY_SYNTHETIC_RUN.json",exact_run)
    # Hard-budget emitter exercised with n fresh simulated trials per count.
    p=compile_plan(64,xq,xc_upper,xh_lower,
                   F(1,100),F(1,100),F(1,100),'global',contrast)
    ng=np.random.default_rng(7310608)
    callback=lambda cell,arm,n: int(ng.binomial(n,float([xc,xh][arm])))
    bits_rng=random.Random(7310609)
    finite_run=bounded_commands(p,callback,lambda cell,k:bits_rng.getrandbits(k))
    finite_run.update(certificate=p.certificate(),
        note='The binomial callback accelerates a synthetic audit only; every generated count is charged n independent source outcomes. Runtime controller receives no arm population.')
    save("BOUNDED_EMITTER_SYNTHETIC_RUN.json",finite_run)
    small=compile_plan(8,xq,xc_upper,xh_lower,F(1,100),F(1,100),F(1,100),'per_cell',contrast)
    fair=compile_fair_bit_plan(small,observed(bracket['cold_lower']),xc_upper,F(1,100))
    supplied_rng_run=bounded_commands_with_source_bits(small,callback,fair)
    supplied_rng_run['fair_source_certificate']=fair
    supplied_rng_run['note']='Same seeded synthetic source supplies both control records and disjoint randomness pairs; no true physical randomness is claimed.'
    save("SOURCE_RANDOMNESS_SYNTHETIC_RUN.json",supplied_rng_run)
    forced=compile_plan(2,F(1,2),F(1,4),F(3,4),F(1,10),F(1,10),F(1,10),'per_cell')
    forced_fair=compile_fair_bit_plan(forced,F(1,4),F(1,4),F(1,10))
    forced_run=bounded_commands_with_source_bits(forced,lambda cell,arm,n:0,forced_fair)
    assert forced_run['fair_source_timeout'] and forced_run['commands']==[0,0]
    assert forced_run['all_source_outcomes'] <= forced_fair['source_total_with_control']
    save("FORCED_TIMEOUT_PATH.json",dict(result=forced_run,
        note='A forced all-zero source transcript exercises unconditional fallback and the resource cap. It is not a statistical source model or a claim of likely failure.'))
    save("QUANTUM_REFERENCE_AND_REUSE_AUDIT.json",quantum_fixture())
    # Probe indistinguishability without a calibrated observation anchor.
    readout=F(1,20)
    p0,p1=F(1,10),F(2,5)
    p0b,p1b=(p0-readout)/(1-2*readout),(p1-readout)/(1-2*readout)
    assert readout+(1-2*readout)*p0b==p0
    assert readout+(1-2*readout)*p1b==p1
    minimax_weight=F(31,57)
    minimax_error=F(1,76)
    assert abs(p0+(p1-p0)*minimax_weight-q)==minimax_error
    assert abs(p0b+(p1b-p0b)*minimax_weight-q)==minimax_error
    save("OBSERVATION_ANCHOR_OBSTRUCTION.json",dict(
        observed_cold=str(p0),observed_hot=str(p1),
        apparatus_A=dict(readout_flip='0',cold=str(p0),hot=str(p1),required_hot_weight=str(exact_weight(p0,p1,q))),
        apparatus_B=dict(readout_flip=str(readout),cold=str(p0b),hot=str(p1b),required_hot_weight=str(exact_weight(p0b,p1b,q))),
        single_output_minimax_trace_error=str(minimax_error),minimax_hot_weight=str(minimax_weight),
        conclusion='Identical complete classical probe laws require different commands. Finite or infinite repetitions of these probes alone cannot identify the missing observation anchor.'))
    save("RUN_SUMMARY.json",dict(status='all_assertions_passed',
         exact_fraction_interpolation_cases=len(algebra),finite_fraction_distribution_cases=len(finite),
         resource_plans=len(table),physical_experiments=0,new_workers=0,
         warnings=['Synthetic probability sources are not acquired apparatus.',
                   'Readout/RNG/storage/calibration/holding errors remain separately paid.',
                   'The exact emitter has no declared hard bit-work budget; the bounded emitter does.']))
    print(json.dumps(dict(status='all_assertions_passed',exact_factory=exact_run,
                          quantum=quantum_fixture()),indent=2))


if __name__=='__main__':
    with threadpool_limits(limits=1):
        run()
