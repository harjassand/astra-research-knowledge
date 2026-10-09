"""Independent checks and smooth physical alternatives, using measured DESI DR2 data.

The curves generated here are fitted theoretical predictions, not new observations.
No joint CMB/SN likelihood or calibration simulation is performed.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.optimize import least_squares, minimize
from scipy.linalg import solve_triangular
from numpy.polynomial.legendre import leggauss
from scipy.stats import chi2

ROOT = Path(__file__).resolve().parent
raw = np.loadtxt(ROOT / 'data/desi_gaussian_bao_ALL_GCcomb_mean.txt', dtype=str)
z, data, kind = raw[:,0].astype(float), raw[:,1].astype(float), raw[:,2]
C = np.loadtxt(ROOT / 'data/desi_gaussian_bao_ALL_GCcomb_cov.txt')
L = np.linalg.cholesky(C)
zs = np.unique(z)
inds = np.searchsorted(zs,z)

def prediction(p, model='lcdm', order=128, radiation=0.0):
    """p uses dimensionless coefficients multiplied by 1000, except in CPL.

    Smooth model: 1000 B(z) = b0 + amp*z/(1+z).
    radiation is the coefficient 1000*Omega_r*(H0*rd/c)^2, not Omega_r.
    """
    x, w = leggauss(order)
    nodes = (x[None,:]+1)*zs[:,None]/2
    weights = w[None,:]*zs[:,None]/2
    def hsquared(t):
        if model == 'cpl':
            om, scale, w0, wa = p
            return (om*(1+t)**3 + (1-om)*(1+t)**(3*(1+w0+wa))*np.exp(-3*wa*t/(1+t)))/scale**2
        alpha, b0 = p[:2]
        amp = 0 if model == 'lcdm' else p[2]
        return (alpha*(1+t)**3 + radiation*(1+t)**4 + b0 + amp*t/(1+t))/1000
    dh = 1/np.sqrt(hsquared(zs))
    dm = np.sum(weights / np.sqrt(hsquared(nodes)),axis=1)
    dv = np.cbrt(zs*dm**2*dh)
    arrays = {'DH_over_rs':dh,'DM_over_rs':dm,'DV_over_rs':dv}
    return np.array([arrays[k][i] for k,i in zip(kind,inds)])

def residual(p,model='lcdm',order=128,radiation=0.):
    return solve_triangular(L, prediction(p,model,order,radiation)-data,lower=True)

def main():
    checks=[]
    for item in json.loads((ROOT/'sources/data_manifest.json').read_text()):
        b=(ROOT/item['path']).read_bytes()
        git=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        assert git == item['git_blob_sha1'], (git,item['git_blob_sha1'])
        assert hashlib.sha256(b).hexdigest() == item['sha256']
        checks.append({'file':item['path'],'git_sha1_ok':True,'sha256_ok':True})
    assert C.shape == (13,13) and np.allclose(C,C.T,rtol=0,atol=0)
    out={'hash_checks':checks,'covariance_eigenvalues':np.linalg.eigvalsh(C).tolist(),
         'scope':'DESI DR2 released compressed Gaussian BAO likelihood only. No SN or CMB joint analysis.'}
    for rad in [0.,.0001]:
        fit=least_squares(lambda p:residual(p,radiation=rad),[.34,.81],bounds=([1e-6,1e-6],[1.,10.]),
            xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=1000)
        alpha,b0=fit.x
        val=float(fit.fun@fit.fun)
        out['lcdm_rad_'+str(rad)]={'alpha':float(alpha),'b0':float(b0),'chi2':val,
            'nominal_11df_tail':float(chi2.sf(val,11)),
            'omega_m':float(alpha/(alpha+b0+rad)), 'c_over_H0_rd':float(np.sqrt(1000/(alpha+b0+rad))),
            '64_vs_128_max_prediction_difference':float(np.max(np.abs(prediction(fit.x,radiation=rad,order=64)-prediction(fit.x,radiation=rad,order=128)))),
            'prediction':prediction(fit.x,radiation=rad).tolist(), 'success':bool(fit.success)}
    smooth=[]
    objective=lambda p:float(residual(p,'smooth')@residual(p,'smooth'))
    for start in [[.34,.81,0.],[.30,.70,.5],[.32,.75,.25],[.25,.5,2.]]:
        fit=minimize(objective,start,method='SLSQP',bounds=[(1e-5,1.),(1e-5,10.),(0.,30.)],
            constraints=[{'type':'ineq','fun':lambda p:6*p[1]-p[2]}],
            options={'ftol':1e-11,'maxiter':1000})
        smooth.append({'parameters':fit.x.tolist(),'chi2':float(fit.fun),'success':bool(fit.success)})
    best=min(smooth,key=lambda r:r['chi2'])
    alpha,b0,amp=best['parameters']
    zz=np.linspace(0,2.33,1001)
    bb=b0+amp*zz/(1+zz)
    eos=-1+amp/(3*(1+zz)*bb)
    pot=3*bb-amp/(2*(1+zz))
    best['w_at_0']=float(-1+amp/(3*b0))
    best['w_at_2p33']=float(eos[-1])
    best['minimum_scaled_potential']=float(pot.min())
    best['prediction']=prediction(best['parameters'],'smooth').tolist()
    best['64_vs_128_max_prediction_difference']=float(np.max(np.abs(prediction(best['parameters'],'smooth',64)-prediction(best['parameters'],'smooth',128))))
    out['smooth_positive_potential_fit']=best
    out['smooth_multistart']=smooth
    cpl=[]
    for start in [[.30,30.,-1.,0.],[.38,33.,-.2,-2.7],[.22,30.,-1.,.5]]:
        fit=least_squares(lambda p:residual(p,'cpl'),start,
            bounds=([.01,15.,-3.,-10.],[.7,50.,1.,5.]),
            xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=3000)
        cpl.append({'parameters':fit.x.tolist(),'chi2':float(fit.fun@fit.fun),'success':bool(fit.success)})
    out['cpl_multistart']=cpl
    bestc=min(cpl,key=lambda r:r['chi2'])
    out['cpl_best']=bestc
    out['lcdm_minus_cpl_chi2']=out['lcdm_rad_0.0']['chi2']-bestc['chi2']
    out['cpl_64_vs_128_max_prediction_difference']=float(np.max(np.abs(prediction(bestc['parameters'],'cpl',64)-prediction(bestc['parameters'],'cpl',128))))
    (ROOT/'results/validation.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__ == '__main__':
    main()
