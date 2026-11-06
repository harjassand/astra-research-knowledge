"""Reproduce the finite-system compiler, interface barriers, and audits.

All physical resources in the report are requirements, not experiments run.
The small-system independent audits use binary64, explicitly labelled.
"""
import json,time,sys,math,random,hashlib
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
from scipy.linalg import expm
from scipy.special import logsumexp
from threadpoolctl import threadpool_limits
from certified_blocks import *
from logical_circuit import *

ROOT=Path(__file__).resolve().parent

def dump(name,obj):
    (ROOT/name).write_text(json.dumps(serializable(obj),indent=2)+'\n')

def trace_distance(A,B): return float(np.linalg.eigvalsh((A-B+(A-B).conj().T)/2).__abs__().sum()/2)

def dense_hamiltonian(N,p):
    # Independent distinct-site Pauli expansion, not the Schur recurrence.
    from itertools import combinations,permutations
    P=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1])]
    H=np.zeros((1<<N,1<<N),complex)
    for alpha,c in p.items():
        letters=tuple(i for i,k in enumerate(alpha) for _ in range(k)); terms=set(permutations(letters))
        count=math.comb(N,len(letters))*len(terms)
        for sites in combinations(range(N),len(letters)):
            for assignment in terms:
                word=dict(zip(sites,assignment)); M=np.ones((1,1),complex)
                for site in reversed(range(N)): M=np.kron(M,P[word[site]] if site in word else np.eye(2))
                H+=float(N*c/count)*M
    return H

