import runpy,contextlib,io,json
from pathlib import Path
import numpy as np
root=Path(__file__).parent
with contextlib.redirect_stdout(io.StringIO()):state=runpy.run_path(str(root/'capture_one_axis.py'))
lw=state['logw'];probs=np.exp(lw-lw.max(axis=1)[:,None]);probs/=probs.sum(axis=1)[:,None]
r=dict(source='exact replay capture_one_axis.py',T=state['T'],probe_calls=state['nprobe'],service_calls=state['nservice'],final_logweights=lw.tolist(),final_candidate_probabilities=probs.tolist(),final_bath_real=state['bath'].real.tolist(),final_bath_imag=state['bath'].imag.tolist(),net_rotations=state['Cs'].tolist(),net_unitaries_real=state['Vs'].real.tolist(),net_unitaries_imag=state['Vs'].imag.tolist(),hidden_indices=state['hidden'],post_training_policy='For a declared evaluation only: continue source index1, theta0.8 hidden collective Jz coupled to bathZ plus0.37 bathX. No additional training and no implication of future real-source stationarity.')
(root/'one_axis_controller_checkpoint.json').write_text(json.dumps(r,indent=2)+'\n');print('checkpoint written')
