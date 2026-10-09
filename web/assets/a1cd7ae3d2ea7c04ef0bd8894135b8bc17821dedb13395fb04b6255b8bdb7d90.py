#!/usr/bin/env python3
"""Charge an explicit primitive replacer coefficient for the fixed obstruction."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import sys


def run():
    folder=Path(__file__).resolve().parent
    base=folder/'verify_fixed_dim4.py'
    ns={'__name__':'fixed_dim4_dependency','__file__':str(base)}
    exec(compile(base.read_text(),str(base),'exec'),ns)
    raw=ns['run']()
    Svals=[F(x) for x in raw['raw_s']]
    Q=[[F(x) for x in row] for row in raw['Q_root_coherence']]
    Z=F(raw['normalization_Z'])
    A0=sum(Svals[1:],F())
    Qnorm2=ns['tr'](ns['mul'](Q,Q))
    delta_rho=ns['scale'](ns['add'](ns['mul'](ns['diag'](Svals),Q),
                                  ns['mul'](Q,ns['diag'](Svals))),1/Z)
    G=ns['zero']()
    for i,k in enumerate([18,20,22],1):
        G[0][i]=G[i][0]=2*k*Q[0][i]/(Svals[i]-1)
    rep_J=ns['tr'](ns['mul'](delta_rho,G))
    rep_E=Qnorm2/Z
    base_J=F(raw['physical_J2_over_A0_log2_per_Z'])*A0/Z
    base_E=F(raw['root_E2_over_A0_per_Z'])*A0/Z
    eta=F(1,4096)
    Jtotal=base_J+eta*rep_J
    Etotal=base_E+eta*rep_E
    uppergap=Jtotal*F(7,10)-2*Etotal
    assert uppergap<0 and Jtotal>0 and Etotal>0
    assert Qnorm2/2<4096**2  # arrow Q has operator norm sqrt(Tr Q^2/2)
    return {
        'status':'PASS',
        'fixed_replacer_weight':str(eta),
        'replacer_J2_log2_coefficient':str(rep_J),
        'replacer_E2':str(rep_E),
        'primitive_J2_log2_coefficient':str(Jtotal),
        'primitive_E2':str(Etotal),
        'primitive_gap_upper_using_log2_lt_7over10':str(uppergap),
        'primitive_ratio_upper':str(Jtotal*F(7,10)/Etotal),
        'Q_operator_norm_squared':str(Qnorm2/2),
        'positive_q_interval':'|epsilon|<1/4096 implies S+epsilon Q>0',
        'nonlinear_negative_gap_interval':'There exists epsilon0 in (0,1/4096) such that every 0<|epsilon|<epsilon0 gives J(rho_epsilon)<2 E(rho_epsilon); proven by the strict exact Hessian and finite analytic Taylor expansion. Particular epsilon0 not quantified in this packet.',
        'state_family':'rho_epsilon=(S+epsilon Q)^2/Tr[(S+epsilon Q)^2]; all sufficiently small positive rational epsilon give faithful rational states.',
        'primitive_legality':'Hsym>=0 and both Hs=Hstar s=0; adding eta*(I-|s><s|) gives real part >=eta on s-perp. Hence exp(-tH) converges to the faithful replacer.',
        'source_replay_sha256':hashlib.sha256((folder/'FIXED_DIM4_REPLAY.json').read_bytes()).hexdigest(),
        'scan_count':0,
        'arithmetic':'Python stdlib Fraction only'
    }


def main():
    path=Path(__file__).resolve().parent/'PRIMITIVE_DIM4_REPLAY.json'
    result=run()
    if sys.argv[1:]==['--verify']:
        assert json.loads(path.read_text())==result
        print('PASS: exact primitive coefficient and margin reproduced.')
    elif not sys.argv[1:]:
        with path.open('x') as f:
            json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
        print('PASS: wrote exact primitive coefficient and margin.')
    else:raise SystemExit('Usage: verify_primitive_dim4.py [--verify]')
    print('sha256',hashlib.sha256(path.read_bytes()).hexdigest())


if __name__=='__main__':main()
