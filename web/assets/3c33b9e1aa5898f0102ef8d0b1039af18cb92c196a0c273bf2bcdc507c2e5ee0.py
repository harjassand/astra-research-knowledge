"""Independent exact cross-audit of the single Hodge-cancelled cube.

Keeps the Phase C audits and Phase D blind baseline unchanged. Source maps
are reconstructed with independent tensor matrix-unit images; all positivity
checks use rational LDL rather than the candidate's Bareiss determinants.
"""
import hashlib
import json
import sys
import time
from pathlib import Path
import numpy as np
from independent_maps import build_exact,choi
from cross_audit import checked_ints,determinant_fraction,positive_by_ldl

HERE=Path(__file__).parent
SOURCE=HERE.parent/'ppt_cube_chain_sol'
CERT=SOURCE/'phase_d_alignment'/'gram_cube_separable_certificate.json'
EXPECTED='b0696ab44ecccafa02e80ee9376db1f61a5ab5bbb6a6437fffc1873d127bce2b'

def run():
    if not __debug__ or sys.flags.optimize:raise RuntimeError('Assertions must be enabled')
    start=time.monotonic();raw=CERT.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==EXPECTED
    z=json.loads(raw)
    assert z['schema']=='family272_hodge_cancelled_cube_separable_v1'
    assert z['boundary_dim']==[10,6]
    for name in ('amendment_U','x_numerator','y_numerator','filter_denominator',
                 'input_numerators','input_denominator','output_numerators',
                 'output_denominator','rational_target_trace'):
        checked_ints(z[name])
    A0,K,F4,Q4=build_exact()
    Fc=Q4@A0
    J=choi(Fc,10,6)
    assert np.array_equal(J,J.T)
    t=sum(J[i,i] for i in range(60))
    assert t==29063574533380571168==z['rational_target_trace']
    # Compare to the matrix frozen before originator exposure.
    frozen=np.array(json.loads((HERE/'phase_d_cancelled_integer_superoperator.json').read_text()),dtype=object)
    assert np.array_equal(Fc,frozen)
    u=np.eye(21,dtype=object)
    u[10:16,10:16]=K
    assert z['amendment_U']==u.tolist()
    assert np.array_equal(u.T@u,np.eye(21,dtype=object))
    assert np.array_equal(K@K,np.eye(6,dtype=object))
    xn,yn=z['x_numerator'],z['y_numerator']
    vs,bs=z['input_numerators'],z['output_numerators']
    qx,qv,den=z['filter_denominator'],z['input_denominator'],z['output_denominator']
    assert qx>0 and qv>0 and den>0
    assert len(xn)==10 and all(len(r)==10 for r in xn)
    assert len(yn)==6 and all(len(r)==6 for r in yn)
    assert len(vs)==len(bs)==400 and all(len(v)==10 for v in vs)
    assert determinant_fraction(xn)!=0 and determinant_fraction(yn)!=0
    assert vs[:10]==[[qv*int(i==j) for j in range(10)] for i in range(10)]
    for b in bs:
        assert len(b)==6 and all(len(r)==6 for r in b)
        positive_by_ldl(b)
        shifted=[[100000*b[i][j]-den*int(i==j) for j in range(6)] for i in range(6)]
        positive_by_ldl(shifted)
    local=np.kron(np.array(xn,dtype=object),np.array(yn,dtype=object))
    target=local@J@local.T
    reconstruction=np.zeros((60,60),dtype=object)
    for v,b in zip(vs,bs):
        va=np.array(v,dtype=object)
        reconstruction+=np.kron(np.outer(va,va),np.array(b,dtype=object))
    assert all(x==0 for x in (reconstruction*(t*qx**4)-target*(qv*qv*den)).ravel())
    hashes={str(p.relative_to(SOURCE)):hashlib.sha256(p.read_bytes()).hexdigest()
      for p in [SOURCE/'PHASE_D_ALIGNMENT.txt',CERT,SOURCE/'phase_d_alignment'/'verify_gram_stdlib.py',
                SOURCE/'phase_d_alignment'/'symmetric_range_stdlib.py',SOURCE/'verify_cube_stdlib.py']}
    report={
      'status':'INDEPENDENT_EXACT_PHASE_D_CROSS_AUDIT_PASS',
      'no_go':'For CP R:M10->M6 and real lambda>0, BRBS != lambda BS',
      'no_go_status':'independent blind pure-state proof and post-exposure Choi-inequality proof reviewed',
      'range_S':'complex dimension20, W={Y=Y^T:Tr(KY)=0}',
      'rank_baseline':'independent 20 by 20 determinant27 mod41 plus exact upper bound20',
      'cancelled_map':'Fc=32 SS^dagger S composed with Ad_D',
      'rational_target_trace':int(t),
      'frozen_blind_target_matches':True,
      'all_3600_identity_entries_exact':True,
      'positive_terms':400,
      'output_margin':'all 400 factors B-I6/100000 SPD by exact rational LDL',
      'filters':'independent rational Gaussian determinants nonzero',
      'amendment_U':'I10 direct-sum (K direct-sum I4) direct-sum 1, independently exactly orthogonal',
      'channel_claim':'(Theta composed with Ad_U)^3 is EB for this fixed signed permutation',
      'amended_square':'unresolved; original square non-EB proof is not imported',
      'robustness':'same full complex Hermitian max-entry radius 1/20900000 follows from coordinate reserve',
      'scope':'No claim for all unitary amendments or unrestricted PPT cubes; no external/formal certification',
      'frozen_input_sha256':hashes,
      'elapsed_seconds':time.monotonic()-start,
    }
    (HERE/'phase_d_cross_audit_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':run()
