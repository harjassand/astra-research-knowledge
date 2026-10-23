"""Independent Python transcription of Esposito/Armenise2017 SI forward rates.
No author executable is run. Literal printed seam and explicitly proposed index
correction are both retained. No reverse rates or nonequilibrium trajectory.
"""
from pathlib import Path
import re,json,hashlib,time,resource
import numpy as np
D=Path(__file__).resolve().parent;P=D.parent/'mode_evidence/jp7b04442_si_002.txt';text=P.read_text();START=time.monotonic()
FLOAT=r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][-+]?\d+)?'
def vector(name,length):
 out=np.full(length,np.nan,dtype=np.longdouble)
 for i,v in re.findall(r'(?im)^\s*'+re.escape(name)+r'\((\d+)\)\s*=\s*('+FLOAT+r')',text):
  if int(i)<length:out[int(i)]=np.longdouble(v.replace('D','E'))
 assert np.isfinite(out).all();return out
EN=vector('En2_onn_3Asec',60);EO=vector('Eno',48)
C={}
for side in ['g','l']:
 a=np.full((3,6,6),np.nan,dtype=np.longdouble)
 hits=re.findall(r'(?im)^\s*coeff_'+side+r'\((\d+),(\d+),(\d+)\)\s*=\s*('+FLOAT+r')',text)
 assert len(hits)==108,(side,len(hits))
 for i,j,k,v in hits:a[int(i),int(j),int(k)]=np.longdouble(v.replace('D','E'))
 assert np.isfinite(a).all();C[side]=a

def coeff(variant):
 bn=np.array([EN**j for j in range(5)]+[1/EN]);bo=np.array([EO**j for j in range(5)]+[1/EO]);aa={s:np.einsum('ijk,jv,kw->ivw',C[s],bn,bo) for s in C}
 out=np.where((EN[:,None]>=EO[None,:])[None],aa['g'],aa['l']);limits=[]
 for w,e in enumerate(EO):
  vi=np.flatnonzero(EN>=e);v=int(vi[0]) if len(vi) else 200;limits.append(v)
  if v==59:lo,hi,targets=56,59,[57,58]
  elif v==58:lo,hi,targets=55,59,[56,57,58]
  elif 3<=v<=57:lo,hi,targets=v-3,v+2,[v-2,v-1,v,v+1]
  elif v==2:lo,hi,targets=0,4,[1,2,3]
  elif v==1:lo,hi,targets=0,3,[1,2]
  else:continue
  a=(out[:,hi,w]-out[:,lo,w])/(EN[hi]-EN[lo]);b=out[:,lo,w]-a*EN[lo]
  if variant=='literal' and 3<=v<=57:
   out[:,v,w+1]=a*EN[v+1]+b
   targets=[v-2,v-1,v]
  for vv in targets:out[:,vv,w]=a*EN[vv]+b
 return out,limits

def rates(T,variant):
 if not 1000<=T<=20000:raise ValueError('Outside printed generated temperature domain')
 a,_=coeff(variant);k=np.exp(a[0]+a[1]/T+a[2]/T**2)/3
 assert np.isfinite(k).all() and (k>=0).all();return k
KB=np.longdouble('8.617333262145e-5');EVJ=np.longdouble('96485.33212331002')
def population(Tv):
 p=np.exp(-(EN-EN[0])/(KB*Tv));return p/p.sum()
def contraction(T,Tv,variant):
 k=rates(T,variant);p=population(Tv);f=p[:,None]*k;total=f.sum();pin=(f.sum(1)*(EN-EN[0])).sum()/total;pout=(f.sum(0)*(EO-EO[0])).sum()/total
 return {'Ttrans_rot_K':T,'Tv_N2_K':Tv,'variant':variant,'forward_k_cm3_s':float(total),'reaction_weighted_N2_excitation_eV':float(pin),'reaction_weighted_NO_excitation_eV':float(pout),'mode_excitation_change_J_mol_forward_event':float((pout-pin)*EVJ),'ground_state_endothermicity_eV':float(EO[0]-EN[0]),'reaction_weighted_bath_energy_demand_J_mol_forward_event':float((EO[0]-EN[0]+pout-pin)*EVJ),'population_fraction_v_ge_10':float(p[10:].sum()),'reaction_fraction_v_ge_10':float(f[10:].sum()/total),'max_single_state_k_cm3_s':float(k.max())}

def main():
 rows=[]
 for v in ['literal','corrected_index']:
  for T,Tv in [(1700,1700),(1700,1959.5075393144),(1700,2700),(2000,2000),(2000,2700),(2300,2300),(2300,2700),(2700,2700)]:
   r=contraction(T,Tv,v);r['enhancement_over_same_QCT_thermal_population']=r['forward_k_cm3_s']/contraction(T,T,v)['forward_k_cm3_s'];r['original_7reaction_thermal_k_cm3_s']=3e-10*np.exp(-38000/T);r['published_2020_corrected_thermal_fit_cm3_s']=1.2686e-13*T**.874*np.exp(-36899/T);r['defined_QCT_thermal_contraction_over_corrected_fit']=contraction(T,T,v)['forward_k_cm3_s']/r['published_2020_corrected_thermal_fit_cm3_s'];rows.append(r)
 out={'scope':__doc__,'sources':{P.name:hashlib.sha256(P.read_bytes()).hexdigest()},'level_population_contract':'p_v proportional to exp[-(E_v-E_0)/(kB Tv)], bound v0..59; no rotational-vibrational partition reweighting. Rates carry source rotational/translational averaging. This defined vibrational population is not a full equilibrium partition-function claim.','units':'source forward rate cm3/s per molecule pair; source energies eV relative separated atoms; weighted excitation energies converted using F J/mol/eV','rows':rows,'missing':['Reverse state-specific rates/statistical partition factors not supplied by this routine.','QCT potential/fit uncertainty is not a measured kinetic uncertainty interval.','NO2 and other chemistry omitted from this contraction.','Printed seam has a cross-index inconsistency; literal and proposed correction not conflated.','Generating a1000K grid does not itself verify interpolation accuracy at every point.'],'elapsed_s':time.monotonic()-START,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 (D/'forward_contraction.json').write_text(json.dumps(out,indent=2));np.savez_compressed(D/'source_arrays.npz',EN_eV=EN.astype(float),EO_eV=EO.astype(float),coeff_g=C['g'].astype(float),coeff_l=C['l'].astype(float));print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
