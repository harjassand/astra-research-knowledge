"""One fixed direct-field baseline on exactly the same synthetic specimen.

No search over losses, material coefficients, or optimized pulse families.
This comparator is not a proof of superiority against optimal direct writing.
"""
from pathlib import Path
import json
import numpy as np
from coupled_cycle import Bar

OUT=Path(__file__).resolve().parent

class Direct(Bar):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        ym=(3*self.b+np.sqrt(9*self.b**2-20*self.a*self.c))/(10*self.c)
        qm=-np.sqrt(ym)
        self.hspin=self.a*qm-self.b*qm**3+self.c*qm**5
        self.H=1.5*self.hspin

    def controls(self,t,T):
        if t<T:
            h=self.H*np.sin(np.pi*t/T)**2
            hd=self.H*np.pi/T*np.sin(2*np.pi*t/T)
            return h,hd,None,self.B,'direct_bias'
        return 0.,0.,None,self.B,'passive_short'

results=[]
for T in [2.,20.,100.]:
    b=Direct(subdivisions=16)
    r,d=b.run(T,100.,rtol=7e-8,atol=7e-10)
    r.update(case=f'direct_{T:g}',field_peak=b.H,
             homogeneous_composite_spinodal=b.hspin,
             pulse='H*sin(pi*t/T)^2; H=1.5 homogeneous negative-well spinodal',
             comparator_limit='One unoptimized pulse; not the minimum cost at specified fidelity/time.')
    results.append(r)
    np.savez_compressed(OUT/f'direct_{T:g}_trajectory.npz',**d)
    print(json.dumps(r),flush=True)
(OUT/'direct_field_results.json').write_text(json.dumps({'same_fixed_specimen_and_losses':True,'cases':results},indent=2)+'\n')
