"""Exact source-binding and rational receiving checks; no independent review."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent;base=root.parent
checks=0
def ck(v):
 global checks
 assert v;checks+=1
D=Q(1,10**100);N=10**200;K=10**40;T=10**40
ck(T**5==N);ck(K*T<=D*N);ck(D*N>=4)
# Geometric bounds: 2^(-3/2)<1/2 and 2^(-1/2)<3/4.
ck(Q(1,8)<Q(1,4));ck(Q(1,2)<Q(9,16))
# Last-partial-stage post-jump C,D,E and B margins.
ck(Q(29,32)*D*N-Q(3,2)>=D*N/2)
ck(Q(4,3)*(1-Q(5,32))>=Q(1,4))
ck((1-3*D-2*Q(1,10**50))*N-3>=N/2)
ck(D/2>=D*(1+D)/4)
ck(Q(1,2)>=D*(1+D)/4)
ck(Q(1,2*10**50)>=D*(1+D)/4)
ck(Q(7,8)*(1+D)*N<Q(15,16)*(N+2))
ck(Q(32,K)<1) # K^(3/2)>=K.
ck(D*N/2-2>0)
# Drift-solver tail algebra: [8/27]*(3/4)^(3/2)=sqrt(3)/9, checked by square.
ck((Q(8,27)**2)*(Q(3,4)**3)==Q(3,81))
# Source hashes bind exact accepted components; no import of author code.
expected={
'FINITE_LEVEL_CORRECTED_CLOCK.md':(root/'FINITE_LEVEL_CORRECTED_CLOCK.md','e0700bad37717a38976f295049a8d2cb1120aeb155c343783780d6b201f20c9d'),
'dyadic_source':(base/'rate2_dyadic_continuation/EXACT_CORRECTOR_AND_STAGE_LEMMA.md','0ddcfb78c068ae58c2e5ddae1da015ba70d76acae67a2b0e9104f7358775e0a2'),
'dyadic_receipt':(base/'rate2_dyadic_continuation/audit_stage_20261101_0422/SOURCE_BOUND_ACCEPTANCE.md','b96a909e99ed17b463bca5bacaf4ed340a4b65109c3ad41c1fdad09887487dd0'),
'dyadic_conventions':(base/'rate2_dyadic_continuation/receiving_conventions_20261101/EXACT_RECEIVING_ADDENDUM.md','f312ac1f91b479acd5684966f80509ac1349e21803c411952aed8f17cb2222f5'),
'interior_source':(base/'rate2_paid_interior_removal/PAID_INTERIOR_REMOVAL.md','a8e0bd383b053021f72e8197986581c87878046cdeaa7570536e44f5cf71a1cf')}
for _,(f,sha) in expected.items():ck(hashlib.sha256(f.read_bytes()).hexdigest()==sha)
result={'status':'PASS_AUTHOR_CONTINUATION_CHECKS_NOT_INDEPENDENT_REVIEW','exact_checks':checks,'dependency_hashes':{k:sha for k,(_,sha) in expected.items()},'proof_sha256':hashlib.sha256((root/'ACTUAL_CLEARANCE_WINDOW_AND_OCCUPATION.md').read_bytes()).hexdigest(),'numerical_acquisition_gate':'Interior c(epsilon), n0(epsilon) remain existence constants; finite numerical admission must acquire or refuse them.'}
(root/'CLEARANCE_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
