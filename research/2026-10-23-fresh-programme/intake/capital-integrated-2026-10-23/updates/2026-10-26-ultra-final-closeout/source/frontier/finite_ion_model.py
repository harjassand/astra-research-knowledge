#!/usr/bin/env python3
"""Finite extracellular mass/water extension of the reconstructed Dijkstra cell.

This is a new conditional model, not a reproduction of a finite-space experiment.
The original source fixes extracellular concentrations. Here closed Na,K,Cl and
water inventories determine them. A hypothetical Na/K exchanger has finite sites,
finite chemical-potential-driven exchange and explicitly specified hydration.
"""
from pathlib import Path
import json
import math
from types import SimpleNamespace
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import dijkstra_model as d

OUT=Path(__file__).resolve().parent
HEALTH=d.steady_guess([-65.,10.,145.,7.])
CHI=5.
THETA_LO=brentq(lambda x: math.log(x/(1-x))+CHI*(1-2*x),1e-8,.49)
THETA_HI=1-THETA_LO
RSTAR=3./152.


class ClosedBath:
    def __init__(self,allocation=.5,capacity=0.,site_density=5000.,
                 initial_theta=None,mode='phase',gamma=3.,hydration=0.,khalf=1.,inert_volume=0.,initial_cell=None):
        # pL, fmol, fmol/pL, dimensionless, fmol/s, waters/site, mM.
        self.capacity=capacity;self.site_density=site_density;self.mode=mode
        self.gamma=gamma;self.hydration=hydration;self.khalf=khalf;self.inert_volume=inert_volume
        self.cell0=HEALTH.copy() if initial_cell is None else np.asarray(initial_cell,dtype=float).copy()
        self.theta0=THETA_LO if initial_theta is None else initial_theta
        self.b0=capacity*self.theta0
        self.volume0=allocation-self.material_volume(self.b0)
        if self.volume0<=0: raise ValueError('Material exceeds allocated extracellular volume')
        self.total_water=self.cell0[7]/1000.+allocation
        self.total_na=self.cell0[4]+152*self.volume0+capacity-self.b0
        self.total_k=self.cell0[5]+3*self.volume0+self.b0
        self.total_cl=self.cell0[6]+135*self.volume0
        self.external_a=20*self.volume0
        # Independent sites share the selected initial occupancy at normal bath.
        self.g0=math.log(RSTAR)-math.log(self.theta0/(1-self.theta0))

    def material_volume(self,b):
        # 18 cm3/mol per bound hydration water =18e-6 pL/fmol.
        return self.inert_volume+self.capacity/self.site_density+18e-6*self.hydration*(self.capacity-b)

    def initial(self):return np.r_[self.cell0,self.b0,0.]

    def extracellular(self,y):
        b=y[8];ve=self.total_water-y[7]/1000.-self.material_volume(b)
        ne=np.array([self.total_na-y[4]-self.capacity+b,
                     self.total_k-y[5]-b,self.total_cl-y[6],self.external_a])
        return ve,ne/ve

    def material_mu(self,theta):
        z=min(1-1e-14,max(1e-14,theta))
        if self.mode=='phase':
            if THETA_LO<=z<=THETA_HI:return math.log(RSTAR)
            return math.log(z/(1-z))+CHI*(1-2*z)+math.log(RSTAR)
        if self.mode=='independent':return math.log(z/(1-z))+self.g0
        raise ValueError(self.mode)

    def rhs(self,t,y,pump=1.,nat=1.,external=None):
        v,m,h,n,nna,nk,ncl,w,b,atp=y
        ve,ce=self.extracellular(y) if external is None else external
        nae,ke,cle,ae=ce
        na,kk,cl=np.array([nna,nk,ncl])*1000/w
        if min(ve,w,nae,ke,cle,ae,na,kk,cl)<=0:
            raise ValueError('Nonpositive physical amount/concentration')
        aa,bb=d.gates(v)
        ina=d.ghk(d.PNAL+d.PNAT*nat*m**3*h,na,nae,1,v)
        ik=d.ghk(d.PKL+d.PKD*n*n,kk,ke,1,v)
        pcl=d.PCLL+d.PCLG/(1+d.ex(-(v+10)/10))
        icl=d.ghk(pcl,cl,cle,-1,v)
        # Added, explicitly uncalibrated external-K gate. Source has fixed Ke3.
        fk=ke/(ke+self.khalf)*(3+self.khalf)/3 if self.khalf else 1.
        ip=pump*d.QPUMP*(.62/(1+(6.7/na)**3)+.38/(1+(67.6/na)**3))*fk
        jk=d.UKCL*d.RTF*math.log(kk*cl/(ke*cle))
        di=np.array([-(ina+3*ip),-(ik-2*ip),icl])*1000/d.F-np.array([0,jk,jk])
        dv=-(ina+ik+icl+ip)/d.C*1000
        dg=aa*(1-np.array([m,h,n]))-bb*np.array([m,h,n])
        osmi=(nna+nk+ncl+d.NA_FIXED)*1000/w
        dw=d.LW*d.R*d.T*(osmi-ce.sum())/1e5
        # A Na-rich site binds `hydration` more waters than a K-rich site.
        # Its ideal dilute water-activity correction is calibrated at310mM.
        # No actual material hydration number or phase diagram is supplied.
        mu_water=18e-6*self.hydration*(310.-ce.sum())
        db=0. if not self.capacity else self.gamma*(math.log(ke/nae)-self.material_mu(b/self.capacity)-mu_water)
        return np.r_[dv,dg,di,dw,db,ip*1000/d.F]

    def integrate(self,y,seconds,pump=1.,nat=1.,rtol=2e-7,samples=501,method='LSODA'):
        controls=(lambda t:(pump,nat)) if not callable(pump) else pump
        def crossing(t,z):return z[0]
        crossing.direction=1;crossing.terminal=False
        sol=solve_ivp(lambda t,z:self.rhs(t,z,*controls(t)),(0.,seconds),y,
                      method=method,rtol=rtol,events=crossing,
                      atol=np.r_[1e-6,np.full(3,1e-9),np.full(3,1e-8),1e-5,1e-8,1e-8],
                      t_eval=np.linspace(0.,seconds,samples),max_step=5.)
        if not sol.success:raise RuntimeError(sol.message)
        return sol

    def describe(self,y):
        ve,ce=self.extracellular(y);z=d.describe(y[:8])
        z.update(extracellular_volume_pl=float(ve),na_e_mm=float(ce[0]),
                 k_e_mm=float(ce[1]),cl_e_mm=float(ce[2]),a_e_mm=float(ce[3]),
                 reservoir_k_fmol=float(y[8]),pump_atp_fmol=float(y[9]))
        return z


