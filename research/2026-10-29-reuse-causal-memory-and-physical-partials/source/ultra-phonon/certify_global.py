"""One bounded exact whole-Brillouin certificate attempt, no sample grid proof."""
from pathlib import Path
from fractions import Fraction as F
import gzip,hashlib,json,time
import numpy as np
from polynomial_charts import charts,split,approximate_whitener,exact_margin
BASE=Path(__file__).parent

def main():
    start=time.perf_counter();stats=[];leaves=[];nodes=0;success=True;eta=None
    for name,re,im,den in charts():
        begin=time.perf_counter();pending=[('',re,im,den)];count=0;accepted=0;depthmax=0
        while pending:
            path,re,im,den=pending.pop();nodes+=1;count+=1;depthmax=max(depthmax,len(path))
            S,preview=approximate_whitener(re,im,den)
            if S is not None and preview>.03:
                margin,lower,sr,si,bits=exact_margin(re,im,den,S)
                if margin>0:
                    leaves.append(dict(chart=name,path=path,whitener_real=[[int(x) for x in row] for row in sr],
                        whitener_imag=[[int(x) for x in row] for row in si],whitener_bits=bits,
                        integer_margin=str(margin),coefficient_denominator=str(den),
                        matrix_lower_numerator=str(lower.numerator),matrix_lower_denominator=str(lower.denominator)))
                    eta=lower if eta is None else min(eta,lower);accepted+=1;continue
            if nodes>=20000 or len(path)>=30:
                success=False;print(json.dumps(dict(stopped=name,nodes=nodes,depth=len(path),preview=preview,pending=len(pending))),flush=True);break
            axis=[1,2,0][len(path)%3];left,right,factor=split(re,im,axis)
            pending.append((path+'1',right[0],right[1],den*factor));pending.append((path+'0',left[0],left[1],den*factor))
        st=dict(chart=name,nodes=count,leaves=accepted,max_depth=depthmax,seconds=time.perf_counter()-begin,complete=not pending and success)
        stats.append(st);print(json.dumps(st),flush=True)
        if not success:break
    out=dict(status='EXACT_ALL_TORUS_ACOUSTIC_BLOWUP_CERTIFICATE' if success else 'BOUNDED_ATTEMPT_INCOMPLETE',
        model_sha256=hashlib.sha256((BASE/'MODEL.json').read_bytes()).hexdigest(),charts=stats,nodes=nodes,
        leaves=len(leaves),integer_whitener_bits=24,all_arithmetic_accepted_leaves_exact=True,
        common_chart_matrix_lower_bound=str(eta) if eta else None,
        seconds=time.perf_counter()-start,cap_nodes=20000,cap_depth=30,
        physical_specimen_stability='NOT_ACQUIRED',coefficient_uncertainty='NOT_YET_CONSUMED',
        note='Numerical eigensolvers only propose congruences. Every accepted coefficient is exactly Hermitian and strictly diagonally dominant after an exact rational congruence.')
    with gzip.open(BASE/'LEAVES.json.gz','wt') as f:json.dump(leaves,f,separators=(',',':'))
    (BASE/'GLOBAL_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2),flush=True)

if __name__=='__main__':main()
