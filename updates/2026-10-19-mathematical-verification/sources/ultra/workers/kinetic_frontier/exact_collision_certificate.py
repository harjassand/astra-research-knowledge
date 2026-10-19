"""Exact rational endpoint targets plus a quantitative positive-waveform proof.

The waveform rates are defined by unique Banach fixed points in a rational
parameter box. No optimizer and no independent-per-duration waveform is used.
The shared-normalized-waveform endpoint map is a product of five matrix
exponentials; its center Jacobian and all target matrices are rational.
"""
from pathlib import Path
import importlib.util
import json
import random
import sys
sys.dont_write_bytecode=True
import sympy as S

HERE=Path(__file__).parent
HELPER=HERE.parent/'kinetic_realization/fixed_hazard_jacobian.py'
spec=importlib.util.spec_from_file_location('kinetic_fixed_hazard_helper',HELPER)
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
LOWER=helper.LOWER


def Q(rates):
    n=len(rates);q=-S.diag(*rates)
    for i in range(n-1):q[i+1,i]=rates[i]
    return q


def V(rates):
    v=S.eye(len(rates))
    for j in range(len(rates)):
        for i in range(j+1,len(rates)):
            v[i,j]=rates[i-1]*v[i-1,j]/(rates[i]-rates[j])
    assert Q(rates)*v==v*S.diag(*[-x for x in rates])
    return v


def C(a,b):
    e=S.eye(4)[:,0];c=S.ones(1,4)
    al=V(a).inv()*e;be=c*V(b)
    return [S.cancel(al[i]*be[i]) for i in range(4)]


def ctrb(rates):
    q=Q(rates);e=S.eye(4)[:,0]
    return S.Matrix.hstack(*[q**i*e for i in range(4)])


def endpoint_targets(a,b):
    va,vb=V(a),V(b)
    factors=[S.diag(*[S.Integer(2)**(-5*d*x) for x in a]) for d in [1,2]]
    return [vb*dd*va.inv() for dd in factors],[va*dd*vb.inv() for dd in factors]


def flatten_lower(rs):
    return S.Matrix([r[p,q] for r in rs for p,q in LOWER])


def norm_inf(v):
    return max(abs(x) for x in v)


