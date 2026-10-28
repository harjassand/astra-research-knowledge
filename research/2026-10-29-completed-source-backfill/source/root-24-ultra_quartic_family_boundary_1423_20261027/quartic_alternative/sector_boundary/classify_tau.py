"""Exact rational-input decision on the proved oriented quartic line."""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,json
from verify_boundary import Q

SUPPORT='66901f304531cbc969ccc7f89e5a7e57091e57cefba21133355b0d2cb54be554'
PAIR='c57502de52215737c319374669a32b8e31983fbd7bc89c0fe6b8315aa0b36aa3'


def classify(tau):
    tau=F(tau);difference=Q(tau-89,12);root=Path(__file__).resolve().parent
    cert=root/'EXACT_BOUNDARY_SUPPORT.json';pair=root/'CRITICAL_PAIR.json'
    assert hashlib.sha256(cert.read_bytes()).hexdigest()==SUPPORT
    assert hashlib.sha256(pair.read_bytes()).hexdigest()==PAIR
    positive=difference==0 or difference.positive()
    out={'input_tau':str(tau),'family':'u^2+v^2+3w^2+tau*q^2+4q*(u-v)',
         'threshold':'89-12sqrt42','ROC':positive,'PC':positive,'QC':positive,
         'boundary_support_sha256':SUPPORT,'critical_pair_sha256':PAIR,
         'decision_arithmetic':'EXACT_RATIONAL_AND_Q_SQRT42',
         'scope':'This fixed oriented one-parameter line only; PRIMARY_PROOF.md supplies the theorem.'}
    if positive:
        record=json.loads(cert.read_bytes());delta=Q(*record['selector_delta'])+2*difference
        out['positive_support']={'alpha':record['selector_alpha'],'delta':delta.pair(),
            'extra_square_weight':difference.pair(),
            'identity':'P_tau=P_boundary+(tau-tau_c)*(det(A+X)-det(A))^2'}
    else:
        out['negative_acoustic_witness']={'source':'CRITICAL_PAIR.json',
            'same_pair_for_all_lower_tau':True,'coefficient_of_nonzero_squared_pairing':(2*difference).pair(),
            'identity':'D2F_tau(A0)[H,H]=2*(tau-tau_c)*(cof(A0):H)^2<0'}
    return out


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('tau',help='exact rational, e.g.113/10')
    print(json.dumps(classify(parser.parse_args().tau),indent=2))
