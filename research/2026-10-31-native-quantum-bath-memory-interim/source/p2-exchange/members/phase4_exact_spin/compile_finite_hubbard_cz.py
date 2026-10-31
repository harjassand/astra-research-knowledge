"""Compile the calibrated native cell to CZ using exact finite-U pair revivals.

The logical cell is the calibrated diagonal UNITARY target in the independent
joint-cell computation; the actual noisy cell retains its stated instrument
bound. Local rectangular pair pulses have exact return only in the admitted
one-orbital Hubbard model. Switching/higher orbitals/sensors are not certified.
"""
import json
from pathlib import Path
from math import pi,sqrt,ceil
import numpy as np
from scipy.linalg import expm,eigh

root=Path(__file__).resolve().parent.parent
data=json.loads((root/'phase4_exact_spin/joint_hubbard_cell_results.json').read_text())
row=data['cases'][-1]
phase=np.array(row['gate_phase_angles']);phi=row['actual_conditional_phase']
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.])
n=np.sqrt(3)/2*X+.5*Z
def rz(x):return expm(-.5j*x*Z)
def ry(x):return expm(-.5j*x*Y)
def rn(x):return expm(-.5j*x*n)
theta=np.arccos(-1/3)
B=rn(theta);M=B@Z@B.conj().T
vec=np.array([np.trace(M@p).real/2 for p in [X,Y,Z]])
lam=-np.arctan2(vec[1],vec[0])
A=rz(lam)@B
assert np.linalg.norm(A@Z@A.conj().T-X)<1e-12
tmax=1/(2*sqrt(50))
max_fraction=1-1/sqrt(1+16*tmax*tmax)

def phase_invariant_error(U,V):
    a=np.trace(V.conj().T@U)/len(U);return float(np.linalg.norm(U-a/abs(a)*V,2))

def pair_pulse(axis,angle):
    # A pair singlet phase is Rz(-area) on pair12 and Rn(area) on pair23.
    area=float((-angle if axis=='z' else angle)%(2*pi))
    if min(area,2*pi-area)<1e-11:return None
    m=max(1,ceil(area/(pi*max_fraction)))
    f=1-area/(pi*m)
    t=.25*sqrt(f**(-2)-1)
    duration=2*pi*m*f
    hs=np.array([[0,-2*t],[-2*t,1.]])
    u=expm(-1j*duration*hs)
    assert abs(u[1,0])<1e-10
    assert abs(u[0,0]-np.exp(1j*area))<1e-10
    return dict(axis=axis,angle=float(angle),exchange_area=area,revival_integer=m,
                t_over_U=t,duration_U_units=duration,charge_return_residual=float(abs(u[1,0])))

def compile_local(U,name):
    # Drop only a physically irrelevant whole-block phase.
    S=U*np.exp(-.5j*np.angle(np.linalg.det(U)))
    a,b=S[0,0],S[0,1]
    if abs(b)<1e-10:
        ops=[('z',-2*np.angle(a))]
    else:
        beta=2*np.arctan2(abs(b),abs(a))
        total=-2*np.angle(a) if abs(a)>1e-12 else 0.
        diff=-2*np.angle(-b)
        alpha=(total+diff)/2;gamma=(total-diff)/2
        # Ordered product, left to right; scheduling is its reversal.
        ops=[('z',alpha+pi/2+lam),('n',theta),('z',beta),('n',-theta),('z',gamma-pi/2-lam)]
    comp=I.astype(complex)
    for ax,ang in ops:comp=comp@(rz(ang) if ax=='z' else rn(ang))
    err=phase_invariant_error(comp,U)
    assert err<1e-11,(name,err)
    pulses=[p for p in (pair_pulse(ax,ang) for ax,ang in reversed(ops)) if p]
    return dict(name=name,pair_pulses=pulses,logical_error=err,
                serial_duration_U_units=sum(p['duration_U_units'] for p in pulses))

nz=1/(np.tan(phi)*np.tan(phi/2));assert abs(nz)<1
beta=np.arccos(nz)
R=rz(2*phi)@ry(beta)@rz(phi)@ry(-beta)
val,E=eigh(1j*R);V=E[:,[1,0]]
V*=np.exp(-.5j*np.angle(np.linalg.det(V)))
DA=np.diag([1,np.exp(-1j*(phase[2]-phase[0]))])
DB=np.diag([1,np.exp(-1j*(phase[1]-phase[0]))])
Dnative=np.diag(np.exp(1j*phase))
CP=np.kron(DA,DB)@Dnative
idealCP=np.diag([1,1,1,np.exp(1j*phi)])
assert phase_invariant_error(CP,idealCP)<1e-12
control=np.diag([1,np.exp(1j*(pi/2-3*phi/2))])
total=np.kron(control,I)@np.kron(I,V.conj().T)@CP@CP@np.kron(I,ry(beta))@CP@np.kron(I,ry(-beta)@V)
target=np.diag([1,1,1,-1])
assert phase_invariant_error(total,target)<1e-12
locals_=[compile_local(ry(-beta)@V,'B before first cell'),
         compile_local(ry(beta),'B between first and second cell'),
         compile_local(V.conj().T,'B after third cell'),
         compile_local(control,'A final phase')]
for k in range(3):
    locals_+=[compile_local(DA,f'A native phase correction {k+1}'),
              compile_local(DB,f'B native phase correction {k+1}')]
local_time=sum(x['serial_duration_U_units'] for x in locals_)
cell_time=data['successful_preparation_control_duration_parallel_filters_U_units']
result=dict(actual_native_conditional_phase=phi,beta=float(beta),axis_z=float(nz),
            exact_target_cz_error_up_to_global_phase=phase_invariant_error(total,target),
            native_checked_cells=3,
            local_pair_pulse_count=sum(len(x['pair_pulses']) for x in locals_),
            local_serial_duration_U_units=local_time,
            three_successful_cells_duration_U_units=3*cell_time,
            total_specified_serial_control_duration_U_units=3*cell_time+local_time,
            sensors_loading_routing_retry_and_flag_recovery_not_in_this_time=True,
            formal_sum_of_numerically_evaluated_cell_error_bounds=3*row['conversion_included_half_diamond_upper_bound'],
            local_controls=locals_)
(root/'phase4_exact_spin/finite_hubbard_cz_compiler_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='local_controls'},indent=2))
