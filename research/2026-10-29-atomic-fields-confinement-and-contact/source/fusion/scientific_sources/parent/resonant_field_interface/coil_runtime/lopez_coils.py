"""Ordinary current-potential realization, explicit for arXiv:2610.29921v1.
On Q=1, B=grad(phi) is tangent. K= -n_out x B/mu0, with zero
outside field, is a Maxwell jump solution. Equipotential filaments are
phi=2*pi*j/N with current I=2*pi/(mu0*N). Finite-coil tests below are
sampled, not a uniform field-error or manufacturability certificate.
"""
from pathlib import Path
import json,time
import numpy as np
from lopez_field import surface,surface_theta,B_at_labels

def field(targets,N,M,rcoil=1.,offset=.5):
    theta=2*np.pi*np.arange(M)/M
    phi=2*np.pi*(np.arange(N)+offset)/N
    th,ph=np.meshgrid(theta,phi,indexing='ij')
    xx=surface(rcoil,th,ph).reshape(3,-1).T
    tangent=surface_theta(rcoil,th,ph).reshape(3,-1).T
    out=[]
    for first in range(0,len(targets),12):
        rr=targets[first:first+12,None,:]-xx[None,:,:]
        r2=np.sum(rr*rr,axis=2)
        out.append(np.sum(np.cross(tangent[None,:,:],rr)/r2[:,:,None]**1.5,axis=1)*np.pi/(N*M))
    return np.concatenate(out)

def run():
 start=time.time()
 labels=[];targets=[];refs=[]
 for rr in [0,.3,.6]:
  for th in (np.arange(8)*2*np.pi/8 if rr else [0.]):
   for ph in np.arange(24)*2*np.pi/24:
    l=.15+rr*np.cos(th)/30;b=.02+rr*np.sin(th)/10
    labels.append([rr,float(th),float(ph)]);targets.append(surface(rr,th,ph));refs.append(B_at_labels(l,b,ph))
 targets=np.array(targets);refs=np.array(refs);norm=np.linalg.norm(refs,axis=1)
 rows=[];previous=None
 for N,M in [(16,256),(32,256),(64,256),(128,256),(256,256),(256,512)]:
  st=time.time();bb=field(targets,N,M)
  er=np.linalg.norm(bb-refs,axis=1)/norm
  by_r={str(rr):float(er[np.array(labels)[:,0]==rr].max()) for rr in [0,.3,.6]}
  row=dict(N_coils=N,M_quadrature=M,max_sample_relative_error=float(er.max()),rms_sample_relative_error=float(np.sqrt(np.mean(er*er))),max_error_by_target_radius=by_r,seconds=time.time()-st)
  if previous is not None and N==256 and M==512:row['M_doubling_change']=float(np.max(np.linalg.norm(bb-previous,axis=1)/norm))
  previous=bb;rows.append(row)
 theta=np.arange(4096)*2*np.pi/4096;phis=np.arange(256)*2*np.pi/256
 lengths=[]
 for ph in phis:lengths.append(float(np.linalg.norm(surface_theta(1,theta,ph),axis=0).mean()*2*np.pi))
 out=dict(target_count=len(targets),coil_surface_Q=1,rows=rows,current_formula='I = (2*pi/N)*(B_unit*L_unit/mu0)',coil_length_range=[min(lengths),max(lengths)],total_coil_length_for_N256=sum(lengths),seconds=time.time()-start)
 Path('results/lopez_coils.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
