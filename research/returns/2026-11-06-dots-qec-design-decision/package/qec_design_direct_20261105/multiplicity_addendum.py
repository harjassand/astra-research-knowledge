"""Post-run, more conservative CS enclosures on unchanged precommitted trajectories.
No new samples and no original result/source/precommit changes.
"""
import json,sys
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT));import sequential_decision as s
sys.path.insert(0,str(ROOT/'canonical_qec_witness_20261105'));from confidence_fast import exact_cp
out=[]
for denominator in [6000,9000]:
 s.ALPHA=F(1,denominator);rows=[]
 for d in [19,21,23]:
  r=json.loads((ROOT/f'd{d}_decision.json').read_text())
  if d==21:
   old=json.loads((ROOT/'inherited_d21/production.json').read_text());meta=json.loads((ROOT/'inherited_d21/parameters.json').read_text());n=old['shots'];k=old['counts']['accepted'];lo,hi=exact_cp(k,n,s.ALPHA,bits=24);Z=F(old['normalizer_exact']);eps=F(meta['conversion_TV_upper_exact'])
  else:
   n=r['shots'];k=r['counts']['accepted'];lo,hi=s.confidence_sequence(n,k);Z=F(r['normalizer_exact']);eps=F(r['conversion_TV_upper_exact'])
  L=max(F(0),Z*lo-eps);U=min(F(1),Z*hi+eps);decision='pass' if U<=F(1,10**12) else 'reject' if L>F(1,10**12) else 'inconclusive'
  rows.append({'distance':d,'n':n,'k':k,'alpha_exact':str(s.ALPHA),'failure_interval_exact':[str(L),str(U)],'failure_interval_float':[float(L),float(U)],'decision':decision})
 out.append({'per_candidate_alpha_exact':str(s.ALPHA),'standalone_three_candidate_error_upper_exact':str(3*s.ALPHA),'rows':rows,'same_trajectories_no_new_samples':True})
(ROOT/'MULTIPLICITY_ADDENDUM.json').write_text(json.dumps({'scope':'More conservative post-run interval evaluation on fixed existing samples/anytime sequences. Original stopping rule and result files unchanged. These can support a separately specified global family budget; they do not by themselves authorize arbitrary historical selection.','evaluations':out},indent=2)+'\n');print(json.dumps(out,indent=2))
