"""Emit one fully acquired, factored mathematical certificate for review."""
from fractions import Fraction
from pathlib import Path
import json
from shared_port_modules import acquire


def plain(x):
    if isinstance(x,Fraction):return dict(numerator=str(x.numerator),denominator=str(x.denominator))
    if isinstance(x,dict):return {k:plain(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [plain(v) for v in x]
    return x


def main():
    raw=[((1,2,0),(2,1,0),1),((2,1,0),(3,0,0),2),((3,0,0),(1,2,0),3),
         ((2,0,2),(3,0,1),5),((3,0,1),(4,0,0),7),((4,0,0),(2,0,2),11)]
    cert=acquire(raw,(0,4,5),1,1)
    receipt={key:cert[key] for key in ['raw','x0','lam','mu','p','shift','C','M','head_values',
             'eta','t','epsilon','delta','E','Acut','head','nu','zeta','rho','count_offset',
             'count_slope','head_count_bounds','head_rate_bound','head_drift_bound',
             'stationary_total_moment_bound']}
    receipt['modules']=[]
    for block in cert['live']:
        c=block['cert']
        receipt['modules'].append(dict(indices=block['indices'],v=c['v'],offset=c['offset'],
                                      r=c['r'],s=c['s'],Qcut=block['qcut'],Z0=c['Z0'],
                                      selected=[dict(source=g['selected'][0],target=g['selected'][1],
                                                     rate=g['selected'][2],c=g['c'],m=g['m'],b=g['b'])
                                                for g in c['groups']]))
    receipt['function']='W=t^(A+sum_i r_i q_i) [1+epsilon/(A+shift)^p+delta H(A)]'
    receipt['scope']='Concrete acquired certificate for two nonlinear modules; universal modular theorem is established by the analytic proof.'
    path=Path('outputs/capability_first_20261101/shared_port_example.json')
    path.write_text(json.dumps(plain(receipt),indent=2)+'\n')
    print(json.dumps(dict(output=str(path),head_bits=cert['head'].bit_length(),
                          M=cert['M'],p=cert['p'],factored_actual_count_moment=True)))


if __name__=='__main__':main()
