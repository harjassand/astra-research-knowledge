import sys,os
FORBIDDEN=('producer-workspace/explicit_memory_witness_20261102','producer-workspace/explicit_cochain_fibers_20261102','producer-workspace/component_decoder_threshold_20261102','producer-workspace/local_duality_transfer_20261102')
def check(event,args):
 if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
  p=os.fsdecode(args[0])
  if any(p.startswith(x) for x in FORBIDDEN):raise RuntimeError('Clean replay attempted original-workspace read: '+p)
sys.addaudithook(check)
