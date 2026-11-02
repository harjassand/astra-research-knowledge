import sys,runpy,os
from pathlib import Path
p=Path(sys.argv[1]).resolve()
def audit(event,args):
 if event=="open" and args and isinstance(args[0],(str,bytes,os.PathLike)):
  s=os.fsdecode(args[0])
  if s.startswith("producer-workspace/shared"):raise RuntimeError("Original science path forbidden: "+s)
sys.addaudithook(audit)
sys.path.insert(0,str(p.parent))
runpy.run_path(str(p),run_name="__main__")
