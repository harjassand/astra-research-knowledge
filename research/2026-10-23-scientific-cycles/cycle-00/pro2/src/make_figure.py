"""Scientific display of saved results; the plot is not certificate arithmetic."""
from pathlib import Path
import json,time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]

def main():
    t=time.perf_counter()
    cdf=json.loads((ROOT/'results/cdf_results.json').read_text())
    mechanism=json.loads((ROOT/'results/error_mechanism.json').read_text())
    rows=cdf['cases'][1]['threshold_rows']
    rat=lambda q:int(q['numerator'])/int(q['denominator'])
    xs=np.array([rat(r['threshold_scaled']) for r in rows])
    fig,(ax,bx)=plt.subplots(1,2,figsize=(11.3,4.6),gridspec_kw={'width_ratios':[1.8,1]})
    for label,key,color,marker,factor in [('Verified dense','dense','#151515','o',1),
                 ('Weighted SLQ, k=64','candidate','#1260A3','s',1.045),
                 ('Classical SLQ, k=64','classical','#BB5715','^',.955)]:
        lo=np.array([r[key]['lower_float'] for r in rows]);hi=np.array([r[key]['upper_float'] for r in rows])
        mid=(lo+hi)/2
        ax.errorbar(xs*factor,mid,yerr=np.array([mid-lo,hi-mid]),fmt=marker,
                    color=color,ms=4,capsize=3,lw=1.3,label=label)
    ax.set_xscale('log');ax.set_ylim(-.035,1.04)
    ax.set_xlabel('Scaled eigenvalue threshold')
    ax.set_ylabel('Fraction of eigenvalues at or below threshold')
    ax.set_title('Verified intervals at nine display thresholds',loc='left',fontsize=11)
    ax.grid(alpha=.18);ax.legend(loc='lower right',fontsize=8,framealpha=.9)
    q=np.array([z['floor_float'] for z in mechanism['cases']])
    n=np.array([z['numerical_transfer_increment'] for z in mechanism['cases']])
    s=np.array([z['statistical_increment'] for z in mechanism['cases']])
    pos=np.arange(2)
    bx.bar(pos,q,color='#667B91',label='CMS width remaining at zero error')
    bx.bar(pos,n,bottom=q,color='#F2B447',label='Numerical transfer')
    bx.bar(pos,s,bottom=q+n,color='#1260A3',label='Sampling and Gaussian conversion')
    for j,total in enumerate(q+n+s):bx.text(j,total+.015,f'{total:.4f}',ha='center',fontsize=10)
    bx.set_xticks(pos,['32 steps','64 steps']);bx.set_ylim(0,.79)
    bx.set_ylabel('CDF interval width at median display threshold')
    bx.set_title('Why the interval remains wide',loc='left',fontsize=11)
    bx.legend(loc='lower left',fontsize=7.5,framealpha=.95)
    bx.grid(axis='y',alpha=.18);bx.set_axisbelow(True)
    fig.suptitle('Finite-precision spectral certificates on NIST bcsstk08 / bcsstm08',fontsize=13,y=.995)
    fig.text(.06,.015,'Exact saved witnesses; n=1074, s=8. Each stochastic band has a 0.01 failure budget under the stated random-bit model.\nMarkers are slightly offset horizontally for readability; only the nine marked thresholds are depicted.',fontsize=8)
    fig.tight_layout(rect=(0,.09,1,.96))
    out=ROOT/'figures';out.mkdir(exist_ok=True)
    fig.savefig(out/'spectral_certificate.png',dpi=180)
    fig.savefig(out/'spectral_certificate.pdf')
    (ROOT/'results/figure_resources.json').write_text(json.dumps({'wall_seconds_body':time.perf_counter()-t,
        'status':'display only; uses stored numbers; no new scientific calculation'},indent=2)+'\n')

if __name__=='__main__':main()
