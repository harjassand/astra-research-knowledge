"""Read-only exact certificate checker for a finite-family profile panel.

Does not call either compiler. It rebuilds words, certifies algebra closure,
checks state/product certificates, and checks the uniform perturbation bound.
The rational arithmetic kernel and mixture checker are shared. This is an
implementation audit, not independent scientific review or formal verification.
"""
import argparse,json,copy
from pathlib import Path
from exact import *
from check_certificate import must,check_mixture

def rank(rows):
    sp=Span()
    for row in rows:sp.insert([q(x) for x in row])
    return len(sp.rows)

def belongs(sp,v):
    other=Span();other.rows=copy.deepcopy(sp.rows)
    return not other.insert(v)

def word_values(channels,basis,word):
    values=[]
    for ch in channels:
        z=ch.omega
        for i in word:z=mul(mul(z,ch.oinv),ch.apply(basis[i]))
        values.append(z)
    return values

def check_panel(objects,cert):
    channels=[Channel(ob) for ob in objects];must(bool(channels),'Empty family')
    a=channels[0].a;k=len(channels);must(all(ch.a==a for ch in channels),'Input mismatch')
    must(cert['status']=='complete_affine_profile_panel','Unexpected certificate')
    must(cert['input_dim']==a and cert['channel_count']==k,'Family metadata')
    N=sum(ch.rank**2 for ch in channels)
    must(cert['effective_output_ranks']==[ch.rank for ch in channels] and cert['reference_bound']==N,'Support metadata')
    basis,labels=hermitian_basis(a);must(cert['basis_labels']==labels,'Basis labels')
    words=cert['word_basis'];D=len(words)
    must(D==cert['word_algebra_dimension'] and 1<=D<=N,'Word dimension')
    must(words[0]==[] and len({tuple(w) for w in words})==D,'Word basis indexing')
    algebra=Span();values=[];moments=[]
    for word in words:
        must(len(word)<=D-1 and all(type(i)==int and 0<=i<len(basis) for i in word),'Word bound or alphabet')
        zs=word_values(channels,basis,word);values.append(zs)
        must(algebra.insert(sum((flat(x) for x in zs),[])),'Dependent word basis')
        moments.append([tr(x)/a for x in zs])
    for zs in values:
        for h in basis:
            nxt=[mul(mul(z,ch.oinv),ch.apply(h)) for z,ch in zip(zs,channels)]
            must(belongs(algebra,sum((flat(x) for x in nxt),[])),'Word span not closed under a generator')
    must(out(moments)==cert['basis_moments'],'Moment mismatch')
    M=[[F(1)]*k]+[[x.re for x in row] for row in moments]+[[x.im for x in row] for row in moments]
    p=rank(M);must(p==cert['augmented_profile_rank'] and p-1==cert['affine_profile_dimension'],'Profile rank')
    probes=cert['probes'];must(len(probes)==p-1==cert['probe_count'],'Probe count is not minimal')
    u=F(cert['common_parameter']);eta=F(cert['relative_radius_bound'])
    must(0<u<=F(1,16) and eta==2*u and eta<=F(1,8),'Radius bound')
    G=[[F(1)]*k];states=[];diagnostics=[]
    for probe in probes:
        r=probe['reference_dim'];dim=a*r
        must(type(r)==int and 1<=r<=N,'Reference dimension')
        rho,sigma=mat(probe['rho']),mat(probe['sigma'])
        for state in [rho,sigma]:
            must(len(state)==dim and all(len(row)==dim for row in state),'State shape')
            must(tr(state)==q(1),'State trace')
            must(psd(add(state,scale(-F(1,2*dim),eye(dim)))),'State lower bound')
            must(psd(add(scale(F(3,2*dim),eye(dim)),scale(-1,state))),'State upper bound')
        must(partial(rho,a,r,'right')==scale(F(1,a),eye(a)),'Input marginal')
        must(partial(sigma,a,r,'right')==partial(rho,a,r,'right'),'Different input marginals')
        must(partial(sigma,a,r,'left')==partial(rho,a,r,'left'),'Different reference marginals')
        check_mixture(probe['rho_product_mixture'],rho,a,r)
        check_mixture(probe['sigma_product_mixture'],sigma,a,r)
        dd=add(sigma,scale(-1,rho))
        must(psd(add(scale(eta,rho),dd)) and psd(add(scale(eta,rho),scale(-1,dd))),'Relative operator bound')
        row=[ch.chi(sigma,rho,r)/(u*u) for ch in channels]
        must(all(x>=0 for x in row) and [str(x) for x in row]==probe['quadratic_coefficients'],'Quadratic row')
        G.append(row);states.append((rho,sigma,r))
        bits=max(max_bits(rho),max_bits(sigma))
        must(bits==probe['largest_state_entry_bits'],'Bit-size metadata')
        diagnostics.append({'reference_dim':r,'largest_state_entry_bits':bits,
          'product_terms':[len(probe['rho_product_mixture']),len(probe['sigma_product_mixture'])]})
    must([[str(x) for x in row] for row in G]==cert['augmented_quadratic_matrix'],'Quadratic matrix')
    must(rank(G)==p and rank(M+G)==p,'Moment and probe row spaces differ')
    J=cert['selected_basis_channel_indices']
    must(len(J)==p and len(set(J))==p and all(type(j)==int and 0<=j<k for j in J),'Basis channel indices')
    V=[[q(row[j]) for j in J] for row in G];vi=inv(V)
    K=max(sum(abs(real(x)) for x in row) for row in vi)
    R=max([F(0)]+[sum(row[j] for j in J) for row in G[1:]])
    must(K==F(cert['minor_inverse_infinity_norm']) and R==F(cert['minor_quadratic_row_sum_bound']),'Condition accounting')
    must(u==min(F(1,16),1/(16*K*max(F(1),R))),'Uniform parameter')
    perturb=K*eta/(1-eta)*R
    must(perturb==F(cert['inverse_perturbation_norm_bound']) and perturb<=F(1,7),'Uniform invertibility bound')
    beta=mat(cert['affine_reconstruction'])
    must(len(beta)==p and all(len(row)==k for row in beta),'Reconstruction shape')
    must(all(not x.im for x in flat(beta)),'Reconstruction not real')
    must(beta==mul(vi,[[q(x) for x in row] for row in G]),'Reconstruction coefficients')
    must(all(sum((beta[i][j] for i in range(p)),Q())==q(1) for j in range(k)),'Coefficients not affine')
    for row in moments:
        must(mul([[row[j] for j in J]],beta)==[row],'Reconstruction fails an ordered moment')
    relations=[[q(x) for x in row] for row in cert['affine_relations']]
    must(len(relations)==k-p and rank(relations)==k-p and all(len(row)==k for row in relations),'Relation basis dimension')
    for row in relations:
        must(all(not x.im for x in row) and sum(row,Q())==Q(),'Relation not a real affine contrast')
        must(all(sum((x*y for x,y in zip(row,v)),Q())==Q() for v in moments),'False relation')
    Z=[[q(x) for x in row] for row in cert['moment_basis_rows']]
    must(len(Z)==p and all(len(row)==k for row in Z) and Z[0]==[q(1)]*k,'Moment basis shape')
    must(rank(Z)==p and rank(M+Z)==p,'Moment basis span')
    J0=cert['moment_basis_minor_columns'];must(len(J0)==p and len(set(J0))==p,'Moment minor columns')
    v0i=inv([[row[j] for j in J0] for row in Z]);K0=max(sum(abs(real(x)) for x in row) for row in v0i)
    must(K0==F(cert['moment_minor_inverse_infinity_norm']),'Moment minor norm')
    mp=cert['maximum_path_length'];t=F(cert['uniform_path_parameter'])
    must(type(mp)==int and 1<=mp<=max(1,D-3),'Maximum path bound')
    must(t==1/(16*max(F(1),K0*p)*2**(mp+1)),'Path parameter')
    err=2**(mp+1)*t/(1-2*t)
    must(err==F(cert['moment_approximation_error_bound']) and K0*p*err<1,'Moment interpolation bound')
    must(cert['candidate_pair_count']==2*(p-1),'Candidate count')
    kernel_checks=[]
    for s in [F(0),F(1),F(8)]:
        rows=[[F(1)]*k]
        for rho,sigma,r in states:
            row=[]
            for ch in channels:
                rr,ss=ch.apply(rho,r),ch.apply(sigma,r);dd=add(ss,scale(-1,rr))
                pp,_,_=pinv_psd(add(ss,scale(s,rr)))
                row.append((1+s)*real(tr(mul(mul(dd,pp),dd)))/(u*u))
            rows.append(row)
        must(rank(rows)==p,'Kernel regression rank')
        must(mul([[q(row[j]) for j in J] for row in rows],beta)==[[q(x) for x in row] for row in rows],'Kernel regression reconstruction')
        kernel_checks.append({'s':str(s),'augmented_rank':p,'reconstruction_passed':True})
    return {'passed':True,'channel_count':k,'word_algebra_dimension':D,'augmented_profile_rank':p,
      'probe_count':p-1,'affine_relation_count':k-p,'selected_basis_channel_indices':J,
      'inverse_perturbation_norm_bound':str(perturb),'probes':diagnostics,'kernel_regressions':kernel_checks,
      'review_status':'Exact implementation audit with shared rational arithmetic and mixture checks; not independent scientific review or formal verification.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('input');parser.add_argument('certificate');parser.add_argument('output');args=parser.parse_args()
    objects=json.loads(Path(args.input).read_text())['channels'];cert=json.loads(Path(args.certificate).read_text())
    result=check_panel(objects,cert);Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:result[key] for key in ['passed','channel_count','word_algebra_dimension','augmented_profile_rank','probe_count']}))
