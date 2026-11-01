"""Outward interval evaluation of the selected finite receiver inequalities.

This certifies arithmetic and strict margins at the stated analytic model;
it is not independent verification of the cited block-converse proof or
of any physical component.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/external_openings_20261101'
iv=mp.iv;iv.dps=60
def v(x):return iv.mpf(str(x))
def g(x):return (1+x)*iv.ln(1+x)-x*iv.ln(x)
def d(p,q):return p*iv.ln(p/q)+(1-p)*iv.ln((1-p)/(1-q))
def endpoints(x):return [str(x.a),str(x.b)]

def main():
    selected=json.loads((OUT/'receiver_bounds.json').read_text())['best'];row=selected['block'];test=selected['test']
    n=v(row['n']);eta=v(row['eta']);b=v(row['b']);ret=v(row['retention']);em=v(row['memory_transmission'])
    eb=v(row['heterodyne_transmission']);er=v(row['selector_transmission']);align=v(row['alignment'])
    add=v(row['added_occupation']);dark=v(row['dark_probability']);ell=row['ell'];blocks=test['blocks'];threshold=test['threshold_clicks']
    y=ret*n;ym=em*y;sb=eb*(eta*n+b);cross=eb*eta*ret*em*n*(1+n)
    a=cross/(1+sb);nu=ym-a;noise=er*nu+add
    missg=(1-dark)/(1+noise)*iv.exp(-ell*iv.ln(1+er*align*a/(1+noise)))
    tail=(y/(1+y))**2;p0=1-missg-2*iv.sqrt(ell*tail)-v(row['selector_bad_record_probability'])
    p1=dark+er*(em*y/(1+y)**2+tail)+add
    cost=g(n)+g(ret*n)-g((1-ret)*n)
    cn=eta*iv.ln(1+1/(eta*n+b))/iv.ln(1+1/n)
    mean=blocks*p0;miss=iv.exp(-(mean-threshold)**2/(2*mean))
    logq=-blocks*d(v(threshold)/blocks,p1)
    logc=-(blocks*ell*cn*cost+iv.ln(2))/v('.9')
    margin=logc-logq
    assert miss.b<v('.1').a and margin.a>0 and p0.a>p1.b
    result={'status':'PASS outward 60-digit interval arithmetic',
            'source_pairs':ell*blocks,'block_size':ell,'blocks':blocks,'threshold':threshold,
            'miss_probability_upper_interval':endpoints(miss),
            'log_quantum_false_match_upper_interval':endpoints(logq),
            'log_every_classical_false_match_lower_interval':endpoints(logc),
            'log_separation_margin_interval':endpoints(margin),
            'actual_block_click_H0_lower_interval':endpoints(p0),'actual_block_click_H1_upper_interval':endpoints(p1),
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'bound_script_sha256':hashlib.sha256(Path(__file__).with_name('receiver_frontier.py').read_bytes()).hexdigest()}
    (OUT/'interval_receiver_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
