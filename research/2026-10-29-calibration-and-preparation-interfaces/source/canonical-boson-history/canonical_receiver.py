"""Canonical conjugate-boson receiver using a finite positive HS alphabet.

No external solver/source-code import. Shen2020's canonical recurrence and
ordinary positive trigonometric quadrature are credited in PROOF.md.
The hot loop uses binary64, not interval arithmetic. RNG is a finite seeded
PCG64 realization, separately from the ideal independent-fair-bit theorem.
"""
from __future__ import annotations
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path
import time

import mpmath as mp
import numpy as np
from scipy.linalg import eigh, expm
from scipy.stats import beta as beta_distribution

HERE=Path(__file__).resolve().parent
mp.mp.dps=110


def positive_root_two(degree,bits=100):
    n=int(mp.floor(mp.power(2,mp.mpf(1)/degree)*2**bits))
    rhs=2*(2**bits)**degree
    assert n**degree<=rhs<(n+1)**degree
    lo,hi=F(n,2**bits),F(n+1,2**bits)
    return (lo+hi)/2,lo,hi


def fm(x):return mp.mpf(x.numerator)/x.denominator
def frac(x):return {'numerator':str(x.numerator),'denominator':str(x.denominator)}


def phase_quadrature(K,L,probability_bits=60,phase_bits=90):
    """beta=log2,U=1/2: moments r^(-m²), r=2^(1/(2L))."""
    assert K>=2 and K%2==0, 'Executable real-orthogonal compiler is restricted to even K.'
    start=time.perf_counter()
    r,rlo,rhi=positive_root_two(2*L)
    mu=[fm(r)**(-m*m) for m in range(K+1)]
    G=mp.matrix([[mu[abs(i-j)] for j in range(K+1)] for i in range(K+1)])
    V=mp.cholesky(G).T
    A=V[:,:K];B=V[:,1:]
    aperp=mp.matrix(K+1,1);aperp[K]=1
    bperp=mp.matrix(K+1,1);bperp[K]=1
    top=B[:K,:].T;bottom=B[K,:].T
    sol=mp.lu_solve(top,-bottom)
    for i in range(K):bperp[i]=sol[i]
    bperp/=mp.norm(bperp)
    partial=B*(A.T*A)**-1*A.T
    U=partial+bperp*aperp.T
    if mp.det(U)<0:U=partial-bperp*aperp.T
    unitary_error=mp.norm(U.T*U-mp.eye(K+1))
    assert unitary_error<mp.mpf('1e-80')
    eigenvalues,eigenvectors=mp.eig(U)
    pairs=[];zero_weight=None
    for j,z in enumerate(eigenvalues):
        vec=eigenvectors[:,j];vec/=mp.norm(vec)
        w=abs((vec.conjugate().T*V[:,0])[0])**2
        if abs(z-1)<mp.mpf('1e-60'):
            zero_weight=w
        elif mp.im(z)>mp.mpf('1e-60'):
            pairs.append((mp.arg(z),w))
    assert zero_weight is not None and len(pairs)==K//2
    pairs.sort()
    scale=1<<probability_bits
    atoms=[complex(1)];exact_atoms=[(F(1),F(0))];tickets=[0]
    for theta,w in pairs:
        tangent=int(mp.nint(mp.tan(theta/2)*2**phase_bits))
        t=F(tangent,2**phase_bits)
        re=(1-t*t)/(1+t*t);im=2*t/(1+t*t)
        assert re*re+im*im==1
        amount=int(mp.nint(w*scale))
        assert amount>0
        for sign in (1,-1):
            atoms.append(complex(float(re),sign*float(im)))
            exact_atoms.append((re,sign*im));tickets.append(amount)
    tickets[0]=scale-sum(tickets)
    assert tickets[0]>0 and sum(tickets)==scale
    residuals=[];moments=[]
    powers=[(F(1),F(0)) for _ in exact_atoms]
    for m in range(K+1):
        rr=sum((F(w,scale)*z[0] for w,z in zip(tickets,powers)),F(0))
        ii=sum((F(w,scale)*z[1] for w,z in zip(tickets,powers)),F(0))
        assert ii==0 and rr>0
        target=r**(-m*m)
        error=abs(rr-target)
        residuals.append(error);moments.append(rr)
        for j,((xr,xi),(yr,yi)) in enumerate(zip(powers,exact_atoms)):
            powers[j]=(xr*yr-xi*yi,xr*yi+xi*yr)
    minimum=min(r**(-m*m) for m in range(K+1))
    relative=max(residuals)/(minimum-max(residuals))
    receipt={
        'K':K,'L':L,'mp_digits':mp.mp.dps,'probability_bits':probability_bits,
        'phase_tangent_bits':phase_bits,'root':frac(r),'root_lower':frac(rlo),'root_upper':frac(rhi),
        'tickets':tickets,'ticket_total':scale,
        'atoms':[{'real':frac(x),'imag':frac(y)} for x,y in exact_atoms],
        'moments':[frac(x) for x in moments],
        'moment_error_upper_display':mp.nstr(fm(max(residuals)),35),
        'relative_moment_log_error_upper_display':mp.nstr(fm(relative),35),
        'mp_orthogonal_extension_residual':mp.nstr(unitary_error,12),
        'seconds':time.perf_counter()-start,
        'scope':'Exact rational compiled probabilities/unit-circle atoms and exact residual versus rational-root heat-kernel moments. MP constructs proposals; Fraction checks the compiled output. Native root is independently bracketed by integer powers.'}
    return {'K':K,'L':L,'r':r,'root_width':rhi-rlo,'moments':moments,
            'moment_relative':relative,'atoms':np.array(atoms),
            'tickets':np.array(tickets,dtype=np.uint64),
            'thresholds':np.cumsum(np.array(tickets,dtype=np.uint64)),
            'probability_bits':probability_bits,'receipt':receipt}


