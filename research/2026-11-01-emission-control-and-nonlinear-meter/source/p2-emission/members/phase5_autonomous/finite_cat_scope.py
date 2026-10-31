"""Localization diagnostics; neither a full tail nor a nonlinear error proof."""
from pathlib import Path
import json,sys
import numpy as np
from scipy.special import eval_genlaguerre,gammaln
from nonlinear_mean_model import Model,classical_trajectory,trajectory_at


def displaced_overlap(alpha,cutoff):
    beta=-2*complex(alpha);x=abs(beta)**2;out=np.zeros((cutoff,cutoff),complex)
    for k in range(cutoff):
        for l in range(cutoff):
            if k>=l:v=np.exp(-x/2+.5*(gammaln(l+1)-gammaln(k+1)))*beta**(k-l)*eval_genlaguerre(l,k-l,x)
            else:v=np.exp(-x/2+.5*(gammaln(k+1)-gammaln(l+1)))*(-beta.conjugate())**(l-k)*eval_genlaguerre(k,l-k,x)
            out[k,l]=v*(-1)**l
    s=float(np.linalg.svd(out,compute_uv=False)[0])
    return {'max_overlap_singular_value':s,'local_Gram_condition_number':(1+s)/(1-s)}


def gaussian_number_probabilities(mean,V,N=128,r=.8,count=20):
    z=r*np.exp(2j*np.pi*np.arange(N)/N)
    M=(1-z)[:,None,None]*V+(1+z)[:,None,None]*np.eye(2)/2
    inv=np.linalg.inv(M)
    f=np.exp(-.5*(1-z)*np.einsum('i,nij,j->n',mean,inv,mean))/np.sqrt(np.linalg.det(M))
    p=(np.fft.fft(f)/N)[:count]/r**np.arange(count)
    return p.real


def main():
    root=Path(__file__).parent;m=Model(modulated=True,odd=.0001,cycles=16,steps_per_segment=32)
    ts,aa=classical_trajectory(m)
    zs=np.array([[1.,1.,1.],[1.,1.,-1.]])
    tc,ac=classical_trajectory(m,z=zs,include_parasitics=False,include_odd=False)
    minradius=float(abs(aa[:,:,:3]).min())
    snapshots=json.loads((root/'joint_nonlinear_mean_mod_moments.json').read_text())['snapshots']
    cutoffs=(3,4,6,8);tails={str(k):0. for k in cutoffs};buffer_tail2=0.;buffer_tail3=0.
    for snap in snapshots:
        t=snap['time'];mean=np.array(snap['mean']);V=np.array(snap['covariance'])
        ref=trajectory_at(tc,ac,t)
        for zidx in range(8):
            common=ref[0 if m.S[zidx]>0 else 1]-np.r_[np.full(3,m.alpha),np.zeros(3)]
            commonvec=np.zeros(12);commonvec[::2]=np.sqrt(2)*common.real;commonvec[1::2]=np.sqrt(2)*common.imag
            for j in range(6):
                ps=gaussian_number_probabilities((mean[zidx]-commonvec)[2*j:2*j+2],V[zidx,2*j:2*j+2,2*j:2*j+2])
                if j<3:
                    for k in cutoffs:tails[str(k)]=max(tails[str(k)],float(1-ps[:k].sum()))
                else:
                    buffer_tail2=max(buffer_tail2,float(1-ps[:2].sum()))
                    buffer_tail3=max(buffer_tail3,float(1-ps[:3].sum()))
    out={'minimum_classical_branch_radius':minradius,
         'local_cat_basis_overlap_at_minimum_radius':{str(k):displaced_overlap(minradius,k) for k in cutoffs},
         'max_snapshot_Gaussian_storage_probability_at_or_above_cutoff_in_common_frame':tails,
         'max_snapshot_Gaussian_buffer_probability_at_or_above2_in_common_frame':buffer_tail2,
         'max_snapshot_Gaussian_buffer_probability_at_or_above3_in_common_frame':buffer_tail3,
         'qualification':'Finite snapshot Gaussian tail estimates and finite local Gram conditioning. They are not full nonlinear continuous-time cutoff certificates.'}
    (root/'finite_cat_scope_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
