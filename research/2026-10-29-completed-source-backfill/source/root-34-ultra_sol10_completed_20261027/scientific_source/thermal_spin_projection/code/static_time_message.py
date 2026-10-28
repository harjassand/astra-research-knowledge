"""NEW zero-imaginary-time-frequency boundary-message preview.

The history transfer commutes with circle translations. Averaging a boundary
spin insertion in imaginary time projects its trial message to frequency0.
Its moments are integrated physical endpoint (Kubo) correlations, not the
equal-time correlations of the old fugacity/minres span.

Numerical preview only; no physical trace/residual enclosure is acquired.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
import pathlib,json,time
import numpy as np
import scipy.linalg as la
from scipy.optimize import minimize_scalar
from angular_spin_projection import ROOT,PRIOR,sector_parts

def integrated_end_correlation(n,beta):
    static=0.;equal=0.;Z=0.;rows=[]
    for mag in range(2*n+1):
        states,parts=sector_parts(n,mag)
        if not states:continue
        d0,d1,e0,e1=parts
        h=(d0+np.sqrt(6)*d1).toarray()
        left=np.array([w[0]for w in states],dtype=float);right=np.array([w[-1]for w in states],dtype=float)
        h[np.diag_indices_from(h)]-=left*right
        es,us=la.eigh(h,check_finite=False,overwrite_a=True)
        weights=np.exp(-beta*es)
        l=us.T@(left[:,None]*us);r=us.T@(right[:,None]*us)
        t=beta*(es[:,None]-es[None,:])/2
        sinhc=np.ones_like(t);mask=np.abs(t)>1e-7
        sinhc[mask]=np.sinh(t[mask])/t[mask]
        sinhc[~mask]=1+t[~mask]**2/6+t[~mask]**4/120
        kernel=np.exp(-beta*(es[:,None]+es[None,:])/2)*sinhc
        block_static=-float(np.sum(l*r.T*kernel))
        diagonal=np.sum(us**2*(left*right)[:,None],axis=0)
        block_equal=-float(np.dot(diagonal,weights))
        mult=1 if mag==0 else 2
        static+=mult*block_static;equal+=mult*block_equal;Z+=mult*float(np.sum(weights))
        # Arithmetic cross-check of the endpoint-sum transformed diagonal.
        # This is not an independent Kubo normalization certificate.
        rows.append({'M':mag,'dimension':len(states),'multiplicity':mult,
                     'kernel_symmetry_max':float(np.max(abs(kernel-kernel.T))),
                     'endpoint_operator_diagonal_sum_error':float(np.max(abs(np.diag(l+r)-np.sum(us**2*(left+right)[:,None],axis=0))))})
    return {'n':n,'beta':beta,'integrated_minus_SzSz':static,
            'equal_time_minus_SzSz':equal,'partition_trace':Z,'sectors':rows}

def message_metrics(moments,center=None):
    # A=-J: projected spin1 mode is on the AF branch.
    m=np.array([(-1)**r*x for r,x in enumerate(moments)])
    g=np.array([[m[i+j]for j in range(2)]for i in range(2)])
    h=np.array([[m[i+j+1]for j in range(2)]for i in range(2)])
    m2=np.array([[m[i+j+2]for j in range(2)]for i in range(2)])
    e,u=la.eigh(h,g);c=u[:,-1]
    def read(c,shift=None):
        den=c@g@c;r=c@h@c/den;v=c@m2@c/den-r*r
        return {'Rayleigh':float(r),'variance':float(v),'coefficients':(c/max(abs(c))).tolist(),
                'prescribed_shift':shift}
    baseline=read(c);scan=[]
    if center is None:center=baseline['Rayleigh']
    for shift in np.linspace(.95*center,1.05*center,41):
        val,vec=la.eigh(m2-2*shift*h+shift*shift*g,g)
        scan.append(read(vec[:,0],float(shift)))
    return {'G':g.tolist(),'H':h.tolist(),'M2':m2.tolist(),
            'Gram_eigenvalues':la.eigvalsh(g).tolist(),
            'max_Rayleigh':baseline,'minimum_variance_scan':min(scan,key=lambda x:x['variance']),
            'scan':scan}

def main():
    start=time.monotonic();results=[]
    for beta in [1.5,3.]:
        chains=[]
        for n in range(2,7):
            row=integrated_end_correlation(n,beta);chains.append(row)
            print('beta',beta,'n',n,'static',row['integrated_minus_SzSz'],'equal',row['equal_time_minus_SzSz'],'seconds',time.monotonic()-start,flush=True)
        static_m=[r['integrated_minus_SzSz']/5**(r['n']-2)for r in chains]
        equal_m=[r['equal_time_minus_SzSz']/5**(r['n']-2)for r in chains]
        item={'beta':beta,'chains':chains,'static_projected_moments':static_m,
              'equal_time_moments':equal_m,'zero_frequency_trial':message_metrics(static_m),
              'equal_time_trial_control':message_metrics(equal_m),
              'scope':'NEW_TIME_AVERAGED_SOURCE_MESSAGE_NUMERICAL_PREVIEW_ONLY'}
        results.append(item)
        print('trial',beta,item['zero_frequency_trial']['max_Rayleigh'],flush=True)
    data={'status':'ZERO_TIME_FREQUENCY_BOUNDARY_MESSAGE_PREVIEW','rows':results,
          'seconds':time.monotonic()-start,'new_exact_acquisition':False,
          'next_connected_input_acquired':False,
          'interface':'<P0 f,J^r P0 f>=-1/(beta*5^r) integral_0^beta Tr[SzL exp(-tH) SzR exp(-(beta-t)H)]dt on open r+2 sites.',
          'source_scope':'All physical M sectors, full Hermitian eigenvectors. Float64 divided differences and matrix products; not validated physical enclosures.'}
    (ROOT/'results/static_time_message_preview.json').write_text(json.dumps(data,indent=2)+'\n')

if __name__=='__main__':main()
