"""Necessary oxygen-dominance condition, not a kinetic trajectory or yield model.
Coefficients transcribed from Wallace2610.17021v1 Table4R5/R6, Table5R30.
"""
from pathlib import Path
import json
k2=4.1e9;k3=9.7e9;o2=5.26e6
rows=[]
for C in [2.5,1.,.001,.0005,2.6e-7]:
 for y in [0.,.5,.9,1.]:
  fn=o2/(o2+C*((1-y)*k2+y*k3))
  rows.append({'total_nitrite_plus_nitrate_M':C,'nitrate_fraction':y,'oxygen_electron_capture_share_upper':fn})
out={'source':'Wallace et al., arXiv2610.17021v1, Tables4/5','rates':{'nitrite_Minv_sinv':k2,'nitrate_Minv_sinv':k3,'oxygen_pseudo_first_order_sinv':o2},
'necessary_total_concentration_M_for_possible_oxygen_majority':{'all_nitrite':o2/k2,'all_nitrate':o2/k3,'90pct_nitrate':o2/(.1*k2+.9*k3)},
'one_mM_nitrate_fraction_above_which_oxygen_majority_impossible_in_stated_competition':(o2/.001-k2)/(k3-k2),
'strict_majority_boundary':'Equality yields at most50%, not strict majority; largest individual sink is not majority.','rows':rows,'scope':'At prescribed dissolved oxygen and supplied rate coefficients. Other nonnegative sinks only lower this share. Passing condition is NOT sufficient. Unknown mixture/activity/mass-transfer changes and other nitrogen species are not measured by this calculation. No nitrate yield, retention or process claim.'}
assert 0<out['one_mM_nitrate_fraction_above_which_oxygen_majority_impossible_in_stated_competition']<1
Path(__file__).with_name('electron_competition.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
