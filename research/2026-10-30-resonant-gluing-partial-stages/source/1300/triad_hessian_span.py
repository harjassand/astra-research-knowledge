"""Can a compatible cubic moment be glued using its own three wave rays?"""
from pathlib import Path
from fractions import Fraction as R
import sys,json
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/quadratic_boundary'))
import check_shape as m
cert=json.loads((root/'outputs/graded_stabilization/certificate.json').read_text());F,C,T=m.acquired();powers=cert['cubic_powers']
modes=[{'frequency':[1,0],'sine':['1','0']},{'frequency':[0,1],'sine':['0','1']},{'frequency':[1,1],'sine':['1','1']}]
G=m.gradient(modes);cbar=[m.average({tuple(pw):R(1)},G) for pw in powers]
rays=[[R(1),R(0),R(0),R(0)],[R(0),R(0),R(0),R(1)],[R(1)]*4]
columns=[]
for rv in rays:
    for j in range(4):columns.append([m.core.evaluate(m.core.diff({tuple(pw):R(1)},j),rv) for pw in powers])
M=[list(row) for row in zip(*columns)];basis=[list(map(R,v)) for v in cert['cubic_kernel_basis']]
reduced=[[m.dot(v,col) for col in columns] for v in basis];target=[m.dot(v,cbar) for v in basis]
rank=m.core.rank(reduced);aug=m.core.rank([row+[co] for row,co in zip(reduced,target)])
out={'wave_evaluation_rank':rank,'with_compatible_cubic_moment_rank':aug,'own_wave_backgrounds_suffice':rank==aug,
     'scope':'Exact linear compatibility only. Positivity and quartic cost still require construction.'}
(root/'work/triad_hessian_span.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
