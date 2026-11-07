"""Exact finite source-sector separation; not a proof of the whole sector."""
from itertools import combinations, product
from pathlib import Path
import json
import sympy as sp

DIMS=(3,3,3)

def flat(t):return 9*t[0]+3*t[1]+t[2]

def ket(*labels):
    z=sp.zeros(27,1)
    for label in labels:z[flat(label)]=1
    return z

def ptrace(X,remove):
    keep=[i for i in range(3) if i not in remove]
    n=3**len(keep);Y=sp.zeros(n)
    allidx=list(product(range(3),repeat=3))
    def kflat(a):
        z=0
        for i in keep:z=3*z+a[i]
        return z
    for a,b in product(allidx,repeat=2):
        if all(a[i]==b[i] for i in remove):Y[kflat(a),kflat(b)]+=X[flat(a),flat(b)]
    return Y

def main():
    labels={'u':[(0,0,0),(0,1,1)],'x':[(1,2,0),(2,0,2)],
            'v':[(1,0,0),(1,1,1)],'y':[(0,2,2),(2,0,0)]}
    u,x,v,y=[ket(*labels[n]) for n in ('u','x','v','y')]
    K=u*v.H+x*y.H
    q=sp.Rational(0)
    components={}
    for j in range(4):
        for rem in combinations(range(3),j):
            z=ptrace(K,rem);n=sp.trace(z.H*z)
            components[str(rem)]=str(n);q+=(-sp.Rational(1,2))**j*n
    supports={}
    for name,R in [('range',u*u.H+x*x.H),('adjoint_range',v*v.H+y*y.H)]:
        supports[name]=[ptrace(R,[j for j in range(3) if j!=i]).rank() for i in range(3)]
    out={'status':'EXACT_SOURCE_SECTOR_SEPARATION','vectors_unnormalized':labels,
         'K':'|u><v|+|x><y|','rank_K':K.rank(),'rank_combined_support':sp.Matrix.hstack(u,x,v,y).rank(),
         'K_squared_zero':K*K==sp.zeros(27),'normal':K*K.H==K.H*K,
         'q3_K':str(q),'partial_trace_norm_squares':components,
         'local_support_ranks':supports,
         'local_overlap_Tr_PQ':[3,3,3],
         'single_partial_traces_nonzero':[ptrace(K,[i])!=sp.zeros(9) for i in range(3)],
         'reference_u_local_Schmidt_ranks':[ptrace(u*u.H,[j for j in range(3) if j!=i]).rank() for i in range(3)],
         'range_no_product_ray_proof':'Projection of alpha*u+beta*x onto first-site |0> is alpha*(|00>+|11>). A fully product vector forces alpha=0, but x has first-site Schmidt rank2. Thus no nonzero fully product ray exists.',
         'adjoint_range_no_product_ray_proof':'Projection of alpha*v+beta*y onto first-site |1> is alpha*(|00>+|11>). A fully product vector forces alpha=0, but y has first-site Schmidt rank2.',
         'outside_crossed_locally_orthogonal_code_proof':'Every nonzero vector in a locally orthogonal product-code span has equal local Schmidt ranks at all three sites: each equals the number of nonzero code coefficients. The range contains u, whose ranks are (1,2,2), so it cannot lie in any such code span.',
         'source_pin':'https://arxiv.org/html/2608.02647v1, Theorems7.2,7.3 and C.1,C.2'}
    assert out['rank_K']==2 and not out['normal'] and out['rank_combined_support']==4
    assert all(s==[3,3,3] for s in supports.values())
    assert all(out['single_partial_traces_nonzero'])
    assert out['reference_u_local_Schmidt_ranks']==[1,2,2]
    Path(__file__).with_name('scope_check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
