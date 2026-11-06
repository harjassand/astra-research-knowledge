"""Exact affine geometry and one uniform physical probe panel for a finite family.

All relations are affine (sum of contrast coefficients zero). The common
panel works for every nonaffine maximal operator-convex divergence, without
requesting an evaluator for f. The input consists of explicit rational Chois.
"""
import argparse,json
from pathlib import Path
from exact import *
from compile_witness import edge,product_mixture

def rref(rows,width=None):
    z=[[q(x) for x in row] for row in rows];w=width if width is not None else len(z[0]);piv=[];h=0
    for j in range(w):
        i=next((i for i in range(h,len(z)) if z[i][j]),None)
        if i is None:continue
        z[h],z[i]=z[i],z[h];d=z[h][j];z[h]=[x/d for x in z[h]]
        for i in range(len(z)):
            if i!=h and z[i][j]:
                d=z[i][j];z[i]=[x-d*y for x,y in zip(z[i],z[h])]
        piv.append(j);h+=1
        if h==len(z):break
    return z[:h],piv

def nullspace(rows,k):
    rr,piv=rref(rows,k);free=[j for j in range(k) if j not in piv];res=[]
    for j in free:
        v=[F(0)]*k;v[j]=F(1)
        for row,p in zip(rr,piv):v[p]=-real(row[j])
        res.append(v)
    return res

def family_words(channels,basis):
    letters=[[ch.apply(h) for h in basis] for ch in channels]
    initial=[ch.omega for ch in channels];span=Span();span.insert(sum((flat(x) for x in initial),[]))
    queue=[((),initial)];head=0
    while head<len(queue):
        word,values=queue[head];head+=1
        for i in range(len(basis)):
            nxt=[mul(mul(x,ch.oinv),ls[i]) for x,ch,ls in zip(values,channels,letters)]
            if span.insert(sum((flat(x) for x in nxt),[])):queue.append((word+(i,),nxt))
    moments=[[tr(x)/channels[0].a for x in values] for word,values in queue]
    return queue,moments

def dot(c,v):return sum((q(x)*y for x,y in zip(c,v)),Q())

def contrast_probe(channels,basis,word,delta,c):
    a=channels[0].a;n=len(word)
    if n<2:raise AssertionError('Affine contrasts of TP channels vanish at lengths zero and one')
    middle=[basis[i] for i in word[1:-1]] if n>2 else [eye(a)]
    m=len(middle);r=m+2;spare=r-1
    d=max(abs(delta.re),abs(delta.im));C=sum(abs(x) for x in c)
    phase=q(1) if abs(delta.re)>=abs(delta.im) else Q(0,F(1))
    t=d/(C*2**(m+4));u0=F(1,8);L=zero(a*r);base=[]
    for j,h in enumerate(middle):
        ke=edge(r,j,j+1);L=add(L,kron(h,ke));base.append((-t,h,ke))
    ka=edge(r,spare,0);kb=edge(r,spare,m,phase)
    ya=kron(basis[word[0]],ka);yb=kron(basis[word[-1]],kb)
    rho=scale(F(1,a*r),add(eye(a*r),scale(-t,L)))
    options=[]
    for sign in [1,-1]:
        yy=add(ya,scale(sign,yb));ss=add(rho,scale(u0/F(a*r),yy))
        gg=[ch.chi(ss,rho,r)/(u0*u0) for ch in channels]
        delta_g=sum(x*y for x,y in zip(c,gg));options.append((abs(delta_g),sign,yy,gg,delta_g))
    gap,sign,yy,gg,delta_g=max(options,key=lambda z:z[0])
    if gap<d*t**m/r:raise AssertionError('Weighted path margin failed')
    record={'reference_dim':r,'separating_word':list(word),'moment_contrast':delta.out(),
       'contrast':[str(x) for x in c],'contrast_norm':str(C),'component_magnitude':str(d),
       'identity_inserted':n==2,'path_length':m,'path_parameter':str(t),'phase':phase.out(),
       'selected_sign':sign,'quadratic_coefficients':[str(x) for x in gg],
       'quadratic_contrast':str(delta_g),'quadratic_contrast_lower_bound':str(d*t**m/r)}
    return record,rho,yy,base,[(basis[word[0]],ka),(basis[word[-1]],kb)]

