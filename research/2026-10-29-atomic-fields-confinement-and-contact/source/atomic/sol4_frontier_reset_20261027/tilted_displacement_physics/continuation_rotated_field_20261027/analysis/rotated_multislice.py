"""Finite rotated-crystal IAM multislice; site fluence is not a write hazard."""
from pathlib import Path
import argparse,json,math,time,resource
import numpy as np
from scipy.fft import ifft2
from scipy.linalg import eigh_tridiagonal
from scipy.special import j0
from numpy.polynomial.hermite_e import hermegauss
from ase import Atoms
from ase.io import read,write
import abtem,dask
from abtem.multislice import conventional_multislice_step,FresnelPropagator
from abtem.antialias import AntialiasAperture
from abtem.core.energy import energy2wavelength
from abtem.core.axes import OrdinalAxis
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT.parents[1]/'empirical_operation_invention'
ENERGY=200000.;LAM=energy2wavelength(ENERGY);ALPHA=.032
abtem.config.set({'device':'cpu','fft':'fftw','fftw.threads':2,'fftw.planning_effort':'FFTW_ESTIMATE','diagnostics.progress_bar':False})
dask.config.set({'num_workers':2,'temporary_directory':str(ROOT/'tmp/dask')})

def geometry(aa,bb,hw,box,dz,fixed_depth=None):
 uc=read(SRC/'sources/CrSBr.cif');cell=uc.cell.lengths();target=uc.positions[0]+[0,0,7*cell[2]];pts=[];nums=[];labels=[]
 for k in range(16):
  for ia in range(-12,13):
   for ib in range(-10,11):
    for basis,(num,p) in enumerate(zip(uc.numbers,uc.positions)):
     q=p+[ia*cell[0],ib*cell[1],k*cell[2]]-target
     if abs(q[0])<=hw and abs(q[1])<=hw:pts.append(q);nums.append(num);labels.append((k+1,basis,ia,ib))
 crystal=np.array(pts);labels=np.array(labels);n=np.r_[np.tan(np.deg2rad([aa,bb])),1.];n/=np.linalg.norm(n);ex=np.array([1.,0.,-n[0]/n[2]]);ex/=np.linalg.norm(ex);ey=np.cross(n,ex);R=np.stack([ex,ey,n]);rot=crystal@R.T;shift=np.array([box/2,box/2,-rot[:,2].min()+8. if fixed_depth is None else fixed_depth]);rot+=shift
 height=math.ceil((rot[:,2].max()+8)/dz)*dz;atoms=Atoms(numbers=nums,positions=rot,cell=[box,box,height],pbc=False);atoms.new_array('crystal_positions',crystal);atoms.info['halfwidth']=hw
 ti=np.where((labels==[8,0,0,0]).all(1))[0].item();margins=np.minimum(rot.min(0),np.array([box,box,height])-rot.max(0));assert np.all(margins>5),margins
 assert np.linalg.norm(rot[ti]-shift)<1e-9 and np.linalg.norm(R@R.T-np.eye(3))<1e-12
 return atoms,labels,R,shift,ti,margins

def positive_quad(nodes,weights,N):
 weights=np.array(weights,float);weights/=weights.sum();q=np.sqrt(weights);basis=[];diag=[];off=[];prev=np.zeros_like(q);beta=0.
 for j in range(min(N,len(q))):
  basis.append(q.copy());v=nodes*q-beta*prev;alpha=float(q@v);v-=alpha*q
  for _ in range(2):
   for old in basis:v-=old*(old@v)
  diag.append(alpha);newbeta=np.linalg.norm(v)
  if j==N-1 or newbeta<1e-14:break
  off.append(newbeta);prev,q=q,v/newbeta;beta=newbeta
 x,V=eigh_tridiagonal(diag,off);return x,V[0]**2

def specs(kind,sigma,N):
 h,w=hermegauss(N);h*=sigma;w/=np.sqrt(2*np.pi);xy=np.array(np.meshgrid(h,h,indexing='ij')).reshape(2,-1).T;ww=np.outer(w,w).ravel();gs=.8/math.sqrt(8*math.log(2))
 out=[('parked_ideal32',np.zeros((1,2)),np.ones(1),0.),('parked_coherent08',np.zeros((1,2)),np.ones(1),gs),('parked_incoherent08',xy,ww,0.)]
 if kind=='onaxis':
  phase=(np.arange(32)+.5)*2*np.pi/32;s=4.7703/4*(1+np.cos(phase));pos=np.c_[np.zeros(len(s)),s]
  out += [('plus_b_ideal32',pos,np.ones(len(s))/len(s),0.),('plus_b_coherent08',pos,np.ones(len(s))/len(s),gs)]
  yn=(s[:,None]+h[None,:]).ravel();yw=(np.ones((len(s),1))/len(s)*w[None,:]).ravel();yn,yw=positive_quad(yn,yw,20);xy=np.array(np.meshgrid(h,yn,indexing='ij')).reshape(2,-1).T;ww=np.outer(w,yw).ravel();out.append(('plus_b_incoherent08',xy,ww,0.))
 return out

