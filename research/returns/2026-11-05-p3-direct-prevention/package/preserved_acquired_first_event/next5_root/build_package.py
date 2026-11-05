"""Assemble this continuation without changing any accepted original."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

WORK = Path(__file__).resolve().parent.parent
DEST = WORK / 'acquired_first_event_research_package'
OUT = WORK / 'output'
PDFOUT = OUT / 'pdf' / 'Astra_Acquired_First_Event_Law.pdf'
ZIPOUT = OUT / 'Astra_Acquired_First_Event_Research_Package.zip'
SOURCE = WORK / 'first_event_research_package'
BASELINE = json.loads((WORK / 'next5_root/PRESERVATION_BASELINE.json').read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    for name, digest in BASELINE['files'].items():
        assert sha(SOURCE / name) == digest, f'Original changed: {name}'
    DEST.mkdir(exist_ok=True)
    preserved = DEST / 'preserved_first_event'
    shutil.copytree(SOURCE, preserved, dirs_exist_ok=True)
    excluded = {'.aux', '.log', '.out', '.pyc'}
    for directory in ['next5_root', 'next5_decision', 'next5_fixedlaw', 'next5_physical']:
        source = WORK / directory
        for p in sorted(source.rglob('*')):
            rel = p.relative_to(source)
            if not p.is_file() or any(x in ('__pycache__', 'tmp') for x in rel.parts):
                continue
            if p.suffix in excluded or p.name == 'build.stdout.txt':
                continue
            target = DEST / directory / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
    PDFOUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(WORK / 'next5_root/acquired_first_event_report.pdf', PDFOUT)
    shutil.copy2(PDFOUT, DEST / PDFOUT.name)
    matches = []
    for name, digest in BASELINE['files'].items():
        assert sha(preserved / name) == digest, f'Preserved copy changed: {name}'
        matches.append(name)
    receipt = dict(original_file_count=len(matches), all_originals_unchanged=True,
                   all_preserved_copies_match=True, matched_files=matches,
                   governing_public_revision='719e201332992002528c221c49f80f69431485f6')
    (DEST / 'PRESERVATION_RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
    readme = '''ACQUIRING THE FIRST-EVENT LAW — COMPLETE RESEARCH PACKAGE
5 November 2026

Start with Astra_Acquired_First_Event_Law.pdf. It contains the full marked-law
bridge, acquired confidence/decision composition, physical query factories,
unknown-weight static interface, finite error/cost ledger and primary comparison.

CURRENT GOVERNING CONSTRUCTIONS
next5_root/
  acquired_first_event_report.tex plus its four local input .tex files
  (the report also inputs the Gibbs/operating/static proofs in next5_decision).
  certificate.py and run_bridge_diagnostic.py: exact-rational certificate
  calculator and small analytic diagnostic; bridge_execution.json and stdout.
  SELECTION_AND_SCOPE.txt: full endpoint, premises, costs, alternatives and
  useful failed attempts. BRIDGE_CHECKPOINT.txt is an earlier working note;
  the final report and SELECTION_AND_SCOPE govern its completed items.
next5_decision/
  experiment_fed_first_event.pdf and complete standalone LaTeX sources;
  STATUS.txt, factory_audit.py, factory_results.json, execution_receipt.json.
  This consumes fresh local experiments per record; it is not an unlimited
  offline model learned once. Actual field, pin and timer costs remain.
next5_fixedlaw/
  FOUNDATIONAL_CONTRACTION_BOUNDARY.md, complete rational compiler,
  exact execution record and status/limits. The result concerns exact
  events with shrinking signals; finite positive margins remain decidable.
next5_physical/
  CONTROLLED_TRANSPORT.md, complete controlled information bound and
  finite-slew specified-pair diagnostic, scripts, interval certificate,
  execution/source records and checksums. It is not a uniform transport
  estimator or a manufactured apparatus.

PRESERVED ORIGINALS
preserved_first_event/ contains all 182 files of the complete preceding
package, byte for byte. Its nested preserved_correlated_reliability/ contains
the previous correlated counting/CDF, transport and passive-memory work,
passive Hamiltonian calibration and reliability certificate, deferred quantum
calibration, all-strength control law and thermal-effusion companion, together
with their earlier source registers and recorded failures. The original
active acquisition/preparation/prevention, first-event finite clock, fixed-law
and fixed-mechanics thermal work is also intact. Older 'incomplete' statuses
remain as historical originals; read the newest governing reports for results
completed subsequently. No original is silently rewritten.

REPRODUCTION
From next5_root/, run pdflatex twice on acquired_first_event_report.tex.
From next5_decision/, run pdflatex twice on experiment_fed_first_event.tex.
From the package root, run:
  python3 next5_root/run_bridge_diagnostic.py
  python3 next5_decision/factory_audit.py
The fixed-law and physical folders give their own exact reproduction commands
and environments. The root diagnostic uses mpmath only for its explicitly
nonrigorous analytic reference; its upper certificate uses exact rationals.
Reproduction may refresh result files in the extracted copy.

EXECUTION LIMITS
The new programs check finite formulas, a compiler and specified instances.
They do not implement a general large correlated cut/first-event engine and
do not execute physical calibration, source preparation, detectors or pins.
The general consequence follows from the full constructions and the accepted
governing algorithms, not from a small benchmark. No economical physical
regime or universal lower cost is claimed.

CERTIFICATES
PRESERVATION_RECEIPT.json verifies every original and its preserved copy.
SHA256_MANIFEST.json hashes every package file except itself.
The outer ZIP's receipt is saved beside the delivered ZIP.
The public governing revision is 719e201332992002528c221c49f80f69431485f6;
all public source links and the distinction between premises and executions
are retained in the reports and original source registers.
'''
    (DEST / 'README.txt').write_text(readme)
    sources = {
        'governing_revision':'719e201332992002528c221c49f80f69431485f6',
        'governing_url':'https://github.com/harjassand/astra-research-knowledge/tree/719e201332992002528c221c49f80f69431485f6/research/returns/2026-11-05-p3-first-event',
        'primary_research':[
            'https://arxiv.org/abs/1906.09282',
            'https://arxiv.org/abs/1805.06917',
            'https://arxiv.org/abs/math/0309222',
            'https://arxiv.org/abs/1709.07710',
            'https://www.cs.cornell.edu/~rdk/papers/stoc17-rad.pdf',
            'https://arxiv.org/abs/1507.00843',
            'https://web.stanford.edu/~jblanche/papers/RareJackson7.pdf',
            'https://wrap.warwick.ac.uk/id/eprint/84735/3/WRAP_st-160317-wrap_-reverse_time_smc.pdf',
            'https://www.math.colostate.edu/~aristoff/parrep_dynamics.pdf',
            'https://arxiv.org/abs/1903.10474',
            'https://proceedings.mlr.press/v139/dutt21a.html'],
        'retrieval_limit':'2026 conditional-path Monte Carlo abstracts were found, but their full texts were unavailable; no theorem-level comparison is claimed.',
        'preservation':'Earlier exact source revisions remain in the unmodified nested original source registers.'
    }
    (DEST/'GOVERNING_SOURCES.json').write_text(json.dumps(sources,indent=2)+'\n')
    files = {str(p.relative_to(DEST)):sha(p) for p in sorted(DEST.rglob('*'))
             if p.is_file() and p.name != 'SHA256_MANIFEST.json'}
    # Preserve nested original manifests as ordinary hashed files too.
    for p in sorted((DEST/'preserved_first_event').rglob('SHA256_MANIFEST.json')):
        files[str(p.relative_to(DEST))]=sha(p)
    manifest = dict(algorithm='SHA-256', files=dict(sorted(files.items())))
    (DEST/'SHA256_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    OUT.mkdir(exist_ok=True)
    with zipfile.ZipFile(ZIPOUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(DEST.rglob('*')):
            if p.is_file(): z.write(p,p.relative_to(DEST.parent))
    with zipfile.ZipFile(ZIPOUT) as z:
        assert z.testzip() is None
        for name,digest in BASELINE['files'].items():
            key=str((DEST.name and Path(DEST.name))/'preserved_first_event'/name)
            assert hashlib.sha256(z.read(key)).hexdigest()==digest
    result = {
        'pdf':str(PDFOUT),'pdf_sha256':sha(PDFOUT),'pdf_bytes':PDFOUT.stat().st_size,
        'zip':str(ZIPOUT),'zip_sha256':sha(ZIPOUT),'zip_bytes':ZIPOUT.stat().st_size,
        'package_files':sum(p.is_file() for p in DEST.rglob('*')),
        'original_files_verified':len(matches),'all_originals_unchanged':True,
        'zip_crc_check':'passed','zip_original_sha256_check':'passed'
    }
    (OUT/'Astra_Acquired_First_Event_Package_Receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
