"""Rebuild signed A5 odd moments with the new literal physical constructor.

The odd-history closure proof is in ODD_CLOSURE_AND_TIME_PROJECTION.md.
This numerical control independently checks the earlier p3/p5 numbers and
signs. It does not rerun a new moment-filter search or certify physical traces.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
import json,time,math
import numpy as np
import scipy.linalg as la
from angular_spin_projection import ROOT,PRIOR,sector_parts

def triplet_project(z):
    golden=(1+np.sqrt(5))/2;conjugate=(1-np.sqrt(5))/2
    return (3*z[0]-15*z[1]+12*golden*z[3]+12*conjugate*z[4])/60

def traces(n,beta):
    angles=[0.,np.pi,2*np.pi/3,2*np.pi/5,4*np.pi/5];out=np.zeros(5);untwisted=[]
    for mag in range(2*n+1):
        states,parts=sector_parts(n,mag)
        if not states:continue
        d0,d1,e0,e1=parts;d=(d0+np.sqrt(6)*d1).toarray();e=(e0+np.sqrt(6)*e1).toarray()
        for j,phi in enumerate(angles):
            z=np.exp(1j*phi);h=d+z*e+z.conjugate()*e.T
            vals=la.eigvalsh(h,check_finite=False,overwrite_a=True)
            out[j]+=(1 if mag==0 else 2)*np.sum(np.exp(-beta*vals))/5**n
            if j==0:untwisted.extend(vals.tolist()*(1 if mag==0 else 2))
    if n==3:
        analytic=[]
        for total in range(7):
            multiplicity=sum(abs(pair-2)<=total<=pair+2 for pair in range(5))
            analytic.extend([(total*(total+1)-18)/2]*((2*total+1)*multiplicity))
        assert len(analytic)==125
        assert np.max(abs(np.sort(untwisted)-np.sort(analytic)))<1e-11
    return out

def main():
    start=time.monotonic();prior=json.loads((PRIOR/'results/a5_hankel_preview.json').read_text())
    theta=next(x for x in json.loads((PRIOR/'results/a5_preview.json').read_text())['rows']if x['beta']==3.)['scalar_theta']
    rows=[]
    for n in [2,3,5]:
        z=traces(n,3.);moment=float(triplet_project(z));scaled=moment/theta**n
        old=prior['M3_moments_scaled_by_scalar_theta'][str(n)]
        if n in [3,5]:assert moment<0
        assert abs(scaled-old)/max(1,abs(old))<1e-11
        rows.append({'p':n,'all_physical_states':5**n,'five_angle_traces_normalized':z.tolist(),
                     'actual_signed_A5_triplet_moment_preview':moment,
                     'moment_over_scalar_theta_power':scaled,'earlier_value':old,
                     'scaled_absolute_difference':abs(scaled-old)})
    result={'status':'PASS_NUMERICAL_ODD_SIGN_AND_SOURCE_REBUILD_CONTROL','rows':rows,
            'beta':3,'seconds':time.monotonic()-start,
            'odd_closure_identity':'Tr(J_beta^p U_g)=Tr_phys exp(-beta H_p(g))/5^p for p>=3; no reflection or cycle-parity correction.',
            'signed_odd_values_retained_in_previous_Hankel':True,
            'new_filter_search_performed':False,'physical_traces_certified':False}
    (ROOT/'results/odd_moment_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
