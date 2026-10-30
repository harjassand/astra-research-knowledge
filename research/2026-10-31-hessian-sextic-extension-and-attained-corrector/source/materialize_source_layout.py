"""Copy the supplied Ultra receiver/dependency layout; execute no scientific code."""
from pathlib import Path, PurePosixPath
import argparse,hashlib,json
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repository',required=True);p.add_argument('--layout',required=True);p.add_argument('--output',required=True);a=p.parse_args();root=Path(a.repository).resolve();out=Path(a.output).resolve();spec=json.loads(Path(a.layout).read_bytes())
for item in spec['files']:
 rel=PurePosixPath(item['destination']);assert not rel.is_absolute()and '..'not in rel.parts
 data=(root/item['repository_path']).read_bytes();assert len(data)==item['bytes']and hashlib.sha256(data).hexdigest()==item['sha256']
 target=out/str(rel);target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists():assert target.read_bytes()==data,str(target)
 else:target.write_bytes(data)
print(json.dumps(dict(result='pass',files=len(spec['files']),scientific_execution=False,scope='Byte-preserving copy only;no proof/receiver execution or executed-version certification.')))
