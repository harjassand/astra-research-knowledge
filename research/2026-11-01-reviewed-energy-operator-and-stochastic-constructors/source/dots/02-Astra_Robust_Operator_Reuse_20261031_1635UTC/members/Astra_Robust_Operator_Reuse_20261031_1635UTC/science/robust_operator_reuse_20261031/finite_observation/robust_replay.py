#!/usr/bin/env python3
"""Set-valued operator observations and bounded-bit, contraction-certified replay.

Exact arithmetic is used OFFLINE to check finite data, not to access the truth.
The only hidden-matrix access is in OutwardOracle, used by tests as a mock.
"""
import json
import math
from pathlib import Path
import sys
import time
import sympy as sp

sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from learn import inner, residual, measure, encode_matrix
from verify import matrix as decode_matrix


def sqrt_up(x,bits=30):
    x=sp.Rational(x)
    if x<0:raise ValueError('negative square')
    s=1<<bits; z=math.isqrt(int(x.p)*s*s//int(x.q))
    if z*z*int(x.q)<int(x.p)*s*s:z+=1
    return sp.Rational(z,s)


def rounded(x,bits):
    """Nearest grid point, ties toward +infinity, using integer arithmetic."""
    x=sp.Rational(x);s=1<<bits
    return sp.Rational((2*int(x.p)*s+int(x.q))//(2*int(x.q)),s)


def round_matrix(A,bits):return A.applyfunc(lambda x:rounded(x,bits))


def psd(S):
    if S.rows!=S.cols or S!=S.T:return False
    T=S.copy();n=T.rows
    for k in range(n):
        pivot=T[k,k]
        if pivot<0:return False
        if pivot==0:
            if any(T[k,j]!=0 for j in range(k+1,n)):return False
            continue
        for i in range(k+1,n):
            for j in range(i,n):
                T[i,j]-=T[i,k]*T[k,j]/pivot;T[j,i]=T[i,j]
    return True


def norm_up(A,G,bits=26):
    """Rational upper bound on the induced G norm; final PSD test is exact."""
    F=(G.inv()*A.T*G*A).trace()
    hi=int(sp.ceiling(sqrt_up(F,bits)*(1<<bits)));lo=0;s=1<<bits
    while lo<hi:
        mid=(lo+hi)//2;t=sp.Rational(mid,s)
        if psd(t*t*G-A.T*G*A):hi=mid
        else:lo=mid+1
    out=sp.Rational(hi,s)
    assert psd(out*out*G-A.T*G*A)
    return out


def validate_boxes(boxes):
    if type(boxes) is not list or not boxes:raise ValueError('empty boxes')
    n=boxes[0][0].rows
    if n<1:raise ValueError('dimension')
    for pair in boxes:
        if type(pair) not in (tuple,list) or len(pair)!=2:raise ValueError('box pair')
        low,up=pair
        if low.shape!=up.shape or low.shape!=(n,n):raise ValueError('shape')
        if any(not isinstance(x,sp.Rational) for x in list(low)+list(up)):raise ValueError('rational boxes')
        if any(not 0<=l<=u<=1 for l,u in zip(low,up)):raise ValueError('entry interval')
        if any(sum(low.row(i))>1 or sum(up.row(i))<1 for i in range(n)):raise ValueError('empty row simplex')
    return n


def centers(boxes):
    n=validate_boxes(boxes);out=[]
    for low,up in boxes:
        C=low.copy()
        for i in range(n):
            need=1-sum(low.row(i));cap=sum(up.row(i)-low.row(i))
            if cap:
                for j in range(n):C[i,j]+=need*(up[i,j]-low[i,j])/cap
        assert C*sp.ones(n,1)==sp.ones(n,1)
        out.append(C)
    return out


class OutwardOracle:
    """Mock certified precision oracle; hidden truth is NOT passed to learn()."""
    def __init__(self,truth):self._truth=truth;self.calls=[]
    def observe(self,bits):
        if type(bits) is not int or bits<1:raise ValueError('precision')
        s=1<<bits;boxes=[]
        for A in self._truth:
            low=A.applyfunc(lambda x:sp.Rational(int(sp.floor(x*s)),s))
            up=low.applyfunc(lambda x:min(sp.Rational(1),x+sp.Rational(1,s)))
            assert all(l<=x<=u for l,x,u in zip(low,A,up))
            boxes.append((low,up))
        self.calls.append({'entry_precision_bits':bits,'returned_interval_endpoints':2*sum(A.rows*A.cols for A in self._truth),
                           'output_payload_bit_upper':2*(bits+2)*sum(A.rows*A.cols for A in self._truth),
                           'scope':'Oracle output accounting only; a real certified solver/sample acquisition cost is additional.'})
        return boxes


def geometries(C,bits=16):
    n=C[0].rows;uniform=sp.ones(n,1)/n;out=[]
    avg=sum(C,sp.zeros(n))/len(C)
    null=(avg.T-sp.eye(n)).nullspace()
    if len(null)==1 and sum(null[0])!=0:
        h=null[0]/sum(null[0])
        if all(x>0 for x in h):
            # Positive bounded-precision weights, normalized exactly.
            counts=[max(1,int(sp.floor(x*(1<<bits)))) for x in h]
            proposal=sp.Matrix(counts)/sum(counts)
            out.append(('observed_pooled_equilibrium_proposal',proposal))
    if not out or out[0][1]!=uniform:out.append(('uniform_fallback',uniform))
    return out


def uncertainty(boxes,C,h):
    n=len(h);sq=sp.Rational(0)
    for (low,up),A in zip(boxes,C):
        sq=max(sq,sum(h[i]/h[j]*max(A[i,j]-low[i,j],up[i,j]-A[i,j])**2 for i in range(n) for j in range(n)))
    return sqrt_up(sq)


def append_basis(x,basis,h):
    v=residual(x,basis,h)
    if v==sp.zeros(len(h),1):return False
    g=inner(v,v,h)
    # Rational power-of-two scaling; resulting Gram diagonal is in [1,4).
    while g<1:v*=2;g*=4
    while g>=4:v/=2;g/=4
    basis.append(v);return True


def stable_blocks(C,V,h,coefficient_bits=24):
    H=sp.diag(*h);G=V.T*H*V;blocks=[];scales=[]
    for A in C:
        K=G.inv()*V.T*H*A*V
        M=round_matrix(K,coefficient_bits)
        scale=max(sp.Rational(1),norm_up(M,G))
        B=M/scale
        assert psd(G-B.T*G*B)
        blocks.append(B);scales.append(str(scale))
    return blocks,scales


def certificate(boxes,b,ell,V,h,B,length,query_bits):
    n=validate_boxes(boxes);m=len(boxes)
    if type(length) is not int or length<0 or type(query_bits) is not int or query_bits<1:raise ValueError('task')
    if h.shape!=(n,1) or any(x<=0 for x in h) or sum(h)!=1:raise ValueError('geometry')
    if b.shape!=ell.shape or b.shape!=(n,1):raise ValueError('observable shape')
    if any(not isinstance(x,sp.Rational) for x in list(h)+list(b)+list(ell)+list(V)):raise ValueError('rational data')
    H=sp.diag(*h);G=V.T*H*V;r=V.cols
    if r<1 or r>n or G!=sp.diag(*[G[i,i] for i in range(r)]) or any(G[i,i]<=0 for i in range(r)):raise ValueError('orthogonal full-rank basis')
    left=H.inv()*ell;u=G.inv()*V.T*H*b
    if V*u!=b or V*(G.inv()*V.T*ell)!=left or V*(G.inv()*V.T*h)!=sp.ones(n,1):raise ValueError('task/constant missing from basis')
    if len(B)!=m or any(X.shape!=(r,r) or not psd(G-X.T*G*X) for X in B):raise ValueError('unstable replay')
    C=centers(boxes);adj=[H.inv()*A.T*H for A in C]
    images=[[[A*V[:,j] for j in range(r)] for A in ops] for ops in (C,adj)]
    (in2,out2),_=measure([V[:,j] for j in range(r)],images,h,m)
    # Transport observations in the original Markov infinity norm before
    # invoking the learned Hilbert geometry on the finite observed centers.
    eta_inf=max(sum(max(A[i,j]-low[i,j],up[i,j]-A[i,j]) for j in range(n))
                for (low,up),A in zip(boxes,C) for i in range(n))
    eta=sp.Rational(0)
    enter=(sqrt_up(in2)+eta) if r<n else sp.Rational(0)
    leave=(sqrt_up(out2)+eta) if r<n else sp.Rational(0)
    discrepancy=eta+max(norm_up(G.inv()*V.T*H*A*V-X,G) for A,X in zip(C,B))
    minor=min(A[i,j]/h[j] for A in C for i in range(n) for j in range(n))
    minor=max(0,min(1,minor))
    kappa=max(sum(h[i]*A[i,j] for i in range(n))/h[j] for A in C for j in range(n))
    if kappa<minor:raise ValueError('invalid minorization envelope')
    alpha=sqrt_up((1-minor)*(kappa-minor)) if r<n else sp.Rational(0)
    maxb=max(abs(x) for x in b);normleft=sqrt_up((ell.T*H.inv()*ell)[0])
    t=sp.Rational(0);tsum=sp.Rational(0)
    for _ in range(length):tsum+=t;t=min(1,alpha*t+enter)
    observation=sum(abs(x) for x in ell)*maxb*length*eta_inf
    compression=normleft*maxb*(length*discrepancy+leave*tsum)
    model=observation+compression
    round_step=sqrt_up(max(G[i,i] for i in range(r))*r)*sp.Rational(1,2**(query_bits+1))
    execution=normleft*(length+1)*round_step+sp.Rational(1,2**(query_bits+1))
    bound=model+execution
    return {'bound':bound,'model_bound':model,'observation_bound':observation,'compression_bound':compression,
            'execution_bound':execution,'eta_inf':eta_inf,'eta':eta,'enter':enter,'leave':leave,
            'alpha':alpha,'minorization':minor,'geometry_incoming_bound':kappa,'discrepancy':discrepancy,
            'normleft':normleft,'maxb':maxb,'round_step':round_step,'gram':G,'right':u,'output':V.T*ell,
            'rank':r,'ambient':n,'length':length,'query_bits':query_bits}


def replay(model,word):
    cert=model['certificate'];p=cert['query_bits'];L=cert['length']
    if len(word)>L:raise ValueError('horizon')
    state=round_matrix(cert['right'],p);bits=0
    for a in word:
        if type(a) is not int or not 0<=a<len(model['operators']):raise ValueError('letter')
        state=round_matrix(model['operators'][a]*state,p)
        bits=max(bits,max(max(abs(int(x.p)).bit_length(),int(x.q).bit_length()) for x in state))
    ans=rounded((cert['output'].T*state)[0],p)
    return ans,{'state_integer_bits':bits,'state_entries':len(state),'word_length':len(word)}


def common_integer_matrix(A):
    denominator=math.lcm(*(int(x.q) for x in A))
    numerators=[[int(A[i,j]*denominator) for j in range(A.cols)] for i in range(A.rows)]
    return {'denominator':denominator,'numerators':numerators}


def compile_integer_replay(operators,u,output,p):
    """Paid common-denominator acquisition for an actual integer replay backend."""
    if type(p) is not int or p<1:raise ValueError('grid precision')
    scale=1<<p
    blocks=[common_integer_matrix(A) for A in operators]
    out=common_integer_matrix(output.T)
    state=[int(rounded(x,p)*scale) for x in u]
    common_bits=max([abs(x).bit_length() for block in blocks+[out] for row in block['numerators'] for x in row]+
                    [block['denominator'].bit_length() for block in blocks+[out]])
    return {'operators':blocks,'output':out,'initial_grid_state':state,'bits':p,
            'common_denominator_coefficient_bits':common_bits}


def integer_step(block,state):
    D=block['denominator'];sums=[sum(x*y for x,y in zip(row,state)) for row in block['numerators']]
    return [(2*x+D)//(2*D) for x in sums],max((abs(x).bit_length() for x in sums),default=0)


def integer_output(compiled,state):
    grid,_=integer_step(compiled['output'],state)
    return sp.Rational(grid[0],1<<compiled['bits'])


def acquire(oracle,b,ell,length,tolerance,precisions=(8,12,16,20,24),coefficient_bits=24,query_bits=30):
    tic=time.perf_counter();trials=[];total_mvps=0;check_mvps=0;projection_blocks=0;peak_images=0
    for p in precisions:
        boxes=oracle.observe(p);C=centers(boxes);n=C[0].rows
        for name,h in geometries(C):
            H=sp.diag(*h)
            eta_inf=max(sum(max(A[i,j]-low[i,j],up[i,j]-A[i,j]) for j in range(n))
                        for (low,up),A in zip(boxes,C) for i in range(n))
            floor=sum(abs(x) for x in ell)*max(abs(x) for x in b)*length*eta_inf
            if floor>tolerance:
                trials.append({'precision':p,'geometry':name,'status':'SKIP_THIS_CERTIFICATE_NOISE_FLOOR','bound_floor':str(floor)})
                continue
            basis=[];adj=[H.inv()*A.T*H for A in C]
            images=[[[] for _ in C] for _ in range(2)]
            def add(x):
                nonlocal total_mvps
                if not append_basis(x,basis,h):return False
                for side,ops in enumerate((C,adj)):
                    for a,A in enumerate(ops):images[side][a].append(A*basis[-1]);total_mvps+=1
                return True
            for x in (sp.ones(n,1),b,H.inv()*ell):add(x)
            while True:
                V=sp.Matrix.hstack(*basis);B,scales=stable_blocks(C,V,h,coefficient_bits)
                cert=certificate(boxes,b,ell,V,h,B,length,query_bits)
                check_mvps+=2*len(C)*len(basis);projection_blocks+=2*len(C)
                peak_images=max(peak_images,2*len(C)*n*len(basis))
                trials.append({'precision':p,'geometry':name,'rank':len(basis),'bound':str(cert['bound']),
                               'bound_float':float(cert['bound']),'model_bound_float':float(cert['model_bound']),
                               'stabilizing_scales':scales,'status':'PASS' if cert['bound']<=tolerance else 'REFINE_BASIS'})
                if cert['bound']<=tolerance:
                    return {'basis':V,'metric':h,'operators':B,'boxes':boxes,'certificate':cert,
                            'tolerance':sp.Rational(tolerance),'ledger':{'trials':trials,'oracle_calls':oracle.calls,
                                'construction_generator_adjoint_mvps':total_mvps,
                                'candidate_certificate_center_image_mvps':check_mvps,
                                'candidate_dense_center_projection_blocks':projection_blocks,
                                'peak_retained_construction_image_entries':peak_images,
                                'acquisition_seconds':time.perf_counter()-tic,
                                'scope':'All candidate time included. Dense metric/projection/PSD work is not reduced to the image-MVP counters. Scalar/intermediate bit operations are not individually instrumented; complete observations stored.'}}
                if len(basis)==n:break
                _,best=measure(basis,images,h,len(C))
                if best[0]==0:break
                assert add(best[1])
    return {'admitted':False,'ledger':{'trials':trials,'oracle_calls':oracle.calls,'construction_generator_adjoint_mvps':total_mvps,
            'candidate_certificate_center_image_mvps':check_mvps,'candidate_dense_center_projection_blocks':projection_blocks,
            'peak_retained_construction_image_entries':peak_images,'acquisition_seconds':time.perf_counter()-tic},
            'scope':'INCONCLUSIVE at this budget, not proof that no useful representation exists.'}


def encode_model(model):
    cert=model['certificate']
    out={'basis':encode_matrix(model['basis']),'metric':encode_matrix(model['metric']),
         'operators':[encode_matrix(A) for A in model['operators']],
         'length':cert['length'],'query_bits':cert['query_bits'],'tolerance':str(model['tolerance']),
         'bound':str(cert['bound']),'ledger':model['ledger']}
    return out


def verify(boxes,b,ell,record,*,expected_length,expected_tolerance):
    try:
        if type(record) is not dict or type(expected_length) is not int or expected_length<0:return False
        if isinstance(expected_tolerance,(bool,float)):return False
        tol=sp.Rational(expected_tolerance)
        if tol<=0 or record['length']!=expected_length or type(record['length']) is not int:return False
        if type(record['tolerance']) is not str or sp.Rational(record['tolerance'])!=tol:return False
        if type(record['query_bits']) is not int:return False
        V=decode_matrix(record['basis']);h=decode_matrix(record['metric'])
        B=[decode_matrix(X) for X in record['operators']]
        cert=certificate(boxes,b,ell,V,h,B,expected_length,record['query_bits'])
        return type(record['bound']) is str and sp.Rational(record['bound'])==cert['bound'] and bool(cert['bound']<=tol)
    except (KeyError,ValueError,TypeError,IndexError,AttributeError,AssertionError,ZeroDivisionError):return False
