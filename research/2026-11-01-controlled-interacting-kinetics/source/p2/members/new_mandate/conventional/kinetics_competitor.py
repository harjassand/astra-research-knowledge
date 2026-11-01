"""Conventional operator solution of a published two-path energy landscape.

Run: python3 new_mandate/conventional/kinetics_competitor.py

Potential: Trizio, Kang & Parrinello, Nat Comput Sci (2025),
DOI 10.1038/s43588-025-00799-5, arXiv:2410.17029, Eq. S5.
Dynamics here are a REVERSIBLE FINITE GRID CTMC approximating overdamped
Langevin dynamics with beta=1 and diffusion coefficient D=1. This is not
the paper's underdamped simulation. No kinetic calibration is claimed.

The code receives U(x,y), grid and observable predicates only. It does not
receive a committor, basin partition, intermediate states, or rate constants.
It solves the conventional backward equation directly, and reports a
deliberately restricted x-only Dirichlet construction as a failure witness.
"""
import json
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import spsolve


def potential(x, y):
    return (10*(2+4*x**4/3-2*y*y+y**4+10*x*x*(y*y-1)/3)
            +7*np.exp(-((x+.7)**2+(y-.8)**2)/.4**2)
            +np.exp(-((x-1)**2+(y+.3)**2)/.4**2)
            -6*np.exp(-((x+1)**2+(y+.6)**2)/.4**2)-2.35906)


def calculate(nx, ny):
    x=np.linspace(-1.7,1.7,nx)
    y=np.linspace(-1.5,1.5,ny)
    dx=x[1]-x[0]; dy=y[1]-y[0]
    X,Y=np.meshgrid(x,y,indexing='ij')
    u=potential(X,Y).ravel()
    pi=np.exp(-(u-u.min())); pi/=pi.sum()
    ids=np.arange(nx*ny).reshape(nx,ny)
    ei=np.concatenate([ids[:-1,:].ravel(),ids[:,:-1].ravel()])
    ej=np.concatenate([ids[1:,:].ravel(),ids[:,1:].ravel()])
    spacing=np.concatenate([np.full((nx-1)*ny,dx),np.full(nx*(ny-1),dy)])
    kij=np.exp(-(u[ej]-u[ei])/2)/spacing**2
    kji=np.exp(-(u[ei]-u[ej])/2)/spacing**2
    rows=np.concatenate([ei,ej]); cols=np.concatenate([ej,ei])
    vals=np.concatenate([kij,kji])
    Q=coo_matrix((vals,(rows,cols)),shape=(nx*ny,nx*ny)).tocsr()
    Q=Q-diags(np.asarray(Q.sum(axis=1)).ravel())
    # Observable-defined source/target sets. Intermediate basins are unknown.
    A=X.ravel()<=-.85; B=X.ravel()>=.85; interior=~(A|B)
    q=np.zeros(nx*ny); q[B]=1
    q[interior]=spsolve(Q[interior][:,interior],-Q[interior][:,B]@np.ones(B.sum()))
    conductance=pi[ei]*kij
    cap=np.sum(conductance*(q[ej]-q[ei])**2)
    a_flux=np.sum(pi[A]*(Q[A]@q))
    # Competing reactive flux through x=0; split by upper/lower pathway.
    cut=(X.ravel()[ei]<0)&(X.ravel()[ej]>=0)
    current=conductance[cut]*(q[ej[cut]]-q[ei[cut]])
    upper=(Y.ravel()[ei[cut]]>0)
    upper_fraction=current[upper].sum()/current.sum()
    # Conventional backward Poisson equation for source-law-specific MFPT.
    t=np.zeros(nx*ny); transient=~B
    t[transient]=spsolve(-Q[transient][:,transient],np.ones(transient.sum()))
    mfpt=float(np.dot(pi[A],t[A])/pi[A].sum())
    # Best x-only ansatz: minimize the same Dirichlet energy. This does not
    # receive the exact q, only summed nearest-layer conductances.
    cx=conductance[:(nx-1)*ny].reshape(nx-1,ny).sum(axis=1)
    ia=np.where(x<=-.85)[0][-1]; ib=np.where(x>=.85)[0][0]
    qx=np.zeros(nx); qx[ib:]=1
    resistance=1/cx[ia:ib]
    qx[ia+1:ib+1]=np.cumsum(resistance)/resistance.sum()
    q_trial=np.repeat(qx,ny)
    cap_x=np.sum(conductance*(q_trial[ej]-q_trial[ei])**2)
    tx=conductance[cut]*(q_trial[ej[cut]]-q_trial[ei[cut]])
    # Independent checks on the finite system, not tests of new physics.
    rel_capacity_balance=abs(a_flux-cap)/cap
    rel_cut_balance=abs(current.sum()-cap)/cap
    max_bvp_residual=float(np.max(np.abs((Q@q)[interior])))
    max_poisson_residual=float(np.max(np.abs((Q@t)[transient]+1)))
    return dict(grid=[nx,ny],energy_evaluations=nx*ny,directed_edges=2*len(ei),
                beta=1.0,diffusion=1.0,source_predicate='x <= -0.85',
                target_predicate='x >= 0.85',source_law='Boltzmann conditional on source predicate',
                capacity=float(cap),capacity_over_source_mass=float(cap/pi[A].sum()),
                source_mass=float(pi[A].sum()),mfpt_from_source_law=mfpt,
                inverse_source_mfpt=1/mfpt,upper_reactive_flux_fraction=float(upper_fraction),
                lower_reactive_flux_fraction=float(1-upper_fraction),
                x_only_capacity=float(cap_x),x_only_capacity_ratio=float(cap_x/cap),
                x_only_upper_fraction=float(tx[upper].sum()/tx.sum()),
                relative_capacity_balance=float(rel_capacity_balance),
                relative_cut_balance=float(rel_cut_balance),
                max_bvp_residual=max_bvp_residual,max_poisson_residual=max_poisson_residual)


def exposure_witness():
    """Exact limited-oracle obstruction, not a bound on all force algorithms."""
    # If each physical-time interval is conditionally an exponential race with
    # no changing precursor, the number of discoveries in aggregate simulated
    # exposure T is Poisson((lambda1+lambda2)*T). Cloning changes scheduling only.
    rates=[1e-6,3e-7]
    exposure=1e6
    return dict(scope='propagator-only memoryless channel; NOT full energy-oracle lower bound',
                rates=rates,total_simulated_exposure=exposure,
                no_exit_probability=float(np.exp(-sum(rates)*exposure)),
                no_second_channel_probability=float(np.exp(-rates[1]*exposure)),
                exposure_for_95_percent_second_channel_discovery=float(-np.log(.05)/rates[1]))


if __name__=='__main__':
    results={'description':__doc__,'grid_solutions':[calculate(69,61),calculate(103,91),calculate(137,121)],
             'restricted_oracle_witness':exposure_witness()}
    target=Path(__file__).with_name('kinetics_results.json')
    target.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
