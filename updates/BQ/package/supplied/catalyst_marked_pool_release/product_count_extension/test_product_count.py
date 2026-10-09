import numpy as np
from marked_pool_partial import MarkedPoolLikelihood, full_cme_endpoint
from run_product_count import model


def close(a,b,rtol=2e-7,atol=2e-9):
    assert abs(a-b) <= atol+rtol*abs(b),(a,b,abs(a-b))


def main():
    Q,mu=model()
    # Product-only observation: exact query-specific cap agrees with the full
    # finite CME, and the independent candidate-clock lower interval encloses it.
    N,T,lam,koff,kcat=7,.9,1.6,.6,1.1
    full,full_dim,_=full_cme_endpoint(N,Q,0,3,lam,koff,kcat,mu,T,{3:1},direction='forward')
    cap,cap_dim,_=full_cme_endpoint(N,Q,0,3,lam,koff,kcat,mu,T,{3:1},direction='forward',monotone_cap=(3,1))
    assert full_dim > cap_dim
    close(cap,full,rtol=2e-12,atol=2e-13)
    marked=MarkedPoolLikelihood(N,Q,0,3,lam,koff,kcat,mu).solve(T,14,{3:1},rtol=2e-11,atol=1e-14)
    assert marked.lower <= full+1e-10 <= marked.lower+marked.poisson_tail+1e-10

    # General partial-state marginal exercises the multinomial lump of the
    # untouched pool; it is not special to the absorbing product category.
    obs={0:3}
    exact,_d,_m=full_cme_endpoint(N,Q,0,3,lam,koff,kcat,mu,T,obs,direction='forward')
    m=MarkedPoolLikelihood(N,Q,0,3,lam,koff,kcat,mu).solve(T,14,obs,rtol=2e-11,atol=1e-14)
    assert m.lower <= exact+1e-10 <= m.lower+m.poisson_tail+1e-10

    # No catalyst means an absorbing, initially empty product cannot appear.
    zero,_,_=full_cme_endpoint(N,Q,0,3,0.0,koff,kcat,mu,T,{3:1},direction='forward',monotone_cap=(3,1))
    assert zero == 0.0
    print({"status":"pass","full_vs_cap_product":abs(full-cap),"full_states":full_dim,"cap_states":cap_dim,"product_interval_tail":marked.poisson_tail,"partial_A_likelihood":exact,"partial_A_interval_tail":m.poisson_tail})

if __name__=='__main__': main()