def compile_panel(objects):
    if not objects:raise ValueError('At least one channel is required')
    channels=[Channel(x) for x in objects];a=channels[0].a;k=len(channels)
    if any(ch.a!=a for ch in channels):raise ValueError('Common input dimension required')
    basis,labels=hermitian_basis(a);queue,moments=family_words(channels,basis)
    G=[[F(1)]*k];probes=[]
    while True:
        found=None
        for c in nullspace(G,k):
            for (word,_),v in zip(queue,moments):
                delta=dot(c,v)
                if delta:found=(word,delta,c);break
            if found:break
        if not found:break
        z=contrast_probe(channels,basis,*found);probes.append(z)
        G.append([F(x) for x in z[0]['quadratic_coefficients']])
        if len(G)>k:raise AssertionError('Exceeded family rank')
    p=len(G);_,cols=rref(G,k);V=[[q(row[j]) for j in cols] for row in G];vi=inv(V)
    K=max(sum(abs(real(x)) for x in row) for row in vi)
    R=max([F(0)]+[sum(row[j] for j in cols) for row in G[1:]])
    u=min(F(1,16),1/(16*K*max(F(1),R)));eta=2*u
    beta=mul(vi,[[q(x) for x in row] for row in G]);records=[]
    for record,rho,yy,base,ends in probes:
        r=record['reference_dim'];sig=add(rho,scale(u/F(a*r),yy));sign=record['selected_sign']
        record.update({'rho':out(rho),'sigma':out(sig),
          'rho_product_mixture':product_mixture(a,r,base),
          'sigma_product_mixture':product_mixture(a,r,base+[(u,*ends[0]),(sign*u,*ends[1])]),
          'largest_state_entry_bits':max(max_bits(rho),max_bits(sig))})
        records.append(record)
    return {'status':'complete_affine_profile_panel','input_dim':a,'channel_count':k,
      'effective_output_ranks':[ch.rank for ch in channels],
      'reference_bound':sum(ch.rank**2 for ch in channels),'word_algebra_dimension':len(queue),
      'basis_labels':labels,'word_basis':[list(w) for w,_ in queue],
      'basis_moments':out(moments),'augmented_profile_rank':p,'affine_profile_dimension':p-1,
      'probe_count':len(probes),'selected_basis_channel_indices':cols,'affine_reconstruction':out(beta),
      'affine_relations':[[str(x) for x in c] for c in nullspace(G,k)],
      'augmented_quadratic_matrix':[[str(x) for x in row] for row in G],
      'minor_inverse_infinity_norm':str(K),'minor_quadratic_row_sum_bound':str(R),
      'common_parameter':str(u),'relative_radius_bound':str(eta),
      'inverse_perturbation_norm_bound':str(K*eta/(1-eta)*R),'probes':records,
      'contract':'For every nonaffine real operator-convex f on (0,infinity), the augmented matrix of maximal f-divergences on these common probes has exactly the stated affine relation kernel. The same rational reconstruction expresses every supplied channel profile using the selected channels, on every faithful input pair with every finite reference. This asserts profile identities, not signed physical channel simulations.',
      'review_status':'Unreviewed mathematical construction with exact implementation checks; no scalability or experimental sample-efficiency claim.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output');a=p.parse_args()
    objects=json.loads(Path(a.input).read_text())['channels'];cert=compile_panel(objects)
    Path(a.output).write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps({x:cert[x] for x in ['channel_count','word_algebra_dimension','augmented_profile_rank','probe_count','common_parameter']}))
