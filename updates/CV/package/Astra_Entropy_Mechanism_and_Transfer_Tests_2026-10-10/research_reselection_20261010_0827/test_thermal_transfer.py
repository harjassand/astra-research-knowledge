"""Exact contract check; no numerical diagonalization or external compute."""
from fractions import Fraction
import json
from pathlib import Path

a=Fraction(1,4)
r=Fraction(3,2)
assert a*r*r < 1 # K1=diag(1,a) lies in LY(r); strict sufficient check
rows=[]
for n,T in [(1,4),(16,4),(256,4),(1024,4),(4096,4),(4096,8)]:
    b=a**T
    top=(1/(1+b))**n
    distance=1-top
    rows.append(dict(n=n,T=T,a=str(a),radius=str(r),relative_operator_error=str(b),normalized_trace_distance_float=float(distance),exact_distance_positive=distance>0,exact_distance_exceeds_999_over_1000=distance>Fraction(999,1000),partition_numerator_bits=((1+b)**n).numerator.bit_length(),partition_denominator_bits=((1+b)**n).denominator.bit_length()))
assert rows[4]['relative_operator_error']=='1/256'
assert rows[4]['exact_distance_exceeds_999_over_1000']
# Fixed total imaginary time: q^k subdivided into k identical roots equals q.
# Use rational root families: diag(1,a)^T=diag(1,a^T), independently of regrouping.
for T in range(1,11):
    for k in range(1,6):
        assert (a**T)**k==(a**k)**T
out={'status':'PASS_EXACT_FAMILY_CHECK','not_a_general_complexity_lower_bound':True,'rows':rows,'formula':'D(diag(1,b)^tensor_n/(1+b)^n, |0^n><0^n|)=1-(1+b)^(-n); best rank-one relative operator error b; b=a^T'}
Path(__file__).with_name('thermal_transfer_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
