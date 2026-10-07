"""Bounded N<=3 whole-Gibbs fixture using explicitly imported exact LP.

Independent full-matrix rational certificate; no polynomial simplex claim.
Reads c01_s03 helper without writing its directory. Does not modify its source.
"""
from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import combinations
import json
import math
from pathlib import Path
import random
import sys
import time

from dicke_compiler import (as_record,from_record,compile_state,verify_model,
                            recovered_populations,exp_negative_interval,
                            sample_product,outward_dyadic)

HERE = Path(__file__).resolve().parent
PEER_SOURCE = HERE.parents[1]/'c01_s03'/'axial_compiler'/'axial_acquisition.py'
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('c01_s03_axial_readonly',PEER_SOURCE)
peer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(peer)


def matmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def joint_projectors(N):
    """Acquire J² exactly in computational basis; no Schur oracle."""
    dim = 1 << N
    J2 = [[F(0) for _ in range(dim)] for _ in range(dim)]
    for z in range(dim):
        m = F(2*z.bit_count()-N,2)
        J2[z][z] = m*m+F(N,2)
        for i in range(N):
            for j in range(i):
                if ((z >> i)&1) != ((z >> j)&1):
                    J2[z ^ (1 << i) ^ (1 << j)][z] += 1
    eigenvalues = [F(N-2*b,2)*(F(N-2*b,2)+1) for b in range(N//2+1)]
    all_projectors = []
    I = [[F(int(i==j)) for j in range(dim)] for i in range(dim)]
    for b,e in enumerate(eigenvalues):
        P = I
        for c,other in enumerate(eigenvalues):
            if c == b:
                continue
            factor = [[(J2[i][j]-other*int(i==j))/(e-other)
                       for j in range(dim)] for i in range(dim)]
            P = matmul(P,factor)
        assert matmul(P,P)==P
        for r in range(N+1):
            Q = [[P[i][j] if i.bit_count()==r and j.bit_count()==r else F(0)
                  for j in range(dim)] for i in range(dim)]
            tr = sum(Q[i][i] for i in range(dim))
            if tr:
                assert tr.denominator==1 and matmul(Q,Q)==Q
                all_projectors.append((e,F(2*r-N,2),int(tr),Q))
    total = [[sum(Q[i][j] for _,_,_,Q in all_projectors)
              for j in range(dim)] for i in range(dim)]
    assert total==I
    return all_projectors


def target_matrix_intervals(N,alpha,delta,h,bits=180):
    projects = joint_projectors(N)
    logs = [alpha*e/N-delta*m*m/N+h*m for e,m,_,_ in projects]
    peak = max(logs)
    values = [exp_negative_interval(peak-v,bits)[:2] for v in logs]
    Zlo = sum(tr*lo for (_,_,tr,_),(lo,hi) in zip(projects,values))
    Zhi = sum(tr*hi for (_,_,tr,_),(lo,hi) in zip(projects,values))
    dim = 1 << N
    result = []
    for i in range(dim):
        row = []
        for j in range(dim):
            lo=hi=F(0)
            for (_,_,_,Q),(a,b) in zip(projects,values):
                c = Q[i][j]
                lo += c*(a if c>=0 else b)
                hi += c*(b if c>=0 else a)
            options = [x/Z for x in (lo,hi) for Z in (Zlo,Zhi)]
            row.append((min(options),max(options)))
        result.append(row)
    return result


def mixture_matrix(N,branches,models):
    dim = 1 << N
    rho = [[F(0) for _ in range(dim)] for _ in range(dim)]
    for branch,model in zip(branches,models):
        k,u = branch['k'],branch['u']
        weight = branch['probability']
        q = recovered_populations(k,[int(v) for v in model['node_integers']],
                                  [int(v) for v in model['weight_integers']],model['node_weight_bits'])
        for subset in combinations(range(N),k):
            complement = [i for i in range(N) if i not in subset]
            for ones in combinations(complement,u):
                fixed = sum(1 << i for i in ones)
                for l in range(k+1):
                    states = [fixed+sum(1 << i for i in local)
                              for local in combinations(subset,l)]
                    atom = weight*q[l]/(math.comb(N,k)*math.comb(N-k,u)*math.comb(k,l))
                    for a in states:
                        for b in states:
                            rho[a][b] += atom
    assert sum(rho[i][i] for i in range(dim))==1
    return rho


def recursive_record(x):
    if isinstance(x,F):
        return as_record(x)
    if isinstance(x,dict):
        return {str(k):recursive_record(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):
        return [recursive_record(v) for v in x]
    return x


def sample_whole(N,branches,models,rng):
    index = peer.sample_dyadic([b['probability'] for b in branches],rng)
    branch,model = branches[index],models[index]
    k,u = branch['k'],branch['u']
    # The bounded fixture explicitly materializes <=3-site subset lists.
    subsets = list(combinations(range(N),k))
    rank = (rng.getrandbits(128)*len(subsets)) >> 128
    subset = subsets[rank]
    complement = [i for i in range(N) if i not in subset]
    strings = list(combinations(complement,u))
    rank = (rng.getrandbits(128)*len(strings)) >> 128
    ones = strings[rank]
    component = sample_product(model,rng)
    pure0 = {'diagonal':[as_record(1),as_record(0)],
             'upper_right_real':as_record(0),'upper_right_imag':as_record(0),
             'PSD_and_trace_one_exact':True}
    pure1 = {'diagonal':[as_record(0),as_record(1)],
             'upper_right_real':as_record(0),'upper_right_imag':as_record(0),
             'PSD_and_trace_one_exact':True}
    states = [component['finite_product_local_density'] if i in subset
              else (pure1 if i in ones else pure0) for i in range(N)]
    for s in states:
        diag = list(map(from_record,s['diagonal']))
        re,im = from_record(s['upper_right_real']),from_record(s['upper_right_imag'])
        assert sum(diag)==1 and diag[0]*diag[1] >= re*re+im*im
    return {'branch_index':index,'k':k,'u':u,'subset':list(subset),
            'complement_ones':list(ones),'local_density_matrices':states}


def run(delta_one=False):
    start=time.perf_counter()
    records=[]
    rng=random.Random(20261008)
    inner=[('1','1/3'),('1','-2/5')] if delta_one else [('1/2','1/3'),('1/4','-2/5')]
    grid=[(N,a,d,h) for N in [2,3] for a in ['0','1/2','3'] for d,h in inner]
    for N,astr,dstr,hstr in grid:
        alpha,delta,h=map(F,(astr,dstr,hstr))
        epsilon=F('1e-12')
        w,meta=peer.acquire_k_weights(N,alpha,delta,h,epsilon,
                                      lp_backend=peer.exact_simplex_fixture)
        assert w is not None and sum(w)==1 and min(w)>=0
        branches,bmeta=peer.acquire_branches(N,delta,h,w,epsilon)
        models=[]
        for branch in branches:
            k=branch['k']
            dd=delta*F(k,N)
            hh=h-2*delta*branch['m']/N
            model=compile_state(k,dd,hh,epsilon='1e-30')
            assert verify_model(model)
            models.append(model)
        rho=mixture_matrix(N,branches,models)
        interval=target_matrix_intervals(N,alpha,delta,h)
        raw=F(0)
        for i,row in enumerate(rho):
            for j,value in enumerate(row):
                lo,hi=interval[i][j]
                raw+=max(abs(value-lo),abs(value-hi))
        matrix_bound=outward_dyadic(raw/2,160,True)
        # Exact uniform phase/subsets give rho. Charge bounded draw biases and
        # finite density preparation for the actual sampler separately.
        preparation=F(0)
        for branch,model in zip(branches,models):
            k,u=branch['k'],branch['u']
            bias=(F(math.comb(N,k)+math.comb(N-k,u),2*(1 << 128))
                  +from_record(model['phase_uniform_TV_upper'])
                  +from_record(model['finite_density_trace_distance_upper']))
            preparation+=branch['probability']*bias
        bound=matrix_bound+preparation
        assert bound <= epsilon
        record={'N':N,'alpha':astr,'delta':dstr,'h':hstr,
                'full_matrix_rational_certificate_trace_distance_upper':as_record(matrix_bound),
                'finite_sampler_additional_error_upper':as_record(preparation),
                'total_target_trace_distance_upper':as_record(bound),
                'epsilon':as_record(epsilon),'K_weights':recursive_record(w),
                'LP_metadata':recursive_record(meta),'branch_metadata':recursive_record(bmeta),
                'branches':recursive_record([{'k':b['k'],'u':b['u'],'probability':b['probability']} for b in branches]),
                'branch_count':len(branches),'Dicke_models':models,
                'samples':[sample_whole(N,branches,models,rng) for _ in range(2)],
                'certificate':'Exact joint-spin projector target entry intervals; half entrywise L1 bounds half trace norm',
                'LP_backend':'SymPy exact bounded simplex fixture; no polynomial runtime claim'}
        records.append(record)
    text=json.dumps({'status':'PASS','cases':len(records),'records':records,
                     'elapsed_seconds':time.perf_counter()-start,
                     'peer_source':str(PEER_SOURCE),
                     'peer_source_sha256':hashlib.sha256(PEER_SOURCE.read_bytes()).hexdigest(),
                     'scope':'N2/N3 bounded whole finite-alpha Gibbs fixture; exact posterior matrix certificate'},indent=2)+'\n'
    filename='finite_alpha_delta1_checks.json' if delta_one else 'finite_alpha_checks.json'
    (HERE/filename).write_text(text)
    print(json.dumps({'status':'PASS','cases':len(records),
                      'elapsed_seconds':time.perf_counter()-start,'output_bytes':len(text.encode())}),flush=True)


if __name__=='__main__':
    run('--delta-one' in sys.argv)
