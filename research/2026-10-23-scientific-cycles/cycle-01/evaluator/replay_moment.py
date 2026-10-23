"""Relocatable replay of the two accepted moment witnesses.

python replay_moment.py                 # verify supplied witnesses and source binding
python replay_moment.py --construct     # additionally reconstruct both, no retuning

Requires Python3 and numpy for the independent saved-NPZ input identity check.
The constructor's interval arithmetic is supplied in the unchanged Pro2 archive.
This replays conditional exact computations, not the global mathematical proofs.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

start = time.perf_counter()
root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--construct', action='store_true')
args = parser.parse_args()
archive = root / 'sources/Astra_Restore_PRO2_20261021.zip'
assert hashlib.sha256(archive.read_bytes()).hexdigest() == 'f58b4f09eb259f0ac2d3962b955abd0fc7d603a7960a038257b72b1f00624115'
receipts = []
def run(argv, cwd):
    t = time.perf_counter()
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=60, check=True)
    return p.stdout, time.perf_counter() - t
with tempfile.TemporaryDirectory(prefix='astra_moment_receiving_') as td:
    temp = Path(td)
    with zipfile.ZipFile(archive) as z:
        for item in z.infolist():
            p = PurePosixPath(item.filename)
            assert not p.is_absolute() and '..' not in p.parts
            assert ((item.external_attr >> 16) & 0o170000) != 0o120000
        z.extractall(temp)
    owner = temp / 'Astra_Restore_PRO2_20261021'
    assert (owner / 'results/krylov_certificates.json').is_file()
    base = root / 'experiments/moment'
    constructor = (base / 'stage1_frozen/construct.py').read_text()
    for probe, relative in [(0, 'stage1_frozen'), (7, 'heldout_ell7')]:
        supplied = base / relative
        witness = temp / ('probe_' + str(probe))
        witness.mkdir()
        construction_seconds = None
        if args.construct:
            # Only bind source location and selected saved probe; preserve the mathematics.
            adapted, n = re.subn(r'^ROOT=Path\(.*\)$', lambda _: 'ROOT=Path(' + repr(str(owner)) + ')', constructor, count=1, flags=re.M)
            assert n == 1
            assert "c=jall['64'][0]" in adapted
            adapted = adapted.replace("c=jall['64'][0]", "c=jall['64'][" + str(probe) + "]", 1)
            (witness / 'construct.py').write_text(adapted)
            _, construction_seconds = run([sys.executable, str(witness / 'construct.py')], witness)
        else:
            for name in ['input.json', 'maximum_witness.json', 'near_infimum_witness.json', 'summary.json']:
                shutil.copy2(supplied / name, witness / name)
        shutil.copy2(base / 'stage1_frozen/verify.py', witness / 'verify.py')
        output, verification_seconds = run([sys.executable, str(witness / 'verify.py')], witness)
        verification = json.loads(output)
        output, binding_seconds = run([sys.executable, str(base / 'bind_to_owner.py'), str(owner), str(witness), str(probe)], witness)
        binding = json.loads(output)
        assert verification['PASS'] and binding['PASS']
        summary = json.loads((witness / 'summary.json').read_text())
        receipts.append({'probe': probe, 'exact_witness_pass': verification['PASS'],
          'independent_source_binding_pass': binding['PASS'], 'construction_wall_seconds': construction_seconds,
          'verification_subprocess_wall_seconds': verification_seconds, 'binding_subprocess_wall_seconds': binding_seconds,
          'ambiguity_width': summary['extremal_width'], 'infimum_attained': summary['infimum_inclusive']['attained']})
print(json.dumps({'PASS': True, 'reconstructed': args.construct, 'receipts': receipts,
 'whole_receiving_wrapper_wall_seconds': time.perf_counter() - start,
 'scope': 'Exact atomic checks and pinned input binding at ell0/ell7. Global dual inequalities need the written proof; no joint-probe or speedup claim.'}, indent=2))
