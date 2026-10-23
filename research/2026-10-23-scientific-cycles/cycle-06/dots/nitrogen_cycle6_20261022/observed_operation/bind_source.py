"""Bind actual input image bytes to the unchanged primary PDF, without redrawing."""
from pathlib import Path
import hashlib,json,time,resource
import fitz
D=Path(__file__).resolve().parent;src=D.parent/'electrodeless_evidence/2026_forced_intrinsic.pdf';st=time.monotonic();doc=fitz.open(src);rows=[]
for xref,name,alt in [(91,'intrinsic.jpeg','page9_image0.jpeg'),(92,'forced.jpeg','page9_image1.jpeg')]:
 b=doc.extract_image(xref)['image'];p=D/name;q=src.parent/alt;assert p.read_bytes()==b==q.read_bytes()
 rows.append({'xref':xref,'image':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'article_page':8,'pdf_page_1based':9})
out={'primary_pdf_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'images':rows,'scope':'Source binding only, not experimental validity or error guarantee.','elapsed_s':time.monotonic()-st,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(D/'source_binding.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
