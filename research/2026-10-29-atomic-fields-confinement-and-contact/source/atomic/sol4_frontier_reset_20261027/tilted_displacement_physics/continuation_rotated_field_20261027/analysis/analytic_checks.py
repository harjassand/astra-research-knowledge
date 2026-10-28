from pathlib import Path
import json,math
import numpy as np
from scipy.special import j0
from numpy.polynomial.hermite_e import hermegauss
from rotated_multislice import positive_quad,LAM,ALPHA
ROOT=Path(__file__).resolve().parents[1];cal=json.loads((ROOT/'outputs/probe_calibration.json').read_text());sigma=cal['source_sigma_A'];out={}
# Physical longitudinal phase error. Piston/linear terms are not image aberrations.
x=np.linspace(-ALPHA,ALPHA,161);ux,uy=np.meshgrid(x,x,indexing='ij');mask=ux*ux+uy*uy<=ALPHA*ALPHA;ux=ux[mask];uy=uy[mask];k=2*np.pi/LAM;L=130.
rows=[]
for aa,bb,label in [(0,0,'rotated frame'),(1,10,'direct high-tilt wave')]:
 n=np.r_[np.tan(np.deg2rad([aa,bb])),1.];n/=np.linalg.norm(n);qx=ux+n[0];qy=uy+n[1];r2=qx*qx+qy*qy;phase=k*L*(np.sqrt(1-r2)-1+r2/2)
 basis=np.stack([np.ones(len(ux)),ux,uy],axis=1);fit=basis@np.linalg.lstsq(basis,phase,rcond=None)[0];res=phase-fit
 basis2=np.c_[basis,ux*ux+uy*uy];res2=phase-basis2@np.linalg.lstsq(basis2,phase,rcond=None)[0]
 rows.append(dict(frame=label,phase_error_range_rad=[float(phase.min()),float(phase.max())],rms_after_piston_and_linear_rad=float(np.sqrt(np.mean(res*res))),rms_after_best_isotropic_focus_also_rad=float(np.sqrt(np.mean(res2*res2)))))
out['paraxial_phase']=rows
freq=np.linspace(-2*ALPHA/LAM,2*ALPHA/LAM,2001);rows=[]
for N in [7,9,13,17]:
 h,w=hermegauss(N);h*=sigma;w/=np.sqrt(2*np.pi);numerical=np.exp(-2j*np.pi*freq[:,None]*h)@w;exact=np.exp(-2*np.pi**2*sigma*sigma*freq*freq);rows.append(dict(order=N,max_characteristic_function_error=float(np.max(np.abs(numerical-exact)))))
out['incoherent_source_characteristic_checks']=rows
N=9;h,w=hermegauss(N);h*=sigma;w/=np.sqrt(2*np.pi);phase=(np.arange(32)+.5)*2*np.pi/32;center=4.7703/4;amp=center;s=center+amp*np.cos(phase);yn=(s[:,None]+h[None,:]).ravel();yw=(np.ones((len(s),1))/len(s)*w[None,:]).ravel();rows=[]
full=np.exp(-2j*np.pi*freq[:,None]*yn)@yw
for n in [16,20,24,32]:
 q,v=positive_quad(yn,yw,n);approx=np.exp(-2j*np.pi*freq[:,None]*q)@v;rows.append(dict(order=n,max_error_relative_to_full_discrete_source=float(np.max(np.abs(approx-full)))))
out['scan_position_compression_checks']=rows
out['probe_note']='Source sigma matches continuum incoherent 0.8 A FWHM. Quadrature convergence and actual focus profiles are separately reported.'
(ROOT/'outputs/analytic_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
