from pathlib import Path
import json
import numpy as np
from scipy.linalg import eigh_tridiagonal

def example(a=2.0, barrier=1.0, ngrid=2001):
    x=np.linspace(-7,7,ngrid)
    dx=x[1]-x[0]
    v=barrier*(x*x-a*a)**2
    diag=1/dx**2+v
    off=np.full(ngrid-1,-0.5/dx**2)
    es, us=eigh_tridiagonal(diag,off,select='i',select_range=(0,11))
    # Euclidean-normalized grid vectors already make multiplication matrix
    # elements a plain inner product.
    if us[:,0].sum()<0: us[:,0]*=-1
    if (x@us[:,1])<0: us[:,1]*=-1
    wleft=(us[:,0]-us[:,1])/np.sqrt(2)
    wright=(us[:,0]+us[:,1])/np.sqrt(2)
    mode=np.exp(-x*x/0.7**2)
    p=np.column_stack((wleft,wright))
    mp=p.T@(mode[:,None]*p)
    qnorm=np.sqrt(np.linalg.eigvalsh(p.T@((mode**2)[:,None]*p)-mp@mp).max())
    return {'a':a,'barrier_coefficient':barrier,'energies':es[:6].tolist(),
            'bare_t':float((es[1]-es[0])/2),'orbital_gap':float(es[2]-es[1]),
            'mode_diagonal':float(mp[0,0]),'mode_hopping':float(mp[0,1]),
            'mode_diagonal_mismatch':float(abs(mp[0,0]-mp[1,1])),
            'mode_off_orbital_norm':float(qnorm)}

if __name__=='__main__':
    rows=[example(barrier=b) for b in (0.25,0.5,0.75,1.0,1.5)]
    dest=Path(__file__).with_name('double_well_results.json')
    dest.write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps(rows,indent=2))
