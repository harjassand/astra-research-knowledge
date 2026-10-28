"""Acquire a rational fixed24-state physical frame and all two-site kernels.

The theorem covers arbitrary rational two-qubit operations followed by fresh
unobserved Phi_7/4 noise on both sites. This actual kernel uses a rational
non-Clifford controlled rotation. LP is only a suggestion; each column is
reconstructed and checked with exact Fraction arithmetic.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import permutations,product
import warnings,json,time,hashlib
import numpy as np,sympy as S
from scipy.optimize import linprog,OptimizeWarning
ROOT=Path(__file__).resolve().parent
warnings.filterwarnings('ignore',message='Unrecognized options detected.*',category=OptimizeWarning)


def exact_solve(columns,b):
    n=len(columns);M=[[columns[j][i] for j in range(n)]+[b[i]] for i in range(16)]
    for j in range(n):
        pivot=next(i for i in range(j,16) if M[i][j])
        M[j],M[pivot]=M[pivot],M[j];d=M[j][j]
        M[j]=[x/d for x in M[j]]
        for i in range(16):
            if i!=j:
                t=M[i][j]
                if t:M[i]=[x-t*y for x,y in zip(M[i],M[j])]
    assert all(not any(row[:-1]) and row[-1]==0 for row in M[n:])
    return [M[j][-1] for j in range(n)]


def main():
    start=time.monotonic()
    frames=sorted(set(tuple(F(s*x,5) for s,x in zip(signs,p))
                      for p in permutations((0,3,4)) for signs in product((-1,1),repeat=3)))
    assert len(frames)==24 and all(sum(x*x for x in r)==1 for r in frames)
    ext=[(F(1),)+r for r in frames]
    columns=[[x*y for x in r for y in t] for r in ext for t in ext]
    A=np.array(columns,dtype=float).T
    average=[sum((col[i] for col in columns),F(0))/576 for i in range(16)]
    assert average==[F(1)]+[F(0)]*15
    pauli=[S.eye(2),S.Matrix([[0,1],[1,0]]),S.Matrix([[0,-S.I],[S.I,0]]),S.diag(1,-1)]
    basis=[S.kronecker_product(p,q) for p in pauli for q in pauli]
    U=S.diag(1,1,1,1)
    U[2,2]=U[3,3]=S.Rational(3,5);U[2,3]=-S.Rational(4,5);U[3,2]=S.Rational(4,5)
    assert U.H*U==S.eye(4)
    transfer=[[F(S.simplify(S.trace(P*U*Q*U.H)/4)) for Q in basis] for P in basis]
    noise=[F(1),-F(2,5),F(2,5),-F(2,5)]
    factors=[x*y for x in noise for y in noise]
    transfer=[[factors[i]*x for x in row] for i,row in enumerate(transfer)]
    reserve=F(1,64);kernels=[];maxbits=0
    for j,col in enumerate(columns):
        target=[sum((x*y for x,y in zip(row,col)),F(0)) for row in transfer]
        assert target[0]==1
        remainder=[(x-reserve*e)/(1-reserve) for x,e in zip(target,average)]
        lp=linprog(np.zeros(576),A_eq=A,b_eq=np.array(remainder,float),bounds=(0,None),
                   method='highs',options={'threads':1,'presolve':True})
        assert lp.success,(j,lp.message)
        support=np.flatnonzero(lp.x>1e-10).tolist()
        assert 1<=len(support)<=16
        weights=exact_solve([columns[k] for k in support],remainder)
        assert min(weights)>=0 and sum(weights)==1
        assert all(sum((w*columns[k][i] for w,k in zip(weights,support)),F(0))==remainder[i] for i in range(16))
        assert all(reserve*average[i]+(1-reserve)*sum((w*columns[k][i] for w,k in zip(weights,support)),F(0))==target[i] for i in range(16))
        maxbits=max(maxbits,max(max(abs(w.numerator).bit_length(),w.denominator.bit_length()) for w in weights))
        kernels.append({'input_pair':[j//24,j%24],'output_pair_indices':support,
                        'remainder_probabilities':[str(w) for w in weights]})
        if (j+1)%144==0:print(json.dumps({'exact_columns':j+1,'seconds':time.monotonic()-start}),flush=True)
    out={'status':'EXACT24_STATE_UNIVERSAL_FRAME_GATE_INSTANCE_ACQUIRED',
      'local_Bloch_vertices':[[str(x) for x in r] for r in frames],
      'channel_c':'7/4','Phi_Bloch_factors':['-2/5','2/5','-2/5'],
      'gate_rows':[[str(x) for x in row] for row in U.tolist()],
      'gate':'Controlled real rotation with entries3/5,4/5; non-Clifford',
      'reserved_uniform_product_probability':str(reserve),
      'reserve_sampler':'With probability1/64 choose both output indices independently uniform0..23; otherwise use the sparse remainder column.',
      'kernels':kernels,'exact_columns':len(kernels),'Pauli_intertwining_equations':16*len(kernels),
      'maximum_sparse_remainder_support':max(len(k['output_pair_indices']) for k in kernels),
      'maximum_probability_integer_bits':maxbits,'seconds':time.monotonic()-start,
      'scope':'Exact rational kernels for this gate and fresh unobserved local noise. General fixed-frame inclusion is a separate proved interface; no noisy-circuit tractability novelty, calibration or hardware advantage.'}
    (ROOT/'EXACT24_KERNEL.json').write_text(json.dumps(out,indent=2)+'\n')
    summary={k:v for k,v in out.items() if k not in ('kernels','local_Bloch_vertices','gate_rows')}
    summary['kernel_sha256']=hashlib.sha256((ROOT/'EXACT24_KERNEL.json').read_bytes()).hexdigest()
    (ROOT/'KERNEL_RESULT.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
