"""Independent check of the supplied Gaussian comparator and cap-free opening.

The classical-record budget S(A^K) is intrinsic, not an imposed information cap.
Its contraction still uses the explicitly cited external theorem.
"""
import sys,json,math,hashlib
from pathlib import Path
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/coherent_inference_20261101'
sys.path.insert(0,str(ROOT/'work/external_openings_20261101'))
from receiver_frontier import block,finite_count_test,g
iv=mp.iv;iv.dps=70
def v(s):return iv.mpf(str(s))
def endpoints(x):return [str(x.a),str(x.b)]
def comparator():
    ell=32768;cutoff=3276;mu=v('.00002');q=v(cutoff)/ell
    dim=math.comb(ell+cutoff,cutoff);bits=(dim-1).bit_length()
    logtail=-ell*(q*iv.ln(q/mu)-(1+q)*iv.ln((1+q)/(1+mu)))
    logerr=iv.ln(4)+logtail/2;total=iv.ln(3000)+logerr
    assert bits==15832 and total.b<v('-12000').a
    return {'block_size':ell,'cutoff_total_photons':cutoff,'exact_qubits':bits,
            'log_single_block_trace_error_interval':endpoints(logerr),
            'log_3000_block_sum_trace_error_interval':endpoints(total),
            'physical_compressor':'not supplied; mathematical isometry/reset only',
            'classical_budget_preservation':'CPTP data processing',
            'same_marginal_under_both_hypotheses':True}
def main():
    rows=[]
    # Retain the entire source purifier. The only loss is actual hardware.
    for n in (1e-2,3e-3,1e-3,3e-4,1e-4,3e-5):
      for ell in (32,128,512,2048,8192,32768):
       for eta_m in (.3,.5,.7,.9):
        r=block(n,ell,retention=1.,memory_transmission=eta_m)
        r['source_information_budget_per_pair']=g(n) # intrinsic classical record ceiling
        r['classical_fixed_miss_exponent_ceiling']=r['classical_contraction']*g(n)/.9
        for blocks in (100,300,1000,3000,10000,30000):
          test=finite_count_test(r,blocks)
          if test and test['log_separation_margin']>1:
            rows.append({'block':r,'test':test});break
    rows.sort(key=lambda x:x['test']['total_source_pairs'])
    assert rows
    result={'Gaussian_total_memory_comparator':comparator(),
            'cap_free_classical_scope':'all normal classical records of the complete purified thermal source, arbitrary joint encoding/readout; source marginal remains fixed',
            'intrinsic_information_inequality':'I(A^K:L)<=S(A^K)=K*g(n) for every classical L',
            'qualified_points':rows,'best_floating_point':rows[0],
            'limits':'not an arbitrary-transmitter or practical hardware advantage; physical memory/collector budgets still assumptions',
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'opening_controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'comparator':result['Gaussian_total_memory_comparator'],'qualifying_points':len(rows),'best':rows[0]},indent=2))
if __name__=='__main__':main()
