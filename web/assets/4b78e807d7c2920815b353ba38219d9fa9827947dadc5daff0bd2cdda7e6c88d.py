"""Bounded N<=16 whole-Gibbs compiler with compressed posterior certificate.

Root supplied filtered-column preconditioning; c01_s03 reconstructed it.
Owned implementation uses a rounded rational table, a TIME-LIMITED simplex
subprocess, exact rational final certificates, and cached zero-field quadrature.
No dense 2**N matrix. No polynomial/simplex/uniform-success runtime claim.
"""
import argparse
from fractions import Fraction as F
import json
import math
import os
from pathlib import Path
import random
import resource
import subprocess
import sys
import time

for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import mpmath as mp
import dicke_compiler as dc
from check_finite_alpha import peer

HERE=Path(__file__).resolve().parent


def dyadic_simplex(p,bits):
    D=1 << bits
    assert min(p)>=0 and sum(p)==1
    ints=[(x*D).numerator//(x*D).denominator for x in p]
    order=sorted(range(len(p)),key=lambda i:p[i]*D-ints[i],reverse=True)
    for i in order[:D-sum(ints)]:
        ints[i]+=1
    return [F(x,D) for x in ints]


def filter_data(N,alpha,delta,h,bits=160):
    a=dc.exponents(N,delta,h)
    peak=max(a)
    f=[dc.exp_negative_interval(peak-x,bits)[:2] for x in a]
    e=[dc.exp_negative_interval(alpha*b*F(N+1-b,N),bits)[:2]
       for b in range(N//2+1)]
    fhat=[dc.outward_dyadic((lo+hi)/2,128) for lo,hi in f]
    assert min(fhat)>0
    return f,e,fhat


def certify_joint(N,alpha,delta,h,w,fhat,bits=160):
    """Full physical joint spin/magnetization TV, retaining multiplicity."""
    f,e,_=filter_data(N,alpha,delta,h,bits)
    dims=peer.spin_dimensions(N)
    multiplicities=[dims[b]//(N-2*b+1) for b in range(len(dims))]
    Aw=peer.matvec(peer.sector_matrix(N),w)
    target=[]
    candidate=[]
    for b in range(len(dims)):
        r=N-2*b+1
        for t in range(b,N-b+1):
            target.append((multiplicities[b]*e[b][0]*f[t][0],
                           multiplicities[b]*e[b][1]*f[t][1]))
            candidate.append(Aw[b]*fhat[t]/r)
    Zlo=sum(lo for lo,hi in target)
    Zhi=sum(hi for lo,hi in target)
    Zhat=sum(candidate)
    assert min(candidate)>=0 and Zhat>0 and Zlo>0
    error=sum(max(abs(q/Zhat-lo/Zhi),abs(q/Zhat-hi/Zlo))
              for q,(lo,hi) in zip(candidate,target))/2
    return dc.outward_dyadic(error,bits,True),{'joint_entries':len(target),
        'candidate_normalizer':Zhat,'target_normalizer_lower':Zlo,'target_normalizer_upper':Zhi}


def acquire_filtered_table(N,alpha,delta,h):
    f,e,fhat=filter_data(N,alpha,delta,h)
    A=peer.sector_matrix(N)
    c=[sum(fhat[b:N-b+1])/F(N-2*b+1) for b in range(N//2+1)]
    Z=[sum(A[b][k]*c[b] for b in range(len(c))) for k in range(N+1)]
    columns=[[A[b][k]*c[b]/Z[k] for b in range(len(c))] for k in range(N+1)]
    dims=peer.spin_dimensions(N)
    raw=[dims[b]*((e[b][0]+e[b][1])/2)*c[b] for b in range(len(c))]
    q=[x/sum(raw) for x in raw]
    return q,columns,Z,fhat


def solve_bounded_lp(q,columns,tag,timeout=15):
    payload={'q':[dc.as_record(x) for x in dyadic_simplex(q,40)],
             'columns':[[dc.as_record(x) for x in dyadic_simplex(col,40)] for col in columns]}
    inp=HERE/(tag+'_lp_input.json')
    out=HERE/(tag+'_lp_output.json')
    inp.write_text(json.dumps(payload)+'\n')
    start=time.perf_counter()
    try:
        process=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--solve-lp',
                                '--input',str(inp),'--output',str(out)],
                               capture_output=True,text=True,timeout=timeout,
                               env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'})
    except subprocess.TimeoutExpired:
        receipt={'status':'TIMEOUT_REJECTED','declared_timeout_seconds':timeout,
                 'elapsed_seconds':time.perf_counter()-start,'N':len(columns)-1}
        (HERE/(tag+'_lp_failure.json')).write_text(json.dumps(receipt,indent=2)+'\n')
        raise ArithmeticError('bounded filtered-sector simplex timed out; no output accepted')
    if process.returncode:
        receipt={'status':'LP_SUBPROCESS_REJECTED','returncode':process.returncode,
                 'stderr':process.stderr[-2000:],'elapsed_seconds':time.perf_counter()-start}
        (HERE/(tag+'_lp_failure.json')).write_text(json.dumps(receipt,indent=2)+'\n')
        raise ArithmeticError('bounded filtered-sector simplex failed')
    result=json.loads(out.read_text())
    v=[dc.from_record(x) for x in result['v']]
    assert len(v)==len(columns) and min(v)>=0 and sum(v)==1
    return v,{'backend':'SymPy exact simplex on 40-bit rounded filtered-sector table',
              'objective':result['objective'],'declared_timeout_seconds':timeout,
              'subprocess_seconds':time.perf_counter()-start,
              'child_peak_rss_bytes':result['peak_rss_bytes']}


class CachedBlocks:
    def __init__(self):
        self.cache={}
        self.acquisitions=0

    def compile(self,n,delta,h):
        if n<=1:
            return dc.compile_state(n,delta,h,epsilon='1e-20')
        bits=128
        dps=max(100,math.ceil(bits*0.302)+2*n+50)
        key=(n,delta,dps)
        if key not in self.cache:
            self.cache[key]=dc.numeric_quadrature(n,delta,F(0),dps)
            self.acquisitions+=1
        bx,bw,base_diagnostic=self.cache[key]
        start=time.perf_counter()
        with mp.workdps(dps):
            eh=mp.exp(mp.mpf(h.numerator)/h.denominator)
            factors=[1-x+eh*x for x in bx]
            logs=[mp.log(w)+n*mp.log(t) for w,t in zip(bw,factors)]
            peak=max(logs)
            ws=[mp.exp(x-peak) for x in logs]
            total=mp.fsum(ws)
            ws=[w/total for w in ws]
            xs=[eh*x/t for x,t in zip(bx,factors)]
            D=1 << bits
            nodes=[max(0,min(D,int(mp.floor(x*D+mp.mpf('.5'))))) for x in xs]
            weights=dc.apportion_weights(ws,bits)
        cert=dc.certify_measure(n,delta,h,nodes,weights,bits,bits+32)
        phase_bits,phase_budget=dc.phase_sampling_budget(n,bits)
        density_budget=F(8*n,1 << bits)
        total_budget=dc.from_record(cert['target_trace_distance_upper'])+phase_budget+density_budget
        if total_budget>F('1e-20'):
            raise ArithmeticError('cached block failed exact posterior certificate')
        model={'format':'DICKE_GAUSSIAN_CERTIFIED_V1','n':n,
               'delta':dc.as_record(delta),'h':dc.as_record(h),'epsilon':dc.as_record(F('1e-20')),
               'node_weight_bits':bits,'node_integers':[str(x) for x in nodes],
               'weight_integers':[str(w) for w in weights],
               'phase_modulus':n+1,'phase_sampling_bits':phase_bits,
               'phase_uniform_TV_upper':dc.as_record(phase_budget),
               'predetermined_random_bits_per_sample':bits+phase_bits,
               'component_count':len(nodes)*(n+1),'product_components_stored':False,
               'density_bits':bits,'finite_density_trace_distance_upper':dc.as_record(density_budget),
               'total_output_trace_distance_upper':dc.as_record(total_budget),'certificate':cert,
               'floating_diagnostics':{**base_diagnostic,'field_acquisition':'cached zero-field rule followed by high-precision tilt'},
               'acquisition_attempts':[],'compile_seconds':time.perf_counter()-start,
               'analytic_input_dependency':'c07_s02 delta1 theorem and independent audits',
               'randomness':'Independent uniform bits required; deterministic fixtures use PRNG'}
        assert dc.verify_model(model)
        return model


def all_raw_branches(N,w,fhat):
    raw=[]
    for k in range(N+1):
        for u in range(N-k+1):
            Z=sum(fhat[u:u+k+1])
            mass=w[k]*F(math.comb(N-k,u),(k+1)*(1 << (N-k)))*Z
            raw.append((k,u,Z,mass))
    total=sum(mass for k,u,Z,mass in raw)
    assert total>0
    return raw,total


def hierarchy_error(N,delta,h,w,fhat,branches):
    raw,Z=all_raw_branches(N,w,fhat)
    p={(k,u):mass/Z for k,u,z,mass in raw}
    delivered={(b['k'],b['u']):dc.from_record(b['probability']) for b in branches}
    assert len(delivered)==len(branches) and sum(delivered.values())==1 and min(delivered.values())>=0
    outer=sum(abs(p[key]-delivered.get(key,F(0))) for key in p)/2
    inner=prep=F(0)
    rank_bits=128
    for b in branches:
        k,u=b['k'],b['u']
        model=b['Dicke_model']
        assert dc.verify_model(model)
        assert model['n']==k and dc.from_record(model['delta'])==delta*F(k,N)
        assert dc.from_record(model['h'])==h-delta*F(2*u-(N-k),N)
        q=dc.recovered_populations(k,[int(x) for x in model['node_integers']],
                                  [int(x) for x in model['weight_integers']],model['node_weight_bits'])
        Zblock=sum(fhat[u:u+k+1])
        block_error=sum(abs(x-fhat[u+l]/Zblock) for l,x in enumerate(q))/2
        weight=delivered[(k,u)]
        inner+=weight*block_error
        prep+=weight*(F(math.comb(N,k)+math.comb(N-k,u),2*(1 << rank_bits))
                     +dc.from_record(model['phase_uniform_TV_upper'])
                     +dc.from_record(model['finite_density_trace_distance_upper']))
    return outer,inner,prep


def compile_filtered(N,alpha='3',delta='1',h='1/3',epsilon='1e-6',tag=None):
    start=time.perf_counter()
    alpha,delta,h,epsilon=map(F,(alpha,delta,h,epsilon))
    if type(N) is not int or not 2<=N<=16 or not 0<=alpha<=16 or not 0<=delta<=1 or abs(h)>2:
        raise ValueError('bounded filtered prototype: 2<=N<=16,alpha<=16,delta<=1,|h|<=2')
    if not F('1e-12')<=epsilon<1:
        raise ValueError('bounded filtered accuracy requires 1e-12<=eps<1')
    tag=tag or ('filtered_N'+str(N))
    q,columns,Zcolumns,fhat=acquire_filtered_table(N,alpha,delta,h)
    v,lp=solve_bounded_lp(q,columns,tag,timeout=15)
    iso=[x/z for x,z in zip(v,Zcolumns)]
    norm=sum(iso)
    w=dyadic_simplex([x/norm for x in iso],128)
    joint,jdiag=certify_joint(N,alpha,delta,h,w,fhat)
    raw,normalizer=all_raw_branches(N,w,fhat)
    assert normalizer==jdiag['candidate_normalizer']
    probabilities=dyadic_simplex([mass/normalizer for k,u,z,mass in raw],128)
    cache=CachedBlocks()
    branches=[]
    for (k,u,Z,mass),weight in zip(raw,probabilities):
        if weight==0:
            continue
        inner=cache.compile(k,delta*F(k,N),h-delta*F(2*u-(N-k),N))
        branches.append({'k':k,'u':u,'probability':dc.as_record(weight),'Dicke_model':inner})
    outer,inner,prep=hierarchy_error(N,delta,h,w,fhat,branches)
    total=joint+outer+inner+prep
    if total>epsilon:
        receipt={'status':'POSTERIOR_REJECTED','joint_bound':dc.as_record(joint),
                 'total_bound':dc.as_record(total),'epsilon':dc.as_record(epsilon),'LP':lp}
        (HERE/(tag+'_posterior_failure.json')).write_text(json.dumps(receipt,indent=2)+'\n')
        raise ArithmeticError('filtered output failed exact posterior accuracy gate')
    outer_bits=max(dc.from_record(b['probability']).denominator.bit_length()-1 for b in branches)
    max_inner=max(b['Dicke_model']['predetermined_random_bits_per_sample'] for b in branches)
    if time.perf_counter()-start>30:
        raise ArithmeticError('declared 30s case budget exceeded; output rejected')
    return {'format':'FILTERED_SECTOR_GIBBS_CERTIFIED_BOUNDED_V1','N':N,
            'alpha':dc.as_record(alpha),'delta':dc.as_record(delta),'h':dc.as_record(h),
            'epsilon':dc.as_record(epsilon),'isotropic_weights':[dc.as_record(x) for x in w],
            'filter_values':[dc.as_record(x) for x in fhat],'branches':branches,
            'target_vs_ideal_joint_TV_upper':dc.as_record(joint),
            'outer_rounding_TV':dc.as_record(outer),'block_population_TV':dc.as_record(inner),
            'finite_preparation_TV_upper':dc.as_record(prep),
            'total_target_trace_distance_upper':dc.as_record(total),
            'uniform_rank_bits':128,'outer_sampling_bits':outer_bits,
            'max_inner_sampling_bits':max_inner,
            'predetermined_random_bits_per_sample':outer_bits+256+max_inner,
            'LP':lp,'joint_certificate_entries':jdiag['joint_entries'],
            'cached_zero_field_rules':cache.acquisitions,'branch_count':len(branches),
            'dense_matrix_formed':False,'compile_seconds':time.perf_counter()-start,
            'declared_case_compute_budget_seconds':30}


def verify_filtered(model):
    assert model['format']=='FILTERED_SECTOR_GIBBS_CERTIFIED_BOUNDED_V1'
    N=model['N']
    alpha,delta,h,epsilon=map(dc.from_record,(model['alpha'],model['delta'],model['h'],model['epsilon']))
    assert type(N) is int and 2<=N<=16 and 0<=alpha<=16 and 0<=delta<=1 and abs(h)<=2
    assert F('1e-12')<=epsilon<1
    w=[dc.from_record(x) for x in model['isotropic_weights']]
    fhat=[dc.from_record(x) for x in model['filter_values']]
    assert len(w)==N+1 and len(fhat)==N+1 and min(w)>=0 and sum(w)==1 and min(fhat)>0
    branches=model['branches']
    for b in branches:
        assert type(b['k']) is int and type(b['u']) is int and 0<=b['k']<=N and 0<=b['u']<=N-b['k']
        p=dc.from_record(b['probability'])
        assert p.denominator & (p.denominator-1)==0
    joint,diag=certify_joint(N,alpha,delta,h,w,fhat)
    outer,inner,prep=hierarchy_error(N,delta,h,w,fhat,branches)
    for value,key in [(joint,'target_vs_ideal_joint_TV_upper'),(outer,'outer_rounding_TV'),
                      (inner,'block_population_TV'),(prep,'finite_preparation_TV_upper')]:
        assert value==dc.from_record(model[key])
    total=joint+outer+inner+prep
    assert total==dc.from_record(model['total_target_trace_distance_upper']) and total<=epsilon
    assert type(model['uniform_rank_bits']) is int and model['uniform_rank_bits']==128
    ob=max(dc.from_record(b['probability']).denominator.bit_length()-1 for b in branches)
    ib=max(b['Dicke_model']['predetermined_random_bits_per_sample'] for b in branches)
    assert type(model['outer_sampling_bits']) is int and model['outer_sampling_bits']==ob
    assert type(model['max_inner_sampling_bits']) is int and model['max_inner_sampling_bits']==ib
    assert type(model['predetermined_random_bits_per_sample']) is int and model['predetermined_random_bits_per_sample']==ob+256+ib
    return True


def unrank_subset(N,k,rank):
    assert 0<=rank<math.comb(N,k)
    result=[]
    start=0
    for remaining in range(k,0,-1):
        for i in range(start,N):
            count=math.comb(N-i-1,remaining-1)
            if rank<count:
                result.append(i)
                start=i+1
                break
            rank-=count
    return result


def sample_filtered(model,rng=None):
    rng=random.SystemRandom() if rng is None else rng
    N=model['N']
    branches=model['branches']
    index=peer.sample_dyadic([dc.from_record(b['probability']) for b in branches],rng)
    b=branches[index]
    k,u=b['k'],b['u']
    subset=unrank_subset(N,k,(rng.getrandbits(128)*math.comb(N,k)) >> 128)
    complement=[i for i in range(N) if i not in subset]
    ones=[complement[i] for i in unrank_subset(N-k,u,(rng.getrandbits(128)*math.comb(N-k,u)) >> 128)]
    component=dc.sample_product(b['Dicke_model'],rng)
    pad=model['max_inner_sampling_bits']-component['random_bits_consumed']
    if pad:
        rng.getrandbits(pad)
    local=[]
    for i in range(N):
        if i in subset:
            state=component['finite_product_local_density']
        else:
            bit=int(i in ones)
            state={'diagonal':[dc.as_record(1-bit),dc.as_record(bit)],
                   'upper_right_real':dc.as_record(0),'upper_right_imag':dc.as_record(0),
                   'PSD_and_trace_one_exact':True}
        local.append(state)
    return {'branch_index':index,'k':k,'u':u,'subset':subset,'complement_ones':ones,
            'local_density_matrices':local,'random_bits_consumed':model['predetermined_random_bits_per_sample'],
            'ensemble_target_trace_distance_upper':model['total_target_trace_distance_upper']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--solve-lp',action='store_true')
    parser.add_argument('--input',type=Path)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--n',type=int,default=8)
    parser.add_argument('--alpha',default='3')
    parser.add_argument('--delta',default='1')
    parser.add_argument('--h',default='1/3')
    parser.add_argument('--epsilon',default='1e-6')
    args=parser.parse_args()
    if args.solve_lp:
        payload=json.loads(args.input.read_text())
        v,obj=peer.exact_simplex_fixture([dc.from_record(x) for x in payload['q']],
                                        [[dc.from_record(x) for x in col] for col in payload['columns']])
        import platform
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if platform.system()=='Darwin' else 1024)
        args.output.write_text(json.dumps({'v':[dc.as_record(x) for x in v],
                                          'objective':dc.as_record(obj),'peak_rss_bytes':rss})+'\n')
        return
    model=compile_filtered(args.n,args.alpha,args.delta,args.h,args.epsilon)
    assert verify_filtered(model)
    result={'model':model,'samples':[sample_filtered(model,random.Random(20261008+i)) for i in range(4)]}
    text=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text,end='')


if __name__=='__main__':
    main()
