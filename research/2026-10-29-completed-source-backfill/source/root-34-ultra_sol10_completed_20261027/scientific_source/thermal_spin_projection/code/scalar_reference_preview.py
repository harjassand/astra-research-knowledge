"""Same-information scalar comparison and a real scalar eigenvalue interval.

Uses an existing ordinary scalar fugacity family at beta3, plus the NEW full
spin0 sixth moment. Numerical only; reads the frozen sol9 source code.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
import sys,json,time
import numpy as np
import scipy.linalg as la
from angular_spin_projection import ROOT,PRIOR
sys.path.insert(0,str(PRIOR/'code'))
from fugacity_messages import entries

def main():
    start=time.monotonic();beta=3.;messages=[(r,3*a)for r in [.6,.8,1.,1.2,1.4]for a in [0.,.5,1.,1.5,2.]]
    g,h,m2=entries(beta,messages);h/=5;m2/=25
    sc=1/np.sqrt(np.diag(g));g,h,m2=[sc[:,None]*a*sc[None,:]for a in [g,h,m2]]
    vals,vecs=la.eigh(g);source=json.loads((ROOT/'results/spin_projection_preview.json').read_text());source=next(x for x in source['rows']if x['beta']==3 and x['angle_samples']==64)
    M=source['spin_list_sixth_moments_preview'][0];rows=[]
    for cut in [1e-6,1e-8,1e-10,1e-12]:
        keep=vals>cut*vals[-1];q=vecs[:,keep]/np.sqrt(vals[keep]);gp=q.T@g@q;hp=q.T@h@q;mp=q.T@m2@q
        es,us=la.eigh(hp,gp);ritz=es.tolist();lower=max(ritz);R=M-sum(abs(x)**6 for x in ritz);assert R>0
        other=[x for x in ritz if x!=lower];alpha=(R+max([x for x in other if x>0]+[0.])**6)**(1/6)
        rho=(R+max([abs(x)for x in other]+[0.])**6)**(1/6);cap=(R+lower**6)**(1/6)
        def read(c,t):
            d=c@g@c;r=float(c@h@c/d);v=float(c@m2@c/d-r*r);temple=r+v/(r-alpha)if r>alpha and v>=0 else None
            return {'Rayleigh':r,'variance':v,'prescribed_shift':t,'Temple_upper':temple,
                    'combined_scalar_upper':min(cap,temple)if temple is not None else cap,
                    'coefficient_l1_squared_over_G_norm':float(np.sum(abs(c))**2/d)}
        baseline=read(q@us[:,-1],None);scan=[]
        for t in np.linspace(lower*.98,cap*1.02,61):
            ee,uu=la.eigh(mp-2*t*hp+t*t*gp,gp);scan.append(read(q@uu[:,0],float(t)))
        best=min(scan+[baseline],key=lambda x:x['combined_scalar_upper'])
        row={'Gram_cutoff':cut,'retained_rank':int(sum(keep)),
             'retained_Gram_condition':float(vals[-1]/vals[keep][0]),'Ritz_J':ritz,
             'spin0_M6':M,'unassigned_moment6':R,'rest_positive_upper':alpha,'rest_modulus_upper':rho,
             'scalar_lower':lower,'moment_scalar_upper':cap,'max_Rayleigh':baseline,'best_upper':best}
        rows.append(row);print('scalar',cut,'rank',sum(keep),'interval',lower,best['combined_scalar_upper'],'variance',baseline['variance'],flush=True)
    (ROOT/'results/scalar_reference_preview.json').write_text(json.dumps({'status':'NUMERICAL_SAME_INFORMATION_SCALAR_REFERENCE_AND_UPPER',
        'beta':3,'messages':messages,'normalized_Gram_eigenvalues':vals.tolist(),'rows':rows,
        'seconds':time.monotonic()-start,'new_exact_acquisition':False,
        'scope':'Ordinary scalar message comparator. Real spin0 moment upper and deflated tails retained; no verified physical source enclosure.'},indent=2)+'\n')

if __name__=='__main__':main()
