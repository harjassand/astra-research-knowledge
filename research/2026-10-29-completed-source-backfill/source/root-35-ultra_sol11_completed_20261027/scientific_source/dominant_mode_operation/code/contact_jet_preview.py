"""New internal-relative-time spin1 contact jet; bounded numerical preview.

The trial span is P0 f, A P0 f, A d_delta g_delta|0+, A=-J. Applying A to
the new jet avoids the overlapping-dimer contact term in its squared form.
All physical magnetization sectors are included. No source validation.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
import sys,time,json,hashlib
import numpy as np
import scipy.linalg as la
import scipy.sparse as ss

ROOT=Path(__file__).resolve().parents[1];WORK=ROOT.parents[1]
OLD=WORK/'sol10_constructive_frontier_20261028/thermal_spin_projection'
sys.path.insert(0,str(OLD/'code'))
from angular_spin_projection import sector_parts
from projected_fugacity_preview import all_mode_count

def boundary_bond(states,edge):
    lookup={w:i for i,w in enumerate(states)};rows=[];cols=[];vals=[]
    for col,w in enumerate(states):
        rows.append(col);cols.append(col);vals.append(float(w[edge]*w[edge+1]))
        a,b=w[edge:edge+2]
        for step in (-1,1):
            if not(-2<=a+step<=2 and -2<=b-step<=2):continue
            v=list(w);v[edge]+=step;v[edge+1]-=step
            rows.append(lookup[tuple(v)]);cols.append(col)
            vals.append(np.sqrt((6-a*(a+step))*(6-b*(b-step)))/2)
    return ss.csr_matrix((vals,(rows,cols)),shape=(len(states),len(states)))

def integrated(n,beta=3.):
    start=time.monotonic();tot=np.zeros((2,2));equal=np.zeros((2,2));parts=[]
    for mag in range(2*n+1):
        states,matrices=sector_parts(n,mag)
        if not states:continue
        d0,d1,_,_=matrices
        l=np.array([w[0]for w in states]);r=np.array([w[-1]for w in states])
        h=(d0+np.sqrt(6)*d1).toarray();h[np.diag_indices_from(h)]-=l*r
        h*=beta
        bl=beta*boundary_bond(states,0);br=beta*boundary_bond(states,n-2)
        dl=6*beta*np.diag([w[1]for w in states])-.5*(l[:,None]+l[None,:])*bl.toarray()
        dr=6*beta*np.diag([w[-2]for w in states])-.5*(r[:,None]+r[None,:])*br.toarray()
        energies,u=la.eigh(h,check_finite=False,overwrite_a=True)
        a=[u.T@(l[:,None]*u),u.T@dl@u]
        b=[u.T@(r[:,None]*u),u.T@dr@u]
        x=abs(energies[:,None]-energies[None,:]);psi=np.ones_like(x)
        nz=x>1e-8;psi[nz]=-np.expm1(-x[nz])/x[nz]
        psi[~nz]=1-x[~nz]/2+x[~nz]**2/6
        kernel=np.exp(-np.minimum(energies[:,None],energies[None,:]))*psi
        weights=np.exp(-energies);mult=1 if mag==0 else 2
        for i in range(2):
            for j in range(2):
                tot[i,j]+=mult*float(np.sum(a[i]*b[j].T*kernel))
                equal[i,j]+=mult*float(np.dot(np.diag(a[i]@b[j]),weights))
        parts.append({'M':mag,'dimension':len(states),'multiplicity':mult,
                      'max_boundary_jet_norm':max(float(la.norm(dl,2)),float(la.norm(dr,2)))if n<=3 else None})
    assert sum(p['dimension']*p['multiplicity']for p in parts)==5**n
    symmetry=abs(tot[0,1]-tot[1,0])/max(1.,abs(tot[0,1]),abs(tot[1,0]))
    assert symmetry<2e-11
    return {'n':n,'beta':beta,'C':tot.tolist(),'equal_time_C':equal.tolist(),
            'endpoint_reflection_relative_error':symmetry,'sectors':parts,
            'seconds':time.monotonic()-start,
            'contact_scope':'C11 at n2 is NOT identified with the two-jet source norm; shared-edge contact not included.'}

def analyze(mats,source,a5,name):
    raw=[np.array(x)for x in mats];sc=1/np.sqrt(np.diag(raw[0]));g,h,m2=[sc[:,None]*x*sc[None,:]for x in raw]
    ev,vec=la.eigh(g);out=[]
    for cutoff in (1e-8,1e-10,1e-12):
        keep=ev>cutoff*ev[-1];q=vec[:,keep]/np.sqrt(ev[keep]);gp=q.T@g@q;hp=q.T@h@q;mp=q.T@m2@q
        es,us=la.eigh(hp,gp);ritz=es.tolist()
        schur=la.eigvalsh(mp-hp@la.solve(gp,hp))
        def read(c,shift=None):
            norm=c@g@c;r=float(c@h@c/norm);v=float(c@m2@c/norm-r*r)
            return {'Rayleigh':r,'variance':v,'prescribed_shift':shift,
                    'coefficient_l1_squared_over_G_norm':float(np.sum(abs(c))**2/norm),
                    'coefficients_normalized_basis':c.tolist(),**all_mode_count(r,v,ritz,source,a5)}
        baseline=read(q@us[:,-1]);scan=[]
        for shift in np.linspace(300000.,340000.,81):
            _,u=la.eigh(mp-2*shift*hp+shift**2*gp,gp);scan.append(read(q@u[:,0],float(shift)))
        out.append({'Gram_cutoff':cutoff,'retained_rank':int(sum(keep)),
                    'retained_Gram_condition':float(ev[-1]/ev[keep][0]),'Ritz_minus_J':ritz,
                    'residual_Gram_eigenvalues':schur.tolist(),'max_Rayleigh':baseline,
                    'best_variance':min(scan,key=lambda x:x['variance']),
                    'best_target_upper':min(scan+[baseline],key=lambda x:x['combined_target_upper'])})
    return {'name':name,'G':g.tolist(),'H':h.tolist(),'M2':m2.tolist(),
            'normalization_scale':sc.tolist(),'Gram_eigenvalues':ev.tolist(),'rows':out}

def main():
    start=time.monotonic();traces={}
    old=json.loads((OLD/'results/static_time_message_preview.json').read_text())
    old=next(x for x in old['rows']if x['beta']==3.)
    for n in range(2,7):
        tr=integrated(n);traces[n]=tr
        reference=next(x for x in old['chains']if x['n']==n)['integrated_minus_SzSz']
        tr['relative_error_vs_frozen_C00']=abs((-tr['C'][0][0])/reference-1)
        assert tr['relative_error_vs_frozen_C00']<3e-12
        print('TRACE',n,tr['C'],'seconds',time.monotonic()-start,flush=True)
        (ROOT/'results/contact_jet_trace_preview.json').write_text(json.dumps(list(traces.values()),indent=2)+'\n')
    messages=[(0,0),(0,1),(1,1)];mats=[]
    for shift in range(3):
        m=np.zeros((3,3))
        for i,(a,d)in enumerate(messages):
            for j,(b,e)in enumerate(messages):
                p=d+e+shift
                if a and b:assert p>=2
                if a or b:assert p>=1
                m[i,j]=(-1)**(p+1)*traces[p+2]['C'][a][b]/5**p
        assert np.allclose(m,m.T,rtol=3e-12,atol=1e-8)
        mats.append((m+m.T)/2)
    source=json.loads((OLD/'results/spin_projection_preview.json').read_text())
    source=next(x for x in source['rows']if x['beta']==3 and x['angle_samples']==64)
    a5=json.loads((WORK/'sol9_frontier_20261028/thermal/results/a5_preview.json').read_text())
    a5=next(x for x in a5['rows']if x['beta']==3)
    result={'status':'INTERNAL_RELATIVE_TIME_CONTACT_JET_NUMERICAL_PREVIEW',
      'beta':3,'messages':messages,'source_operator':'D=6 beta Sz_neighbor - {Sz_endpoint,beta h_edge}/2',
      'rows':[analyze([m[:2,:2]for m in mats],source,a5,'unchanged_uniform_P0_control'),
              analyze(mats,source,a5,'new_A_times_relative_time_jet')],
      'distinct_uniform_open_Hamiltonians':5,'maximum_sites':6,'seconds':time.monotonic()-start,
      'new_validated_source_acquisition':False,
      'scope':'All physical sectors, float64 Kubo forms. Source contact identity requires independent algebraic checks; not certified thermal eigenvalue enclosures.'}
    np.savez(ROOT/'results/contact_jet_matrices.npz',G=mats[0],H=mats[1],M2=mats[2])
    (ROOT/'results/contact_jet_preview.json').write_text(json.dumps(result,indent=2)+'\n')
    for row in result['rows']:print('SUMMARY',row['name'],row['rows'][0],flush=True)

if __name__=='__main__':main()
