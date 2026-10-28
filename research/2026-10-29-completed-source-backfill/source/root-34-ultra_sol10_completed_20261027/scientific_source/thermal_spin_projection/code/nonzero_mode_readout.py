"""Nonzero-mode loop readout; same ratio at n and2n; all tails retained.

Numerical assessment only. A genuine scalar upper is used, not Rayleigh
substitution for exact pressure. No certified physical input is produced.
"""
import json,math
from angular_spin_projection import ROOT,PRIOR

def base(q,n=256):
    x=q**n
    return math.log1p(3*x*x)-2*math.log1p(3*x)

def main():
    spin=json.loads((ROOT/'results/spin_projection_preview.json').read_text());spin=next(x for x in spin['rows']if x['beta']==3 and x['angle_samples']==64)
    a5=json.loads((PRIOR/'results/a5_preview.json').read_text());a5=next(x for x in a5['rows']if x['beta']==3)
    scalar=json.loads((ROOT/'results/scalar_reference_preview.json').read_text())['rows'][0]
    wide=json.loads((ROOT/'results/wider_time_projection.json').read_text());out=[]
    L0=scalar['scalar_lower'];U0=scalar['best_upper']['combined_scalar_upper'];M0=scalar['spin0_M6'];M1=spin['spin1_M6']
    complement0=a5['moments']['6']['1']-M0;complement1=a5['moments']['6']['3']-M1
    assert min(complement0,complement1)>0
    for row in wide['rows']:
        c=row['cases'][0];candidate=c['best_fixed_reference_loop'];L1=max(c['Ritz_minus_J']);U1=candidate['combined_target_upper']
        qlo=L1/U0;qhi=U1/L0
        def rest(n):
            total=((M0-L0**6)/L0**6)*(scalar['rest_modulus_upper']/L0)**(n-6)
            total+=3*((M1-L1**6)/L0**6)*(candidate['rest_modulus_upper']/L0)**(n-6)
            total+=(complement0**(1/6)/L0)**n+3*(complement1**(1/6)/L0)**n
            for ir,dim in [('3prime',3),('4',4),('5',5)]:total+=dim*(a5['moments']['6'][ir]**(1/6)/L0)**n
            return total
        Rn=rest(256);R2n=rest(512);points=[qlo,qhi]+([1.]if qlo<=1<=qhi else[])
        low=min(base(q)for q in points)-2*math.log1p(Rn)
        high=min(0.,max(base(q)for q in points)+math.log1p(R2n))
        connected=(low,high+6.01e-11)
        def sensitivity(q):
            x=q**256
            return abs(6*256*(x*x/(1+3*x*x)-x/(1+3*x)))
        out.append({'channel':row['channel'],'span':row['span'],
                    'scalar_eigenvalue_interval':[L0,U0],'spin1_eigenvalue_interval':[L1,U1],
                    'rho_interval':[qlo,qhi],'rho_relative_interval_width':(qhi-qlo)/qlo,
                    'remainder_n':Rn,'remainder_2n':R2n,
                    'logS256_beta3_interval_preview':[low,high],
                    'connected_beta1point5_interval_preview':connected,
                    'connected_interval_width':connected[1]-connected[0],
                    '7point44e_minus7_benchmark_met':connected[1]-connected[0]<7.44e-7,
                    'relative_ratio_width_for_7point44e_minus7_at_0point9558':7.44e-7/sensitivity(.9558),
                    'log_ratio_sensitivity_at_interval_upper':sensitivity(qhi),
                    'local_relative_ratio_width_for_benchmark_at_upper':7.44e-7/sensitivity(qhi)})
    result={'status':'NUMERICAL_NONZERO_DOMINANT_MODE_READOUT_WITH_FULL_TAILS','rows':out,
            'scalar_trace_upper_was_actually_used':True,'no_exact_acquisition':True,
            'scope':'Numerical interval proposals, not certified enclosures; the actual precision gap is charged.'}
    (ROOT/'results/nonzero_mode_readout.json').write_text(json.dumps(result,indent=2)+'\n')
    for row in out:print(row)

if __name__=='__main__':main()
