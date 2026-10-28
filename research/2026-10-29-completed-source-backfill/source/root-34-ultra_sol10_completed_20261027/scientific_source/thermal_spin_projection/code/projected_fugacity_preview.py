"""Bounded three-fugacity test AFTER zero-time-frequency projection.

This is a new projected message space, not a repeat of the old16 vectors.
Only numerical all-state Kubo correlations are evaluated; no exact data job.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
import pathlib,json,itertools,math,time,functools
import numpy as np
import scipy.linalg as la
from angular_spin_projection import ROOT

@functools.lru_cache(None)
def open_bonds(n,mag):
    states=[w for w in itertools.product(range(-2,3),repeat=n)if sum(w)==mag]
    lookup={w:i for i,w in enumerate(states)}
    bonds=[np.zeros((len(states),len(states)))for _ in range(n-1)]
    for col,w in enumerate(states):
        for edge in range(n-1):
            bonds[edge][col,col]=w[edge]*w[edge+1]
            for step in [-1,1]:
                a=w[edge];b=w[edge+1]
                if not(-2<=a+step<=2 and -2<=b-step<=2):continue
                v=list(w);v[edge]+=step;v[edge+1]-=step
                product=(6-a*(a+step))*(6-b*(b-step))//4
                bonds[edge][lookup[tuple(v)],col]=np.sqrt(product)
    return states,bonds

CACHE={}
def correlation(edges):
    edges=tuple(edges)
    reverse=tuple(reversed(edges))
    key=min(edges,reverse)
    if key in CACHE:return CACHE[key]
    n=len(edges)+1;total=0.
    for mag in range(2*n+1):
        states,bonds=open_bonds(n,mag)
        if not states:continue
        h=sum(a*b for a,b in zip(edges,bonds))
        es,us=la.eigh(h,check_finite=False,overwrite_a=True)
        left=np.array([w[0]for w in states]);right=np.array([w[-1]for w in states])
        l=us.T@(left[:,None]*us);r=us.T@(right[:,None]*us)
        t=(es[:,None]-es[None,:])/2
        sinhc=np.ones_like(t);mask=np.abs(t)>1e-7;sinhc[mask]=np.sinh(t[mask])/t[mask]
        sinhc[~mask]=1+t[~mask]**2/6+t[~mask]**4/120
        kernel=np.exp(-(es[:,None]+es[None,:])/2)*sinhc
        total-=(1 if mag==0 else 2)*float(np.sum(l*r.T*kernel))
    CACHE[key]=total
    print('Kubo edges',edges,'value',total,flush=True)
    return total

def entries(beta=3.,rs=(.6,1.,1.4)):
    messages=[(r,d)for r in rs for d in [0,1]];mats=[]
    for shift in range(3):
        a=np.zeros((len(messages),len(messages)))
        for i,(r,d)in enumerate(messages):
            for j,(s,e)in enumerate(messages[:i+1]):
                p=d+e+shift
                edges=(beta*r*s,)if p==0 else(beta*r,)+(beta,)*(p-1)+(beta*s,)
                a[i,j]=a[j,i]=(-1)**p*correlation(edges)/5**p
        mats.append(a)
    return messages,mats

def all_mode_count(ray,var,ritz,source,a5):
    M=source['spin1_M6'];theta=source['scalar_theta'];mu=max(ritz)
    residue=M-sum(abs(x)**6 for x in ritz)
    assert residue>0
    other=[x for x in ritz if x!=mu]
    alph=(residue+max([x for x in other if x>0]+[0.])**6)**(1/6)
    rho=(residue+max([abs(x)for x in other]+[0.])**6)**(1/6)
    cap=(residue+mu**6)**(1/6)
    temple=ray+var/(ray-alph)if ray>alph and var>=0 else None
    upper=min(cap,temple)if temple is not None else cap
    tau=sum(dim*a5['radius_over_theta'][ir]**256 for ir,dim in [('1',1),('3prime',3),('4',4),('5',5)])
    tau+=3*source['complement_radius_over_scalar_lower']**256
    tau+=3*(upper/theta)**256+3*((M-mu**6)/theta**6)*(rho/theta)**250
    return {'spin1_moment_residual':residue,'target_Ritz_lower':mu,
            'rest_positive_upper':alph,'rest_modulus_upper':rho,
            'moment_target_upper':cap,'Temple_upper':temple,'combined_target_upper':upper,
            'upper_over_scalar_lower':upper/theta,'all_mode_loop_tail_proposal':tau}

def main():
    start=time.monotonic();old=json.loads((ROOT/'results/static_time_message_preview.json').read_text())
    uniform=next(x for x in old['rows']if x['beta']==3.)
    for x in uniform['chains']:CACHE[(3.,)*(x['n']-1)]=x['integrated_minus_SzSz']
    messages,mats=entries();g,h,m2=mats;scale=1/np.sqrt(np.diag(g))
    normalized=[scale[:,None]*x*scale[None,:]for x in mats];g,h,m2=normalized
    np.savez(ROOT/'results/projected_fugacity_matrices.npz',G=g,H=h,M2=m2,messages=np.array(messages),scale=scale)
    es,us=la.eigh(g);source=json.loads((ROOT/'results/spin_projection_preview.json').read_text())
    source=next(x for x in source['rows']if x['beta']==3. and x['angle_samples']==64)
    a5=json.loads((ROOT.parents[1]/'sol9_frontier_20261028/thermal/results/a5_preview.json').read_text())
    a5=next(x for x in a5['rows']if x['beta']==3.);rows=[]
    for cut in [1e-6,1e-8,1e-10,1e-12]:
        keep=es>cut*es[-1];q=us[:,keep]/np.sqrt(es[keep]);gp=q.T@g@q;hp=q.T@h@q;mp=q.T@m2@q
        ee,vv=la.eigh(hp,gp);ritz=ee.tolist()
        def read(c,shift):
            den=c@g@c;r=float(c@h@c/den);v=float(c@m2@c/den-r*r)
            return {'Rayleigh':r,'variance':v,'prescribed_shift':shift,
                    'coefficients_normalized_basis':c.tolist(),**all_mode_count(r,v,ritz,source,a5)}
        baseline=read(q@vv[:,-1],None);scan=[]
        for shift in np.linspace(300000.,330000.,61):
            e,u=la.eigh(mp-2*shift*hp+shift**2*gp,gp)
            scan.append(read(q@u[:,0],float(shift)))
        row={'Gram_cutoff':cut,'retained_rank':int(sum(keep)),
             'retained_Gram_condition':float(es[-1]/es[keep][0]),'Ritz_minus_J':ritz,
             'max_Rayleigh':baseline,'best_variance':min(scan,key=lambda x:x['variance']),
             'best_loop':min(scan+[baseline],key=lambda x:x['all_mode_loop_tail_proposal']),
             'scan':scan}
        rows.append(row);print('SUMMARY',cut,baseline,'BEST_LOOP',row['best_loop'],flush=True)
    result={'status':'THREE_FUGACITY_ZERO_FREQUENCY_MESSAGE_NUMERICAL_PREVIEW',
            'messages':messages,'normalized_Gram_eigenvalues':es.tolist(),'rows':rows,
            'seconds':time.monotonic()-start,'inhomogeneous_Kubo_trace_count':len(CACHE),
            'new_exact_acquisition':False,'next_connected_input_acquired':False,
            'scope':'New P0-projected messages, all physical states in each numerical Kubo trace; no verified source/field/roundoff enclosures.'}
    (ROOT/'results/projected_fugacity_preview.json').write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'results/projected_fugacity_Kubo_inputs.json').write_text(json.dumps({','.join(map(str,k)):v for k,v in CACHE.items()},indent=2)+'\n')

if __name__=='__main__':main()