def build_modes(gpts,box,focus,center,kind,sigma,tail,N):
 dx=box/gpts;freq=np.fft.fftfreq(gpts,dx);kx,ky=np.meshgrid(freq,freq,indexing='ij');k2=kx*kx+ky*ky;mask=k2<=(ALPHA/LAM)**2;k=np.c_[kx[mask],ky[mask]];k2m=k2[mask];f=np.unique(k[:,0]);ix=np.searchsorted(f,k[:,0]);iy=np.searchsorted(f,k[:,1]);delta=f[:,None]-f[None,:];position_phase=np.exp(-2j*np.pi*(k@center)).astype(np.complex64);phase=position_phase*np.exp(1j*np.pi*LAM*focus*k2m).astype(np.complex64)
 arrays=[];infos=[];offset=0;vacuum={};names=['parked_ideal32','parked_coherent08','parked_incoherent08']
 if kind=='onaxis':names+=['plus_b_ideal32','plus_b_coherent08','plus_b_incoherent08']
 for name in names:
  gs=.8/math.sqrt(8*math.log(2)) if 'coherent08' in name and 'incoherent08' not in name else 0.;A=np.exp(-4*np.pi**2*gs*gs*k2m);A/=np.linalg.norm(A);sigs=sigma if 'incoherent08' in name else 0.
  Kx=np.exp(-2*np.pi**2*sigs*sigs*delta*delta).astype(complex);Ky=Kx.copy()
  if name.startswith('plus_b'):
   mid=4.7703/4;Ky*=np.exp(-2j*np.pi*mid*delta)*j0(2*np.pi*mid*delta)
  factors=[];oneD=[]
  for K in [Kx,Ky]:
   ev,V=np.linalg.eigh(K);ev=np.maximum(ev[::-1],0);V=V[:,::-1];keep=min(len(ev),int(np.searchsorted(np.cumsum(ev),np.trace(K).real*(1-1e-12)))+1);ev=ev[:keep];V=V[:,:keep];factors.append(V*np.sqrt(ev)[None,:]);oneD.append(keep)
  Fx,Fy=factors;Agrid=np.zeros((len(f),len(f)));Agrid[ix,iy]=A*A;weights=(np.abs(Fx)**2).T@Agrid@(np.abs(Fy)**2);order=np.argsort(weights.ravel())[::-1];sortedw=weights.ravel()[order];keep=min(len(order),int(np.searchsorted(np.cumsum(sortedw),1-tail))+1);order=order[:keep];ev=sortedw[:keep];indices=np.array(np.unravel_index(order,weights.shape)).T
  Q=np.array([A*Fx[ix,m]*Fy[iy,n]/math.sqrt(w) for (m,n),w in zip(indices,ev)]);arr=np.zeros((keep,gpts,gpts),np.complex64);arr[:,mask]=(Q*phase).astype(np.complex64);arr=ifft2(arr,axes=(-2,-1),norm='ortho',workers=2).astype(np.complex64);arrays.append(arr);infos.append(dict(name=name,start=offset,stop=offset+keep,weights=ev.tolist(),retained_trace=float(ev.sum()),source_model='analytic Gaussian coherence times analytic sinusoidal-scan characteristic function',one_dimensional_factor_ranks=oneD,coherent_modes=keep));offset+=keep
  if name.startswith('parked'):
   field=np.zeros((keep,gpts,gpts),np.complex64);field[:,mask]=(Q*position_phase).astype(np.complex64);field=ifft2(field,axes=(-2,-1),norm='ortho',workers=2);I=np.einsum('i,ijk->jk',ev,np.abs(field)**2)/(dx*dx);vacuum[name]=dict(peak_per_A2=float(I.max()),norm=float(I.sum()*dx*dx),x_line=I[:,gpts//2].tolist(),y_line=I[gpts//2].tolist())
  print(json.dumps(dict(controller=name,modes=keep,trace=float(ev.sum()))),flush=True)
 return np.concatenate(arrays),infos,vacuum

def stencil(xy,gpts,box,radius):
 dx=box/gpts;n=math.ceil(radius/dx)+1;off=np.array(np.meshgrid(np.arange(-n,n+1),np.arange(-n,n+1),indexing='ij')).reshape(2,-1).T;ix=np.floor(xy/dx).astype(int)[:,None,:]+off[None];delta=ix*dx-xy[:,None,:];area=np.zeros(delta.shape[:2]);sub=(np.arange(4)+.5)/4-.5
 for sx in sub:
  for sy in sub:area+=np.sum((delta+[sx*dx,sy*dx])**2,axis=-1)<=radius*radius
 area/=area.sum(1)[:,None];return ((ix[:,:,0]%gpts)*gpts+(ix[:,:,1]%gpts)).astype(np.int64),area

def measure(I,xy,gpts,box):
 out=[];flat=I.reshape(len(I),-1)
 for radius in [.2,.4]:
  ix,w=stencil(xy,gpts,box,radius);out.append(np.einsum('ijk,jk->ij',flat[:,ix],w))
 u=xy/(box/gpts);lo=np.floor(u).astype(int);f=u-lo;point=np.zeros((len(I),len(xy)))
 for i in [0,1]:
  for j in [0,1]:
   idx=((lo[:,0]+i)%gpts)*gpts+(lo[:,1]+j)%gpts;w=(f[:,0] if i else 1-f[:,0])*(f[:,1] if j else 1-f[:,1]);point+=flat[:,idx]*w
 out.append(point);return np.stack(out,axis=-1)

def summarize(local,atoms,labels,ti,infos):
 out=[];syms=np.array(atoms.get_chemical_symbols());cr=syms=='Cr';edges=np.max(np.abs(atoms.arrays['crystal_positions'][:,:2]),axis=1)>atoms.info['halfwidth']-5
 for q in infos:
  lc=np.einsum('i,ijk->jk',q['weights'],local[q['start']:q['stop']]);metrics=[]
  for m,name in enumerate(['disk_r02','disk_r04','point_bilinear']):
   v=lc[:,m];total=v[cr].sum();order=np.argsort(v*cr)[::-1]
   metrics.append(dict(metric=name,target_density_per_e_per_A2=float(v[ti]),species_density_sums={s:float(v[syms==s].sum()) for s in ['Cr','S','Br']},target_over_all_Cr=float(v[ti]/total) if total else None,other_Cr_over_target=float(total/v[ti]-1) if v[ti] else None,top_Cr=[dict(atom=int(i),label=labels[i].tolist(),density=float(v[i]),position_A=atoms.positions[i].tolist()) for i in order[:12]],edge_Cr_sum=float(v[cr&edges].sum())))
  out.append(dict(controller=q['name'],trace=q['retained_trace'],metrics=metrics))
 return out

def run(args):
 start=time.monotonic();aa,bb=(0.,0.) if args.kind=='onaxis' else (1.,10.);atoms,labels,R,center,ti,margins=geometry(aa,bb,args.halfwidth,args.box,args.dz,args.fixed_target_depth)
 potential=abtem.Potential(atoms,gpts=args.gpts,slice_thickness=args.dz,projection=args.projection,periodic=False,device='cpu');transformed=potential.get_transformed_atoms();sliced=potential.get_sliced_atoms();assert len(transformed)==len(atoms) and np.max(np.abs(transformed.positions-atoms.positions))<1e-8;assert len(sliced.atoms)==len(atoms),(len(sliced.atoms),len(atoms));assert np.max(np.abs(sliced.atoms.positions-atoms.positions))<1e-8
 cal=json.loads((ROOT/'outputs/probe_calibration.json').read_text());arr,infos,vacuum=build_modes(args.gpts,args.box,center[2],center[:2],args.kind,cal['source_sigma_A'],args.tail,args.source_order);norm0=(np.abs(arr)**2).sum(axis=(-2,-1));waves=abtem.Waves(arr,energy=ENERGY,sampling=args.box/args.gpts,ensemble_axes_metadata=[OrdinalAxis(label='coherent_mode',values=tuple(range(len(arr))))])
 nsl=len(potential);thick=np.array(potential.slice_thickness);zplanes=np.r_[0,np.cumsum(thick)];assigned=np.minimum(np.searchsorted(zplanes,atoms.positions[:,2],side='right')-1,nsl-1);local=np.zeros((len(arr),len(atoms),3),np.float64);prop=FresnelPropagator();aa_apert=AntialiasAperture();checks=[];snaps={};dx=args.box/args.gpts;border=max(1,int(5/dx));ts=int(assigned[ti])
 print(json.dumps(dict(starting=args.prefix,atoms=len(atoms),modes=len(arr),slices=nsl,box=atoms.cell.lengths().tolist(),margins=margins.tolist(),elapsed=time.monotonic()-start)),flush=True)
 for s,sl in enumerate((None for _ in range(nsl)) if args.vacuum else potential.generate_slices()):
  idx=np.where(assigned==s)[0]
  if len(idx):
   I=np.abs(waves.array)**2/(dx*dx);local[:,idx]=measure(I,atoms.positions[idx,:2],args.gpts,args.box)
  if s%32==0 or s in [ts,nsl-1]:
   I=np.abs(waves.array)**2;norm=I.sum(axis=(-2,-1));edge=norm-I[:,border:-border,border:-border].sum(axis=(-2,-1));checks.append(dict(slice=s,z_A=float(zplanes[s]),min_mode_norm=float(norm.min()),max_mode_norm=float(norm.max()),max_mode_border_probability=float(edge.max()),controller_norms={q['name']:dict(norm=float(np.dot(q['weights'],norm[q['start']:q['stop']])),border_probability=float(np.dot(q['weights'],edge[q['start']:q['stop']]))) for q in infos}))
   if s in [0,ts,nsl-1]:
    if s==ts:
     half=int(np.ceil(4/dx));mid=args.gpts//2;snaps['target_complex_mode_patches']=waves.array[:,mid-half:mid+half+1,mid-half:mid+half+1].copy()/dx;snaps['target_patch_origin_A']=np.array([(mid-half)*dx,(mid-half)*dx,zplanes[s]]);snaps['mode_weights_full']=np.concatenate([q['weights'] for q in infos]);snaps['patch_sampling_A']=np.array(dx)
    for q in infos:
     avg=np.einsum('i,ijk->jk',q['weights'],I[q['start']:q['stop']])/(dx*dx);step=max(1,args.gpts//384);snaps[f"{q['name']}_slice{s}"]=avg[::step,::step]
   print(json.dumps(dict(step=s,total=nsl,elapsed_seconds=time.monotonic()-start,norm_min=float(norm.min()),border_max=float(edge.max()))),flush=True)
  waves=prop.propagate(waves,thickness=float(thick[s]),in_place=True,order=args.propagator_order) if args.vacuum else conventional_multislice_step(waves,sl,prop,aa_apert,order=args.propagator_order)
  if args.stop and s+1>=args.stop:break
 out=dict(scope=__doc__,status='NOT_ACHIEVED',args=vars(args),abtem_version=abtem.__version__,energy_eV=ENERGY,wavelength_A=LAM,aperture_mrad=32,tilt_a_b_deg=[aa,bb],rotation=R.tolist(),target_index=ti,target_position_A=center.tolist(),vacuum_margins_A=margins.tolist(),atoms=len(atoms),species_counts={s:atoms.get_chemical_symbols().count(s) for s in ['Cr','S','Br']},box_A=atoms.cell.lengths().tolist(),transformed_atoms_unchanged=True,padded_atom_count=len(sliced.atoms),slices=nsl,slice_thickness_range_A=[float(thick.min()),float(thick.max())],preplane_atom_gap_A=[float((atoms.positions[:,2]-zplanes[assigned]).min()),float((atoms.positions[:,2]-zplanes[assigned]).max())],controllers=infos,vacuum_focus_profiles=vacuum,initial_mode_norm_range=[float(norm0.min()),float(norm0.max())],norm_and_edge=checks,results=summarize(local,atoms,labels,ti,infos),elapsed_seconds=time.monotonic()-start,peak_resident_memory_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 prefix=ROOT/'outputs'/args.prefix;prefix.with_suffix('.json').write_text(json.dumps(out,indent=2));np.savez_compressed(str(prefix)+'_fields.npz',**snaps,positions=atoms.positions,numbers=atoms.numbers,labels=labels,crystal_positions=atoms.arrays['crystal_positions'],local_densities=local);write(str(prefix)+'_atoms.extxyz',atoms)
 print(json.dumps(dict(finished=args.prefix,seconds=out['elapsed_seconds'],disk04=[dict(controller=q['controller'],**q['metrics'][1]) for q in out['results']]),indent=2),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--kind',choices=['onaxis','oblique'],required=True);p.add_argument('--prefix',required=True);p.add_argument('--gpts',type=int,default=768);p.add_argument('--box',type=float,default=96);p.add_argument('--halfwidth',type=float,default=24);p.add_argument('--dz',type=float,default=1);p.add_argument('--projection',choices=['finite','infinite'],default='finite');p.add_argument('--propagator-order',type=int,default=2);p.add_argument('--source-order',type=int,default=9);p.add_argument('--tail',type=float,default=1e-6);p.add_argument('--stop',type=int,default=0);p.add_argument('--vacuum',action='store_true');p.add_argument('--fixed-target-depth',type=float,default=None);run(p.parse_args())
