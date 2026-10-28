"""Actual multislice detector templates; no physical damage calibration.

One Cr is displaced by (+b/2,-c/4) at one of 16 depths, following the source
unrelaxed construction. All hypotheses share the exact projected composition.
The native crystal is an additional hypothesis. Rigid-lattice diagnostic.
"""
from pathlib import Path
import argparse, json, os, time
ROOT=Path(__file__).resolve().parents[1]
for k,v in {'MPLBACKEND':'Agg','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'2',
            'NUMBA_NUM_THREADS':'2','NUMBA_CACHE_DIR':str(ROOT/'cache/numba'),
            'MPLCONFIGDIR':str(ROOT/'cache/mpl'),'PYTHONDONTWRITEBYTECODE':'1'}.items(): os.environ.setdefault(k,v)
import abtem, dask, numpy as np
from ase.io import read

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--gpts',type=int,default=256)
    p.add_argument('--states',default=','.join(map(str,range(17))))
    p.add_argument('--defocus',type=float,default=0.)
    p.add_argument('--tilt-y',type=float,default=0.)
    p.add_argument('--dz',type=float,default=1.)
    p.add_argument('--offset-x',type=float,default=0.)
    p.add_argument('--offset-y',type=float,default=0.)
    p.add_argument('--phonons',type=int,default=1)
    p.add_argument('--sigma',type=float,default=0.)
    p.add_argument('--seed-base',type=int,default=5021)
    p.add_argument('--also-displace',default='')
    p.add_argument('--layers',type=int,default=16)
    p.add_argument('--repeat-x',type=int,default=6)
    p.add_argument('--repeat-y',type=int,default=4)
    p.add_argument('--tag',default='rigid_256')
    a=p.parse_args(); start=time.monotonic()
    dask.config.set({'num_workers':2})
    abtem.config.set({'device':'cpu','diagnostics.progress_bar':False,'dask.lazy':False})
    crystal=read(ROOT/'sources/CrSBr.cif')*(a.repeat_x,a.repeat_y,a.layers)
    column=np.array([12.27065,9.5406])
    ids=np.flatnonzero((crystal.numbers==24)&(np.linalg.norm(crystal.positions[:,:2]-column,axis=1)<1e-4))
    ids=ids[np.argsort(crystal.positions[ids,2])]
    dx=np.arange(-2,3)*.35; dy=np.arange(-4,5)*.5+4.7703/4
    xx,yy=np.meshgrid(dx,dy,indexing='ij')
    positions=np.column_stack([xx.ravel(),yy.ravel()])+column+[a.offset_x,a.offset_y]
    all_meta=[]
    for state in [int(s) for s in a.states.split(',')]:
        dest=ROOT/f'outputs/{a.tag}_state{state:02d}.npz'
        if dest.exists(): print(f'skip {dest.name}',flush=True); continue
        t=time.monotonic(); atoms=crystal.copy()
        if state: atoms.positions[ids[state-1]]+=np.array([0,4.7703/2,-7.99416/4])
        for extra in [int(s) for s in a.also_displace.split(',') if s]:
            if extra!=state:atoms.positions[ids[extra-1]]+=np.array([0,4.7703/2,-7.99416/4])
        intensity=None
        # Common random displacements reduce Monte Carlo variance between
        # hypotheses. Sigma is an explicit sensitivity setting, not acquired
        # CrSBr thermal displacement data.
        for realization in range(a.phonons):
            snapshot=atoms.copy()
            if a.sigma:
                rng=np.random.default_rng(a.seed_base+realization)
                snapshot.positions+=rng.normal(0,a.sigma,snapshot.positions.shape)
            pot=abtem.Potential(snapshot,gpts=a.gpts,slice_thickness=a.dz,device='cpu').build().compute()
            probe=abtem.Probe(energy=200e3,semiangle_cutoff=32,defocus=a.defocus,
                              tilt=(0.,a.tilt_y),device='cpu')
            probe.grid.match(pot)
            waves=probe.multislice(scan=positions,potential=pot).compute()
            fields=np.asarray(waves.array)
            fft=np.fft.fftshift(np.fft.fft2(fields,axes=(-2,-1),norm='ortho'),axes=(-2,-1))
            incident=np.asarray(probe.build(scan=positions).compute().array)
            norm=(np.abs(incident)**2).sum(axis=(-2,-1))
            contribution=np.abs(fft)**2/norm[...,None,None]/a.phonons
            if intensity is None: intensity=contribution
            else: intensity+=contribution
        extent=np.asarray(atoms.cell.lengths()[:2])
        qx=np.fft.fftshift(np.fft.fftfreq(a.gpts,d=extent[0]/a.gpts))
        qy=np.fft.fftshift(np.fft.fftfreq(a.gpts,d=extent[1]/a.gpts))
        wavelength=probe.wavelength
        thx=qx*wavelength*1000; thy=qy*wavelength*1000
        tx,ty=np.meshgrid(thx,thy,indexing='ij')
        radius=np.hypot(tx,ty); cutoff=min(100.,min(waves.cutoff_angles))
        keep=radius<=cutoff
        probability=intensity[:,keep].astype(np.float32)
        np.savez_compressed(dest,p=probability,theta_x=tx[keep],theta_y=ty[keep],
                            positions=positions,scan_cell_area=.175,
                            lost=1-probability.sum(axis=1),depths=crystal.positions[ids,2])
        meta={'state':state,'elapsed_seconds':time.monotonic()-t,'shape':list(probability.shape),
              'cutoff_mrad':float(cutoff),'sum_probability_min':float(probability.sum(axis=1).min()),
              'sum_probability_max':float(probability.sum(axis=1).max()),
              'wave_norm_min':float((np.abs(fields)**2).sum(axis=(-2,-1)).min()),
              'probe_norm_min':float(norm.min())}
        all_meta.append(meta); print(json.dumps(meta),flush=True)
        del pot, waves, fields, fft, intensity, probability
    metadata_path=ROOT/f'outputs/{a.tag}_metadata.json'
    if not all_meta and metadata_path.exists():
        print('All requested templates already exist; original run metadata preserved.',flush=True)
        return
    previous=json.loads(metadata_path.read_text()) if metadata_path.exists() else None
    meta={'scope':__doc__,'abtem_version':abtem.__version__,'gpts':a.gpts,
          'defocus_angstrom':a.defocus,'beam_tilt_y_mrad':a.tilt_y,'slice_thickness_angstrom':a.dz,
          'elapsed_seconds':time.monotonic()-start,'states':all_meta,'energy_eV':200000,
          'semiangle_mrad':32,'thermal_model':{'gaussian_sigma_angstrom':a.sigma,'num_snapshots':a.phonons,'seed_base':a.seed_base,
          'calibration':'unmeasured sensitivity only'},'detector_efficiency':1,
          'registration_offset_angstrom':[a.offset_x,a.offset_y],
          'layers':a.layers,
          'additional_displaced_layers':[int(s) for s in a.also_displace.split(',') if s],
          'lateral_repeats':[a.repeat_x,a.repeat_y],
          'lateral_cell_angstrom':crystal.cell.lengths()[:2].tolist(),
          'scan_cell_area_angstrom2':.175,'scan_positions':positions.tolist(),
          'scan_area_angstrom2':len(positions)*.175,'thickness_angstrom':float(crystal.cell[2,2]),
          'defect_displacement_angstrom':[0,4.7703/2,-7.99416/4]}
    if previous is not None:
        meta['previous_run_metadata']=previous
    metadata_path.write_text(json.dumps(meta,indent=2))
if __name__=='__main__': main()
