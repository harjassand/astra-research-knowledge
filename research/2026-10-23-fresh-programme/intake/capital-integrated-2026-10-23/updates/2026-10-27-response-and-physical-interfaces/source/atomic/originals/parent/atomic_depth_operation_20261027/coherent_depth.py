"""Conditional coherent-probe selectivity, all Cr competitors and incident norm."""
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parent
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[key] = '2'
os.environ['MPLBACKEND'] = 'Agg'
os.environ['MPLCONFIGDIR'] = str(ROOT/'mpl_cache')
os.environ['NUMBA_CACHE_DIR'] = str(ROOT/'numba_cache')
import json
import time
import numpy as np
import abtem
import dask
from ase.io import read
from scipy.linalg import eigh


def main():
    start = time.monotonic()
    source = ROOT.parents[1]/'empirical_operation_invention'/'sources'
    dask.config.set({'num_workers': 2})
    abtem.config.set({'device': 'cpu', 'diagnostics.progress_bar': False})
    atoms = read(source/'CrSBr.cif')*(6,4,16)
    column = np.array([12.27065,9.5406])
    cr = atoms.positions[atoms.numbers==24]
    depths = np.unique(np.round(cr[:,2],7))
    thickness = atoms.cell[2,2]
    dz = thickness/int(np.ceil(thickness))
    slices = tuple((np.floor(depths/dz)-1).astype(int))
    gpts = 256
    potential = abtem.Potential(atoms,gpts=gpts,slice_thickness=1,
                                exit_planes=slices,device='cpu').build().compute()
    fs, ins = [], []
    focuses = np.arange(-128.,129.,32.)
    for f in focuses:
        probe = abtem.Probe(energy=200e3,semiangle_cutoff=32,defocus=float(f),device='cpu')
        probe.grid.match(potential)
        entry = np.asarray(probe.build(scan=column[None]).compute().array).reshape(gpts,gpts)
        field = np.asarray(probe.multislice(scan=column[None],potential=potential).compute().array)
        field = field.reshape(len(depths),gpts,gpts)
        fs.append(field); ins.append(entry)
        print('defocus',f,'elapsed',round(time.monotonic()-start,2),flush=True)
    fields = np.stack(fs,axis=1).astype(np.complex128)
    inputs = np.stack(ins).reshape(len(focuses),-1).astype(np.complex128)
    gram = inputs.conj()@inputs.T
    lengths = np.array(atoms.cell.lengths()[:2])
    grid = np.moveaxis(np.indices((gpts,gpts)),0,-1)*lengths/gpts
    pixel_area = np.prod(lengths)/gpts**2
    all_m = np.zeros((len(focuses),len(focuses)),complex)
    targets=[]; target_z=[]
    for zi,z in enumerate(depths):
        sites = cr[np.abs(cr[:,2]-z)<1e-5,:2]
        weight = np.zeros((gpts,gpts))
        target_weight = None
        for xy in sites:
            delta = (grid-xy+lengths/2)%lengths-lengths/2
            mask = np.linalg.norm(delta,axis=-1)<=.4
            w = mask/(mask.sum()*pixel_area)
            weight += w
            if np.linalg.norm(xy-column)<1e-4:
                target_weight=w
        f = fields[zi].reshape(len(focuses),-1)
        all_m += (f.conj()*weight.ravel())@f.T
        if target_weight is not None:
            targets.append((f.conj()*target_weight.ravel())@f.T)
            target_z.append(z)
    def herm(x): return (x+x.conj().T)/2
    gram=herm(gram); all_m=herm(all_m)
    ge,gv=eigh(gram)
    assert ge.min()>1e-10
    whiten=gv/np.sqrt(ge)[None,:]
    total=herm(whiten.conj().T@all_m@whiten)
    records=[]
    for j,target in enumerate(targets):
        target=herm(target)
        t=herm(whiten.conj().T@target@whiten)
        ordinary=np.real(np.diag(target)/np.diag(all_m))
        vals,vecs=eigh(t,total)
        v=vecs[:,-1]; v/=np.linalg.norm(v)
        target_at_ratio=float(np.real(v.conj()@t@v))
        maxeff=float(eigh(t,eigvals_only=True)[-1])
        # Each eta solves max input-normalized target density minus eta times
        # collateral density. Supporting points expose the dose/selectivity tradeoff.
        frontier=[]
        for eta in np.r_[0.,np.logspace(-4,4,65)]:
            _,vs=eigh(herm(t-eta*(total-t)))
            v=vs[:,-1]
            power=float(np.real(v.conj()@t@v))
            totalpower=float(np.real(v.conj()@total@v))
            frontier.append({'collateral_penalty':float(eta),
                             'target_density_per_incident_electron_Aminus2':power,
                             'target_fraction_all_Cr':power/totalpower,
                             'relative_target_efficiency':power/maxeff})
        records.append({'layer_1based':j+1,'z_angstrom':float(target_z[j]),
                        'best_single_focus_fraction_all_Cr':float(ordinary.max()),
                        'best_single_focus_defocus_angstrom':float(focuses[ordinary.argmax()]),
                        'maximum_coherent_fraction_all_Cr':float(vals[-1]),
                        'target_density_at_maximum_ratio':target_at_ratio,
                        'maximum_target_density':maxeff,
                        'relative_efficiency_at_maximum_ratio':target_at_ratio/maxeff,
                        'support_points':frontier})
    np.savez_compressed(ROOT/'COHERENT_MATRICES.npz',gram=gram,all_Cr=all_m,
                        targets=np.stack(targets),defocus=focuses,depth=target_z)
    out={'scope':__doc__,'gpts':gpts,'abtem_version':abtem.__version__,
         'n_Cr':len(cr),'n_exit_planes':len(depths),'n_target_layers':len(targets),
         'gram_eigenvalues':ge.tolist(),'input_mode_norms':np.diag(gram).real.tolist(),
         'total_response_eigenvalues':eigh(total,eigvals_only=True).tolist(),
         'records':records,'elapsed_seconds':time.monotonic()-start}
    (ROOT/'COHERENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'fractions':[r['maximum_coherent_fraction_all_Cr'] for r in records],
                      'efficiencies':[r['relative_efficiency_at_maximum_ratio'] for r in records],
                      'elapsed_seconds':out['elapsed_seconds']},indent=2))


if __name__=='__main__': main()
