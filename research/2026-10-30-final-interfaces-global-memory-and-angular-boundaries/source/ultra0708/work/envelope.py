"""Exact cone consequence; the two new seed proofs remain separate inputs."""
from fractions import Fraction as Q
import json
from pathlib import Path
vertices=[(Q(0),Q(1,2)),(Q(11,13),Q(28,13)),(Q(99,100),Q(88,25)),(Q(299,301),Q(1084,301)),(Q(1),Q(4))]
lines=[]
for (b0,r0),(b1,r1) in zip(vertices,vertices[1:]):
    slope=(r1-r0)/(b1-b0);intercept=r0-slope*b0
    assert slope*b0+intercept==r0 and slope*b1+intercept==r1
    lines.append({'from':str(b0),'to':str(b1),'slope':str(slope),'intercept':str(intercept)})
assert all(Q(x['slope'])<Q(y['slope']) for x,y in zip(lines,lines[1:]))
old_at_new=48*vertices[3][0]-44
assert old_at_new-vertices[3][1]==Q(24,301)
out={'vertices':[[str(x),str(y)] for x,y in vertices],'lines':lines,
     'improvement_at_nonpc_seed':str(old_at_new-vertices[3][1]),
     'scope':'QC by nonnegative mixtures of certified seeds plus determinant-square Jensen. No complete ROC/QC classification.'}
Path(__file__).with_name('envelope.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
