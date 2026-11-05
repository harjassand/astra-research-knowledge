"""Package new proofs and checks, preserving the accepted predecessor bytes."""
from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).resolve().parent
out=root.parent/'deliverables'
report=out/'Astra_Bounded_Quantum_Factories.pdf'
previous=out/'Astra_Robust_Many_Body_Preparation_Research_Package.zip'
expected='ffa37d3d32da9d7319123d0c2644e0f54f2ab04fedb5ec75c51ca0a0cbcddaaa'
actual=hashlib.sha256(previous.read_bytes()).hexdigest()
if actual!=expected: raise RuntimeError('Accepted archive changed')
readme='''ASTRA: BOUNDED QUANTUM FACTORIES
Research construction, 5 November 2026.

Read Astra_Bounded_Quantum_Factories.pdf first. Full technical proofs:
 research/control/complete_map_factory_operation.md
 research/control/classical_only_export.md
 research/architecture/channel_interior_audit.md
 research/architecture/finite_bit_decomposition_fallback.md
 research/comparators/cluster_uniform_cone.md
 research/comparators/primary_comparators.md
 research/forward_metrology.md

Audits and marked failed approaches are included at their stated scopes.
The accepted archive in accepted_predecessor/ is unchanged and recursively
preserves earlier results and useful failures.

Reproduce finite checks with Python 3:
 python research/comparators/cluster_cone_certificate.py
 python research/architecture/verify_cluster_boundary.py
 python research/architecture/verify_complete_map_palette.py
 python research/control/verify_classical_ec.py

The complete-map example requires NumPy and SciPy. These checks supplement
analytic all-length proofs; they are not physical experiments or universal
hardware thresholds. The first repetition-three export argument failed;
the final classical controller uses strict repetition five, two refreshes,
and fresh physical majority-five decoding. Read the corresponding audit.

The all-family apparatus has fixed but extremely unfavorable constants.
Its efficient source retains the inherited numerical convention. The
separate finite-bit fallback can be exponentially expensive. The cluster
family has its own polynomial-bit source and an explicit quantum positivity
certificate; classical control has a separately derived fixed threshold.
Total quantum activity includes the bounded data stage, every calibration
probe, and every one-qubit randomness probe. At fixed positive noise rates,
the forward relative-entropy comparison improves the sufficient homogeneous
calibration-shot scaling to linear in chain length; its inverse-rate and
visibility constants remain paid.

No total-resource advantage over an equally informed comparator is proved.
The operation retains the specified stationary circuit law, finite ports,
actual classical protection, acquisition, reset, timing, routing and delivery.
'''
(root/'README_PACKAGE.txt').write_text(readme)
paths=[]
for p in sorted(root.rglob('*')):
    if not p.is_file() or any(x in p.parts for x in ('tmp','equations','__pycache__')): continue
    if p.name in ('package_manifest.json','library_receipt.json'): continue
    if p.suffix in ('.py','.md','.json','.txt','.png','.svg'): paths.append(p)
manifest={'accepted_predecessor_sha256':actual,
 'report_sha256':hashlib.sha256(report.read_bytes()).hexdigest(),'entries':[]}
target=out/'Astra_Bounded_Quantum_Factories_Research_Package.zip'
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    z.write(report,report.name)
    z.writestr('README.txt',readme)
    z.write(previous,'accepted_predecessor/'+previous.name,compress_type=zipfile.ZIP_STORED)
    for p in paths:
        name='research/'+p.relative_to(root).as_posix()
        data=p.read_bytes()
        z.writestr(name,data)
        manifest['entries'].append({'path':name,'size':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    z.writestr('manifest.json',json.dumps(manifest,indent=2))
with zipfile.ZipFile(target) as z:
    assert hashlib.sha256(z.read('accepted_predecessor/'+previous.name)).hexdigest()==expected
    assert z.testzip() is None
manifest['package_sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
manifest['package_bytes']=target.stat().st_size
(root/'package_manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'file':str(target),'bytes':target.stat().st_size,
 'sha256':manifest['package_sha256'],'previous_preserved':True},indent=2))
