"""Explicit all-Schatten amplitude budget for the accepted A4 restart."""
import sys
sys.dont_write_bytecode=True
import math,json
import mpmath as mp
from seam_residual import BASE


def run():
    mp.iv.dps=90;iv=mp.iv;rows=[]
    for k in range(7):
        eps=(iv.mpf(1)/1000-iv.mpf(3)/10**22)/(3*7*2**(6-k))
        ex=iv.exp(eps/4);eta=(ex-1)/(ex+1);nu=iv.log(1+eta)
        for n in (256,512):
            seams=n//4
            rows.append(dict(n=n,beta=.75*2**k,
                requested_log_purity_error=math.nextafter(float(eps.a),-math.inf),
                maximum_global_integrated_multiplicative_residual=math.nextafter(float(nu.a),-math.inf),
                maximum_per_seam_integrated_residual=math.nextafter(float((nu/seams).a),-math.inf),
                collar1_block4_seams=seams,
                target_residual_acquired=False))
    result=dict(status='EXPLICIT_NORMALIZED_PURITY_CERTIFICATE_BUDGET_NOT_ACQUIRED_INPUT',
        rows=rows,propagated_warm_log_debt_reserved='3e-22',final_additional_input='T(512,96) still requires an acquired lower bound; its point value is not assumed.',
        formula='eta=exp(nu)-1; log-purity error<=4log((1+eta)/(1-eta)); hence nu<=log(1+tanh(epsilon/8)).')
    (BASE/'results/RUNG_RESIDUAL_BUDGET.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':run()
