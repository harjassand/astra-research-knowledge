#!/usr/bin/env python3
"""Exact passive-K/Cl stationary reduction of the finite-bath Na-pump model.

This exposes a load/current interface and static folds. It is not a claim that
the static curve alone certifies the full seven-dimensional recovery basin.
"""
import json,math
import numpy as np
from scipy.optimize import brentq,root
import finite_ion_model as f
import light_ion_return_model as m
import dijkstra_model as d


class Curve:
    def __init__(self,nat=1.,drive=30000.):
        self.cell=m.LightCell(current_max_pa=1.,drive_j_mol=drive)
        self.bath=self.cell.bath;self.nat=nat
        b=self.bath
        self.osm=(b.total_na+b.total_k+b.total_cl+d.NA_FIXED+b.external_a)/b.total_water

    def state(self,v):
        b=self.bath;r=math.exp(-v*.001/d.RTF);q=d.C*v/d.F
        def amounts(w):
            ve=b.total_water-w
            nk=b.total_k*r*w/(r*w+ve)
            nc=b.total_cl*w/(w+r*ve)
            nn=d.NA_FIXED-nk+nc+q
            return np.array([nn,nk,nc])
        def osmres(w):return (amounts(w).sum()+d.NA_FIXED)/w-self.osm
        w=brentq(osmres,1e-5,b.total_water-1e-8,xtol=1e-13)
        aa,bb=d.gates(v)
        return np.r_[v,aa/(aa+bb),amounts(w),w*1000,0.,0.,0.,0.,0.]

    def current(self,v):
        y=self.state(v);ve,ce=self.bath.extracellular(y)
        na=y[4]*1000/y[7];mm,hh,nn=y[1:4]
        ina=d.ghk(d.PNAL+d.PNAT*self.nat*mm**3*hh,na,ce[0],1,v)
        unit=self.cell.pump(y,1.)[0]
        return -ina/unit if unit>1e-12 else float('nan')

    def row(self,v):
        y=self.state(v);row=self.cell.describe(y);current=self.current(v)
        self.cell.current_max=current
        residual=self.cell.rhs(0,y,nat=self.nat)[:8]
        self.cell.current_max=1.
        row.update(required_current_max_pa=current,
             maximum_cell_stationary_rhs_residual=float(abs(residual).max()))
        return row


def ordinary_roots():
    b=f.ClosedBath();S=(b.total_na+b.total_k+b.total_cl+d.NA_FIXED+b.external_a)/b.total_water
    def yy(x):
        v,na,kk,cl=x
        denom=S-na-kk-cl
        if denom<=0:return None
        w=d.NA_FIXED/denom
        if not 0<w<b.total_water:return None
        aa,bb=d.gates(v)
        y=np.r_[v,aa/(aa+bb),np.array([na,kk,cl])*w,w*1000.,0.,0.]
        ve,ce=b.extracellular(y)
        if min(na,kk,cl,*ce)<=0:return None
        return y
    def fun(x):
        y=yy(x)
        if y is None:return np.full(4,1e4)+np.minimum(x,0).sum()
        z=b.rhs(0,y)
        return np.r_[z[4:7],(x[0]-d.F/d.C*(y[4]+y[5]-y[6]-d.NA_FIXED))/100.]
    roots=[]
    for v in [-70,-60,-55,-50,-45,-40,-35,-30,-25,-15]:
      for na in [10.,15.,20.,25.,30.,35.]:
        sol=root(fun,[v,na,155-na,7+(na-10)*.85],tol=1e-10)
        y=yy(sol.x)
        if y is not None and abs(fun(sol.x)).max()<1e-7 and not any(abs(y-z).max()<1e-3 for z in roots):roots.append(y)
    roots.sort(key=lambda y:y[0])
    return [b.describe(y) for y in roots]


def main():
    doc=dict(status='conditional exact passive K/Cl stationary reduction; folds not full basin proof',curves=[],
      ordinary_restored_pump_roots=ordinary_roots())
    for nat in [1.,.1,0.]:
        c=Curve(nat);vs=np.linspace(-200.,-.05,1001)
        currents=np.array([c.current(v) for v in vs])
        def derivative(v):return (c.current(v+.001)-c.current(v-.001))/.002
        dd=np.array([derivative(v) for v in vs])
        folds=[]
        for i in range(len(vs)-1):
            if np.isfinite(dd[i]*dd[i+1]) and dd[i]*dd[i+1]<0:
                vf=brentq(derivative,vs[i],vs[i+1],xtol=1e-9)
                folds.append(c.row(vf))
        rows=[c.row(v) for v in [-150.,-120.,-100.,-90.,-80.,-70.,-60.,-50.,-40.,-30.,-10.]]
        doc['curves'].append(dict(nat_fraction=nat,static_folds=folds,selected_states=rows))
        np.savez_compressed(m.OUT/f'light_stationary_nat{nat:g}.npz',voltage_mv=vs,current_max_pa=currents)
    (m.OUT/'light_ion_stationary_results.json').write_text(json.dumps(doc,indent=2)+'\n')
    print(json.dumps(doc,indent=2),flush=True)


if __name__=='__main__':main()
