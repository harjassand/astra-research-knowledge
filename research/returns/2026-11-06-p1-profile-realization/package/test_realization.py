"""Exact positive, boundary, negative, central-quotient, and tamper checks."""
import json,time,copy
from pathlib import Path
from exact import *
from compile_realization import compile_realization
from check_realization import check
from compile_panel import family_words, dot

HERE=Path(__file__).parent

def planar(s,root,kappa=F(1,4)):
    assert root*root==1-s*s
    d0=(1+s)/2;d1=(1-s)/2;off=kappa*root
    return {'input_dim':2,'output_dim':2,'choi':out(mat([[d0,0,0,off],[0,d1,0,0],[0,0,d0,0],[off,0,0,d1]]))}

def run():
    g0=planar(F(0),F(1));g3=planar(F(3,5),F(4,5))
    ident=from_kraus([eye(2)]);replacer=from_kraus([[[1,0],[0,0]],[[0,1],[0,0]]])
    cases=[('signed_interior',{'channels':[g0,g3],'coefficients':['-1/3','4/3']},'realizable'),
      ('positive_nonphysical_boundary',{'channels':[g0,g3],'coefficients':['-2/3','5/3']},'not_realizable_null_ideal'),
      ('negative_density',{'channels':[g0,g3],'coefficients':['-1','2']},'not_realizable_negative_norm'),
      ('central_quotient',{'channels':[ident,replacer],'coefficients':['0','1']},'realizable'),
      ('one_dimensional_input',{'channels':[from_kraus([[[F(3,5)],[F(4,5)]]]),from_kraus([[[1]]])],'coefficients':['-9','10']},'realizable')]
    results=[]
    for name,obj,status in cases:
        before=time.monotonic();cert=compile_realization(obj['channels'],obj['coefficients']);compiled=time.monotonic()
        assert cert['status']==status,(name,cert['status']);checked=check(obj,cert)
        elapsed=time.monotonic()-compiled
        for suffix,value in [('input',obj),('certificate',cert),('checked',checked)]:
            (HERE/f'{name}_{suffix}.json').write_text(json.dumps(value,indent=2)+'\n')
        results.append({'case':name,**checked,'compiler_seconds':compiled-before,'checker_seconds':elapsed})
        broken=copy.deepcopy(cert)
        if status=='realizable':broken['channel']['choi'][0][0]='0'
        else:broken['polynomial_coefficients']=['0']*len(cert['word_basis'])
        try:check(obj,broken)
        except (AssertionError,ValueError):results[-1]['tamper_rejected']=True
        else:raise AssertionError('Tampering accepted')
    # Compare the proposed signed profile directly with the explicit minimal g4.
    # Closed word span, not merely including g4 as an unused compiler input.
    g4=planar(F(4,5),F(3,5));basis,_=hermitian_basis(2)
    queue,moments=family_words([Channel(g0),Channel(g3),Channel(g4)],basis)
    contrast=[F(-1,3),F(4,3),F(-1)]
    assert all(dot(contrast,row)==Q() for row in moments)
    # Unreferenced maximal chi-square survives at the nonphysical boundary limit.
    rho=scale(F(1,2),eye(2));sigma=mat([[F(1,2),F(1,4)],[F(1,4),F(1,2)]])
    assert Channel(g0).chi(sigma,rho,1)==Channel(g3).chi(sigma,rho,1)==Channel(g4).chi(sigma,rho,1)==F(1,64)
    assert Channel(replacer).chi(sigma,rho,1)==0
    result={'all_passed':True,'cases':results,'explicit_minimal_interior_word_relation':{'passed':True,'word_algebra_dimension':len(queue),'maximum_word_length':max(map(lambda z:len(z[0]),queue))},'unreferenced_boundary_limit_chi_squared':'1/64','boundary_replacer_chi_squared':'0',
            'scope':'Finite exact regressions; universal statements depend on the proofs.'}
    (HERE/'realization_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()
