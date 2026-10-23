"""Independent optical gates isolated from the FE high electrode on each face.
Per one-bank area SI, mu in eV==volts for electrochemical reference fixed0.
Stack FE metal |100nmAl2O3|10nm isolated back metal|45nmSiC|graphene|25nmgap.
Optical PEC backing and quoted photon ports remain an optimistic inherited
model: a real10nm optical metal must be checked before claiming same ports.
"""
from pathlib import Path
import sys
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent)) # portable package contains graphene_gate
sys.path.insert(0,str(ROOT.parents[1]/'radiation_valve15/circuit'))
import graphene_gate as g
CG=g.neutral_SiC_Cgeo(45e-9);CGAP=g.EPS0/25e-9
CI=g.EPS0*9/100e-9;PHIR=(.1695+.6)/2
MUL=.1695;MUH=.6;CMASS=2*(100e-9*3e6+10e-9*2.5e6)

def face(mu,T,Vfe=0.):
 d=g.dirac(mu,T);en=g.E_CHARGE*d['n'];enT=g.E_CHARGE*d['n_T'];Cq=g.E_CHARGE**2*d['n_mu']
 vg=(en+(CG+CGAP)*mu-CGAP*PHIR)/CG
 vgT=enT/CG;vgmu=1+(Cq+CGAP)/CG
 qopt=en+CGAP*(mu-PHIR);qiso=CI*(vg-Vfe)
 alpha=enT*CG/(Cq+CG+CGAP)
 ceff=CG*(Cq+CGAP)/(Cq+CG+CGAP)
 cvv=d['Cv_at_mu']-T*enT*enT/(Cq+CG+CGAP)
 G=d['Omega']-.5*CG*(vg-mu)**2-.5*CGAP*(mu-PHIR)**2-.5*CI*(Vfe-vg)**2
 return dict(mu=mu,T=T,Vg=vg,Vg_T=vgT,Vg_mu=vgmu,Qg=qopt+qiso,
  Qg_opt=qopt,Qg_iso=qiso,Qfe_iso=-qiso,Cq=Cq,enT=enT,CVmu=d['Cv_at_mu'],
  alpha_g=alpha,Cgate=ceff,CVgate=cvv,entropy=d['entropy'],G=G,
  Eiso=.5*CI*(Vfe-vg)**2,Egeo=.5*CG*(vg-mu)**2,
  ESiC_V_m=(vg-mu)/45e-9,Eiso_V_m=(Vfe-vg)/100e-9)

def face_flow(mu,T,Vfe,Tdot,Vfedot,mudot):
 z=face(mu,T,Vfe)
 Ig=(z['enT']+CI*z['Vg_T'])*Tdot-CI*Vfedot+(z['Cq']+CGAP+CI*z['Vg_mu'])*mudot
 Ife_iso=CI*(Vfedot-z['Vg_T']*Tdot-z['Vg_mu']*mudot)
 Ir=CGAP*(-mudot)
 return dict(**z,Ig=Ig,Ife_iso=Ife_iso,Ireservoir=Ir,gate_power=z['Vg']*Ig,
  FE_cross_power=Vfe*Ife_iso,reservoir_power=PHIR*Ir,
  thermal_mu_power=T*z['enT']*mudot)

def coupled_derivatives(T,V,mu,mudot,current_FE,heat,FEprops):
 """Use FEprops(CV,C,alpha), already including specified passive stack mass.
 Returns heat/current derivative solution and actual two optical gate flows.
 Optical gates held at prescribedmu by finite external circuit, whose power
 must be accumulated; this is not a free independent clock.
 """
 z=[face(m,T,V) for m in mu]
 A=FEprops['CV']+sum(r['CVmu'] for r in z)
 B=T*FEprops['alpha']
 C=FEprops['alpha']-CI*sum(r['Vg_T'] for r in z)
 D=FEprops['C']+len(mu)*CI
 h=heat-T*sum(r['enT']*md for r,md in zip(z,mudot))
 i=current_FE+CI*sum(r['Vg_mu']*md for r,md in zip(z,mudot))
 det=A*D-B*C
 Td=(D*h-B*i)/det;Vd=(-C*h+A*i)/det
 flows=[face_flow(m,T,V,Td,Vd,md) for m,md in zip(mu,mudot)]
 return Td,Vd,flows

if __name__=='__main__':
 import json
 print(json.dumps(dict(scope=__doc__,CG=CG,CGAP=CGAP,CI=CI,extra_C_J_m2K=CMASS,
  states=[face(m,343.,v) for m in [MUL,MUH] for v in [.1,23.]]),indent=2))
