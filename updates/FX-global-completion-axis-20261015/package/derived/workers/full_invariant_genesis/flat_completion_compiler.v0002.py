"""Exact sufficient compiler; a failed admission check never means not QC."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sympy as s

HERE=Path(__file__).resolve().parent
a,b,c,d=av=s.symbols('a b c d',real=True)
u=a*a+c*c; v=b*b+d*d; w=a*b+c*d; j=a*d-b*c
H=s.expand((u+v-2*j)**2)
MON=(u*u,v*v,u*v,w*w,u*w,v*w,u*j,v*j,w*j)
I_POINT={a:1,b:0,c:0,d:1}


def rational(x):
    # A binary float may already have lost the caller's intended decimal.
    # The JSON loader below creates exact Rational values directly instead.
    if isinstance(x, bool) or not isinstance(x, (str, int, s.Rational)):
        raise ValueError('Scalars must be exact JSON numbers or rational strings; pre-parsed floats are not accepted.')
    try:
        value = s.Rational(x)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValueError('Every scalar must be a finite rational number.') from exc
    if not isinstance(value, s.Rational) or value.is_finite is not True:
        raise ValueError('Every scalar must be a finite rational number.')
    return value


def exact_json_loads(payload):
    def reject_constant(token):
        raise ValueError('Non-finite JSON constants are not accepted: '+token)
    return json.loads(payload, parse_float=s.Rational, parse_constant=reject_constant)


def matrix_json(mat):
    return [[str(entry) for entry in row] for row in mat.tolist()]


def analyse(data):
    if not isinstance(data, dict):
        raise ValueError('The certificate must be a JSON object.')
    if not isinstance(data.get('coefficients'), (list, tuple)) or len(data['coefficients'])!=9:
        raise ValueError('Exactly nine coefficients are required.')
    if 'lambda' not in data:
        raise ValueError('An exact support parameter lambda is required.')
    coeff=tuple(map(rational,data['coefficients']))
    lam=rational(data['lambda'])
    reserve=rational(data.get('reserve','1'))
    if reserve<0:
        raise ValueError('reserve must be nonnegative.')
    G=s.expand(sum(cc*mm for cc,mm in zip(coeff,MON)))
    Q=s.hessian(G,av).subs(I_POINT)/2-lam*s.hessian(j,av)/2
    result={
        'status':'UNRESOLVED_BY_THIS_COMPILER',
        'coefficients':list(map(str,coeff)),
        'lambda':str(lam),
        'reserve':str(reserve),
        'Q':matrix_json(Q),
        'scope':'Sufficient full-space certificate only; failure is not a non-quasiconvexity verdict.',
    }
    minors=[]
    for size in range(1,5):
        for inds in itertools.combinations(range(4),size):
            minor=s.cancel(Q.extract(inds,inds).det())
            minors.append({'indices':list(inds),'value':str(minor)})
            if minor<0:
                result['reason']='The supplied lambda gives a non-PSD quadratic form.'
                result['negative_principal_minor']=minors[-1]
                return result
    result['principal_minors']=minors
    kernel=Q.nullspace()
    rank=Q.rank()
    result['rank']=rank
    result['kernel_basis']=[list(map(str,n)) for n in kernel]
    d3=[[[s.diff(G,av[i],av[jj],av[kk]).subs(I_POINT)
          for kk in range(4)] for jj in range(4)] for i in range(4)]
    flat_checks=[]
    for ii,n1 in enumerate(kernel):
        for jj in range(ii,len(kernel)):
            n2=kernel[jj]
            for ee in range(4):
                val=s.cancel(sum(n1[vv]*n2[ww]*d3[vv][ww][ee]
                                 for vv in range(4) for ww in range(4)))
                flat_checks.append({'kernel_pair':[ii,jj],'coordinate':ee,'value':str(val)})
                if val!=0:
                    result['reason']='Cubic flatness fails on the supplied quadratic kernel.'
                    result['failed_flatness']=flat_checks[-1]
                    return result
    result['flatness_checks']=flat_checks
    if rank==0:
        h_coeff=G.coeff(a,4)
        assert s.expand(G-h_coeff*H)==0, 'Invariant zero-rank flatness reconstruction failed.'
        core_alpha=max(s.Integer(0),-h_coeff)
        result.update({
            'status':'ADMITTED',
            'case':'zero-rank: G is an exact multiple of H',
            'H_coefficient':str(h_coeff),
            'sufficient_alpha':str(core_alpha),
            'output_alpha':str(core_alpha+reserve),
            'gradient_L4_margin':str(s.Rational(4,1875)*reserve),
        })
        return result
    t=s.symbols('t')
    generating=s.Poly((s.eye(4)+t*Q).det(),t)
    er=generating.coeff_monomial(t**rank)
    er_prev=generating.coeff_monomial(t**(rank-1))
    assert er>0 and er_prev>0
    kappa=s.cancel(er/er_prev)
    M=sum(abs(cc) for cc in s.Poly(G,av).coeffs())
    assert M>0
    core_alpha=s.cancel(401296*M*M/kappa+s.Rational(9391,4)*M)
    result.update({
        'status':'ADMITTED',
        'case':'positive-rank degenerate-flat completion',
        'kappa':str(kappa),
        'elementary_symmetric_rank':str(er),
        'elementary_symmetric_previous':str(er_prev),
        'tensor_bound_M':str(M),
        'sufficient_alpha':str(core_alpha),
        'output_alpha':str(core_alpha+reserve),
        'gradient_L4_margin':str(s.Rational(4,1875)*reserve),
        'contract':'Every affine background, bounded planar Lipschitz domain, and W_0^(1,4) perturbation; also periodic gradients.',
    })
    return result


def family(k,ell,m,lam=None):
    if lam is None:
        lam=3*rational(ell)
    return {'coefficients':['0',str(m),'0',str(k),'0','0','0',str(ell),'0'],
            'lambda':str(lam),'reserve':'1'}


def self_check():
    checks=[]
    non_shear=analyse(family('1','-1','3/4'))
    assert non_shear['status']=='ADMITTED'
    assert non_shear['rank']==3
    assert non_shear['kernel_basis']==[['1','0','0','0']]
    # On this block-diagonal stratum, e3/e2 is exactly the harmonic lower
    # bound used in REPORT.md.
    assert non_shear['kappa']=='3/7'
    assert non_shear['sufficient_alpha']=='1359900751/12'
    checks.append('new acoustic-contact stratum admitted with exact one-dimensional rank-one kernel')
    for name,args in [('L_zero',('1','-1','1/2')),
                      ('D_zero',('1','1','1')),
                      ('w_square',('1','0','0'))]:
        rr=analyse(family(*args))
        assert rr['status']=='UNRESOLVED_BY_THIS_COMPILER'
        assert 'failed_flatness' in rr
        checks.append(name+' fails exact cubic flatness, without inferring non-QC from compiler failure')
    radial=analyse({'coefficients':['1','1','2','0','0','0','0','0','0'],'lambda':'0'})
    assert radial['status']=='ADMITTED' and radial['rank']==4
    assert radial['kappa']=='6/5'
    checks.append('full positive quadratic support case admits with exact eigenvalue-free kappa 6/5')
    hvec=[1,1,6,-4,0,0,-4,-4,0]
    negative_h=analyse({'coefficients':[str(-7*vv) for vv in hvec],'lambda':'0'})
    assert negative_h['status']=='ADMITTED' and negative_h['rank']==0
    assert negative_h['H_coefficient']=='-7' and negative_h['sufficient_alpha']=='7'
    checks.append('zero-rank case reconstructs G=-7H and completes by alpha 7')
    fc=s.symbols('f0:9')
    F9=sum(cc*mm for cc,mm in zip(fc,MON))
    equations=[s.diff(F9,*trip).subs(I_POINT)
               for trip in itertools.combinations_with_replacement(av,3)]
    A=s.linear_eq_to_matrix(equations,fc)[0]
    assert A.rank()==8
    assert A*s.Matrix(hvec)==s.zeros(A.rows,1)
    checks.append('all zero-rank cubic-flat invariant quartics form exactly span H by rank-eight elimination')
    rr=s.symbols('r',real=True)
    aa=3*rr/(8*(rr+2)); bb=rr*(rr-1)/6
    Jr=aa*H+bb*u*u+j*j+rr*u*j
    Kr=s.Matrix((1,0,0,-rr-1))
    cubic=sum(s.diff(Jr,av[ii],av[jj],av[kk]).subs(I_POINT)*Kr[ii]*Kr[jj]*Kr[kk]
              for ii in range(4) for jj in range(4) for kk in range(4))/24
    assert s.cancel(cubic+rr*(rr+2)/12)==0
    checks.append('sharp inherited J_r has exact nonflat cubic -r(r+2)/12')
    r=s.Rational(-5,2); al=s.Rational(15,8); be=s.Rational(35,24)
    old=analyse({'coefficients':list(map(str,[al+be,al,6*al+1,-4*al-1,0,0,-4*al+r,-4*al,0])),
                 'lambda':str(r+2)})
    assert old['status']=='UNRESOLVED_BY_THIS_COMPILER'
    assert old['rank']==2 and 'failed_flatness' in old
    checks.append('known inherited QC J_-5/2 is outside this sufficient compiler, proving the predicate is not necessary')
    # General symbolic proof ingredients beyond the concrete fixtures.
    M,kappa=s.symbols('M kappa',positive=True)
    A0=2592*M*M/kappa+8*M
    B0=512*M*M/kappa+3*M
    astar=401296*M*M/kappa+s.Rational(9391,4)*M
    assert s.expand(astar-A0/2-5*s.Rational(625,4)*B0)==0
    checks.append('general Taylor completion constant is an exact identity')
    assert s.hessian(H,av).subs(I_POINT)==s.zeros(4)
    assert all(s.diff(H,*trip).subs(I_POINT)==0
               for trip in itertools.combinations_with_replacement(av,3))
    checks.append('full-space admission predicate is unchanged by adding arbitrary H')
    decimal_literal='{"coefficients":[0,0.75,0,1.00000000000000000001,0,0,0,-1,0],"lambda":-3,"reserve":0}'
    decimal=analyse(exact_json_loads(decimal_literal))
    decimal_exact=s.Rational(100000000000000000001,100000000000000000000)
    assert decimal['status']=='ADMITTED'
    assert rational(decimal['coefficients'][3])==decimal_exact and decimal_exact!=1
    assert decimal['coefficients'][1]=='3/4'
    checks.append('JSON decimal 1.00000000000000000001 is preserved exactly through analyse, without binary rounding')
    scientific_literal='{"coefficients":[-7e0,-7e0,-4.2e1,2.8e1,0,0,2.8e1,2.8e1,0],"lambda":0e0,"reserve":1.234567890123456789e-23}'
    scientific=analyse(exact_json_loads(scientific_literal))
    scientific_exact=s.Rational(1234567890123456789,10**41)
    assert scientific['status']=='ADMITTED' and scientific['H_coefficient']=='-7'
    assert rational(scientific['reserve'])==scientific_exact
    assert rational(scientific['output_alpha'])==7+scientific_exact
    checks.append('JSON scientific notation preserves all decimal digits and the exact negative H coefficients')
    invalid_inputs=[
        ('negative reserve',lambda:analyse({**family('1','-1','3/4'),'reserve':-1})),
        ('binary float',lambda:rational(1.0)),
        ('SymPy float',lambda:rational(s.Float('1.01'))),
        ('boolean',lambda:rational(True)),
        ('non-rational string',lambda:rational('not-a-rational')),
        ('zero denominator',lambda:rational('1/0')),
        ('missing lambda',lambda:analyse({'coefficients':[0]*9})),
        ('wrong coefficient count',lambda:analyse({'coefficients':[0]*8,'lambda':0})),
        ('wrong top-level type',lambda:analyse([])),
    ]
    for token in ('NaN','Infinity','-Infinity'):
        invalid_inputs.append(('nonfinite '+token,
                               lambda token=token:exact_json_loads('{"lambda":'+token+'}')))
    invalid_rejections=[]
    for label,operation in invalid_inputs:
        try:
            operation()
        except ValueError:
            invalid_rejections.append(label)
        else:
            raise AssertionError('Invalid input accepted: '+label)
    checks.append('all twelve invalid fixtures, including negative reserve, nonfinite or inexact scalars, and invalid shapes, are rejected')
    cert={
        'status':'PASS',
        'receipt_version':2,
        'scope':'Exact sufficient-compiler logic and algebraic identities; the analytic theorem requires GENERAL_FLAT_COMPLETION.md.',
        'checks':checks,
        'check_count':len(checks),
        'new_stratum_certificate':non_shear,
        'known_QC_not_admitted':old,
        'exact_parser_regressions':{
            'decimal_literal':decimal_literal,
            'decimal_coefficient':str(decimal_exact),
            'scientific_literal':scientific_literal,
            'scientific_reserve':str(scientific_exact),
            'invalid_rejections':invalid_rejections,
        },
        'proof_sha256':hashlib.sha256((HERE/'GENERAL_FLAT_COMPLETION.md').read_bytes()).hexdigest(),
        'compiler_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'sympy_version':s.__version__,
    }
    path=HERE/'GENERAL_COMPILER_RECEIPT.json'
    path.write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps({'status':'PASS','check_count':len(checks),'receipt':str(path)},indent=2))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--self-check',action='store_true')
    args=parser.parse_args()
    if args.self_check:
        self_check()
        return
    if args.input is None:
        parser.error('--input certificate.json or --self-check is required')
    try:
        result=analyse(exact_json_loads(args.input.read_text()))
    except (ValueError, TypeError, KeyError) as exc:
        parser.error(str(exc))
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered,end='')


if __name__=='__main__':
    main()
