"""Exact finite-form restriction for the stored numerical matrices ONLY.

The numerical source traces are not verified enclosures of the physical
correlations. This Fraction LDL replay treats their saved binary64 entries
as exact dyadic data and proves an all-vector statement for those data.
It is NOT a physical transfer/operator/gap certificate.
"""
from fractions import Fraction as F
import pathlib,json,hashlib,time
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]

def sym(a):
    n=len(a)
    return [[(F(float(a[i,j]))+F(float(a[j,i])))/2 for j in range(n)]for i in range(n)]

def combine(terms):
    n=len(terms[0][1])
    return [[sum(F(c)*a[i][j]for c,a in terms)for j in range(n)]for i in range(n)]

def positive_ldl(a):
    n=len(a);l=[[F(int(i==j))for j in range(n)]for i in range(n)];d=[]
    for i in range(n):
        pivot=a[i][i]-sum(l[i][k]**2*d[k]for k in range(i))
        assert pivot>0,(i,pivot)
        d.append(pivot)
        for j in range(i+1,n):
            l[j][i]=(a[j][i]-sum(l[j][k]*l[i][k]*d[k]for k in range(i)))/pivot
    for i in range(n):
        for j in range(n):assert a[i][j]==sum(l[i][k]*d[k]*l[j][k]for k in range(min(i,j)+1))
    return d

def main():
    start=time.monotonic();path=ROOT/'results/triplet_matrices_beta3.npz';inp=np.load(path)
    g,h,m2=[sym(inp[k])for k in ['G_normalized','H_normalized','M2_normalized']]
    theta=294000;gamma=4700000000;rayleigh_upper=294200;eligible_lower=291900
    constraints={'G_positive':g,
                 'Rayleigh_below_294200':combine([(rayleigh_upper,g),(-1,h)]),
                 'residual_at_294000_exceeds_4point7e9':combine([(1,m2),(-2*theta,h),(theta*theta-gamma,g)])}
    witnesses={name:list(map(str,positive_ldl(matrix)))for name,matrix in constraints.items()}
    distance=max(theta-eligible_lower,rayleigh_upper-theta)
    floor=gamma-distance**2;assert floor==4695590000
    target_scalar=322706;target_loop=303344
    required_scalar=(target_scalar-rayleigh_upper)*(rayleigh_upper-eligible_lower)
    required_loop=(target_loop-rayleigh_upper)*(rayleigh_upper-eligible_lower)
    assert floor>required_scalar and floor>required_loop
    scan=json.loads((ROOT/'results/minres_scan.json').read_text())
    selected=next(r for r in scan['rows']if r['Gram_cutoff_relative']==1e-10)['best_variance']
    c=list(map(F,selected['candidate_coefficients_normalized_message_basis']))
    def quadratic(a):return sum(c[i]*c[j]*a[i][j]for i in range(len(c))for j in range(len(c)))
    dd=quadratic(g);rr=quadratic(h)/dd;vv=quadratic(m2)/dd-rr*rr
    assert dd>0 and vv>floor
    result={'status':'PASS_EXACT_RESTRICTION_FOR_STORED_NUMERICAL_FORMS_ONLY',
            'physical_source_forms_certified':False,'next_connected_input_acquired':False,
            'input_npz_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'symmetric_parts_of_binary64_entries_treated_as_exact_dyadic':True,
            'source_matrix_dimension':len(g),'all_LDL_pivots_strictly_positive':True,
            'exact_LDL_reconstruction_checked':True,'LDL_pivots':witnesses,
            'Rayleigh_upper':rayleigh_upper,'Temple_eligible_Rayleigh_lower_used':eligible_lower,
            'prescribed_shift_for_uniform_bound':theta,'squared_residual_strict_lower':gamma,
            'all_eligible_vectors_variance_strict_lower':floor,
            'favourable_rest_spectrum_bound_used':eligible_lower,
            'generous_scalar_target':target_scalar,'generous_loop_target':target_loop,
            'maximum_variance_allowance_scalar_target':required_scalar,
            'maximum_variance_allowance_loop_target':required_loop,
            'best_candidate_exact_dyadic_Rayleigh':str(rr),
            'best_candidate_exact_dyadic_variance':str(vv),
            'best_candidate_variance_float_minus_exact_dyadic_diagnostic':selected['variance']-float(vv),
            'seconds':time.monotonic()-start,
            'scope':'All-vector obstruction for the frozen numerical matrix pencil and current favourable deflated-count interface. No verified entrywise bound connects these forms to the exact physical source; no general-method impossibility or gap claim.'}
    (ROOT/'results/dyadic_span_replay.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k!='LDL_pivots'},indent=2))

if __name__=='__main__':main()
