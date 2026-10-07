from pathlib import Path
import hashlib,json,zipfile
p=Path(__file__).resolve().parent;m=json.loads((p/'manifest.json').read_text());dst=p/m['archive_name'];h=hashlib.sha256()
with dst.open('wb') as out:
 for row in m['parts']:
  b=(p/row['name']).read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'];out.write(b);h.update(b)
assert dst.stat().st_size==m['archive_bytes'] and h.hexdigest()==m['archive_sha256']
with zipfile.ZipFile(dst) as z:assert len(z.namelist())==m['member_count'] and z.testzip() is None
print('Exact archive reassembled and CRC verified:',dst)
