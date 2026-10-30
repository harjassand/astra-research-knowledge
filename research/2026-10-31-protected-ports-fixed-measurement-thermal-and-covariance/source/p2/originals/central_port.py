"""Full-Fock outer-permutation subsystem and central particle port.

Proves the algebraic no-dark-factor part by an exact modular rank
certificate on the 20-dimensional outer gauge. It does not turn that
algebraic fact into a relaxation-rate assertion. Sequential tunnelling
in a charge plateau can be thermally activated.
"""
import math
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from orbital_echo import fermion_ops, orbital_permutation
from star_subsystem import row_reduce_mod, inverse_mod, range_basis


def permutation(sites):
    return orbital_permutation([2*s+spin for s in sites for spin in range(2)]).real


def representation(sites=4):
    if sites==4:
        C=permutation([0,2,3,1]); T=permutation([0,1,3,2])
        rank=80
    elif sites==3:
        C=permutation([1,2,0]); T=permutation([0,2,1]); rank=20
    I=np.eye(len(C)); pe=(2*I-C-C@C)/3; pp=pe@(I+T)/2
    vp=range_basis(pp,rank)
    vm=(2/math.sqrt(3))*((I-T)/2)@C@vp
    W=np.column_stack([vp,vm])
    return C,T,pp,W


def outer_algebra_certificate(p=1000003):
    C,T,_,_=representation(3); C=C.astype(np.int64); T=T.astype(np.int64)
    I=np.eye(64,dtype=np.int64)
    pp=((2*I-C-C@C)*pow(3,-1,p)%p)@((I+T)*pow(2,-1,p)%p)%p
    _,cols=row_reduce_mod(pp,p); B=pp[:,cols]
    _,rows=row_reduce_mod(B.T,p); L=inverse_mod(B[rows,:],p)
    c=[a.real.astype(np.int64) for a in fermion_ops(6)]
    n=[a.T@a for a in c]; D=sum(n[2*j]@n[2*j+1] for j in range(3))
    cp=sum(c[0::2]); cm=sum(c[1::2])
    operators=[cp,cp.T,cm,cm.T,D]
    coord=[L@((A@B%p)[rows,:])%p for A in operators]
    assert len(cols)==20
    eye=np.eye(20,dtype=np.int64)
    stacked=np.vstack([np.kron(eye,A.T)-np.kron(A,eye) for A in coord])%p
    _,piv=row_reduce_mod(stacked,p)
    assert len(piv)==399
    return dict(prime=p,outer_gauge_dimension=20,commutator_rank=len(piv),
                commutant_dimension=400-len(piv),
                independent_columns=cols,independent_rows=rows,
                claim='Exact nonzero modular minor certifies scalar joint commutant of C_up,C_down,their adjoints,and sum of outer doublons; not a mixing-rate claim.')


def physical_model(Uc=1.,Uo=1.,t=.1,epsilon=.2,Vc=0.,Vo=0.,mu=.5):
    c=fermion_ops(8); ns=[a.conj().T@a for a in c]
    n=[ns[2*j]+ns[2*j+1] for j in range(4)]
    D=[ns[2*j]@ns[2*j+1] for j in range(4)]
    N=sum(n)
    hop=-sum(c[s].conj().T@c[2*j+s]+c[2*j+s].conj().T@c[s]
             for j in range(1,4) for s in range(2))
    H=(Uc*D[0]+Uo*sum(D[1:])+t*hop+epsilon*n[0]
       +Vc*n[0]@sum(n[1:])+Vo*sum(n[i]@n[j] for i in range(1,4) for j in range(i+1,4)))
    S=[]
    for j in range(4):
        plus=c[2*j].conj().T@c[2*j+1]
        minus=plus.conj().T
        S.append([(plus+minus)/2,(plus-minus)/(2j),(ns[2*j]-ns[2*j+1])/2])
    Stotal=[sum(s[k] for s in S) for k in range(3)]
    S2=sum(s@s for s in Stotal)
    return dict(c=c,n=n,N=N,D=D,H=H,K=H-mu*N,S2=S2,spin=S,
                parameters=dict(Uc=Uc,Uo=Uo,t=t,epsilon=epsilon,Vc=Vc,Vo=Vo,mu=mu))


def factor(A,W):
    d=W.shape[1]//2; a=W.conj().T@A@W; g=(a[:d,:d]+a[d:,d:])/2
    return g,float(np.linalg.norm(a-np.kron(np.eye(2),g),2)),float(np.linalg.norm(A@W-W@a,2))


def spectrum(W,**parameters):
    m=physical_model(**parameters); Hg,_,_=factor(m['K'],W)
    e,v=eigh(Hg); ng=factor(m['N'],W)[0]; sg=factor(m['S2'],W)[0]
    ne=np.diag(v.conj().T@ng@v).real; se=np.diag(v.conj().T@sg@v).real
    # Degenerate numerical eigenvectors can mix different N,S eigenstates;
    # the ground is nondegenerate and its labels are decisive.
    thermal=[]
    for beta in [40.,100.,200.,400.]:
        p=np.exp(-beta*(e-e[0])); p/=sum(p)
        thermal.append(dict(beta=beta,ground_population=float(p[0]),
                            mean_particles=float(p@ne),mean_S_squared=float(p@se)))
    ground=v[:,0]
    amps=[]
    for c in m['c'][:2]:
        cg=factor(c,W)[0]
        amps.append(abs(v.conj().T@cg@ground)**2)
        amps.append(abs(v.conj().T@cg.conj().T@ground)**2)
    # Relevant addition/removal gaps, not merely the mathematical spectrum.
    transition=sum(amps)
    significant=(transition>1e-10)&(e>e[0]+1e-10)
    return dict(parameters=m['parameters'],gauge_ground_energy=float(e[0]),
                gauge_gap=float(e[1]-e[0]),ground_particles=float(ne[0]),
                ground_S_squared=float(se[0]),
                first_12_gaps=(e[:12]-e[0]).tolist(),
                thermal=thermal,
                minimum_central_particle_transition_gap=float(min(e[significant]-e[0]))
                if np.any(significant) else None)


def run():
    C,T,pp,W=representation(4); m=physical_model()
    checks={}
    for name,A in [('H',m['H']),('central_annihilate_up',m['c'][0]),
                   ('central_annihilate_down',m['c'][1]),
                   ('central_Sx',m['spin'][0][0]),('central_Sy',m['spin'][0][1]),
                   ('outer_collective_Sz',sum(s[2] for s in m['spin'][1:]))]:
        _,err,leak=factor(A,W)
        checks[name]=dict(factor_residual=err,range_leakage=leak)
        assert max(err,leak)<1e-12
    result=dict(full_fock_dimension=256,characters=dict(identity=256,transposition=int(np.trace(T)),three_cycle=int(np.trace(C))),
                multiplicities=dict(trivial=48,sign=48,standard=80),
                logical_dimension=2,gauge_dimension=80,
                generator_checks=checks,
                exact_outer_certificate=outer_algebra_certificate(),
                spectral_examples=[spectrum(W),spectrum(W,epsilon=.4),
                                   spectrum(W,Vc=.0553,Vo=.0146,epsilon=.1186,mu=.6)],
                caveats=['Invariant operations cannot prepare an E resource from the vacuum.',
                         'Algebraic primitivity is not a useful rate; sequential spin renewal can require thermally activated particle excursions.',
                         'Independent identical outer leads are only covariant and do not commute with the system representation individually.',
                         'The one-edge active force is not an identity on arbitrary gauge states.'])
    Path(__file__).with_name('central_port_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__': run()
