#!/usr/bin/env python3
"""Package scientific state, scoped reviews, and the unchanged prior archive.

This verifies archival identity only. It does not re-audit predecessor science.
Run from the preserved workspace; the resulting ZIP is independently readable.
"""
from pathlib import Path
import hashlib
import json
import zipfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    branch=Path(__file__).resolve().parents[1]
    project=branch.parents[1]
    workspace=project.parent
    predecessor=workspace/'Astra_P1_Thermal_Information_and_Control_20261029.zip'
    prior_bytes=predecessor.read_bytes()
    expected='e3da657427435e01b47e19fd48763c062188d8d717714f59b05fbe0350910862'
    assert digest(prior_bytes)==expected, 'Predecessor archive identity changed'
    target=workspace/'Astra_P1_Acquired_Operation_Algebra_20261029.zip'

    # Reproducible raw public-web readouts are scratch intermediates. The saved
    # primary source indices retain URLs, versions, inspected scope and comparison.
    # User/Astra governing sources and all new proofs/reviews/code are preserved.
    omitted={
        'port_frontier/sources/port_full_primary.json',
        'port_frontier/sources/port_gle_paper_routes.json',
        'port_frontier/sources/port_primary_details.json',
        'port_frontier/sources/port_primary_sources.json',
    }
    entries={}
    for path in sorted(branch.rglob('*')):
        if not path.is_file() or '__pycache__' in path.parts:
            continue
        relative=path.relative_to(branch).as_posix()
        if relative in omitted:
            continue
        entries['new_science/'+relative]=path.read_bytes()
    entries['predecessor/'+predecessor.name]=prior_bytes
    for name in ['README.md','CURRENT_SCIENCE_STATE.md']:
        entries['project_entrypoints/'+name]=(project/name).read_bytes()
    entries['HANDOFF.md']=(
        '# Start here\n\nThe new proof, code, review and source paths in the '
        'handoff below are relative to **new_science/**. The complete previous '
        'snapshot is preserved byte-for-byte under **predecessor/**.\n\n'
        +(branch/'HANDOFF.md').read_text()).encode()
    entries['README.md']=(
        '# Astra P1: acquired operation algebra and finite predictive preparation\n\n'
        'Read [HANDOFF.md](HANDOFF.md), then '
        '[the scientific overview](new_science/README.md).\n\n'
        'The latest receiving proof is '
        '[FINITE_ERROR_PREDICTIVE_PREPARATION.md]'
        '(new_science/FINITE_ERROR_PREDICTIVE_PREPARATION.md). '
        'It follows the physical acquisition construction and the exact-rank '
        'diffusion obstruction. Ordinary proofs, executable population checks, '
        'source comparisons, scoped reviews and corrections are preserved.\n\n'
        'The archive does not claim a physical assay, practical speedup, '
        'external acceptance or established priority. Historical archived '
        'operational instructions do not replace the current user assignment.\n').encode()
    manifest={
        'snapshot':'Astra P1 acquired operation algebra and finite predictive preparation',
        'date':'2026-10-29',
        'predecessor_sha256':expected,
        'predecessor_bytes':len(prior_bytes),
        'omitted_reproducible_public_lookup_intermediates':sorted(omitted),
        'omission_scope':'Only raw public-web readouts and Python caches; primary indices, governing Astra sources and all scientific artifacts remain.',
        'entries':{name:{'bytes':len(data),'sha256':digest(data)}
                   for name,data in sorted(entries.items())},
    }
    manifest_bytes=(json.dumps(manifest,indent=2)+'\n').encode()
    temporary=target.with_suffix('.zip.tmp')
    with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(entries.items()):
            z.writestr(name,data)
        z.writestr('MANIFEST.json',manifest_bytes)
    temporary.replace(target)
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        for name,entry in manifest['entries'].items():
            data=z.read(name)
            assert len(data)==entry['bytes'] and digest(data)==entry['sha256']
        assert z.read('predecessor/'+predecessor.name)==prior_bytes
    print(json.dumps({'path':str(target),'bytes':target.stat().st_size,
                      'sha256':digest(target.read_bytes()),
                      'entry_count':len(entries)+1,
                      'predecessor_preserved':True,
                      'crc_and_manifest_verification':'PASS'},indent=2))


if __name__=='__main__':
    main()
