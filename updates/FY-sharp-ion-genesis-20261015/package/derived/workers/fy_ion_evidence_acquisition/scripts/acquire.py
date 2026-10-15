"""Download publicly available primary sources; originals stay local, unmodified.
Usage: python acquire.py NAME URL [NAME URL ...]
Records successful and unsuccessful attempts with SHA256, bytes, and media type.
"""
import datetime
import hashlib
import json
import pathlib
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / 'raw_originals'
MANIFEST = ROOT / 'acquisition_manifest.json'
records = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else []
assert len(sys.argv[1:]) % 2 == 0
for name, url in zip(sys.argv[1::2], sys.argv[2::2]):
    if pathlib.Path(name).name != name:
        raise ValueError('Only a filename is allowed')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; scientific source acquisition)'})
    rec = {'name': name, 'requested_url': url, 'acquired_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(req, timeout=90) as res:
            data = res.read()
            rec.update(status=res.status, final_url=res.url, headers=dict(res.headers))
        path = RAW / name
        if path.exists() and path.read_bytes() != data:
            raise ValueError('Refusing to overwrite changed source bytes')
        path.write_bytes(data)
        rec.update(local_path=str(path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), signature_hex=data[:16].hex())
    except Exception as exc:
        rec['error'] = repr(exc)
        if isinstance(exc, urllib.error.HTTPError):
            rec.update(status=exc.code, final_url=exc.url, headers=dict(exc.headers))
    records.append(rec)
    MANIFEST.write_text(json.dumps(records, indent=2) + '\n')
    print(json.dumps({k:v for k,v in rec.items() if k not in ['headers']}, sort_keys=True), flush=True)
