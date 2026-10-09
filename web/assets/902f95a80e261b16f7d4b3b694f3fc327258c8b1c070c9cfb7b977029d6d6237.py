#!/usr/bin/env python3
"""Independent CP--KMS family diagnostic, not a theorem certificate."""
from pathlib import Path
import json
import numpy as np
import mpmath as mp

HERE=Path(__file__).resolve().parent


def coefficients(p, r, theta):
    z0=2*p-1
    u,v=np.sqrt(p),np.sqrt(1-p)
    R=1/(u*v)
    ell=.5*np.log(p/(1-p))
    x,z=r*np.sin(theta),r*np.cos(theta)
    q=np.sqrt(1-r*r)
    D=np.arctanh(r)
    E0=R/2-q-(1-q)*x*x/(r*r)-z0*R*z/2
    E1=2*(u-v)/(u+v)*x-2*(1-q)*x*z/(r*r)
    E2=(1-q)*x*x/(r*r)
    J0=.5*(R-2)*D*x*x/r+R*(z-z0)*(D*z/r-ell)
    J1=-2*R/np.sqrt(R+2)*(z-z0)*D*x/r-4/np.sqrt(R+2)*x*(D*z/r-ell)
    J2=2*D*x*x/r
    return (J0,J1,J2),(E0,E1,E2)


def high_precision(p_text,r_text,theta_text):
    mp.mp.dps=90
    p,r,t=map(mp.mpf,[p_text,r_text,theta_text])
    z0=2*p-1
    u,v=mp.sqrt(p),mp.sqrt(1-p)
    R=1/(u*v)
    ell=mp.log(p/(1-p))/2
    x,z=r*mp.sin(t),r*mp.cos(t)
    q=mp.sqrt(1-r*r)
    D=mp.atanh(r)
    E0=R/2-q-(1-q)*x*x/(r*r)-z0*R*z/2
    E1=2*(u-v)/(u+v)*x-2*(1-q)*x*z/(r*r)
    E2=(1-q)*x*x/(r*r)
    J0=(R-2)*D*x*x/(2*r)+R*(z-z0)*(D*z/r-ell)
    J1=-2*R/mp.sqrt(R+2)*(z-z0)*D*x/r-4/mp.sqrt(R+2)*x*(D*z/r-ell)
    J2=2*D*x*x/r
    f0,f1,f2=J0-2*E0,J1-2*E1,J2-2*E2
    a=-f1/(2*f2)
    J=J0+a*J1+a*a*J2
    E=E0+a*E1+a*a*E2
    return {"p":str(p),"r":str(r),"theta":str(t),"a":str(a),
            "J":str(J),"E":str(E),"J_over_E":str(J/E),"J_minus_2E":str(J-2*E)}


def main():
    theta=np.unique(np.r_[np.linspace(.001,np.pi-.001,721),np.geomspace(1e-6,.1,60)])
    ps=[.51,.6,.75,.9,.95,.99]+[1-10.**(-k) for k in range(3,13)]
    radii=np.unique(np.r_[np.linspace(.001,.999,120),1-np.geomspace(1e-12,.1,45)])
    records=[]
    total=0
    for p in ps:
        extra=[2*p-1]+[min(.999999999999,max(1e-6,2*p-1+sgn*10.**(-k)))
                       for k in range(2,10) for sgn in [-1,1]]
        for r in np.unique(np.r_[radii,extra]):
            js,es=coefficients(p,r,theta)
            f0,f1,f2=[js[i]-2*es[i] for i in range(3)]
            a=-f1/(2*f2)
            J=js[0]+a*js[1]+a*a*js[2]
            E=es[0]+a*es[1]+a*a*es[2]
            good=(E>1e-10*(1+a*a+1/np.sqrt(p*(1-p)))) & (J>=0)
            ratio=np.where(good,J/E,np.inf)
            idx=int(np.argmin(ratio))
            if np.isfinite(ratio[idx]):
                records.append({"ratio_float":float(ratio[idx]),"p":str(p),"r":str(r),
                                "theta":str(theta[idx]),"a_float":float(a[idx])})
            total+=len(theta)
    records.sort(key=lambda x:x['ratio_float'])
    high=[high_precision(rec['p'],rec['r'],rec['theta']) for rec in records[:8]]
    report={"status":"NUMERICAL_DIAGNOSTIC_ONLY","no_sibling_cycle06_read":True,
            "family":"Hermitian B=[[a,1],[1,-a]], Lyapunov drift at diagonal sigma",
            "grid_states":total,"float_best":records[:8],"high_precision_best":high,
            "universal_inequality_status":"UNRESOLVED"}
    (HERE/'qubit_search.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({"grid_states":total,"best":high[0]},indent=2))


if __name__=='__main__':
    main()
