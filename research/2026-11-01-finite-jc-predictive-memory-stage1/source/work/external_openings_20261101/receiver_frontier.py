"""Finite-memory, finite-block correlation receiver bounds.

External inputs: He's exact thermal-source/classical-block converse and
standard heterodyne conditional Gaussian states. This script constructs
a physical-head JC write/read approximation, adaptive passive mode
selection, on/off readout, and a binary count decision across blocks.
The higher-photon tail is paid in the actual input, not discarded free.
Numerical evaluations are floating diagnostics; analytic inequalities
and assumptions are stated separately in CONSTRUCTION.txt.
"""
from __future__ import annotations
import hashlib,json,math
from pathlib import Path
import numpy as np
from scipy.special import xlogy
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/external_openings_20261101'

def g(x):return (1+x)*math.log1p(x)-x*math.log(x) if x else 0.
def binary_d(p,q):
    return float(xlogy(p,p/q)+xlogy(1-p,(1-p)/(1-q)))
def source_information(n,retention):
    # Use exact g differences here. n is well above double cancellation.
    return g(n)+g(retention*n)-g((1-retention)*n)
def block(n,ell,eta=.5,b=.5,retention=.2,memory_transmission=.9,
          heterodyne_transmission=.9,selector_transmission=.9,
          alignment=.95,added_occupation=1e-7,dark_probability=1e-7,
          selector_bad_record_probability=1e-8):
    y=retention*n
    ym=memory_transmission*y
    sb=heterodyne_transmission*(eta*n+b)
    cross2=heterodyne_transmission*eta*retention*memory_transmission*n*(1+n)
    a=cross2/(1+sb)
    conditional=ym-a
    assert conditional>=0
    # Alignment is a guaranteed lower bound on squared overlap of the
    # selected mode with the conditional-displacement vector.
    v=selector_transmission*conditional+added_occupation
    drive=selector_transmission*alignment*a
    alpha_gaussian=(1-dark_probability)/(1+v)*math.exp(-ell*math.log1p(drive/(1+v)))
    beta_gaussian=1-(1-dark_probability)/(1+selector_transmission*ym+added_occupation)
    p_tail=(y/(1+y))**2
    union=min(1.,ell*p_tail)
    # General actual JC channel and virtual Gaussian loss agree on the
    # entire optical 0/1 subspace. Both are CPTP on the full source.
    miss_charge=min(1.,2*math.sqrt(union))
    # Under H1 the JC qubits are independent, number diagonal, and
    # independent of the B-derived weights. A normalized passive output
    # has EXACTLY their single-qubit mean, not ell times the tail error.
    # On n=1 the write/read/storage chain transmits with eta_M; n>=2
    # contributes at most its entire input probability.
    pe_upper=memory_transmission*y/(1+y)**2+p_tail
    beta_energy_upper=min(1.,dark_probability+selector_transmission*pe_upper+added_occupation)
    false_charge=0.
    p0=max(0.,1-alpha_gaussian-miss_charge-selector_bad_record_probability)
    p1=beta_energy_upper
    info=source_information(n,retention)
    c=eta*math.log1p(1/(eta*n+b))/math.log1p(1/n)
    return {'n':n,'ell':ell,'eta':eta,'b':b,'retention':retention,
            'memory_transmission':memory_transmission,'heterodyne_transmission':heterodyne_transmission,
            'selector_transmission':selector_transmission,'alignment':alignment,
            'added_occupation':added_occupation,'dark_probability':dark_probability,
            'selector_bad_record_probability':selector_bad_record_probability,
            'source_information_budget_per_pair':info,'classical_contraction':c,
            'Gaussian_miss_probability_upper':alpha_gaussian,'Gaussian_false_match_probability':beta_gaussian,
            'optical_tail_probability_per_pair':p_tail,'tail_union_probability':union,
            'miss_tail_charge':miss_charge,'false_tail_charge':false_charge,
            'actual_JC_qubit_excitation_upper':pe_upper,'false_match_energy_upper':beta_energy_upper,
            'actual_click_H0_lower':p0,'actual_click_H1_upper':p1,
            'guaranteed_binary_relative_entropy_per_pair':binary_d(p0,p1)/ell if p0>p1>0 else 0.,
            'classical_fixed_miss_exponent_ceiling':c*info/.9}

def finite_count_test(row,blocks,miss_target=.1):
    p,q=row['actual_click_H0_lower'],row['actual_click_H1_upper']
    if p<=q:return None
    # Threshold chosen using a completely explicit lower-tail Chernoff
    # guarantee. No numerical tiny binomial tail is used as a proof.
    mu=blocks*p
    threshold=math.floor(mu-math.sqrt(2*mu*math.log(1/miss_target)))
    if threshold<1:return None
    u=threshold/blocks
    if u<=q:return None
    alpha_bound=math.exp(-(mu-threshold)**2/(2*mu))
    log_beta_upper=-blocks*binary_d(u,q)
    pairs=blocks*row['ell']
    log_classical_lower=-(pairs*row['classical_contraction']*row['source_information_budget_per_pair']+math.log(2))/(1-miss_target)
    return {'blocks':blocks,'total_source_pairs':pairs,'threshold_clicks':threshold,
            'miss_probability_upper':alpha_bound,
            'log_false_match_quantum_upper':log_beta_upper,
            'log_false_match_every_classical_lower':log_classical_lower,
            'log_separation_margin':log_classical_lower-log_beta_upper,
            'exact_float_binomial_miss':float(binom.cdf(threshold-1,blocks,p)),
            'total_signal_photons_mean':pairs*row['n'],
            'product_encoder_qubits_per_block':row['ell']}

def main():
    rows=[]
    for n in (.01,.003,.001,3e-4,1e-4,3e-5,1e-5):
        for ell in (64,256,1024,4096,8192,16384,32768):
            row=block(n,ell)
            if row['guaranteed_binary_relative_entropy_per_pair']>row['classical_fixed_miss_exponent_ceiling']:
                for count in (1000,3000,10000,30000,100000,300000,1000000):
                    test=finite_count_test(row,count)
                    if test and test['log_separation_margin']>10:
                        rows.append({'block':row,'test':test});break
    assert rows,'no qualified finite point'
    rows.sort(key=lambda r:r['test']['total_source_pairs'])
    best=rows[0]
    # Failure controls: no across-pair concentration, full thermalized
    # detector, and no retained qubit coherence (drive alignment zero).
    failures=[block(1e-4,1),block(1e-4,8192,added_occupation=.1),block(1e-4,8192,alignment=0.)]
    assert all(x['guaranteed_binary_relative_entropy_per_pair']<=x['classical_fixed_miss_exponent_ceiling'] for x in failures)
    result={'status':'analytic-inequality finite receiver candidate, floating evaluation',
            'best':best,'qualified_points':rows,'failure_controls':failures,
            'same_resource_classical_benchmark':'all normal classical block encoders, unrestricted alphabet and joint B readout, at information cost <=K R',
            'unearned_resources':'actual low-noise mode selector, isolated JC dump ports, timing/noisy control qualification, preparation work and hardware cost',
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'receiver_bounds.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'qualified_points':len(rows),'best':best,'failure_rates':[r['guaranteed_binary_relative_entropy_per_pair'] for r in failures]},indent=2))
if __name__=='__main__':main()
