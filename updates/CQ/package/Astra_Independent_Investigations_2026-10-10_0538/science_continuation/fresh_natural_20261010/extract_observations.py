"""Extract plotted vector symbols, NOT raw experimental records.

Source: arXiv:2511.08932v1, page 7, Figure 2. Coordinates are PDF points.
The y axes use PER MILLE, not percent. No statistical errors are inferred.
Two points at the same B are retained as drawn, not treated as independent runs.
"""
from pathlib import Path
import csv, json, hashlib
import fitz
import numpy as np

ROOT = Path(__file__).resolve().parent
doc = fitz.open(ROOT / 'article.pdf')
page = doc[6]
drawings = page.get_drawings()
rows=[]
def add(i, group, x0, x1, yz, yunit, T, k=None):
    d=drawings[i]; r=d['rect']; x=(r.x0+r.x1)/2; y=(r.y0+r.y1)/2
    rows.append(dict(series=group,pdf_draw_index=i,x_pdf=x,y_pdf=y,
       B_T=-10+20*(x-x0)/(x1-x0),theta_per_mille=(yz-y)/yunit,
       temperature_K=T,kappa_xx_W_mK=k if k is not None else ''))
# Marker rectangles/circles in panel (b); drawing-order ranges exclude legend.
for i in range(315,329): add(i,'sample2_before',405.7262878418,535.3667602539,246.5562744141,65.5640563965,30.2)
for i in range(342,356): add(i,'sample2_after_24h',405.7262878418,535.3667602539,246.5562744141,65.5640563965,28.7)
# Hollow square markers, one rectangle per symbol, in panel (d).
for i in range(356,634):
    d=drawings[i]; r=d['rect']
    if len(d['items'])!=1 or d['items'][0][0]!='re' or not 4<r.width<5.5 or not 4<r.height<5.5: continue
    c=d['color']; x=(r.x0+r.x1)/2
    if c==(0.,0.,0.) and x<346.1:
        add(i,'sample3_before',251.1620178223,345.8969421387,465.9618835449,44.3335876465,29.9,17.6)
    elif c in [(0.,0.,1.),(1.,0.,0.)]:
        pair='T2_T3' if c==(0.,0.,1.) else 'T1_T4'
        if x<442:
            add(i,'sample3_short_'+pair,345.8969421387,440.6318359375,465.9618835449,44.3335876465,28.4,18.2)
        else:
            add(i,'sample3_long_'+pair,440.6318359375,535.3667602539,465.9618835449,44.3335876465,28.3,17.3)
with (ROOT/'figure2_vector_observations.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
stats={}
for name in sorted(set(r['series'] for r in rows)):
    rr=[r for r in rows if r['series']==name]
    b=np.array([r['B_T'] for r in rr]); t=np.array([r['theta_per_mille'] for r in rr])
    slope=float(b@t/(b@b))
    # Offset-free odd-response statistic, not uncertainty or fitting a new exponent.
    stats[name]={'n_plotted_symbols':len(rr),'slope_per_mille_T':slope,
      'temperature_K':rr[0]['temperature_K'],'kappa_xx_W_mK':rr[0]['kappa_xx_W_mK'],
      'largest_abs_theta_per_mille':float(max(abs(t)))}
for state in ['short','long']:
    b=stats['sample3_'+state+'_T2_T3']['slope_per_mille_T']
    r=stats['sample3_'+state+'_T1_T4']['slope_per_mille_T']
    stats['sample3_'+state+'_contrast']={'D':abs(b-r)/(abs(b)+abs(r)), 'slope_ratio_blue_red':b/r}
stats['derived']={
 'sample2_slope_recovery_ratio':stats['sample2_after_24h']['slope_per_mille_T']/stats['sample2_before']['slope_per_mille_T'],
 'sample3_long_over_short_kappa':17.3/18.2,
 'sample3_long_over_short_blue_slope':stats['sample3_long_T2_T3']['slope_per_mille_T']/stats['sample3_short_T2_T3']['slope_per_mille_T'],
 'sample3_long_over_short_red_slope':stats['sample3_long_T1_T4']['slope_per_mille_T']/stats['sample3_short_T1_T4']['slope_per_mille_T'],
 'data_kind':'published vector figure extraction; no raw errors/covariances',
 'source_sha256':hashlib.sha256((ROOT/'article.pdf').read_bytes()).hexdigest()}
(ROOT/'observed_statistics.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats,indent=2))
