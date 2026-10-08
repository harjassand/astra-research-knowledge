"""Blind signed spin1 identities, exact generic weights; no originator imports."""
from itertools import product
from pathlib import Path
import json
from sympy import Matrix, symbols, sqrt, eye, I, kronecker_product as kron, simplify

w = list(symbols('w1 w2 w3', nonnegative=True))
q = list(symbols('q1 q2 q3', real=True))
J = [Matrix([[0,0,0],[0,0,-I],[0,I,0]]),
     Matrix([[0,0,I],[0,0,0],[-I,0,0]]),
     Matrix([[0,-I,0],[I,0,0],[0,0,0]])]
I3 = eye(3)
Q = Matrix.diag(*q)
potential = (3*kron(Q,I3,I3)+kron(I3,Q,I3)+kron(I3,I3,Q))/5
couplings = [kron(J[i],J[i],I3)+kron(J[i],I3,J[i]) for i in range(3)]
states = list(product(range(3), repeat=3))
indices = {s:i for i,s in enumerate(states)}
def vec(s):
    result = Matrix.zeros(27,1)
    result[indices[s]] = 1
    return result
embeddings = []
names = []
for i in range(3):
    j,k = [a for a in range(3) if a != i]
    cols = [vec((i,i,i))]
    for a in [j,k]:
        cols += [vec((i,a,a)), (vec((a,i,a))+vec((a,a,i)))/sqrt(2)]
    embeddings.append(Matrix.hstack(*cols)); names.append(f'odd{i+1}_sym')
    embeddings.append(Matrix.hstack(*[(vec((a,i,a))-vec((a,a,i)))/sqrt(2) for a in [j,k]]))
    names.append(f'odd{i+1}_anti')
for s in [1,-1]:
    embeddings.append(Matrix.hstack(*[(vec((i,(i+1)%3,(i+2)%3))+s*vec((i,(i+2)%3,(i+1)%3)))/sqrt(2) for i in range(3)]))
    names.append('all_sym' if s == 1 else 'all_anti')
S = Matrix.hstack(*embeddings)
assert simplify(S.T*S) == eye(27)

def expected_blocks(e):
    blocks = []
    ew = [e[i]*w[i] for i in range(3)]
    for i in range(3):
        j,k = [a for a in range(3) if a != i]
        qi,qj,qk=q[i],q[j],q[k]; wi,wj,wk=ew[i],ew[j],ew[k]
        blocks += [Matrix([[qi,0,-sqrt(2)*wk,0,-sqrt(2)*wj],
                           [0,(3*qi+2*qj)/5,sqrt(2)*wk,0,0],
                           [-sqrt(2)*wk,sqrt(2)*wk,(qi+4*qj)/5,0,-wi],
                           [0,0,0,(3*qi+2*qk)/5,sqrt(2)*wj],
                           [-sqrt(2)*wj,0,-wi,sqrt(2)*wj,(qi+4*qk)/5]]),
                   Matrix([[(qi+4*qj)/5,-wi],[-wi,(qi+4*qk)/5]])]
    ds=[(3*q[i]+q[(i+1)%3]+q[(i+2)%3])/5 for i in range(3)]
    for s in [1,-1]:
        B=Matrix.diag(*ds)
        for i in range(3):
            for j in range(i+1,3):
                B[i,j]=B[j,i]=s*ew[3-i-j]
        blocks.append(B)
    return blocks

positive = expected_blocks([1,1,1])
negative_bases=[]
for k,B in enumerate(positive):
    if B.rows==5:
        switch=Matrix.diag(1,-1,1,-1,1)
        M=switch*B*switch
    elif k==6:
        M=positive[7]
    else:
        M=B
    for i in range(M.rows):
        for j in range(i):
            assert M[i,j].is_nonpositive is True
    negative_bases.append(M)

records=[]
for e in product([1,-1],repeat=3):
    D=potential+sum((e[i]*w[i]*couplings[i] for i in range(3)), Matrix.zeros(27))
    blocks=expected_blocks(e)
    target=Matrix.diag(*blocks)
    assert simplify(S.T*D*S-target)==Matrix.zeros(27)
    for name,B,M in zip(names,blocks,negative_bases):
        assert B.diagonal()==M.diagonal()
        for i in range(B.rows):
            for j in range(i):
                assert simplify(B[i,j]**2-M[i,j]**2)==0
    records.append({'epsilon':list(e),'all_generic_blocks_exact':True,'absolute_entry_lower_bounds':True})
    print('PASS generic signed-star identities and negative-off-diagonal comparison:',e,flush=True)

# Legal nonsymmetric marginal: measure Y, prepare X on both outputs.
sx=Matrix([[0,1],[1,0]]); sy=Matrix([[0,-I],[I,0]]); sz=Matrix([[1,0],[0,-1]])
paulis=[sx,sy,sz]; I2=eye(2)
R=Matrix.zeros(8)
for e in [1,-1]:
    pin=(I2+e*sy)/2; pout=(I2+e*sx)/2
    R += kron(pin.T,pout,pout)/2
assert R.trace()==1
def ptrace_one(r,axis):
    states2=list(product(range(2),repeat=3)); idx2={s:i for i,s in enumerate(states2)}
    result=Matrix.zeros(2)
    others=[i for i in range(3) if i!=axis]
    for a in range(2):
        for b in range(2):
            for s in product(range(2),repeat=2):
                left=[0,0,0];right=[0,0,0];left[axis]=a;right[axis]=b
                for i,c in zip(others,s): left[i]=right[i]=c
                result[a,b]+=r[idx2[tuple(left)],idx2[tuple(right)]]
    return simplify(result)
for axis in range(3): assert ptrace_one(R,axis)==I2/2
T=Matrix(3,3,lambda i,j:simplify((R*kron(paulis[j].T,paulis[i],I2)).trace()))
assert T==Matrix([[0,1,0],[0,0,0],[0,0,0]])
A=Matrix.diag(0,1,0); B=Matrix.diag(1,0,0)
U=Matrix([[0,1,0],[1,0,0],[0,0,1]])
assert U*A==T and U*A*U.T==B
assert A+B-T-T.T==(eye(3)-U)*A*(eye(3)-U.T)
v=Matrix([1,sqrt(1)/2,0])
assert (v.T*(A-(T+T.T)/2)*v)[0]==-sqrt(1)/4
print('PASS exact legal qubit nonnormal right-modulus failed shortcut; both-modulus polar identity.',flush=True)
Path(__file__).with_name('SIGNED_BLOCK_IDENTITIES.json').write_text(json.dumps({
    'schema_version':1,'universal_proof':'generic algebra plus absolute-entry quadratic bound and frozen all-weight PSD proof',
    'sign_records':records,'legal_qubit_nonnormal_counterexample':'T=e_x e_y^T; x=e_x+e_y/2 gives -1/4',
},indent=2)+'\n')
