"""Genuine n=19 positive control for the existing three-copy relaxation.

Couple rank-two columns, not 8000-by-8000 density matrices. The CG routine is
the inspected, locally authored audit_lift.cg. All constraints are copied in
mathematical form from three_copy_sparse.py, without running its optimization.
"""
import sys,json,time
from pathlib import Path
from functools import lru_cache
import numpy as np
import sympy as s
from sympy.physics.wigner import wigner_6j

out=Path(__file__).resolve().parent
base=out.parent
sys.path.insert(0,str(base))
from audit_lift import cg
start=time.time()
n=19;D=20;K=2;j=9.5;sj=s.Rational(19,2)
V=np.load(out/'positive19_dicke.npz')['V'];P=V@V.T
M=np.array([[float(s.Rational(v)) for v in row] for row in json.loads((base/'transform_n19.json').read_text())])
@lru_cache(None)
def six(a,b,c,d,e,f):return float(wigner_6j(a,b,c,d,e,f))

# Two-copy coupled code-column amplitudes.
pair={}
w=[]
for l in range(D):
    A=np.zeros((2*l+1,4))
    for mm in range(-l,l+1):
        for i in range(D):
            k=mm+n-i
            if 0<=k<D:A[mm+l]+=cg(j,j,l,i-j,k-j,mm)*np.outer(V[i],V[k]).ravel()
    pair[l]=A
    w.append(float(np.sum(A*A)))
w=np.array(w)

# Independent intrinsic enumerators from the code projector.
a=[];b=[]
for k in range(D):
    aa=bb=0.
    for q in range(-k,k+1):
        T=np.zeros((D,D))
        for m in range(D):
            dest=m+q
            if 0<=dest<D:T[dest,m]=np.sqrt((2*k+1)/D)*cg(j,k,j,m-j,q,dest-j)
        aa+=abs(np.trace(P@T))**2
        bb+=np.trace(P@T.T@P@T).real
    a.append(D*aa/K**2);b.append(D*bb/K)
a=np.array(a);b=np.array(b)
print('Pair weights/enumerators built',time.time()-start,flush=True)
Y=np.zeros((D,D))
for i in range(D):Y[n-i,i]=(-1)**(n-i)
Vtr=Y@V

def coupled(J2,ls,third):
    J=J2/2
    C=np.zeros((J2+1,len(ls),8))
    for li,l in enumerate(ls):
        for mm in range(-l,l+1):
            for p in range(D):
                MM=mm+p-j
                if abs(MM)>J:continue
                C[round(MM+J),li]+=cg(l,j,J,mm,p-j,MM)*np.outer(pair[l][mm+l],third[p]).ravel()
    return np.einsum('mia,mja->ij',C,C)/(J2+1)
blocks=[]
for J2 in range(1,58,2):
    J=s.Rational(J2,2)
    ls=[l for l in range(D) if abs(l-sj)<=J<=l+sj]
    R=coupled(J2,ls,V)
    Rtr=coupled(J2,ls,Vtr)
    U=np.array([[(-1)**(n+l+lp)*np.sqrt((2*l+1)*(2*lp+1))*six(sj,sj,l,sj,J,lp) for lp in ls] for l in ls])
    W=np.diag([(-1)**(n-l) for l in ls]);I=np.eye(len(ls))
    Pa=(I-W-U-W@U@W+W@U+U@W)/6
    B=np.diag([w[l]/(2*l+1) for l in ls])
    blocks.append({'J2':J2,'ls':ls,'R':R,'Rtr':Rtr,'U':U,'W':W,'Pa':Pa,'B':B,'Rp':np.zeros_like(R)})
print('Three-copy coupled blocks built',time.time()-start,flush=True)

marg=np.zeros(D);mult=np.zeros(D)
for block in blocks:
    for ii,l in enumerate(block['ls']):
        marg[l]+=(block['J2']+1)*block['R'][ii,ii]
        mult[l]+=(block['J2']+1)*(block['R']@block['U'])[ii,ii]
lift=[]
for rank in range(5):
    for l in range(D):
        for lp in range(l,min(D,l+rank+1)):
            if l+lp<rank:continue
            val=0.
            for block in blocks:
                ls=block['ls']
                if l not in ls or lp not in ls:continue
                J=s.Rational(block['J2'],2)
                coef=float((-1)**(lp+sj+J+rank))*six(l,sj,J,sj,lp,rank)
                val+=(block['J2']+1)*coef*(block['R']@(block['U']-np.eye(len(ls))/K))[ls.index(lp),ls.index(l)]
            lift.append({'rank':rank,'l':l,'lp':lp,'residual':float(val)})
print('Lift KL checked',max(abs(z['residual']) for z in lift),time.time()-start,flush=True)

