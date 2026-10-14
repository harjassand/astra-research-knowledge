#!/usr/bin/env python3
"""Compare guarded local-window and full-sparse replay with archived source JSON."""
import json
from pathlib import Path
root=Path(__file__).parent
source=json.load(open(root/'source_snapshot'/'escape'/'comparators.json'))
fresh=json.load(open(root/'replay'/'independently_replayed_comparators.json'))
rows=[]
for a,b in zip(source['windows'],fresh['windows']):
 rows.append({'kind':'window','window':a['window'],'source_ratio':a['ratio'],'replay_ratio':b['ratio'],
  'source_lower':a['lower']['lo'],'replay_lower':b['lower']['lo'],'source_upper':a['upper']['hi'],'replay_upper':b['upper']['hi'],
  'same_inputs':a['window']==b['window'],'state_count':b['lower']['states'],
  'replay_seconds':b['lower']['total_s']+b['upper']['total_s']})
for a,b in zip(source['full'],fresh['full']):
 rows.append({'kind':'full','n':a['n'],'source_ratio':a['hi']/a['lo'],'replay_ratio':b['hi']/b['lo'],
  'source_lower':a['lo'],'replay_lower':b['lo'],'source_upper':a['hi'],'replay_upper':b['hi'],
  'same_inputs':a['n']==b['n'],'state_count':b['states'],'replay_seconds':b['total_s']})
out={'comparisons':rows,'interpretation':'Local-window comparisons remain orders of magnitude too wide at n=24. Full sparse references are tight for n<=12 and are size-limited; no same-size or matched-accuracy superiority claim follows.'}
(root/'replay'/'comparator_difference_summary.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
