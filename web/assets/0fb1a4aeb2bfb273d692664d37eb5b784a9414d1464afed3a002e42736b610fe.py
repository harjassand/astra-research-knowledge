"""Exact checks of an all-size dense, conditioned approximation family."""
from frontier_rank_guard import *
from representation_compiler import det,minor,rank
from check_banded import determinant_table,table_prefix,encode
from pathlib import Path
from random import Random
import json,time

def family(n,epsilon):
    assert n%2==0 and n>=4
    q=n//2;bound=n*n+2*n
    delta=epsilon/(4*n*q*bound**(q-1)*2**n)
    d=[[C(Q((i+1)**j,n**n)) if i!=j else C(0) for j in range(n)] for i in range(n)]
    base=[[C(3 if i==j else int(1<=j-i<=2)) for j in range(n)] for i in range(n)]
    f=[[base[i][j]+delta*d[i][j] for j in range(n)] for i in range(n)]
    return f,delta,bound

def run():
    output=[];uniform_checks=[]
    for n in (4,6,8,20):
        start=time.monotonic();epsilon=Q(1,10);q=n//2
        f,delta,bound=family(n,epsilon)
        certificate=acquire_banded_certificate(f,2,0,q,epsilon)
        assert certificate['status']=='CERTIFIED'
        uniform=acquire_banded_uniform_certificate(f,2,0,q)
        assert uniform['status']=='UNIFORM_CERTIFIED'
        approximate=norm_uniform_accuracy(uniform,epsilon)
        assert approximate['branch']=='APPROXIMATE_WIDTH_BACKEND'
        assert approximate['norm']==certificate['norm_estimate']
        assert certificate['norm_estimate']>=1
        assert all(f[i][j] for i in range(n) for j in range(n) if i!=j)
        assert recognize_frontier(f)['width']==n-1
        cutrank=rank(minor(f,range(q,n),range(q)))
        assert cutrank==q
        assert certificate['operator_norm_upper_bound']<=bound
        assert certificate['eta_squared']<=n*n*delta*delta
        assert delta*n<=Q(1,16)
        witness=det(minor(certificate['H'],range(0,n,2),range(1,n,2)))
        assert witness.im==0 and witness.re>=1
        z_true=None;relative_error=None
        if n<=8:
            z_true=table_prefix(determinant_table(f),n)[q]
            relative_error=abs(certificate['norm_estimate']-z_true)/z_true
            assert relative_error<=epsilon
        if n==4:
            d2=uniform['amplitude_error_squared_bound'];z=uniform['norm_estimate']
            assert d2>0
            accuracy_bits=d2.denominator.bit_length()+z.numerator.bit_length()+10
            fine_epsilon=Q(1,1<<accuracy_bits)
            fine=norm_uniform_accuracy(uniform,fine_epsilon)
            assert fine['branch']=='EXACT_FINE_ACCURACY' and fine['norm']==z_true
            sample=sample_uniform_accuracy(uniform,fine_epsilon,Random(17).getrandbits)
            assert sample['status']=='SAMPLE' and sample['branch']=='EXACT_FINE_ACCURACY'
            assert det(minor(f,sample['up'],sample['down']))
            uniform_checks.append({'n':n,'accuracy_bits':accuracy_bits,
                'fine_count_branch':fine['branch'],'fine_sampler_branch':sample['branch'],
                'charged_bound_verified':Q(16**n)<fine_epsilon**(-8)})
        output.append({'n':n,'k':q,'status':certificate['status'],
            'uniform_status':uniform['status'],
            'norm_estimate':certificate['norm_estimate'],'delta':delta,
            'original_frontier':n-1,'middle_right_to_left_rank':cutrank,
            'compiled_frontier':certificate['counts']['extended_width'],
            'matrix_condition_upper_bound':Q(81,15),
            'approximate_norm_bit_length':certificate['norm_estimate'].numerator.bit_length()+certificate['norm_estimate'].denominator.bit_length(),
            'true_norm_small_comparator':z_true,'true_relative_error_small_comparator':relative_error,
            'backend_stats':certificate['counts']['stats'],
            'elapsed_seconds_diagnostic':time.monotonic()-start})
    return {'status':'PASS','fixtures':output,'uniform_accuracy_checks':uniform_checks,
            'scope':'all-size theorem is in proof; n20 checks admission, positive witness and exact cut-rank, not original norm'}

if __name__=='__main__':
    result=encode(run());Path(__file__).with_name('dense_admission_family_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'sizes':[x['n'] for x in result['fixtures']],
        'last':{k:result['fixtures'][-1][k] for k in ('n','k','status','original_frontier','middle_right_to_left_rank','compiled_frontier','approximate_norm_bit_length','elapsed_seconds_diagnostic')}}))
