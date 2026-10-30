"""Remove affine/determinant gauges and the four translation cubic modes.

This exact coordinate operation preserves ROC and QC. It does not decide
either property for the remaining eight cubic plus nine quadratic modes.
"""
from pathlib import Path
from fractions import Fraction as R
import json,argparse
import check_shape as m
HERE=Path(__file__).resolve().parent
def normalize(cubic,quadratic):
    cert=json.loads((HERE/'certificate.json').read_text());F,_,_=m.acquired();cp=cert['cubic_powers'];qp=cert['quadratic_powers']
    c=list(map(R,cubic));q=list(map(R,quadratic));assert len(c)==20 and len(q)==10
    coords=[m.dot(list(map(R,row)),c) for row in cert['normal_form_operator']];basis=[list(map(R,row)) for row in cert['normal_form_basis']]
    assert [sum((coords[j]*basis[j][i] for j in range(12)),R(0)) for i in range(20)]==c,'Cubic is not in the acquired admissible space'
    V=coords[:4];C={tuple(pw):co for pw,co in zip(cp,c) if co};Q={tuple(pw):co for pw,co in zip(qp,q) if co}
    Cn=[sum((coords[j]*basis[j][i] for j in range(4,12)),R(0)) for i in range(20)]
    Qn=m.core.add(Q,*(m.core.scale(m.core.diff(C,i),-V[i]) for i in range(4)),
      *(m.core.scale(m.core.diff(m.core.diff(F,i),j),V[i]*V[j]/2) for i in range(4) for j in range(4)))
    det={(1,0,0,1):R(1),(0,1,1,0):R(-1)};lam=(Qn.get((1,0,0,1),0)-Qn.get((0,1,1,0),0))/2
    Qn=m.core.add(Qn,m.core.scale(det,-lam))
    return {'translate_argument_by':list(map(str,(-x for x in V))),'determinant_subtracted':str(lam),
      'cubic_quotient_coordinates':list(map(str,coords[4:])),'normalized_cubic_coefficients':list(map(str,Cn)),
      'normalized_quadratic_coefficients':[str(Qn.get(tuple(pw),0)) for pw in qp],
      'cubic_powers':cp,'quadratic_powers':qp,
      'scope':'Exact normal form modulo affine terms, determinant and argument translation. Global ROC/QC classification is not inferred.'}
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--cubic',type=Path);parser.add_argument('--quadratic',type=Path);parser.add_argument('--nu',default='1859');args=parser.parse_args()
    cert=json.loads((HERE/'certificate.json').read_text());c=json.loads(args.cubic.read_text()) if args.cubic else cert['example_cubic_coefficients']
    q=json.loads(args.quadratic.read_text()) if args.quadratic else [str(R(args.nu)) if 2 in pw else '0' for pw in cert['quadratic_powers']]
    print(json.dumps(normalize(c,q),indent=2))
if __name__=='__main__':main()
