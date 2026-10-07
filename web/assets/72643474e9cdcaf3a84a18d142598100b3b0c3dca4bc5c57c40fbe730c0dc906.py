"""Finite diagnostics for the separately proved symmetric family."""
from frontier_rank_guard import *
from representation_compiler import det,minor,rank
from check_banded import determinant_table,table_prefix,encode
from pathlib import Path
import json,time

def run():
    reports=[]
    for n in (4,6,8,20):
        start=time.monotonic();q=n//2;alpha=Q(1,10);bound=n*n+4*n
        delta=alpha/(4*n*q*bound**(q-1)*2**n)
        base=[[C(5 if i==j else int(1<=abs(i-j)<=2)) for j in range(n)] for i in range(n)]
        d=[[C(Q(1,i+j+1)) if i!=j else C(0) for j in range(n)] for i in range(n)]
        f=[[base[i][j]+delta*d[i][j] for j in range(n)] for i in range(n)]
        assert all(f[i][j]==f[j][i] for i in range(n) for j in range(n))
        assert all(f[i][j] for i in range(n) for j in range(n) if i!=j)
        certificate=acquire_banded_uniform_certificate(f,2,0,q)
        assert certificate['status']=='UNIFORM_CERTIFIED'
        assert certificate['norm_estimate']>=1
        cauchy_rank=rank(minor(d,range(q,n),range(q)));assert cauchy_rank==q
        crossrank=rank(minor(f,range(q,n),range(q)));assert crossrank>=q-2
        witness=det(minor(certificate['H'],range(0,n,2),range(1,n,2)))
        assert witness.im==0 and witness.re>=1
        assert delta*n<=Q(1,16)
        assert certificate['operator_norm_upper_bound']<=bound
        assert certificate['eta_squared']<=n*n*delta*delta
        norm=norm_uniform_accuracy(certificate,Q(1,100))
        assert norm['branch']=='APPROXIMATE_WIDTH_BACKEND'
        actual=None;relative=None
        if n<=8:
            actual=table_prefix(determinant_table(f),n)[q]
            relative=abs(norm['norm']-actual)/actual
            assert relative<=Q(1,100)
        reports.append({'n':n,'k':q,'status':certificate['status'],
            'original_frontier':recognize_frontier(f)['width'],
            'compiled_frontier':certificate['counts']['extended_width'],
            'middle_cross_rank':crossrank,'middle_cross_rank_lower_bound':q-2,
            'Cauchy_cross_rank':cauchy_rank,'condition_number_upper_bound':Q(145,15),
            'norm_bit_length':norm['norm'].numerator.bit_length()+norm['norm'].denominator.bit_length(),
            'true_norm_small_comparator':actual,'relative_error_small_comparator':relative,
            'backend_stats':certificate['counts']['stats'],
            'elapsed_seconds_diagnostic':time.monotonic()-start})
    return {'status':'PASS','fixtures':reports,
        'scope':'n20 checks admission, symmetry, witness and rank; original norm comparison only n<=8'}

if __name__=='__main__':
    result=encode(run());Path(__file__).with_name('symmetric_uniform_family_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'sizes':[x['n'] for x in result['fixtures']],
        'last':result['fixtures'][-1]}))
