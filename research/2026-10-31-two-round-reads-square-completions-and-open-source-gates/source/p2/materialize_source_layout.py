"""Copy verified preserved files to their expected hierarchy; execute no science."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repository',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 root=Path(a.repository).resolve();out=Path(a.output).resolve();spec=json.loads(Path(__file__).with_name('SOURCE_LAYOUT.json').read_bytes());count=0
 for item in spec['files']:
  rel=PurePosixPath(item['destination']);assert not rel.is_absolute() and '..' not in rel.parts
  source=root/item['repository_path'];data=source.read_bytes();assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
  target=out/str(rel);target.parent.mkdir(parents=True,exist_ok=True)
  if target.exists():assert target.read_bytes()==data,str(target)
  else:target.write_bytes(data)
  count+=1
 print(json.dumps(dict(result='pass',files=count,scope='Byte-preserving copy only;no scientist code execution or environment qualification.')))
if __name__=='__main__':main()
