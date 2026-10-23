"""Build a separately pinned continuous h/s NASA variant; never edit source cache."""
from pathlib import Path
import hashlib,json,time
import numpy as np
R=Path(__file__).resolve().parent;S=R.parents[1]/'nitrogen_regenerator_20261021/vector_kernel'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 t=time.perf_counter();original=sha(S/'cache.npz');m=json.loads((S/'manifest.json').read_text());assert original==m['cache_sha256']
 with np.load(S/'cache.npz',allow_pickle=False) as z:d={k:z[k].copy() for k in z.files}
 old=d['nasa'].copy();a=d['nasa'];corrections=[]
 for i,name in enumerate(m['species']):
  T=a[i,0];hi=a[i,1:8];lo=a[i,8:15]
  def hs(c):
   return (sum(c[j]*T**j/(j+1) for j in range(5))+c[5]/T,c[0]*np.log(T)+sum(c[j]*T**j/j for j in range(1,5))+c[6])
  hh,sh=hs(hi);hl,sl=hs(lo);da6=T*(hl-hh);da7=sl-sh;hi[5]+=da6;hi[6]+=da7
  corrections.append({'species':name,'Tmid_K':float(T),'delta_high_a6_K':float(da6),'delta_high_a7':float(da7),'delta_high_h_J_kg':float(m['constants']['R_J_kmol_K']*da6/d['molecular_weights'][i]),'delta_high_s_J_kg_K':float(m['constants']['R_J_kmol_K']*da7/d['molecular_weights'][i])})
 np.savez_compressed(R/'cache.npz',**d);m['original_cache_sha256']=original;m['cache_sha256']=sha(R/'cache.npz');m['variant']='NASA7 high-branch a6/a7 adjusted for continuous h and s at each Tmid; low branch and cp unchanged. This changes reverse equilibrium/rates and is NOT the original operator.';m['base_kernel_sha256']=sha(S/'kernel.py');m['corrections']=corrections;m['pressure_domain_Pa']=[.5*101325,2*101325]
 (R/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 assert sha(S/'cache.npz')==original
 print(json.dumps({'corrections':corrections,'new_cache_sha256':m['cache_sha256'],'wall_s':time.perf_counter()-t},indent=2))
if __name__=='__main__':main()
