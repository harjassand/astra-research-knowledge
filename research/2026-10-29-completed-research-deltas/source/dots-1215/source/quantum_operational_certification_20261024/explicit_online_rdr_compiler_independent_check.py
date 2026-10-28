#!/usr/bin/env python3
"""Independent finite checks of coherent co-CG fallback and sequential intertwiner.
Not an implementation of the high-dimensional asymptotic compiler.
"""
from pathlib import Path
import json, math, itertools
import numpy as np
from causal_random_dimension_reduction_extension_independent_check import IndependentReduction, pmat
ROOT=Path(__file__).resolve().parent

def spin_cg(lam):
    a,b=lam; l=a-b; d=l+1; result={}
    cp=np.zeros((d+1,d,2),complex)
    for t in range(d):
        cp[t,t,0]=math.sqrt((l-t+1)/(l+1))
        cp[t+1,t,1]=math.sqrt((t+1)/(l+1))
    result[(a+1,b)]=cp
    if l:
        cm=np.zeros((d-1,d,2),complex)
        for t in range(d):
            if t:cm[t-1,t,0]=-math.sqrt(t/(l+1))
            if t<l:cm[t,t,1]=math.sqrt((l-t)/(l+1))
        result[(a,b+1)]=cm
    return result

def mem_labels(n):
    return [(a,n-a,u,v) for a in range(n,(n+1)//2-1,-1)
            for u in range(2*a-n+1) for v in range(2*a-n+1)]

def step(n, wrong_phase=False, complex_gauge=False, wrong_conjugation=False):
    old=mem_labels(n-1);new=mem_labels(n);index={z:j for j,z in enumerate(new)}
    V=np.zeros((2,len(new),len(old),2),complex)
    for r,(a,b,u,v) in enumerate(old):
        for mu,C in spin_cg((a,b)).items():
            dl=a-b+1;dm=mu[0]-mu[1]+1
            if complex_gauge and n==3 and (a,b)==(1,1):C=1j*C
            D=math.sqrt(dl/dm)*(C if wrong_conjugation else C.conj()).transpose(2,0,1)
            if wrong_phase and n==3 and (a,b)==(1,1):D=-D
            for un in range(dm):
                for vn in range(dm):
                    z=index[(*mu,un,vn)]
                    for y in range(2):
                        for x in range(2):V[y,z,r,x]=C[un,u,x]*D[y,vn,v]
    return V

def sequential_check():
    Z=np.ones((1,1,1),complex);Zw=Z.copy();Zg=Z.copy();Zbad=Z.copy();records=[]
    for n in range(1,5):
        V=step(n);old=mem_labels(n-1);new=mem_labels(n)
        mat=V.reshape(2*len(new),len(old)*2)
        err=float(np.max(abs(mat.conj().T@mat-np.eye(len(old)*2))))
        Z=np.einsum('ymrx,ora->oymax',V,Z,optimize=True).reshape(2**n,len(new),2**n)
        Vw=step(n,True)
        Zw=np.einsum('ymrx,ora->oymax',Vw,Zw,optimize=True).reshape(2**n,len(new),2**n)
        Vg=step(n,complex_gauge=True)
        Zg=np.einsum('ymrx,ora->oymax',Vg,Zg,optimize=True).reshape(2**n,len(new),2**n)
        Vbad=step(n,complex_gauge=True,wrong_conjugation=True)
        Zbad=np.einsum('ymrx,ora->oymax',Vbad,Zbad,optimize=True).reshape(2**n,len(new),2**n)
        channel=np.einsum('ami,bmj->abij',Z,Z.conj())
        target=IndependentReduction(2,2,n).standard
        rec={'n':n,'memory_dimension':len(new),'local_isometry_error':err,
             'all_matrix_unit_haar_law_error':float(np.max(abs(channel-target))),
             'consistent_complex_edge_gauge_isometry_error':float(np.max(abs(Zg-Z)))}
        assert max(err,rec['all_matrix_unit_haar_law_error'])<1e-12,rec
        records.append(rec)
        if n==3:
            x=np.zeros((8,8));x[2,2]=1
            out=np.einsum('ami,ij,bmj->ab',Zw,x,Zw.conj())
            goal=np.einsum('abij,ij->ab',target,x)
            bad_phase_td=float(np.sum(abs(np.linalg.eigvalsh(out-goal)))/2)
            assert abs(bad_phase_td-1/math.sqrt(3))<1e-12
            outbad=np.einsum('ami,ij,bmj->ab',Zbad,x,Zbad.conj())
            bad_conjugation_td=float(np.sum(abs(np.linalg.eigvalsh(outbad-goal)))/2)
            assert abs(bad_conjugation_td-1/math.sqrt(3))<1e-12
    return {'levels':records,'wrong_relative_edge_phase_trace_distance':bad_phase_td,
            'wrong_coisometry_conjugation_trace_distance':bad_conjugation_td}

# Complete 64-dimensional unitary model of the k=2, mu=(2,1) fallback.
# Wires: predecessor r in {0,1}; padded old irrep b in {0,1,2,3};
# auxiliary i, emitted y, attenuation flag f. After CG, (b,i) encode (nu,c).
def idx(r,b,i,y,f):return ((((r*4+b)*2+i)*2+y)*2+f)
def fallback_check():
    k=2;mu=(2,1);q=2;dim=64;J=8*k*math.ceil(math.sqrt(k))
    theta=math.pi/(4*J+2);amplitude=math.sin(theta)
    dl=[3,1];dm=2
    alpha=[math.sqrt(dm/(k*q*d)) for d in dl]
    attenuation=[amplitude/a for a in alpha]
    H=np.array([[1,1],[1,-1]],complex)/math.sqrt(2)
    # Known attenuation rotation, with computational success f=0.
    A=np.zeros((dim,dim),complex)
    for r in range(2):
        z=attenuation[r];R=np.array([[z,-math.sqrt(1-z*z)],[math.sqrt(1-z*z),z]])
        for b in range(4):
            for i in range(2):
                for y in range(2):
                    for f in range(2):
                        for fp in range(2):A[idx(r,b,i,y,fp),idx(r,b,i,y,f)]=R[fp,f]
    # Bell preparation on (i,y): H_y then CNOT(y -> i).
    Bell=np.zeros_like(A)
    for r in range(2):
        for b in range(4):
            for i in range(2):
                for y in range(2):
                    for f in range(2):
                        for yp in range(2):Bell[idx(r,b,i^yp,yp,f),idx(r,b,i,y,f)]=H[yp,y]
    # Ordinary known CG, conjugated. The chosen concrete coefficients are real.
    blocks=[]
    for r,lam in enumerate([(2,0),(1,1)]):
        U=np.zeros((8,8),complex);cg=spin_cg(lam)
        usedin=[];usedout=[]
        for nu,C in cg.items():
            flag=1 if nu==mu else 0
            for c in range(C.shape[0]):
                for b in range(C.shape[1]):
                    for i in range(2):U[flag*4+c,b*2+i]=C[c,b,i].conjugate()
            usedin.extend(range(C.shape[1]*2));usedout.extend(flag*4+c for c in range(C.shape[0]))
        ins=[z for z in range(8) if z not in usedin];outs=[z for z in range(8) if z not in usedout]
        for a,b in zip(outs,ins):U[a,b]=1
        assert np.max(abs(U.conj().T@U-np.eye(8)))<1e-12
        blocks.append(U)
    CG=np.zeros_like(A)
    for r in range(2):
        for b in range(4):
            for i in range(2):
                for y in range(2):
                    for f in range(2):
                        for packed in range(8):
                            bp,ip=divmod(packed,2)
                            CG[idx(r,bp,ip,y,f),idx(r,b,i,y,f)]=blocks[r][packed,b*2+i]
    erase=np.zeros_like(A)
    for r in range(2):
        for b in range(4):
            for i in range(2):
                for y in range(2):
                    for f in range(2):
                        for rp in range(2):erase[idx(rp,b,i,y,f),idx(r,b,i,y,f)]=H[rp,r]
    W=erase@CG@Bell@A
    assert np.max(abs(W.conj().T@W-np.eye(dim)))<1e-12
    ins=[idx(0,b,0,0,0) for b in range(3)]+[idx(1,0,0,0,0)]
    # nu=1 means packed (b,i)=4+c, c=0,1.
    outs=[idx(0,(4+c)//2,(4+c)%2,y,0) for y in range(2) for c in range(2)]
    F=np.column_stack([math.sqrt(d/dm)*spin_cg(lam)[mu].conj().transpose(2,0,1).reshape(4,d)
                       for d,lam in zip(dl,[(2,0),(1,1)])])
    assert np.max(abs(F.conj().T@F-np.eye(4)))<1e-12
    block=W[np.ix_(outs,ins)]
    blockerr=float(np.max(abs(block-amplitude*F)))
    rin=np.eye(dim);rout=np.eye(dim)
    rin[ins,ins]=-1;rout[outs,outs]=-1
    Q=-W@rin@W.conj().T@rout
    V=W[:,ins]
    for _ in range(J):V=Q@V
    desired=np.zeros_like(V);desired[outs,:]=F
    fullerr=float(np.linalg.norm(V-desired,2))
    leakage=float(np.linalg.norm(np.delete(V,outs,axis=0),2))
    # Off-diagonal input r=0 to r=1 is required; tracing r instead of coherent erasure loses it.
    psi=np.array([1,0,0,1],complex)/math.sqrt(2)
    ideal=F@psi;dephased=0.5*np.outer(F[:,0],F[:,0].conj())+0.5*np.outer(F[:,3],F[:,3].conj())
    missingerase=float(np.sum(abs(np.linalg.eigvalsh(np.outer(ideal,ideal.conj())-dephased)))/2)
    rec={'k':k,'mu':mu,'full_unitary_dimension':dim,'input_domain_dimension':len(ins),
         'output_range_dimension':len(outs),'ordinary_cg_block_count':len(blocks),
         'raw_singular_amplitudes':alpha,'attenuation_coefficients':attenuation,
         'oaa_iterations':J,'common_success_amplitude':amplitude,
         'success_block_error':blockerr,'full_oaa_isometry_operator_error':fullerr,
         'all_failure_flag_leakage_operator_norm':leakage,
         'missing_predecessor_erasure_trace_distance':missingerase}
    assert max(blockerr,fullerr,leakage)<1e-11,rec
    assert abs(missingerase-0.5)<1e-12
    return rec


def target_schur_family(N):
    family=[{'rows':{((0,0),0,()):np.ones(1,complex)},'paths':{(0,0):[()]},'dims':{(0,0):1}}]
    for n in range(1,N+1):
        rows={}
        for (lam,a,path),row in family[-1]['rows'].items():
            for mu,C in spin_cg(lam).items():
                for b in range(C.shape[0]):
                    key=(mu,b,path+(mu,));rows.setdefault(key,np.zeros(2**n,complex))
                    for i in range(2):rows[key]+=C[b,a,i]*np.kron(row,np.eye(2)[i])
        paths={lam:sorted({p for l,q,p in rows if l==lam}) for lam,q,p in rows}
        dims={lam:lam[0]-lam[1]+1 for lam in paths}
        matrix=np.array(list(rows.values()))
        assert np.max(abs(matrix@matrix.conj().T-np.eye(2**n)))<1e-12
        family.append({'rows':rows,'paths':paths,'dims':dims})
    return family

def rectangular_embedding_check(s=3,N=4):
    rng=np.random.default_rng(202610272051)
    target=target_schur_family(N)
    physical=[{'emb':{((0,0),()):np.ones((1,1),complex)},'dims':{(0,0):1}}]
    branching_residual=0.
    for n in range(1,N+1):
        permutations=list(itertools.permutations(range(n)))
        psmall=[pmat(2,n,p) for p in permutations]
        plarge=[pmat(s,n,p) for p in permutations]
        emb={};dims={}
        for lam,paths in target[n]['paths'].items():
            # Read SAME Specht matrices from target spin-CG Schur basis.
            rows=np.array([target[n]['rows'][(lam,0,p)] for p in paths])
            specht=[rows@P@rows.conj().T for P in psmall]
            f=len(paths)
            E00=sum(D[0,0].conjugate()*P for D,P in zip(specht,plarge))*f/math.factorial(n)
            vals,vecs=np.linalg.eigh((E00+E00.conj().T)/2)
            basis=vecs[:,vals>0.5];d=basis.shape[1];dims[lam]=d
            # Arbitrary complex physical irrep basis gauge must NOT affect multiplicities.
            gauge,_=np.linalg.qr(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))
            basis=basis@gauge
            for j,path in enumerate(paths):
                E=sum(D[j,0].conjugate()*P for D,P in zip(specht,plarge))*f/math.factorial(n)
                emb[(lam,path)]=E@basis
        matrix=np.column_stack(list(emb.values()))
        assert np.max(abs(matrix.conj().T@matrix-np.eye(matrix.shape[1])))<1e-11
        physical.append({'emb':emb,'dims':dims})
    # Extract physical CG on a canonical prefix path; independently verify all paths agree.
    cg={}
    for n in range(1,N+1):
        for lam,oldpaths in target[n-1]['paths'].items():
            for mu in spin_cg(lam):
                if mu not in target[n]['paths']:continue
                tensors=[]
                for path in oldpaths:
                    a=physical[n-1]['emb'][(lam,path)]
                    b=physical[n]['emb'][(mu,path+(mu,))]
                    G=b.conj().T@np.kron(a,np.eye(s))
                    tensors.append(G.reshape(physical[n]['dims'][mu],physical[n-1]['dims'][lam],s))
                cg[(n,lam,mu)]=tensors[0]
                for G in tensors:branching_residual=max(branching_residual,float(np.max(abs(G-tensors[0]))))
    assert branching_residual<1e-11,branching_residual
    labels=lambda n:[(lam,a,b) for lam,ds in physical[n]['dims'].items()
                     for a in range(ds) for b in range(target[n]['dims'][lam])]
    Z=np.ones((1,1,1),complex);records=[]
    w,_=np.linalg.qr(rng.normal(size=(s,2))+1j*rng.normal(size=(s,2)))
    wn=np.ones((1,1),complex)
    for n in range(1,N+1):
        old,new=labels(n-1),labels(n);ind={z:i for i,z in enumerate(new)}
        V=np.zeros((2,len(new),len(old),s),complex)
        for r,(lam,a,b) in enumerate(old):
            for mu,Ck in spin_cg(lam).items():
                if mu not in physical[n]['dims']:continue
                Gs=cg[(n,lam,mu)]
                dl,dm=Ck.shape[1],Ck.shape[0]
                F=math.sqrt(dl/dm)*Ck.conj().transpose(2,0,1)
                for ap in range(physical[n]['dims'][mu]):
                    for bp in range(dm):
                        mem=ind[(mu,ap,bp)]
                        for y in range(2):
                            for x in range(s):V[y,mem,r,x]=Gs[ap,a,x]*F[y,bp,b]
        Z=np.einsum('ymrx,ora->oymax',V,Z,optimize=True).reshape(2**n,len(new),s**n)
        wn=np.kron(wn,w)
        restricted=np.einsum('ami,ip->amp',Z,wn,optimize=True)
        channel=np.einsum('ami,bmj->abij',restricted,restricted.conj())
        targetmap=IndependentReduction(2,2,n).standard
        law=float(np.max(abs(channel-targetmap)))
        flat=restricted.reshape(2**n*len(new),2**n)
        nofail=float(np.max(abs(flat.conj().T@flat-np.eye(2**n))))
        rec={'s':s,'k':2,'n':n,'valid_memory_dimension':len(new),
             'random_complex_common_embedding_all_matrix_unit_error':law,
             'promised_subspace_no_failure_error':nofail}
        assert max(law,nofail)<1e-10,rec
        records.append(rec)
    return {'method':'Physical CG extracted from common Specht matrix units, with random complex physical-irrep gauges and one random complex W; finite algebra test, not execution of imported high-dimensional circuit.',
            'physical_branching_path_independence_error':branching_residual,'levels':records}

if __name__=='__main__':
    result={'scope':'Finite explicit full-unitary fallback and U(2) sequential intertwiner checks; not hardware or high-dimensional circuit execution.',
            'fallback':fallback_check(),'sequential_same_dimension':sequential_check(),
            'rectangular_common_embedding':rectangular_embedding_check(),'pass':True}
    (ROOT/'explicit_online_rdr_compiler_independent_check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
