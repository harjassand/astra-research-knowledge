"""Save the declared once-through comparator path; no recycle loop rerun."""
import sys,json,time,resource
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));import ideal_recycle as m
st=time.monotonic();yh,q,rem,neg=m.heater(2700.);yp,s=m.cool(yh)
np.savez_compressed(P/'once_through_2700_reference.npz',hot_Y=yh,cool_t=s.t,cool_Y=s.y,heater_positive_reaction_J_kg=q,heater_removal_J_kg=rem,final_Y=yp)
(P/'reference_receipt.json').write_text(json.dumps({'scope':__doc__,'NOx_mol_kg':m.no(yp),'wall_s':time.monotonic()-st,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2))
