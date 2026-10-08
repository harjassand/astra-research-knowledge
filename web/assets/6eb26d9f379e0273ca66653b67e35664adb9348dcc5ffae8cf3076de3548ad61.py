#!/usr/bin/env python3
"""Exact stdlib verification of the single amended channel's cube.

Uses sibling source helper symmetric_range_stdlib.py and the original frozen
verifier's standard-library matrix helpers; no solver/numpy is imported.
"""
import hashlib,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent))
from verify_cube_stdlib import K,SYMS,kron,matmul,transpose,tr,det,positive_definite,validate_json_types
from symmetric_range_stdlib import source_superoperator

def rational_gram_choi():
    s=source_superoperator();d=[2 if i==j else 1 for i,j in SYMS]
    sd=[[x*d[i]*d[j] for x,(i,j) in zip(row,[(i,j) for i in range(10) for j in range(10)])]
        for row in s]
    m=matmul(matmul(sd,transpose(s)),s)
    return [[m[a*6+b][i*10+j] for j in range(10) for b in range(6)]
            for i in range(10) for a in range(6)]

def verify(path):
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    before=time.monotonic();raw=path.read_bytes();z=json.loads(raw);validate_json_types(z)
    assert z['schema']=='family272_hodge_cancelled_cube_separable_v1'
    assert z['boundary_dim']==[10,6]
    u=[[int(i==j) for j in range(21)] for i in range(21)]
    for i in range(6):
        for j in range(6):u[10+i][10+j]=K[i][j]
    assert z['amendment_U']==u
    assert matmul(transpose(u),u)==[[int(i==j) for j in range(21)] for i in range(21)]
    xi=z['x_numerator'];yi=z['y_numerator'];vi=z['input_numerators'];bi=z['output_numerators']
    qx=z['filter_denominator'];qv=z['input_denominator'];den=z['output_denominator']
    assert len(xi)==10 and all(len(r)==10 for r in xi)
    assert len(yi)==6 and all(len(r)==6 for r in yi)
    assert len(vi)==len(bi)==400 and all(len(v)==10 for v in vi)
    assert qx>0 and qv>0 and den>0 and det(xi)!=0 and det(yi)!=0
    for b in bi:
        assert len(b)==6 and all(len(r)==6 for r in b)
        positive_definite(b)
        positive_definite([[100000*b[i][j]-den*int(i==j) for j in range(6)] for i in range(6)])
    assert vi[:10]==[[qv*int(i==j) for j in range(10)] for i in range(10)]
    j=rational_gram_choi();assert j==transpose(j);trace=tr(j)
    assert trace==z['rational_target_trace'] and trace>0
    local=kron(xi,yi);target=matmul(matmul(local,j),transpose(local))
    reconstructed=[[0]*60 for _ in range(60)]
    for v,b in zip(vi,bi):
      for i in range(10):
        for j0 in range(10):
            c=v[i]*v[j0]
            for a in range(6):
                for b0 in range(6):reconstructed[i*6+a][j0*6+b0]+=c*b[a][b0]
    assert all(reconstructed[i][j0]*(trace*qx**4)==target[i][j0]*(qv*qv*den)
               for i in range(60) for j0 in range(60))
    out={'status':'EXACTLY_VERIFIED','arithmetic':'stdlib integer arithmetic',
      'certificate_sha256':hashlib.sha256(raw).hexdigest(),'certificate_bytes':len(raw),
      'target':'Theta Ad_U with U=I10 direct-sum (K direct-sum I4) direct-sum 1',
      'claim':'amended channel cube is entanglement breaking',
      'terms':400,'output_factors':'all strictly exceed I6/100000',
      'filters':'exact nonzero determinants','equality':'exact integer reconstruction',
      'rational_target_trace':trace,'elapsed_seconds':time.monotonic()-before,
      'square_status':'unresolved for amended channel; original square proof does not transfer'}
    print(json.dumps(out,indent=2));return out

if __name__=='__main__':
    p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('gram_cube_separable_certificate.json')
    verify(p)
