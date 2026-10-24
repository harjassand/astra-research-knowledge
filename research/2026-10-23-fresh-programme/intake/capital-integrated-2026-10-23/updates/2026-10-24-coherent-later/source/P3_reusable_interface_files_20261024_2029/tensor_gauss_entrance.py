"""New positive Gauss entrance compiler; retains prior endpoint implementation.

Dependencies: the available tensor_separator_entrance.py and
pro3_gate_experiment.py.  Correlated posterior is a positive product mixture.
Its full-distribution error uses a rational derivative-norm bound, not a
configuration enumeration or an a posteriori reference discrepancy.
"""
from fractions import Fraction as F
from math import comb, factorial
import json
import time
from tensor_separator_entrance import Entrance, BinaryModule, expanded_reference
from pro3_gate_experiment import I, D, DOWN, UP


def derivative_bounds(modules,gamma,order=8):
    whole=[F(gamma)**d for d in range(order+1)]
    for m in modules:
        A=[[-m.alpha,m.alpha],[m.beta,-m.beta-m.kappa]]
        row=[m.beta/(m.alpha+m.beta),m.alpha/(m.alpha+m.beta)]
        local=[]
        for d in range(order+1):
            local.append(sum(abs(v) for v in row))
            row=[sum(row[k]*A[k][j] for k in range(2)) for j in range(2)]
        whole=[sum(F(comb(d,r))*whole[d-r]*local[r] for r in range(d+1))
               for d in range(order+1)]
    return whole


def nodes():
    zeta=I(F(6,5)).sqrt(); root30=I(30).sqrt()
    big=((3+2*zeta)/7).sqrt(); small=((3-2*zeta)/7).sqrt()
    wb=(18-root30)/72; ws=(18+root30)/72
    return [((1-big)/2,wb),((1-small)/2,ws),((1+small)/2,ws),((1+big)/2,wb)]


def compile_gauss(model,number_cells):
    h=model.t/number_cells; parts=[]
    for cell in range(number_cells):
        for z,w in nodes():
            u=(cell+z)*I(h)
            vv=model.vectors(u)
            coeff=I(h)*w*model.weight(u)
            rows_lo=[]; rows_hi=[]
            for i,(v0,v1) in enumerate(vv):
                if i==model.mark:
                    rate=I(model.modules[i].kappa)*v1
                    rows_lo.append((max(D(0),rate.lo),D(0)))
                    rows_hi.append((rate.hi,D(0)))
                else:
                    rows_lo.append((max(D(0),v0.lo),max(D(0),v1.lo)))
                    rows_hi.append((v0.hi,v1.hi))
            parts.append({'cl':coeff.lo,'cu':coeff.hi,
                          'rows_l':rows_lo,'rows_u':rows_hi})
    lower,upper=model.sums(parts)
    bound8=derivative_bounds(model.modules,model.gamma)[8]
    gauss=F(factorial(4)**4,9*factorial(8)**3)*model.t*h**8
    gauss*=model.gamma*model.modules[model.mark].kappa*bound8
    rounding=UP.subtract(upper.hi,lower.lo)
    delta=I(gauss)+I(rounding)
    epsilon=(delta/I(lower.lo)).hi
    return parts,lower,upper,delta,epsilon,gauss,rounding


def run(n,t,gamma,tolerance,check=False):
    modules=[BinaryModule(F(3,5)+F(i,100),F(2,5)+F(i%5,50),F(3,2)+F(i%3,10)) for i in range(n)]
    model=Entrance(modules,F(gamma),F(t),0)
    started=time.time(); cells=4
    while True:
        parts,lower,upper,delta,eps,ge,re=compile_gauss(model,cells)
        if eps<=I(tolerance).lo: break
        cells*=2
        if cells>4096: raise RuntimeError('Declared numerical budget insufficient')
    density_lower=DOWN.subtract(lower.lo,delta.hi)
    density_upper=UP.add(lower.hi,delta.hi)
    def moment(ones):
        val,_=model.sums(parts,ones)
        approx=val/lower
        return max(D(0),DOWN.subtract(approx.lo,eps)),min(D(1),UP.add(approx.hi,eps))
    m1=moment((1,)); m2=moment((2,)); p12=moment((1,2))
    covariance=[DOWN.subtract(p12[0],UP.multiply(m1[1],m2[1])),
                UP.subtract(p12[1],DOWN.multiply(m1[0],m2[0]))]
    result={'new_work':True,'modules':n,'configuration_count':str(2**(n+1)),
            'event_time':str(t),'gamma':str(gamma),'event_mark':0,
            'time_cells':cells,'positive_product_terms':len(parts),
            'entrance_density_interval':[str(density_lower),str(density_upper)],
            'unnormalized_entrance_L1_error_upper':str(delta.hi),
            'quadrature_error_upper':str(I(ge).hi),'outward_rounding_error_upper':str(re),
            'posterior_TV_upper':str(eps),'requested_posterior_TV':str(tolerance),
            'posterior_marginal_1_interval':[str(x) for x in m1],
            'posterior_marginal_2_interval':[str(x) for x in m2],
            'posterior_pair_probability_interval':[str(x) for x in p12],
            'posterior_covariance_interval':[str(x) for x in covariance],
            'elapsed_seconds':time.time()-started}
    if check:
        ref=expanded_reference(modules,F(gamma),F(t),0,[])
        ref.pop('maximum_signed_componentwise_violation')
        assert float(density_lower)<=ref['density']<=float(density_upper)
        assert float(covariance[0])<=ref['posterior_covariance_1_2']<=float(covariance[1])
        result['independent_expanded_reference']=ref
    return result


if __name__=='__main__':
    results=[run(3,F(2),F(7,10),F(1,10**9),True),
             run(24,F(3,2),F(7,10),F(1,10**7),False)]
    print(json.dumps(results,indent=2))
    with open('tensor_gauss_entrance_results.json','w') as f: json.dump(results,f,indent=2)
