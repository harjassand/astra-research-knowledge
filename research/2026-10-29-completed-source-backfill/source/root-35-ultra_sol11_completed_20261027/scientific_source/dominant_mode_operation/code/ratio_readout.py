"""Both scalar endpoints, a common mode ratio, and every even-power tail."""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT.parents[1]
OLD=WORK/'sol10_constructive_frontier_20261028/thermal_spin_projection'

def base(q,n=256):
    x=q**n
    return math.log1p(3*x*x)-2*math.log1p(3*x)

def main():
    source=json.loads((OLD/'results/spin_projection_preview.json').read_text())
    source=next(x for x in source['rows']if x['beta']==3 and x['angle_samples']==64)
    a5=json.loads((WORK/'sol9_frontier_20261028/thermal/results/a5_preview.json').read_text())
    a5=next(x for x in a5['rows']if x['beta']==3)
    scalar=json.loads((OLD/'results/scalar_reference_preview.json').read_text())['rows'][0]
    aug=json.loads((ROOT/'results/frozen_span_augmentation.json').read_text())
    L0=scalar['scalar_lower'];U0=scalar['best_upper']['combined_scalar_upper'];M0=scalar['spin0_M6'];M1=source['spin1_M6']
    complement0=a5['moments']['6']['1']-M0;complement1=a5['moments']['6']['3']-M1
    assert complement0>0 and complement1>0
    configs=[]
    for row in aug['rows']:
        c=row['rows'][0];configs.append((row['name'],max(c['Ritz_minus_J']),c['best_target_upper']['combined_target_upper'],c['best_target_upper']['rest_modulus_upper']))
    configs.append(('best_combined_preview',max(x[1]for x in configs),min(x[2]for x in configs),min(x[3]for x in configs)))
    output=[]
    for name,L1,U1,rho in configs:
        qlo=L1/U0;qhi=U1/L0
        def tail(n):
            r=((M0-L0**6)/L0**6)*(scalar['rest_modulus_upper']/L0)**(n-6)
            r+=3*((M1-L1**6)/L0**6)*(rho/L0)**(n-6)
            r+=(complement0**(1/6)/L0)**n+3*(complement1**(1/6)/L0)**n
            for ir,dim in (('3prime',3),('4',4),('5',5)):r+=dim*(a5['moments']['6'][ir]**(1/6)/L0)**n
            return r
        r=tail(256);r2=tail(512)
        lo=base(qhi)-2*math.log1p(r);hi=min(0.,base(qlo)+math.log1p(r2))+6.01e-11
        x=qhi**256;sensitivity=abs(1536*(x*x/(1+3*x*x)-x/(1+3*x)))
        output.append({'name':name,'scalar_interval':[L0,U0],'spin_interval':[L1,U1],
          'mode_ratio_interval':[qlo,qhi],'relative_ratio_width':qhi/qlo-1,
          'all_other_modes_tail256':r,'all_other_modes_tail512':r2,
          'connected_beta1point5_interval_preview':[lo,hi],'connected_width':hi-lo,
          'width_divided_by_7point44e_minus7':(hi-lo)/7.44e-7,
          'local_log_ratio_sensitivity_at_upper':sensitivity,
          'local_relative_ratio_width_for_target_at_upper':7.44e-7/sensitivity})
    last=output[-1];target_base=last['connected_beta1point5_interval_preview'][1]-7.44e-7+2*math.log1p(last['all_other_modes_tail256'])
    left,right=last['mode_ratio_interval'][0],1.
    for _ in range(80):
        mid=(left+right)/2
        if base(mid)>target_base:left=mid
        else:right=mid
    needed_U1=right*L0
    projected=next(x for x in aug['rows']if x['name']=='P0_frozen10_plus2_bilocal')['rows'][0]['best_variance']
    ray=projected['Rayleigh'];alpha=projected['rest_positive_upper']
    needed_var=(needed_U1-ray)*(ray-alpha)
    result={'status':'PREVIEW_MISSING_RATIO_NOT_ACQUIRED','rows':output,
      'target_debt_at_fixed_current_lower_and_rest_bounds':{
        'maximum_ratio_upper_for_7point44e_minus7_width':right,
        'maximum_spin_upper_for_width':needed_U1,
        'current_min_variance_Rayleigh':ray,'current_rest_positive_upper':alpha,
        'maximum_variance_for_current_Temple_route':needed_var,
        'current_variance_divided_by_needed':projected['variance']/needed_var,
        'scope':'Conditional target calculation, not an acquired stronger residual or a lower bound on other methods.'},
      'both_scalar_endpoints_used':True,'same_ratio_at_256_and_512':True,
      'all_modes_counted':True,'validated_thermal_input_acquired':False,
      'scope':'Numerical source/moment proposals only. Combining independently valid lower/upper proposals is allowed; no ratio of lower bounds is treated as an enclosure.'}
    (ROOT/'results/ratio_readout.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'best':output[-1],'target_debt':result['target_debt_at_fixed_current_lower_and_rest_bounds']},indent=2))

if __name__=='__main__':main()
