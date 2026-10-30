"""Ordinary meet-in-the-middle compiler for the exact S3/CZ gate alphabet.

A=exp(-i*2*pi*YI/3), B=CZ exp(-i*2*pi*IY/3) CZ. Their abstract SU(2)
axes anticommute. The other commuting SU(2) factor follows by swapping
the two blocks. This is a finite example compiler, not an optimal
synthesis algorithm or a certified physical error budget.

Run: OPENBLAS_NUM_THREADS=1 python p2_continuous/real_compiler.py --depth 15
"""
import argparse
import json
import math
import time
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree


def mul(a, b):
    a, b = np.broadcast_arrays(np.asarray(a), np.asarray(b))
    return np.concatenate([
        (a[..., :1]*b[..., :1] - np.sum(a[..., 1:]*b[..., 1:], axis=-1, keepdims=True)),
        a[..., :1]*b[..., 1:] + b[..., :1]*a[..., 1:]
        + np.cross(a[..., 1:], b[..., 1:])], axis=-1)


def conj(a):
    b = np.array(a, copy=True); b[..., 1:] *= -1; return b


S = math.sqrt(3)/2
GENERATORS = np.array([[-.5,S,0,0],[-.5,-S,0,0],[-.5,0,S,0],[-.5,0,-S,0]])
LABELS = ['A','a','B','b']


def net(depth):
    """Every reduced word in C3*C3 up to depth, without quadratic pairs."""
    qs = [np.array([[1.,0,0,0]])]
    codes = [np.array([0], dtype=np.uint64)]
    lengths = [np.array([0], dtype=np.uint8)]
    q = GENERATORS.copy()
    code = np.arange(4,dtype=np.uint64)
    last = np.arange(4,dtype=np.uint8)//2
    for length in range(1, depth+1):
        qs.append(q); codes.append(code); lengths.append(np.full(len(q),length,dtype=np.uint8))
        if length == depth: break
        nxt = np.repeat(2*(1-last),2) + np.tile(np.array([0,1],dtype=np.uint8),len(last))
        q = mul(np.repeat(q,2,axis=0), GENERATORS[nxt])
        code = (np.repeat(code,2) << np.uint64(2)) | nxt.astype(np.uint64)
        last = nxt//2
    return np.concatenate(qs),np.concatenate(codes),np.concatenate(lengths)


def decode(code, length):
    out=[]
    for _ in range(int(length)):
        out.append(int(code)&3); code=int(code)>>2
    return out[::-1]


def reduce_word(word):
    out=[]
    for g in word:
        if out and out[-1]//2 == g//2:
            old=out.pop(); power=((1 if old%2==0 else -1)+(1 if g%2==0 else -1))%3
            if power: out.append(2*(g//2)+(0 if power==1 else 1))
        else: out.append(g)
    return out


def product(word):
    q=np.array([1.,0,0,0])
    for x in word: q=mul(q,GENERATORS[x])
    return q


def compile_target(target, q, codes, lengths, tree):
    # v*w=target -> v=target*w^{-1}; global +/- is immaterial.
    desired=mul(target,conj(q))
    dp,ip=tree.query(desired,workers=1)
    dm,im=tree.query(-desired,workers=1)
    choose_minus=dm<dp
    distances=np.minimum(dp,dm)
    ix=int(np.argmin(distances)); iy=int(im[ix] if choose_minus[ix] else ip[ix])
    word=reduce_word(decode(codes[iy],lengths[iy])+decode(codes[ix],lengths[ix]))
    got=product(word)
    err=float(min(np.linalg.norm(got-target),np.linalg.norm(got+target)))
    b_count=sum(x//2==1 for x in word)
    return dict(target_quaternion=target.tolist(),quaternion=got.tolist(),
                word=''.join(LABELS[x] for x in word),letters=len(word),
                cyclic_permutations=len(word),orbital_transpositions=2*len(word),
                parity_CZ=2*b_count,projective_operator_norm_error=err,
                matrix_order='Left-to-right written product; execute physical gates in reversed matrix order.')


def realification(U):
    return np.block([[U.real,-U.imag],[U.imag,U.real]])


def run(depth):
    start=time.perf_counter(); q,codes,lengths=net(depth); nettime=time.perf_counter()-start
    assert np.max(abs(np.linalg.norm(q,axis=1)-1))<1e-12
    start=time.perf_counter(); tree=cKDTree(q); treetime=time.perf_counter()-start
    samples=[('local_rebit_pi_over_8',np.array([math.cos(math.pi/8),math.sin(math.pi/8),0,0])),
             ('coupled_rebit_pi_over_8',np.array([math.cos(math.pi/8),0,math.sin(math.pi/8),0])),
             ('generic',np.r_[math.cos(.731),math.sin(.731)*np.array([1.,2.,3.])/math.sqrt(14)])]
    results=[]
    for name,target in samples:
        then=time.perf_counter(); result=compile_target(target,q,codes,lengths,tree)
        result.update(name=name,query_seconds=time.perf_counter()-then)
        results.append(result)
    I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1.,-1.]).astype(complex)
    first=[np.kron(Y,I),np.kron(Z,Y),np.kron(X,Y)]
    second=[np.kron(I,Y),np.kron(Y,Z),np.kron(Y,X)]
    commute=max(np.linalg.norm(a@b-b@a,2) for a in first for b in second)
    lie_rank=int(np.linalg.matrix_rank(np.stack([(1j*p).real.ravel() for p in first+second])))
    def embed(q):
        return q[0]*np.eye(4)-1j*sum(q[k+1]*first[k] for k in range(3))
    for result in results:
        unitary=np.eye(4,dtype=complex)
        for label in result['word']:
            unitary=unitary@embed(GENERATORS[LABELS.index(label)])
        target=embed(result['target_quaternion'])
        result['independent_matrix_norm_error']=float(min(
            np.linalg.norm(unitary-target,2),np.linalg.norm(unitary+target,2)))
        assert abs(result['independent_matrix_norm_error']-result['projective_operator_norm_error'])<1e-12
    rz=np.diag([np.exp(-.231j),np.exp(.231j)])
    re=realification(rz)
    assert np.linalg.norm(re.T@re-np.eye(4))<1e-12
    result=dict(half_depth=depth,net_size=len(q),net_seconds=nettime,tree_seconds=treetime,
                largest_net_norm_error=float(np.max(abs(np.linalg.norm(q,axis=1)-1))),
                first_second_lie_commutator_norm=float(commute),so4_lie_rank=lie_rank,
                product_half_trace=float(mul(GENERATORS[0],GENERATORS[2])[0]),
                compiled=results,
                scope='Established real simulation with one extra initialized rebit; not an isometric realification of an arbitrary unknown complex input. Search and error numbers are floating point. Physical gate error, state preparation, measurement, routing and wall time are additional.')
    Path(__file__).with_name(f'real_compiler_depth{depth}_results.json').write_text(json.dumps(result,indent=2)+'\n')
    Path(__file__).with_name('real_compiler_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--depth',type=int,default=15);a=p.parse_args();run(a.depth)
