"""Initial primary-data analysis. Predictions use the released Gaussian BAO likelihood."""
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.integrate import quad
from scipy.stats import chi2
ROOT=Path(__file__).resolve().parent
raw=np.loadtxt(ROOT/'data/desi_gaussian_bao_ALL_GCcomb_mean.txt',dtype=str)
z=raw[:,0].astype(float); d=raw[:,1].astype(float); kind=raw[:,2]
C=np.loadtxt(ROOT/'data/desi_gaussian_bao_ALL_GCcomb_cov.txt'); W=np.linalg.inv(C)
zn=np.unique(z)
from numpy.polynomial.legendre import leggauss
xx,ww=leggauss(64)
zz=(xx[None,:]+1)*zn[:,None]/2
weights=ww[None,:]*zn[:,None]/2

def pred(p,mode='lcdm'):
    om,t=p[:2] # t = c/(H0 rd)
    if mode=='lcdm':
        eh=lambda x: om*(1+x)**3+1-om
    else:
        w0,wa=p[2:]
        eh=lambda x:om*(1+x)**3+(1-om)*(1+x)**(3*(1+w0+wa))*np.exp(-3*wa*x/(1+x))
    dh=t/np.sqrt(eh(zn)); dm=t*(weights/np.sqrt(eh(zz))).sum(axis=1)
    dv=np.cbrt(zn*dm**2*dh)
    j=np.searchsorted(zn,z)
    return np.array([dict(DH_over_rs=dh,DM_over_rs=dm,DV_over_rs=dv)[k][i] for k,i in zip(kind,j)])
def cost(p,mode='lcdm'):
    r=pred(p,mode)-d
    return float(r@W@r)
res=minimize(cost,[.30,30.],method='Nelder-Mead',options={'maxiter':10000,'xatol':1e-11,'fatol':1e-11})
print('LCDM:',res.x,'chi2',res.fun,'nominal dof 11, p',chi2.sf(res.fun,11))
print('A=',res.x[0]/res.x[1]**2,'B=',(1-res.x[0])/res.x[1]**2)
for p0 in [[.30,30,-1,0],[.35,30,-.6,-1.5],[.2,30,-1,.5]]:
    rr=minimize(lambda x:cost(x,'cpl'),p0,bounds=[(.01,.7),(15,50),(-3,1),(-10,5)],method='Nelder-Mead',options={'maxiter':10000,'xatol':1e-10,'fatol':1e-10})
    print('CPL:',rr.x,'chi2',rr.fun)
print('data and baseline predicted residuals in marginal sigma:')
for v,pp,sd,k,rz in zip(d,pred(res.x),np.sqrt(np.diag(C)),kind,z):print(rz,k,v,pp,(v-pp)/sd)
mask=kind=='DH_over_rs'; zs=z[mask];ds=d[mask];ss=np.sqrt(np.diag(C))[mask]
# secant matter ceilings in h^2 units
for i in range(len(zs)-1):
 j=i+1;dx=(1+zs[j])**3-(1+zs[i])**3
 cap=(1/ds[j]**2-1/ds[i]**2)/dx
 err=2*np.sqrt((ss[j]/ds[j]**3)**2+(ss[i]/ds[i]**3)**2)/dx
 print('matter cap',zs[i],zs[j],cap,err)
np.savez(ROOT/'results'/'baseline.npz',lcdm_parameters=res.x,lcdm_prediction=pred(res.x),lcdm_chi2=res.fun)
