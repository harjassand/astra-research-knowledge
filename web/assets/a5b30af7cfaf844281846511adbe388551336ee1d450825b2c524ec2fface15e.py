#!/usr/bin/env python3
"""Standalone exact verifier for the original family272 cube certificate.

Only the Python standard library is used. All reconstructed arithmetic is in
integers. The input JSON is candidate data, not trusted proof output.
Run: python3 verify_cube_stdlib.py [cube_separable_certificate.json]
"""
import hashlib,json,sys,time
from pathlib import Path

BLOCKS=[
 [[6,0,0,0],[0,6,0,0],[0,0,6,0],[0,0,0,6],[0,0,0,0],[0,0,0,0]],
 [[-12,0,0,0],[0,-6,0,0],[0,0,6,0],[0,0,0,12],[-6,0,6,6],[-6,-6,6,0]],
 [[0,6,-2,0],[6,6,0,2],[-2,0,10,0],[0,2,0,24],[0,0,0,6],[0,-6,6,-6]],
 [[0,0,-4,-3],[0,-2,-3,-4],[-4,-3,11,6],[-3,-4,6,25],[6,6,0,0],[0,-6,6,6]]
]
K=[[0,0,0,0,0,1],[0,0,0,0,-1,0],[0,0,0,1,0,0],
   [0,0,1,0,0,0],[0,-1,0,0,0,0],[1,0,0,0,0,0]]
SYMS=[(i,j) for i in range(4) for j in range(i,4)]
WEDS=[(i,j) for i in range(4) for j in range(i+1,4)]

def tr(a):return sum(a[i][i] for i in range(len(a)))
def transpose(a):return list(map(list,zip(*a)))
def matmul(a,b):
    cols=list(zip(*b))
    return [[sum(x*y for x,y in zip(row,col)) for col in cols] for row in a]
