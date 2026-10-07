"""Exact rational certificates for a supplied diagonal covariance-field table.
No Gaussian likelihood integration, matrix-log oracle, or scientific packages.
"""
from fractions import Fraction as F
import json, math, time, pathlib


def log_interval(x, eta=F(1, 2**36)):
    x=F(x)
    if x<=0: raise ValueError('strictly positive covariance eigenvalue required')
    z=x; k=0
    while z>=2: z/=2; k+=1
    while z<1: z*=2; k-=1
    target=eta/(abs(k)+1)
    def atanh_log(z):
        t=(z-1)/(z+1); s=F(0); power=t; n=0
        while True:
            s+=2*power/(2*n+1); n+=1; power*=t*t
            rem=2*power/((2*n+1)*(1-t*t))
            if rem<=target: return (s,s+rem,n)
    a,b,n1=atanh_log(z); c,d,n2=atanh_log(F(2))
    lo=a+(k*c if k>=0 else k*d)
    hi=b+(k*d if k>=0 else k*c)
    assert hi-lo<=eta
    return lo,hi,n1+n2


def square_interval(lo,hi):
    if lo<=0<=hi: return F(0),max(lo*lo,hi*hi)
    return min(lo*lo,hi*hi),max(lo*lo,hi*hi)


def certificate(weights, diagonal_table, saturation=F(1), eta=F(1,2**36)):
    weights=list(map(F,weights)); K=len(weights); m=len(diagonal_table[0])
    if sum(weights)!=1 or min(weights)<0: raise ValueError('invalid table law')
    if any(len(row)!=m for row in diagonal_table): raise ValueError('dimension mismatch')
    intervals=[]; terms=0
    for row in diagonal_table:
        out=[]
        for val in row:
            lo,hi,n=log_interval(F(val),eta); terms+=n; out.append((lo,hi))
        intervals.append(out)
    vlo=vhi=F(0)
    for a in range(K):
        for b in range(K):
            for i in range(m):
                lo=intervals[a][i][0]-intervals[b][i][1]
                hi=intervals[a][i][1]-intervals[b][i][0]
                qlo,qhi=square_interval(lo,hi)
                factor=weights[a]*weights[b]/2
                vlo+=factor*qlo; vhi+=factor*qhi
    info_upper=F(saturation)**2*vhi/24
    return {'variance_lower':str(vlo),'variance_upper':str(vhi),
        'scale_information_upper_nats':str(info_upper),
        'upper_float_for_display':float(info_upper),'states_read':K,'matrix_dimension':m,
        'model_scalar_entries_read':K*m+K,'atanh_terms':terms,
        'log_abs_interval_width_target':str(eta),
        'scope':'analytic upper certificate; actual mutual information was not numerically computed'}


def exact_integrand_identity(b,c,u):
    b,c,u=F(b),F(c),F(u); d=b-c
    if d==0: return True
    lhs=u*d*d/((1+b*u)**2*(1+c*u)**2)
    rhs=(b+c)*b/d/(1+b*u)-b/(1+b*u)**2-(b+c)*c/d/(1+c*u)-c/(1+c*u)**2
    return lhs==rhs


def main():
    start=time.perf_counter()
    weights=[F(1,4),F(1,2),F(1,4)]
    table=[[F(1,2),F(1),F(4)],[F(1),F(2),F(2)],[F(2),F(4),F(1)]]
    c=certificate(weights,table)
    fixtures=0
    for b in [F(1,8),F(1,2),F(1),F(2),F(8)]:
        for d in [F(1,3),F(1),F(3)]:
            for u in [F(0),F(1,7),F(1),F(7)]:
                assert exact_integrand_identity(b,d,u); fixtures+=1
    # Bounds for the scalar kernel, with sign-aware certified log intervals.
    kernel_checks=[]
    for k in range(1,17):
        ratio=F(2**k); tlo,thi,_=log_interval(ratio)
        a=(ratio+1)/(ratio-1)
        klo=a*tlo-2; khi=a*thi-2
        assert klo>=0 and khi<=tlo*tlo/6 and khi<=tlo
        kernel_checks.append({'ratio':str(ratio),'kernel_upper':str(khi),'log_lower':str(tlo)})
    # Controlled-dependence table: all modes see the same reference state.
    dependent=certificate([F(1,2),F(1,2)],[[F(1)]*8,[F(2)]*8])
    # A null mode is admitted exactly, outside the log theorem: its covariance is constant.
    null_covariance_note='Common nullspace can be removed; mismatched positive-probability nullspaces can give an infinite scale integral.'
    result={'table_certificate':c,'exact_partial_fraction_fixtures':fixtures,
        'kernel_interval_checks':kernel_checks,'dependent_eight_mode_table':dependent,
        'null_boundary':null_covariance_note,'elapsed_seconds':time.perf_counter()-start,
        'proof_scope':'finite exact algebra/interval certificates, not empirical MI or external theorem validation'}
    dest=pathlib.Path(__file__).with_name('log_covariance_checks.json')
    dest.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'certificate_upper_nats':c['upper_float_for_display'],
        'exact_fixtures':fixtures,'elapsed_seconds':result['elapsed_seconds'],'output':str(dest)},indent=2))

if __name__=='__main__': main()
