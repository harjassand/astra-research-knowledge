"""Exact ordinary multistage comparator; not acquired capture chemistry."""
from fractions import Fraction as F
from pathlib import Path
import json

def hit(p,n,i):
    r=(1-p)/p
    return F(i,n) if p==F(1,2) else (1-r**i)/(1-r**n)

def mean_visits(p,n,i):
    return F(i*(n-i)) if p==F(1,2) else (n*hit(p,n,i)-i)/(2*p-1)

def solve_linear(p,n):
    # Independent rational tridiagonal elimination, not closed formulas.
    s=n-1; upper=[-p]*(s-1); diag=[F(1)]*s; lower=[-(1-p)]*(s-1)
    rh=[F(0)]*s; rh[-1]=p; rt=[F(1)]*s
    for j in range(1,s):
        x=lower[j-1]/diag[j-1]; diag[j]-=x*upper[j-1]
        rh[j]-=x*rh[j-1]; rt[j]-=x*rt[j-1]
    hs=[F(0)]*s; ts=[F(0)]*s; hs[-1]=rh[-1]/diag[-1]; ts[-1]=rt[-1]/diag[-1]
    for j in range(s-2,-1,-1):
        hs[j]=(rh[j]-upper[j]*hs[j+1])/diag[j]
        ts[j]=(rt[j]-upper[j]*ts[j+1])/diag[j]
    return hs,ts

def record(x): return {'rational':str(x),'decimal':float(x)}

def main():
    # rho=133/103 is illustrative. Bulk diffusion does NOT acquire release rates.
    pl=F(27,50); pnlo,pnhi=F(451284,10**6),F(451285,10**6)
    assert pnlo**103 < pl**133 < pnhi**103
    n,i=90,15; hl=hit(pl,n,i); hnhi=hit(pnhi,n,i); source_n=F(10000)
    purity=hl/(hl+source_n*hnhi)
    # For pn<1/2, E visits=(i-n*h)/(1-2*pn)<=i/(1-2*pnhi).
    nv=F(i)/(1-2*pnhi); lv=mean_visits(pl,n,i)
    gross=source_n*nv/hl; total=(source_n*nv+lv)/hl
    assert hl>F(9,10) and purity>F(99,100) and gross<1700000
    checks=[]
    for p in (F(1,3),F(1,2),pl,pnhi):
        hs,ts=solve_linear(p,9)
        assert all(x==hit(p,9,j) for j,x in enumerate(hs,1))
        assert all(x==mean_visits(p,9,j) for j,x in enumerate(ts,1))
        checks.append({'p':str(p),'states':10,'all_hitting_and_visit_equations':'PASS'})
    result={'scope':'ideal ordinary 89-stage wash cascade; not physical acquisition',
      'physical_capture_release_ratio_acquired':False,
      'hardware_or_full_cycle_advantage_established':False,
      'right_endpoint':n,'active_stages':n-1,'feed_stage':i,
      'initial_background_per_target':str(source_n),
      'target_right_probability':str(pl),
      'background_right_probability_enclosure':[str(pnlo),str(pnhi)],
      'release_ratio_enclosure_verified_by_integer_powers':True,
      'target_recovery':record(hl),'background_product_fraction_upper':record(hnhi),
      'product_target_purity_lower':record(purity),
      'background_stage_visits_per_feed_background_upper':record(nv),
      'target_stage_visits_per_feed_target':record(lv),
      'gross_background_captures_per_recovered_target_upper':record(gross),
      'all_stage_captures_per_recovered_target_upper':record(total),
      'independent_finite_chain_checks':checks,
      'missing_interfaces':['many independently routed inventories and beds',
        'nonselective complete cohort capture and elution',
        'acquired first-order release contrast at actual loading',
        'water and solvent transport, dead volume, rebinding and mixing',
        'capacity, cycle time, work, regeneration and losses']}
    Path(__file__).with_name('RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in (
      'active_stages','target_recovery','product_target_purity_lower',
      'gross_background_captures_per_recovered_target_upper',
      'all_stage_captures_per_recovered_target_upper')}))

if __name__=='__main__':main()
