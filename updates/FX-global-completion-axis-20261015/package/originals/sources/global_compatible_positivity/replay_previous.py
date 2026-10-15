#!/usr/bin/env python3
"""Hash-check and replay the unchanged incoming package in an isolated directory."""
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
import hashlib,json,subprocess,sys,zipfile

root=Path(__file__).parent
archive=root/'inputs'/'previous_moving_kernel_package.zip'
receipt={'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'checks':[]}
with zipfile.ZipFile(archive) as z:
    prefix='astra_compatible_heat_result/'
    manifest=json.loads(z.read(prefix+'MANIFEST.json'))
    for name,item in manifest['files'].items():
        payload=z.read(prefix+name)
        assert len(payload)==item['bytes'],name+' size'
        assert hashlib.sha256(payload).hexdigest()==item['sha256'],name+' hash'
    receipt['manifest_payloads_checked']=len(manifest['files'])
    with TemporaryDirectory(prefix='astra_prior_replay_') as work:
        dest=Path(work)
        for member in z.infolist():
            parts=PurePosixPath(member.filename)
            if parts.is_absolute() or '..' in parts.parts:
                raise ValueError('unsafe archive path')
            if member.is_dir():
                (dest/member.filename).mkdir(parents=True,exist_ok=True)
            else:
                target=dest/member.filename
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(z.read(member))
        cwd=dest/'astra_compatible_heat_result'
        for name in ['verify_moving_acoustic.py','verify_structure.py','reconstruct.py']:
            run=subprocess.run([sys.executable,name],cwd=cwd,text=True,capture_output=True,timeout=180,check=False)
            receipt['checks'].append({'script':name,'returncode':run.returncode,'stdout':run.stdout,'stderr':run.stderr})
            print(run.stdout,end='')
            if run.returncode:
                (root/'PREVIOUS_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
                raise RuntimeError(name+' failed')
receipt['status']='HASH_CHECK_AND_EXACT_REPLAY_PASS'
receipt['scope']='Incoming finite algebra replay; separate from external analytic review or priority.'
(root/'PREVIOUS_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('Previous package hash-check and replay passed.')
