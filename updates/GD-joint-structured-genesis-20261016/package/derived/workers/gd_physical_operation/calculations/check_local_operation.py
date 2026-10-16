#!/usr/bin/env python3
"""Finite algebra checks and explicit rate arithmetic, not hardware evidence."""
import itertools, json, math, pathlib
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parent
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); Z=np.diag([1,-1]).astype(complex)
def kron(*v):
 r=np.array([[1]],complex)
 for m in v:r=np.kron(r,m)
 return r
def channel(kraus,rho):return sum(k@rho@k.conj().T for k in kraus)
def choi(kraus):
 d=kraus[0].shape[0]
 return sum(np.outer(k.reshape(-1),k.reshape(-1).conj())/d for k in kraus)
d=8; Id=np.eye(d,dtype=complex)
S1=kron(Z,Z,I); S2=kron(I,Z,Z); Q=kron(I,X,I)
P={t:((Id+(-1)**t[0]*S1)/2)@((Id+(-1)**t[1]*S2)/2) for t in itertools.product([0,1],repeat=2)}
Pi=P[(1,1)]
coarse=[Q@Pi,Id-Pi]
fine=[Q@Pi]+[P[t] for t in P if t!=(1,1)]
E=list(P.values())
checks={}
checks['coarse_TP_error']=float(np.linalg.norm(sum(k.conj().T@k for k in coarse)-Id))
checks['fine_TP_error']=float(np.linalg.norm(sum(k.conj().T@k for k in fine)-Id))
checks['coarse_choi_min']=float(np.linalg.eigvalsh(choi(coarse))[0])
checks['fine_choi_min']=float(np.linalg.eigvalsh(choi(fine))[0])
vec=np.zeros(d,complex);vec[0]=vec[1]=1/math.sqrt(2)
rho=np.outer(vec,vec.conj())
c=channel(coarse,rho);f=channel(fine,rho)
checks['inactive_coarse_error']=float(np.linalg.norm(c-rho))
checks['inactive_offdiagonal_coarse']=float(c[0,1].real)
checks['inactive_offdiagonal_fine']=float(f[0,1].real)
checks['inactive_difference_unhalved_trace_norm']=float(np.abs(np.linalg.eigvalsh(c-f)).sum())
# Verify E o C = C o E = fine on the complete matrix-unit basis.
comp_err=0
for a,b in itertools.product(range(d),repeat=2):
 mat=np.zeros((d,d),complex);mat[a,b]=1
 out=channel(fine,mat)
 comp_err=max(comp_err,float(np.linalg.norm(out-channel(E,channel(coarse,mat)))),float(np.linalg.norm(out-channel(coarse,channel(E,mat)))))
checks['refinement_composition_error']=comp_err
# Ideal Boolean-predicate isometry: compute syndromes, AND into flag,
# uncompute work syndromes, then conditional X on middle data qubit.
K=[np.zeros((d,d),complex) for _ in range(8)]
for x in range(d):
 bits=[(x>>2)&1,(x>>1)&1,x&1]
 a=bits[0]^bits[1];b=bits[1]^bits[2]
 flag=a&b
 a^=bits[0]^bits[1];b^=bits[1]^bits[2]
 bits[1]^=flag
 y=(bits[0]<<2)|(bits[1]<<1)|bits[2]
 anc=(a<<2)|(b<<1)|flag
 K[anc][y,x]=1
checks['AND_dilation_kraus_errors']=[float(np.linalg.norm(K[1]-coarse[0])),float(np.linalg.norm(K[0]-coarse[1]))]
checks['AND_work_ancilla_leakage_norm']=float(sum(np.linalg.norm(k) for k in K[2:]))
# At gamma=|h| the finite-rate channel is a pi/2 rotation (up to phase).
h=.37; gamma=abs(h); lam=gamma+h*h/gamma
U=(math.sqrt(gamma)*Z+1j*h/math.sqrt(gamma)*I)/math.sqrt(lam)
checks['single_pauli_unitarity_error']=float(np.linalg.norm(U.conj().T@U-I))
maxerr=0
for a,b in itertools.product(range(2),repeat=2):
 mat=np.zeros((2,2),complex);mat[a,b]=1
 L=gamma*(Z@mat@Z-mat)-1j*h*(Z@mat-mat@Z)
 maxerr=max(maxerr,float(np.linalg.norm(L-lam*(U@mat@U.conj().T-mat))))
