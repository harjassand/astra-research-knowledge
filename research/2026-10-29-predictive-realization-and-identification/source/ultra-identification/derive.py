"""Exact analytic identification response; no producer imports or dynamics."""
from pathlib import Path
import json,time
from fractions import Fraction as F
import sympy as s

HERE=Path(__file__).resolve().parent


def main():
    start=time.perf_counter()
    u,c,b,z=s.symbols('u c b z',positive=True)
    Q=s.Matrix([[-(c+2),c+2,0],[u/2,-u,u/2],[0,c,-c]])
    D=s.diag(0,1,2);one=s.ones(3,1);w=s.Matrix([-1,0,1])
    p=s.Matrix([[0,1,0]])
    assert Q*one==s.zeros(3,1)
    A=Q-D
    assert A*one==-one-w
    assert A*w==-(c+2)*w
    # Consequently the entire vector of survival functions is independent
    # of u at baseline, not just the one reset's scalar function.
    a=c+2
    den0=(z+b)*(z+a)*(z+c+2*b)
    denu=z*z+(c+1+2*b)*z+b*(c+2)
    den=den0+u*denu
    lhs=s.factor((p*(z*s.eye(3)-Q+b*D).inv()*one)[0])
    delta=s.factor(lhs-1/(z+b))
    assert s.factor(delta-u*b*(b-1)/((z+b)*den))==0
    original=s.factor(lhs.subs(c,0))
    root_claim=1/(z+b)+b*u*(b-1)/((z+b)*(z+2*b)*(z*z+(2+u+b)*z+u+2*b))
    assert s.factor(original-root_claim)==0
    assert s.factor((p*(Q-b*D)**3*one)[0]-(-b**3+u*b*(b-1)))==0
    v=s.symbols('v',positive=True)
    distinct=s.factor(lhs-lhs.subs(u,v))
    expected=b*(b-1)*(u-v)*(z+a)*(z+c+2*b)/(den*(den0+v*denu))
    assert s.factor(distinct-expected)==0
    # c>0 gives an irreducible reversible path support for every u>0.
    pi=s.Matrix([[u/(2*(c+2)),1,u/(2*c)]])
    assert s.simplify(pi*Q)==s.zeros(1,3)
    for i,j in [(0,1),(1,2)]:assert s.simplify(pi[i]*Q[i,j]-pi[j]*Q[j,i])==0
    # A strictly positive intensity floor is obtained by D -> D+rho I.
    rho=s.symbols('rho',positive=True)
    assert s.simplify((z*s.eye(3)-Q+b*(D+rho*s.eye(3)))-((z+b*rho)*s.eye(3)-Q+b*D))==s.zeros(3,3)
    # The root same-support pair has a simple exact discounted reward gap.
    l1=s.factor(original.subs({u:1,b:s.Rational(1,2),z:1}))
    l2=s.factor(original.subs({u:2,b:s.Rational(1,2),z:1}))
    assert l1==s.Rational(17,26) and l2==s.Rational(11,17)
    assert l1-l2==s.Rational(3,442)
    # A deterministic horizon6 retains a strictly positive bounded-reward
    # gap: exp(-6)<1/400 from an EXACT positive Taylor lower polynomial.
    e6_lower=sum(F(6**k,s.factorial(k)) for k in range(18))
    assert e6_lower>400
    finite_gap=F(3,442)-F(1,400)
    assert finite_gap==F(379,88400)>0
    out={'status':'PASS exact symbolic/rational identification derivation',
         'root_resolvent_identity':True,'same_support_u1_u2_counterexample':True,
         'all_baseline_initial_distributions_same_for_each_u':True,
         'irreducible_reversible_extension_c_positive':True,
         'positive_intensity_floor_extension':True,
         'original_discounted_survival_rewards_u1_u2':[str(l1),str(l2)],
         'exact_discounted_reward_gap':'3/442',
         'deterministic_horizon6_gap_lower':'379/88400',
         'exp6_positive_Taylor_lower':str(e6_lower),
         'wall_seconds':time.perf_counter()-start,
         'no_producer_imports':True,'no_simulations':True}
    (HERE/'EXACT_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
