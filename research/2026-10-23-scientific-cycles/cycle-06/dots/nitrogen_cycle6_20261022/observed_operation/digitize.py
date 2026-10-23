"""Finite chart extraction, NOT original experimental samples or statistical CIs.
Black experimental errorbar caps from exact embedded Fig7 JPEGs. Printed errorbar
meaning and replication count are not stated in recovered article. Include a
separate2px reading allowance plus1px axis-location allowance. This is graphical
resolution bookkeeping, not a complete measurement uncertainty model.
"""
from pathlib import Path
import json,hashlib,time,resource
import numpy as np
from PIL import Image
D=Path(__file__).resolve().parent;start=time.monotonic()
# Manual axis calibration checked visually against ticks in original embedded image.
configs={'intrinsic':{'x0':84,'x1':884,'y0':664,'y4':19,'windows':[(400,527),(500,493),(600,470),(700,448)]},'forced':{'x0':81,'x1':883,'y0':666,'y4':20,'windows':[(400,506),(500,469),(600,436),(700,404)]}}
rows=[]
for name,c in configs.items():
 path=D/(name+'.jpeg');a=np.asarray(Image.open(path).convert('RGB')).astype(int);black=(a.max(2)<110)&(a.max(2)-a.min(2)<35)
 for power,yguess in c['windows']:
  x=int(round(c['x0']+(power-300)/500*(c['x1']-c['x0'])));ys=np.arange(yguess-15,yguess+16)
  count=black[ys,x-16:x+17].sum(1);caps=ys[count>=20]
  if len(caps)<2:raise RuntimeError('Could not resolve caps')
  top,bottom=int(caps.min()),int(caps.max());center=(top+bottom)/2
  def pct(y,y0=c['y0'],y4=c['y4']):return 4*(y0-y)/(y0-y4)
  # Extremize independently over stated graphic-axis and cap-reading tolerances.
  values=[pct(y,y0,y4) for y in [top-2,bottom+2] for y0 in [c['y0']-1,c['y0']+1] for y4 in [c['y4']-1,c['y4']+1]]
  rows.append({'configuration':name,'reported_power_W':power,'x_pixel':x,'upper_cap_pixel_y':top,'lower_cap_pixel_y':bottom,'center_fraction':pct(center)/100,'graphic_envelope_fraction':[min(values)/100,max(values)/100],'source_image_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
r={'scope':__doc__,'axis_calibration':configs,'rows':rows,'calibration_threshold':'R,G,B each<110; max-min<35; horizontal cap support>=20 pixels in33px window. Red CFD markers excluded.','elapsed_s':time.monotonic()-start,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(D/'digitized.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
