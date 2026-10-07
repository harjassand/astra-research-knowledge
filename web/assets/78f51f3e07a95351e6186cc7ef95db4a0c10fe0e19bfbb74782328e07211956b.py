"""Independent determinant comparisons for the owned phase-two backend."""
import sys,json
from pathlib import Path
from random import Random
from itertools import combinations
sys.path.insert(0,str(Path(__file__).resolve().parent))
from frontier_rank_guard import *
from representation_compiler import det,minor,rank
from check_banded import determinant_table,table_prefix,encode

def run():
    rng=Random(623207)
    fixtures=[];total_queries=0;sector_checks=0;minor_checks=0
    for n,r in ((2,0),(3,1),(4,1),(4,2),(5,1),(6,1)):
        base=[[C(rng.randrange(-1,3),rng.randrange(-1,2)) if 0<abs(i-j)<=1 else C(0)
               for j in range(n)] for i in range(n)]
        u=[[C(Q(rng.randrange(-2,3),2),Q(rng.randrange(-1,2),3)) for _ in range(r)] for _ in range(n)]
        v=[[C(Q(rng.randrange(-2,3),3),Q(rng.randrange(-1,2),2)) for _ in range(r)] for _ in range(n)]
        f=[[base[i][j]+sum((u[i][a]*v[j][a] for a in range(r)),C(0)) for j in range(n)] for i in range(n)]
        ext=augmented_matrix(base,u,v);aux=list(range(n,n+r));table=determinant_table(f)
        for k in range(n//2+1):
            for ii in combinations(range(n),k):
                for jj in combinations(sorted(set(range(n))-set(ii)),k):
                    assert det(minor(ext,list(ii)+aux,list(jj)+aux))==det(minor(f,ii,jj))
                    minor_checks+=1
        queries=[({},{}),({(0,'U'):1},{}),({(0,'U'):1,(0,'D'):1},{}),
                 ({(n-1,'D'):0},{}),({}, {n-1:{0,2}})]
        first=None
        for modes,sites in queries:
            counts=count_rank_update(base,u,v,modes,sites,collect_stats=True)
            expected=table_prefix(table,n,modes,sites)
            assert counts['coefficients']==expected,(n,r,modes,sites,counts,expected)
            total_queries+=1;sector_checks+=len(expected)
            if first is None:first=counts
        fixtures.append({'n':n,'r':r,'counts':first})
    # Exact rank recovery and an explicitly charged sparse base.
    n=5
    u=[[C(i+1,1-i)] for i in range(n)];v=[[C(1,Q(i,3))] for i in range(n)]
    residual=[[u[i][0]*v[j][0] for j in range(n)] for i in range(n)]
    acquired=rational_rank_approximation(residual,1)
    assert acquired['rank']==1 and not acquired['frobenius_residual_squared']
    base=[[C(i+1) if j==i+1 else C(0) for j in range(n)] for i in range(n)]
    delta=Q(1,1<<70)
    f=[[base[i][j]+residual[i][j]+(C(delta) if i==j else C(0)) for j in range(n)] for i in range(n)]
    certificate=acquire_certificate(f,base,1,2,Q(1,20),order=list(range(n)))
    assert certificate['status']=='CERTIFIED',certificate
    truez=table_prefix(determinant_table(f),n)[2]
    estimated=certificate['norm_estimate']
    assert abs(estimated-truez)<=certificate['epsilon']*truez
    # F-only acceptance beyond exact support frontier: tiny dense off-band noise.
    n=8;delta=Q(1,1<<80)
    base=[[C(0) if i==j or abs(i-j)>2 else C(1 if i<j else Q(1,2),Q((-1)**(i+j),3))
           for j in range(n)] for i in range(n)]
    f=[[base[i][j]+(C(delta*(pow(i+1,j+1,101)+1)) if abs(i-j)>2 else C(0))
        for j in range(n)] for i in range(n)]
    dense=acquire_banded_certificate(f,2,0,4,Q(1,100))
    assert dense['status']=='CERTIFIED',dense
    assert recognize_frontier(f)['width']==n-1
    dense_original_width=recognize_frontier(f)['width']
    table=determinant_table(f);truez=table_prefix(table,n)[4]
    estimated=dense['norm_estimate'];assert abs(estimated-truez)<=dense['epsilon']*truez
    physical_weights=[(o,w) for k,o,w in table if k==4]
    htable=determinant_table(dense['H']);hweights={o:w for k,o,w in htable if k==4}
    tv=sum((abs(w/truez-hweights.get(o,Q(0))/estimated) for o,w in physical_weights),Q(0))/2
    assert tv<=dense['epsilon']/4
    # Small matrix error alone is not enough: a zero approximate sector rejects.
    zero=matrix([[int(i!=j) for j in range(4)] for i in range(4)])
    perturbed=[[zero[i][j]+(C(delta) if (i,j)==(0,1) else C(0)) for j in range(4)] for i in range(4)]
    rejected=acquire_certificate(perturbed,zero,0,2,Q(1,100),order=list(range(4)))
    assert rejected['status']=='UNKNOWN_ADMISSION' and rejected['norm_estimate']==0
    assert table_prefix(determinant_table(perturbed),4)[2]==2*delta*delta
    # A whole-law guard gives no relative guarantee on a rare prefix.
    d=Q(1,10000)
    h=matrix([[0,1,0,0],[0,0,0,0],[0,0,0,d],[0,0,0,0]])
    f=matrix([[0,1,0,0],[0,0,0,0],[0,0,0,d*d],[0,0,0,0]])
    rare=acquire_certificate(f,h,0,1,Q(1,100),order=list(range(4)))
    assert rare['status']=='CERTIFIED'
    prefix={(2,'U'):1,(3,'D'):1}
    z_h=table_prefix(determinant_table(h),4,prefix)[1]
    z_f=table_prefix(determinant_table(f),4,prefix)[1]
    assert z_h==d*d and z_f==d**4 and z_h/z_f==10**8
    # Executed random seeds only test support/code; randomness theorem requires fair bits.
    sampled=[]
    for seed in range(3):
        result=sample_certified(certificate,Random(seed).getrandbits)
        assert result['status']=='SAMPLE'
        sampled.append(result)
    return {'status':'PASS','checks':{'augmented_minor_identities':minor_checks,
        'prefix_polynomials':total_queries,'sector_coefficients':sector_checks,
        'exact_greedy_rank_recovery':1,'certified_rank_approximation':1,
        'F_only_dense_full_occupancy_certificate':1,'correct_zero_approximate_sector_rejection':1,
        'rare_prefix_relative_failure':1,'seeded_sampler_support_runs':len(sampled)},
        'fixtures':fixtures,'rank_certificate':{k:certificate[k] for k in ('rank','eta_squared','amplitude_error_squared_bound','norm_estimate','counts')},
        'dense_certificate':{k:dense[k] for k in ('rank','eta_squared','amplitude_error_squared_bound','norm_estimate','guard_right_hand_side','counts')},
        'dense_original_support_frontier':dense_original_width,
        'dense_original_middle_cut_rank_sum':rank(minor(dense['F'],range(4),range(4,8)))+rank(minor(dense['F'],range(4,8),range(4))),
        'dense_exact_true_norm':truez,'dense_exact_TV':tv,
        'rare_prefix_ratio':z_h/z_f,'samples':sampled,
        'scope':'finite exact diagnostics; full all-size proof is separate; circuit unimplemented'}

if __name__=='__main__':
    output=encode(run());Path(__file__).with_name('frontier_rank_guard_checks.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'checks':output['checks'],'dense_norm':output['dense_certificate']['norm_estimate'],
        'dense_cut_rank':output['dense_original_middle_cut_rank_sum']}))
