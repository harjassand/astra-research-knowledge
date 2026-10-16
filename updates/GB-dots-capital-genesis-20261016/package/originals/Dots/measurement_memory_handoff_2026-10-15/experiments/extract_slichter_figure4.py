"""Reconstruct published experimental symbols, not raw observations, from CC BY 3.0 PDF.
No author code is used. PDF 7/Fig4: red squares=experiment; blue lines=theory;
black circles=simulation. Tick values visually checked against rendered page.
"""
from pathlib import Path
import fitz,csv,json,hashlib
ROOT=Path(__file__).resolve().parent
pdf=ROOT/'sources/slichter2016.pdf'
p=fitz.open(pdf)[6]; paths=p.get_drawings()
cols=[147.803,230.653,313.437,396.221,479.005]
bottoms=[140.221,221.614]
strengths=[134,179,203,226,248,270,297,334,364,393]
letters=['a','b','c','d','e','f','g','h','j','k']
rows=[]; calibration=[]
for k,(g,label) in enumerate(zip(strengths,letters)):
 left=cols[k%5]; bottom=bottoms[k//5]
 # Identify bottom x-axis ticks and left y-axis ticks by their short line geometry.
 xt=[];yt=[]
 for d in paths:
  r=d['rect']
  if d['color']!=(0.,0.,0.) or len(d['items'])!=1 or d['items'][0][0]!='l':continue
  if abs(r.y1-bottom)<.01 and 1.5<r.height<2.2 and r.width<.01 and left+5<r.x0<left+60:xt.append(r.x0)
  if abs(r.x0-left)<.01 and 1.5<r.width<2.2 and r.height<.01 and bottom-55<r.y0<bottom-5:yt.append(r.y0)
 xt=sorted(set(round(v,3) for v in xt)); yt=sorted(set(round(v,3) for v in yt),reverse=True)
 assert len(xt)==4,(k,xt)
 assert len(yt)==5,(k,yt)
 # Tick labels are x=(2,4,6,8) MHz and y=(2,4,6,8,10) us^-1.
 sx=(xt[-1]-xt[0])/6; sy=(yt[0]-yt[-1])/8
 xzero=xt[0]-2*sx; yzero=yt[0]+2*sy
 calibration.append(dict(panel=label,gamma_m_per_us=g,x_ticks_pdf=xt,y_ticks_pdf=yt,xzero=xzero,yzero=yzero,x_scale=sx,y_scale=sy))
 for d in paths:
  if d['color']!=(1.,0.,0.) or len(d['items'])!=1 or d['items'][0][0]!='re':continue
  r=d['rect'];x=(r.x0+r.x1)/2;y=(r.y0+r.y1)/2
  if not(left-.1<x<left+63.1 and bottom-59<y<bottom+.1):continue
  if not(2.3<r.width<2.8 and 2.3<r.height<2.8):continue
  # Find corresponding vertical red 95%-CI bar. Tiny uncertainty can be below symbol size.
  bars=[]
  for e in paths:
   q=e['rect']
   if e['color']==(1.,0.,0.) and len(e['items'])==1 and e['items'][0][0]=='l' and q.width<.01 and abs(q.x0-x)<.05 and q.y0<=y+.07 and q.y1>=y-.07 and q.y0>bottom-70 and q.y1<bottom+2:
    bars.append(q)
  assert len(bars)<=1,(k,x,y,bars)
  b=bars[0] if bars else None
  rows.append(dict(figure='4',panel=label,gamma_m_per_us=g,omega_over_2pi_MHz=round((x-xzero)/sx,3),gamma_up_drive_per_us=round((yzero-y)/sy,3),ci95_low_per_us=round((yzero-b.y1)/sy,3) if b else '',ci95_high_per_us=round((yzero-b.y0)/sy,3) if b else '',source_kind='published_PDF_vector_digitization_not_raw',center_x_pdf_pt=round(x,6),center_y_pdf_pt=round(y,6)))
rows.sort(key=lambda x:(x['gamma_m_per_us'],x['omega_over_2pi_MHz']))
assert len(rows)>80
out=ROOT/'derived';out.mkdir(exist_ok=True)
with (out/'slichter2016_fig4_experimental_digitized.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(out/'digitization_calibration.json').write_text(json.dumps(dict(source_pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),panels=calibration,points=len(rows),caveat='Published summary estimates only; no quantum-jump traces. Geometric precision is not measurement accuracy. Report rounded ~0.02 MHz / ~0.02 per us; paper CI refers to rate extraction and original systematic analysis, not this digitization.'),indent=2)+'\n')
print('points',len(rows))
for g in strengths:
 group=[r for r in rows if r['gamma_m_per_us']==g]
 print(g,'points',len(group),'near 3 MHz:',min(group,key=lambda r:abs(r['omega_over_2pi_MHz']-3)))
