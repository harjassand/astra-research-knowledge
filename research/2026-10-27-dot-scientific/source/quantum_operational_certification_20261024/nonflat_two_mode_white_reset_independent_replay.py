from pathlib import Path
import runpy
q=Path('/workspace/scratch/57d8dd795b13/quantum_operational_certification_20261024');old=Path.write_text
Path.write_text=lambda self,data,*a,**k: len(data) if self.read_text()==data else (_ for _ in ()).throw(AssertionError(str(self)))
try:
 for f in ['nonflat_two_mode_white_rank_one_reset_certificate.py','nonflat_two_mode_white_rank_one_reset_actual_ratio_check.py']:
  print('BEGIN',f,flush=True);runpy.run_path(str(q/f),run_name='__main__')
finally:Path.write_text=old
