"""Check saved outputs without running the Galerkin search/iteration history.

The uniform convergence theorem is analytic. These checks validate only the
listed finite identities and the explicit infinite-series tail certificates.
"""
import json
from pathlib import Path
from exact_response import Q, StepField, product, bases, combine, mesh, certificate, inverse, serializable

ROOT=Path(__file__).resolve().parent


def load(name):
    def convert(v):
        if isinstance(v,str) and '/' in v:
            try:return Q(v)
            except (ValueError,ZeroDivisionError):pass
        if isinstance(v,list):return [convert(x) for x in v]
        if isinstance(v,dict):return {k:convert(x) for k,x in v.items()}
        return v
    return convert(json.loads((ROOT/name).read_text()))


def verify_trial(record,a,f,e,true_minimum):
    level=record['mesh_level']
    g,h,ids=bases(a.d,level)
    assert record['dimension']==a.d
    assert serializable(ids)==record['flux_basis_ids']
    assert record['epsilon']>0
    assert record['gap']==record['upper']-record['lower']
    cells=len(mesh(a.d,level))
    ef=combine(g,record['potential_coefficients'],e,cells)
    bf=combine(h,record['flux_coefficients'],[Q(0)]*a.d,cells)
    assert [list(v) for v in ef]==record['electric_field']
    assert [list(v) for v in bf]==record['conserved_flux']
    c=StepField(a.d,a.level,{box:inverse(v) for box,v in a.values.items()})
    exact=certificate(a,c,f,e,level,ef,bf)
    assert exact['lower']<=true_minimum<=exact['upper']
    assert record['lower']<=exact['lower']
    assert exact['upper']<=record['upper']
    assert 0<=record['gap']<=record['epsilon']**2
    # Each side separately equals the corresponding squared weighted error.
    return dict(primal_squared_error=exact['upper']-true_minimum,
                flux_squared_error=true_minimum-exact['lower'],
                exact_gap=exact['gap'],advertised_gap=record['gap'])


def frac_tree(v):
    if isinstance(v,Q):return str(v)
    if isinstance(v,list):return [frac_tree(x) for x in v]
    if isinstance(v,dict):return {k:frac_tree(x) for k,x in v.items()}
    return v


def main():
    a=StepField(2,1,{p:[[Q(1+p[0]),Q(0)],[Q(0),Q(1+p[0])]]
                      for p in product(range(2),repeat=2)})
    zero=StepField(2,0,{(0,0):[Q(0),Q(0)]})
    finite=verify_trial(load('FINITE_GRID_CERTIFICATE.json'),a,zero,[Q(1),Q(0)],Q(4,3))
    a2=StepField(2,0,{(0,0):[[Q(2),Q(1)],[Q(1),Q(2)]]})
    f2=StepField(2,1,{p:([Q(1),Q(2)] if p[0]==0 else [Q(-1),Q(1)])
                      for p in product(range(2),repeat=2)})
    forced=verify_trial(load('FORCED_PROBLEM_CERTIFICATE.json'),a2,f2,[Q(1,2),Q(0)],Q(0))
    r=load('INVERSE_FILTER_CERTIFICATE.json')
    actual=max(sum((abs(r['exact_inverse'][i][j]-r['inverse_approximant'][i][j])
                    for j in range(2)),Q(0)) for i in range(2))
    assert actual==r['actual_operator_error_upper']<=r['certified_L1_error']<=Q(1,256)

    v=load('UNBOUNDED_LAMINATE_CERTIFICATE.json')
    j=v['truncation_index']
    ap=ip=Q(0)
    for i in range(1,j+1):
        a_i=Q(i) if i%2 else Q(1,i)
        ap+=Q(1,2**i)*a_i
        ip+=Q(1,2**i)/a_i
    assert ap==v['prefix_a'] and ip==v['prefix_inverse_a']
    mass=Q(1,2**j)
    odd_sum_tail=Q(10,9)-sum((Q(i,2**i) for i in range(1,j+1,2)),Q(0))
    even_sum_tail=Q(8,9)-sum((Q(i,2**i) for i in range(2,j+1,2)),Q(0))
    odd_mass_tail=Q(2,3)-sum((Q(1,2**i) for i in range(1,j+1,2)),Q(0))
    even_mass_tail=Q(1,3)-sum((Q(1,2**i) for i in range(2,j+1,2)),Q(0))
    ta=odd_sum_tail+even_mass_tail/(j+1)
    ti=even_sum_tail+odd_mass_tail/(j+1)
    assert ta==v['tail_a_upper'] and ti==v['tail_inverse_a_upper']
    h=1/(ip+mass)
    assert v['tensor_approximation']==[[h,Q(0)],[Q(0),ap+mass]]
    assert v['tensor_operator_error_upper']==Q(1,10**6)
    lo1=2*h-h*h*(ip+ti);up1=h*h*(ip+ta)
    lo2=ap+2*mass-ti;up2=ap+ta
    assert (lo1,up1)==(v['first_loading']['lower'],v['first_loading']['upper'])
    assert (lo2,up2)==(v['second_loading']['lower'],v['second_loading']['upper'])
    assert 0<=up1-lo1<=Q(1,10**12)/16
    assert 0<=up2-lo2<=Q(1,10**12)/16
    # Independently tighter reciprocal-mean interval using twenty more strips.
    jref=j+20
    inv_ref=sum((Q(1,2**i)/(Q(i) if i%2 else Q(1,i))
                 for i in range(1,jref+1)),Q(0))
    even_ref=Q(8,9)-sum((Q(i,2**i) for i in range(2,jref+1,2)),Q(0))
    odd_ref=Q(2,3)-sum((Q(1,2**i) for i in range(1,jref+1,2)),Q(0))
    href_lower=1/(inv_ref+even_ref+odd_ref/(jref+1))
    href_upper=1/(inv_ref+even_ref)
    assert lo1<=href_lower<=href_upper<=up1
    report=dict(all_checks_passed=True,
        scope='Finite rational certificates and explicit tail bounds; not empirical proof of the universal theorem',
        finite_grid=finite,forced_problem=forced,
        inverse_filter_bound_valid=True,unbounded_laminate_bound_valid=True,
        laminate_reference_interval=[href_lower,href_upper],
        laminate_display=dict(first_interval=[float(lo1),float(up1)],
            second_interval=[float(lo2),float(up2)],
            first_gap=float(up1-lo1),second_gap=float(up2-lo2),
            tensor_operator_error=1e-6))
    (ROOT/'VERIFICATION_RESULTS.json').write_text(json.dumps(frac_tree(report),indent=2)+'\n')
    print(json.dumps(dict(all_checks_passed=True,laminate=report['laminate_display']),indent=2))


if __name__=='__main__':main()
