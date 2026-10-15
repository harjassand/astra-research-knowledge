import json,pickle,hashlib
from pathlib import Path
import sympy as s
from verify_positive_obstruction import build_system
base=Path(__file__).parent
with open(base/'positive_augmented_dual.pkl','rb') as ff:discovery=pickle.load(ff)
built=build_system();r=built['r']
assert built['E'].shape==discovery['E'].shape
assert all(s.cancel(vv)==0 for vv in built['E']-discovery['E'])
assert all(s.cancel(vv)==0 for vv in built['L']-discovery['L'])
def pol(vv):
    pp=s.Poly(vv,r)
    return [str(pp.coeff_monomial(r**ii)) for ii in range(pp.degree()+1)] if vv!=0 else ['0']
def rat(vv):
    nn,dd=s.fraction(s.cancel(vv));return {'numerator':pol(nn),'denominator':pol(dd)}
terms=[{'row':ii,'multiplier':rat(vv)} for ii,vv in enumerate(discovery['lam']) if vv!=0]
out={'schema':'astra.positive_sharp_input_heat_obstruction.v1','domain':'r>0',
     'status':'exact_non_sos_class_obstruction_external_review_unresolved',
     'formula':'F=3r/[8(r+2)] H+r(r-1)u²/6+j²+r uj',
     'system_shape':[411,62],'variable_order':'60 two-form coefficients row-major, then d1,d2',
     'two_form_pair_order':[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],
     'quadratic_monomial_order':[[0,0],[0,1],[0,2],[0,3],[1,1],[1,2],[1,3],[2,2],[2,3],[3,3]],
     'row_sections':built['sections'],
     'within_section_order':'as regenerated explicitly by verify_positive_obstruction.py; symmetry monomials in SymPy descending lexicographic order',
     'new_forced_zero':{'A':[1,0,0,1],'z':['0','1','0','0','0','-(r+1)']},
     'dual_terms':terms,
     'dual_identity':'sum_i lambda_i (E_i vars) = P(e21,(0,1,0,0,0,0)) + r(r+1)(2r+1)d2/(r+2)',
     'diffusion_positive_after_averaging':'d2>0 and 3d1=(2r+1)d2',
     'SOS_assumption':False,'nonquasiconvexity_proved':False,
     'excluded_class':'fixed positive input diffusion; local closed two-form with homogeneous-quadratic coefficients, extended to C2 coefficients near zero by homogeneous Taylor reduction',
     'outside_scope':['output-coupled heat','nonlocal corrections','singular angular corrections','higher jets','general quasiconvexity']}
path=base/'POSITIVE_INPUT_HEAT_OBSTRUCTION.json';path.write_text(json.dumps(out,indent=2)+'\n')
print(path.name,hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
