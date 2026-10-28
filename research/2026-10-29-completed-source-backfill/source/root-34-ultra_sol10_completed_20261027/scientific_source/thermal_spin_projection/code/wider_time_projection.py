"""One nested wider P0 span, with an unchanged matched equal-time span.

Both use r=.2,.6,1,1.4,1.8 and d=0,1. Kubo and equal-time correlations are
read from the SAME full physical eigensystems. Numerical preview only.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
import json,time
import numpy as np
import scipy.linalg as la
from projected_fugacity_preview import ROOT,open_bonds,all_mode_count

CACHE={}
def pair_correlations(edges):
    edges=tuple(edges);key=min(edges,tuple(reversed(edges)))
    if key in CACHE:return CACHE[key]
    n=len(edges)+1;static=0.;equal=0.
    for mag in range(2*n+1):
        states,bonds=open_bonds(n,mag)
        if not states:continue
        h=sum(x*b for x,b in zip(edges,bonds));es,us=la.eigh(h,check_finite=False,overwrite_a=True)
        left=np.array([w[0]for w in states]);right=np.array([w[-1]for w in states])
        weights=np.exp(-es);mult=1 if mag==0 else 2
        equal-=mult*float(np.dot(np.sum(us**2*(left*right)[:,None],axis=0),weights))
        l=us.T@(left[:,None]*us);r=us.T@(right[:,None]*us)
        t=(es[:,None]-es[None,:])/2;kernel=np.ones_like(t);mask=abs(t)>1e-7
        kernel[mask]=np.sinh(t[mask])/t[mask]
        kernel[~mask]=1+t[~mask]**2/6+t[~mask]**4/120
        kernel*=np.exp(-(es[:,None]+es[None,:])/2)
        static-=mult*float(np.sum(l*r.T*kernel))
    CACHE[key]=(static,equal);print('trace',edges,'static/equal',static,equal,flush=True)
    return static,equal

def main():
    start=time.monotonic();rs=(.2,.6,1.,1.4,1.8);messages=[(r,d)for r in rs for d in [0,1]]
    matrices=[[],[]]
    for shift in range(3):
        aa=[np.zeros((len(messages),len(messages)))for _ in range(2)]
        for i,(r,d)in enumerate(messages):
            for j,(s,e)in enumerate(messages[:i+1]):
                p=d+e+shift;edges=(3*r*s,)if p==0 else(3*r,)+(3.,)*(p-1)+(3*s,)
                values=pair_correlations(edges)
                for channel in range(2):aa[channel][i,j]=aa[channel][j,i]=(-1)**p*values[channel]/5**p
        for channel in range(2):matrices[channel].append(aa[channel])
    source=json.loads((ROOT/'results/spin_projection_preview.json').read_text());source=next(x for x in source['rows']if x['beta']==3 and x['angle_samples']==64)
    a5=json.loads((ROOT.parents[1]/'sol9_frontier_20261028/thermal/results/a5_preview.json').read_text());a5=next(x for x in a5['rows']if x['beta']==3)
    output=[]
    for name,mats in zip(['zero_frequency','matched_equal_time'],matrices):
        # The old three-r subset is preserved exactly as a nested span.
        for subset,indices in [('old_three_r',[2,3,4,5,6,7]),('wide_five_r',list(range(10)))]:
            raw=[a[np.ix_(indices,indices)]for a in mats];sc=1/np.sqrt(np.diag(raw[0]));g,h,m2=[sc[:,None]*a*sc[None,:]for a in raw]
            vals,vecs=la.eigh(g);cases=[]
            for cut in [1e-6,1e-8,1e-10,1e-12]:
                keep=vals>cut*vals[-1];q=vecs[:,keep]/np.sqrt(vals[keep]);gp=q.T@g@q;hp=q.T@h@q;mp=q.T@m2@q
                es,us=la.eigh(hp,gp);ritz=es.tolist()
                def read(c,shift):
                    den=c@g@c;r=float(c@h@c/den);v=float(c@m2@c/den-r*r)
                    return {'Rayleigh':r,'variance':v,'prescribed_shift':shift,
                            'coefficient_l1_squared_over_G_norm':float(np.sum(abs(c))**2/den),
                            'coefficients_normalized_basis':c.tolist(),**all_mode_count(r,v,ritz,source,a5)}
                baseline=read(q@us[:,-1],None);scan=[]
                for shift in np.linspace(300000.,340000.,81):
                    es2,us2=la.eigh(mp-2*shift*hp+shift**2*gp,gp);scan.append(read(q@us2[:,0],float(shift)))
                case={'Gram_cutoff':cut,'retained_rank':int(sum(keep)),
                      'retained_Gram_condition':float(vals[-1]/vals[keep][0]),'Ritz_minus_J':ritz,
                      'max_Rayleigh':baseline,'best_variance':min(scan,key=lambda x:x['variance']),
                      'best_fixed_reference_loop':min(scan+[baseline],key=lambda x:x['all_mode_loop_tail_proposal']),
                      'scan':scan}
                cases.append(case)
                print('SUMMARY',name,subset,cut,'rank',sum(keep),'Rayleigh',baseline['Rayleigh'],'var',baseline['variance'],'bestloop',case['best_fixed_reference_loop']['all_mode_loop_tail_proposal'],flush=True)
            output.append({'channel':name,'span':subset,'messages':[messages[i]for i in indices],
                           'Gram_eigenvalues':vals.tolist(),'cases':cases,
                           'G':g.tolist(),'H':h.tolist(),'M2':m2.tolist()})
    result={'status':'ONE_WIDER_PROJECTED_SPAN_AND_UNCHANGED_EQUAL_TIME_CONTROL_NUMERICAL',
            'beta':3,'rows':output,'distinct_Kubo_and_equal_time_trace_pairs':len(CACHE),
            'seconds':time.monotonic()-start,'new_exact_acquisition':False,
            'scope':'All physical states per source eigensystem. Kubo source and conditioning costs charged; no validated source enclosures.'}
    (ROOT/'results/wider_time_projection.json').write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'results/wider_time_trace_inputs.json').write_text(json.dumps({','.join(map(str,k)):v for k,v in CACHE.items()},indent=2)+'\n')

if __name__=='__main__':main()
