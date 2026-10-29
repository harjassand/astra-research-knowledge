"""Small SAME-seed matrix diagnostic of the quantum-polymer identities.

Binary64 exponentials are diagnostic, not interval certificates. The all-size
claim rests on STATIC_PEIERLS.md and ordinary scalar KP inputs. This is not a
thermal-memory trajectory, a qualified 3D embedding or a device acquisition.
"""
from pathlib import Path
import itertools,json,time,sys
import numpy as np
from scipy.linalg import expm

HERE=Path(__file__).parent
sys.path.insert(0,str(HERE.parent))
from compile_complex import seed,bits


def pauli(n,x,z):
    # Hermitian tensor-Pauli convention: Y=i XZ at an overlap.
    a=np.zeros((1<<n,1<<n),dtype=complex)
    phase=1j**((x&z).bit_count())
    for k in range(1<<n):a[k^x,k]=phase*(-1)**((k&z).bit_count())
    assert np.max(np.abs(a-a.conj().T))==0
    return a


def main():
    start=time.perf_counter();c=seed();n=c.n;dim=1<<n;I=np.eye(dim,dtype=complex)
    checks=[pauli(n,x,0) for x in c.xs]+[pauli(n,0,z) for z in c.zs]
    H0=sum((I-S)/2 for S in checks)
    group=[I]
    for S in checks:group += [G@S for G in list(group)]
    def twirl(A):return sum(G@A@G for G in group)/len(group)
    def norm(A):return float(np.linalg.norm(A,2))
    Pstack=np.array([pauli(n,x,z) for x in range(dim) for z in range(dim)])
    def l1(A):return float(np.sum(np.abs(np.einsum('aij,ji->a',Pstack,A)/dim)))
    beta=1.;v=1e-5
    # Two noncommuting fields on mode0 plus fields making both logical
    # directions available at second order. Every term is native one-site.
    specs=[(1,0,1.),(0,1,.5),(0,2,.75),(8,0,-1.)]
    Vs=[v*a*pauli(n,x,z) for x,z,a in specs]
    masks=[x|z for x,z,a in specs]
    count=len(Vs);allmask=(1<<count)-1
    touching=[{j for j,s in enumerate(c.xs+c.zs) if s&a} for a in masks]
    graph=[sum(1<<j for j in range(count) if i!=j and (masks[i]&masks[j] or touching[i]&touching[j])) for i in range(count)]
    def components(mask):
        result=[]
        while mask:
            seen=mask&-mask;todo=seen
            while todo:
                new=0
                for i in bits(todo):new|=graph[i]
                new&=mask&~seen;seen|=new;todo=new
            result.append(seen);mask&=~seen
        return result
    T={};W={};eplus=expm(beta*H0)
    for mask in range(1<<count):
        H=H0+sum((Vs[i] for i in bits(mask)),np.zeros_like(H0))
        T[mask]=eplus@twirl(expm(-beta*H))
        W[mask]=T[mask]-sum((W[sub] for sub in range(mask) if sub&mask==sub),np.zeros_like(H0))
    logicals=[pauli(n,0b01001,0),pauli(n,0,0b00011)]
    activity_stats=[];factor_err=0.
    for mask in range(1,1<<count):
        comp=components(mask);P=I.copy()
        for a in comp:P=P@W[a]
        factor_err=max(factor_err,norm(W[mask]-P))
        activity_stats.append({'mask':mask,'size':mask.bit_count(),'connected':len(comp)==1,
             'Pauli_l1_diagnostic':l1(W[mask]),'Hermiticity_defect':norm(W[mask]-W[mask].conj().T),
             'max_logical_commutator':max(norm(W[mask]@Q-Q@W[mask]) for Q in logicals)})
    # d_seed=2 and nativeq1: small polymers are exactly the singletons.
    small=[1<<i for i in range(count)];Zs=np.zeros_like(H0)
    for family in range(1<<count):
        chosen=[1<<i for i in bits(family)]
        if any(graph[i]&family for i in bits(family)):continue
        product=I.copy()
        for s in chosen:product=product@W[s]
        Zs+=product
    # Reconstruct the complete polymer gas directly, all connected components.
    reconstruct=np.zeros_like(H0)
    for selected in range(1<<count):
        product=I.copy()
        for comp in components(selected):product=product@W[comp]
        reconstruct+=product
    H=H0+sum(Vs);rho=expm(-beta*H);rho/=np.trace(rho)
    Hchecktouch=max(map(len,touching));a=beta*np.exp(beta*Hchecktouch)*v
    w=np.expm1(a);Delta=max(x.bit_count() for x in graph)
    B=(Delta+1)**2*np.exp(2)*w;b=B/np.exp(1);L=2
    delta=count*b**L/(1-b)
    relative=T[allmask]@np.linalg.inv(Zs)-I
    result={'input':{'seed':'own exact [[5,1,2]] planar seed','n':n,'beta':beta,'native_q':1,'v':v,
              'native_specs':specs,'touching_checks':[sorted(x) for x in touching],
              'interaction_graph':graph,'Delta':Delta,'energy_convention':'sum(I−S)/2'},
            'checks':{'mobius_polymer_reconstruction_error':norm(reconstruct-T[allmask]),
              'component_factorization_error':factor_err,
              'small_centrality_error':max(x['max_logical_commutator'] for x in activity_stats if x['size']==1),
              'small_gas_min_eigenvalue':float(np.min(np.linalg.eigvalsh((Zs+Zs.conj().T)/2))),
              'relative_full_vs_small_norm':norm(relative),
              'relative_bound_exp_delta_minus1':float(np.expm1(delta)),
              'full_gibbs_offdiagonal_twirl_trace_distance':float(np.sum(np.linalg.svd(rho-twirl(rho),compute_uv=False)))},
            'formal_majorants_diagnostic':{'a':float(a),'w0':float(w),'B':float(B),
              'KP_sufficient_ceiling':1/(2*(Delta+2)),'L':L,'delta':float(delta)},
            'activities':activity_stats,'wall_seconds_after_imports':time.perf_counter()-start,
            'scope':'Binary64 finite algebra diagnostic only. Tiny higher-order activities can be below cancellation precision; no certified arithmetic, beta_c admission, 3D embedding, storage lifetime, native bath or speed advantage.'}
    assert result['checks']['mobius_polymer_reconstruction_error']<1e-10
    assert factor_err<1e-10
    assert result['checks']['small_centrality_error']<1e-10
    assert B<1/(2*(Delta+2))
    assert norm(relative)<np.expm1(delta)
    (HERE/'POLYMER_EXECUTION.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='activities'},indent=2))


if __name__=='__main__':main()
