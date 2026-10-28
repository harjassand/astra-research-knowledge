#!/usr/bin/env python3
"""Independent composition checks; no author check script imported or executed."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

expected = {
 'ordinary_balanced_row_anchor_20261028/AUTOMATIC_ROW_FAST_PATH_FINITE_M_SUBSTITUTION.md':'c0846b68556ff828bac8221078ae129c411976f080389470fad5d587bc0ff599',
 'ordinary_balanced_row_anchor_20261028/AUTOMATIC_VALIDATED_ROW_FAST_PATH.md':'69b012d669b6e8a32a587b804768acf2bc3155906ea2598727275c357a89fd05',
 'ordinary_balanced_row_anchor_20261028/automatic_row_fast_path_independent_receipt.json':'52388d7dc9184fe4fa26a5ebb7971992f655abb772c00a14912940ac63309044',
 'ordinary_balanced_row_anchor_20261028/FAST_PATH_RESOURCE_EVENT_IMPLEMENTATION_CLARIFICATION.md':'cea657a43f9b6fac5a9567a285de21676e523b0cb54b1b2f768332896f74d3b0',
 'ordinary_generic_matrix_gls_multipayload_relative_20261028.md':'cee0f8d6755f6a50ed8e21e7aea94da42703e1ffca4d5ef38e4f427df693c518',
 'direct_cptp_bures_bridge_20261027/PRIVATE_FRAMED_COMPLETE_OPTIMALITY.md':'718c8658211d88a135ff8aea28be652bed14dc16e025f518ca0e4c4b35db9708',
}
for p,h in expected.items(): assert sha(ROOT/p)==h, p
imports = json.loads((HERE/'automatic_row_fast_path_independent_receipt.json').read_text())
for p,h in imports['sha256_relative_to_programme_root'].items():
    assert sha(ROOT/p)==h, p

power_cases=0
mixture_cases=0
for M in range(1,65):
    for ia in range(21):
        a=F(ia,20)
        tangent=M*a**(M-1)
        assert tangent*(1-a)<=1-a**M
        for jf in range(21):
            f=a*F(jf,20)
            assert a**M-f**M<=tangent*(a-f)
            power_cases+=1
        # Correlated calibration: do not replace E[f^M] by (Ef)^M.
        for w in [F(0),F(1,7),F(1,2),F(1)]:
            f1,f2=a/3,4*a/5
            ef=w*f1+(1-w)*f2
            efm=w*f1**M+(1-w)*f2**M
            assert a**M-efm<=tangent*(a-ef)
            assert efm>=ef**M
            mixture_cases+=1
assert F(1,2) != F(1,2)**2 # explicit shared-record countercheck

parameter_cases=0
for M in [1,2,3,7,31,256,4096]:
    for gamma in [F(1),F(1,3),F(1,1024)]:
        for eps in [F(1),F(1,7),F(1,1024)]:
            gl,el=gamma/2,eps/(4*M)
            assert gl*el==gamma*eps/(8*M)
            local_delta=17*el/4096
            assert local_delta==17*eps/(16384*M)
            assert 2*M*local_delta==17*eps/8192
            assert 2*M*local_delta+eps/2 < eps
            assert el/1024==eps/(4096*M)
            assert 3*el/1024<eps/(1024*M)
            assert eps/2>=el/1024
            parameter_cases+=1

result=dict(status='PASS_INDEPENDENT_AUTOMATIC_ROW_FINITE_M_COMPOSITION',
 source_sha256=expected['ordinary_balanced_row_anchor_20261028/AUTOMATIC_ROW_FAST_PATH_FINITE_M_SUBSTITUTION.md'],
 script_sha256=sha(Path(__file__)),new_source_bindings=len(expected),
 local_receipt_manifest_bindings=len(imports['sha256_relative_to_programme_root']),
 exact_power_cases=power_cases,exact_shared_history_mixture_cases=mixture_cases,
 exact_parameter_budget_cases=parameter_cases,
 source_calls=0,rng_draws=0,sampled_source_outcomes=0,
 scope='Only new finite-M parameter/shared-history/resource-event composition. Accepted acquisition, compiler and comparator primitives imported, not independently re-proved or executed.')
(HERE/'automatic_row_finite_m_independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