# Apply exactly the sparse constructor's partial-time-reversal 6j map, and
# compare with an independent direct coupled-column calculation of its image.
orth=0.;involution=0.
for l in range(D):
    for lp in range(l,D):
        allowed=[bb for bb in blocks if l in bb['ls'] and lp in bb['ls']]
        ranks=list(range(abs(l-lp),min(l+lp,n)+1))
        C=np.array([[float((-1)**(lp+sj+s.Rational(bb['J2'],2)+rank))*six(l,sj,s.Rational(bb['J2'],2),sj,lp,rank) for rank in ranks] for bb in allowed])
        weightsJ=np.array([bb['J2']+1 for bb in allowed]);weightsr=np.array([2*rank+1 for rank in ranks])
        orth=max(orth,float(np.max(np.abs(C.T@np.diag(weightsJ)@C-np.diag(1/weightsr)))))
        F=(C*np.array([(-1)**rank*(2*rank+1) for rank in ranks])[None,:])@C.T@np.diag(weightsJ)
        involution=max(involution,float(np.max(np.abs(F@F-np.eye(len(allowed))))))
        original=np.array([bb['R'][bb['ls'].index(l),bb['ls'].index(lp)] for bb in allowed])
        pred=F@original
        for v,bb in zip(pred,allowed):
            ii=bb['ls'].index(l);jj=bb['ls'].index(lp)
            bb['Rp'][ii,jj]=bb['Rp'][jj,ii]=v

def norm(X):return float(np.max(np.abs(X)))
def mineig(X):return float(np.linalg.eigvalsh((X+X.T)/2).min())
G=K*M-np.eye(D)
receipt={
 'n':n,'distance':5,'source':'Aydin-Alekseyev-Barg 2024, Section 7, exact root certified in positive19_certificate.json',
 'construction':'Direct Clebsch-Gordan coupling of V tensor V tensor V, followed by trace over magnetic quantum number divided by 2J+1; no optimization and no dense D^3 density matrix.',
 'checks':{
 'V_Gram_error':norm(V.T@V-np.eye(2)),
 'P_projector_error':norm(P@P-P),
 'pair_trace_error':abs(float(sum(w))-K*K),
 'triple_trace_error':abs(sum((bb['J2']+1)*np.trace(bb['R']) for bb in blocks)-K**3),
 'a0_error':abs(float(a[0])-1),
 'a_sum_error':abs(float(sum(a))-D/K),
 'a_min':float(a.min()),'B_minus_A_min':float((G@a).min()),'w_min':float(w.min()),
 'MacWilliams_identity_error':norm(b-K*M@a),
 'enumerator_KL_error':norm((G@a)[1:5]),
 'pair_weights_identity_error':norm(w-(K*K/D)*M@(np.array([(-1)**l for l in range(D)])*a)),
 'marginal_error':norm(marg-K*w),
 'multiplier_error':norm(mult-w),
 'commutator_U_error':max(norm(bb['R']@bb['U']-bb['U']@bb['R']) for bb in blocks),
 'commutator_W_error':max(norm(bb['R']@bb['W']-bb['W']@bb['R']) for bb in blocks),
 'antisymmetric_support_error':max(norm(bb['Pa']@bb['R']) for bb in blocks),
 'lift_KL_max_error':max(abs(z['residual']) for z in lift),
 'PPT_6j_orthogonality_error':orth,
 'PPT_map_involution_error':involution,
 'PPT_direct_coupling_error':max(norm(bb['Rp']-bb['Rtr']) for bb in blocks),
 'time_reversal_P_error':norm(Y@P.T@Y.T-P),
 'R_min_eigenvalue':min(mineig(bb['R']) for bb in blocks),
 'PPT_R_min_eigenvalue':min(mineig(bb['Rp']) for bb in blocks),
 'complement_B_minus_R_min_eigenvalue':min(mineig(bb['B']-bb['R']) for bb in blocks),
 'complement_B_minus_PPT_R_min_eigenvalue':min(mineig(bb['B']-bb['Rp']) for bb in blocks),
 },
 'block_count':len(blocks),'largest_block':max(len(bb['ls']) for bb in blocks),'lift_KL_equation_count':len(lift),'a':a.tolist(),'w':w.tolist(),'seconds':time.time()-start,
 'per_block':[{'J2':bb['J2'],'l_values':bb['ls'],'R_min_eigenvalue':mineig(bb['R']),'PPT_R_min_eigenvalue':mineig(bb['Rp']),'complement_min_eigenvalue':mineig(bb['B']-bb['R']),'PPT_complement_min_eigenvalue':mineig(bb['B']-bb['Rp'])} for bb in blocks],
 'all_lift_KL_residuals':lift,
}
receipt['passed_at_1e-10']=all(abs(v)<1e-10 for k,v in receipt['checks'].items() if 'error' in k) and all(v>-1e-10 for k,v in receipt['checks'].items() if 'min' in k)
(out/'positive19_lift_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
np.savez(out/'positive19_lift_blocks.npz',a=a,w=w,**{f"J{bb['J2']}_{key}":bb[key] for bb in blocks for key in ['R','Rp','Rtr','U','W','B']})
print(json.dumps({'checks':receipt['checks'],'seconds':receipt['seconds'],'passed':receipt['passed_at_1e-10']},indent=2),flush=True)
assert receipt['passed_at_1e-10']