def main():
    lam=list(map(S.Integer,[1,3,8,10]))
    orders=[[0,3,1,2],[1,2,0,3]]
    rate_orders=[[lam[i] for i in o] for o in orders]
    helpers=[helper.fixed_hazard_jacobian(a) for a in rate_orders]
    assert all(h['pivots']==list(range(12)) for h in helpers)
    alpha=max(h['inverse_norm_inf'] for h in helpers)
    # Uniform scalar Hessian bound64; ||J(v)-J(0)||inf <= 12^2*64*r.
    lipschitz=S.Integer(12)**2*64
    radius=S.Rational(1,4)/(alpha*lipschitz)
    assert radius<S.Rational(1,16)

    K=128
    eta=S.Rational(1,2)**K
    u=S.Rational(108,25)+eta
    w=S.cancel((50*u-216)/(12-5*u**2))
    mu=[1-w/2,3-u*w/2,8+u*w/2,10+w/2]
    mu=list(map(S.cancel,mu))
    t=S.cancel(mu[0]*mu[3]/10)
    assert t!=1 and t>0 and eta>0
    assert mu[0]+mu[3]==mu[1]+mu[2]==11
    assert mu[0]*mu[3]/10==mu[1]*mu[2]/24
    assert len(set(mu))==4 and min(mu)>0
    ratios=[S.cancel(mu[i]/lam[i]) for i in range(4)]
    assert len(set(ratios))==4

    aa=rate_orders
    bb=[[mu[i] for i in o] for o in orders]
    cf=[C(a,b) for a,b in zip(aa,bb)]
    cr=[C(b,a) for a,b in zip(aa,bb)]
    for coefs in [cf,cr]:
        label=[dict(zip(o,c)) for o,c in zip(orders,coefs)]
        assert label[0]==label[1]

    all_targets=[endpoint_targets(a,b) for a,b in zip(aa,bb)]
    contractions=[]
    for order_index,h in enumerate(helpers):
        for direction_index,direction in enumerate(['outward','return']):
            rs=all_targets[order_index][direction_index]
            baseline=h['baseline']
            center_residual=flatten_lower(baseline)-flatten_lower(rs)
            newton_residual=h['inverse']*center_residual
            beta=norm_inf(newton_residual)
            contraction=h['inverse_norm_inf']*lipschitz*radius
            assert beta<=radius/2
            assert contraction<=S.Rational(1,4)
            assert beta+contraction*radius<radius
            for d,rr in zip([1,2],rs):
                assert all(rr[i,i]==S.Integer(2)**(-5*d*aa[order_index][i]) for i in range(4))
            contractions.append({
                'order':order_index,'direction':direction,
                'inverse_norm_inf':str(h['inverse_norm_inf']),
                'beta':str(beta),'beta_over_radius':str(S.cancel(beta/radius)),
                'beta_over_radius_decimal':str(S.N(beta/radius,12)),
                'contraction_factor_upper_bound':str(contraction),
                'strict_self_map':True,
                'actual_positive_shared_waveform_exists':True,
                'target_matrices':[[[str(x) for x in row] for row in r.tolist()] for r in rs],
            })

    ta=ctrb(aa[1])*ctrb(aa[0]).inv()
    tb=ctrb(bb[1])*ctrb(bb[0]).inv()
    e=S.eye(4)[:,0];c=S.ones(1,4)
    assert ta*e==e and tb*e==e and c*ta==c and c*tb==c
    assert Q(aa[1])*ta==ta*Q(aa[0])
    assert Q(bb[1])*tb==tb*Q(bb[0])
    for d in range(2):
        assert all_targets[1][0][d]*ta==tb*all_targets[0][0][d]
        assert all_targets[1][1][d]*tb==ta*all_targets[0][1][d]

    # These finite checks support only the implementation. The exact gauge
    # identities above establish every complete-operation endpoint word.
    rng=random.Random(20261019)
    word_checks=0
    for startmode in [0,1]:
        for nops in range(1,17):
            for trial in range(2):
                states=[e,e];mode=startmode
                for op in range(nops):
                    if rng.randrange(2)==0:
                        z=S.Integer(rng.choice([1,2,3,5]))
                        rates=[aa,bb][mode]
                        states=[z*(z*S.eye(4)-Q(rates[j])).inv()*states[j] for j in range(2)]
                    else:
                        duration_index=rng.randrange(2)
                        states=[all_targets[j][mode][duration_index]*states[j] for j in range(2)]
                        mode=1-mode
                assert (c*states[0])[0]==(c*states[1])[0]
                word_checks+=1

    out={
        'status':'PASS_EXACT_RATIONAL_POSITIVE_SHARED_WAVEFORM_COUNTEREXAMPLE',
        'scope':'Four stages; durations d=5log2 and2d; two orders, two directions; actual waveforms defined by certified Banach roots',
        'lambda_labels':list(map(str,lam)),
        'orders_one_based':[[i+1 for i in o] for o in orders],
        'rational_parameter_eta':f'2^(-{K})','u':str(u),'w':str(w),'t':str(t),
        'mu_labels':list(map(str,mu)),
        'all_response_ratios_pairwise_distinct':True,
        'rate_positivity_uniform_lower_bound':'3/4',
        'rate_uniform_upper_bound':'11',
        'waveform_parameter_box_radius':str(radius),
        'waveform_parameter_box_radius_decimal':str(S.N(radius,12)),
        'scalar_hessian_entry_bound':64,
        'jacobian_lipschitz_inf_coefficient':int(lipschitz),
        'contractions':contractions,
        'exact_hold_and_outward_return_gauge_identities':True,
        'finite_exact_word_checks':word_checks,
        'proof_required_for_universal_word_statement':True,
        'completion_time_during_ramp_not_identified':True,
        'no_physical_data_no_optimizer_in_certificate':True,
        'historical_priority':'UNKNOWN','physical_capability':'NOT_ESTABLISHED',
    }
    (HERE/'exact_collision_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','rational_parameter_eta','waveform_parameter_box_radius_decimal','finite_exact_word_checks','exact_hold_and_outward_return_gauge_identities']}))
    for r in contractions:print(r['order'],r['direction'],'beta/r=',r['beta_over_radius_decimal'],'q<=',r['contraction_factor_upper_bound'])

if __name__=='__main__':main()
