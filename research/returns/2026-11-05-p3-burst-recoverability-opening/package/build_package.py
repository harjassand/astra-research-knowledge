"""Create the selection return, preserving completed predecessors unchanged."""
from pathlib import Path
import ast
import hashlib
import io
import json
import shutil
import zipfile

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/"deliverables"
PACKAGE=OUT/"burst_recoverability_question_package"
PACKAGE.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
previous=OUT/"Astra_Productive_Control_Research_Package.zip"
previous_bytes=previous.read_bytes()
assert sha(previous_bytes)=="a94aefd585ce5a61e3e19dabf79fe27c61480ea302062bb78a2621c3992d9a62"
with zipfile.ZipFile(io.BytesIO(previous_bytes)) as z:
    assert z.testzip() is None
    prefix="productive_control_research_package/"
    manifest=json.loads(z.read(prefix+"SHA256_MANIFEST.json"))["files"]
    for name,expected in manifest.items():assert sha(z.read(prefix+name))==expected,name
    direct=z.read(prefix+"preserved/Astra_Direct_Prevention_Research_Package.zip")
    old_receipt=json.loads(z.read(prefix+"PRESERVATION_RECEIPT.json"))
    with zipfile.ZipFile(io.BytesIO(direct)) as zz:
        assert zz.testzip() is None
        mf=[n for n in zz.namelist() if n.endswith("SHA256_MANIFEST.json") and n.count("/")==1][0]
        direct_prefix=mf.rsplit("/",1)[0]+"/"
        direct_manifest=json.loads(zz.read(mf))["files"]
        for name,expected in direct_manifest.items():assert sha(zz.read(direct_prefix+name))==expected,name

for name in ("build_report.py","build_package.py","check_opening.py","STATUS.txt","report_text.txt","root_screening.txt"):
    shutil.copy2(ROOT/name,PACKAGE/name)
for name in ("figures","results"):
    shutil.copytree(ROOT/name,PACKAGE/name,dirs_exist_ok=True)
independent_hashes={}
for name in ("fault_tolerance","first_principles","transfer"):
    target=PACKAGE/"independent"/name
    shutil.copytree(ROOT/name,target,dirs_exist_ok=True)
    for f in (ROOT/name).rglob("*"):
        if f.is_file():
            rel=f.relative_to(ROOT)
            assert sha(f.read_bytes())==sha((PACKAGE/"independent"/rel).read_bytes())
            independent_hashes[str(rel)]=sha(f.read_bytes())
shutil.copy2(OUT/"Astra_Burst_Recoverability_Question.pdf",PACKAGE/"Astra_Burst_Recoverability_Question.pdf")
(PACKAGE/"preserved").mkdir(exist_ok=True)
shutil.copy2(previous,PACKAGE/"preserved"/previous.name)
assert sha((PACKAGE/"preserved"/previous.name).read_bytes())==sha(previous_bytes)

refs=[]
for n in ast.parse((ROOT/"build_report.py").read_text()).body:
    if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="refs" for t in n.targets):
        refs=ast.literal_eval(n.value)
(PACKAGE/"SOURCES.json").write_text(json.dumps({
    "retrieved":"2026-11-05",
    "scope":"Primary comparators and exact accepted source. No claim of exhaustive historical novelty.",
    "references":[{"number":n,"citation":citation,"url":url} for n,citation,url in refs],
    "p2_exact_provenance":old_receipt["p2_exact_source"],
    "selection_independence":"No other Pro researcher's new tournament proposal was consulted."
},indent=2,ensure_ascii=False)+"\n")

receipt={
    "date":"2026-11-05",
    "previous_package":{"name":previous.name,"bytes":len(previous_bytes),"sha256":sha(previous_bytes),"manifest_members_verified":len(manifest),"crc_check":"PASS","copied_unchanged":True},
    "nested_direct_package":{"bytes":len(direct),"sha256":sha(direct),"manifest_members_verified":len(direct_manifest),"crc_check":"PASS"},
    "earlier_first_event_receipt":old_receipt["earlier_first_event_receipt"],
    "p2_exact_source":old_receipt["p2_exact_source"],
    "independent_notes_copied_unchanged":independent_hashes,
    "preservation_scope":"All completed predecessor statements retain their original premises; no physical-class bridge is inferred."
}
(PACKAGE/"PRESERVATION_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")

