#!/usr/bin/env python3
"""Render the current proof for visual QA; not a scientific diagnostic."""
from pathlib import Path
from PIL import Image, ImageDraw
import subprocess,time,json,hashlib
r=Path(__file__).resolve().parent
p=r/"output/pdf/ENTROPY_DRIFT_AND_DEPTH_COST.pdf"
out=r/"tmp/pdfs/render"
out.mkdir(parents=True,exist_ok=True)
for x in out.glob("page-*.png"): x.unlink()
for x in out.glob("contact_*.png"): x.unlink()
t=time.perf_counter()
proc=subprocess.run(["pdftoppm","-r","65","-png",str(p),str(out/"page")],capture_output=True,text=True)
assert proc.returncode==0,proc.stderr
pages=sorted(out.glob("page-*.png"))
thumbs=[]
for i,path in enumerate(pages,1):
    im=Image.open(path).convert("RGB");im.thumbnail((330,470))
    canvas=Image.new("RGB",(350,500),"#e5e7eb")
    canvas.paste(im,((350-im.width)//2,18))
    ImageDraw.Draw(canvas).text((12,480),f"Page {i}",fill="black")
    thumbs.append(canvas)
for start in range(0,len(thumbs),8):
    sheet=Image.new("RGB",(1400,1000),"white")
    for i,im in enumerate(thumbs[start:start+8]):
        sheet.paste(im,((i%4)*350,(i//4)*500))
    sheet.save(out/f"contact_{start//8+1}.png")
rec={"pages":len(pages),"observed_render_seconds":time.perf_counter()-t,
     "pdf_sha256":hashlib.sha256(p.read_bytes()).hexdigest(),
     "contact_sheets":[str(x.relative_to(r)) for x in sorted(out.glob("contact_*.png"))],
     "render_exit_code":0,"scope":"Visual PDF inspection only"}
(r/"evidence/pdf_render_receipt.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec))
