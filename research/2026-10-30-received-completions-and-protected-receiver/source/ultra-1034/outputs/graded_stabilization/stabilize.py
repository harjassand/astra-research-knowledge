"""Construct a QC, non-PC polynomial or return an exact acoustic obstruction.

No arguments: use the explicit cubic outside the translation span.
--coefficients PATH: JSON list of 20 rational strings, ordered by cubic_powers
in certificate.json. --quartic-scale is positive; --nu controls only the
rank-one obstruction witness when the cubic is inadmissible.
The acquired proof and certificate are the mathematical authority.
"""
from fractions import Fraction as R
from pathlib import Path
from math import prod
import argparse,json

HERE=Path(__file__).resolve().parent
def acoustic_score(coefficients,powers,K,Rv):
    ans=R(0)
    for co,pw in zip(coefficients,powers):
        for j,power in enumerate(pw):
            if power:
                ee=list(pw);ee[j]-=1
                ans+=2*co*power*K[j]*prod(z**e for z,e in zip(Rv,ee))
    return ans
def construct(coefficients,quartic_scale=R(1),witness_nu=R(1)):
    cert=json.loads((HERE/'certificate.json').read_text());powers=cert['cubic_powers'];cs=list(map(R,coefficients))
    quartic_scale=R(quartic_scale);witness_nu=R(witness_nu)
    if len(cs)!=20 or quartic_scale<=0:raise ValueError('Require 20 cubic coefficients and positive quartic scale')
    scores=[sum(R(m)*c for m,c in zip(row,cs)) for row in cert['cubic_constraint_matrix']]
    if any(scores):
        av=list(map(R,cert['base_parameters']));a,b,c,d=av;av2=[-b,a,d,-c]
        for spatial,K0 in ((0,av),(1,av2)):
            for x,y in ((1,0),(0,1),(1,1),(1,-1)):
                K=[x*K0[0]-y*K0[2],x*K0[1]-y*K0[3],y*K0[0]+x*K0[2],y*K0[1]+x*K0[3]]
                Rv=[R(x if spatial==0 else 0),R(x if spatial==1 else 0),R(y if spatial==0 else 0),R(y if spatial==1 else 0)]
                eta=acoustic_score(cs,powers,K,Rv)
                if eta:
                    s=-(2*witness_nu*sum(z*z for z in Rv)+1)/eta
                    return {'admissible':False,'scope':'No finite quadratic can make this cubic plus the specified quartic ROC or QC.',
                      'witness_quadratic_coefficient':str(witness_nu),'base':[str(s*z) for z in K],
                      'rank_one_direction':list(map(str,Rv)),'second_line_derivative':'-1',
                      'acoustic_cubic_score':str(eta)}
        raise AssertionError('A nonzero binary cubic must have a nonzero value at one of four distinct projective points')
    norm=sum(map(abs,cs));nu=R(2**cert['stabilization_power'])*norm*norm/quartic_scale
    return {'admissible':True,'quartic_scale':str(quartic_scale),
      'quartic':'F_* from ../hopf_structure/certificate.json',
      'cubic_powers':powers,'cubic_coefficients':list(map(str,cs)),
      'quadratic':'nu*(a*a+b*b+c*c+d*d)','nu':str(nu),
      'strong_QC_modulus':str(nu/2),'nonpolyconvex':True,
      'scope':'Constructive theorem in PROOF.txt; bound is conservative and not a practical performance claim.'}
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--coefficients',type=Path);parser.add_argument('--quartic-scale',default='1');parser.add_argument('--nu',default='1')
    args=parser.parse_args();cert=json.loads((HERE/'certificate.json').read_text())
    coefficients=json.loads(args.coefficients.read_text()) if args.coefficients else cert['example_cubic_coefficients']
    print(json.dumps(construct(coefficients,R(args.quartic_scale),R(args.nu)),indent=2))
if __name__=='__main__':main()