def protocol(model,injury_s=600.,repair_s=3600.,block_s=300.,rtol=2e-7):
    y=model.initial();inj=model.integrate(y,injury_s,pump=0.,rtol=rtol)
    y=inj.y[:,-1]
    if 0<block_s<repair_s:
        # Solve each side of an imposed discontinuity separately.
        s1=model.integrate(y,block_s,nat=0.,rtol=rtol,samples=int(block_s/2)+1)
        s2=model.integrate(s1.y[:,-1],repair_s-block_s,rtol=rtol,samples=int((repair_s-block_s)/2)+1)
        repair=SimpleNamespace(t=np.r_[s1.t,s2.t[1:]+block_s],
            y=np.c_[s1.y,s2.y[:,1:]],nfev=s1.nfev+s2.nfev,
            t_events=[np.r_[s1.t_events[0],s2.t_events[0]+block_s]])
    else:
        repair=model.integrate(y,repair_s,nat=0. if block_s>=repair_s else 1.,rtol=rtol,samples=1801)
    k=repair.y[5]*1000/repair.y[7];na=repair.y[4]*1000/repair.y[7]
    good=(repair.y[0]<-60)&(na<20)&(k>130)
    indices=np.flatnonzero(good)
    out=dict(parameters=dict(allocation_pl=model.total_water-HEALTH[7]/1000,
        capacity_fmol=model.capacity,mode=model.mode,site_density_mm=model.site_density,
        hydration_waters=model.hydration,gamma_fmol_s=model.gamma,khalf_mm=model.khalf,
        inert_volume_pl=model.inert_volume,
        injury_s=injury_s,repair_s=repair_s,block_s=block_s),
        injury=model.describe(inj.y[:,-1]),final=model.describe(repair.y[:,-1]),
        first_sampled_healthy_ionic_time_s=float(repair.t[indices[0]]) if len(indices) else None,
        maximum_injury_k_e_mm=max(model.extracellular(z)[1][1] for z in inj.y.T),
        injury_upward_zero_crossings=int(len(inj.t_events[0])),
        recovery_upward_zero_crossings=int(len(repair.t_events[0])),
        minimum_injury_extracellular_volume_pl=min(model.extracellular(z)[0] for z in inj.y.T),
        maximum_charge_error_mv=max(abs(d.describe(z[:8])['charge_identity_error_mv']) for z in np.c_[inj.y,repair.y].T),
        rhs_evaluations=inj.nfev+repair.nfev)
    return out,inj,repair


def main():
    doc=dict(status='conditional finite-inventory source extension; not a tissue or material result',
             source='10.1523/JNEUROSCI.1934-16.2016; extracellular-K pump gate added',
             chi=CHI,phase_endpoints=[THETA_LO,THETA_HI],cases=[])
    cases=[ClosedBath(),ClosedBath(capacity=240.),ClosedBath(capacity=240.,mode='independent'),
           ClosedBath(inert_volume=.048)]
    for i,model in enumerate(cases):
        row,inj,rep=protocol(model);doc['cases'].append(row)
        print(json.dumps(row),flush=True)
        np.savez_compressed(OUT/f'finite_ion_closed_case{i}.npz',injury_t=inj.t,injury_y=inj.y,
                            recovery_t=rep.t,recovery_y=rep.y)
        (OUT/'finite_ion_closed_results.json').write_text(json.dumps(doc,indent=2)+'\n')


if __name__=='__main__':main()
