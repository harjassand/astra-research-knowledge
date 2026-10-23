"""Reproducible axis-linear readout of embedded source raster plots.
The point centers and error-cap rows were inspected in the source images.
These are digitized plotted values, not raw observations. Error-bar semantics
(replication, SD/SEM/CI) are not specified in the retrieved main article.
Pixel-readout uncertainty is +/-2 pixels, in addition to plotted error bars.
"""
import csv,json
from pathlib import Path
p=Path(__file__).parent
P=[400,500,600,700]
# Axis rows correspond to zero and max ordinate; rounded symbol centers.
plots={
 'NOx_intrinsic':dict(image='page9_image0.jpeg',zero=664,top=19,max=4,centers=[526.5,492.5,469.5,447.5],caps=[(523,530),(488,497),(464,475),(442,453)]),
 'NOx_forced':dict(image='page9_image1.jpeg',zero=666,top=20,max=4,centers=[506.5,469,436.5,403.5],caps=[(502,511),(464,474),(430,442),(397,410)]),
 'SEC_intrinsic':dict(image='page10_image0.jpeg',zero=577,top=16,max=5,centers=[216.5,215,195.5,177.5],caps=[(211,222),(209,221),(189,202),(171,184)]),
 'SEC_forced':dict(image='page10_image1.jpeg',zero=578,top=18,max=5,centers=[268,264,256,249],caps=[(262,274),(258,270),(250,262),(243,255)])}
for d in plots.values():
 d['values']=[(d['zero']-y)*d['max']/(d['zero']-d['top']) for y in d['centers']]
 d['error_halfwidths']=[(b-a)/2*d['max']/(d['zero']-d['top']) for a,b in d['caps']]
 d['readout_uncertainty']=2*d['max']/(d['zero']-d['top'])
json.dump(plots,open(p/'digitization_receipt.json','w'),indent=2)
rows=[]
for i,power in enumerate(P):
 for mode in ['intrinsic','forced']:
  x=plots['NOx_'+mode]['values'][i]/100
  e=plots['SEC_'+mode]['values'][i]
  rows.append(dict(power_W=power,mode=mode,main_feed_SLM=20 if mode=='intrinsic' else 10,quench_feed_SLM=0 if mode=='intrinsic' else 10,NOx_pct=100*x,NOx_errorbar_halfwidth_pct=plots['NOx_'+mode]['error_halfwidths'][i],SEC_MJ_molN=e,SEC_errorbar_halfwidth_MJ_molN=plots['SEC_'+mode]['error_halfwidths'][i],conditional_fixedN_per_original_feed_mol_lower=x/(1+x/2),conditional_fixedN_per_original_feed_mol_upper=x,product_umol_s_from_plotted_SEC=power/e))
with open(p/'digitized_experiments.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for i,power in enumerate(P):
 a,b=rows[2*i:2*i+2]
 print(power, 'NOx%', a['NOx_pct'], b['NOx_pct'], 'SEC',a['SEC_MJ_molN'],b['SEC_MJ_molN'], 'gain%',100*(b['NOx_pct']/a['NOx_pct']-1),'SEC reduction%',100*(1-b['SEC_MJ_molN']/a['SEC_MJ_molN']))
