"""Eight-call noncertified error-composition check of the independent prototype."""
from pathlib import Path
import hashlib,json,time
import mpmath as mp
import rounded_relative_doubling as r

def main():
    D0=[mp.mpf('.7'),mp.mpf('2.0')];initial=[mp.mpf('1.3'),mp.mpf('4.5')]
    D=list(initial);A0=r.sumabel(D0);Ai=r.sumabel(initial);records=[];bound=mp.mpf(0)
    for step in range(1,9):
        rec=r.run_case('doubling_chain_'+str(step),D0,D,128,24,True)
        if rec['status']!='CHECKED_NOT_CERTIFIED' or not rec['matching_below_quarter_input_separation'] or not rec['output_one_point_per_gap']:
            records.append({'step':step,'result':rec,'status':'STOPPED_FAILED_ADMISSION'});break
        D=[mp.mpf(v) for v in rec['projected_output_angles']]
        actual=r.mod_period(r.sumabel(D)-2**step*Ai+(2**step-1)*A0)
        per_call=mp.mpf(rec['abel_perturbation_norm'])+mp.mpf(rec['abel_perturbed_section_residual']['residual_norm'])
        bound=2*bound+per_call
        records.append({'step':step,'direct_residual_from_exact_2power_target':actual,
                        'accumulated_two_e_plus_delta_bound':r.outnum(bound),
                        'observed_below_accumulated_bound':mp.mpf(actual['residual_norm'])<=bound*(1+mp.mpf('1e-20')),
                        'result':rec})
        out={'warning':'NONCERTIFIED, floating analytic evaluation; exact rational section algebra only.',
             'prototype_sha256':hashlib.sha256(Path(r.__file__).read_bytes()).hexdigest(),
             'records':records}
        Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
        print(json.dumps({k:v for k,v in records[-1].items() if k!='result'}),flush=True)
if __name__=='__main__':main()
