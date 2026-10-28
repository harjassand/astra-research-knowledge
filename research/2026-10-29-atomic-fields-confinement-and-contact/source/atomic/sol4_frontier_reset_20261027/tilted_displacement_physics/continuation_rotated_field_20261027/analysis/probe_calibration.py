from pathlib import Path
import json, math
import numpy as np
from scipy.special import j1
from scipy.optimize import brentq
from numpy.polynomial.hermite_e import hermegauss
from abtem.core.energy import energy2wavelength
ROOT=Path(__file__).resolve().parents[1]
lam=energy2wavelength(200000);kcut=.032/lam
x=np.linspace(0,2,4001)
def intensity(r):
 z=2*np.pi*kcut*r
 amp=np.empty_like(r);np.divide(j1(z),np.sqrt(np.pi)*r,out=amp,where=r!=0);amp[r==0]=np.sqrt(np.pi)*kcut
 return amp*amp
def mixed(sigma,N):
 p,w=hermegauss(N);w=w/np.sqrt(2*np.pi);p=p*sigma
 return sum(w[i]*w[j]*intensity(np.sqrt((x-p[i])**2+p[j]**2)) for i in range(N) for j in range(N))
def width(y):
 idx=np.where(y<y[0]/2)[0][0];return 2*np.interp(y[0]/2,y[idx-1:idx+1][::-1],x[idx-1:idx+1][::-1])
sigma=brentq(lambda s:width(mixed(s,21))-.8,.05,.6)
rows=[dict(N=n,fwhm_A=width(mixed(sigma,n)),peak_per_A2=float(mixed(sigma,n)[0])) for n in [3,5,7,9,13,21]]
out=dict(energy_eV=200000,aperture_mrad=32,wavelength_A=lam,ideal_fwhm_A=width(intensity(x)),source_sigma_A=sigma,target_broadened_fwhm_A=.8,quadrature_checks=rows)
(ROOT/'outputs/probe_calibration.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