def graph(kind):
    if kind=='triangle':
        T=np.ones((3,3))-np.eye(3)
        projectors={2:np.ones((3,3))/3,-1:np.eye(3)-np.ones((3,3))/3}
        return T,projectors
    assert kind=='triangular_3x3'
    T=np.zeros((9,9))
    for x in range(3):
        for y in range(3):
            i=3*x+y
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)):
                j=3*((x+dx)%3)+(y+dy)%3
                T[i,j]=1
    assert np.array_equal(T,T.T) and np.all(T.sum(axis=0)==6)
    I=np.eye(9)
    projectors={6:T@(T+3*I)/54,0:-(T-6*I)@(T+3*I)/18,-3:T@(T-6*I)/27}
    for l,P in projectors.items():assert np.linalg.norm(T@P-l*P)<1e-12
    return T,projectors


def h_complete_eigen(values,K):
    coeff=[F(1)]+[F(0)]*K
    for value in values:
        for k in range(1,K+1):coeff[k]+=value*coeff[k-1]
    return coeff[K]


def free_data(kind,quad):
    T,Ps=graph(kind);M=len(T);K,L=quad['K'],quad['L'];r=quad['r']
    minimum=min(Ps)
    E=np.zeros_like(T);values=[]
    for lam,P in Ps.items():
        value=r**(-2*(lam-minimum))
        E+=float(value)*P
        multiplicity=int(round(np.trace(P)))
        values.extend([value**L]*multiplicity)
    free_exact=h_complete_eigen(values,K)
    free_upper=np.nextafter(float(free_exact),np.inf)
    assert F.from_float(free_upper)>=free_exact
    d=math.comb(M+K-1,K)
    U=F(1,2)
    uniform_v=U*(2*K+F(4*K*(K-1),M+1)-F(2*K*K,M))
    # Shifted T has uniform trace 2K*(-minimum).
    uniform_h=F(-2*K*minimum)+uniform_v
    beta=mp.log(2)
    alpha_lower=d*d*mp.exp(-beta*fm(uniform_h))/fm(free_exact)**2
    return {'T':T,'E':E,'free':free_exact,'free_upper':free_upper,
            'dimension_one_flavor':d,'dimension_full':d*d,'M':M,
            'minimum':minimum,'alpha_lower':alpha_lower}


