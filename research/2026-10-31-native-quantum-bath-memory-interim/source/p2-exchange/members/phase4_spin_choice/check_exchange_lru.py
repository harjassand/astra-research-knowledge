"""Exact five-spin audit for a single-edge, energy-selective leakage reset.

No bath approximation, source contract, fitted reduced Hamiltonian, or
parameter optimization is used.  The analytic contact prescription is
tested in the complete 32-dimensional spin space.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm, eigh

I2=np.eye(2,dtype=complex)
pauli=[np.array([[0,1],[1,0]],complex),
       np.array([[0,-1j],[1j,0]],complex),np.diag([1.,-1.]).astype(complex)]
up=np.array([1.,0.]); down=np.array([0.,1.])
singlet=(np.kron(up,down)-np.kron(down,up))/np.sqrt(2)

def spinops(n):
    out=[]
    for i in range(n):
        xyz=[]
        for p in pauli:
            a=np.array([[1.]],complex)
            for j in range(n): a=np.kron(a,p/2 if j==i else I2)
            xyz.append(a)
        out.append(xyz)
    return out

def dot(s,i,j): return sum(s[i][a]@s[j][a] for a in range(3))
def norm(a): return float(np.linalg.norm(a,2))
def comm(a,b): return a@b-b@a
def basis_bit(bits):
    a=np.array([1.])
    for bit in bits: a=np.kron(a,up if bit==0 else down)
    return a

def code_isometries():
    l0p=np.kron(singlet,up)
    l1p=np.sqrt(2/3)*basis_bit([0,0,1])-(basis_bit([0,1,0])+basis_bit([1,0,0]))/np.sqrt(6)
    sd=spinops(3)
    lowering=sum(a[0]-1j*a[1] for a in sd)
    l0m=lowering@l0p; l1m=lowering@l1p
    vc=np.column_stack([l0p,l0m,l1p,l1m])
    leakp=basis_bit([0,0,0])
    leakhalf=lowering@leakp/np.sqrt(3)
    leakminushalf=lowering@leakhalf/2
    leakminus=lowering@leakminushalf/np.sqrt(3)
    vl=np.column_stack([leakp,leakhalf,leakminushalf,leakminus])
    return vc,vl,l0p,l1p

def main():
    s=spinops(5); eye=np.eye(32)
    sd=[sum(s[i][a] for i in range(3)) for a in range(3)]
    sd2=sum(x@x for x in sd)
    pl=(sd2-.75*eye)/3; pc=eye-pl
    e12=dot(s,0,1); e34=dot(s,2,3); e45=dot(s,3,4)
    phs=.25*eye-e45; pht=eye-phs
    vc,vl,l0p,l1p=code_isometries()
    jc=np.kron(vc,singlet[:,None])
    jl=np.kron(vl,singlet[:,None])
    # Highest-weight representatives suffice to derive the multiplicity blocks.
    aa=np.kron(vl[:,0],singlet)
    bb=np.kron(l1p,np.kron(up,up))
    ab=np.vdot(bb,e34@aa).real
    cc=(e34@aa-ab*bb)/np.sqrt(5/48)
    bl=np.column_stack([aa,bb,cc])
    ml=bl.conj().T@e34@bl
    target_l=np.array([[0,-1/(2*np.sqrt(3)),np.sqrt(15)/12],
                       [-1/(2*np.sqrt(3)),-1/12,np.sqrt(5)/6],
                       [np.sqrt(15)/12,np.sqrt(5)/6,-1/6]])
    a0=np.kron(l0p,singlet)
    b0=e34@a0/(np.sqrt(3)/4)
    m0=np.column_stack([a0,b0]).conj().T@e34@np.column_stack([a0,b0])
    a1=np.kron(l1p,singlet)
    b1=-(pc@pht@e34@a1)/(1/(4*np.sqrt(3)))
    c1=(pl@pht@e34@a1)/(1/np.sqrt(6))
    bcode=np.column_stack([a1,b1,c1])
    m1=bcode.conj().T@e34@bcode
    target_1=np.array([[0,-1/(4*np.sqrt(3)),1/np.sqrt(6)],
                       [-1/(4*np.sqrt(3)),1/6,np.sqrt(2)/6],
                       [1/np.sqrt(6),np.sqrt(2)/6,-5/12]])
    assert norm(ml-target_l)<1e-14
    assert norm(m1-target_1)<1e-14
    assert norm(m0-np.array([[0,np.sqrt(3)/4],[np.sqrt(3)/4,-.5]]))<1e-14
    checks=[]
    for g in [.2,.1,.05,.02]:
        delta=1.
        jh=delta+g/12+5*g*g/(144*delta)
        lam=g/(2*np.sqrt(3))*(1+5*g/(12*delta))
        time=np.pi/(2*lam)
        h=delta*pl+jh*pht+g*e34
        u=expm(-1j*h*time)
        leaked=jl.conj().T@u.conj().T@pl@u@jl
        leakage_eigs=np.linalg.eigvalsh(leaked).real
        ks=jc.conj().T@u@jc
        k0=ks[0,0]; k1=ks[2,2]
        form=np.diag([k0,k0,k1,k1])
        assert norm(ks-form)<1e-12
        p_bad=max(0.,1-abs(k0)**2,1-abs(k1)**2)
        code_bound=1-np.sqrt(max(0.,1-p_bad))+p_bad/2
        check={'g_over_gap':g,'helper_gap':jh,'contact_time':time,
               'g_times_contact_time':g*time,
               'worst_residual_leakage':float(leakage_eigs[-1]),
               'leakage_effect_eigenvalue_spread':float(np.ptp(leakage_eigs)),
               'unleaked_helper_triplet_probability_bound':float(p_bad),
               'phase_corrected_code_channel_half_diamond_bound':float(code_bound),
               'required_known_exchange_phase_correction':float(np.angle(k1/k0)),
               'singlet_kraus_multiplicity_form_error':norm(ks-form)}
        checks.append(check)
    # The first and second spectral moments rule out exact A->B transfer.
    g=.3; delta=1.; jh=delta+g/12
    hl=np.diag([delta,jh,delta+jh])+g*ml
    moment1=float((hl[1,1]-hl[0,0]).real)
    moment2=float(((hl@hl)[1,1]-(hl@hl)[0,0]).real)
    assert abs(moment1)<1e-14
    assert abs(moment2-5*g*g/144)<1e-14
    # Spectator-pair gates commute with the full contact; another axis does not.
    h=pl+1.1*pht+.2*e34
    zcomm=norm(comm(e12,h)); xcomm=norm(comm(dot(s,1,2),h))
    # Four-spin singlet code: local magnetic errors are detected but not corrected.
    s4=spinops(4); total=[sum(s4[i][a] for i in range(4)) for a in range(3)]
    st2=sum(x@x for x in total)
    vals,vecs=eigh(st2); vzero=vecs[:,vals<1e-10]
    kl=vzero.conj().T@s4[0][2]@s4[1][2]@vzero
    kl_eigs=np.linalg.eigvalsh(kl).real
    out={'leaked_J_three_halves_exchange_block':ml.real.tolist(),
         'code_logical_zero_exchange_block':m0.real.tolist(),
         'code_logical_one_exchange_block':m1.real.tolist(),
         'analytic_block_residuals':{'leak':norm(ml-target_l),'code1':norm(m1-target_1)},
         'finite_gap_contacts':checks,
         'constant_contact_cospectral_obstruction':{'first_moment_difference':moment1,
             'second_moment_difference':moment2,'required_nonzero_difference':5*g*g/144},
         'spectator_pair_gate_commutator':zcomm,
         'other_axis_gate_commutator':xcomm,
         'four_spin_singlet_KL_cross_error_eigenvalues':kl_eigs.tolist(),
         'scope':'Exact 5-spin model, analytic pulse prescription, no optimization or material-performance claim.'}
    Path(__file__).with_name('exchange_lru_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
