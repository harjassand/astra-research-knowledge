"""Use the SAME optimized physical waveform in the full CNOT instrument."""
from pathlib import Path
import sys,json
import numpy as np
from scipy.integrate import simpson
from finite_mediator_parity import instrument_gram
from compose_parity_cnot import metrics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'conventional_routes'))
from optimize_finite_mediator import matrices

def main():
    path=Path(__file__).resolve().parents[1]/'conventional_routes'/'finite_mediator_optimization_results.json'
    source=json.loads(path.read_text());m=source['model'];best=source['optimized'][-1]
    c=np.array(best['coefficients']);t=np.linspace(0,m['T'],24001)
    f={k:v@c for k,v in matrices(len(c)-1,t,m).items()}
    J=lambda v:float(simpson(v,x=t))
    r={'model':m,'N':J(f['A']**2),'IB':J(f['B']**2),'IU':J(f['U']**2),'IV':J(f['V']**2)}
    r['CU']=J(f['U']*f['B']);r['CV']=J(f['V']*f['B'])
    r['K']=m['kc']*r['CV']-m['kb']*r['CU']
    r['phase_Z1']=-J(f['u']*f['U']+f['w']*f['V'])
    r['local_Z1_correction']=r['phase_Z1']-r['K']
    grams=[instrument_gram(r,s) for s in (1,-1)]
    out={'model':m,'integrals':r,'cases':[]}
    for name,noise in [
            ('meter_only',{}),
            ('helper_prep_and_read_0.001',{'prep':.001,'read':.001}),
            ('helper_and_each_H_0.001_and_phase_0.0001',{'prep':.001,'read':.001,'single':.001,'phase':.0001}),
            ('above_plus_commuting_Z_0.0001_per_meter_qubit',{'prep':.001,'read':.001,'single':.001,'phase':.0001,'idle_dephase':.0001})]:
        row={'name':name,'noise':noise,**metrics(grams,**noise)}
        out['cases'].append(row);print(name,row)
    out['scope']='Same optimized waveform and exact finite cold-bath instrument. Initial thermal and continuous thermal noise, parameter errors, actual midpulse X/T1, additional Hamiltonian terms, and physical reset/local operation durations are NOT included in these entanglement infidelities.'
    Path(__file__).with_name('optimized_cnot_results.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
