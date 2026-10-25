#!/usr/bin/env python3
"""Conditional membrane-local Na pump; not a fitted KR2 or recovery model.

Finite closed bath, original shared charge/ion/water coordinates. The extra
photopump has an explicit bounded uncalibrated rate/affinity law and counted
productive-photon lower bound. No ATP supply is silently restored during light.
"""
from pathlib import Path
import json,math
import numpy as np
from scipy.integrate import solve_ivp
import dijkstra_model as d
import finite_ion_model as f

OUT=Path(__file__).resolve().parent
N_AV=6.02214076e23
H_PLANCK=6.62607015e-34
C_LIGHT=299792458.
WAVELENGTH=525e-9
PHOTON_MOLAR=H_PLANCK*C_LIGHT/WAVELENGTH*N_AV


class LightCell:
    def __init__(self,current_max_pa=100.,km_na_mm=5.,drive_j_mol=30000.,
                 initial_cell=None,allocation=.5):
        self.bath=f.ClosedBath(allocation=allocation,initial_cell=initial_cell)
        self.current_max=current_max_pa;self.km=km_na_mm;self.drive=drive_j_mol
        if not 0<drive_j_mol<=PHOTON_MOLAR:raise ValueError('Drive exceeds supplied photon energy')

    def pump(self,y,light):
        ve,ce=self.bath.extracellular(y)
        na=y[4]*1000/y[7]
        cost=d.R*d.T*math.log(ce[0]/na)-d.F*y[0]*.001
        affinity=self.drive-cost
        # An explicitly added constitutive law. Positive-affinity turnover is
        # bounded by current_max and falls to zero at stall. This is not fitted
        # to a recorded KR2 I-V curve; the rate is not its transient peak.
        factor=-math.expm1(-max(0.,affinity)/(d.R*d.T))
        current=light*self.current_max*na/(self.km+na)*factor
        return current,cost,affinity

    def rhs(self,t,y,light=1.,metabolism=0.,nat=1.):
        dy=self.bath.rhs(t,y[:10],pump=metabolism,nat=nat)
        ip,cost,affinity=self.pump(y,light)
        j=ip*1000/d.F # fmol/s outward Na
        dy[0]-=ip/d.C*1000
        dy[4]-=j
        # n_export, delivered ion work, minimum productive photon energy.
        return np.r_[dy,j,j*1e-15*cost,j*1e-15*PHOTON_MOLAR]

    def integrate(self,y,seconds,light=1.,metabolism=0.,nat=1.,rtol=2e-7,samples=601):
        sol=solve_ivp(lambda t,z:self.rhs(t,z,light,metabolism,nat),(0.,seconds),y,
          method='BDF',rtol=rtol,
          atol=np.r_[1e-6,np.full(3,1e-9),np.full(3,1e-8),1e-5,1e-8,1e-8,1e-8,1e-18,1e-18],
          t_eval=np.linspace(0.,seconds,samples),max_step=5.)
        if not sol.success:raise RuntimeError(sol.message)
        return sol

    def describe(self,y):
        row=self.bath.describe(y[:10]);ip,cost,affinity=self.pump(y,1.)
        ve,ce=self.bath.extracellular(y)
        row.update(fully_lit_model_photocurrent_pa=ip,na_export_work_j_mol=cost,
          remaining_pump_affinity_j_mol=affinity,pump_na_export_fmol=y[10],
          pump_useful_ion_work_j=y[11],minimum_productive_photon_energy_j=y[12],
          k_reversal_mv=d.RTF*1000*math.log(ce[1]/row['k_mm']),
          cl_reversal_mv=-d.RTF*1000*math.log(ce[2]/row['cl_mm']))
        return {k:float(v) for k,v in row.items()}


def good_time(sol):
    na=sol.y[4]*1000/sol.y[7];kk=sol.y[5]*1000/sol.y[7]
    ii=np.flatnonzero((sol.y[0]<-60)&(na<20)&(kk>130))
    return float(sol.t[ii[0]]) if len(ii) else None