checks['single_pauli_compiler_error']=maxerr
# Pauli-floor reset identity on all matrix units.
sm=np.array([[0,1],[0,0]],complex);kap=.7
def dissip(A,r):return A@r@A.conj().T-(A.conj().T@A@r+r@A.conj().T@A)/2
reseterr=0
for a,b in itertools.product(range(2),repeat=2):
 mat=np.zeros((2,2),complex);mat[a,b]=1
 lhs=kap*dissip(sm,mat)+(kap/4)*dissip(Z,mat)
 rhs=kap*(np.diag([np.trace(mat),0])-mat)
 reseterr=max(reseterr,float(np.linalg.norm(lhs-rhs)))
checks['amplitude_damping_floor_reset_identity_error']=reseterr
# Enumeration of one CSS sector on a periodic 4D lattice verifies support incidence.
L=4; origins=list(itertools.product(range(L),repeat=4));dirs=range(4)
def shift(v,j,step):
 w=list(v);w[j]=(w[j]+step)%L;return tuple(w)
def star_edge(v,i):
 return {(v,tuple(sorted((i,j)))) for j in dirs if j!=i}|{(shift(v,j,-1),tuple(sorted((i,j)))) for j in dirs if j!=i}
counts={}
supportsizes=set()
for v in origins:
 for i,j in itertools.combinations(dirs,2):
  patch=star_edge(v,i)|star_edge(v,j)
  supportsizes.add(len(patch))
  for q in patch:counts[q]=counts.get(q,0)+1
checks['primal_patch_support_sizes']=sorted(supportsizes)
checks['primal_stream_incidence_per_data']=sorted(set(counts.values()))
checks['primal_streams']=len(origins)*6
checks['data_qubits']=len(counts)
checks['both_sector_stream_incidence_by_duality']=22
# Direct gate implementation only: probability another physical start sharing
# one chosen data qubit occurs during a duration tau. Excludes current stream.
collision=[]
for tau_us in [1,5,10,100]:
 tau=tau_us*1e-6
 limit=-math.log(.99)/(21*tau)
 collision.append({'tau_microseconds':tau_us,'kappa_per_stream_max_for_1pct_one_constituent_collision_per_second':limit,'mean_data_duty_fraction_at_limit':22*limit*tau})
checks['collision_bound_table']=collision
checks['hypothetical_floor_table']=[{'residual_detuning_bound_hz':df,'u_rad_per_second':math.pi*df,'gamma_per_second':math.pi*df,'compiled_rate_per_data_per_second':2*math.pi*df,'owner_cell_compiled_rate_6_data_per_second':12*math.pi*df,'added_ramsey_time_seconds':1/(2*math.pi*df)} for df in [1,10,100,1000]]
# Idle damping comparison uses published mean T1=68 us only as illustration;
# it does not assert an acquired AD-only model or a memory threshold.
kappa_1us=-math.log(.99)/(21e-6)
checks['published_T1_68us_illustration']={'amplitude_damping_rate_per_second':1/(68e-6),'rate_divided_by_direct_gate_kappa_1us_collision_ceiling':1/(68e-6)/kappa_1us,'floor_regularized_reset_proposal_per_second':1/(68e-6)}
assert checks['inactive_difference_unhalved_trace_norm']>0.999999999
assert checks['primal_patch_support_sizes']==[11]
assert checks['primal_stream_incidence_per_data']==[11]
assert max(checks['coarse_TP_error'],checks['fine_TP_error'],comp_err,maxerr,reseterr)<1e-12
(ROOT/'CHECK_RESULTS.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
