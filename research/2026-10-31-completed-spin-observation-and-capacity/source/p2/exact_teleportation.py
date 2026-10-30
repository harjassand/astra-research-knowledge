"""Exact rational certificate for singlet-only forced teleportation.

No floating-point arithmetic or unprovided Pauli corrections are used.
The singlet embeddings are unnormalised by sqrt(2), which cancels in
all branch probabilities. Projectors and amplitudes are rational.
"""
from fractions import Fraction as F


def zeros(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def identity(n):
    a=zeros(n,n)
    for i in range(n): a[i][i]=F(1)
    return a


def multiply(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def subtract(a,b):
    return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]


def transpose(a): return [list(x) for x in zip(*a)]


def scale(a,c): return [[c*x for x in row] for row in a]


def pair_projector(pair):
    """Three-spin singlet projector, order A,B,C, most significant first."""
    a=zeros(8,8)
    rest=next(i for i in range(3) if i not in pair)
    for bit in [0,1]:
        indices=[]
        for pairbits in [(0,1),(1,0)]:
            bits=[0]*3; bits[rest]=bit
            for k,v in zip(pair,pairbits): bits[k]=v
            indices.append(4*bits[0]+2*bits[1]+bits[2])
        for i,si in zip(indices,[1,-1]):
            for j,sj in zip(indices,[1,-1]): a[i][j]=F(si*sj,2)
    return a


def embeddings():
    ein=zeros(8,2); eout=zeros(8,2)
    for bit in [0,1]:
        ein[4*bit+1][bit]=F(1); ein[4*bit+2][bit]=F(-1)
        eout[2+bit][bit]=F(1); eout[4+bit][bit]=F(-1)
    return ein,eout


def probability(k):
    gram=multiply(transpose(k),k)
    assert gram[0][1]==gram[1][0]==0 and gram[0][0]==gram[1][1]
    return gram[0][0]/2


def certify(max_attempts=8,reverse=False):
    ps=pair_projector((0,1)); qs=pair_projector((1,2))
    ein,eout=embeddings()
    if reverse: ps,qs=qs,ps; ein,eout=eout,ein
    pt=subtract(identity(8),ps); qt=subtract(identity(8),qs)
    pivot=next((i,j) for i in range(8) for j in range(2) if eout[i][j])
    frontier=[('',ein)]; rows=[]; success_total=F(0); branch_count=0
    for attempt in range(1,max_attempts+1):
        remaining=[]; pstep=F(0)
        for record,k in frontier:
            success=multiply(ps,k)
            i,j=pivot; coefficient=success[i][j]/eout[i][j]
            assert success==scale(eout,coefficient), (record,success)
            p=probability(success)
            assert p==coefficient**2
            pstep+=p; branch_count+=1
            failed=multiply(pt,k)
            remaining.append((record+'t',failed))
        failure=sum((probability(k) for _,k in remaining),F(0))
        expected=F(3,4)*F(5,8)**(attempt-1)
        assert failure==expected
        success_total+=pstep
        assert success_total+failure==1
        rows.append({'primary_pair_attempts':attempt,'success_this_attempt':str(pstep),
                     'failure_tail':str(failure),
                     'successful_histories_through_here':branch_count})
        frontier=[]
        for record,k in remaining:
            for outcome,q in [('s',qs),('t',qt)]:
                frontier.append((record+outcome,multiply(q,k)))
    # Each remaining AB-triplet branch is a fixed intertwiner. The next
    # BC measurement gives probabilities 3/4,1/4, and the next AB singlet
    # probabilities are respectively 1/4,3/4.
    failed=multiply(pt,ein); base=probability(failed)
    conditional=[]
    for q in [qs,qt]:
        intermediate=multiply(q,failed); weight=probability(intermediate)
        pnext=probability(multiply(ps,intermediate))
        conditional.append((str(weight/base),str(pnext/weight)))
    assert conditional==[('3/4','1/4'),('1/4','3/4')]
    mean_ab=1+F(3,4)/(1-F(5,8)); mean_bc=mean_ab-1
    assert mean_ab==3 and mean_bc==2
    identity_label=('c_h * identity_C_to_A tensor singlet_BC' if reverse
                    else 'c_h * singlet_AB tensor identity_A_to_C')
    return {'arithmetic':'exact fractions','success_branch_identity':identity_label,
            'primary_pair':'BC' if reverse else 'AB','reset_pair':'AB' if reverse else 'BC',
            'branches_checked':branch_count,'tail_rows':rows,
            'conditional_probabilities_reset_then_primary':conditional,
            'mean_primary_pair_measurements':str(mean_ab),'mean_reset_pair_measurements':str(mean_bc),
            'mean_total_ST_measurements':str(mean_ab+mean_bc)}


if __name__=='__main__':
    import json
    print(json.dumps(certify(),indent=2))
