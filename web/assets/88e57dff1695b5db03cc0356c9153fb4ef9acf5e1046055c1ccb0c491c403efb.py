"""Independent exact audit of the frozen rational separability certificate.

The target is built with direct L tensor L matrix-unit images, not the
originator's Kraus constructor. Positivity is checked with rational LDL,
not the originator's Bareiss leading determinants.
"""
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path
import numpy as np
from independent_maps import build_exact, choi

HERE = Path(__file__).parent
CERT = HERE.parent/'ppt_cube_chain_sol'/'cube_separable_certificate.json'
EXPECTED='256745ff4887eadb653a8fdb416ccb15e91051756065396eb58d11761173d961'

def checked_ints(a):
    if isinstance(a,list):
        for b in a: checked_ints(b)
    else:
        assert type(a) is int, ('not a Python integer',type(a))

def determinant_fraction(a):
    """Ordinary rational Gaussian elimination, with row pivoting."""
    a=[[Fraction(x) for x in r] for r in a]
    sign=1;result=Fraction(1)
    for k in range(len(a)):
        p=next((i for i in range(k,len(a)) if a[i][k]),None)
        if p is None:return Fraction(0)
        if p!=k:a[k],a[p]=a[p],a[k];sign=-sign
        pivot=a[k][k];result*=pivot
        for i in range(k+1,len(a)):
            scale=a[i][k]/pivot
            for j in range(k+1,len(a)):a[i][j]-=scale*a[k][j]
            a[i][k]=Fraction(0)
    return sign*result

def positive_by_ldl(a):
    """Exact real symmetric SPD iff every unpivoted LDL pivot is positive."""
    n=len(a)
    assert all(a[i][j]==a[j][i] for i in range(n) for j in range(n))
    l=[[Fraction(int(i==j)) for j in range(n)] for i in range(n)]
    d=[]
    for i in range(n):
        pivot=Fraction(a[i][i])-sum(l[i][k]**2*d[k] for k in range(i))
        assert pivot>0, ('nonpositive LDL pivot',i)
        d.append(pivot)
        for j in range(i+1,n):
            l[j][i]=(Fraction(a[j][i])-sum(l[j][k]*l[i][k]*d[k] for k in range(i)))/pivot
    # Reconstruct once to audit the recurrence itself, exactly.
    assert all(sum(l[i][k]*d[k]*l[j][k] for k in range(n))==a[i][j]
               for i in range(n) for j in range(n))
    return d

def run():
    start=time.monotonic()
    raw=CERT.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    assert digest==EXPECTED
    z=json.loads(raw)
    assert z['schema']=='family272_original_cube_separable_v1'
    assert z['boundary_dim']==[10,6]
    for name in ('x_numerator','y_numerator','filter_denominator','input_numerators',
                 'input_denominator','output_numerators','output_denominator','rational_target_trace'):
        checked_ints(z[name])
    xn,yn=z['x_numerator'],z['y_numerator']
    vs,bs=z['input_numerators'],z['output_numerators']
    qx,qv,den=z['filter_denominator'],z['input_denominator'],z['output_denominator']
    assert qx>0 and qv>0 and den>0
    assert len(xn)==10 and all(len(r)==10 for r in xn)
    assert len(yn)==6 and all(len(r)==6 for r in yn)
    assert len(vs)==len(bs)==400
    assert all(len(v)==10 for v in vs)
    dx=determinant_fraction(xn);dy=determinant_fraction(yn)
    assert dx!=0 and dy!=0
    assert vs[:10]==[[qv*int(i==j) for j in range(10)] for i in range(10)]
    for b in bs:
        assert len(b)==6 and all(len(r)==6 for r in b)
        positive_by_ldl(b)
        shifted=[[100000*b[i][j]-den*int(i==j) for j in range(6)] for i in range(6)]
        positive_by_ldl(shifted)
    A0,K,F4,Q4=build_exact()
    J=choi(F4,10,6)
    assert np.array_equal(J,J.T)
    tr=sum(J[i,i] for i in range(60))
    assert tr==z['rational_target_trace'] and tr>0
    # The certificate represents H=(X tensor Y) J(F4)/tr (X tensor Y)^T.
    # X=xn/qx, Y=yn/qx. Sum of atoms is sum(vv^T tensor b), with
    # v=vn/qv and b=bn/den. Clear all positive denominators exactly.
    local=np.kron(np.array(xn,dtype=object),np.array(yn,dtype=object))
    target=local@J@local.T
    reconstructed=np.zeros((60,60),dtype=object)
    for v,b in zip(vs,bs):
        va=np.array(v,dtype=object)
        reconstructed+=np.kron(np.outer(va,va),np.array(b,dtype=object))
    delta=reconstructed*(tr*qx**4)-target*(qv*qv*den)
    assert all(x==0 for x in delta.ravel())
    report={
        'status':'INDEPENDENT_EXACT_CROSS_AUDIT_PASS',
        'certificate_sha256':digest,
        'source_commit':'fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb',
        'target':'F4=32 ABA composed with Ad_D, reconstructed independently',
        'target_convention':'Choi ordering (input,output), C-order matrix-unit superoperators',
        'integer_schema':True,
        'all_3600_identity_entries_exact':True,
        'product_terms':400,
        'positive_output_factors':'400 rational LDL decompositions checked and reconstructed',
        'strict_output_margin':'all B_r - I6/100000 strictly positive by rational LDL',
        'coordinate_input_atoms':'first ten exactly e_i',
        'filter_invertibility':'independent rational Gaussian determinants nonzero',
        'rational_target_trace':int(tr),
        'source_c1_c2':'1/1485980',
        'claim':'J(ABA) separable, hence BAB EB, hence pinned Theta^3 EB',
        'square_nonEB':'Imported source lower bound; not checked by this audit',
        'scope':'Finite exact candidate certificate plus hand-derived branch theorem; no external or formal certification',
        'elapsed_seconds':time.monotonic()-start,
    }
    (HERE/'cross_audit_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':run()
