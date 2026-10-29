"""Bind frozen outputs and final scope; no dynamics, optimization or PSD replay."""
from pathlib import Path
from fractions import Fraction as F
import ast, hashlib, json, time

HERE=Path(__file__).resolve().parent
A=HERE.parent/'a_span_transfer_interface'
EXPECTED='a962a6121b7b1985fe5e33cbd38cf7d0d846d66b16cd7edb6592e7c93b2b560d'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def get(p): return json.loads(p.read_text())

def main():
    start=time.perf_counter()
    assert sha(HERE/'HISTORY_KERNELS.json')==EXPECTED
    h=get(HERE/'HISTORY_KERNELS.json'); k=get(A/'KERNEL_BOUND.json')
    assert k['kernel_sha256']==EXPECTED
    binding=get(A/'KERNEL_BINDING.json')
    for name in ['HISTORY_KERNELS.json','history_kernel_consumer.py',
                 'native_return_consumer.py','parking_preview.py','NATIVE_RETURN.json']:
        assert sha(HERE/name)==binding[name]['sha256']
    syntax=[]
    for p in sorted(HERE.glob('*.py')):
        ast.parse(p.read_text()); syntax.append(p.name)
    parsed=[]
    for p in sorted(HERE.rglob('*.json')):
        if p.name!='FINAL_RECEIPT.json': get(p); parsed.append(str(p.relative_to(HERE)))
    # Deliberately looser than A's saved tighter rational algebraic enclosure.
    sqrt_upper=F(223607,100000); assert sqrt_upper**2>5
    pentagon_upper=(1+sqrt_upper)/5
    rows=[]
    for r in k['reports']:
        if r['pulse']!='smooth_BB1': continue
        radius=F(r['radius_exact']); assert radius>0
        assert all(c['exact_positive_LDL'] for c in r['certificate_blocks'])
        bound=radius/2*(pentagon_upper if r['harmonic'] else 1)
        rows.append({'observable':r['observable'],'science_class':r['science_class'],
          'harmonic':r['harmonic'],'probability_upper_exact':str(bound),
          'approximate_display':float(bound),'scope':'Accepted exact certificate consumed, LDL not rerun here'})
    raw=get(HERE/'source_cache'/'RAW_SOURCE_STRINGS.json'); source_checks=[]
    for s in raw['sources']:
        actual=hashlib.sha256(s['utf8_exact'].encode()).hexdigest()
        source_checks.append({'key':s['key'],'actual_decoded_string_sha256':actual,
          'declared_original_artifact':s['declared_source']['sha256'],
          'matches_original':actual==s['declared_source']['sha256']})
    exact=get(A/'EXACT_WORD_COEFFICIENT.json')
    examples=[]
    for r in exact['reports']:
        if r['pulse']=='smooth_BB1' and r['p']=='3/100' and r['q']==[1,-1,1,1]:
            assert r['target_nonzero_exact'] and F(r['target_probability_coefficient_exact'][0])!=0
            examples.append(r)
    assert len(examples)==2
    smooth=h['reports'][1]
    out={'status':'FROZEN_CONSTRUCTIVE_MODEL_AND_CONDITIONAL_RECEIVER_NOT_PHYSICAL_QUERY',
      'kernel_sha256':EXPECTED,'scope':['Span parking plus physical-command return constructed in one-mode source-informed model',
        'Finite-word PSD/lag-sum/Toeplitz receiver proved with no molecular dimension cap',
        'Independent A exact certificates consume supplied binary64 kernels only',
        'Root whole-read analytic/code/primary-scope intake accepted, no native ODE interval claim'],
      'model_meta':{key:value for key,value in smooth.items() if key!='observables'},
      'modeled_Hamiltonian_clock_s':smooth['total_control_time_s']+350e-6+smooth['observables']['Y_analysis']['analysis_duration_s'],
      'probability_bounds':rows,'non_null_exact_model_examples':examples,
      'source_exact_string_checks':source_checks,'syntax_parsed_without_import':syntax,
      'json_parsed':parsed,'noisy_prototype':'UNEXECUTED; required explicit magnetic_fraction and extra_ground_rate',
      'remaining_NOT_ACQUIRED':['Actual encoding/B/Zeeman-polarization selectivity and added ground RF',
        'ODE/tail/all-mode physical error bound and actual native control/noise',
        'Complete loaded history kernel or sufficient warranted error budget',
        'Ideal complex-readout analyzer qualification beyond modeled reference instrument',
        'Molecular finite band, coherent phases, signal, survival and full attempt rate',
        'Affordable precision or advantage over matched ordinary spectroscopy','Historical novelty'],
      'physical_shots':0,'paid_compute':False,'external_writes':False,
      'metadata_consumer_seconds':time.perf_counter()-start,
      'manifest':{str(p.relative_to(HERE)):{'bytes':p.stat().st_size,'sha256':sha(p)}
        for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='FINAL_RECEIPT.json' and '__pycache__' not in p.parts}}
    (HERE/'FINAL_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({key:out[key] for key in ['status','kernel_sha256','modeled_Hamiltonian_clock_s',
      'source_exact_string_checks','metadata_consumer_seconds']},indent=2))

if __name__=='__main__': main()
