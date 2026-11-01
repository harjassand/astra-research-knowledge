"""Independent dense audit of root's Gaussian-reference extension.

The root module supplies its microscopic disordered Glauber model. This file
independently constructs all local generator pieces, adds two-spectator rate
modifiers, and checks the operator theorems without using a Gaussian formula
for the perturbed inverse. It also tests an explicit positive exponential sum.
"""
import importlib.util
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import eigh, solve
from numpy.polynomial import Chebyshev, Polynomial

root_file=Path(__file__).resolve().parents[1]/"root"/"gaussian_kinetics.py"
spec=importlib.util.spec_from_file_location("root_gaussian",root_file)
root=importlib.util.module_from_spec(spec)
spec.loader.exec_module(root)


def local_generators(m,strength):
    n=m['n']
    states=[s for s in range(1<<n) if s.bit_count()%2==0]
    ix={s:j for j,s in enumerate(states)}
    weights=np.array([np.exp(-sum(2*m['J'][i]*((s>>i)&1) for i in range(n))) for s in states])
    pi=weights/weights.sum()
    pieces=[]; baseline=[]
    for i in range(n):
        j=(i+1)%n; k=(i+2)%n; ell=(i+3)%n
        Qi=np.zeros((len(states),len(states)));Q0i=Qi.copy()
        for col,s in enumerate(states):
            xy=((s>>i)&1,(s>>j)&1)
            q={(0,0):m['c'][i],(1,1):m['a'][i],(1,0):m['d'][i],(0,1):m['e'][i]}[xy]
            a=math.exp(strength*(2*((s>>k)&1)-1)*(2*((s>>ell)&1)-1))
            row=ix[s^(1<<i)^(1<<j)]
            Q0i[row,col]+=q; Q0i[col,col]-=q
            Qi[row,col]+=a*q; Qi[col,col]-=a*q
        D=np.sqrt(pi)
        baseline.append(-Q0i*D[None,:]/D[:,None])
        pieces.append(-Qi*D[None,:]/D[:,None])
    return pi,baseline,pieces


def geometric_inverse(delta,Lambda,eta):
    tmin=eta/(4*Lambda)
    tmax=math.log(4/eta)/delta
    h=eta/2
    count=int(math.ceil(math.log(tmax/tmin)/math.log1p(h)))
    grid=tmin*np.exp(np.arange(count+1)*math.log1p(h))
    grid[-1]=tmax
    return grid[:-1],np.diff(grid)