def healthy_final(y):
    # A retained source-model classifier; physiological viability is not implied.
    return bool(y[0]<-60 and y[4]*1000/y[7]<20 and y[5]*1000/y[7]>130)


def run_case(initial,current,drive=30000.,light_s=1200.,nat=1.,metabolism=0.,tag=None):
    cell=LightCell(current_max_pa=current,drive_j_mol=drive)
    y=np.r_[initial,np.zeros(3)]
    lit=cell.integrate(y,light_s,metabolism=metabolism,nat=nat)
    # All cases are handed to identical restored ordinary pumps afterwards.
    handoff=cell.integrate(lit.y[:,-1],1800.,light=0.,metabolism=1.)
    yy=np.c_[lit.y,handoff.y]
    maxcharge=max(abs(d.describe(z[:8])['charge_identity_error_mv']) for z in yy.T)
    row=dict(current_max_pa=current,drive_j_mol=drive,light_s=light_s,
      metabolism_during_light=metabolism,nat_during_light=nat,
      initial=cell.describe(y),light_final=cell.describe(lit.y[:,-1]),
      handoff_final=cell.describe(handoff.y[:,-1]),
      first_sampled_ionic_return_in_light_s=good_time(lit),
      first_sampled_ionic_return_after_handoff_s=good_time(handoff),
      light_final_passes_provisional_ionic_thresholds=healthy_final(lit.y[:,-1]),
      handoff_final_passes_provisional_ionic_thresholds=healthy_final(handoff.y[:,-1]),
      minimum_voltage_in_light_mv=float(lit.y[0].min()),
      minimum_free_external_k_in_light_mm=min(cell.bath.extracellular(z)[1][1] for z in lit.y.T),
      minimum_stall_affinity_in_light_j_mol=min(cell.pump(z,1.)[2] for z in lit.y.T),
      maximum_charge_identity_error_mv=maxcharge,
      rhs_evaluations=lit.nfev+handoff.nfev)
    if tag:
        np.savez_compressed(OUT/('light_ion_'+tag+'.npz'),light_t=lit.t,light_y=lit.y,
              handoff_t=handoff.t,handoff_y=handoff.y)
    return row


def main():
    # Source closed-bath injury, without material or extra free ion inventory.
    model=f.ClosedBath()
    injury=model.integrate(model.initial(),600.,pump=0.)
    initial=injury.y[:,-1]
    doc=dict(status='conditional pure-Na photopump law; no fitted actuator/biology result',
      photon_wavelength_m=WAVELENGTH,photon_energy_j_mol=PHOTON_MOLAR,
      initial_closed_bath_injury_s=600.,cases=[],
      assumptions=['preexpressed pure sodium pump; actual KR2 low-Na proton coupling not modeled',
        'bounded added flux law and20/30/50kJ/mol stall resource are uncalibrated',
        'productive photon energy is a lower bound, excluding futile cycles/illumination losses',
        'same finite closed water and ion inventory; no new K source or ionic feed',
        'ordinary NaK pumps off during light except explicit comparator; restored at handoff',
        'no calcium, pH, death, axons, diffusion, irradiation heating or excitability test'])
    specs=[(0.,30000.,1200.,1.,0.,'dark'),(20.,30000.,1200.,1.,0.,'20pa'),
      (50.,30000.,1200.,1.,0.,'50pa'),(100.,30000.,1200.,1.,0.,'100pa'),
      (150.,30000.,1200.,1.,0.,'150pa'),(200.,30000.,1200.,1.,0.,'200pa'),
      (100.,20000.,1200.,1.,0.,'100pa20kj'),(100.,50000.,1200.,1.,0.,'100pa50kj'),
      (0.,30000.,300.,0.,1.,'ordinary_block')]
    for current,drive,seconds,nat,metab,tag in specs:
        row=run_case(initial,current,drive,seconds,nat,metab,tag)
        doc['cases'].append(row)
        (OUT/'light_ion_return_results.json').write_text(json.dumps(doc,indent=2)+'\n')
        print(json.dumps(row),flush=True)


if __name__=='__main__':main()
