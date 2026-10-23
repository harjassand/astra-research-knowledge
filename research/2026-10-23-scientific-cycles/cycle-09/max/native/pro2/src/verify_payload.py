"""Check the archived payload manifest; this is transport, not scientific proof."""
from pathlib import Path
import hashlib,json

BASE=Path(__file__).resolve().parents[1]

def main():
    manifest=json.loads((BASE/'PAYLOAD_MANIFEST.json').read_text())
    expected={r['path']:r for r in manifest['files']}
    observed={p.relative_to(BASE).as_posix() for p in BASE.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts
              and p.name!='PAYLOAD_MANIFEST.json'}
    assert observed==set(expected),('payload paths',observed^set(expected))
    for name,row in expected.items():
        data=(BASE/name).read_bytes()
        assert len(data)==row['bytes'],('size',name)
        assert hashlib.sha256(data).hexdigest()==row['sha256'],('digest',name)
    print(json.dumps({'status':'PASS','files':len(expected),
        'scope':'Exact payload transport only; no scientific replay.'}))

if __name__=='__main__':main()
