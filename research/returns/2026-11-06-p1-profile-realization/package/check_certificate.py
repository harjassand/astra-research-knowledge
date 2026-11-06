"""Read-only exact checker. Shares only the rational matrix kernel with compiler.

Checks physicality, equal marginals, explicit separability, the exact quadratic
coefficient gap and a sufficient uniform bound for every maximal f-divergence.
The integral representation proving the last implication is in the manuscript.
"""
import argparse,json
from pathlib import Path
from exact import *

def must(value,message):
    if not value:raise ValueError(message)

def check_mixture(items,target,a,r):
    result=zero(a*r);total=F(0)
    for term in items:
        p=F(term['weight']);x,y=mat(term['left']),mat(term['right'])
        must(p>=0,'Negative mixture weight')
        must(len(x)==a and all(len(z)==a for z in x),'Left factor shape')
        must(len(y)==r and all(len(z)==r for z in y),'Right factor shape')
        must(psd(x) and psd(y),'Nonpositive product factor')
        must(tr(x)==q(1) and tr(y)==q(1),'Product factor not normalized')
        result=add(result,scale(p,kron(x,y)));total+=p
    must(total==1,'Mixture weights do not sum to one')
    must(result==target,'Mixture reconstruction mismatch')

def check_pair(eobj,fobj,cert):
    e,f=Channel(eobj),Channel(fobj)
    must(e.a==f.a,'Different input dimensions')
    must(cert['status']=='different_maximal_profiles','Checker expects a witness')
    a=e.a;r=cert['reference_dim'];s=mat(cert['sigma']);rho=mat(cert['rho']);dim=a*r
    must(r>=1 and r<=e.rank**2+f.rank**2,'Reference bound')
    for state in [rho,s]:
        must(len(state)==dim and all(len(row)==dim for row in state),'State shape')
        must(tr(state)==q(1),'State not normalized')
        must(psd(add(state,scale(-F(1,2*dim),eye(dim)))),'Lower conditioning bound')
        must(psd(add(scale(F(3,2*dim),eye(dim)),scale(-1,state))),'Upper conditioning bound')
    must(partial(rho,a,r,'right')==scale(F(1,a),eye(a)),'First marginal not uniform')
    must(partial(s,a,r,'right')==partial(rho,a,r,'right'),'Different first marginals')
    must(partial(s,a,r,'left')==partial(rho,a,r,'left'),'Different reference marginals')
    check_mixture(cert['rho_product_mixture'],rho,a,r)
    check_mixture(cert['sigma_product_mixture'],s,a,r)
    u=F(cert['final_parameter']);eta=F(cert['relative_radius_bound']);mu=F(cert['universal_normalized_margin'])
    must(0<u<=F(1,16) and eta==2*u and eta<1,'Perturbation size')
    perturbation=add(s,scale(-1,rho))
    must(psd(add(scale(eta,rho),perturbation)) and psd(add(scale(eta,rho),scale(-1,perturbation))),'Relative order bound')
    ce,cf=e.chi(s,rho,r),f.chi(s,rho,r)
    ge,gf=ce/(u*u),cf/(u*u)
    must([str(ge),str(gf)]==cert['quadratic_coefficients'],'Incorrect quadratic coefficients')
    delta=abs(ge-gf);total=ge+gf
    must(delta>0 and total>0,'No quadratic separation')
    must(delta==F(cert['coefficient_gap']) and total==F(cert['coefficient_sum']),'Coefficient accounting')
    must(u==delta/(16*total),'Final parameter mismatch')
    must(mu==u*u*delta/2 and mu>0,'Margin mismatch')
    must((ge>gf)==(cert['orientation']=='E>F'),'Orientation mismatch')
    must(eta/(1-eta)*total<=delta/2,'Uniform f error not dominated')
    # These finitely many exact tests are regression checks, not the proof for all f.
    checks=[];direction=1 if ge>gf else -1
    for parameter in [F(0),F(1,8),F(1),F(8),F(10**6)]:
        vals=[]
        for ch in [e,f]:
            rr=ch.apply(rho,r);ss=ch.apply(s,r);dd=add(ss,scale(-1,rr))
            ii,_,_=pinv_psd(add(ss,scale(parameter,rr)))
            vals.append(real(tr(mul(mul(dd,ii),dd))))
        oriented=direction*(vals[0]-vals[1]);bound=mu/(1+parameter)
        must(oriented>=bound,'Integral-kernel regression failed')
        checks.append({'s':str(parameter),'oriented_difference':str(oriented),'bound':str(bound)})
    return {'passed':True,'reference_dimension':r,'state_dimension':dim,'quadratic_difference':str(direction*(ce-cf)),
      'universal_normalized_margin':str(mu),'rho_product_terms':len(cert['rho_product_mixture']),
      'sigma_product_terms':len(cert['sigma_product_mixture']),'kernel_regressions':checks,
      'review_status':'Exact implementation checks, with shared arithmetic kernel; not independent or formal scientific verification.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('certificate');p.add_argument('output');arg=p.parse_args()
    ob=json.loads(Path(arg.input).read_text());cert=json.loads(Path(arg.certificate).read_text())
    result=check_pair(ob['E'],ob['F'],cert);Path(arg.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['passed','reference_dimension','state_dimension','rho_product_terms','sigma_product_terms']}))
