#!/usr/bin/env python3
"""Bounded independent Cycle11 cost-envelope algebra check; no old code replay."""
from decimal import Decimal, localcontext
from pathlib import Path
import hashlib,json,time

def main():
    started=time.perf_counter(); root=Path(__file__).resolve().parents[2]
    records=[]
    with localcontext() as ctx:
        ctx.prec=90; D=Decimal; ell=D(2).ln(); tol=D('1e-75')
        def phi(z,b,v):
            a=1-b;return ((3*b+a*(z+2/z)).ln()+v*z.ln())/ell
        for b in map(D,['0','0.000001','0.0009765625','0.1','0.5','0.999','1']):
            a=1-b
            for fraction in map(D,['0','0.1','0.5','0.9','1','1.1']):
                v=fraction*a/3
                if a>0 and v<a/3:
                    z=((9*b*b*v*v+8*a*a*(1-v*v)).sqrt()-3*b*v)/(2*a*(1+v))
                    stationary=a*(1+v)*z*z+3*b*v*z-2*a*(1-v)
                    assert abs(stationary)<tol and z>1
                else:
                    z=D(1);stationary=None
                value=phi(z,b,v)
                for ztest in [D(1),z.sqrt(),z*z,D(2),D(4)]:
                    assert phi(ztest,b,v)>=value-tol
                if b==0 and v<=D(1)/3:
                    p=(1+v)/2
                    entropy=-(p*p.ln()+(1-p)*(1-p).ln())/ell+p
                    assert abs(value-entropy)<tol
                if v>=a/3:
                    assert abs(value-D(3).ln()/ell)<tol
                records.append({'b':str(b),'v':str(v),'z_optimizer':str(z),
                                'ceiling_bits':str(value),
                                'stationarity_residual':None if stationary is None else str(stationary)})
        dstar=3/(2*D(2).sqrt())-1
        constants={'upper_linear_coefficient':str(dstar/ell),'retained_lower_coefficient':str(ell/(D(2)**20))}
    files=[]
    for name in ['ENTROPY_DRIFT_AND_DEPTH_COST.tex','contributions/depth_budget/INHERITED_CODE_DEPTH_BUDGET.tex']:
        p=Path(__file__).resolve().parent/'reviewed'/Path(name).name;raw=p.read_bytes();files.append({'file':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    result={'status':'PASS_BOUNDED_NEW_ALGEBRA','precision_decimal_digits':90,
            'cases':records,'constants':constants,'reviewed_source_files':files,
            'body_seconds':time.perf_counter()-started,'scope':'Envelope algebra and interface review only, no re-audit of inherited code',
            'discovery_review_total_cost':'unknown'}
    out=Path(__file__).with_suffix('.json');out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'cases':len(records),'body_seconds':result['body_seconds'],'sources':files,'constants':constants},indent=2))

if __name__=='__main__':main()
