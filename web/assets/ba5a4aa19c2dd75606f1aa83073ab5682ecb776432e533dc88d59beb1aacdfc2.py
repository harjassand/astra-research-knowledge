"""Exact operator-range facts used in the Phase D literal-retention no-go."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent))
from verify_cube_stdlib import BLOCKS,K,tr,transpose,matmul

def source_superoperator():
    syms=[(i,j) for i in range(4) for j in range(i,4)]
    weds=[(i,j) for i in range(4) for j in range(i+1,4)]
    qs=[[[BLOCKS[j][r][i] for j in range(4)] for i in range(4)] for r in range(6)]
    ks=[]
    for q in qs:
      for r in qs:
        matrix=[]
        for a,b in weds:
            row=[]
            for i,j in syms:
                val=q[a][i]*r[b][j]-q[b][i]*r[a][j]
                if i!=j:val+=q[a][j]*r[b][i]-q[b][j]*r[a][i]
                row.append(val)
            matrix.append(row)
        ks.append(matrix)
    s=[[sum(k[a][i]*k[b][j] for k in ks) for i in range(10) for j in range(10)]
       for a in range(6) for b in range(6)]
    return s

def rank_mod(a,p):
    a=[[x%p for x in row] for row in a];rank=0;pivots=[]
    for col in range(len(a[0])):
        pivot=next((r for r in range(rank,len(a)) if a[r][col]),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank];z=a[rank][col];pivots.append(z)
        a[rank]=[x*pow(z,-1,p)%p for x in a[rank]]
        for r in range(rank+1,len(a)):
            z=a[r][col]
            if z:a[r]=[(x-z*y)%p for x,y in zip(a[r],a[rank])]
        rank+=1
        if rank==len(a):break
    return rank,pivots

def verify():
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    s=source_superoperator()
    assert K==transpose(K) and tr(K)==0
    assert matmul(K,K)==[[int(i==j) for j in range(6)] for i in range(6)]
    for col in range(100):
        assert sum(K[b][a]*s[a*6+b][col] for a in range(6) for b in range(6))==0
    for a in range(6):
      for b in range(6):
        for i in range(10):
          for j in range(10):
            assert s[a*6+b][i*10+j]==s[b*6+a][i*10+j]
            assert s[a*6+b][i*10+j]==s[a*6+b][j*10+i]
    output_pairs=[(a,b) for a in range(6) for b in range(a,6)]
    input_pairs=[(i,j) for i in range(10) for j in range(i,10)]
    restricted=[[s[a*6+b][i*10+j]*(1 if i==j else 2) for i,j in input_pairs]
                for a,b in output_pairs]
    rank,pivots=rank_mod(restricted,101);assert rank==20
    out={'status':'EXACTLY_VERIFIED','arithmetic':'Python stdlib integers',
         'integer_A0_symmetric_matrix_shape':[21,55],
         'prime':101,'rank_mod_prime':rank,'pivots':pivots,
         'exact_upper_bound':'all columns have Tr(K image)=0',
         'conclusion':'range(S)={Y=Y^T:Tr(KY)=0}; B symmetric kernel is span(K)',
         'K_signature':[3,3]}
    print(json.dumps(out,indent=2));return out

if __name__=='__main__':verify()
