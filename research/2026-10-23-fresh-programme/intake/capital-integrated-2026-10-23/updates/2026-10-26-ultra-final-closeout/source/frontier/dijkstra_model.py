#!/usr/bin/env python3
"""Independent reconstruction of Dijkstra et al. J Neurosci 2016 Eqs 1-12.

Primary source: 10.1523/JNEUROSCI.1934-16.2016, visually inspected pp 11882-4.
Not the authors' implementation; all reconstruction checks are explicit.

For an existing read-only SciPy installation, run with:
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=work/next_unit/flavor_finite_certificate/solver_deps python3 ...
"""
from pathlib import Path
import json
import math
import numpy as np
from scipy.optimize import root
from scipy.integrate import solve_ivp

F,R,T,C=96485.333,8.3144598,310.0,20.0  # C/mol, J/(mol K), K, pF
RTF=R*T/F
NA_FIXED=296.0  # fmol, source Table 1
PNAT,PNAL,PKD,PKL,PCLG,PCLL=800.0,2.0,400.0,20.0,19.5,2.5 # um^3/s
QPUMP,UKCL,LW=54.5,1.3,2.0  # pA, fmol/(s V), um^3/(s bar)
OUT=Path(__file__).resolve().parent


def ex(x):
    return math.exp(max(-700.,min(700.,float(x))))


def exprel(x):
    # x/(exp(x)-1), including its removable singularity.
    if abs(x)<1e-5:
        return 1-x/2+x*x/12-x**4/720
    if x>50:return x*ex(-x)
    if x<-50:return -x
    return x/math.expm1(x)


def gates(v):
    # Source Table 2 uses mV and kHz; rates here are per second.
    am=1000*.32*4*exprel(-(v+52)/4)
    bm=1000*.28*5*exprel((v+25)/5)
    ah=1000*.128*ex(-(v+53)/18)
    bh=1000*4/(1+ex(-(v+30)/5))
    an=1000*.016*5*exprel(-(v+35)/5)
    bn=1000*.25*ex(-(v+50)/40)
    a=np.array([am,ah,an]);b=np.array([bm,bh,bn])
    return a,b


def ghk(p,ci,ce,z,v):
    # p um^3/s, ci/ce mM == mol/m^3; v mV. Output pA.
    u=z*v*.001/RTF
    # z^2 F^2 V/RT * (ci-ce exp(-u))/(1-exp(-u))
    # = z F [ci*u/(1-exp(-u))-ce*u/(exp(u)-1)].
    return p*1e-6*z*F*(ci*exprel(-u)-ce*exprel(u))


def currents(v,na,kk,cl,mhn,pump=1.,nat=1.,delta=0.):
    nae,ke,cle=152.-delta,3.,135.-delta
    if min(na,kk,cl,nae,cle)<=0:raise ValueError('Nonpositive ion concentration')
    m,h,n=mhn
    ina=ghk(PNAL+PNAT*nat*m**3*h,na,nae,1,v)
    ik=ghk(PKL+PKD*n**2,kk,ke,1,v)
    pcl=PCLL+PCLG/(1+ex(-(v+10)/10))
    icl=ghk(pcl,cl,cle,-1,v)
    ip=pump*QPUMP*(.62/(1+(6.7/na)**3)+.38/(1+(67.6/na)**3))
    jk=UKCL*RTF*math.log(kk*cl/(ke*cle))
    return ina,ik,icl,ip,jk


def steady_guess(guess,pump=1.,nat=1.,osm=0.,delta=0.):
    def residual(x):
        v,na,kk,cl=x
        if min(na,kk,cl)<=0:return np.ones(4)*1e5+np.minimum(x,0).sum()
        a,b=gates(v);ina,ik,icl,ip,jk=currents(v,na,kk,cl,a/(a+b),pump,nat,delta)
        denom=310+osm-na-kk-cl
        # W can be eliminated by osmotic balance; then retain exact charge.
        if denom<=0:return np.ones(4)*1e5+abs(denom)
        w=NA_FIXED*1000/denom
        charge=(na+kk-cl)-NA_FIXED*1000/w-C*v*1000/(F*w)
        return [(ina+3*ip)/100,(ik-2*ip+F*jk/1000)/100,
                (icl-F*jk/1000)/100,charge/100]
    sol=root(residual,guess,tol=1e-11)
    if not sol.success or np.max(np.abs(residual(sol.x)))>1e-8:
        return None
    v,na,kk,cl=sol.x;w=NA_FIXED*1000/(310+osm-na-kk-cl)
    a,b=gates(v)
    yy=np.array([v,*list(a/(a+b)),na*w/1000,kk*w/1000,cl*w/1000,w])
    return yy


