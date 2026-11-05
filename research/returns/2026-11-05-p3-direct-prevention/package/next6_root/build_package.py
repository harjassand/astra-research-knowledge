"""Build this research continuation; verify and preserve every prior byte."""
from pathlib import Path
import hashlib,json,shutil,zipfile

WORK=Path(__file__).resolve().parent.parent
DEST=WORK/'direct_prevention_research_package'
SOURCE=WORK/'acquired_first_event_research_package'
OUT=WORK/'output'
PDF=OUT/'pdf/Astra_Direct_Acquired_Prevention.pdf'
ZIP=OUT/'Astra_Direct_Prevention_Research_Package.zip'
DIRECTORIES=['next6_root','next6_decision_theory','next6_direct_decision',
             'next6_rate_assay','next6_physical','next6_preparation']

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    baseline=json.loads((WORK/'next6_root/PRESERVATION_BASELINE.json').read_text())
    files=baseline['files']
    assert len(files)==229
    for item in files:
        assert sha(SOURCE/item['path'])==item['sha256'],item['path']
    DEST.mkdir(exist_ok=True)
    preserved=DEST/'preserved_acquired_first_event'
    shutil.copytree(SOURCE,preserved,dirs_exist_ok=True)
    for directory in DIRECTORIES:
        for p in sorted((WORK/directory).rglob('*')):
            if not p.is_file():continue
            rel=p.relative_to(WORK/directory)
            if any(s in ('tmp','__pycache__') for s in rel.parts):continue
            if p.suffix in ('.aux','.log','.out','.pyc','.toc'):continue
            if p.name.startswith('compile_') and p.name.endswith('.txt'):continue
            if p.name in ('compile_stdout.txt','build.stdout.txt'):continue
            target=DEST/directory/rel
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(p,target)
    PDF.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(WORK/'next6_root/direct_prevention_report.pdf',PDF)
    shutil.copy2(PDF,DEST/PDF.name)
    for item in files:
        assert sha(preserved/item['path'])==item['sha256']
    receipt={'original_file_count':len(files),'all_originals_unchanged':True,
      'all_preserved_copies_match':True,'original_bytes':sum(x['size'] for x in files),
      'original_baseline':'next6_root/PRESERVATION_BASELINE.json',
      'governing_prior_revision':'719e201332992002528c221c49f80f69431485f6'}
    (DEST/'PRESERVATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    readme='''DIRECT ACQUIRED PREVENTION WITHOUT ABSOLUTE FORECASTS
5 November 2026

Start with Astra_Direct_Acquired_Prevention.pdf (complete main report).
The endpoint is a finite acquired intervention decision for the mean time
to a singleton all-failed state in heterogeneous interacting binary Gibbs
systems. Menus change reciprocal kinetics and share the same unknown
invariant law. Local reliability, operating clock and mixing envelopes are
certified; declared model closure and faithful experimental copies remain
premises. This is not a general natural-system safety certificate.

MAIN CONSTRUCTIONS
next6_root/: main proof sources; exact-rational boundary certificate;
growing interacting-ring binary-hold execution; finite coarse acquisition;
same-data arbitrary-safe-start, finite warm-up and one-bit deployment composition; full
cost evaluation; original preservation baseline and this package builder.
The root report inputs the rate-assay proof and prediction lower bound
from their independent folders. Recompile from next6_root/ using pdflatex
twice on direct_prevention_report.tex.

next6_rate_assay/: finite grouped first-exit assay for the arithmetic mean
of heterogeneous operating recovery rates, exact censor/clip/timer/error
costs, dependent-cell confidence and matched exposure lower bound.
Its eight-page PDF and complete source and execution are included.
The canonical execution is the linear-contrast direct-mean schedule.
The larger median-of-means historical execution remains separately named.

next6_decision_theory/: full absolute-prediction information lower bound,
independent exact optimization of all clock-module assignments under its
additional transferable-module and independent-component premises,
finite return certificate, rational audits, receipts and sources.

next6_direct_decision/: independent continuum completion-time minimization
under certified reciprocal multiplier access. This is a different objective
and its general evaluated schedule is enormous. Complete PDF, proof,
execution, costs and useful failed routes are retained.

next6_physical/: independent quantum export without Hamiltonian learning,
with actual additional source-control access, pure coherent Weyl ports,
full-dilation comparison, finite pulses and receiver costs. Its three
governing P1 source files and hashes are included. BOUNDARY_COMPARATOR.md
contains the independent true-generator boundary-decision derivation.

next6_preparation/: a retained stronger relative-density relaxation theorem
from Marton's quantitative influence condition and hypercontractivity,
with exact finite schedules and explicit whole-system exposure. The
mean-only main decision instead uses its uniform safe-start theorem and
bounded operating warm-up, with a one-bit alternative. The inspection
companion proves the dominating-process warm-up and states its own read
and latency premises; a perfect-inspection ledger is labeled as such.

REPRODUCTION
From the package root:
  python3 next6_root/run_direct_decision.py
  python3 next6_root/compose_deployment.py
  python3 next6_root/calibration_ledger.py
  python3 next6_rate_assay/audit_rate_assay.py
Other independent folders give their own commands and environments.
Running a program can refresh result files in the extracted copy.

EXECUTION AND PRACTICAL LIMITS
The root execution simulates actual-context binary holds. Coarse bounds
are supplied to that execution; a finite acquisition protocol is proved
and its conservative bill evaluated, not physically executed. The rate
assay is a separate synthetic service execution. One-bit physical meter
fidelity, latency and warm-up prices are evaluated, not manufactured.
No experiment excludes arbitrary omitted failure mechanisms. No
economical general prototype, historical priority or civilization-scale
impact is asserted. Ordinary capacity, exact product, likelihood,
rearrangement and concentration methods are explicit comparators.

PRESERVED ORIGINALS
preserved_acquired_first_event/ contains ALL 229 files of the immediately
preceding complete package, byte for byte, including nested sources,
manifests, earlier independent results and failed attempts. This preserves
the full fitted-model and experiment-fed first-event constructions and
their marked-law bridge; operating/static coin constructions; first-event
clock and sampling; active acquisition and prevention; fixed-law and
thermal constructions; correlated reliability and whole-CDF results;
passive and deferred quantum calibration; all-strength quantum laws,
effusion and the earlier governing scopes. Older incomplete statuses are
historical and are not silently rewritten by this continuation.

INTEGRITY
PRESERVATION_RECEIPT.json verifies the prior originals and copied bytes.
SHA256_MANIFEST.json covers every file except that top-level manifest.
Nested original manifests are ordinary preserved and hashed files.
The outer ZIP receipt verifies CRCs and the original SHA-256 values again.
Source/access/noise assumptions are part of the results, not learned facts
about an unspecified natural system.
'''
    (DEST/'README.txt').write_text(readme)
    sources={'prior_governing_revision':'719e201332992002528c221c49f80f69431485f6',
      'prior_governing_url':'https://github.com/harjassand/astra-research-knowledge/tree/719e201332992002528c221c49f80f69431485f6/research/returns/2026-11-05-p3-first-event',
      'primary_comparison_sources':[
       {'title':'Reversible Markov Chains and Random Walks on Graphs','authors':'Aldous and Fill','url':'https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch3.S7.html','use':'Green, Dirichlet, capacity and hitting-time machinery'},
       {'title':'Capacities and efficient computation of first-passage probabilities','authors':'Loper, Zhou and Geman','year':2020,'url':'https://stanniszhou.github.io/papers/diffusion_manuscript.pdf','use':'Strong target-local capacity comparator; not a new invention here'},
       {'title':'On the Complexity of Best-Arm Identification in Multi-Armed Bandit Models','authors':'Kaufmann, Cappe and Garivier','year':2016,'url':'https://www.jmlr.org/papers/volume17/kaufman16a/kaufman16a.pdf','use':'Established sequential change-of-measure machinery'},
       {'title':'Statistical Inference, Chapter 3 Example 3.4','authors':'Garcia-Portugues and Molina','url':'https://egarpor.github.io/SI-UC3M/point.html','use':'Classical unbiased exponential-rate statistic'},
       {'title':'On Tail Probabilities for Martingales','authors':'Freedman','year':1975,'doi':'10.1214/aop/1176996452','use':'Martingale concentration; needed bound proved directly'},
       {'title':'Logarithmic Sobolev inequalities in discrete product spaces: a proof by a transportation cost distance','authors':'Marton','url':'https://arxiv.org/abs/1507.02803','use':'Retained stronger relative-density preparation, with acquired spectral influence condition'},
       {'title':'Random decoupling schemes for quantum dynamical control and error suppression','authors':'Viola and Knill','url':'https://arxiv.org/abs/quant-ph/0511120','use':'Independent quantum construction prior machinery'},
       {'title':'Faster Randomized Dynamical Decoupling','authors':'Yi, Kim and Marvian','url':'https://arxiv.org/abs/2409.18369','use':'Independent quantum construction comparison'}],
      'scope':'Full exact source registers also remain in every independent and preserved folder. No historical-priority claim.'}
    (DEST/'GOVERNING_SOURCES.json').write_text(json.dumps(sources,indent=2)+'\n')
    manifest={str(p.relative_to(DEST)):sha(p) for p in sorted(DEST.rglob('*'))
              if p.is_file() and p!=DEST/'SHA256_MANIFEST.json'}
    (DEST/'SHA256_MANIFEST.json').write_text(json.dumps({'algorithm':'SHA-256','files':manifest},indent=2)+'\n')
    with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(DEST.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(DEST.parent))
    with zipfile.ZipFile(ZIP) as z:
        assert z.testzip() is None
        for item in files:
            key=str(Path(DEST.name)/'preserved_acquired_first_event'/item['path'])
            assert hashlib.sha256(z.read(key)).hexdigest()==item['sha256']
    result={'pdf':str(PDF),'pdf_bytes':PDF.stat().st_size,'pdf_sha256':sha(PDF),
      'zip':str(ZIP),'zip_bytes':ZIP.stat().st_size,'zip_sha256':sha(ZIP),
      'original_files_verified':len(files),'all_originals_unchanged':True,
      'package_files':len(manifest)+1,'zip_crc_check':'passed',
      'zip_original_sha256_check':'passed'}
    (OUT/'Astra_Direct_Prevention_Package_Receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
