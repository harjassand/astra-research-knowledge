import sympy as s
from pathlib import Path
import json
r=s.Rational
U=s.diag(1,r(1,1000));V=s.Matrix([[999,31],[31,10]])/1000
I=s.eye(2)
def pd(M):return M[0,0]>0 and M.det()>0
assert pd(U) and pd(V) and pd(I-V)
assert pd(8*V-5*U)
B=(U+8*V)/9
a=1-B[0,0];b=a*a+B[0,1]**2
assert a==r(1,1125) and b==r(962,1265625)
assert b>r(5,6)*a and b>(3*a+a*a)/4
report={'status':'PASS','a':str(a),'b':str(b),'b_over_a':str(b/a),'index6_cap_excess':str(b-r(5,6)*a),'proposed_physical_variance_excess':str(b-(3*a+a*a)/4),'det_V':str(V.det()),'det_I_minus_V':str((I-V).det()),'det_8V_minus_5U':str((8*V-5*U).det()),'source_scope':'faithful unique-top physical3/reference6; relative peak <=3/2'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
