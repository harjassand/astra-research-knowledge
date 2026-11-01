"""Outward arithmetic for the final analytic examples, not ODE validation."""
import json,hashlib
from pathlib import Path
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/coherent_inference_20261101'
iv=mp.iv;iv.dps=80
def v(s):return iv.mpf(str(s))
def endpoints(x):return [str(x.a),str(x.b)]
def main():
    delta=v('.1');T=iv.pi/2;eta=v('.95');dark=v('.000001');p=v('.00001')
    down=v('.002');phi=v('.001');up=down*p/(1-p);gain=iv.cos(iv.pi*delta/2)**2
    w=1-(1-p)**2*(1-dark)**2*iv.exp(-4*up*T)
    e=1-(1-p)**2*(1-dark)**2*iv.exp(-4*(down+2*phi+up)*T)*eta*gain
    ordinary_e=1-(1-p)**2*(1-dark)**2*iv.exp(-4*(down+2*phi+up)*T)*eta*(1-(iv.pi*delta/2)**2)
    ordinary_w=w;ordinary_rows=[];rows=[]
    for level in range(6):
        rows.append({'level':level,'data_dual_rail_qubits':7**level,'erasure_upper_interval':endpoints(e),
                     'wrong_label_upper_interval':endpoints(w)})
        ordinary_rows.append({'level':level,'erasure_upper_interval':endpoints(ordinary_e),
                              'wrong_label_upper_interval':endpoints(ordinary_w)})
        if level==1:assert (e+w).b<v('.01').a
        if level==3:assert e.b<v('.00000003801').a and w.b<v('.00000003801').a
        if level==4:assert e.b<v('.000000000000091').a and w.b<v('.000000000000091').a
        if level==3:assert (e+w).a>v('.00000001').b and (ordinary_e+ordinary_w).a>v('.00000001').b
        if level==4:assert (ordinary_e+ordinary_w).b<v('.00000001').a
        bad=42*e*w+21*w*w;e,w=7*e**3+bad,bad
        ordinary_bad=42*ordinary_e*ordinary_w+21*ordinary_w**2
        ordinary_e,ordinary_w=7*ordinary_e**3+ordinary_bad,ordinary_bad
    result={'status':'PASS 80-digit outward intervals for analytic readout recursion',
        'gain_efficiency_lower_interval':endpoints(gain),'raw_noiseless_erasure_interval':endpoints(1-eta*gain),
        'parallel_thermal_code_bounds':rows,
        'matched_ordinary_fault_path_bounds':ordinary_rows,
        'convergence':'f_1=e_1+w_1<.01; f_next<=43*f^2 for f<=1/7, giving arbitrary-accuracy asymptotic suppression',
        'limits':'arithmetic certification of formulas conditional on the analytic model, not validated dynamics, code preparation, or device errors',
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'interval_controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'level3':rows[3],'level4':rows[4]},indent=2))
if __name__=='__main__':main()
