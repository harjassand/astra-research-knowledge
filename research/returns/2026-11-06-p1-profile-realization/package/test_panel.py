"""Exact regressions for common panels, signed reconstruction, and zero dimension.

The checker verifies word-span closure, physical product mixtures and uniform
perturbation bounds. Tests of three rational Loewner kernels supplement, but
cannot replace, the proof for all operator-convex functions.
"""
import copy,json,time
from pathlib import Path
from exact import *
from compile_panel import compile_panel
from check_panel import check_panel

HERE=Path(__file__).resolve().parent

def replacer(a,rho):
    rho=mat(rho)
    return {'input_dim':a,'output_dim':len(rho),'choi':out(kron(eye(a),rho))}

def flagged(first,second,weight):
    a=first['input_dim'];assert a==second['input_dim']
    b1,b2=first['output_dim'],second['output_dim'];b=b1+b2
    j=zero(a*b)
    for ob,p,off in [(first,weight,0),(second,1-weight,b1)]:
        old=mat(ob['choi']);bb=ob['output_dim']
        for i in range(a):
            for z in range(a):
                for k in range(bb):
                    for l in range(bb):
                        j[i*b+off+k][z*b+off+l]=p*old[i*bb+k][z*bb+l]
    return {'input_dim':a,'output_dim':b,'choi':out(j)}

def rejected(objects,cert):
    try:check_panel(objects,cert)
    except (ValueError,AssertionError,IndexError):return True
    return False

def run():
    ident=from_kraus([eye(2)])
    replace=replacer(2,[[F(1,2),0],[0,F(1,2)]])
    mixed=flagged(ident,replace,F(1,3))
    down=from_kraus([[[1,0],[0,F(3,5)]],[[0,F(4,5)],[0,0]]])
    up=from_kraus([[[F(3,5),0],[0,1]],[[0,0],[F(4,5),0]]])
    unitary=from_kraus([[[1,0],[0,Q(F(3,5),F(4,5))]]])
    cases=[('six_channel_family',[ident,replace,mixed,down,up,unitary],4),
       ('signed_reconstruction',[mixed,replace,ident],2),
       ('zero_dimensional_replacer_family',[replace,replacer(2,[[1,0,0],[0,0,0],[0,0,0]]),replacer(2,[[1]])],1),
       ('reference_only_one_dimensional_input',[from_kraus([[[F(3,5)],[F(4,5)]]]),from_kraus([[[1]]])],1)]
    results=[]
    for name,objects,p in cases:
        start=time.perf_counter();cert=compile_panel(objects);compiled=time.perf_counter()
        checked=check_panel(objects,cert);finished=time.perf_counter()
        assert cert['augmented_profile_rank']==p
        assert cert['probe_count']==p-1
        if name=='six_channel_family':
            assert cert['selected_basis_channel_indices']==[0,1,3,4]
            assert mat(cert['affine_reconstruction'])==mat([[1,0,F(1,3),0,0,1],[0,1,F(2,3),0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0]])
        if name=='signed_reconstruction':
            assert cert['selected_basis_channel_indices']==[0,1]
            assert [row[2] for row in mat(cert['affine_reconstruction'])]==[q(3),q(-2)]
        bad=copy.deepcopy(cert)
        bad['affine_reconstruction'][0][-1]=str(F(bad['affine_reconstruction'][0][-1])+1)
        assert rejected(objects,bad),'False affine reconstruction accepted'
        checks={'tampered_reconstruction_rejected':True}
        if p>1:
            bad=copy.deepcopy(cert);bad['probes'].pop()
            assert rejected(objects,bad),'Missing required probe accepted'
            checks['missing_probe_rejected']=True
        for suffix,value in [('input',{'channels':objects}),('certificate',cert),('checked',checked)]:
            (HERE/f'{name}_{suffix}.json').write_text(json.dumps(value,indent=2)+'\n')
        results.append({'case':name,**checked,**checks,
            'compiler_seconds':compiled-start,'checker_seconds':finished-compiled})
    result={'all_passed':True,'cases':results,
        'scope':'Explicit rational matrices; finite regressions and certificate checks. Proofs supply the universal quantifiers. Timings are toy diagnostics, not scaling benchmarks.'}
    (HERE/'panel_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':run()
