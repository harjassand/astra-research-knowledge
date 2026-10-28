"""Separate comparison adapter; the literal comparator imports no producer.

All independent outputs exist before this reference call. This script only
compares exact rational results and records the actual reviewed scope.
"""
from fractions import Fraction as F
import pathlib,json,sys,time,hashlib,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
PRODUCER=ROOT/'inputs/reviewed_producer/waiting_loss_factory.py'

def run(n,lam):
    path=ROOT/'results'/f'literal_n{n}_lambda{lam.numerator}_{lam.denominator}.json'
    own=json.loads(path.read_text())
    spec=importlib.util.spec_from_file_location('producer_for_comparison_only',PRODUCER)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    start=time.monotonic();other=module.Acquisition(lam,exact=True)
    at1=other.H(n,0);atpoint=other.H(n,own['joint_pgf_lambda_exponent'])
    assert list(map(F,own['exact_output_probabilities']))==[r[0]for r in at1]
    assert list(map(F,own['exact_joint_photon_source_first_moments']))==[r[1]for r in at1]
    assert list(map(F,own['exact_joint_photon_wall_first_moments']))==[r[2]for r in at1]
    assert list(map(F,own['exact_joint_pgf_probabilities']))==[r[0]for r in atpoint]
    output={'status':'PASS_COMPONENTWISE_EXACT_CHAIN_VS_COMPILER','n':n,'lambda':str(lam),
      'exact_photon_probability_components':2*n+1,'exact_source_joint_components':2*n+1,
      'exact_time_joint_components':2*n+1,'exact_additional_PGF_components':2*n+1,
      'additional_z':own['joint_pgf_z'],'compiler_call_seconds':time.monotonic()-start,
      'literal_chain_seconds':own['elapsed_seconds'],
      'producer_code_sha256':hashlib.sha256(PRODUCER.read_bytes()).hexdigest(),
      'literal_output_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
      'scope':'Independent literal chain validated exact small-depth model output/rewards/finite PGF point. Not an audit of larger dyadic runs or comparative advantage over structured phase-type methods.'}
    (ROOT/'results'/f'comparison_n{n}_lambda{lam.numerator}_{lam.denominator}.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))

if __name__=='__main__':run(4,F(999,1000))
