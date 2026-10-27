"""Endpoint-only received moment difference; ONE coarse compact-objective line gate."""
from pathlib import Path
from fractions import Fraction as Q
import numpy as np,json,time,resource,hashlib,itertools,sys
P=Path(__file__).resolve().parent;B=P.parent;G=B.parent/'morrey_global_w1_receiver_20261025/intrinsic/genuine_w1_column_step';E=G/'five_feature_pole_gate/enlarged_finegrid_simplex/six_law_endpoint_interface';from damped_arithmetic_primitives import I,mid_guard
st=time.time();K=96;k=np.arange(1,K+1);r=2**-37;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();selected=B/'newton_six_law_direction/SELECTED_ACTUAL_RAW_STRESS_ROOT_MIXTURE.json';a=Q(json.loads(selected.read_text())['selected_alpha']);ap=Q(739,131072)
D=np.load(P/'two_new_h41_pair_endpoint_delta_moments.npy');pair=read_pair=json.loads((P/'cubic_balanced_catalog_pair_receipt.json').read_text());cur=json.loads((P/'SELECTED_COMPACT_NEW_H41_MIXTURE.json').read_text());step=float(Q(cur['alpha']));radmax=0.
M=np.load(P/'received_damped_moments.npy');ht=np.load(P/'received_damped_coefficients.npz')['H_table'];k2=k*k;H1=ht[k2];H2=ht[k2[:,None]+k2[None,:]];H3=ht[k2[:,None,None]+k2[None,:,None]+k2[None,None,:]];b0,brad=mid_guard(I.div(I.rat(2),I.mul(I.PI,I.exact(k))),relative=2**-40);bs={-1:b0,1:b0*(-1.)**(k+1)}
def coeff(T):
 C=T[2:,2:,2:]*H3;FF=[];EE=[]
 for i in range(3):
  j,l=[v for v in range(3)if v!=i];A=T.transpose(i,j,l);V=C.transpose(i,j,l)
  for s in[-1,1]:FF.append((A[0,2:,2:]+s*A[1,2:,2:])/2*H2-np.einsum('i,ijk->jk',bs[s],V))
 for l in range(3):
  i,j=[v for v in range(3)if v!=l];A=T.transpose(i,j,l);V=C.transpose(i,j,l)
  for s in[-1,1]:
   for q in[-1,1]:
    L=(A[0,0,2:]+s*A[1,0,2:]+q*A[0,1,2:]+s*q*A[1,1,2:])/4;L1=(A[2:,0,2:]+q*A[2:,1,2:])/2;L2=(A[0,2:,2:]+s*A[1,2:,2:])/2
    EE.append(L*H1-np.einsum('i,ik->k',bs[s],L1*H2)-np.einsum('i,ik->k',bs[q],L2*H2)+np.einsum('i,j,ijk->k',bs[s],bs[q],V))
 return C,np.stack(FF),np.stack(EE)
angle=I.mul(I.PI,I.exact(np.arange(257)[:,None]*k[None,:]/256));TN,rad=mid_guard(I.sincos(angle)[0],radius=r);TN[0]=TN[-1]=0;radmax=max(radmax,rad)
angle=I.mul(I.PI,I.exact((2*np.arange(512)[:,None]+1)*k[None,:]/1024));TC,rad=mid_guard(I.mul(I.sincos(angle)[0],I.sinc_small(I.mul(I.PI,I.exact(k[None,:]/1024)))),radius=r);radmax=max(radmax,rad);TE=TN

def field(T):
 C,F,E=coeff(T);A=(TN@C.reshape(K,-1)).reshape(257,K,K);B=np.einsum('bj,ajk->abk',TN,A,optimize=True);V=(B.reshape(257*257,K)@TN.T).reshape(257,257,257);return V,np.stack([TC@f@TC.T for f in F]),E@TE.T
zz=np.load(P/'new_h41_compact_full_direction_arrays.npz');V0=zz['volume_base']+step*zz['volume_delta'];F0=zz['faces_base']+step*zz['faces_delta'];E0=zz['edges_base']+step*zz['edges_delta'];VD,FD,ED=field(D)
oldj=json.loads((P/'new_h41_compact_full_direction_diagnostic.json').read_text());d0=oldj['rows'][0]['delta']+step*(oldj['rows'][-1]['delta']-oldj['rows'][0]['delta']);cl,ch=map(Q,json.loads((P/'new_h41_cubic_balanced_pair_receipt.json').read_text())['actual_cubic_interval']);d6=float(Q(1,4)-(cl+ch)/2);rows=[]
for numerator in range(17):
 q=Q(numerator,16);qf=float(q);V=V0+qf*VD;F=F0+qf*FD;EE=E0+qf*ED;d=d0+qf*(d6-d0);volume=3*float(np.maximum(-V,0).sum())/128**3;face=0.
 for idx,f in enumerate(F):
  s=-1 if idx%2==0 else 1;z=f+s*d/24;face+=float((np.maximum(-f,0)+(np.sqrt(z*z+d*d/1152)-z)/2).sum())/256**2
 edge=float(np.maximum(-EE,0).sum())/128;rows.append({'alpha':str(q),'volume':volume,'face':face,'edge':edge,'sum':volume+face+edge,'delta':d})
best=min(rows,key=lambda r:r['sum']);out={'status':'FULL_GRID_BALANCED_PAIR_DIAGNOSTIC_NOT_YET_EXACT_SUM_RECEIVED','candidate_actual_cubic_interval':[str(cl),str(ch)],'candidate_pair_receipt_sha256':sha(P/'new_h41_cubic_balanced_pair_receipt.json'),'endpoint_delta_receipt_sha256':sha(P/'two_new_h41_pair_endpoint_moment_receipt.json'),'base_actual_moments_sha256':sha(P/'received_damped_moments.npy'),'volume_nodes_per_axis':257,'face_cells_per_axis':512,'edge_nodes':257,'rows':rows,'selected_diagnostic':best,'diagnostic_gain':rows[0]['sum']-best['sum'],'full_replacement':rows[-1],'max_target_radius':radmax,'b_radius':brad,'seconds':time.time()-st,'peak_RSS_MiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'scope':'Fixed existing actual raw endpoint direction; no new control/source quadrature. Coarse numerical functionals only, not new N upper or true-N ordering; finer receiving allowances NOT assigned to these arrays. Selected .06953396112407359 unchanged.'};(P/'two_new_h41_pair_compact_full_direction_diagnostic.json').write_text(json.dumps(out,indent=2)+'\n');np.savez(P/'two_new_h41_pair_compact_full_direction_arrays.npz',volume_base=V0,volume_delta=VD,faces_base=F0,faces_delta=FD,edges_base=E0,edges_delta=ED);print(json.dumps({'base':rows[0],'best':best,'replacement':rows[-1],'gain':out['diagnostic_gain'],'seconds':out['seconds']},indent=2))
