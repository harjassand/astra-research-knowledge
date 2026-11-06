"""Exact regression suite for proof-relevant failure modes, no dependencies."""
import json,time,copy
from pathlib import Path
from exact import *
from compile_witness import compile_pair,word_delta
from check_certificate import check_pair
ROOT=Path(__file__).resolve().parent

def replacer(a,rho):
    rho=mat(rho);return {'input_dim':a,'output_dim':len(rho),'choi':out(kron(eye(a),rho))}

def pad(ch,newb):
    a,b=ch['input_dim'],ch['output_dim'];jj=zero(a*newb);old=mat(ch['choi'])
    for i in range(a):
        for j in range(a):
            for k in range(b):
                for l in range(b):jj[i*newb+k][j*newb+l]=old[i*b+k][j*b+l]
    return {'input_dim':a,'output_dim':newb,'choi':out(jj)}

identity=from_kraus([eye(2)])
replace=replacer(2,[[F(1,2),0],[0,F(1,2)]])
down=from_kraus([[[1,0],[0,F(3,5)]],[[0,F(4,5)],[0,0]]])
up=from_kraus([[[F(3,5),0],[0,1]],[[0,0],[F(4,5),0]]])
unitary=from_kraus([[[1,0],[0,Q(F(3,5),F(4,5))]]])
basis,_=hermitian_basis(2)
assert word_delta(Channel(down),Channel(up),basis,[1,2])==Q(0,F(32,41))
for i in range(3):
    for j in range(3):assert not word_delta(Channel(down),Channel(up),basis,[i,j]).re
cases=[('identity_vs_replacer',identity,replace,None,False),
       ('imaginary_second_moment',down,up,None,False),
       ('rank_deficient_outputs',pad(down,3),pad(up,4),None,False),
       ('longer_path',identity,replace,[0,0,0,0],False),
       ('unitary_equivalence',identity,unitary,None,True),
       ('replacer_equivalence',replace,replacer(2,[[1,0,0],[0,0,0],[0,0,0]]),None,True)]
results=[]
for name,e,f,forced,equal in cases:
    start=time.perf_counter();cert=compile_pair(e,f,forced_word=forced)
    assert (cert['status']=='equal_maximal_profiles')==equal
    inp={'E':e,'F':f}
    (ROOT/(name+'_input.json')).write_text(json.dumps(inp,indent=2)+'\n')
    (ROOT/(name+'_certificate.json')).write_text(json.dumps(cert,indent=2)+'\n')
    summary={'name':name,'passed':True,'status':cert['status'],'elapsed_seconds':round(time.perf_counter()-start,6)}
    if not equal:
        checked=check_pair(e,f,cert)
        (ROOT/(name+'_checked.json')).write_text(json.dumps(checked,indent=2)+'\n')
        summary.update({k:cert[k] for k in ['reference_dim','separating_word','moment_difference','largest_state_entry_bits','orientation','universal_normalized_margin']})
        summary['product_terms']=[len(cert['rho_product_mixture']),len(cert['sigma_product_mixture'])]
        if name=='imaginary_second_moment':
            assert cert['identity_inserted'] and q(cert['moment_difference']).im and not q(cert['moment_difference']).re
        # A reported large margin must not be accepted just because states are valid.
        bad=copy.deepcopy(cert);bad['universal_normalized_margin']=str(2*F(cert['universal_normalized_margin']))
        try:check_pair(e,f,bad)
        except ValueError:pass
        else:raise AssertionError('Tampered margin accepted')
    results.append(summary);print(json.dumps(summary),flush=True)
for label,obj in [('not_tp',{'input_dim':2,'output_dim':2,'choi':out(scale(2,mat(identity['choi'])))}),
                  ('not_cp',{'input_dim':1,'output_dim':2,'choi':[[2,0],[0,-1]]})]:
    try:Channel(obj)
    except ValueError:results.append({'name':label,'passed':True,'result':'rejected'})
    else:raise AssertionError('Invalid channel accepted')
(ROOT/'verification.json').write_text(json.dumps({'tests':results,'all_passed':True},indent=2)+'\n')
