"""Represent an admissible cubic by translation plus two binary jet cubics."""
from pathlib import Path
from fractions import Fraction as R
import argparse,json
from kernel import data
from receive import b
HERE=Path(__file__).resolve().parent

def normalize(coefficients):
    d=data();qc=json.loads((HERE.parent/'quadratic_boundary/certificate.json').read_text());cert=json.loads((HERE/'certificate.json').read_text())
    c=list(map(R,coefficients));assert len(c)==20;op=[list(map(R,row)) for row in qc['normal_form_operator']]
    coords=[sum(a*v for a,v in zip(row,c)) for row in op];assert [sum(coords[j]*d['basis'][j][i] for j in range(12)) for i in range(20)]==c,'Cubic outside the admitted space'
    jetop=[list(map(R,row)) for row in cert['jet_operator_on_normal_basis']];charges=[sum(row[j]*coords[j] for j in range(12)) for row in jetop];JB=[list(map(R,row)) for row in cert['unit_charge_basis']]
    assert [sum(coords[j]*d['basis'][j][i] for j in range(4))+sum(charges[j]*JB[j][i] for j in range(8)) for i in range(20)]==c
    return {'translation':list(map(str,coords[:4])),'first_acoustic_binary_cubic':list(map(str,charges[:4])),'second_acoustic_binary_cubic':list(map(str,charges[4:])),'binary_coefficient_order':['x^3','x^2 y','x y^2','y^3'],'exact_reconstruction':True,'scope':'Natural coordinates on all twelve admissible cubic modes; this is not a QC decision.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--cubic',type=Path);args=parser.parse_args();qc=json.loads((HERE.parent/'quadratic_boundary/certificate.json').read_text());c=json.loads(args.cubic.read_text()) if args.cubic else qc['example_cubic_coefficients'];print(json.dumps(normalize(c),indent=2))
if __name__=='__main__':main()
