"""All-sector, finite-N interval certificate for the executed quartic family.

This emitter specializes the report's general Schur/inertia construction to
the tridiagonal X/Z benchmark. It does not assert that all degree-four models
are tridiagonal. Sturm signs and eigenvalue brackets use exact rationals.
"""
import json,time
from pathlib import Path
from fractions import Fraction as Q
from math import comb
from decimal import Decimal as D
from entropy_bounds import DOWN,UP,NEAR,log_interval,floor_grid,ceil_grid
from polynomial_tools import decode_polynomial,combine
from certified_thermodynamics import point_value,dot

ROOT=Path(__file__).resolve().parent


def jacobi_data(N,L,Gamma,h):
    diagonal=[]
    for k in range(L+1):
        m=L-2*k
        quartic=Q(m**4-(6*N-8)*m*m+3*N*(N-2),N*(N-1)*(N-2)*(N-3))
        diagonal.append(-quartic-h*Q(m,N))
    off2=[Gamma*Gamma*Q(k*(L-k+1),N*N) for k in range(1,L+1)]
    return diagonal,off2


def sturm_count(diagonal,off2,x):
    previous=Q(1); current=diagonal[0]-x
    signs=[1]
    if current: signs.append(1 if current>0 else -1)
    for k in range(1,len(diagonal)):
        nxt=(diagonal[k]-x)*current-off2[k-1]*previous
        previous,current=current,nxt
        if current: signs.append(1 if current>0 else -1)
    return sum(a!=b for a,b in zip(signs,signs[1:])),(current==0)


def eigen_intervals(diagonal,off2,bound,tolerance):
    result=[]; calls=0
    for index in range(len(diagonal)):
        low=-bound; high=bound
        while high-low>tolerance:
            mid=(low+high)/2; count,root=sturm_count(diagonal,off2,mid); calls+=1
            if root and count==index:
                low=high=mid; break
            if count>index: high=mid
            else: low=mid
        result.append((low,high))
    return result,calls


def exp_interval(x):
    a=DOWN.divide(D(x.numerator),D(x.denominator))
    b=UP.divide(D(x.numerator),D(x.denominator))
    return Q(NEAR.next_minus(NEAR.exp(a))),Q(NEAR.next_plus(NEAR.exp(b)))


def finite_pressure(N,Gamma,h,beta,tolerance=Q(1,1000000)):
    start=time.perf_counter(); sectors=[]; terms=[]; calls=0
    bound=1+abs(Gamma)+abs(h)
    for L in range(N%2,N+1,2):
        diagonal,off2=jacobi_data(N,L,Gamma,h)
        assert all(x>0 for x in off2)
        intervals,ncalls=eigen_intervals(diagonal,off2,bound,tolerance)
        mult=comb(N,(N-L)//2)-(comb(N,(N-L)//2-1) if (N-L)//2 else 0)
        sectors.append({'twice_spin':L,'multiplicity':str(mult),
                        'energy_density_intervals':[[str(a),str(b)] for a,b in intervals]})
        terms.extend((a,b,mult) for a,b in intervals); calls+=ncalls
    assert sum(len(s['energy_density_intervals'])*int(s['multiplicity']) for s in sectors)==2**N
    shift=min(a for a,b,m in terms)
    if beta is None:
        low=shift; high=min(b for a,b,m in terms)
    else:
        zlo=Q(0); zhi=Q(0)
        for a,b,m in terms:
            el=exp_interval(-beta*N*(b-shift))[0]
            eh=exp_interval(-beta*N*(a-shift))[1]
            zlo+=m*el; zhi+=m*eh
        low=floor_grid(shift-log_interval(zhi)[1]/(beta*N))
        high=ceil_grid(shift-log_interval(zlo)[0]/(beta*N))
    return {'N':N,'beta':None if beta is None else str(beta),
            'Gamma':str(Gamma),'h':str(h),'free_energy_interval':[str(low),str(high)],
            'free_energy_interval_float':[float(low),float(high)],'sectors':sectors,
            'sturm_calls':calls,'seconds':time.perf_counter()-start}


def main():
    acquired=json.loads((ROOT/'ACQUISITION_CERTIFICATE.json').read_text())
    base=decode_polynomial(acquired['learned_polynomial'])
    assert base=={(0,0,4):Q(-1),(1,0,0):Q(-1,4)},'This emitter is specialized.'
    nu=Q(acquired['coefficient_l1_error'])
    decision=json.loads((ROOT/'DECISION_FINITE_TEMPERATURE.json').read_text())
    g,h=map(Q,decision['control']); beta=Q(2)
    result=finite_pressure(64,g+Q(1,4),h,beta)
    lo,hi=map(Q,result['free_energy_interval'])
    result['true_model_free_energy_interval']=[str(lo-nu),str(hi+nu)]
    points=[tuple(Q(x) for x in r) for r in decision['state_points']]
    weights=[Q(x) for x in decision['dual_weights']]
    p=combine(base,[{(1,0,0):Q(1)},{(0,0,1):Q(1)}],(g,h))
    upper=sum((w*point_value(p,r,beta)[1] for w,r in zip(weights,points)),Q(0))
    deficit=upper-lo+2*nu
    response=[sum((w*r[j] for w,r in zip(weights,points)),Q(0)) for j in [0,2]]
    result['product_mixture_free_energy_deficit_upper']=str(deficit)
    result['product_mixture_free_energy_deficit_upper_float']=float(deficit)
    result['product_mixture_response']=[str(x) for x in response]
    result['preparation_status']='Mathematical product-state mixture recipe only; no physical preparation performed. Finite-N entropy concavity certifies the stated upper bound.'
    (ROOT/'FINITE_N_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['N','free_energy_interval_float','sturm_calls','seconds',
                                         'product_mixture_free_energy_deficit_upper_float']},indent=2),flush=True)


if __name__=='__main__': main()
