"""Full finite quantum channels with all Pauli thermal ports and controllers.

Exact conserved-charge block decomposition; no controller elimination.
Verified against an independently assembled small full Hilbert-space model.
The complete [[5,1,3]] fixture is NOT the three-dimensional memory family.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.sparse import bmat,csr_matrix,diags,eye,kron
from scipy.sparse.linalg import expm_multiply
from port_model import I,X,Y,Z,ten,norm,perfect_code,ports,charge_hamiltonians

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/thermal_ports_20261101'


def kernel(blocks,beta,Gamma=.7,good=False,delta=0):
    hs=blocks['H_good' if good else 'H'];D=blocks['block_dimension']
    C=blocks['C'];B=blocks['B'];idn=eye(D,format='csr',dtype=complex)
    rates=np.exp(-beta*blocks['gaps'][1:]);anti=np.zeros(D)
    jumps=[]
    for c in range(1,C):
        j=np.zeros((D,D),complex)
        for q in range(2):
            for b in range(B):j[q*C*B+b,q*C*B+c*B+b]=1
        j=csr_matrix(j)
        jumps.extend([(blocks['tags'][c],Gamma*kron(j.conj(),j,format='csr')),
                      (blocks['tags'][c],Gamma*rates[c-1]*kron(j.T,j.conj().T,format='csr'))])
        for q in range(2):
            for b in range(B):
                anti[q*C*B+c*B+b]+=Gamma
                anti[q*C*B+b]+=Gamma*rates[c-1]
    ant=diags(anti,format='csr')
    common=-(kron(idn,ant,format='csr')+kron(ant.T,idn,format='csr'))/2
    layout=[[None]*16 for _ in range(16)]
    for k in range(16):
        layout[k][k]=-1j*(kron(idn,hs[k],format='csr')-kron(hs[k^delta].T,idn,format='csr'))+common
        for tag,superjump in jumps:
            target=k^tag
            layout[target][k]=superjump if layout[target][k] is None else layout[target][k]+superjump
    return bmat(layout,format='csr')


def thermal(beta,energies):
    p=np.exp(-beta*np.array(energies,dtype=float));return p/p.sum()


def initial_channels(model,blocks,beta,bath_prob=None):
    D=blocks['block_dimension'];C=blocks['C'];B=blocks['B'];A=C*B
    ps=thermal(beta,model['energies']);pc=thermal(beta,blocks['gaps'])
    pb=thermal(beta,[0,blocks['bath_gap']]) if bath_prob is None and B==2 else np.ones(1)
    if bath_prob is not None:pb=np.array(bath_prob)
    initial=np.zeros((16*D*D,4),complex)
    for k in range(16):
        for c in range(C):
            for b in range(B):
                s=k^blocks['tags'][c]^(blocks['bath_tag'] if b else 0)
                w=ps[s]*pc[c]*pb[b];a=c*B+b
                for q in range(2):
                    for v in range(2):initial[k*D*D+(q*A+a)+D*(v*A+a),2*q+v]=w
    return initial,ps,pc,pb


def decode_columns(columns,blocks,delta=0):
    D=blocks['block_dimension'];C=blocks['C'];B=blocks['B'];A=C*B
    out=np.zeros((D,D,columns.shape[1]),complex)
    tags=[blocks['tags'][c]^(blocks['bath_tag'] if b else 0) for c in range(C) for b in range(B)]
    for k in range(16):
        r=columns[k*D*D:(k+1)*D*D,:].reshape((D,D,-1),order='F')
        for a in range(A):
            for b in range(A):
                if tags[a]^tags[b]!=delta:continue
                for q in range(2):
                    for v in range(2):out[q*A+a,v*A+b,:]+=r[q*A+a,v*A+b,:]
    return out


def choi(columns,blocks):
    decoded=decode_columns(columns,blocks);D=blocks['block_dimension']
    jj=np.zeros((2*D,2*D),complex)
    for a in range(2):
        for b in range(2):
            jj[np.ix_(2*np.arange(D)+a,2*np.arange(D)+b)]=decoded[:,:,2*a+b]/2
    return jj


def target_choi(pc,pb):
    env=np.kron(pc,pb);A=len(env);out=np.zeros((4*A,4*A),complex)
    for q in range(2):
        for v in range(2):
            for a,p in enumerate(env):out[(q*A+a)*2+q,(v*A+a)*2+v]=p/2
    return out


def trace_norm(a):return float(np.abs(np.linalg.eigvalsh((a+a.conj().T)/2)).sum())


def metrics(jj,target):
    assert norm(jj-jj.conj().T)<1e-9
    assert abs(np.trace(jj)-1)<1e-8
    assert np.linalg.eigvalsh((jj+jj.conj().T)/2)[0]>-1e-8
    A=jj.shape[0]//4;jq=np.zeros((4,4),complex)
    for q in range(2):
        for v in range(2):
            for r in range(2):
                for s in range(2):jq[2*q+r,2*v+s]=sum(jj[(q*A+a)*2+r,(v*A+a)*2+s] for a in range(A))
    bell=np.array([1,0,0,1],complex)/np.sqrt(2)
    logical=trace_norm(jq-np.outer(bell,bell.conj()))
    joint=trace_norm(jj-target)
    bell_basis=np.array([[1,1,0,0],[0,0,1,1],[0,0,1,-1],[1,-1,0,0]],complex)/np.sqrt(2)
    bell_matrix=bell_basis.conj().T@jq@bell_basis
    offdiag=float(np.max(np.abs(bell_matrix-np.diag(np.diag(bell_matrix)))))
    assert offdiag<1e-9
    probs=np.real(np.diag(bell_matrix))
    return {'logical_choi_distance':logical,'logical_diamond_upper':min(2,2*logical),
            'logical_Pauli_diamond':float(2*(1-probs[0])),
            'logical_Pauli_probabilities':{'I':float(probs[0]),'X':float(probs[2]),'Y':float(probs[3]),'Z':float(probs[1])},
            'logical_Bell_offdiagonal_residual':offdiag,
            'logical_X_Y_Z_retention':[float(np.real(np.trace(np.kron(p,p.T)@jq))) for p in (X,Y,Z)],
            'joint_controller_bath_choi_distance':joint,'joint_channel_diamond_upper':min(2,2*joint),
            'entanglement_infidelity':float(np.real(1-bell.conj()@jq@bell)),
            'minimum_Choi_eigenvalue':float(np.linalg.eigvalsh((jj+jj.conj().T)/2)[0])}


def reset_syndrome(columns,blocks):
    """Ideal scheduled Dec then ground-code Enc, retaining controllers/bath."""
    out=decode_columns(columns,blocks);D=blocks['block_dimension'];C=blocks['C'];B=blocks['B'];A=C*B
    tags=[blocks['tags'][c]^(blocks['bath_tag'] if b else 0) for c in range(C) for b in range(B)]
    result=np.zeros_like(columns)
    for a in range(A):
        for b in range(A):
            if tags[a]!=tags[b]:continue
            k=tags[a]
            for q in range(2):
                for v in range(2):result[k*D*D+q*A+a+D*(v*A+b),:]=out[q*A+a,v*A+b,:]
    return result


def full_model_check(model,entries,beta,g=.6,Gamma=.7):
    # Small two-port fixture, assembled on the full PHYSICAL data Hilbert
    # space, independently of total-charge block Hamiltonian assembly.
    sub=[next(p for p in entries if p['label']=='XIIII' and p['omega']==1),
         next(p for p in entries if p['label']=='IZIII' and p['omega']==2)]
    blocks=charge_hamiltonians(model,sub,g=g);C=3;D=32*C
    h=np.kron(model['H0'],np.eye(C))+np.kron(np.eye(32),np.diag(blocks['gaps']))
    U=model['recovery_unitary']
    jumps=[]
    for c,p in enumerate(sub,1):
        up=np.zeros((C,C),complex);up[c,0]=1
        physical=U@p['operator']@U.conj().T
        b=g*np.kron(physical,up);h+=b+b.conj().T
        j=np.kron(np.eye(32),up.conj().T);jumps.extend([np.sqrt(Gamma)*j,np.sqrt(Gamma*np.exp(-beta*p['omega']))*j.conj().T])
    ident=eye(D,format='csr',dtype=complex);hh=csr_matrix(h)
    L=-1j*(kron(ident,hh)-kron(hh.T,ident))
    for j in jumps:
        j=csr_matrix(j);a=j.conj().T@j
        L+=kron(j.conj(),j)-(kron(ident,a)+kron(a.T,ident))/2
    small,ps,pc,pb=initial_channels(model,blocks,beta)
    start=[]
    for a in range(2):
        for b in range(2):
            r=np.zeros((32,32),complex)
            for s in range(16):r[a*16+s,b*16+s]=ps[s]
            start.append(np.kron(U@r@U.conj().T,np.diag(pc)).reshape(-1,order='F'))
    T=.7;full=expm_multiply(T*L,np.stack(start,axis=1))
    reduced=expm_multiply(T*kernel(blocks,beta,Gamma),small)
    err=0.
    for col in range(4):
        r=full[:,col].reshape((D,D),order='F');frame=np.kron(U,np.eye(C));r=frame.conj().T@r@frame
        rebuilt=np.zeros_like(r)
        for k in range(16):
            b=reduced[k*36:(k+1)*36,col].reshape((6,6),order='F')
            inds=[(q*16+(k^blocks['tags'][c]))*C+c for q in range(2) for c in range(C)]
            rebuilt[np.ix_(inds,inds)]=b
        err=max(err,float(np.max(np.abs(r-rebuilt))))
    assert err<1e-10
    return err


def main():
    model=perfect_code();entries=ports(model);g=.6;Gamma=.7
    residual=full_model_check(model,entries,beta=2.,g=g,Gamma=Gamma)
    rows=[];equilibrium=[]
    for beta in (2.,4.,8.):
        blocks=charge_hamiltonians(model,entries,g=g)
        L=kernel(blocks,beta,Gamma);initial,ps,pc,pb=initial_channels(model,blocks,beta)
        target=target_choi(pc,pb)
        # Mixed logical state is the exact joint stationary reference.
        stationary=(initial[:,0]+initial[:,3])/2
        stationarity=float(np.max(np.abs(L@stationary)))
        assert stationarity<1e-11
        times=(0.,2.,10.,30.)
        for T in times:
            evolved=initial if T==0 else expm_multiply(T*L,initial)
            jj=choi(evolved,blocks);row={'beta':beta,'T':T,**metrics(jj,target)}
            rows.append(row)
        # Strong scheduled reference has EXACTLY the same port dynamics,
        # retaining C, plus ideal instantaneous data recovery every 2 units.
        scheduled=initial.copy()
        for _ in range(5):scheduled=reset_syndrome(expm_multiply(2*L,scheduled),blocks)
        rows.append({'beta':beta,'T':10.,'ideal_scheduled_recovery_period':2.,
                     'ideal_recovery_rounds':5,**metrics(choi(scheduled,blocks),target)})
        equilibrium.append({'beta':beta,'stationarity_max_residual':stationarity,
                            'ground_syndrome_probability':float(ps[0]),
                            'bad_probability_per_seed':{s['label']:float(ps[s['bad_syndromes']].sum()) for s in model['seeds']},
                            'equilibrium_controller_jump_rate':float(2*Gamma*(1-pc[0])),
                            'controller_levels':blocks['C']})
        print(json.dumps({'beta_complete':beta,'last_uncontrolled':rows[-2],
                          'same_device_ideal_scheduled':rows[-1]}),flush=True)
    # A single persistent bath qubit has no reset and couples coherently to
    # the data through one additional energy-conserving local port.
    bp=next(p for p in entries if p['label']=='IIXII' and p['omega']==2).copy();bp['g']=.9
    beta=4.;blocks=charge_hamiltonians(model,entries,g=g,bath=bp)
    L=kernel(blocks,beta,Gamma);LG=kernel(blocks,beta,Gamma,good=True)
    bathrows=[]
    for label,prob in (('thermal',None),('excited',[0.,1.])):
        initial,ps,pc,pb=initial_channels(model,blocks,beta,bath_prob=prob)
        T=10.;actual=expm_multiply(T*L,initial);comparison=expm_multiply(T*LG,initial)
        jj=choi(actual,blocks);jg=choi(comparison,blocks)
        d=trace_norm(jj-jg)
        # Logical-erased comparison retains and evolves the SAME bath.
        A=blocks['A'];logical_check=0.
        for a in range(2):
            for b in range(2):
                col=decode_columns(comparison,blocks)[:,:,2*a+b]
                template=decode_columns(comparison,blocks)[:A,:A,0]
                e=np.zeros((2,2),complex);e[a,b]=1
                logical_check=max(logical_check,norm(col-np.kron(e,template)))
        assert logical_check<1e-9
        thermal_b=thermal(beta,[0,blocks['bath_gap']])
        M=float(max(pb/thermal_b))
        bathrows.append({'bath_initial':label,'T':T,'bath_reset':False,
                         'bath_coupling':bp['g'],'initial_bath_Dmax':float(np.log(M)),
                         'joint_Choi_distance_to_same_bath_comparison':d,
                         'joint_Q_input_diamond_upper':min(2,2*d),
                         'logical_identity_comparison_residual':logical_check,
                         **metrics(jj,target_choi(pc,pb))})
        print(json.dumps({'bath_complete':label,'joint_same_bath_choi_distance':d}),flush=True)
    out={'fixture':'all 15 Pauli seeds of [[5,1,3]], 27 thermal ports on one 28-level controller; optional one persistent bath qubit; not the 3D family',
         'g':g,'Gamma':Gamma,'controller_elimination':False,
         'independent_full_Hilbert_space_check_residual':residual,
         'rows':rows,'equilibrium':equilibrium,'persistent_bath':bathrows,
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'model_sha256':hashlib.sha256((Path(__file__).parent/'port_model.py').read_bytes()).hexdigest(),
         'scope':'Floating full finite-controller unknown-input/reference channels with all Pauli ports and retained C/B. The conserved-charge representation is exact and independently checked in a smaller full model. No asymptotic family, hardware, useful threshold, or practical advantage is inferred.',
         'scheduled_scope':'Ideal instantaneous data syndrome recovery every 2 time units, same actual port Hamiltonian and reservoirs, controllers retained; hardware errors, circuit time and reset cost of recovery are not supplied.'}
    OUT.mkdir(parents=True,exist_ok=True);path=OUT/'quantum_port_controls.json';path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'passed':True,'output':str(path),'full_model_residual':residual}))


if __name__=='__main__':main()
