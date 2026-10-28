"""Bounded beta3 residual-minimization preview in the existing triplet span.

Only a numerical preview. The accepted first connected input is read-only.
All G/H/M2 entries are full physical inhomogeneous open-chain correlations.
The present script acquires no exact A5 moments or next connected input.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import pathlib,sys,json,time,hashlib
import numpy as np
import scipy.linalg as la
from scipy.optimize import minimize_scalar

ROOT=pathlib.Path(__file__).resolve().parents[1]
THERMAL=ROOT.parent
sys.path.insert(0,str(THERMAL/'code'))
from triplet_discovery import correlation_edges

def inputs(beta=3.,rs=(.2,.4,.6,.8,1.,1.2,1.4,1.6)):
    messages=[(r,d)for r in rs for d in [0,1]];mats=[]
    for shift in range(3):
        mat=np.zeros((len(messages),len(messages)))
        for i,(r,d)in enumerate(messages):
            for j,(s,e)in enumerate(messages[:i+1]):
                p=d+e+shift
                edges=(beta*r*s,)if p==0 else(beta*r,)+(beta,)*(p-1)+(beta*s,)
                mat[i,j]=mat[j,i]=(-1)**p*correlation_edges(edges)/5**p
        mats.append(mat)
    g,h,m2=mats;scale=1/np.sqrt(np.diag(g))
    normalized=[scale[:,None]*m*scale[None,:]for m in mats]
    return messages,scale,mats,normalized

def evaluate(c,g,h,m2,shift):
    # longdouble contractions cross-check cancellation in candidate readout.
    cc=np.asarray(c,dtype=np.longdouble)
    gg=np.asarray(g,dtype=np.longdouble);hh=np.asarray(h,dtype=np.longdouble);mm=np.asarray(m2,dtype=np.longdouble)
    d=cc@(gg@cc);u=cc@(hh@cc);v=cc@(mm@cc)
    ray=u/d;variance=v/d-ray*ray;residual=variance+(ray-shift)**2
    amp=float(np.sum(np.abs(cc))**2/d)
    sensitivity=amp*(float(np.max(abs(m2)))+2*abs(float(ray))*float(np.max(abs(h)))
                     +(float(ray)**2+abs(float(variance)))*float(np.max(abs(g))))
    return {'Rayleigh':float(ray),'variance':float(variance),
            'residual_squared_at_shift':float(residual),'G_norm':float(d),
            'coefficient_l1_squared_over_G_norm':amp,
            'variance_first_order_sensitivity_per_common_relative_entry_error':sensitivity,
            'common_relative_entry_error_for_2e6_variance_error':2e6/sensitivity,
            'candidate_coefficients_normalized_message_basis':list(map(float,c))}

def count_inputs():
    a5path=THERMAL/'results/a5_preview.json'
    a5=json.loads(a5path.read_text());a5=next(r for r in a5['rows']if r['beta']==3.)
    return a5path,a5

def count(candidate,ritz,a5):
    """All assigned Ritz modes counted by sign/minmax; no free deflation.

    M6-sum|mu|6 bounds unassigned eigenvalues only. For each assigned
    non-target mode, its upper is (R+|mu|6)^(1/6). Temple needs the
    second-largest signed A eigenvalue, not the largest negative modulus.
    """
    M=a5['moments']['6']['3'];thetaI=a5['scalar_theta'];mu=max(ritz)
    rem=M-sum(abs(x)**6 for x in ritz)
    assert rem>0
    other=[x for x in ritz if x!=mu]
    positive_other=max([x for x in other if x>0]+[0.])
    modulus_other=max([abs(x)for x in other]+[0.])
    rest_signed=(rem+positive_other**6)**(1/6)
    rest_modulus=(rem+modulus_other**6)**(1/6)
    moment_cap=(rem+mu**6)**(1/6)
    ray=candidate['Rayleigh'];var=candidate['variance']
    temple=ray+var/(ray-rest_signed)if ray>rest_signed and var>=0 else None
    top_upper=min(moment_cap,temple)if temple is not None else moment_cap
    # Full I/O and other A5-list masses, retaining all non-target modes.
    tau=0.
    dims={'1':1,'3prime':3,'4':4,'5':5}
    for ir,dim in dims.items():tau+=dim*a5['radius_over_theta'][ir]**256
    tau+=3*(top_upper/thetaI)**256
    # Every other triplet mode, including the assigned non-target Ritz modes.
    rest_mass=M-mu**6
    tau+=3*(rest_mass/thetaI**6)*(rest_modulus/thetaI)**250
    return {'A5_M3_6_numerical':M,'max_Ritz_lower':mu,
            'unassigned_sixth_mass':rem,'unassigned_modulus_bound_proposal':rem**(1/6),
            'all_other_positive_spectrum_upper_proposal':rest_signed,
            'all_other_moduli_upper_proposal':rest_modulus,
            'target_sixth_moment_upper_proposal':moment_cap,
            'Temple_target_upper_proposal':temple,'combined_target_upper_proposal':top_upper,
            'target_upper_over_scalar_lower':top_upper/thetaI,
            'all_mode_relative_loop_tail_proposal':tau,
            'scalar_lower_numerical':thetaI,
            'scope':'All values depend on unacquired numerical A5 moments and float64 matrices.'}

def main():
    start=time.monotonic();messages,scale,raw,normalized=inputs()
    g,h,m2=normalized
    np.savez(ROOT/'results/triplet_matrices_beta3.npz',G=raw[0],H=raw[1],M2=raw[2],
             G_normalized=g,H_normalized=h,M2_normalized=m2,normalizing_scale=scale,
             messages=np.array(messages))
    vals,vecs=la.eigh(g);a5path,a5=count_inputs();rows=[]
    for cutoff in [1e-6,1e-8,1e-10,1e-12]:
        keep=vals>cutoff*vals[-1];q=vecs[:,keep]/np.sqrt(vals[keep])
        gp=q.T@g@q;hp=q.T@h@q;mp=q.T@m2@q
        ge=la.eigvalsh(gp);whitening_error=float(la.norm(gp-np.eye(sum(keep)),2))
        re,ru=la.eigh(hp,gp);baseline=evaluate(q@ru[:,-1],g,h,m2,float(re[-1]))
        baseline.update(count(baseline,re.tolist(),a5))
        scanned=[]
        def at(shift):
            residual=mp-2*shift*hp+shift**2*gp
            residual=(residual+residual.T)/2
            es,us=la.eigh(residual,gp)
            c=q@us[:,0]
            item=evaluate(c,g,h,m2,shift)
            item.update({'prescribed_shift':float(shift),
                         'smallest_GEP_residual_eigenvalue':float(es[0]),
                         'GEP_vs_direct_longdouble_difference':item['residual_squared_at_shift']-float(es[0])})
            item.update(count(item,re.tolist(),a5))
            return item
        for shift in np.linspace(294000.,315000.,85):scanned.append(at(float(shift)))
        # A bounded adaptive check refines the best variance, without enlarging
        # the prescribed shift interval or changing the message span.
        opt=minimize_scalar(lambda x:at(float(x))['variance'],bounds=(294000.,315000.),method='bounded',options={'xatol':.01,'maxiter':80})
        scanned.append(at(float(opt.x)))
        bestvar=min(scanned,key=lambda x:x['variance'])
        bestloop=min(scanned,key=lambda x:x['all_mode_relative_loop_tail_proposal'])
        rows.append({'Gram_cutoff_relative':cutoff,'retained_rank':int(sum(keep)),
                     'retained_Gram_condition_number':float(vals[-1]/vals[keep][0]),
                     'whitened_G_eigenvalues':ge.tolist(),'whitening_operator_error':whitening_error,
                     'baseline_max_Rayleigh':baseline,'best_variance':bestvar,
                     'best_loop_count':bestloop,'scan':scanned})
        print({'cutoff':cutoff,'rank':int(sum(keep)),
               'baseline_variance':baseline['variance'],'minres_shift':bestvar['prescribed_shift'],
               'minres_Rayleigh':bestvar['Rayleigh'],'minres_variance':bestvar['variance'],
               'best_loop_target_upper':bestloop['combined_target_upper_proposal'],
               'best_loop_relative_tail':bestloop['all_mode_relative_loop_tail_proposal']},flush=True)
    source_paths=[a5path,THERMAL/'code/triplet_discovery.py',THERMAL/'code/fugacity_messages.py']
    result={'status':'BOUNDED_MINIMUM_RESIDUAL_PREVIEW_ONLY','beta':3.,'messages':messages,
            'prescribed_shift_range':[294000.,315000.],'Gram_eigenvalues_normalized':vals.tolist(),
            'normalized_matrix_max_abs':dict(zip(['G','H','M2'],[float(np.max(abs(x)))for x in normalized])),
            'rows':rows,'seconds':time.monotonic()-start,
            'input_receipts':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in source_paths],
            'new_exact_acquisition':False,'next_connected_input_acquired':False,
            'arithmetic_scope':'float64 source traces/GEP; candidate contractions additionally read in longdouble; no verified trace/roundoff enclosure.'}
    (ROOT/'results/minres_scan.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
