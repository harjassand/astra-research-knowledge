#!/usr/bin/env python3
"""Verify exact payload hashes, locally or inside a delivered ZIP."""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile


def digest(b): return hashlib.sha256(b).hexdigest()


def verify(root=None,archive=None):
    if archive:
        with ZipFile(archive) as z:
            assert z.testzip() is None,'CRC failure'
            manifests=[n for n in z.namelist() if n.count('/')==1 and n.endswith('/MANIFEST.json')]
            assert len(manifests)==1,'top-level manifest missing or ambiguous'
            prefix=manifests[0].rsplit('/',1)[0]+'/'
            manifest=json.loads(z.read(manifests[0]))
            for item in manifest['files']:
                b=z.read(prefix+item['path'])
                assert len(b)==item['bytes'] and digest(b)==item['sha256'],item['path']
            actual={n[len(prefix):] for n in z.namelist() if n.startswith(prefix) and not n.endswith('/')}
            assert actual=={x['path'] for x in manifest['files']}|{'MANIFEST.json'},'unexpected ZIP members'
    else:
        root=Path(root or Path(__file__).resolve().parent)
        manifest=json.loads((root/'MANIFEST.json').read_text())
        for item in manifest['files']:
            b=(root/item['path']).read_bytes()
            assert len(b)==item['bytes'] and digest(b)==item['sha256'],item['path']
    return {'status':'passed','payload_files':len(manifest['files']),
            'qualification':'Byte integrity only, not mathematical acceptance.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--zip',type=Path)
    a=p.parse_args();print(json.dumps(verify(archive=a.zip),indent=2))
