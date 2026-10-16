from pathlib import Path
import zipfile,sys
r=Path(__file__).resolve().parent
out=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else r.with_suffix('.zip')
if out.is_relative_to(r): raise RuntimeError('ZIP must be outside source directory')
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(r.rglob('*')):
  if not p.is_file() or '__pycache__' in p.parts: continue
  i=zipfile.ZipInfo(r.name+'/'+p.relative_to(r).as_posix(),date_time=(2026,10,15,0,0,0));i.external_attr=0o100644<<16
  z.writestr(i,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
print(out)
