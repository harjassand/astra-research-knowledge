#!/usr/bin/env python3
"""Scoped continuum coupling calculation, NOT ab initio materials validation.

A surface hole polarizes a confined effective-mass electron in a dielectric
sphere. The same dielectric boundaries determine the terminal weighting field.
SI source geometry/mass do not establish dielectric constants or hole centroid.
Hard-wall confinement; no self-image potential, atomistic surface, ligand
hybridization, nonlocal screening, or polaron relaxation is included.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.constants import hbar, electron_mass, elementary_charge, epsilon_0
from scipy.special import eval_legendre
from scipy.sparse import diags, bmat
from scipy.sparse.linalg import eigsh
from numpy.polynomial.legendre import leggauss

E = elementary_charge
COULOMB = E / (4*np.pi*epsilon_0)*1e9  # eV nm
KINETIC = hbar**2/(2*electron_mass)/E*1e18  # eV nm^2


def solve(radius_nm: float=2.05, hole_offset_nm: float=.30,
          eps_core: float=9., eps_host: float=2., mass_ratio: float=.2,
          nr: int=160, lmax: int=6, hole_scale: float=1.,
          applied_field_v_per_nm: float=0.) -> dict:
    if min(radius_nm, eps_core, eps_host, mass_ratio)>0 and hole_offset_nm>=0:
        pass
    else:
        raise ValueError('Require positive physical constants and exterior hole')
    rh=radius_nm+hole_offset_nm
    dr=radius_nm/(nr+1)
    r=dr*np.arange(1,nr+1)
    x,w=leggauss(max(40,4*lmax+8))
    # Spherical harmonics Y_l0, integrated over azimuth: phi_l=sqrt((2l+1)/2)P_l.
    basis=np.array([np.sqrt((2*l+1)/2)*eval_legendre(l,x) for l in range(lmax+1)])
    potential=np.zeros((nr,len(x)))
    # Angular products of retained l<=lmax only need potential degrees <=2*lmax.
    for j in range(2*lmax+1):
        coef=(2*j+1)/(j*eps_core+(j+1)*eps_host)
        potential-=hole_scale*COULOMB*coef*(r[:,None]**j/rh**(j+1))*eval_legendre(j,x)[None,:]
    local=3*eps_host/(eps_core+2*eps_host)
    # Electron energy +e phi; phi=E_local*z, in eV when E is V/nm.
    potential+=applied_field_v_per_nm*local*r[:,None]*x[None,:]
    vblocks=np.einsum('li,mi,ri,i->lmr',basis,basis,potential,w,optimize=True)
    kin=KINETIC/mass_ratio
    lap=diags([-np.ones(nr-1),2*np.ones(nr),-np.ones(nr-1)],[-1,0,1],format='csr')*kin/dr**2
    blocks=[]
    for l in range(lmax+1):
        row=[]
        for m in range(lmax+1):
            block=diags(vblocks[l,m],format='csr')
            if l==m:
                block=block+lap+diags(kin*l*(l+1)/r**2,format='csr')
            row.append(block)
        blocks.append(row)
    H=bmat(blocks,format='csr')
    ev,vec=eigsh(H,k=1,which='SA',tol=1e-10,v0=np.ones(H.shape[0]))
    u=vec[:,0].reshape(lmax+1,nr)  # discrete-normalized; dr incorporated by norm.
    angular_z=np.einsum('li,mi,i,i->lm',basis,basis,x,w,optimize=True)
    mean_z=float(np.einsum('lr,mr,r,lm->',u,u,r,angular_z,optimize=True))
    mean_r2=float(np.sum(u*u*r[None,:]**2))
    kappa=(eps_core-eps_host)/(eps_core+2*eps_host)
    hole_weight_length=rh-kappa*radius_nm**3/rh**2
    terminal_mu_enm=hole_weight_length-local*mean_z
    residual=float(np.linalg.norm(H@vec[:,0]-ev[0]*vec[:,0]))
    return dict(radius_nm=radius_nm,hole_offset_nm=hole_offset_nm,eps_core=eps_core,
                eps_host=eps_host,mass_ratio=mass_ratio,nr=nr,lmax=lmax,
                hole_scale=hole_scale,field_v_per_nm=applied_field_v_per_nm,
                ground_energy_ev=float(ev[0]),electron_mean_z_nm=mean_z,
                electron_rms_radius_nm=float(np.sqrt(mean_r2)),
                local_field_factor=local,hole_weight_length_nm=hole_weight_length,
                terminal_dipole_e_nm=terminal_mu_enm,eigen_residual_ev=residual)


def main() -> None:
    folder=Path(__file__).resolve().parent/'results'
    folder.mkdir(exist_ok=True)
    cases=[solve(eps_core=ec,hole_offset_nm=off,nr=120,lmax=5)
           for ec in [5.,9.,12.] for off in [0.,.15,.30]]
    nominal=solve()
    finer=solve(nr=240,lmax=8)
    neutral=solve(hole_scale=0.)
    field=1e-4
    plus=solve(applied_field_v_per_nm=field)
    minus=solve(applied_field_v_per_nm=-field)
    derivative=(plus['ground_energy_ev']-minus['ground_energy_ev'])/(2*field)
    expected=nominal['local_field_factor']*nominal['electron_mean_z_nm']
    tests={
        'zero_hole_parity':abs(neutral['electron_mean_z_nm'])<1e-8,
        'zero_hole_infinite_well_energy':abs(neutral['ground_energy_ev']/(KINETIC/.2*np.pi**2/2.05**2)-1)<5e-5,
        'nominal_eigen_residual':nominal['eigen_residual_ev']<1e-7,
        'mesh_and_angular_dipole_convergence':abs(finer['terminal_dipole_e_nm']-nominal['terminal_dipole_e_nm'])<3e-4,
        'hellmann_feynman_weighting_charge':abs(derivative-expected)<1e-6,
        'all_means_inside_sphere':all(0<=x['electron_mean_z_nm']<2.05 for x in cases),
        'all_dipoles_positive':all(x['terminal_dipole_e_nm']>0 for x in cases)
    }
    data={'status':'Continuum sensitivity calculation; not a measured or ab initio dipole.',
          'source_inputs':{'radius_nm':{'value':2.05,'status':'half reported 4.1 nm upper CdS QD diameter'},
                           'mass_ratio':{'value':.2,'status':'source SI effective-mass model parameter'}},
          'assumptions':['spherical uniform linear dielectric core and host',
                         'hard-wall confinement replaces finite source barrier ~2.84 eV',
                         'external localized hole centroid; no atomistic geometry acquired',
                         'eps_core 5,9,12 and eps_host 2 are sensitivity inputs, not measurements',
                         'no electron self-image, crystal anisotropy, polaron or ligand hybridization'],
          'nominal':nominal,'refined':finer,'no_hole':neutral,'sensitivity_cases':cases,
          'finite_field_energy_derivative_e_nm':derivative,
          'hellmann_feynman_expected_e_nm':expected,'checks':tests,
          'check_count':len(tests),'all_checks_pass':all(tests.values())}
    (folder/'coupling_results.json').write_text(json.dumps(data,indent=2))
    print(json.dumps(data,indent=2))
    if not all(tests.values()):
        raise AssertionError('Continuum diagnostic failed')

if __name__=='__main__':
    main()
