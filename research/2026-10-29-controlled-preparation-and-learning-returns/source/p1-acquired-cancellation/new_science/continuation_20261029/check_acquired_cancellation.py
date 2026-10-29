"""Exact population checks and a SEPARATE synthetic acquisition rehearsal.
Fraction polynomials integrate frozen h. The compiler sees visible moments only.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, math, hashlib
import numpy as np
from scipy.optimize import minimize

ROOT=Path(__file__).resolve().parent
U=[F(1,10),F(3,10),F(1,4),F(7,20)]
V=[F(1,20),-F(3,20),F(1,10),-F(1,10)]
MIX=[[F(3,4),F(1,4),F(0),F(0)],[F(0),F(0),F(1,2),F(1,2)]]
PERT=[[F(76,100),F(24,100),F(0),F(0)],[F(0),F(0),F(51,100),F(49,100)]]

def mul(p,q):
    r=[F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):r[i+j]+=a*b
    while len(r)>1 and not r[-1]:r.pop()
    return r

def integ(p,lo=F(-1),hi=F(1)):
    return sum(c*(hi**(i+1)-lo**(i+1))/F(i+1) for i,c in enumerate(p))/(hi-lo)

def rates(mix,v=V):
    return [[sum(p*x for p,x in zip(w,U)),sum(p*x for p,x in zip(w,v))] for w in mix]

def gram(v):
    L=[[F(1)-U[i]-U[j]+2*U[i]*U[j]+F(2,3)*v[i]*v[j] for j in range(4)] for i in range(4)]
    H=[[L[i][j]-((1-U[i])*(1-U[j])+U[i]*U[j]) for j in range(4)] for i in range(4)]
    assert H==[[F(2,3)*a*b for b in v] for a in v]
    return L,H

def quad(H,p):return sum(p[i]*H[i][j]*p[j] for i in range(4) for j in range(4))

def path_prob(tree,y0,path,rs):
    node=0;y=y0;p=[F(1)]
    for yp in path:
        r=rs[tree[node]]
        p=mul(p,r if yp!=y else [1-r[0],-r[1]])
        node=2*node+1+yp;y=yp
    return p

def exhaustive_records(rs,reference,depth=3):
    maxima={};all_exact=True;checked=0
    for y0 in (0,1):
        for lo,hi in ((F(-1),F(0)),(F(0),F(1))):
            best=F(0);besttree=None
            for tree in product((0,1),repeat=2**depth-1):
                pa=[];pr=[]
                for path in product((0,1),repeat=depth):
                    p=path_prob(tree,y0,path,rs);q=path_prob(tree,y0,path,reference)
                    all_exact &= p==q
                    pa.append(integ(p,lo,hi));pr.append(integ(q,lo,hi));checked+=1
                assert sum(pa)==sum(pr)==1
                tv=sum(abs(a-b) for a,b in zip(pa,pr))/2
                if tv>best:best=tv;besttree=tree
            maxima[f'y0={y0},h=({lo},{hi})']={'tv':best,'tree':besttree}
    return {'all_probability_polynomials_identical':all_exact,'path_checks':checked,
            'history_branch_maxima':maxima,'worst_joint_tv':sum(x['tv'] for x in maxima.values())/4}

def det(mat):
    A=[r[:] for r in mat];ans=F(1)
    for i in range(len(A)):
        j=next(j for j in range(i,len(A)) if A[j][i])
        if j!=i:A[j],A[i]=A[i],A[j];ans=-ans
        p=A[i][i];ans*=p
        for j in range(i+1,len(A)):
            q=A[j][i]/p
            for k in range(i+1,len(A)):A[j][k]-=q*A[i][k]
    return ans

def optimize(H,u,target):
    H=np.asarray(H,float);u=np.asarray(u,float)
    res=minimize(lambda p:p@H@p,np.ones(4)/4,jac=lambda p:2*H@p,
      constraints=[{'type':'eq','fun':lambda p:p.sum()-1,'jac':lambda p:np.ones(4)},
                   {'type':'eq','fun':lambda p:p@u-target,'jac':lambda p:u}],
      bounds=[(0,1)]*4,method='SLSQP',options={'ftol':1e-14,'maxiter':2000})
    assert res.success,res.message
    return res.x

def population_checks():
    L,H=gram(V);Lb,Hb=gram(list(map(abs,V)))
    assert all(quad(H,p)==0 for p in MIX)
    rs=rates(MIX);assert rs==[[F(3,20),F(0)],[F(3,10),F(0)]]
    exact=exhaustive_records(rs,[[r[0],F(0)] for r in rs])
    assert exact['all_probability_polynomials_identical'] and exact['worst_joint_tv']==0
    isolated=0
    for j in range(4):
        for y0 in (0,1):
            for path in product((0,1),repeat=5):
                tr=(0,)*31
                a=integ(path_prob(tr,y0,path,[[U[j],V[j]]]))
                b=integ(path_prob(tr,y0,path,[[U[j],abs(V[j])]]))
                assert a==b;isolated+=1
    assert Lb[0][1]-L[0][1]==F(1,100)
    c=min(row[0] for row in Hb);v2=Hb[0][0]
    assert c*c/v2==F(1,600)
    moment=lambda n:(F(9,10)**(n+1)-F(7,10)**(n+1))/(F(1,5)*(n+1))
    hankel=[det([[moment(i+j) for j in range(n)] for i in range(n)]) for n in range(1,7)]
    assert all(x>0 for x in hankel)
    prs=rates(PERT);assert [r[1] for r in prs]==[F(1,500)]*2
    perturb=exhaustive_records(prs,[[r[0],F(0)] for r in prs])
    row_variances=[quad(H,p) for p in PERT]
    tau=min(min(r[0],1-r[0]) for r in prs)
    kl_bound=F(3)*2*sum(row_variances)/tau;tv_bound2=kl_bound/2
    assert perturb['worst_joint_tv']**2<=tv_bound2
    qp=[]
    for target in (.15,.30):
        p=optimize(H,U,target);pb=optimize(Hb,U,target)
        assert p@np.array(H,float)@p<1e-11
        qp.append({'target':target,'same_information_QP_weights':p.tolist(),
          'residual_squared':float(p@np.array(H,float)@p),
          'noncancellable_source_weights':pb.tolist(),
          'noncancellable_residual_squared':float(pb@np.array(Hb,float)@pb)})
    exposed=sum(p*2*abs(v) for p,v in zip(MIX[0],V));assert exposed==F(3,20)
    # At h=-1, reuse of the same selector twice gives a nonzero two-flip gap.
    reused_gap=sum(p*(u-v)**2 for p,u,v in zip(MIX[0],U,V))-F(3,20)**2
    assert reused_gap>0
    prep=F(1,2)*F(2,5)**8;assert prep==F(128,390625)
    return {'scope':'Exact population algebra; not finite-sample or apparatus acquisition',
      'cross_gram':H,'opposite_source_cross_gram':Hb,'compiled_rates':rs,
      'exact_complete_records':exact,'isolated_length_five_path_checks':isolated,
      'cross_loop_return_difference':Lb[0][1]-L[0][1],
      'all_mixture_exclusion_squared_floor':c*c/v2,'hankel_determinants_1_to_6':hankel,
      'perturbed_mixtures':PERT,'perturbed_compiled_rates':prs,
      'perturbed_complete_records':perturb,'perturbed_KL_upper_bound':kl_bound,
      'perturbed_TV_upper_bound':math.sqrt(float(tv_bound2)),
      'eight_call_preparation_bound':prep,'eight_call_preparation_bound_float':float(prep),
      'exposed_key_one_stage_TV':exposed,'reused_key_two_flip_gap_at_h_minus_one':reused_gap,
      'same_information_conventional_comparison':qp}

def sample_rehearsal(N=100000,seed=20261029):
    rng=np.random.default_rng(seed);u=np.array(U,float);v=np.array(V,float)
    counts={};uhat=[]
    for j in range(4):
        h=rng.uniform(-1,1,N);y0=rng.integers(0,2,N)
        flip=rng.random(N)<(u[j]+v[j]*h);y1=y0^flip
        counts[f'one_{j}']=np.bincount(2*y0+y1,minlength=4).tolist()
        uhat.append(float(flip.mean()))
    uhat=np.array(uhat);Lhat=np.zeros((4,4))
    for i in range(4):
        for j in range(i,4):
            # h is internal to the source and is NOT supplied to the estimator.
            h=rng.uniform(-1,1,N);y0=rng.integers(0,2,N)
            y1=y0^(rng.random(N)<u[i]+v[i]*h)
            y2=y1^(rng.random(N)<u[j]+v[j]*h)
            counts[f'two_{i}_{j}']=np.bincount(4*y0+2*y1+y2,minlength=8).tolist()
            Lhat[i,j]=Lhat[j,i]=np.mean(y0==y2)
    Hhat=Lhat-((1-uhat)[:,None]*(1-uhat)[None,:]+uhat[:,None]*uhat[None,:])
    vals,vec=np.linalg.eigh(Hhat);Hpsd=(vec*np.maximum(vals,0))@vec.T
    delta=.01;settings=14
    eta=math.sqrt(math.log(2*settings/delta)/(2*N))
    # WARRANTED binary-symmetric static-H structure: return radius eta plus
    # mean product error <=2eta gives a 3eta cross-Gram entry radius.
    d=3*eta;out=[]
    for target in (.15,.30):
        p=optimize(Hpsd,uhat,target)
        variance=max(0,float(p@Hhat@p+d));meanerr=2*eta**2
        true_mean=float(p@u);true_variance=float(F(2,3))*(p@v)**2
        out.append({'weights':p.tolist(),'reference_flip_probability':float(p@uhat),
          'certified_variance_upper':variance,'certified_mean_square_upper':meanerr,
          'population_check_variance':true_variance,'population_check_mean':true_mean})
        assert true_variance<=variance
        assert 2*(true_mean-target)**2<=meanerr+1e-12
    Htrue=np.array(gram(V)[1],float)
    assert np.max(abs(Hhat-Htrue))<=d
    assert np.max(abs(uhat-u))<=eta
    tau=min(min(x['reference_flip_probability'],1-x['reference_flip_probability']) for x in out)
    total=2*sum(x['certified_variance_upper']+x['certified_mean_square_upper'] for x in out)
    bounds={str(n):min(1.,math.sqrt(n*total/(2*tau))) for n in (1,3,100)}
    return {'scope':'Synthetic ideal-source acquisition rehearsal, not laboratory data',
      'warranted_structure':'Frozen H; binary symmetric rows; iid ensemble preparation and independent deployment; exact labels/calls',
      'N_per_setting':N,'seed':seed,'confidence_failure_budget':delta,'scalar_radius':eta,
      'cross_Gram_entry_radius':d,'counts':counts,'estimated_means':uhat.tolist(),
      'estimated_cross_Gram':Hhat.tolist(),'optimizer_PSD_eigenvalues':np.maximum(vals,0).tolist(),
      'compiled_actions':out,'uniform_complete_record_TV_bounds':bounds,
      'resource_counts':{'independent_baseline_preparations':14*N,'native_calls':24*N,'label_reads':38*N},
      'not_paid_by_counts':['preparation apparatus and work','timing and switching calibration',
        'sensor imperfections','physical randomization and key disposal'],
      'long_record_certificate_useful':bounds['100']<1}

def serial(o):
    if isinstance(o,F):return {'fraction':str(o),'float':float(o)}
    if isinstance(o,np.generic):return o.item()
    raise TypeError(type(o).__name__)

if __name__=='__main__':
    result={'population':population_checks(),'synthetic_acquisition':sample_rehearsal()}
    result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    path=ROOT/'ACQUIRED_CANCELLATION_CHECKS.json'
    path.write_text(json.dumps(result,default=serial,indent=2)+'\n')
    print(json.dumps({'output':str(path),
      'population_TV':result['population']['exact_complete_records']['worst_joint_tv'],
      'perturbed_worst_TV':result['population']['perturbed_complete_records']['worst_joint_tv'],
      'perturbed_bound':result['population']['perturbed_TV_upper_bound'],
      'synthetic_bounds':result['synthetic_acquisition']['uniform_complete_record_TV_bounds']},default=serial,indent=2))
