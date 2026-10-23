#!/usr/bin/env python3
"""New Cycle11 scalar diagnostic only; no physical channel or old suite replay."""
from decimal import Decimal, localcontext
from math import comb
from pathlib import Path
import hashlib, json, time

def pair_log_pressure(k, r, ell):
    # t=ln(2)/(2a), b=r/k: 2tab=ln(2)b.
    b=r/Decimal(k)
    terms=[]
    total_mult=0
    for q in range(k+1):
        for j in range(min(q,k-q)+1):
            multiplicity=comb(k,j)-(comb(k,j-1) if j else 0)
            eigenvalue=(q-j)*(k-q-j)-j
            terms.append(Decimal(multiplicity)*(ell*b*eigenvalue).exp())
            total_mult+=multiplicity
    assert total_mult==2**k
    return (sum(terms)/(Decimal(2)**k)).ln()

def main():
    started=time.perf_counter()
    with localcontext() as ctx:
        ctx.prec=80
        ell=Decimal(2).ln(); r=Decimal(1)/256
        theta=ell*r/2
        analytic=-theta-(1-theta).ln()
        looser=theta**2/(2*(1-theta))
        pairs=[]
        for k in [2,4,8,16,32,64]:
            actual=pair_log_pressure(k,r,ell)
            assert Decimal(0)<=actual<=analytic<=looser
            pairs.append({'k':k,'log_pressure':str(actual),'analytic_upper':str(analytic),
                          'upper_over_r_squared':str(analytic/r**2)})
        rare=[]
        for k in [256,1024,16384,262144,1048576,4194304]:
            b=r/Decimal(k); a=1-b; t=ell/(2*a)
            lambda_m2=12*Decimal(comb(k//2,2))**2*(a*b)**2
            formula=Decimal(3)/16*a*a*r*r*Decimal(k-2)**2
            assert abs(lambda_m2-formula)<Decimal('1e-65')
            lower=t*lambda_m2-Decimal(k)*ell
            rare.append({'k':k,'b':str(b),'m2_central_eigenvalue':str(lambda_m2),
                         'log_pressure_lower':str(lower),
                         'physical_K_norm_upper':str((1+a)*k),
                         'majorant_m2_exceeds_physical_norm':lambda_m2>(1+a)*k})
        assert rare[-1]['majorant_m2_exceeds_physical_norm']
        assert Decimal(rare[-1]['log_pressure_lower'])>0
    here=Path(__file__).resolve().parent
    source=here.parents[1]/'dependencies/cycle10/contributions/hamming_response/FULL_HAMMING_RESPONSE.tex'
    result={'scope':'Scalar majorants only, no physical capacity or full K assertion',
            'precision_decimal_digits':80,'r':'1/256','t':'ln(2)/(2(1-r/k))',
            'pair_control':pairs,'distance_four_rare_sector':rare,
            'passed':True,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'observed_script_body_seconds':time.perf_counter()-started,
            'discovery_and_total_reasoning_cost':'unknown'}
    out=here/'scalar_pressure_check.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':True,'output':str(out),'body_seconds':result['observed_script_body_seconds']}))

if __name__=='__main__': main()
