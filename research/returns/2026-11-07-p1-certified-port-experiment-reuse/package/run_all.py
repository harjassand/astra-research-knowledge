"""Run the complete executed SOFTWARE example and exact claim controls."""
import json,sys,time
from pathlib import Path
import numpy,scipy
import run_acquire,run_use,run_controls


if __name__=='__main__':
    start=time.perf_counter()
    run_acquire.main()
    run_use.main()
    run_controls.main()
    report={'python':sys.version.split()[0],'numpy':numpy.__version__,
            'scipy':scipy.__version__,'elapsed_seconds':time.perf_counter()-start,
            'source_channel':'finite-harmonic software, continuously evolving state',
            'between_trial_resets':0,'physical_experiments':0,
            'general_SDP_fallback_execution':False,'general_CAD_execution':False,
            'digital_hold_waveform_execution':False,'new_workers':0}
    (Path(__file__).resolve().parent/'results'/'runtime.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'runtime':report}),flush=True)
