"""Polynomial exact-description compiler for maximal-profile inequality.

Input: two explicit rational-complex Choi matrices, same input dimension.
Output: equality verdict, or one rational separable pair with equal marginals
that separates every nonaffine operator-convex maximal f-divergence at once.
Historical novelty is unreviewed. No experimental sample bound is claimed.
"""
import argparse,json
from pathlib import Path
from exact import *

def different_word(e,f,basis):
    alphabet=[(e.apply(h),f.apply(h)) for h in basis]
    span=Span();initial=(e.omega,f.omega)
    span.insert(flat(initial[0])+flat(initial[1]));queue=[((),initial)]
    k=0
    while k<len(queue):
        word,(we,wf)=queue[k];k+=1
        delta=(tr(we)-tr(wf))/e.a
        if delta:return word,delta,len(queue)
        for i,(xe,xf) in enumerate(alphabet):
            pair=(mul(mul(we,e.oinv),xe),mul(mul(wf,f.oinv),xf))
            if span.insert(flat(pair[0])+flat(pair[1])):queue.append((word+(i,),pair))
    return None,Q(),len(queue)

def word_delta(e,f,basis,word):
    z=[]
    for channel in [e,f]:
        w=channel.omega
        for i in word:w=mul(mul(w,channel.oinv),channel.apply(basis[i]))
        z.append(tr(w)/channel.a)
    return z[0]-z[1]

def edge(r,i,j,phase=1):
    k=zero(r);k[i][j]=q(phase);k[j][i]=q(phase).conj();return k

def product_mixture(a,r,terms):
    mass=sum((abs(c) for c,h,k in terms),F(0))
    if mass>1:raise ValueError('Mixture budget exceeded')
    result=[{'weight':str(1-mass),'left':out(scale(F(1,a),eye(a))),'right':out(scale(F(1,r),eye(r)))}]
    for c,h,k in terms:
        if not c:continue
        sign=1 if c>0 else -1
        if h==eye(a):
            result.append({'weight':str(abs(c)),'left':out(scale(F(1,a),eye(a))),
              'right':out(scale(F(1,r),add(eye(r),scale(sign,k))))})
        else:
            assert tr(h)==Q()
            for s in [1,-1]:
                result.append({'weight':str(abs(c)/2),'left':out(scale(F(1,a),add(eye(a),scale(s,h)))),
                  'right':out(scale(F(1,r),add(eye(r),scale(s*sign,k))))})
    return result

def compile_pair(eobj,fobj,forced_word=None):
    e,f=Channel(eobj),Channel(fobj)
    if e.a!=f.a:raise ValueError('Channels must have the same input space')
    a=e.a;basis,labels=hermitian_basis(a)
    word,delta,dimension=different_word(e,f,basis)
    if forced_word is not None:
        word=tuple(forced_word);delta=word_delta(e,f,basis,word)
        if not delta:raise ValueError('Forced word does not separate')
    meta={'input_dim':a,'effective_output_ranks':[e.rank,f.rank],'ambient_bound':e.rank**2+f.rank**2,
      'explored_dimension':dimension,'basis_labels':labels}
    if word is None:return {'status':'equal_maximal_profiles','metadata':meta}
    n=len(word)
    if n<2:raise AssertionError('TP implies agreement at lengths zero and one')
    middle=[basis[i] for i in word[1:-1]] if n>2 else [eye(a)]
    m=len(middle);r=m+2;spare=r-1
    d=max(abs(delta.re),abs(delta.im))
    phase=q(1) if abs(delta.re)>=abs(delta.im) else Q(F(0),F(1))
    t=d/F(2**(m+4));u0=F(1,8)
    L=zero(a*r);base_terms=[]
    for j,h in enumerate(middle):
        k=edge(r,j,j+1);L=add(L,kron(h,k));base_terms.append((-t,h,k))
    ka=edge(r,spare,0);kb=edge(r,spare,m,phase)
    ya=kron(basis[word[0]],ka);yb=kron(basis[word[-1]],kb)
    rho=scale(F(1,a*r),add(eye(a*r),scale(-t,L)))
    alternatives=[]
    for sign in [1,-1]:
        yy=add(ya,scale(sign,yb))
        sig0=add(rho,scale(u0/F(a*r),yy))
        ge=e.chi(sig0,rho,r)/(u0*u0);gf=f.chi(sig0,rho,r)/(u0*u0)
        alternatives.append((abs(ge-gf),sign,yy,ge,gf))
    diff,sign,yy,ge,gf=max(alternatives,key=lambda z:z[0])
    if diff<d*t**m/r:raise AssertionError('Path witness margin failed')
    total=ge+gf;u=diff/(16*total)
    sigma=add(rho,scale(u/F(a*r),yy))
    mu=u*u*diff/2
    sigma_terms=base_terms+[(u,basis[word[0]],ka),(sign*u,basis[word[-1]],kb)]
    certificate={'status':'different_maximal_profiles','metadata':meta,'reference_dim':r,
      'separating_word':list(word),'word_labels':[labels[i] for i in word],'moment_difference':delta.out(),
      'path_length':m,'identity_inserted':n==2,'phase':phase.out(),'component_magnitude':str(d),
      'path_parameter':str(t),'quadratic_probe_parameter':str(u0),'selected_sign':sign,
      'quadratic_coefficients':[str(ge),str(gf)],'coefficient_gap':str(diff),'coefficient_sum':str(total),
      'final_parameter':str(u),'orientation':'E>F' if ge>gf else 'F>E',
      'universal_normalized_margin':str(mu),'quadratic_margin_lower_bound':str(u*u*d*t**m/r),
      'relative_radius_bound':str(2*u),'rho':out(rho),'sigma':out(sigma),
      'rho_product_mixture':product_mixture(a,r,base_terms),
      'sigma_product_mixture':product_mixture(a,r,sigma_terms),
      'largest_state_entry_bits':max(max_bits(rho),max_bits(sigma)),
      'contract':'For every real nonaffine operator-convex f on (0,infinity), the oriented difference of maximal f-divergences is at least (f-second-derivative-at-1 / 2) times universal_normalized_margin. All channels act only on the first tensor factor.'}
    return certificate

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output');args=p.parse_args()
    obj=json.loads(Path(args.input).read_text())
    result=compile_pair(obj['E'],obj['F'])
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','reference_dim','orientation','largest_state_entry_bits'] if k in result}))