def kron(a,b):
    return [[a[i][j]*b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]
def det(a):
    a=[row[:] for row in a];n=len(a);previous=1;sign=1
    for k in range(n-1):
        if not a[k][k]:
            pivot=next((i for i in range(k+1,n) if a[i][k]),None)
            if pivot is None:return 0
            a[k],a[pivot]=a[pivot],a[k];sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                z=a[i][j]*pivot-a[i][k]*a[k][j]
                assert z%previous==0
                a[i][j]=z//previous
            a[i][k]=0
        previous=pivot
    return sign*a[-1][-1]
def positive_definite(a):
    assert a==transpose(a)
    for k in range(1,len(a)+1):assert det([row[:k] for row in a[:k]])>0

def validate_json_types(value):
    """This schema has strings and integers only; reject floats and bools."""
    if type(value) is dict:
        assert all(type(k) is str for k in value)
        for v in value.values():validate_json_types(v)
    elif type(value) is list:
        for v in value:validate_json_types(v)
    else:
        assert type(value) in (int,str), 'Certificate contains a non-integer numeric value.'

def rational_model():
    assert K==transpose(K)
    assert matmul(K,K)==[[int(i==j) for j in range(6)] for i in range(6)]
    # Q_r[output][input]=BLOCKS[input][r][output].
    qs=[[[BLOCKS[j][r][i] for j in range(4)] for i in range(4)] for r in range(6)]
    ks=[]
    for q in qs:
      for r in qs:
        matrix=[]
        for a,b in WEDS:
            row=[]
            for i,j in SYMS:
                val=q[a][i]*r[b][j]-q[b][i]*r[a][j]
                if i!=j:val+=q[a][j]*r[b][i]-q[b][j]*r[a][i]
                row.append(val)
            matrix.append(row)
        ks.append(matrix)
    # A0 is CP by its explicitly constructed Kraus matrices.
    s=[[sum(k[a][i]*k[b][j] for k in ks) for i in range(10) for j in range(10)]
       for a in range(6) for b in range(6)]
    # Both transpose symmetries are checked exactly; A0 and A0* are PPT.
    for a in range(6):
      for b in range(6):
        for i in range(10):
          for j in range(10):
            assert s[a*6+b][i*10+j]==s[b*6+a][i*10+j]
            assert s[a*6+b][i*10+j]==s[a*6+b][j*10+i]
    d=[2 if i==j else 1 for i,j in SYMS]
    sd=[[x*d[i]*d[j] for x,(i,j) in zip(row,[(i,j) for i in range(10) for j in range(10)])]
        for row in s]
    # M = A0 Ad_(2D^-2) A0* Ad_K A0, where D^2=diag(1,2).
    m=matmul(matmul(matmul(sd,transpose(s)),kron(K,K)),s)
    choi=[[m[a*6+b][i*10+j] for j in range(10) for b in range(6)]
          for i in range(10) for a in range(6)]
    assert choi==transpose(choi)
    # Source normalization coefficients coincide and are exactly rational.
    four_trace_effect=sum(k[a][i]**2*(2 if p==q else 1)
      for k in ks for a in range(6) for i,(p,q) in enumerate(SYMS))
    return choi,four_trace_effect

def verify(path):
    if not __debug__:
        raise RuntimeError('Exact verification requires assertions enabled; remove -O/-OO.')
    before=time.monotonic();raw=path.read_bytes();z=json.loads(raw)
    validate_json_types(z)
    assert z['schema']=='family272_original_cube_separable_v1'
    assert z['boundary_dim']==[10,6]
    xi=z['x_numerator'];yi=z['y_numerator'];vi=z['input_numerators'];bi=z['output_numerators']
    qx=z['filter_denominator'];qv=z['input_denominator'];den=z['output_denominator']
    assert len(xi)==10 and all(len(r)==10 for r in xi)
    assert len(yi)==6 and all(len(r)==6 for r in yi)
    assert len(vi)==len(bi)==400 and all(len(v)==10 for v in vi)
    assert qx>0 and qv>0 and den>0
    assert all(type(v) is int for row in xi+yi+vi for v in row)
    assert all(type(v) is int for b in bi for row in b for v in row)
    assert det(xi)!=0 and det(yi)!=0
    for b in bi:
        assert len(b)==6 and all(len(r)==6 for r in b)
        positive_definite(b)
        # Strict exact margin B > I/100000, used in the neighborhood criterion.
        shifted=[[100000*b[i][j]-den*int(i==j) for j in range(6)] for i in range(6)]
        positive_definite(shifted)
    # First ten input factors are precisely the coordinate projectors.
    assert vi[:10]==[[qv*int(i==j) for j in range(10)] for i in range(10)]
    j,four_effect_trace=rational_model();trace=tr(j)
    assert trace==z['rational_target_trace'] and trace>0
    local=kron(xi,yi);target=matmul(matmul(local,j),transpose(local))
    reconstructed=[[0]*60 for _ in range(60)]
    for v,b in zip(vi,bi):
      for i in range(10):
        for j0 in range(10):
            c=v[i]*v[j0]
            for a in range(6):
                for b0 in range(6):reconstructed[i*6+a][j0*6+b0]+=c*b[a][b0]
    lhs_scale=trace*qx**4;rhs_scale=qv*qv*den
    assert all(reconstructed[i][j0]*lhs_scale==target[i][j0]*rhs_scale
               for i in range(60) for j0 in range(60))
    out={'status':'EXACTLY_VERIFIED','arithmetic':'Python stdlib integers only',
      'certificate_sha256':hashlib.sha256(raw).hexdigest(),'certificate_bytes':len(raw),
      'separable_terms':400,'PSD_factors':'all 400 strictly exceed I/100000',
      'equality':'exact integer equality','filters':'exact nonzero determinants',
      'source_PPT':'both transpose invariances verified for the CP Kraus map A0',
      'rational_target_trace':trace,
      'source_trace_effect_numerator_over_4':four_effect_trace,
      'source_channel_coefficient':'4/'+str(4+four_effect_trace),
      'elapsed_seconds':time.monotonic()-before,
      'claim':'J(ABA) is separable; flag-block reduction gives source Theta^3 EB',
      'square_nonEB':'source-dependent; not checked by this verifier'}
    print(json.dumps(out,indent=2))
    return out

if __name__=='__main__':
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('cube_separable_certificate.json')
    verify(path)
