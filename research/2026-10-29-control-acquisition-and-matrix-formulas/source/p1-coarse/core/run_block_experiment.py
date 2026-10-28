from fractions import Fraction as F
from pathlib import Path
import itertools,json,random,math
from echo_compiler import EchoCompiler,propose_maps
from uniform_certificate import uniform_certificate,psd,diagonal,sub
from block_echo_compiler import BlockEchoCompiler,propose_block_maps,uniform_block_certificate
from run_echo_experiment import Instrument,truth,dumpable

def outer(x):return [[a*b for b in x] for a in x]

def run():
    n0=[F(3,5),F(0),F(4,5)];n1=[F(0),F(3,5),F(4,5)]
    maps=[outer(n0),outer(n1)];b=[F(0),F(0),F(1)]
    for a in maps:
        assert psd(a) and psd(sub(diagonal([F(1)]*3),a))
    dictionary=[(),(0,),(1,)]
    blocks=[(0,1),(1,0)]
    required=BlockEchoCompiler.required_block_words(dictionary,blocks)
    required |= EchoCompiler.required_words(dictionary,2)
    inst=Instrument(maps,b,eta=F(1,10**8));inst.calibrate()
    records={w:inst.query(w) for w in sorted(required,key=lambda w:(len(w),w))}
    primitive=EchoCompiler(dictionary,2,records,propose_maps(dictionary,2,records))
    failed=False
    try:uniform_certificate(primitive,rho=F(9,10))
    except ValueError:failed=True
    assert failed
    forward,dual=propose_block_maps(dictionary,blocks,records)
    learner=BlockEchoCompiler(dictionary,blocks,records,forward,dual)
    uniform=uniform_block_certificate(learner,rho=F(7,10))
    tasks=list(itertools.product(range(2),repeat=5))
    rng=random.Random(829)
    tasks +=[tuple(rng.randrange(2) for _ in range(h)) for h in [0,1,2,10,30,100]]
    checks=[]
    for w in tasks:
        native=tuple(v for i in w for v in blocks[i])
        actual=truth(maps,b,native);cert=learner.certificate(w)
        assert cert['interval'].contains(actual)
        assert abs(actual-cert['corrected_prediction'].center)<=uniform['all_word_total_bound']
        checks.append({'blocks':w,'native_length':len(native),'truth':actual,'certificate':cert})
    # Interpretation only: Bloch amplitude f=2p-1 for qubit survival p.
    # A simultaneous Hoeffding amplitude radius a needs probability radius a/2.
    desired_amplitude_radius=F(1,10**6);failure_probability=F(1,100)
    count=len(records)
    shots_per_mean=math.ceil(math.log(2*count/float(failure_probability))/
                             (2*(float(desired_amplitude_radius)/2)**2))
    out={'dictionary':dictionary,'blocks':blocks,'records':len(records),
         'calibration_standards':2,'total_readings':inst.calls,
         'native_primitive_executions':inst.operations,'max_query_length':max(map(len,records)),
         'records_shared_with_failed_primitive_attempt':True,
         'raw_records':inst.raw,'decoded_records':[{'word':w,'interval':x} for w,x in records.items()],
         'primitive_rho_0_9_certificate_failed':failed,'forward_maps':forward,'dual_maps':dual,
         'uniform_certificate':uniform,'checked_tasks':checks,'all_exact_checks_passed':True,
         'quantum_interpretation_only':{'survival_probability':'(1+centered_amplitude)/2',
          'known_identity_component':'1/2','assumed_IID_shots_not_executed':True,
          'illustrative_amplitude_radius':desired_amplitude_radius,
          'failure_probability':failure_probability,'hoeffding_shots_per_mean':shots_per_mean,
          'hoeffding_shots_total':count*shots_per_mean}}
    p=Path(__file__).resolve().parents[1]/'results'/'BLOCK_EXPERIMENT.json'
    p.write_text(json.dumps(dumpable(out),indent=2))
    print('readings',inst.calls,'native operations',inst.operations,
          'uniform amplitude error',float(uniform['all_word_total_bound']),
          'tasks',len(tasks),'illustrative shots',count*shots_per_mean)

if __name__=='__main__':run()
