"""Full exact SOS face at the independently reconstructed acoustic boundary.

All 78 symmetric Gram coefficients, all 60 quadratic two-form coefficients,
and both diagonal diffusion coefficients are variable. No source coefficients
are frozen. Reflection averaging permits diagonal diffusion without loss for
the SOS/local corrected-heat class.
"""
from geometry import *
from pathlib import Path
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
import pickle,time,json

base=Path(__file__).parent
xb=list(cwr(range(4),2));zb=list(cwr(range(6),2));vars_=list(x)+list(z)
exps=[]
for i,j0 in xb:
    for ki,l in zb:
        ee=[0]*10;ee[i]+=1;ee[j0]+=1;ee[4+ki]+=1;ee[4+l]+=1
        exps.append(tuple(ee))
ix={ee:ki for ki,ee in enumerate(exps)}
def pcol(pol):
    out=s.zeros(226,1)
    for ee,vv in s.Poly(s.expand(pol),*vars_).terms():
        out[ix[ee],0]=s.cancel(vv)
    return out

print('construct support',flush=True)
C=s.Matrix.hstack(*K.T.nullspace())
assert C.shape==(24,12) and all(s.cancel(vv)==0 for vv in K.T*C)
ell=C.T*Z
print('construct Gram',flush=True)
GM=s.Matrix.hstack(*[pcol((1 if i==j0 else 2)*ell[i]*ell[j0]) for i,j0 in cwr(range(12),2)])
print('construct correction',flush=True)
pairs=list(combinations(range(4),2));WM=[]
for i,k in pairs:
    for ii,jj in xb:
        pol=x[ii]*x[jj];OO=s.zeros(4);OO[i,k]=pol;OO[k,i]=-pol
        col=pcol((B1.T*OO*B2)[0]);offset=210
        for i0,k0,l0 in combinations(range(4),3):
            closed=s.expand(s.diff(OO[k0,l0],x[i0])-s.diff(OO[i0,l0],x[k0])+s.diff(OO[i0,k0],x[l0]))
            for aa in range(4):
                col[offset]=s.diff(closed,x[aa]);offset+=1
        WM.append(col)
WM=s.Matrix.hstack(*WM)
HH=s.hessian(F,x)
FM=s.Matrix.hstack(pcol((B1.T*HH*B1)[0]),pcol((B2.T*HH*B2)[0]))
M=GM.row_join(-WM).row_join(-FM)
print('rref',M.shape,flush=True);start=time.time()
rr,piv=DomainMatrix.from_Matrix(M).convert_to(QQ.frac_field(r)).rref()
rr=rr.to_Matrix();print('rank',len(piv),'seconds',time.time()-start,flush=True)
constraints=[]
for row in range(rr.rows):
    if all(vv==0 for vv in rr[row,:138]) and any(vv!=0 for vv in rr[row,138:]):
        constraints.append(rr[row,138:])
print('diffusion constraints',constraints,flush=True)
free=[col for col in range(140) if col not in piv]
print('free',free,flush=True)
data={'r':r,'C':C,'K':K,'GM':GM,'WM':WM,'FM':FM,'M':M,'rr':rr,'piv':piv,'free':free,'constraints':constraints}
with open(base/'full_face.pkl','wb') as ff:pickle.dump(data,ff)
(base/'full_face_summary.json').write_text(json.dumps({'rank':len(piv),'free_indices':free,'diffusion_constraints':[[str(vv) for vv in cc] for cc in constraints]},indent=2)+'\n')
