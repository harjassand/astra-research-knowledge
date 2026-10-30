"""Separate the eight nontranslation cubic modes by compatible fields."""
import compatible_moment_schur as m
from fractions import Fraction as R
from pathlib import Path
import json,time
start=time.perf_counter();F,C,T=m.acquired();gd=json.loads((m.root/'outputs/graded_stabilization/certificate.json').read_text())
cp=[tuple(p) for p in gd['cubic_powers']];basis=[list(map(R,v)) for v in gd['cubic_kernel_basis']]
def functional(modes):
    G=m.gradient(modes);H=[[m.average(m.core.diff(m.core.diff(F,i),j),G) for j in range(4)] for i in range(4)]
    v=[m.average(m.core.diff(F,i),G) for i in range(4)];sv=m.linear_solve(H,v)
    row=[]
    for pw in cp:
        pol={pw:R(1)};w=[m.average(m.core.diff(pol,i),G) for i in range(4)]
        row.append(m.average(pol,G)-m.dot(sv,w))
    return row
shapes=[[[1,0],[0,1],[1,1]],[[1,0],[1,1],[0,1]],[[1,1],[1,-1],[2,1]],[[1,0],[1,1],[1,-1]]]
selected=[];rows=[];rank=0
for shape in shapes:
    for x,y in ((1,0),(0,1),(1,1),(1,-1)):
        vv=[[x*a-y*b,y*a+x*b] for a,b in shape]
        modes=[{'frequency':k,'sine':list(map(str,v))} for k,v in zip(([1,0],[0,1],[1,1]),vv)]
        row=functional(modes);reduced=[m.dot(row,v) for v in basis]
        rr=m.core.rank(rows+[reduced])
        if rr>rank:rows.append(reduced);selected.append({'modes':modes,'functional':list(map(str,row))});rank=rr
        if rank==8:break
    if rank==8:break
assert rank==8
translations=[list(map(R,v)) for v in gd['translation_cubics']]
assert all(m.dot(list(map(R,case['functional'])),v)==0 for case in selected for v in translations)
out={'rank':rank,'fields':selected,'reduced_matrix':[[str(z) for z in row] for row in rows],
  'seconds':time.perf_counter()-start,'scope':'Eight actual compatible fields detect precisely the cubic quotient by translations. This is not a QC separation.'}
(m.root/'work/resonance_quotient.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'exact_rank':rank,'compatible_fields':len(selected),'seconds':out['seconds']},indent=2))
