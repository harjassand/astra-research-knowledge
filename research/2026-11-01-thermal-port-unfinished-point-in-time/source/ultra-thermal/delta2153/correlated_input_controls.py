"""Reference-uniform warm-start ingredients and a correlated finite-bath test.

The initial Q/B/R state is a coherent GHZ state with THERMAL B marginal.
All controllers and the persistent bath remain in the simulated dynamics.
The comparison erases logical action from operators, not from the state,
and evolves the same input controllers/bath without resetting them.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix,eye,kron
from scipy.sparse.linalg import expm_multiply
from port_model import I,X,Y,Z,ten,norm,perfect_code,ports,charge_hamiltonians,logical_expectation
from quantum_port_controls import kernel,thermal,decode_columns,trace_norm

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/thermal_ports_20261101'

def diss(j,r):
    a=j.conj().T@j;return j@r@j.conj().T-(a@r+r@a)/2


def full_correlated_check(model,entries):
    """Independent full physical-Hilbert check of offdiagonal bath charges."""
    beta=1.;Gamma=.7;g=.6;T=.4
    sub=[next(p for p in entries if p['label']=='XIIII' and p['omega']==1),
         next(p for p in entries if p['label']=='IZIII' and p['omega']==2)]
    bp=next(p for p in entries if p['label']=='IIXII' and p['omega']==2).copy();bp['g']=.9
    blocks=charge_hamiltonians(model,sub,g=g,bath=bp)
    C=3;B=2;A=C*B;d=32*A;bd=blocks['block_dimension'];delta=bp['syndrome']
    U=model['recovery_unitary'];up=np.array([[0,0],[1,0]],complex);num=up@up.conj().T
    h=ten(model['H0'],np.eye(C),I)+ten(np.eye(32),np.diag(blocks['gaps']),I)+bp['omega']*ten(np.eye(32),np.eye(C),num)
    jumps=[]
    for c,p in enumerate(sub,1):
        r=np.zeros((C,C),complex);r[c,0]=1
        term=g*ten(U@p['operator']@U.conj().T,r,I);h+=term+term.conj().T
        j=ten(np.eye(32),r.conj().T,I)
        jumps.extend([np.sqrt(Gamma)*j,np.sqrt(Gamma*np.exp(-beta*p['omega']))*j.conj().T])
    term=bp['g']*ten(U@bp['operator']@U.conj().T,np.eye(C),up);h+=term+term.conj().T
    ident=eye(d,format='csr',dtype=complex);hh=csr_matrix(h)
    L=-1j*(kron(ident,hh)-kron(hh.T,ident))
    for j in jumps:
        j=csr_matrix(j);jj=j.conj().T@j
        L+=kron(j.conj(),j)-(kron(ident,jj)+kron(jj.T,ident))/2
    ps=thermal(beta,model['energies']);pc=thermal(beta,blocks['gaps']);pb=thermal(beta,[0,bp['omega']])
    full_initial=[];starts={0:np.zeros((16*bd*bd,4),complex),delta:np.zeros((16*bd*bd,4),complex)}
    for a in range(2):
        for b in range(2):
            e=np.zeros((2,2),complex);e[a,b]=1
            data=U@ten(e,np.diag(ps))@U.conj().T
            full_initial.append((np.sqrt(pb[a]*pb[b])*ten(data,np.diag(pc),e)).reshape(-1,order='F'))
            for s in range(16):
                for c in range(C):
                    k=s^blocks['tags'][c]^(delta if a else 0)
                    row=a*A+2*c+a;column=b*A+2*c+b
                    starts[(a^b)*delta][k*bd*bd+row+bd*column,2*a+b]=np.sqrt(pb[a]*pb[b])*ps[s]*pc[c]
    full=expm_multiply(T*L,np.stack(full_initial,axis=1))
    reduced={diff:expm_multiply(T*kernel(blocks,beta,Gamma,delta=diff),start) for diff,start in starts.items()}
    frame=ten(U,np.eye(C),I);residual=0.
    for a in range(2):
        for b in range(2):
            col=2*a+b;diff=(a^b)*delta
            r=full[:,col].reshape((d,d),order='F');r=frame.conj().T@r@frame
            rebuilt=np.zeros_like(r)
            for k in range(16):
                block=reduced[diff][k*bd*bd:(k+1)*bd*bd,col].reshape((bd,bd),order='F')
                def indices(charge):
                    return [((q*16+(charge^blocks['tags'][c]^(delta if z else 0)))*C+c)*2+z
                            for q in range(2) for c in range(C) for z in range(2)]
                rebuilt[np.ix_(indices(k),indices(k^diff))]=block
            residual=max(residual,float(np.max(np.abs(r-rebuilt))))
    assert residual<1e-10
    return residual


def main():
    model=perfect_code();entries=ports(model)
    full_residual=full_correlated_check(model,entries)
    # A non-normal one-data-site/controller jump. Full support-algebra
    # protection is required, including J^dagger J, not just J's columns.
    site=[s for s in model['seeds'] if s['site']==0]
    pc=np.array([.4,.6]);J=.2*np.eye(64,dtype=complex)
    for seed,a in zip(site,[np.array([[0,1],[0,0]],complex),Z,X]):
        coeff={'X':.6+.1j,'Y':.3,'Z':.4j}[seed['axis']]
        J+=coeff*ten(seed['recovery_pauli'],a)
    J0=logical_expectation(J,32)
    bad=np.logical_or.reduce([s['bad_syndromes'] for s in site])
    B=ten(I,np.diag(bad.astype(float)),I)
    residual=norm((J-J0)-B@(J-J0)@B)
    K=J.conj().T@J-J0.conj().T@J0
    variance_residual=norm(K-B@K@B)
    assert max(residual,variance_residual)<1e-11
    rng=np.random.default_rng(73191);normrows=[]
    good_indices=np.flatnonzero(np.diag(np.eye(64)-B).real>.5)
    bad_indices=np.flatnonzero(np.diag(B).real>.5)
    for p in (1e-6,.001,.1):
        a=np.zeros(64,complex);a[good_indices]=rng.normal(size=len(good_indices))+1j*rng.normal(size=len(good_indices));a/=np.linalg.norm(a)
        b=np.zeros(64,complex);b[bad_indices]=rng.normal(size=len(bad_indices))+1j*rng.normal(size=len(bad_indices));b/=np.linalg.norm(b)
        v=np.sqrt(1-p)*a+np.sqrt(p)*b;rho=np.outer(v,v.conj())
        actual=trace_norm(diss(J,rho)-diss(J0,rho));upper=6*norm(J)**2*np.sqrt(p)
        assert actual<=upper+1e-11
        normrows.append({'bad_population':p,'actual_dissipator_difference_trace_norm':actual,'proved_upper':upper})
    # Source-column protection alone is insufficient: J and J^dagger
    # satisfy it here but their product does not. The false p=0 estimate
    # would miss an actual coherent Lindblad defect.
    s0=np.array([[1,0],[0,0]],complex);s1=np.diag([0,1]).astype(complex)
    rise=np.array([[0,0],[1,0]],complex)
    toy=ten(I,rise)+ten(Z,s1);toy0=logical_expectation(toy,2)
    pg=ten(I,s0);plus=np.array([1,1],complex)/np.sqrt(2);r=ten(np.outer(plus,plus.conj()),s0)
    source_comm=max(norm((toy@ten(a,I)-ten(a,I)@toy)@pg) for a in (X,Y,Z))
    adjoint_source=max(norm((toy.conj().T@ten(a,I)-ten(a,I)@toy.conj().T)@pg) for a in (X,Y,Z))
    missed=trace_norm(diss(toy,r)-diss(toy0,r))
    assert source_comm<1e-12 and adjoint_source<1e-12 and missed>.9
    # Full all-Pauli-port model with one genuinely persistent bath qubit.
    bp=next(p for p in entries if p['label']=='IIXII' and p['omega']==2).copy();bp['g']=.9
    blocks=charge_hamiltonians(model,entries,g=.6,bath=bp)
    beta=4.;Gamma=.7;T=10.;D=blocks['block_dimension'];C=blocks['C'];A=blocks['A']
    ps=thermal(beta,model['energies']);pc=thermal(beta,blocks['gaps']);pb=thermal(beta,[0,blocks['bath_gap']])
    delta=blocks['bath_tag'];starts={0:np.zeros((16*D*D,4),complex),delta:np.zeros((16*D*D,4),complex)}
    for a in range(2):
        for b in range(2):
            diff=(a^b)*delta;col=2*a+b
            for s in range(16):
                for c in range(C):
                    k=s^blocks['tags'][c]^(delta if a else 0)
                    row=a*A+2*c+a;column=b*A+2*c+b
                    starts[diff][k*D*D+row+D*column,col]=np.sqrt(pb[a]*pb[b])*ps[s]*pc[c]
    actual_decoded=np.zeros((D,D,4),complex);good_decoded=np.zeros_like(actual_decoded)
    for diff,start in starts.items():
        # Only the two populated reference blocks are propagated.
        active=[j for j in range(4) if np.linalg.norm(start[:,j])>0]
        L=kernel(blocks,beta,Gamma,delta=diff);LG=kernel(blocks,beta,Gamma,good=True,delta=diff)
        actual=expm_multiply(T*L,start[:,active]);good=expm_multiply(T*LG,start[:,active])
        actual_decoded[:,:,active]=decode_columns(actual,blocks,delta=diff)
        good_decoded[:,:,active]=decode_columns(good,blocks,delta=diff)
    ra=np.zeros((2*D,2*D),complex);rg=np.zeros_like(ra)
    for a in range(2):
        for b in range(2):
            inds_a=2*np.arange(D)+a;inds_b=2*np.arange(D)+b
            ra[np.ix_(inds_a,inds_b)]=actual_decoded[:,:,2*a+b]
            rg[np.ix_(inds_a,inds_b)]=good_decoded[:,:,2*a+b]
    for state in (ra,rg):
        assert norm(state-state.conj().T)<1e-9 and abs(np.trace(state)-1)<1e-9
        assert np.linalg.eigvalsh((state+state.conj().T)/2)[0]>-1e-9
    out={'fixture':'complete 5-qubit-code thermal ports, 28-level controller, one persistent bath qubit and untouched R',
         'initial_state':'sqrt(p0)|0_Q 0_B 0_R> + sqrt(p1)|1_Q 1_B 1_R>, with p the bath Gibbs law; independent thermal syndrome and controller',
         'auxiliary_CB_marginal_Dmax':0.,'arbitrary_reference_kept':True,'bath_reset':False,
         'beta':beta,'T':T,'g':.6,'Gamma':Gamma,'bath_g':.9,
         'independent_full_correlated_Hilbert_space_check_residual':full_residual,
         'joint_Q_C_B_R_trace_distance_to_logical_identity_same_bath_comparison':trace_norm(ra-rg),
         'jump_bad_block_residual':residual,'anticommutator_bad_block_residual':variance_residual,
         'pointwise_dissipator_bounds':normrows,
         'source_only_protection_countermodel':{'J_source_commutator':source_comm,'J_adjoint_source_commutator':adjoint_source,
                                               'missed_generator_trace_norm_at_bad_population_zero':missed,
                                               'scope':'Need full support-algebra protection, including J^dagger J; mere source-column jump protection does not prove the warm-start estimate'},
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'model_sha256':hashlib.sha256((Path(__file__).parent/'port_model.py').read_bytes()).hexdigest(),
         'kernel_sha256':hashlib.sha256((Path(__file__).parent/'quantum_port_controls.py').read_bytes()).hexdigest(),
         'scope':'One correlated finite quantum input plus local norm/countermodel controls; not verification over every input, family size, physical bath, or an experimental device'}
    OUT.mkdir(parents=True,exist_ok=True);path=OUT/'correlated_input_controls.json';path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'passed':True,'output':str(path),'correlated_joint_trace_distance':out['joint_Q_C_B_R_trace_distance_to_logical_identity_same_bath_comparison'],
                      'full_correlated_model_residual':full_residual,'variance_residual':variance_residual,'source_only_countermodel_defect':missed}))


if __name__=='__main__':main()
