"""Phase D rank certificate and Hodge-cancelled map, independently built."""
import json
from pathlib import Path
import numpy as np
from independent_maps import build_exact, choi

def pivots_mod(a,p):
    b=[[int(x)%p for x in r] for r in a]
    row_ids=list(range(len(b)));cols=[];rows=[];r=0
    for c in range(len(b[0])):
        pivot=next((i for i in range(r,len(b)) if b[i][c]),None)
        if pivot is None:continue
        b[r],b[pivot]=b[pivot],b[r]
        row_ids[r],row_ids[pivot]=row_ids[pivot],row_ids[r]
        rows.append(row_ids[r]);cols.append(c)
        inv=pow(b[r][c],-1,p)
        b[r]=[v*inv%p for v in b[r]]
        for i in range(r+1,len(b)):
            scale=b[i][c]
            b[i]=[(x-scale*y)%p for x,y in zip(b[i],b[r])]
        r+=1
    return rows,cols

def det_mod(a,p):
    b=[[int(x)%p for x in r] for r in a];res=1
    for k in range(len(b)):
        i=next((i for i in range(k,len(b)) if b[i][k]),None)
        if i is None:return 0
        if i!=k:b[i],b[k]=b[k],b[i];res=-res
        v=b[k][k];res=res*v%p
        for i in range(k+1,len(b)):
            scale=b[i][k]*pow(v,-1,p)%p
            for j in range(k,len(b)):b[i][j]=(b[i][j]-scale*b[k][j])%p
    return res%p

def run():
    A0,K,F4,Q4=build_exact()
    assert all(x==0 for x in K.ravel()@A0)
    rows,cols=pivots_mod(A0,41)
    minor=[[A0[i,j] for j in cols] for i in rows]
    determinant=det_mod(minor,41)
    assert len(rows)==len(cols)==20 and determinant!=0
    Fc=Q4@A0  # 32 SS^dagger S Ad_D.
    J=choi(Fc,10,6)
    assert np.array_equal(J,J.T)
    t=sum(J[i,i] for i in range(60))
    j=np.asarray(J,dtype=float)/float(t)
    eig=np.linalg.eigvalsh(j)
    ccnr=np.linalg.svd(j.reshape(10,6,10,6).transpose(0,2,1,3).reshape(100,36),compute_uv=False).sum()
    z={'rank_S_exact':20,'rank_upper_bound':'Output symmetric and Tr(KY)=0, dimension20',
       'prime':41,'rank_minor_rows':rows,'rank_minor_columns':cols,'rank_minor_determinant_mod41':determinant,
       'image_S':'W={Y=Y^T:Tr(KY)=0}, complex dimension20',
       'kernel_B_on_Sym6':'span(K), complex dimension1',
       'alignment_status':'independent hand proof excludes CP R and positive lambda',
       'cancelled_target':'Fc=32 SS^dagger S composed with Ad_D',
       'cancelled_target_trace':int(t),'cancelled_normalized_min_eig_numeric':float(eig[0]),
       'cancelled_realignment_norm_numeric':float(ccnr),'cancelled_EB_status':'unknown before separate certificate'}
    root=Path(__file__).parent
    (root/'phase_d_baseline_results.json').write_text(json.dumps(z,indent=2)+'\n')
    (root/'phase_d_cancelled_integer_superoperator.json').write_text(json.dumps(Fc.tolist())+'\n')
    print(json.dumps(z,indent=2))

if __name__=='__main__':run()
