"""Independent ODE checks of the actual filtered fields with dirty initial modes."""
from pathlib import Path
import json,sys
import numpy as np
from scipy.integrate import solve_ivp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'new_research'/'conventional_routes'))
from optimize_finite_mediator import matrices
from project_initial_memory import project,simpson_weights

def check(row):
    m=row['model'];c=np.array(row['coefficients']);order=len(c)-1
    t=np.linspace(0,m['T'],24001);weights=simpson_weights(t)
    phi={k:v@c for k,v in matrices(order,t,m).items()}
    info,f,H=project(m,t,phi['A'],'ode_checked')
    rng=np.random.default_rng(70231)
    raw=rng.normal(size=3)+1j*rng.normal(size=3);raw/=np.linalg.norm(raw)
    checks=[]
    for energy in (0.,1.,10000.):
        for z1,z2 in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            # Branch-dependent initial amplitudes deliberately retain data tags.
            initial=raw*np.sqrt(energy)*np.exp(1j*(.23*z1+.71*z2))
            def rhs(tt,y):
                ff={k:(v@c).item() for k,v in matrices(order,np.array([tt]),m).items()}
                b,cc,mm=y
                return [-m['kb']/2*b-1j*m['g']*mm-1j*ff['u']*z2,
                        -(m['kc']/2+1j*m['chi']*z1)*cc-1j*m['g']*mm-1j*ff['w']*z2,
                        -m['Gamma']/2*mm-1j*m['g']*(b+cc)]
            sol=solve_ivp(rhs,[0,m['T']],initial,t_eval=t,method='DOP853',rtol=2e-12,atol=2e-13)
            observed=np.vdot(f,weights*np.sqrt(m['Gamma'])*sol.y[2])
            target=z1*z2*np.sqrt(info['N_effective'])
            # Exact zero-initial drive solution, independently checked by ODE.
            checks.append(dict(z1=z1,z2=z2,initial_energy=energy,
                               actual_signal=[observed.real,observed.imag],target=float(target),
                               absolute_signal_error=float(abs(observed-target)),
                               terminal_population=float(np.sum(abs(sol.y[:,-1])**2))))
    return dict(T=m['T'],order=order,projection=info,checks=checks,
                max_signal_error=max(x['absolute_signal_error'] for x in checks))

def main():
    source=json.loads((HERE/'memory_rejecting_optimization_results.json').read_text())
    rows=[]
    for row in source['rows']:
        if row['order']==14 and row['model']['T'] in (8.,10.,16.):
            out=check(row);rows.append(out)
            print(out['T'],out['max_signal_error'],flush=True)
    out=dict(scope='Independent finite physical ODE with branch-tagged coherent initial states. The arbitrary nonGaussian/entangled-state claim is proved by the annihilator/isometry argument, not inferred from these means.',rows=rows)
    (HERE/'memory_rejection_ode_results.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
