"""Independent hand-transcription from original embedded Fig. 7 JPEGs.
No parent CSV/script/receipt was read. Coordinates are pixel indexes.
Visual bar envelopes are NOT confidence intervals or validated tolerances.
"""
import csv, json, hashlib
from pathlib import Path
root = Path(__file__).parent
source = root.parent / 'electrodeless_evidence'
# Pixel axes and manually selected dot centers and outer cap strokes.
# One pixel uncertainty is added to each cap endpoint before outward rounding.
data = [
 ('intrinsic',400,0,19,664,244,527.0,523,531),
 ('intrinsic',500,0,19,664,404,493.0,488,498),
 ('intrinsic',600,0,19,664,564,470.0,465,475),
 ('intrinsic',700,0,19,664,724,447.5,441,454),
 ('forced',400,1,20,666,242,506.5,502,511),
 ('forced',500,1,20,666,402,469.5,464,475),
 ('forced',600,1,20,666,562,436.5,430,443),
 ('forced',700,1,20,666,722,403.5,397,411),
]
import math
rows=[]
for config,power,panel,ytop,yzero,x,yc,bar_top,bar_bottom in data:
 scale=(yzero-ytop)/4
 center=(yzero-yc)/scale
 lower=(yzero-bar_bottom-1)/scale
 upper=(yzero-bar_top+1)/scale
 rows.append(dict(configuration=config,power_W=power,source_image=f'page9_image{panel}.jpeg',
   x_px=x,center_y_px=yc,bar_top_px=bar_top,bar_bottom_px=bar_bottom,
   center_NOx_percent=round(center,4),
   raw_bar_low_percent=round((yzero-bar_bottom)/scale,4),
   raw_bar_high_percent=round((yzero-bar_top)/scale,4),
   visual_envelope_low_percent=math.floor(lower*100)/100,
   visual_envelope_high_percent=math.ceil(upper*100)/100))
with (root/'independent_fig7_experiments.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
comparisons=[]
for power in [400,500,600,700]:
 a=next(r for r in rows if r['configuration']=='intrinsic' and r['power_W']==power)
 b=next(r for r in rows if r['configuration']=='forced' and r['power_W']==power)
 r=b['center_NOx_percent']/a['center_NOx_percent']
 lo=b['visual_envelope_low_percent']/a['visual_envelope_high_percent']
 hi=b['visual_envelope_high_percent']/a['visual_envelope_low_percent']
 comparisons.append(dict(power_W=power,center_concentration_ratio=r,
    visual_envelope_ratio_low=lo,visual_envelope_ratio_high=hi,
    center_reported_power_specific_energy_reduction_percent=100*(1-1/r),
    center_allowance_if_total_baseline_equals_reported_power_W=(r-1)*power))
with (root/'independent_ratios.json').open('w') as f:json.dump(comparisons,f,indent=2)
receipt=dict(independent_of_parent_digitization=True,
 source_pdf_sha256=hashlib.sha256((source/'2026_forced_intrinsic.pdf').read_bytes()).hexdigest(),
 original_pdf_page_1based=9,article_page=8,
 original_images=[dict(name=f'page9_image{i}.jpeg',sha256=hashlib.sha256((source/f'page9_image{i}.jpeg').read_bytes()).hexdigest()) for i in [0,1]],
 axis_calibrations=[dict(panel='a',top_y_px=19,top_NOx_percent=4,bottom_y_px=664,bottom_NOx_percent=0),dict(panel='b',top_y_px=20,top_NOx_percent=4,bottom_y_px=666,bottom_NOx_percent=0)],
 method='Manual independent visual selection from original JPEGs, enlarged point crops, and grayscale/low-chroma endpoint inspection. Numerical conversion only uses linear axes. Outward rounded visual envelopes add one pixel at each outer cap endpoint.',
 limitations='No source numerical data, replicate count, covariance, stated error-bar definition, or calibration uncertainty available in main article. Envelopes are only visible plotted extent plus raster-reading allowance, not statistical CI, physical tolerance, or process qualification.',
 independence='Did not open parent digitized_experiments.csv, digitize_figures.py, or digitization_receipt.json.')
(root/'independent_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(comparisons,indent=2))