def h_batch(B,K):
    batch,M,_=B.shape
    traces=[];power=np.broadcast_to(np.eye(M,dtype=np.complex128),(batch,M,M)).copy()
    for j in range(1,K+1):
        power=power@B
        traces.append(np.trace(power,axis1=1,axis2=2))
    coeff=[np.ones(batch,dtype=np.complex128)]
    for k in range(1,K+1):
        coeff.append(sum(traces[j-1]*coeff[k-j] for j in range(1,k+1))/k)
    return coeff[K]


def receiver(kind,quad,proposals=65536,batch_size=256,seed=20261029):
    start=time.perf_counter();data=free_data(kind,quad)
    K,L=quad['K'],quad['L'];M=data['M'];rng=np.random.Generator(np.random.PCG64(seed))
    accepted=0;sum_f=0.;sum_f2=0.;minimum=1.;maximum=0.;words=0
    accepted_digests=hashlib.sha256();stored=0;cut=64-quad['probability_bits']
    for offset in range(0,proposals,batch_size):
        n=min(batch_size,proposals-offset)
        raw=rng.bit_generator.random_raw(n*L*M).reshape(n,L,M);words+=n*L*M
        tickets=raw>>cut
        labels=np.searchsorted(quad['thresholds'],tickets,side='right')
        B=np.broadcast_to(np.eye(M,dtype=np.complex128),(n,M,M)).copy()
        for ell in range(L):B=data['E']@(quad['atoms'][labels[:,ell,:]][:,:,None]*B)
        amplitudes=h_batch(B,K)/data['free_upper']
        f=abs(amplitudes)**2
        minimum=min(minimum,float(f.min()));maximum=max(maximum,float(f.max()))
        assert np.all(f>=0) and np.all(f<=1+1e-11)
        sum_f+=float(f.sum());sum_f2+=float(np.dot(f,f))
        bits=rng.bit_generator.random_raw(n)>>11;words+=n
        keep=bits.astype(np.float64)/2**53<np.minimum(f,1.)
        accepted+=int(keep.sum())
        if stored<1024:
            chosen=labels[keep][:1024-stored].astype(np.uint8)
            accepted_digests.update(chosen.tobytes());stored+=len(chosen)
    delta=.05
    lower=0. if not accepted else beta_distribution.ppf(delta/2,accepted,proposals-accepted+1)
    upper=1. if accepted==proposals else beta_distribution.ppf(1-delta/2,accepted+1,proposals-accepted)
    mean=sum_f/proposals
    se=math.sqrt(max(0,(sum_f2/proposals-mean**2)/(proposals-1)))
    gap=max(graph(kind)[1])-data['minimum']
    root_relative=quad['root_width']/F(**{'numerator':int(quad['receipt']['root_lower']['numerator']),'denominator':int(quad['receipt']['root_lower']['denominator'])})
    input_log_error=L*M*fm(quad['moment_relative'])+(4*K*gap+M*K*K)*L*fm(root_relative)
    return {
        'kind':kind,'M':M,'K_per_flavor':K,'total_particles':2*K,'L':L,
        'beta':'log(2)','U1':'1/2','U2':0,'t':1,'one_flavor_Fock_dimension':data['dimension_one_flavor'],
        'full_Fock_dimension':data['dimension_full'],'stored_propagator_dimension':M,
        'proposal_count':proposals,'accepted_count':accepted,'acceptance_fraction':accepted/proposals,
        'ideal_Binomial_95percent_acceptance_interval':[float(lower),float(upper)],
        'weight_mean':mean,'weight_mean_standard_error_diagnostic':se,
        'weight_relative_second_moment_diagnostic':sum_f2/proposals/mean**2,
        'interaction_free_energy_estimate':-math.log(mean)/math.log(2),
        'interaction_free_energy_interval_from_acceptance':[-math.log(upper)/math.log(2),-math.log(lower)/math.log(2)] if lower else None,
        'minimum_weight':minimum,'maximum_weight':maximum,
        'exact_free_normalizer_description_bits':data['free'].numerator.bit_length()+data['free'].denominator.bit_length(),
        'conservative_ideal_acceptance_floor_display':mp.nstr(data['alpha_lower'],35),
        'rational_input_log_partition_error_bound_display':mp.nstr(input_log_error,35),
        'rng':'PCG64 finite seed realization; mathematical confidence assumes independent uniform words',
        'seed':seed,'rng_64bit_words':words,
        'categorical_draws':proposals*L*M,'bernoulli_draws':proposals,
        'single_particle_matrix_products':proposals*(L+K),
        'first_accepted_history_count_hashed':stored,
        'accepted_history_sha256':accepted_digests.hexdigest(),
        'seconds':time.perf_counter()-start,
        'scope':'Binary64 finite compiled-HS transfer-law execution; no end-to-end directed hot-loop arithmetic. Binomial confidence is ideal finite-law/iid only. No continuum Gibbs or hardware/phase advantage inferred.'}