readme="""ASTRA - BURST RECOVERABILITY QUESTION SELECTION
5 November 2026

START HERE
Astra_Burst_Recoverability_Question.pdf is the governing 12-page question
dossier. STATUS.txt states what is proved and what is still unproved.

SELECTED QUESTION
The exact heavy-tail boundary for uniformly reliable finite-seed local memory,
including corruptible control/decoding state, finite causal readout and all
finite-horizon resources. The two-dimensional alpha=3 boundary is the first
concrete construction target. The necessity theorem is proved. The local
recovery converse is not proved and no apparatus is claimed.

QUANTIFIERS
Law and sufficiently small fixed positive intensity first; finite seed radius
may depend on them and the fixed accuracy target, but not on the horizon T.
One uniform algorithm may construct different input-independent local hardware
and schedules for each T; that hardware and its execution are charged. The
governing refinement does not require autonomous self-fabrication. Every
mutable information/control/decoding record is exposed to the fault model.

CONTENTS
- PDF, editable ReportLab source build_report.py and extracted report_text.txt.
- check_opening.py, exact/numerical check receipts, and analytic plot files.
- independent/: three independent constructions and audits, with code/checks.
  These are chronological research notes; the main dossier and
  fault_tolerance/uniform_horizon_refinement.md govern the final selection.
- root_screening.txt: the root's rejected energy/locality-only opening.
- SOURCES.json: primary research citations and exact P2 provenance.
- preserved/: the complete preceding productive-control package, unchanged.
  It contains the direct acquired-prevention and first-event predecessors,
  complete independent constructions and their preservation receipts.
- PRESERVATION_RECEIPT.json and SHA256_MANIFEST.json.

REPRODUCE
Requirements: Python 3, numpy, scipy, matplotlib, reportlab, Pillow; DejaVu
Serif/Sans fonts under /usr/share/fonts/truetype/dejavu for the PDF builder.
From this directory:
  python3 check_opening.py
  python3 independent/fault_tolerance/check_opening.py
  python3 independent/first_principles/check_opening.py
  python3 build_report.py
The root checker writes figures/ and results/. The PDF builder recreates the
report in a sibling deliverables/ directory. It creates equation PNGs locally.
The independent scripts test only their declared algebraic/finite examples.
build_package.py records the original assembly and expects the original
workspace layout; it is retained as provenance, not as the extracted-package
verification command. To verify this extracted package, hash every file named
in SHA256_MANIFEST.json and compare with its recorded digest.

SCIENTIFIC LIMITS
The checks do not establish the unproved recurrence or sufficiency theorem.
The plot is a lower bound, not measured or simulated recovery performance.
No laboratory experiment or physical platform reduction was performed.
Strict finite-speed circuits are the governing class. Poisson local clocks
and Lieb-Robinson tails require an additional probabilistic-cone bridge.
The inherited Gibbs, skip-free, repair and loaded-LTI classes remain separate.
No new tournament proposal from another Pro researcher informed selection.
"""
(PACKAGE/"README.txt").write_text(readme)

from pypdf import PdfReader
reader=PdfReader(PACKAGE/"Astra_Burst_Recoverability_Question.pdf")
assert len(reader.pages)==12
checks=json.loads((ROOT/"results/opening_checks.json").read_text())
assert checks["status"]=="PASS" and checks["recovery_sufficiency_proved"] is False
qa={"pdf_pages":len(reader.pages),"all_pages_rendered_and_visually_reviewed":True,
    "root_scoped_checks":"PASS","independent_check_receipts_retained":True,
    "previous_manifest_files_verified":len(manifest),"nested_direct_manifest_files_verified":len(direct_manifest),
    "recovery_converse_proved":False,"physical_validation_performed":False}
(PACKAGE/"results/final_audit_receipt.json").write_text(json.dumps(qa,indent=2)+"\n")
files={str(f.relative_to(PACKAGE)):sha(f.read_bytes()) for f in sorted(PACKAGE.rglob("*")) if f.is_file() and f.name!="SHA256_MANIFEST.json"}
(PACKAGE/"SHA256_MANIFEST.json").write_text(json.dumps({"algorithm":"SHA-256","scope":"Every other regular file in this selection package.","files":files},indent=2)+"\n")
dest=OUT/"Astra_Burst_Recoverability_Research_Package.zip"
with zipfile.ZipFile(dest,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for f in sorted(PACKAGE.rglob("*")):
        if f.is_file():z.write(f,arcname=str(Path(PACKAGE.name)/f.relative_to(PACKAGE)))
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    for name,expected in files.items():assert sha(z.read(PACKAGE.name+"/"+name))==expected,name
print(json.dumps({"package":str(dest),"bytes":dest.stat().st_size,"sha256":sha(dest.read_bytes()),
                  "manifest_members_verified":len(files),"prior_manifest_members_verified":len(manifest),
                  "nested_direct_manifest_members_verified":len(direct_manifest),"pdf_pages":len(reader.pages)},indent=2))
