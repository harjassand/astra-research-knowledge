"""Package this research and preserve the accepted predecessor byte for byte."""
from pathlib import Path
import hashlib, json, zipfile
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'deliverables'
PDF=OUT/'Astra_Robust_Many_Body_Preparation.pdf'
PRIOR=OUT/'Astra_Noisy_Thermal_Interface_Research_Package.zip'
EXPECTED='8c34f81e2f68a84963d86c67db26d3e1e8fe7f4f2b99f13485e63fc8f0d9a1fb'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert digest(PRIOR)==EXPECTED, 'Accepted predecessor bytes changed'
assert len(PdfReader(PDF).pages)==22
with zipfile.ZipFile(PRIOR) as z:
    assert z.testzip() is None

files=[(PDF,PDF.name),(ROOT/'README_PACKAGE.txt','README.txt')]
for f in sorted(ROOT.rglob('*')):
    if not f.is_file(): continue
    rel=f.relative_to(ROOT)
    if any(p in {'tmp','equations','figures','__pycache__'} for p in rel.parts): continue
    if f.name in {'README_PACKAGE.txt','package_receipt.json'}: continue
    if f.suffix not in {'.md','.py','.json','.txt','.png','.pdf'}: continue
    files.append((f,'research/'+rel.as_posix()))
files.append((PRIOR,'accepted_predecessor/'+PRIOR.name))
manifest={
 'title':'Thermal quantum states through imperfect apparatus',
 'date':'2026-11-05',
 'accepted_predecessor_sha256':EXPECTED,
 'scope':'New robust block theorem and compatible noisy preparation; no practical advantage claim',
 'files':[{'path':arc,'bytes':p.stat().st_size,'sha256':digest(p)} for p,arc in files],
}
target=OUT/'Astra_Robust_Many_Body_Preparation_Research_Package.zip'
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for f,arc in files:
        z.write(f,arc,compress_type=zipfile.ZIP_STORED if f==PRIOR else zipfile.ZIP_DEFLATED)
    z.writestr('MANIFEST.json',json.dumps(manifest,indent=2))
with zipfile.ZipFile(target) as z:
    assert z.testzip() is None
    assert hashlib.sha256(z.read('accepted_predecessor/'+PRIOR.name)).hexdigest()==EXPECTED
receipt={'report':str(PDF),'pages':len(PdfReader(PDF).pages),'report_sha256':digest(PDF),
         'archive':str(target),'archive_bytes':target.stat().st_size,'archive_sha256':digest(target),
         'predecessor_verified_unchanged':True,'members':len(files)+1}
(ROOT/'package_receipt.json').write_text(json.dumps(receipt,indent=2))
print(json.dumps(receipt,indent=2))