def compositions(K,M):
    if M==1:return [(K,)]
    return [(i,)+tail for i in range(K+1) for tail in compositions(K-i,M-1)]


def many_body_small(K=2):
    start=time.perf_counter();T,_=graph('triangle');M=3
    states=compositions(K,M);d=len(states);index={a:i for i,a in enumerate(states)}
    H1=np.zeros((d,d))
    for col,occ in enumerate(states):
        for i in range(M):
            for j in range(M):
                if i==j or not occ[j] or not T[i,j]:continue
                target=list(occ);target[i]+=1;target[j]-=1
                H1[index[tuple(target)],col]+=T[i,j]*math.sqrt((occ[i]+1)*occ[j])
    kinetic=np.kron(H1,np.eye(d))+np.kron(np.eye(d),H1)
    interaction=np.array([sum((x-y)**2 for x,y in zip(a,b))/2 for a in states for b in states])
    H=kinetic+np.diag(interaction)
    beta=math.log(2);eigen=eigh(H,eigvals_only=True)
    Z=float(np.exp(-beta*eigen).sum())
    free=float(np.exp(-beta*eigh(kinetic,eigvals_only=True)).sum())
    refs=[]
    for L in (8,16,32):
        half=expm(-beta*kinetic/(2*L));A=half@np.diag(np.exp(-beta*interaction/L))@half
        vals=eigh(A,eigvals_only=True)
        ZL=float(np.power(vals,L).sum())
        refs.append({'L':L,'Z_L':ZL,'alpha_L':ZL/free,
                     'interaction_free_energy':-math.log(ZL/free)/beta,
                     'relative_partition_bias_to_Gibbs':ZL/Z-1})
    return {'K':K,'M':M,'dimension':d*d,'Gibbs_Z':Z,'free_Z':free,
            'Gibbs_interaction_free_energy':-math.log(Z/free)/beta,
            'minimum_energy':float(eigen[0]),'references':refs,
            'seconds':time.perf_counter()-start,
            'scope':'Independent direct finite many-body binary64 Gibbs/Trotter control, no projected-field imports or sign assumptions. Not directed arithmetic.'}


def main():
    start=time.perf_counter();quads={}
    for K in (2,4):
        q=phase_quadrature(K,16);quads[K]=q
        (HERE/f'QUADRATURE_K{K}.json').write_text(json.dumps(q['receipt'],indent=2)+'\n')
        print('quadrature',K,q['receipt']['moment_error_upper_display'],flush=True)
    small=many_body_small()
    runs=[receiver('triangle',quads[2]),receiver('triangular_3x3',quads[4],seed=20261030)]
    result={'small_direct_control':small,'runs':runs,
            'wall_seconds_after_imports':time.perf_counter()-start,
            'input_contract':'Native stable U1 density-difference interaction with U2=0; two separately fixed balanced boson flavors, frustrated hopping. No local occupation cap; no interacting state preparation oracle.',
            'ordinary_comparator':'Shen2020 canonical AFQMC supplies recurrence; Yu2026 supplies conjugate positivity. No speed claim over an equally informed canonical AFQMC field sampler.',
            'statistical_limit':'Independent rejection avoids a mixing assumption, but its full proposal cost can be exponential at finite density. Finite PRNG/float execution is separate from ideal statistical theorem.'}
    (HERE/'EXECUTION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
