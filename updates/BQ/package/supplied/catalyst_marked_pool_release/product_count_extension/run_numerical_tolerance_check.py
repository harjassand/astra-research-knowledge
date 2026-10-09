"""ODE tolerance stability evidence; explicitly not a rigorous solver bound."""
import json,os
import numpy as np
from run_product_count import model
from unique_mark_engine import UniqueMarkLikelihood
from marked_pool_partial import full_cme_endpoint


def main():
    Q,mu=model(); N,T,lam,koff,kcat,K=300,1.0,2.2,.55,1.3,12
    obs={3:1}
    exact,dim,_=full_cme_endpoint(N,Q,0,3,lam,koff,kcat,mu,T,obs,direction='forward',monotone_cap=(3,1))
    rows=[]
    for rtol in (1e-7,1e-9,1e-11,1e-13):
        atol=max(1e-16,rtol*1e-3)
        obj=UniqueMarkLikelihood(N,Q,0,3,lam,koff,kcat,mu)
        result=obj.solve(T,K,obs,rtol=rtol,atol=atol)
        rows.append({"rtol":rtol,"atol":atol,"lower":result.lower,"tail":result.poisson_tail,"tail_over_lower":result.poisson_tail/result.lower,"retained_mass":result.retained_mass,"states":result.dimension,"seconds":result.seconds,"difference_vs_query_specific_FSP":result.lower-exact})
    baseline=rows[-1]["lower"]
    for row in rows: row["difference_vs_tightest_rtol_run"]=row["lower"]-baseline
    payload={"scope":"Numerical stability only. The Poisson tail is the analytic state-pruning error for the exact ODE, not a rigorous enclosure of floating-point integration or expm errors.","model":{"N":N,"T":T,"lambda":lam,"koff":koff,"kcat":kcat,"K":K,"observation":obs},"query_specific_fsp":{"states":dim,"likelihood":exact},"runs":rows,"max_variation_across_tolerances":max(r["lower"] for r in rows)-min(r["lower"] for r in rows)}
    path=os.path.join(os.path.dirname(__file__),"numerical_tolerance_unique_mark.json")
    with open(path,'w') as f:json.dump(payload,f,indent=2)
    print(json.dumps(payload,indent=2))
if __name__=='__main__':main()
