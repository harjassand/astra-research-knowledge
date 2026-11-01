"""Independent high-precision closed-form source overlap and exact budget checks."""
from pathlib import Path
from fractions import Fraction as F
import json
import mpmath as mp
from exact_source_overlap import certify_overlap
root=Path(__file__).resolve().parent;mp.mp.dps=110
checks=[]
def mf(x):
 x=F(x);return mp.mpf(x.numerator)/x.denominator
rows=json.loads((root/'scalar_budget_certificates.json').read_text())['rows'];seen={}
for row in rows:
 p=row['parameters'];key=(p['lambda'],p['b'],p['T']);seen[key]=row['source_exact_overlap']
rel=json.loads((root/'release_budget_certificate.json').read_text());p=rel['parameters'];seen[(p['lambda'],p['b'],str(F(p['T_phase'])+F(p['switch_time'])))]=rel['source_overlap_at_end_of_switch']
for key,cert in seen.items():
 l,b,t=map(mf,key);mu=mp.sqrt(l*l/16+l*b*b);nu=-l/4-2*b*b
 a=(1+l/(4*mu))/2*mp.exp((nu+mu)*t)+(1-l/(4*mu))/2*mp.exp((nu-mu)*t)
 lo,hi=map(mf,cert['amplitude_interval']);assert lo<=a<=hi
 checks.append({'parameters':key,'amplitude':mp.nstr(a,90),'interval_width':mp.nstr(hi-lo,10)})
# Test certified frontend at zero time / zero drive / rational-square decay extremes.
for l,b,t in [(F(1,16),F(0),F(2)),(F(9,4),F(1,3),F(0)),(F(1,100),F(2),F(1,100)),(F(10**6),F(1,100),F(3,7))]:
 c=certify_overlap(l,b,t);ll,bb,tt=map(mf,[l,b,t]);mu=mp.sqrt(ll*ll/16+ll*bb*bb);nu=-ll/4-2*bb*bb
 a=(1+ll/(4*mu))/2*mp.exp((nu+mu)*tt)+(1-ll/(4*mu))/2*mp.exp((nu-mu)*tt)
 lo,hi=map(mf,c['amplitude_interval']);assert lo-mp.mpf('1e-105')<=a<=hi+mp.mpf('1e-105')
 checks.append({'parameters':list(map(str,[l,b,t])),'amplitude':mp.nstr(a,90),'interval_width':mp.nstr(hi-lo,10)})
# Rational release inequality independently assemble all terms from their records.
R=F(rel['coherent_reference_with_switch_upper']);a=F(rel['source_overlap_at_end_of_switch']['amplitude_interval'][0]);d=1-a*a;before=F(rel['before_swap_upper'])
root_term=(before-R-2*d)/2
assert root_term>=0 and root_term*root_term>=2*d*R
l=F(p['lambda']);b=F(p['b']);tau=F(p['swap_time']);handoff=16*b*b/l+8*b*b*tau
assert handoff==F(rel['correlated_source_swap_upper'])
assert before+handoff+F(p['supplied_other_complete_error'])==F(rel['total_upper'])<F(rel['target'])
# Program frontend limitation is not a physical impossibility claim.
try:certify_overlap(F(2),F(1,5),F(1))
except AssertionError as e:assert 'rational sqrt' in str(e)
else:raise AssertionError('Expected declared rational-square frontend restriction')
out={'high_precision_overlap_cases':len(checks),'cases':checks,'exact_release_total':rel['total_upper'],'exact_release_total_display':float(F(rel['total_upper'])),'release_margin':str(F(rel['target'])-F(rel['total_upper'])),'frontend_restriction_checked':True,'scope':'High-precision checks diagnostic; exact rational assembly and square-root inequalities independently verified. Enclosure error proof separately reviewed.'}
(root/'independent_certificate_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))
