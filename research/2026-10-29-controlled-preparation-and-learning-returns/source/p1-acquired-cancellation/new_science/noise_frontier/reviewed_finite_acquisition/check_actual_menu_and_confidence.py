#!/usr/bin/env python3
"""New actual-kinetics and interval-certificate checks, exact rational arithmetic."""
from pathlib import Path
from fractions import Fraction as F
import contextlib, io, json, runpy
import numpy as np

with contextlib.redirect_stdout(io.StringIO()):
    b=runpy.run_path(str(Path(__file__).with_name('check_pulse_closure.py')))
eye,diag,inv,zero,tilt,serial=(b[x] for x in ['eye','diag','inv','zero','tilt','serial'])
Qd,F8,Q8,E8,G8,L,Wb=(b[x] for x in ['Qd','F8','Q8','E8','G8','L','Wb'])
alpha=F(128); n=8; r=4

def norminf(A): return max(sum(abs(x) for x in row) for row in A)
def normone(A): return norminf(A.T)
def psd(A):
    assert zero(A-A.T)
    B=A.copy()
    for i in range(len(B)):
        if B[i,i]<0: return False
        if B[i,i]==0:
            if any(B[i,j]!=0 for j in range(i+1,len(B))): return False
            continue
        for j in range(i+1,len(B)):
            for k in range(i+1,len(B)):
                B[j,k]-=B[j,i]*B[i,k]/B[i,i]
    return True

# An actual operation with the correct visible Gibbs weight but DIFFERENT
# symmetric kinetic factors. The canonical interpolation is now deliberately wrong.
h4=[F(1),F(1),F(1),F(3,2)]; Qop4=tilt(Qd,h4)
factors=b['mat']([[1,F(3,2),1,F(4,3)],[F(3,2),1,F(5,4),1],
                  [1,F(5,4),1,F(7,6)],[F(4,3),1,F(7,6),1]])
for i in range(4):
    for j in range(4):
        if i!=j: Qop4[i,j]*=factors[i,j]
    Qop4[i,i]=-sum(Qop4[i,j] for j in range(4) if j!=i)
Qop=np.kron(Qop4,eye(2))+np.kron(eye(4),b['mat']([[-7,7],[7,-7]]))
hv=[x for x in h4 for _ in range(2)]; W=diag([x*x/F(8) for x in hv])
assert zero(W@Qop-Qop.T@W) and zero(Qop@b['ones'](8))
S=alpha*inv(alpha*eye(8)-Qop)
G=F8.T@W@F8; K=F8.T@W@S@F8; D=F8.T@W@S@S@F8
res=D-K@inv(G)@K; assert zero(res)
C=inv(G)@K; Lop=alpha*(eye(r)-inv(C)); assert zero(Qop@F8-F8@Lop)
Pi=inv(G8)@(F8.T@E8@F8/F(8)); HH=eye(r)+F(1,2)*Pi
wrong=inv(HH)@(L@HH-F(1,2)*Wb)
assert not zero(Qop@F8-F8@wrong)

# Deliberately imperfect moment entries; these are NOT measured samples.
eta=F(1,10**50); Gh=G+eta*eye(r); Kh=K+eta*eye(r); Dh=D-eta*eye(r)
assert psd(Gh) and psd(Kh)
g=1/norminf(inv(Gh)); g0=g-eta; assert g0>0
kn=norminf(Kh)
eR=eta+eta*(2*kn+eta)/g0+kn*kn*eta/(g*g0)
Rh=Dh-Kh@inv(Gh)@Kh
assert psd(eR*eye(r)-(Rh-res)) and psd(eR*eye(r)+(Rh-res))
eps2=(norminf(Rh)+eR)/g0
Ch=inv(Gh)@Kh
eC=eta/g+eta*(kn+eta)/(g*g0)
c=1/max(norminf(inv(Ch)),normone(inv(Ch))); assert c>eC
errL=alpha*eC/(c*(c-eC))
Lh=alpha*(eye(r)-inv(Ch)); delta=Lh-Lop
assert psd(errL*errL*eye(r)-delta.T@delta)

# Clock probabilities can be finite and independently redrawn. Range/precision
# below are apparatus parameters only; no physical timing or entropy is claimed.
A=6; Wrange=F(64); cap=F(64); amin=F(16); Tc=F(4); dt=F(1,2**40)
M=int(Tc/dt); bits=128
tail=F(1,2**64) # e^(-alpha_min Tc)<=2^(-64), since e>2.
clock_bound=2*Wrange*A*(tail+F(M+1,2**bits)+2*cap*dt)

out={'result':'PASS','scope':'Exact synthetic matrix/interval checks, no actual data.',
 'unknown_kinetic_prefactors':{'weighted_detailed_balance':True,
  'actual_menu_reconstruction_exact':True,'canonical_extrapolation_fails':True,
  'actual_exit_ceiling':max(-Qop[i,i] for i in range(n))},
 'finite_entry_error_certificate':{'imposed_entry_radius':eta,'gram_floor':g0,
  'residual_error_upper':eR,'normalized_defect_upper':eps2,
  'generator_inversion_error_upper_euclidean':errL,
  'exact_psd_checks':'Both residual-error signs and generator squared-error checked'},
 'finite_clock_bound':{'stages':A,'weight_range':Wrange,'pulse_cap':cap,
  'alpha_min':amin,'censor_time':Tc,'timer_grid':dt,'uniform_bits_per_clock':bits,
  'grid_bins':M,'expectation_error_upper':clock_bound,
  'implementation':'Binary search certified CDF; do not allocate an M-entry table.'}}
p=Path(__file__).with_name('ACTUAL_MENU_CONFIDENCE_RESULTS.json')
p.write_text(json.dumps(serial(out),indent=2)+'\n')
print(json.dumps({'result':'PASS','actual_menu_reconstruction':'exact',
 'wrong_canonical_model_detected':True,'matrix_intervals_checked':'exact PSD',
 'normalized_defect_upper_float':float(eps2),'clock_error_upper_float':float(clock_bound),
 'output':str(p)},indent=2))
