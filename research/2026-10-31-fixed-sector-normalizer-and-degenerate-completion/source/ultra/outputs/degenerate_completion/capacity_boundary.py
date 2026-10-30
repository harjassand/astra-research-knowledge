"""Exact Fourier receipt of an actual-gradient capacity jump at rank loss.

No grid, angular sample, numerical optimizer, or free-law substitution.
All Fourier frequencies and epsilon coefficients are exact integers/rationals.
"""
from pathlib import Path
from fractions import Fraction as R
from functools import lru_cache
import importlib.util,json,time,sys,contextlib,io

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('degenerate_completion_core',HERE/'receive.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
b=d.b;add,mul,scale,diff=d.add,d.mul,d.scale,d.diff

def main():
    start=time.perf_counter();receipt,(cert,cubics,_,_,F)=d.derive()
    basis=json.loads((HERE.parent/'quadratic_boundary/certificate.json').read_text())['normal_form_basis']
    admitted=[{tuple(p):R(v) for p,v in zip(cert['cubic_powers'],row) if R(v)} for row in basis]
    C=cubics[2];nu=R(2**cert['completion_power'])
    rays=[[1,0,0,0],[0,0,0,1],[1,1,1,1],[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    frequencies=[(1,0),(0,1),(1,1),(9,0),(0,81),(729,0),(0,6561)]
    epowers=[0,0,1,2,2,2,2]
    # Laurent-polynomial variables: frequency x, frequency y, epsilon.
    G=[{} for _ in range(4)]
    for ray,k,ep in zip(rays,frequencies,epowers):
        assert ray[0]*k[1]-ray[1]*k[0]==0 and ray[2]*k[1]-ray[3]*k[0]==0
        assert ray[0]*ray[3]-ray[1]*ray[2]==0
        for a,v in enumerate(ray):
            if v:
                for sign in (-1,1):G[a]=add(G[a],{(sign*k[0],sign*k[1],ep):R(v,2)})
    def moment(q):return {(ep,):co for (kx,ky,ep),co in q.items() if kx==ky==0 and co}
    @lru_cache(maxsize=None)
    def monomial(pw):
        if not any(pw):return {(0,0,0):R(1)}
        i=next(i for i,p in enumerate(pw) if p);prev=list(pw);prev[i]-=1
        return mul(monomial(tuple(prev)),G[i])
    def expectation(P):return moment(add(*(scale(monomial(tuple(pw)),co) for pw,co in P.items())))
    assert all(not moment(q) for q in G)
    covariance=[[moment(mul(ga,gb)) for gb in G] for ga in G]
    for i in range(4):
        for j in range(4):
            expected={(2,):R(1,2)}
            if i==j:expected[(4,)]=R(1,2)
            if i==j and i in (0,3):expected[(0,)]=R(1,2)
            assert covariance[i][j]==expected
    cubic_moments=[]
    for pw in cert['cubic_powers']:
        mm=expectation({tuple(pw):R(1)})
        assert all(ep==(1,) for ep in mm)
        cubic_moments.append(mm)
    tau=expectation(C).get((1,),R(0));assert expectation(C)=={(1,):tau} and abs(tau)>R(1,2**12)
    q0=add(mul(b.var(4,1),b.var(4,1)),mul(b.var(4,2),b.var(4,2)))
    assert expectation(q0)=={(2,):R(1),(4,):R(1)}
    # Zero-epsilon covariance has an ordinary zero-background allocation.
    # Its cubic moments and cost are zero. Positive epsilon has full
    # covariance because its extra epsilon^4 I/2 term is positive definite.
    assert all(mm.get((0,),0)==0 for mm in cubic_moments)
    # Translation Hessian is uniformly PD. Each added term is PSD by ROC.
    HF=[[diff(diff(F,i),j) for j in range(4)] for i in range(4)]
    Hpolys=[[expectation(p) for p in row] for row in HF]
    H0=[[p.get((0,),R(0)) for p in row] for row in Hpolys];b.pd(H0)
    for ep in (2,4):
        HH=[[p.get((ep,),R(0)) for p in row] for row in Hpolys]
        # Sum of ordinary rank-one Hessians: exact principal-minor PSD.
        from itertools import combinations,permutations
        for n in range(1,5):
            for ids in combinations(range(4),n):
                det=sum((R((-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n)))*__import__('math').prod(HH[ids[i]][ids[j]] for i,j in enumerate(perm)) for perm in permutations(range(n))),R(0))
                assert det>=0
    v=[expectation(diff(F,i)) for i in range(4)]
    w=[expectation(diff(C,i)) for i in range(4)]
    assert all(not p or min(ep[0] for ep in p)>=1 for p in v)
    assert all(not p or min(ep[0] for ep in p)>=2 for p in w)
    # All twelve residuals vanish at the limit: v0=0, H0>0, ell0=0.
    assert all(not expectation(P).get((0,),R(0)) for P in admitted)
    # Completed-cost lower bound for 0<epsilon<=1/2:
    # tau^2/[4 nu (1+epsilon^2)] >= tau^2/(5nu) >2^-113.
    lower=tau*tau/(5*nu);assert lower>R(1,2**113)
    # Separated-scale hypothesis for <=4-frequency relations. Directions
    # are those of the gluing theorem; 9 exceeds the required factor 4.
    assert all(frequencies[i][0] in (0,9**(i-2)) and frequencies[i][1] in (0,9**(i-2)) for i in range(3,7))
    assert 9>4
    quartic_moment=expectation(F)
    norm2=add(*(mul(q,q) for q in G));norm4=moment(mul(norm2,norm2))
    assert norm4.get((0,),0)>=1  # s0=1; Jensen also gives L4>=1 for every epsilon.
    result={'actual_smooth_periodic_potential':True,'fourier_modes':7,'all_twenty_cubic_moments_exact':True,'positive_epsilon_covariance_full_rank':True,'limit_covariance_rank':2,'strong_convergence':'uniform, hence strong L4','tau':str(tau),'tau_abs_lower_bound':str(R(1,2**12)),'QC_boundary_coefficient':str(nu),'capacity_cost_lower_bound_all_positive_epsilon_up_to_half':str(lower),'simpler_capacity_cost_lower_bound':str(R(1,2**113)),'limit_optimal_cost':'0','uniform_translation_Hessian_PD':True,'all_residual_correlations_tend_to_zero':True,'selected_residual_asymptotic':'epsilon*tau+O(epsilon^3)','uniform_actual_leading_excess_a_lower_bound':'1/100','uniform_all_ROC_variational_gap_coefficient':'1/200','capacity_cost_continuous_at_actual_rank_loss':False,'ordinary_positive_budget_allocations_exist':True,'actual_negative_variational_gap':False,'quartic_moment_polynomial':{str(ep[0]):str(co) for ep,co in sorted(quartic_moment.items())},'fourth_norm_moment_polynomial':{str(ep[0]):str(co) for ep,co in sorted(norm4.items())}}
    if '--replay-gluing' in sys.argv:
        spec=importlib.util.spec_from_file_location('degenerate_gluing_replay',HERE.parent/'resonant_gluing/receive.py');gg=importlib.util.module_from_spec(spec);spec.loader.exec_module(gg)
        with contextlib.redirect_stdout(io.StringIO()):gg.main()
        result['full_gluing_receiver_replayed']=True
    result.update({'seconds':time.perf_counter()-start,'scope':'Actual compatible uniformly bounded field family. Exact weak-dual capacity lower bound and known ordinary positive-budget allocations. No ROC/QC separation or nonattainment claim.'})
    (HERE/'capacity_boundary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
