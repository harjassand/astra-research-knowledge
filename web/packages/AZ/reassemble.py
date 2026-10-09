from pathlib import Path
import argparse,hashlib,json,os,tempfile
p=argparse.ArgumentParser(description='Reassemble exact AZ evidence bytes from downloaded parts;no scientific code is executed.')
p.add_argument('--directory',default='.')
p.add_argument('--output',default='research_evidence.zip')
a=p.parse_args();root=Path(a.directory);meta=json.loads((root/'package.json').read_text());out=Path(a.output)
if out.exists():
    if out.stat().st_size==meta['bytes'] and hashlib.sha256(out.read_bytes()).hexdigest()==meta['sha256']:print('Existing exact archive verified');raise SystemExit(0)
    raise SystemExit('Output exists with different bytes;choose another --output')
out.parent.mkdir(parents=True,exist_ok=True)
handle,name=tempfile.mkstemp(prefix='.AZ-evidence-',dir=out.parent);total=0;whole=hashlib.sha256()
try:
    with os.fdopen(handle,'wb') as dest:
        for part in sorted(meta['parts'],key=lambda x:x['order']):
            data=(root/part['path']).read_bytes()
            if len(data)!=part['bytes'] or hashlib.sha256(data).hexdigest()!=part['sha256']:raise ValueError('Part integrity mismatch: '+part['path'])
            dest.write(data);whole.update(data);total+=len(data)
    if total!=meta['bytes'] or whole.hexdigest()!=meta['sha256']:raise ValueError('Full archive integrity mismatch')
    os.rename(name,out);print('Reassembled exact archive: '+str(out)+';hashes verify bytes,not scientific truth')
finally:
    if Path(name).exists():Path(name).unlink()
