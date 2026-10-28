"""Source-bound exact/sparse interfaces for PC(level1)+closed heat.

No source generator is executed: its arrays and exact compiler are read only.
Numerical solvers are acquisition tools; none of their statuses is science.
"""
from pathlib import Path
from itertools import combinations_with_replacement as cwr
from fractions import Fraction as F
import hashlib,json,sys
import numpy as np
import scipy.sparse as sp

ROOT=Path(__file__).resolve().parent
SOL8=ROOT.parent.parent
SOURCE=Path('producer-workspace/principal')


def acquire():
    sys.path.insert(0,str(SOL8/'principal_combined_quartic'))
    from compile_hierarchy import compile_level
    from verify_dual import plus,times,var,invariants
    a=[var(i) for i in range(4)];u,v,w,q=invariants(a)
    basis=[times(u,u),times(v,v),times(u,v),times(w,w),times(u,w),times(v,w),times(q,u),times(q,v),times(q,w)]
    empty=compile_level({},1);rows=empty['rows'];rr=[];cc=[];vv=[]
    for i,row in enumerate(rows):
        for j,c in row['entries']:rr.append(i);cc.append(j);vv.append(float(F(c)))
    A=sp.coo_matrix((vv,(rr,cc)),shape=(658,1840)).tocsr()
    B=[]
    for p in basis:
        data=compile_level({e[:4]:c for e,c in p.items()},1)
        assert all(row['exponent']==old['exponent'] for row,old in zip(data['rows'],rows))
        B.append([float(F(row['rhs'])) for row in data['rows']])
    B=np.array(B).T
    source=np.load(SOURCE/'interfaces.npz')
    for key in ['E','Q','O','C']:assert np.array_equal(source[key],np.rint(source[key]))
    assert np.array_equal(2*source['N'],np.rint(2*source['N']))
    assert np.array_equal(source['C']@source['N'],np.zeros((16,45)))
    assert np.array_equal(source['O']@source['N'],source['ON'])
    pairs4=list(cwr(range(4),2));pairs6=list(cwr(range(6),2));pairs24=list(cwr(range(24),2))
    gh=np.zeros((210,300));heat_indices=[]
    for i in range(24):
        for j in range(24):heat_indices.append(21*pairs4.index(tuple(sorted((i//6,j//6))))+pairs6.index(tuple(sorted((i%6,j%6)))))
    for col,(i,j) in enumerate(pairs24):gh[heat_indices[i*24+j],col]=1 if i==j else 2
    scale=np.array([1 if i==j else np.sqrt(2) for i,j in pairs24])
    assert np.max(np.abs(source['P']*scale[None,:]-gh))<1e-14
    exponents=[tuple(row['exponent']) for row in rows];lookup={e:i for i,e in enumerate(exponents)}
    features=[]
    for i in range(4):
        for j,k in cwr(range(4),2):
            e=[0]*8;e[i]+=1;e[j+4]+=1;e[k+4]+=1;features.append(tuple(e))
    for i,j,k in cwr(range(4),3):
        e=[0]*8;e[i+4]+=1;e[j+4]+=1;e[k+4]+=1;features.append(tuple(e))
    pc_indices=[lookup[tuple(a+b for a,b in zip(e,f))] for e in features for f in features]
    np.savez(ROOT/'MAPS.npz',pc_rows=np.array(rr),pc_cols=np.array(cc),pc_values=np.array(vv),
             B=B,pc_indices=np.array(pc_indices),heat_indices=np.array(heat_indices),
             G=gh,E=source['E'],ON=source['ON'],N=source['N'],O=source['O'],C=source['C'],Q=source['Q'],
             pc_exponents=np.array(exponents),pc_features=np.array(features))
    paths=[SOURCE/'interfaces.npz',SOURCE/'build_interfaces.py',SOL8/'principal_combined_quartic/compile_hierarchy.py',
           SOL8/'principal_combined_quartic/verify_dual.py']
    binding={'sources':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],
             'PC':'Unrestricted60-feature,10-selector norm-multiplied global support',
             'heat':'Componentwise spatial Laplacian; all45 closed quadratic two-form directions; bilinear24-feature Gram',
             'scope':'SDP sufficient classes; neither numerical feasibility nor failure is a QC classification.'}
    (ROOT/'SOURCE_BINDING.json').write_text(json.dumps(binding,indent=2)+'\n')


def load():
    if not (ROOT/'MAPS.npz').exists():acquire()
    d=dict(np.load(ROOT/'MAPS.npz'))
    d['A']=sp.coo_matrix((d['pc_values'],(d['pc_rows'],d['pc_cols'])),shape=(658,1840)).tocsr()
    return d


def gaussian_moment(e):
    value=1
    for n in e:
        if n%2:return 0
        for k in range(1,n,2):value*=k
    return value


def common_gaussian(d):
    lp=np.array([gaussian_moment(e) for e in d['pc_exponents']],float)
    H=np.array([[3,0,1],[0,1,0],[1,0,3]],float);cov=np.kron(np.eye(2),H)
    lh=np.array([(cov[k,l] if i==j else 0)*1.25
                 for i,j in cwr(range(4),2) for k,l in cwr(range(6),2)])
    assert np.max(np.abs(d['A'][:,1830:].T@lp))==0
    assert np.max(np.abs(d['ON'].T@lh))==0
    assert np.max(np.abs(d['B'].T@lp-d['E'].T@lh))==0
    mp=lp[d['pc_indices']].reshape(60,60);mh=lh[d['heat_indices']].reshape(24,24)
    assert np.trace(mp)==172 and np.trace(mh)==70
    assert np.linalg.eigvalsh(mp)[0]>0 and np.linalg.eigvalsh(mh)[0]>0
    g=d['B'].T@lp
    assert np.array_equal(g,np.array([160,160,80,40,0,0,0,0,0]))
    return lp/242,lh/242


if __name__=='__main__':
    d=load();lp,lh=common_gaussian(d)
    print(json.dumps({'PC_constraints':658,'PC_variables':1840,'heat_constraints':210,
                      'heat_closed_directions':45,'common_gaussian_normal':(d['B'].T@lp).tolist()},indent=2))