def main():
    rng=np.random.default_rng(30721)
    records=[]
    for n in (4,6,8):
        m=root.model(rng.uniform(.2,1.1,n),rng.uniform(.7,1.3,n))
        strength=.7
        pi,local0,local1=local_generators(m,strength)
        K0=sum(local0);K=sum(local1);g=np.sqrt(pi)
        lo,hi=math.exp(-strength),math.exp(strength)
        center=(lo+hi)/2;rho=(hi-lo)/(hi+lo)
        localE=[y-center*x for x,y in zip(local0,local1)]
        annihilation=max(float(np.linalg.norm(E@g)) for E in localE)
        symmetry=max(float(np.linalg.norm(E-E.T)) for E in localE)
        ev,U=eigh(K0);delta=ev[1];Lambda=ev[-1]
        R=U[:,1:]/np.sqrt(ev[1:])[None,:]
        H=R.T@K@R
        he,V=eigh(H)
        h=R[0,:]
        weights=(V.T@h)**2
        exact=float(np.sum(weights/he))
        # independent killed-generator physical-clock check
        q=-K*np.sqrt(pi)[:,None]/np.sqrt(pi)[None,:]
        t=solve(-q[1:,1:].T,np.ones(len(pi)-1))
        direct=float(pi[1:]@t/(1-pi[0]))
        assert abs(exact/(pi[0]*(1-pi[0]))/direct-1)<1e-9
        C=(H-center*np.eye(len(H)))/center
        ce,O=eigh(C)
        wh=(O.T@(h/math.sqrt(center)))**2
        series=[]
        for k in range(9):
            scalar=sum((-ce)**j for j in range(k+1))
            estimate=float(wh@scalar)
            rel=abs(estimate/exact-1)
            assert rel<=rho**(k+1)+1e-10
            series.append({'order':k,'relative_error':rel,'bound':rho**(k+1)})
        cheb=[]
        for k in range(9):
            degree=k+1
            z=(hi+lo-2*he)/(hi-lo)
            z0=(hi+lo)/(hi-lo)
            Tk=Chebyshev.basis(degree)
            relbound=1/abs(float(Tk(z0)))
            p=(1-Tk(z)/Tk(z0))/he
            estimate=float(weights@p)
            rel=abs(estimate/exact-1)
            assert rel<=relbound+1e-10
            cheb.append({'order':k,'relative_error':rel,'bound':relbound})
        eta=.05
        nodes,ww=geometric_inverse(delta,Lambda,eta)
        x=np.geomspace(delta,Lambda,2001)
        approx=np.exp(-np.outer(x,nodes))@ww
        err=float(np.max(abs(x*approx-1)))
        assert err<=eta/2+1e-12
        # A second source class: centered physical wall energy.
        states=[s for s in range(1<<n) if s.bit_count()%2==0]
        energy=np.array([sum(2*m['J'][i]*((s>>i)&1) for i in range(n)) for s in states])
        f=(energy-energy@pi)*np.sqrt(pi)
        B=m['U'].T@np.diag(2*m['J'])@m['V']
        F=B-B.T
        aa,bb=np.triu_indices(n,1)
        gaussian_variance=float(np.sum(F[aa,bb]**2))
        gaussian_chi=float(np.sum(F[aa,bb]**2/(m['eps'][aa]+m['eps'][bb])))
        exact_reference_chi=float(np.sum((U[:,1:].T@f)**2/ev[1:]))
        energy_h=R.T@f
        energy_weights=(V.T@energy_h)**2
        exact_perturbed_chi=float(np.sum(energy_weights/he))
        k=6;Tk=Chebyshev.basis(k+1)
        z=(hi+lo-2*he)/(hi-lo);z0=(hi+lo)/(hi-lo)
        energy_approx=float(energy_weights@((1-Tk(z)/Tk(z0))/he))
        energy_cheb_error=abs(energy_approx/exact_perturbed_chi-1)
        assert abs(gaussian_variance/(f@f)-1)<1e-10
        assert abs(gaussian_chi/exact_reference_chi-1)<1e-10
        assert energy_cheb_error<=1/abs(Tk(z0))+1e-10
        records.append({'n':n,'stationary_annihilation_by_every_local_E':annihilation,
                        'local_symmetry_error':symmetry,'spectral_min':float(he[0]),
                        'spectral_max':float(he[-1]),'claimed_interval':[lo,hi],
                        'reference_gap':float(delta),'gaussian_predicted_gap':m['gap'],
                        'physical_mean':direct,'neumann':series,'chebyshev':cheb,
                        'energy_source':{'variance':float(f@f),
                          'gaussian_variance':gaussian_variance,
                          'gaussian_reference_chi':gaussian_chi,
                          'dense_reference_chi':exact_reference_chi,
                          'nonGaussian_perturbed_chi':exact_perturbed_chi,
                          'degree_six_chebyshev_relative_error':energy_cheb_error,
                          'degree_six_chebyshev_bound':float(1/abs(Tk(z0)))},
                        'geometric_quadrature':{'eta':eta,'nodes':len(nodes),
                                               'max_relative_error_on_grid':err}})
        assert annihilation<1e-12 and symmetry<1e-12
        assert he[0]>=lo-1e-10 and he[-1]<=hi+1e-10
    out={'all_checks_pass':True,'qualification':'Floating point independent algebra checks, not interval arithmetic.',
         'records':records}
    target=Path(__file__).with_name('audit_gaussian_extension_results.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'all_checks_pass':True,'models':len(records),
                      'max_local_stationary_residual':max(x['stationary_annihilation_by_every_local_E'] for x in records),
                      'path':str(target)},indent=2))


if __name__=='__main__': main()
