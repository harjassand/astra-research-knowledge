"""Controls for multivariate readout with fully correlated quantum controllers.

Exact source operators, simultaneous reads, bounded-degree source example,
and the charge-block Poisson representation of the supplied thermal noise.
"""
import json,math,hashlib,itertools
from pathlib import Path
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/coherent_inference_20261101'
def opnorm(a):return float(np.linalg.norm(a,2))
def maxeig(a):return float(np.linalg.eigvalsh((a+a.conj().T)/2)[-1])
def lift(a,i,n):
    r=np.ones((1,1),complex)
    for j in range(n):r=np.kron(r,a if j==i else np.eye(2))
    return r
def subset_checks(cells,distributed):
    X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.])
    ds=2**cells if distributed else 2;Ic=np.eye(2**cells);Is=np.eye(ds);delta=.1;T=math.pi/2;eta=.95
    if distributed:
        He=sum((7+i)*lift(X,i,cells) for i in range(cells))
        He+=sum(.31*lift(Z,i,cells)@lift(Z,i+1,cells) for i in range(cells-1))
        gains=[Is+delta*lift(math.cos(i+.2)*Z+math.sin(i+.2)*Y,i,cells) for i in range(cells)]
    else:
        He=17*X+.23*Y
        gains=[Is+delta*(math.cos(.7*i)*Z+math.sin(.7*i)*Y) for i in range(cells)]
    H=np.kron(Ic,He)
    for i,G in enumerate(gains):H+=np.kron(lift(X,i,cells),G)
    U=expm(-1j*T*H);blocks=[U[s*ds:(s+1)*ds,:ds] for s in range(2**cells)]
    r2=math.sin(math.pi*delta/2)**2;p=1-eta*(1-r2);worst_miss=-1.;worst_detect=-1.
    rows=[]
    for mask in range(1,2**cells):
        selected=[i for i in range(cells) if (mask>>i)&1]
        miss=np.zeros((ds,ds),complex);detect=miss.copy()
        for s,B in enumerate(blocks):
            transferred=sum((s>>i)&1 for i in selected)
            BB=B.conj().T@B
            if transferred==0:miss+=BB
            detect+=(1-eta)**transferred*BB
        k=len(selected);g1=maxeig(miss-r2**k*Is);g2=maxeig(detect-p**k*Is)
        assert g1<2e-10 and g2<2e-10
        worst_miss=max(worst_miss,g1);worst_detect=max(worst_detect,g2)
        rows.append({'subset_mask':mask,'read_count':k,'worst_source_no_detect_probability':opnorm(detect),
                     'joint_no_detect_upper':p**k})
    return {'cells':cells,'source_dimension':ds,'distributed_bounded_degree_source':distributed,
       'max_joint_miss_minus_product_bound_eigenvalue':worst_miss,
       'max_joint_collection_failure_minus_product_bound_eigenvalue':worst_detect,'subsets':rows}
def uniformization_check():
    sm=np.array([[0,1],[0,0]],complex);ss=[lift(sm,i,4) for i in range(4)]
    ns=[s.conj().T@s for s in ss];N=sum(ns);I=np.eye(16)
    down=.002;phi=.001;p=1e-5;up=down*p/(1-p)
    rng=np.random.default_rng(1519);v=rng.normal(size=(16,16))+1j*rng.normal(size=(16,16));rho=v@v.conj().T
    # Local charge pinching is exact on the invariant input/noise class.
    charges=np.diag(N).real;rho*=charges[:,None]==charges[None,:];rho/=np.trace(rho)
    residuals=[]
    for Ls,R in (([math.sqrt(down)*s for s in ss]+[math.sqrt(2*phi)*n for n in ns],4*(down+2*phi)),
                 ([math.sqrt(up)*s.conj().T for s in ss],4*up)):
        K=sum(L.conj().T@L for L in Ls);vals,vecs=np.linalg.eigh(R*I-K)
        null=(vecs*np.sqrt(np.maximum(vals,0)))@vecs.conj().T
        direct=sum(L@rho@L.conj().T-(L.conj().T@L@rho+rho@L.conj().T@L)/2 for L in Ls)
        poisson=sum(L@rho@L.conj().T for L in Ls)+null@rho@null.conj().T-R*rho
        error=opnorm(direct-poisson);assert error<2e-14
        assert opnorm(sum(L.conj().T@L for L in Ls)+null.conj().T@null-R*I)<2e-14
        residuals.append(error)
    eta=.95;dark=1e-6;T=math.pi/2;gain=math.cos(math.pi*.1/2)**2
    w=1-(1-p)**2*(1-dark)**2*math.exp(-4*up*T)
    e=1-(1-p)**2*(1-dark)**2*math.exp(-4*(down+2*phi+up)*T)*eta*gain
    levels=[]
    for level in range(6):
        levels.append({'level':level,'data_dual_rail_qubits':7**level,'total_two_level_sites_including_controllers':5*7**level,
            'fresh_thermal_receiver_spins':2*7**level,'simultaneous_read_duration':T,'erasure_upper':e,'wrong_label_upper':w})
        bad=42*e*w+21*w*w;e,w=min(1.,7*e**3+bad),min(1.,bad)
    return {'charge_block_GKSL_vs_independent_Poisson_clock_residuals':residuals,
       'cold_label_preserving_clock_rate':4*(down+2*phi),'thermal_upward_clock_rate':4*up,
       'recursive_bounds':levels,
       'contract':'local charge-diagonal states; uniform per-site rates; all source Hamiltonian terms conserve each cell charge; Poisson marks, fresh receiver thermal mixtures and detector events independent across cells; quantum controller states/dynamics need no spatial independence'}
def main():
    result={'status':'PASS simultaneous operator-subset and conditional thermal-noise controls',
       'shared_source':[subset_checks(m,False) for m in (2,4,6)],
       'local_correlated_source_network':subset_checks(3,True),
       'thermal_parallel_extension':uniformization_check(),
       'scope':'finite controls for analytic multivariate theorem; no hardware qualification or encoded-input preparation',
       'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'parallel_readout_controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'network':{k:v for k,v in result['local_correlated_source_network'].items() if k!='subsets'},
                     'thermal':result['thermal_parallel_extension']},indent=2))
if __name__=='__main__':main()
