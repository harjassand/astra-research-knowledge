"""Exact-rational arithmetic for the conditional NASA7 endpoint ceiling.
Stored float coefficients are interpreted as exact binary rationals; this does not
make a thermochemical table an exact empirical description of real gas.
"""
import time
START=time.monotonic()
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,resource
import numpy as np
R=Path(__file__).resolve().parent;ROOT=R.parent;cache=ROOT/'nitrogen_finite_cycle_20261021/thermo_helper/cache.npz';c=np.load(cache);nasa=c['nasa'];W=c['molecular_weights'];ru=F(float(8314.46261815324))/1000
# Use exact source constant, not a guessed published rounding.
m=json.loads((ROOT/'nitrogen_finite_cycle_20261021/thermo_helper/manifest.json').read_text());ru=F(float(m['constants']['R_J_kmol_K']))/1000
hp=ROOT/'nitrogen_admissibility_20261022/recycle_quench/once_through_2700_reference.npz';cp=ROOT/'nitrogen_admissibility_20261022/recycle_quench/mix_tau_0p0001_trajectory.npz'
rawh=np.load(hp)['hot_Y'];rawc=np.load(cp)['return_Y']
def normalized(a):
 b=[F(float(max(x,0))) for x in a];s=sum(b);return [x/s for x in b]
yh=normalized(rawh);yc=normalized(rawc);ww=[F(float(x))/1000 for x in W];r=F(17,20)
def energy(T,internal):
 out=[]
 for row in nasa:
  a=[F(float(x)) for x in (row[8:15] if T<=1000 else row[1:8])];h=ru*(sum(a[i]*F(T)**(i+1)/F(i+1) for i in range(5))+a[5]);out.append(h-ru*T if internal else h)
 return out
n=[(yh[i]+r*yc[i])/ww[i] for i in range(6)];AN=2*n[0]+n[2]+n[4]+n[5];AO=2*n[1]+n[3]+n[4]+2*n[5];x0=n[4]+n[5]
rows=[]
for internal in [False,True]:
 hi=energy(2700,internal);hc=energy(300,internal);ei=energy(1700,internal);target=sum(yh[i]/ww[i]*hi[i]+r*yc[i]/ww[i]*hc[i] for i in range(6));base=AN*ei[0]/2+AO*ei[1]/2;a=ei[4]-ei[0]/2-ei[1]/2;b=ei[5]-ei[4]-ei[1]/2;cn=ei[2]-ei[0]/2;co=ei[3]-ei[1]/2
 assert a>0 and b<0 and cn>0 and co>0
 for factor,ncap,ocap in [(F(1),F(0),F(0)),(F(1),F(1,10**7),F(3,1000)),(F(101,100),F(1,10**7),F(3,1000))]:
  x=factor*x0;assert AN-x-ncap>=0 and AO-x-ocap>=0
  ceiling=base+a*x+cn*ncap+co*ocap;loss=target-ceiling;assert loss>0
  rows.append({'contract':'internal_energy_rigid' if internal else 'enthalpy_isobaric','NOx_cap_factor':str(factor),'N_radical_cap_mol_per_kg_fresh':str(ncap),'O_radical_cap_mol_per_kg_fresh':str(ocap),'exact_heat_export_lower_bound_J_kg_fresh':str(loss),'float_for_display_J_kg_fresh':float(loss),'exact_coefficient_signs_pass':True})
out={'scope':__doc__,'rows':rows,'input_projection':'Exact rational normalization of nonnegative source mass fractions; explicitly remove only stored negative roundoff in cold return. Not physical measurement correction.','input_sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [cache,hp,cp]},'theorem':'At T<=1700 and positive species heat capacity, E<=Ebase+a*x+b*z+cN*nN+cO*nO. Given b<0,a,cN,cO>0 and feasible independent caps, the maximum occurs at xcap,z=0,radicalcaps. The exact positive difference from initial energy must leave the specified system. Additional NOx beyond cap, other species, different mechanical boundaries or external work change the theorem.','cost_total_s':time.monotonic()-START,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(R/'exact_endpoint_certificate.json').write_text(json.dumps(out,indent=2));print(json.dumps([{k:v for k,v in x.items() if not k.startswith('exact_heat')} for x in rows]))
