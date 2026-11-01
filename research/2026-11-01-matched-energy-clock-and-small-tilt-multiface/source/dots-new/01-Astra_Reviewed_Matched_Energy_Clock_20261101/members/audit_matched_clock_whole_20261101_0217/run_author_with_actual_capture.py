from pathlib import Path
import sys,runpy,json,os,time
A=Path(__file__).resolve().parent;S=A/'replay/matched_energy_clock_constructor_20261101';sys.path.insert(0,str(S));os.chdir(S)
import receive_matched_clock as r
real=r.certify;full_calls=0

def capture(raw,**task):
 global full_calls
 result=real(raw,**task)
 if type(raw)is dict and raw.get('dimension')==512:
  full_calls+=1;(A/'actual_full_recapture.json').write_text(json.dumps(result,indent=2)+'\n')
 return result
r.certify=capture
runpy.run_path(str(S/'check.py'),run_name='__main__')
assert full_calls==1,full_calls
(A/'actual_full_capture_count.json').write_text(json.dumps({'full_actual_successful_producer_calls':full_calls,'via':'actual verify inside complete copied author suite; no cache or primitive replacement'},indent=2)+'\n')
