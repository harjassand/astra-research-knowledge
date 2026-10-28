"""Cross-check directed compiler against independently solved literal chain.

This is a small-component enclosure test, not a replay of any larger run.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys,hashlib,time

ROOT=Path(__file__).resolve().parents[1]
PRODUCER=ROOT/'inputs/reviewed_producer'
sys.path.insert(0,str(PRODUCER))
from certify_waiting_loss import Certified
from dyadic_interval import Ball

def run():
    own=json.loads((ROOT/'results/literal_n4_lambda999_1000.json').read_text())
    begin=time.monotonic();model=Certified(F(999,1000),256)
    at1=model.H(4,0);atpoint=model.H(4,2)
    for column,key in enumerate(('exact_output_probabilities','exact_joint_photon_source_first_moments',
                                  'exact_joint_photon_wall_first_moments')):
        assert all(at1[k][column].contains(F(x)) for k,x in enumerate(own[key]))
    assert all(atpoint[k][0].contains(F(x))for k,x in enumerate(own['exact_joint_pgf_probabilities']))
    output={'status':'PASS_DIRECTED_COMPONENTWISE_ENCLOSURE_OF_INDEPENDENT_CHAIN','n':4,
            'lambda':'999/1000','precision_bits':Ball.BITS,'exact_components_enclosed':36,
            'maximum_probability_width_at_1':max((r[0].hi-r[0].lo)/Ball.SCALE for r in at1),
            'integer_arithmetic_operations':Ball.operations,'elapsed_seconds':time.monotonic()-begin,
            'producer_code_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
             (PRODUCER/'waiting_loss_factory.py',PRODUCER/'dyadic_interval.py',PRODUCER/'certify_waiting_loss.py')},
            'interval_rows_at_1':[[x.record()for x in row]for row in at1],
            'interval_rows_at_lambda2':[[x.record()for x in row]for row in atpoint],
            'scope':'Enclosure arithmetic and exact n4 components only; larger n16/n32 certificates not replayed.'}
    (ROOT/'results/interval_n4_crosscheck.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items()if not k.startswith('interval_rows')},indent=2))

if __name__=='__main__':run()
