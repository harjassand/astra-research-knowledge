import numpy as np
from marked_pool_partial import full_cme_endpoint
from unique_mark_engine import UniqueMarkLikelihood
from run_product_count import model


def main():
    Q,mu=model(); N,T,lam,koff,kcat=9,.8,1.7,.6,1.1
    # Product count is a catalyst-only event; compare product-only, a partial
    # non-product marginal, and a full endpoint vector against exact FSP.
    for obs,bobs in [({3:1},None),({0:4},None),((5,2,1,1),0)]:
        if isinstance(obs,tuple): assert sum(obs)+bobs==N
        exact,_,_=full_cme_endpoint(N,Q,0,3,lam,koff,kcat,mu,T,obs,
                                     observed_bound=bobs,direction='forward',
                                     monotone_cap=(3,1) if obs=={3:1} else None)
        r=UniqueMarkLikelihood(N,Q,0,3,lam,koff,kcat,mu).solve(
            T,12,obs,observed_bound=bobs,rtol=2e-11,atol=2e-14)
        assert r.lower-2e-10<=exact<=r.lower+r.poisson_tail+2e-10,(obs,r.lower,exact,r.poisson_tail)

    # Multi-catalyst valid joint endpoint, including b=2 and a nonvacuous
    # product output, independently checked by full count CME.
    q,N,C=3,16,2
    Q2=np.zeros((q,q))
    for i in range(q): Q2[i,(i+1)%q]+=.4;Q2[i,(i-1)%q]+=.2;Q2[i,i]-=.6
    mu2=np.array([1.,0.,0.]); obs2=(10,3,1); T2=.6; lam2=1.1; off2=.7; cat2=.9
    exact,_,_=full_cme_endpoint(N,Q2,0,1,lam2,off2,cat2,mu2,T2,obs2,2,catalysts=C)
    r=UniqueMarkLikelihood(N,Q2,0,1,lam2,off2,cat2,mu2,catalysts=C).solve(
        T2,12,obs2,observed_bound=2,rtol=2e-11,atol=2e-14)
    assert exact>0 and r.lower-2e-10<=exact<=r.lower+r.poisson_tail+2e-10
    print({"status":"pass","C2_exact":exact,"C2_unique_lower":r.lower,"C2_tail":r.poisson_tail,"C2_states":r.dimension})

if __name__=='__main__': main()
