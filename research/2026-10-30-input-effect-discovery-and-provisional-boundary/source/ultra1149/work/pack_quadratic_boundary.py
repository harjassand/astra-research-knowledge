"""Package the actual-boundary and compatible-correlation operations."""
from pathlib import Path
from fractions import Fraction as R
import importlib.util,json,math,sympy as S
root=Path(__file__).resolve().parents[1];out=root/'outputs/quadratic_boundary';out.mkdir(exist_ok=True)
raw=json.loads((root/'work/actual_boundary.json').read_text());gd=json.loads((root/'outputs/graded_stabilization/certificate.json').read_text())
gram=json.loads((root/'work/roc_biform_1859_1.json').read_text());res=json.loads((root/'work/resonance_quotient.json').read_text())
maximum=json.loads((root/'work/isotropic_boundary.json').read_text())['maxima'][0][1]
yy=R(round(math.tan(maximum[0])*10**6),10**6);tt=R(round(math.tan(maximum[1])*10**6),10**6)
delta={tuple(row[:1]):R(row[1],row[2]) for row in raw['delta']};N={tuple(row[:3]):R(row[3],row[4]) for row in raw['regularized_numerator']}
ev=lambda p,point:sum(co*math.prod(x**e for x,e in zip(point,pw)) for pw,co in p.items())
ratio=ev(N,[tt,R(1),yy])/(2*(1+yy*yy)**3*(1+tt*tt)*ev(delta,[tt]));lower=R(1858795,1000)
assert ratio>lower
T=[S.Matrix(list(map(S.Rational,v))) for v in gd['translation_cubics']];chosen=[];M=S.Matrix.hstack(*T)
for v in gd['cubic_kernel_basis']:
    v=S.Matrix(list(map(S.Rational,v)))
    if M.row_join(v).rank()>M.cols:chosen.append(v);M=M.row_join(v)
    if M.cols==12:break
assert len(chosen)==8
_,indices=M.T.rref();indices=list(indices);sub=M[indices,:];inv=sub.inv();operator=S.zeros(12,20)
for j,idx in enumerate(indices):operator[:,idx]=inv[:,j]
assert operator*M==S.eye(12)
cert={'F':raw['F'],'cubic_powers':gd['cubic_powers'],'example_cubic_coefficients':gd['example_cubic_coefficients'],
  'delta':raw['delta'],'regularized_numerator':raw['regularized_numerator'],
  'ROC_upper':gram,'ROC_lower':str(lower),'lower_rank_one_output':['1',str(yy)],'lower_rank_one_spatial':['1',str(tt)],
  'exact_ratio_at_lower_direction':str(ratio),
  'lower_calibration_modes':[{'frequency':[tt.denominator,tt.numerator],'sine':[str(R(1,tt.denominator)),str(yy/tt.denominator)]}],
  'resonance_fields':res['fields'],'normal_form_basis':[[str(z) for z in v] for v in T+chosen],
  'normal_form_operator':[[str(z) for z in row] for row in operator.tolist()],
  'quadratic_powers':[[i,j,k,2-i-j-k] for i in range(3) for j in range(3-i) for k in range(3-i-j)],
  'scope':'Complete ROC boundary criterion and compatible-gradient correlation reduction. Global QC at the near-boundary ROC fixture remains UNKNOWN.'}
(out/'certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
print(json.dumps({'rigorous_ROC_threshold_lower':str(lower),'rigorous_ROC_threshold_upper':'1859','ratio_at_lower_direction_float':float(ratio),
 'resonance_quotient_rank':8,'normal_form_dimension_fixed_leading_mod_affine_det_translations':17},indent=2))
