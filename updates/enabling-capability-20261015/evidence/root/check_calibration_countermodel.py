from fractions import Fraction as Q
from pathlib import Path
import json
s=[Q(1),Q(2)]; t=[Q(1),Q(1)]
a,b=Q(1,4),Q(3,4); ap,bp=Q(7,20),Q(13,20)
y=[x*a+z*b for x,z in zip(s,t)]
g=[u/(x*ap+z*bp) for u,x,z in zip(y,s,t)]
y2=[gain*(x*ap+z*bp) for gain,x,z in zip(g,s,t)]
assert y==y2 and g[0]==1 and a!=ap
out={'scope':'Exact rational algebra fixture; NOT experimental spectra','spectra':[list(map(str,s)),list(map(str,t))],'concentrations_A':list(map(str,[a,b])),'concentrations_B':list(map(str,[ap,bp])),'gain_B':list(map(str,g)),'identical_observations':list(map(str,y)),'passed':True}
Path(__file__).with_name('CALIBRATION_COUNTERMODEL_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