def rhs(t,y,controls):
    v,m,h,n,nna,nk,ncl,w=y
    pump,nat,osm,delta=controls(t)
    na,kk,cl=np.array([nna,nk,ncl])*1000/w
    a,b=gates(v)
    ina,ik,icl,ip,jk=currents(v,na,kk,cl,[m,h,n],pump,nat,delta)
    dions=np.array([-(ina+3*ip),-(ik-2*ip),icl])*1000/F-np.array([0,jk,jk])
    dv=-(ina+ik+icl+ip)/C*1000
    dg=a*(1-np.array([m,h,n]))-b*np.array([m,h,n])
    osm_i=(nna+nk+ncl+NA_FIXED)*1000/w
    dw=LW*(R*T*(osm_i-310-osm)/1e5)
    return np.array([dv,*list(dg),*list(dions),dw])


def describe(y):
    v,m,h,n,nna,nk,ncl,w=y
    charge_v=F/C*(nna+nk-ncl-NA_FIXED)
    return dict(voltage_mv=float(v),na_mm=float(nna*1000/w),k_mm=float(nk*1000/w),
                cl_mm=float(ncl*1000/w),volume_um3=float(w),
                charge_identity_error_mv=float(v-charge_v))


def integrate(y,seconds,control=(1.,1.,0.,0.),rtol=1e-8,method='BDF',samples=401):
    controls=control if callable(control) else lambda t:control
    result=solve_ivp(lambda t,x:rhs(t,x,controls),(0,seconds),y,method=method,
                     rtol=rtol,atol=np.array([1e-7,1e-9,1e-9,1e-9,1e-9,1e-9,1e-9,1e-6]),
                     t_eval=np.linspace(0,seconds,samples),max_step=10.)
    if not result.success:raise RuntimeError(result.message)
    return result


def jacobian(y,control=(1.,1.,0.,0.)):
    a=np.empty((8,8))
    for j in range(8):
        h=max(abs(y[j])*1e-6,1e-7);xp=y.copy();xm=y.copy();xp[j]+=h;xm[j]-=h
        a[:,j]=(rhs(0,xp,lambda t:control)-rhs(0,xm,lambda t:control))/(2*h)
    # Charge is an exact invariant; one zero eigenvalue is a redundant-state
    # direction. Stability must be assessed on the fixed-charge manifold.
    return a


def main():
    roots=[]
    for guess in [[-65,10,145,7],[-35,60,95,26],[-45,30,125,15],[-25,80,75,40],[-10,130,25,80]]:
        yy=steady_guess(guess)
        if yy is not None and not any(np.linalg.norm(yy-z)<.1 for z in roots):roots.append(yy)
    roots.sort(key=lambda y:y[0])
    data=[]
    for yy in roots:
        j=jacobian(yy);ee=np.linalg.eigvals(j);ee=ee[np.argsort(ee.real)]
        dd=describe(yy);dd.update(state=yy.tolist(),rhs_max=float(np.max(np.abs(rhs(0,yy,lambda t:(1,1,0,0))))),
                                eigenvalues_real=ee.real.tolist(),eigenvalues_imag=ee.imag.tolist())
        data.append(dd)
    doc=dict(status='independent reconstruction; primary single-neuron infinite-bath model, not physical validation',
             source='10.1523/JNEUROSCI.1934-16.2016',source_equations='1-12; Tables 1 and 2',roots=data,
             units='seconds, mV, fmol, um^3; currents pA; extracellular concentrations mM',
             notes=['Voltage ODE is equivalent to source charge algebra on a fixed-charge manifold',
                    'No parameter fitting to new experiments; finite interstitial delivery is not modeled'])
    (OUT/'dijkstra_reconstruction.json').write_text(json.dumps(doc,indent=2)+'\n')
    print(json.dumps(doc,indent=2))


if __name__=='__main__':main()
