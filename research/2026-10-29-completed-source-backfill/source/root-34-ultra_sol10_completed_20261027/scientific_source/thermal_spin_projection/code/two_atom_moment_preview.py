"""New TWO-atom signed-moment exclusion, numerical feasibility only.

For A=-J, two eigenvalue occurrences x,y require
M-x²v(x)v(x)^T-y²v(y)v(y)^T>=0, v=(1,x,x²). Earlier one-atom
Christoffel bounds did not use the leading Rayleigh constraint this way.
No exact/global optimization certification is claimed here.
"""
import json,time
import numpy as np
from scipy.optimize import minimize
from angular_spin_projection import ROOT,PRIOR

def main():
    start=time.monotonic();old=json.loads((PRIOR/'results/a5_hankel_preview.json').read_text())
    moments={int(k):(-1)**int(k)*v for k,v in old['M3_moments_scaled_by_scalar_theta'].items()}
    M=np.array([[moments[i+j+2]for j in range(3)]for i in range(3)]);inverse=np.linalg.inv(M)
    spin=json.loads((ROOT/'results/spin_projection_preview.json').read_text());spin=next(x for x in spin['rows']if x['beta']==3 and x['angle_samples']==64)
    wide=json.loads((ROOT/'results/wider_time_projection.json').read_text());row=next(x for x in wide['rows']if x['channel']=='zero_frequency'and x['span']=='wide_five_r')
    lower=max(row['cases'][0]['Ritz_minus_J'])/spin['scalar_theta'];upper=1.02
    def constraints(z):
        x,y=z;v=np.array([1.,x,x*x]);w=np.array([1.,y,y*y]);a=x*x*(v@inverse@v);b=y*y*(w@inverse@w);c=x*y*(v@inverse@w)
        return np.array([1-a,1-b,(1-a)*(1-b)-c*c,x-y])
    feasible=[]
    for x in np.linspace(lower,upper,101):
        for y in np.linspace(0,min(x,upper),161):
            if np.min(constraints((x,y)))>=0:feasible.append((x,y))
    assert feasible
    answers=[]
    for initial in sorted(feasible,key=lambda z:z[1],reverse=True)[:20]:
        r=minimize(lambda z:-z[1],initial,method='SLSQP',bounds=[(lower,upper),(0.,upper)],constraints=[{'type':'ineq','fun':constraints}],options={'ftol':1e-13,'maxiter':500})
        if r.success and min(constraints(r.x))>-1e-8:answers.append(r.x)
    assert answers
    best=max(answers,key=lambda z:z[1]);theta=spin['scalar_theta']
    result={'status':'NUMERICAL_TWO_ATOM_SIGNED_MOMENT_FEASIBILITY_ONLY',
            'leading_Rayleigh_lower_scaled':lower,'moment_matrix':M.tolist(),
            'largest_second_positive_atom_found_scaled':float(best[1]),
            'associated_first_atom_scaled':float(best[0]),
            'second_positive_bound_proposal':float(best[1]*theta),
            'first_atom_proposal':float(best[0]*theta),'PSD_slacks':constraints(best).tolist(),
            'grid_feasible_points':len(feasible),'successful_local_refinements':len(answers),
            'seconds':time.monotonic()-start,
            'scope':'Signed odd inputs correct; new rank-two moment test. A numerical feasible maximum is NOT a certified global upper or physical input.'}
    (ROOT/'results/two_atom_moment_preview.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

if __name__=='__main__':main()
