#!/usr/bin/env python3
"""Read primary TeX tables; no plot digitization or model/source execution."""
from pathlib import Path
import re,json,hashlib
p=Path(__file__).parent
src=p/'paper_source/appendix.tex'; s=src.read_text()
rows={}
for label in ('tab:forward-pruning-primary','tab:forward-pruning-candidates'):
 end=s.index('\\label{'+label+'}')
 start=s.rfind('\\begin{tabular}',0,end)
 segment=s[start:end]
 parsed=[]
 for name,a,b,c in re.findall(r'^\s*(No pruning|Random|Proof length|Interestingness)\s*&\s*(.*?)\s*&\s*(.*?)\s*&\s*(.*?)\s*\\\\',segment,re.M):
  clean=lambda x:float(re.sub(r'\\textbf\{([^}]+)\}',r'\1',x))
  parsed.append({'policy':name,'mean_I':clean(a),'median_I':clean(b),'mean_proof_lines':clean(c)})
 assert len(parsed)==4
 rows[label]=parsed
pre={r['policy']:r for r in rows['tab:forward-pruning-candidates']}
out={'kind':'primary aggregate table transcription; not regenerated model outcomes','source':'arXiv2609.28603v1 appendix D.1','appendix_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'tables':rows,'prepromotion_I_ratio_vs_raw_proof_length_policy':pre['Interestingness']['mean_I']/pre['Proof length']['mean_I'],'limitations':['No per-theorem or per-round records recovered.','No conditional association, iid uncertainty, actual future task benefit or cost advantage inferred.','Before-promotion shift is stronger evidence than an immediate selection effect, but its target is still the optimized ratio.']}
(p/'CANDIDATE_TABLES.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
