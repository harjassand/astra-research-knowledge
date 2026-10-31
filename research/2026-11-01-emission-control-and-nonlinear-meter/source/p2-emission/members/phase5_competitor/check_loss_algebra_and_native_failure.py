"""Validate the noise/control algebra comparison and one failed native query."""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm,norm

HERE=Path(__file__).resolve().parent


def sector(n):
    na=np.diag(np.arange(n,-1,-1,dtype=float)); nb=n*np.eye(n+1)-na
    ab=np.zeros((n+1,n+1),complex)
    for k in range(1,n+1):
        ab[k-1,k]=np.sqrt((n-k+1)*k)
    return na,nb,ab


def main():
    n2,b2,ab2=sector(2)
    v2=np.column_stack([np.array([0,1,0]),np.array([1,0,1])/np.sqrt(2)]).astype(complex)
    sx=np.array([[0,1],[1,0]],complex)
    kappa,xi,T=.02,.006,1.
    gam=kappa*(n2+b2)+xi*(ab2+ab2.conj().T)
    k=v2.conj().T@expm(-gam*T/2)@v2
    expected=np.exp(-kappa*T)*expm(-xi*T*sx)
    psi=np.array([1,0],complex); got=k@psi; got/=norm(got)
    witness=norm(got-psi*np.vdot(psi,got))
    n4,b4,ab4=sector(4)
    v4=np.column_stack([np.array([1,0,0,0,1])/np.sqrt(2),np.array([0,0,1,0,0])]).astype(complex)
    pair=ab4@ab4+(ab4@ab4).conj().T
    vv=np.kron(v4,v4); U=expm(-1j*np.pi*np.kron(n4,n4)/4)
    cz=np.diag([1,1,1,-1]).astype(complex)
    jx=(ab2+ab2.conj().T)/2; jz=(n2-b2)/2
    vy=np.column_stack([np.array([0,1,0]),np.array([1,0,-1])/np.sqrt(2)]).astype(complex)
    hp=(jx+jz)/np.sqrt(2); hm=(jx-jz)/np.sqrt(2); nt=np.pi
    up=expm(-1j*hp*nt); um=expm(-1j*hm*nt)
    native=(up-um)/2; nk=vy.conj().T@native@vy
    kernels=[]
    for t in np.linspace(0,nt,9):
        A=(expm(-1j*hp*(nt-t))@jz@expm(-1j*hp*t)-expm(-1j*hm*(nt-t))@jz@expm(-1j*hm*t))/2
        logical=nk.conj().T@vy.conj().T@A@vy
        tr=logical-np.trace(logical)*np.eye(2)/2
        kernels.append({"time":float(t),"traceless_kernel_operator_norm":float(norm(tr,2))})
    out={
        "N2_correlated_loss":{
            "P_a_dagger_b_P_equals_X_error":float(norm(v2.conj().T@ab2@v2-sx,2)),
            "positive_G_eigenvalues":[kappa-xi,kappa+xi],
            "exact_logical_filter_formula_error":float(norm(k-expected,2)),
            "conditional_trace_distance_witness":float(witness),
            "warning":"all jumps lower photon number, yet the no-jump logical filter is first order"},
        "N4_CLY_binomial":{
            "Pa_dagger_aP_equals_2I_error":float(norm(v4.conj().T@n4@v4-2*np.eye(2),2)),
            "Pb_dagger_bP_equals_2I_error":float(norm(v4.conj().T@b4@v4-2*np.eye(2),2)),
            "Pa_dagger_bP_norm":float(norm(v4.conj().T@ab4@v4,2)),
            "pair_hopping_logical_sqrt48X_error":float(norm(v4.conj().T@pair@v4-np.sqrt(48)*sx,2)),
            "pair_hopping_code_leakage_norm":float(norm((np.eye(5)-v4@v4.conj().T)@pair@v4,2)),
            "pi_over_four_Kerr_CZ_error":float(norm(vv.conj().T@U@vv-cz,2)),
            "pi_over_four_Kerr_code_leakage_norm":float(norm((np.eye(25)-vv@vv.conj().T)@U@vv,2))},
        "failed_native_single_pulse":{
            "Hamiltonians":"Hpm=(Jx +/- Jz)/sqrt(2), time pi, alternate balanced code span{|11>,(|20>-|02>)/sqrt(2)}",
            "endpoint_minus_X_error":float(norm(nk+sx,2)),
            "endpoint_leakage":float(norm((np.eye(3)-vy@vy.conj().T)@native@vy,2)),
            "first_order_differential_loss_kernels":kernels,
            "conclusion":"An exact endpoint symmetry instrument does not imply no-jump protection during its native pulse."}}
    (HERE/"loss_algebra_and_native_failure_results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()
