from pathlib import Path
import datetime, hashlib, json, urllib.request, urllib.error

BASE=Path(__file__).resolve().parent
OUT=BASE/'acquired_excluded_from_publication'
sources=[
 ('alfonsi_schied_v4.pdf','https://arxiv.org/pdf/1201.2756v4'),
 ('jahnke_reduced_2011_alt.pdf','https://www.math.kit.edu/ianm3/seite/preprints/media/preprint%20nr.%2011-2.pdf'),
 ('mora_tempone_vilanova_2016.pdf','https://repository.kaust.edu.sa/bitstreams/9b571801-c7e9-4fe2-b113-4ea7b713026e/download'),
 ('vo_sidje_2017.html','https://www.researchgate.net/publication/318233496_An_adaptive_solution_to_the_chemical_master_equation_using_tensors'),
 ('holtorf_barton_2024.html','https://link.springer.com/article/10.1007/s10957-023-02335-9'),
]
receipts=[]
for name,url in sources:
 rec={'file':str(OUT/name),'url':url,'acquired_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Astra-primary-proof-read-only/1.0'})
  with urllib.request.urlopen(req,timeout=45) as resp:
   data=resp.read(); rec.update(status=resp.status,final_url=resp.url,content_type=resp.headers.get('Content-Type'))
  (OUT/name).write_bytes(data)
  rec.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),valid_pdf_magic=data.startswith(b'%PDF') if name.endswith('.pdf') else None)
 except Exception as exc: rec['error']=repr(exc)
 receipts.append(rec); print(json.dumps(rec),flush=True)
(BASE/'receipts'/'ACQUISITION_ADDITIONAL.json').write_text(json.dumps(receipts,indent=2)+'\n')
