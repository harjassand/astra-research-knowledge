"""Checks of the explicit ordinary-mechanical staircase; no empirical data.

The theorem is analytic. Numerical calculations verify the finite-stiffness
leading coefficient and the angular-error Schur complement. mpmath prevents
the cancellation and underflow that an exponentially flat example creates.
"""
from pathlib import Path
import json
import time
import mpmath as mp

mp.mp.dps = 220
HERE = Path(__file__).resolve().parent
start = time.perf_counter()

def F(q, ell=mp.mpf(1)):
    return q*q / (ell + mp.sqrt(ell*ell-q*q))

def rigid_chain(x, n):
    q = [mp.mpf(x)]
    for _ in range(n):
        q.append(F(q[-1]))
    return q

def finite_equilibrium(x, n, K=None, k=mp.mpf(1)):
    x=mp.mpf(x)
    K=[mp.mpf(1)]*n if K is None else list(map(mp.mpf,K))
    k=mp.mpf(k)
    scale=[x**(2**j)/mp.mpf(2)**(2**j-1) for j in range(1,n+1)]
    guess=[mp.mpf(1)]*(n-1)+[K[-1]/(K[-1]+k)]
    def gradient(*ys):
        q=[x]+[y*s for y,s in zip(ys,scale)]
        rr=[mp.sqrt(q[i]**2+(1-q[i+1])**2) for i in range(n)]
        # Algebraically equivalent to rr-1, avoiding catastrophic cancellation.
        ss=[(q[i]**2-2*q[i+1]+q[i+1]**2)/(rr[i]+1) for i in range(n)]
        g=[]
        for j in range(1,n+1):
            z=K[j-1]*ss[j-1]*(q[j]-1)/rr[j-1]
            if j<n:
                z+=K[j]*ss[j]*q[j]/rr[j]
            else:
                z+=k*q[j]
            g.append(z/scale[j-1])
        return tuple(g)
    ys=mp.findroot(gradient, tuple(guess), tol=mp.mpf('1e-180'),
                   maxsteps=80, solver='mdnewton')
    q=[x]+[ys[j]*scale[j] for j in range(n)]
    rr=[mp.sqrt(q[i]**2+(1-q[i+1])**2) for i in range(n)]
    ss=[(q[i]**2-2*q[i+1]+q[i+1]**2)/(rr[i]+1) for i in range(n)]
    U=sum(K[i]*ss[i]**2/2 for i in range(n))+k*q[n]**2/2
    keff=K[-1]*k/(K[-1]+k)
    lead=keff/2*x**(2**(n+1))/mp.mpf(2)**(2**(n+1)-2)
    return {'n':n,'input':str(x),'q':[mp.nstr(z,25) for z in q],
            'energy':mp.nstr(U,25),'leading_energy':mp.nstr(lead,25),
            'energy_over_leading':mp.nstr(U/lead,25),
            'normalized_stationarity_residual':mp.nstr(max(abs(z) for z in gradient(*ys)),8)}

rows=[]
for n in range(1,6):
    for x in ['0.2','0.1','0.05']:
        rows.append(finite_equilibrium(x,n))

rigid=[]
for n in range(1,9):
    q=rigid_chain('0.2',n)
    # Last-stage angular derivative d log(q_n)/d delta_(n-1).
    sens=q[-2]/q[-1]
    eps=mp.mpf('0.01')
    linearized_tolerance=eps/sens
    r=mp.mpf('0.2');d=1+mp.sqrt(1-r*r);i=n-1
    lower=(r/2)**(2**i)
    upper=(d/2)*(r/d)**(2**i)
    assert lower <= q[-2]/2 <= upper
    rigid.append({'n':n,'work_order':2**(n+1),
                  'terminal_displacement':mp.nstr(q[-1],20),
                  'last_angular_log_output_sensitivity':mp.nstr(sens,20),
                  'linearized_1_percent_tolerance':mp.nstr(linearized_tolerance,20),
                  'tolerance_bits':mp.nstr(-mp.log(linearized_tolerance,2),15)})

angular=[]
for n in [1,2,3,5,8]:
    K=[mp.mpf(1)+mp.mpf(j)/3 for j in range(n)]
    k=mp.mpf(2)
    ds=[mp.mpf('0.02')+mp.mpf(j)/1000 for j in range(n)]
    A=mp.fprod(ds)
    Bs=[mp.fprod(ds[j+1:]) for j in range(n)]
    formula=A*A/(1/k+sum(B*B/KK for B,KK in zip(Bs,K)))
    # Independent quadratic Hessian and Schur complement in all coordinates.
    H=mp.matrix(n+1)
    for j in range(n):
        H[j,j]+=K[j]*ds[j]**2
        H[j,j+1]-=K[j]*ds[j]
        H[j+1,j]-=K[j]*ds[j]
        H[j+1,j+1]+=K[j]
    H[n,n]+=k
    Hi=H[1:,1:];v=H[1:,0]
    schur=H[0,0]-(v.T*mp.lu_solve(Hi,v))[0]
    relative=abs(schur/formula-1)
    assert relative < mp.mpf('1e-170')
    angular.append({'n':n,'quadratic_boundary_stiffness':mp.nstr(formula,25),
                    'relative_formula_check':mp.nstr(relative,8)})

out={'scope':'Synthetic verification of an explicit ordinary mechanical model, not experimental evidence',
     'precision_decimal_digits':mp.mp.dps,'finite_stiffness_checks':rows,
     'rigid_precision_cost':rigid,'angular_schur_checks':angular,
     'wall_seconds':time.perf_counter()-start,
     'physical_experiments':0,'physical_devices_prepared':0}
(HERE/'staircase_checks.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'rows':len(rows),'last_finite_check':rows[-1],
                  'rigid_precision_cost':rigid,'angular_schur_checks':angular,
                  'wall_seconds':out['wall_seconds']},indent=2))
