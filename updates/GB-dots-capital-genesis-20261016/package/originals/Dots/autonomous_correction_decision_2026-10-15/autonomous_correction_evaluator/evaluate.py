#!/usr/bin/env python3
"""Own stdlib-only evaluator of published aggregates; never imports author code.
python evaluate.py [--time-ms T] [--threshold F]
No refit, invented raw shots, or independence-based significance claims.
"""
import csv,json,math,argparse,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DATA=ROOT/'QEC data/source_data'
def sections(name):
    out=[]; block=[]
    for row in csv.reader((DATA/name).read_text().splitlines()):
        if not row or all(not x for x in row):
            if block: out.append(list(csv.DictReader(block)));block=[]
            continue
        if row[0].lstrip().startswith('#'): continue
        # Re-serialize parsed rows so quoted comments and headers are handled.
        import io
        s=io.StringIO();csv.writer(s).writerow(row);block.append(s.getvalue())
    if block:out.append(list(csv.DictReader(block)))
    return out

def val(row,key):
    return float(row[key]) if row.get(key) else None

def curve(p,t):return float(p['a'])+float(p['c'])*math.exp(-(t/float(p['tau_ms']))**2)

def threshold_time(p,f):
    a,c,tau=map(float,[p['a'],p['c'],p['tau_ms']])
    return tau*math.sqrt(-math.log((f-a)/c)) if a<f<=a+c and c>0 else None

def evaluate(time_ms=29.0445,threshold=.75):
    report={'data_class':'published final plotted aggregates, not raw shots','fit_model':'a+c*exp(-(t/tau)^2); publisher coefficients, no refit','sources':['https://doi.org/10.5281/zenodo.20768851','https://arxiv.org/html/2504.16746v1'],'conditions':{}}
    for stem in ['Fig4a','EDFig4a','Fig4b','EDFig4b']:
        blocks=sections(stem+'_source.csv'); rows=blocks[0];fits={r['series']:r for r in blocks[1]}; norm='_unnorm' if stem.startswith('ED') else ''
        counts={s:sum(val(r,s+'_fidelity'+norm) is not None for r in rows) for s in fits}
        q,p=fits['QEC'],fits['phy']
        ratio=float(q['tau_ms'])/float(p['tau_ms'])
        matched=[]
        # Match only exact archived wall-clock times (1e-9 tolerance).
        for r in rows:
            qv=val(r,'QEC_fidelity'+norm)
            if qv is None:continue
            t=val(r,'storage_time_ms')
            for other in rows:
                pv=val(other,'phy_fidelity'+norm)
                if pv is not None and abs(t-val(other,'storage_time_ms'))<1e-9:
                    matched.append({'time_ms':t,'QEC':qv,'physical':pv,'difference':qv-pv})
        residuals={}
        for s,pfit in fits.items():
            z=[]
            for r in rows:
                y=val(r,s+'_fidelity'+norm);err=val(r,s+'_err'+norm)
                if y is not None and err and err>0:z.append((y-curve(pfit,val(r,'storage_time_ms')))/err)
            residuals[s]={'sum_squared_standardized_residuals':sum(x*x for x in z),'n_points':len(z),'nominal_n_minus_3':len(z)-3,'warning':'Diagnostic only; correlations and fit constraints unavailable.'}
        report['conditions'][stem]={'counts':counts,'publisher_fit_parameters':fits,'tau_ratio_QEC_over_physical':ratio,'threshold':threshold,'model_threshold_time_ms':{s:threshold_time(pf,threshold) for s,pf in fits.items()},'fit_value_at_requested_time':{'time_ms':time_ms,'values':{s:curve(pf,time_ms) for s,pf in fits.items()},'warning':'Model values, possibly extrapolated; not new measurements.'},'exact_time_measured_comparisons':matched,'fit_residual_diagnostics':residuals}
    report['interleaved_pairs']={}
    for stem in ['Fig4a','EDFig4a']:
        rows=sections(stem+'_inset_source.csv')[0];norm='_unnorm' if stem.startswith('ED') else ''
        d=[float(r['QEC_fidelity'+norm])-float(r['phy_fidelity'+norm]) for r in rows]
        report['interleaved_pairs'][stem]={'n':len(d),'QEC_better':sum(x>0 for x in d),'mean_difference':statistics.mean(d),'median_difference':statistics.median(d),'sample_sd_difference':statistics.stdev(d),'warning':'Within-batch interleaved comparisons, not a held-out dataset or calibrated confidence interval.'}
    report['chi_identity_elements']={}
    for stem in ['Fig2b','Fig3e','Fig3f']:
        rows=sections(stem+'_chi_matrix.csv')[0];r=next(r for r in rows if r['basis_element']=='II')
        report['chi_identity_elements'][stem]={'real_II':float(r['chi_real']),'bootstrap_sd':float(r['chi_err_real']),'elements':len(rows),'full_complex_process_available':False}
    return report
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--time-ms',type=float,default=29.0445);ap.add_argument('--threshold',type=float,default=.75);a=ap.parse_args()
    print(json.dumps(evaluate(a.time_ms,a.threshold),indent=2))