def audit_small():
    start=time.perf_counter(); N=6; beta=Q(2)
    # Every degree <=4, including complex Y terms, is exercised.
    indices=[a for a in __import__('itertools').product(range(5),repeat=3) if 1<=sum(a)<=4]
    p={a:Q((i%7)-3,31) for i,a in enumerate(indices) if i%7!=3}
    blocks,cert=compile_blocks(N,p,beta,(-Q(1,3),Q(1,3)))
    H=dense_hamiltonian(N,p); window=[i for i in range(1<<N) if abs(N-2*i.bit_count())<=N//3]
    constrained=np.zeros_like(H); M=expm(-2*H[np.ix_(window,window)]); M/=np.trace(M)
    constrained[np.ix_(window,window)]=M
    actual=np.zeros_like(H); max_rep=0.; paths=0; max_iso=0.
    for b in blocks:
        A=float_A(b); rho=A@A.conj().T; rho/=np.trace(rho)
        q=float(Q(b['probability_count'],1<<b['probability_bits']))
        fullB,GG=rational_block(N,b['L'],p)
        HB=np.zeros((b['L']+1,b['L']+1),complex)
        for (i,j),v in fullB.items(): HB[i,j]=complex(float(v[0]),float(v[1]))*math.sqrt(float(GG[i]/GG[j]))
        for rank in range(b['multiplicity']):
            V=cg_isometry(unrank_path(N,b['L'],rank)); paths+=1
            max_iso=max(max_iso,float(np.linalg.norm(V.conj().T@V-np.eye(V.shape[1]),2)))
            max_rep=max(max_rep,float(np.linalg.norm(H@V-V@HB,2)))
            W=V[:,b['keep']]; actual+=q/b['multiplicity']*(W@rho@W.conj().T)
    td=trace_distance(actual,constrained); assert td<1e-10 and max_rep<1e-10
    audits=[]
    for block in (blocks[0],blocks[1],blocks[-1]):
        C,meta=emit_component(block,block['multiplicity']-1); state=simulate(C)
        V=cg_isometry(meta['path'])[:,block['keep']]; A=float_A(block); VA=V@A/np.linalg.norm(A)
        target=np.zeros_like(state)
        for i in range(1<<N):
            for j in range(block['d']): target[(i<<meta['physical'][0])+(j<<len(meta['main']))]=VA[i,j]
        phase=np.vdot(target,state); normerr=float(np.linalg.norm(state-target*phase/abs(phase)))
        assert normerr<1e-10
        audits.append(dict(L=block['L'],rank=str(block['multiplicity']-1),gates=len(C.gates),
                           qubits=C.nqubits,norm_error_binary64=normerr,
                           proven_logical_trace_bound=meta['logical_trace_error_bound']))
        if block is blocks[1]: dump('COMPLEX_N6_EXAMPLE_CIRCUIT.json',{'meta':meta,'gates':C.gates})
    canonical=expm(-2*H); canonical/=np.trace(canonical)
    post=np.zeros_like(H); post[np.ix_(window,window)]=canonical[np.ix_(window,window)]
    probability=float(np.trace(post).real); post/=probability
    F=-math.log(float(np.trace(expm(-2*H)).real))/2
    FP=-math.log(float(np.trace(expm(-2*H[np.ix_(window,window)])).real))/2
    result={'scope':'Independent binary64 diagnostics; exact certificates are separate.',
            'N':N,'degree':4,'monomials':len(p),'multiplicity_paths_enumerated':paths,
            'Schur_intertwining_operator_error':max_rep,'CG_isometry_error':max_iso,
            'full_mixed_state_trace_distance':td,'circuit_audits':audits,
            'constrained_vs_postselected_trace_distance':trace_distance(constrained,post),
            'canonical_window_probability':probability,'free_energy_penalty':FP-F,
            'rarity_lower_bound':-math.log(probability)/2,'seconds':time.perf_counter()-start}
    dump('SMALL_SYSTEM_AUDIT.json',result); print(json.dumps(result),flush=True)
    return result

def resource_bound(N,d):
    b=N.bit_length()
    return 16*(d**2)+34*b**3+N*((1<<(b+1))+34*b*b+4)

def benchmark64():
    supplied=json.loads((ROOT/'INPUT_MODEL.json').read_text())
    acq=supplied['acquisition']; g,h=map(Q,supplied['control'])
    p={(0,0,4):Q(-1),(1,0,0):-Q(1,4)-g,(0,0,1):-h}
    N=64; beta=Q(2); records=[]; runs={}
    for label,window in [('canonical',(-1,1)),('window',(-Q(1,4),Q(1,4)))]:
        start=time.perf_counter()
        blocks,cert=compile_blocks(N,p,beta,window,progress=lambda L:print(f'{label}: certified L={L}',flush=True) if L%16==0 else None)
        block_seconds=time.perf_counter()-start
        mode=max(blocks,key=lambda b:b['probability_count'])
        C,meta=emit_component(mode,mode['multiplicity']//2)
        circuit_seconds=time.perf_counter()-start-block_seconds
        maxd=max(b['d'] for b in blocks); G=resource_bound(N,maxd)
        logical_uniform=Q(1,1<<48)*(Q(2*N.bit_length()+N,2)+2+G)
        numerical=beta*cert['delta_H']/2+cert['sector_TV_bound']+cert['purification_trace_error']
        # tanh(x)<=x is used as a simple rational rounding bound above.
        prep_error=numerical+logical_uniform+Q(1,1<<80)
        meanx=meanz=secondz=0.
        for bb in blocks:
            AA=float_A(bb); rr=AA@AA.conj().T; rr/=np.trace(rr)
            qq=float(Q(bb['probability_count'],1<<bb['probability_bits']))
            zz=np.array([(bb['L']-2*k)/N for k in bb['keep']])
            xx=np.zeros((bb['d'],bb['d']))
            for i,k in enumerate(bb['keep'][:-1]):
                xx[i,i+1]=xx[i+1,i]=math.sqrt((k+1)*(bb['L']-k))/N
            meanx+=qq*float(np.trace(rr@xx).real)
            meanz+=qq*float(np.dot(rr.diagonal().real,zz))
            secondz+=qq*float(np.dot(rr.diagonal().real,zz*zz))
        rec=dict(label=label,window=list(map(str,window)),N=N,beta=str(beta),
                 coefficients=[{'alpha':a,'coefficient':str(c)} for a,c in p.items()],
                 sectors=len(blocks),max_block=maxd,stored_entries=cert['stored_entries'],
                 full_Hilbert_dimension=str(1<<N),classical_block_seconds=block_seconds,
                 example_circuit_compile_seconds=circuit_seconds,example_circuit=meta,
                 universal_gate_bound=G,certified_numerical_trace_bound=numerical,
                 all_components_logical_angle_bound=logical_uniform,
                 capped_multiplicity_sampling_failure_bound=Q(1,1<<80),
                 ideal_gate_output_trace_bound=prep_error,
                 free_energy_density_interval=[cert['free_energy_lo']/N-cert['delta_H']/N,
                                               cert['free_energy_hi']/N+cert['delta_H']/N],
                 prior_model_error_nu=acq['coefficient_l1_error'],
                 prior_unknown_model_trace_bound_float=math.tanh(float(beta)*N*acq['coefficient_l1_error_float']/2),
                 model_acquisition_failure_probability='1/20',
                 compressed_response_binary64={'mean_X':meanx,'mean_Z':meanz,'variance_Z':secondz-meanz**2},
                 source_status='Obtained prior digital-source model; no physical source acquisition or gate run.')
        records.append(rec); runs[label]=(blocks,cert)
        dump(f'{label.upper()}_N64_BLOCKS.json',{'blocks':blocks,'certificate':cert})
        dump(f'{label.upper()}_N64_EXAMPLE_CIRCUIT.json',{'meta':meta,'gates':C.gates})
        print(label,'done',block_seconds,circuit_seconds,meta['gates'],float(prep_error),flush=True)
    full,fc=runs['canonical']; restricted,rc=runs['window']
    # Compressed diagnostics compare the two full Hilbert-space states exactly
    # by their Schur blocks. Their floating-point evaluation is labelled.
    pwin=0.; post_blocks={}; energy_leak=0.
    for b in full:
        A=float_A(b); rho=A@A.conj().T; rho/=np.trace(rho)
        q=float(Q(b['probability_count'],1<<b['probability_bits']))
        keep=[i for i in range(b['L']+1) if abs(b['L']-2*i)<=N//4]
        post=q*rho[np.ix_(keep,keep)]; pwin+=float(np.trace(post).real); post_blocks[b['L']]=post
        H,G=rational_block(N,b['L'],p)
        outside=set(range(b['L']+1))-set(keep)
        B=np.zeros((len(outside),len(keep)),complex)
        for ii,i in enumerate(sorted(outside)):
            for jj,j in enumerate(keep):
                v=H.get((i,j),ZERO); B[ii,jj]=complex(float(v[0]),float(v[1]))*math.sqrt(float(G[i]/G[j]))
        if B.size: energy_leak=max(energy_leak,float(np.linalg.norm(B,2)))
    td=0.
    for b in restricted:
        A=float_A(b); rho=A@A.conj().T; rho/=np.trace(rho)
        q=float(Q(b['probability_count'],1<<b['probability_bits']))
        td+=trace_distance(q*rho,post_blocks[b['L']]/pwin)
    penaltylo=rc['free_energy_lo']-fc['free_energy_hi']-rc['delta_H']-fc['delta_H']
    penaltyhi=rc['free_energy_hi']-fc['free_energy_lo']+rc['delta_H']+fc['delta_H']
    result={'runs':records,'hard_window_total_free_energy_penalty_interval':[penaltylo,penaltyhi],
            'compressed_binary64_diagnostics':{'canonical_window_probability':pwin,
                'constrained_vs_postselected_trace_distance':td,
                'rarity_free_energy_lower_bound':-math.log(pwin)/2,
                'native_H_off_window_coupling_norm':energy_leak}}
    dump('FINITE_SYSTEM_CONSTRUCTION.json',result)
    return result

def structural_examples():
    sectors=[]
    for N,beta in [(8,20),(16,32),(64,64)]:
        weights=[]; labels=list(range(0,N+1,2))
        for L in labels:
            energy=Q(L*(L+2)-3*N,N-1)
            weights.append(math.log(multiplicity(N,L)*(L+1))-beta*float(energy))
        p0=math.exp(weights[0]-logsumexp(weights))
        bath=Q(multiplicity(N-1,1),1<<(N-2))
        # A fully rational lower bound on p0 uses exp(-x)<=1/(1+x)^r
        # after splitting x into r equal pieces: e^-x <= (1+x/r)^-r.
        ratio_upper=Q(0); r=128; m0=multiplicity(N,0)
        for L in labels[1:]:
            gap=Q(beta*L*(L+2),N-1)
            term=Q(multiplicity(N,L)*(L+1),m0)/(1+gap/r)**r
            S=1<<96; v=term*S
            ratio_upper+=Q(-((-v.numerator)//v.denominator),S)
        p0lo=1/(1+ratio_upper)
        J2max=Q(N*(N+2),4); J2upper=J2max*(1-p0lo)
        sectors.append({'N':N,'beta':beta,'canonical_J0_probability_binary64':p0,
                        'canonical_J0_probability_certified_lower':p0lo,
                        'tagged_product_bath_reachable_upper':bath,
                        'trace_error_certified_lower':p0lo-bath,
                        'total_spin_squared_certified_upper':J2upper,
                        'fully_separable_total_spin_squared_lower':Q(N,2),
                        'entanglement_witness_tolerated_trace_error':(Q(N,2)-J2upper)/J2max})
    cw=[]
    for N in [8,16,32,64,128,256]:
        beta=2.; J=1.; a=2.; ms=np.arange(-N,N+1,2,dtype=float)
        # Distinct-site normalization: H=-N Azz - h sum Z.
        E=-(ms*ms-N)/(N-1)
        logdeg=np.array([math.log(math.comb(N,k)) for k in range(N+1)])
        h=a/(2*beta*N)
        lp=logdeg-beta*(E-h*ms); lm=logdeg-beta*(E+h*ms)
        qp=np.exp(lp-logsumexp(lp)); qm=np.exp(lm-logsumexp(lm))
        lzero=logdeg-beta*E; qzero=np.exp(lzero-logsumexp(lzero)); w=np.abs(ms)<=N/4
        prob=float(qzero[w].sum()); td=float(abs(qp-qm).sum()/2)
        log2hi=log_bounds(Q(2))[1]
        log_window_upper=(N-1)*log2hi-Q(2)*Q(15,16)*Q(N*N,N-1)
        prob_upper=exp_bounds(log_window_upper)[1]
        log_central_half=(N-1)*log2hi-Q(3,2)*Q(N*N,N-1)
        tail_upper=exp_bounds(log_central_half)[1]
        ratio_lower=(exp_bounds(-Q(1,2))[0]-exp_bounds(-Q(3,2))[1])/(1+exp_bounds(-Q(2))[1])
        separation_lower=(1-tail_upper)*ratio_lower
        cw.append({'N':N,'beta':beta,'field_plus':h,'field_minus':-h,
                   'Gibbs_trace_distance':td,'sharp_uniform_upper':math.tanh(a/2),
                   'Gibbs_trace_distance_certified_lower':separation_lower,
                   'zero_field_mean_magnetization':float(qzero@(ms/N)),
                   'central_window_probability':prob,'hard_window_free_energy_penalty':-math.log(prob)/beta,
                   'central_window_probability_certified_upper':prob_upper,
                   'hard_window_free_energy_penalty_certified_lower':-log_window_upper/2})
    result={'tagged_sector_obstruction':sectors,
            'Curie_Weiss_binary64_diagnostics':cw,
            'scope':'Sector lower bounds exact rational. Curie-Weiss numbers are diagnostic exact-formula evaluations.'}
    dump('STRUCTURAL_RESULTS.json',result); return result

def main():
    t=time.perf_counter(); small=audit_small(); large=benchmark64(); structural=structural_examples()
    dump('RUN_SUMMARY.json',{'total_seconds':time.perf_counter()-t,
                          'physical_experiments':0,'additional_workers':0,
                          'new_infrastructure':0,'physical_shots':0})
    print('COMPLETE seconds',time.perf_counter()-t,flush=True)

if __name__=='__main__':
    with threadpool_limits(limits=1): main()
