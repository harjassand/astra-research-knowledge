"""Exact realization of signed affine complete maximal-f profiles.

A YES output is an explicit rational CPTP Choi matrix. A NO output is a
negative squared norm or a null relation not preserved by right multiplication.
Finite dense input only. No access to a divergence evaluator or physical device.
"""
import argparse,json
from pathlib import Path
from exact import *
from compile_panel import family_words,rref


def blockdiag(blocks):
    sizes=[len(x) for x in blocks];z=zero(sum(sizes));offset=0
    for x,n in zip(blocks,sizes):
        for i in range(n):
            for j in range(n):z[offset+i][offset+j]=x[i][j]
        offset+=n
    return z


def complex_kernel(rows,k):
    rr,piv=rref(rows,k);result=[]
    for j in range(k):
        if j in piv:continue
        v=[Q() for _ in range(k)];v[j]=q(1)
        for row,p in zip(rr,piv):v[p]=-row[j]
        result.append(v)
    return result


def quadratic(v,g):
    return real(sum((x.conj()*g[i][j]*y for i,x in enumerate(v) for j,y in enumerate(v)),Q()))


def negative_vector(g):
    """Rational Schur elimination; None exactly when Hermitian g is PSD."""
    n=len(g)
    for i in range(n):
        if real(g[i][i])<0:
            v=[Q() for _ in range(n)];v[i]=q(1);return v
    pivot=next((i for i in range(n) if real(g[i][i])>0),None)
    if pivot is None:
        for i in range(n):
            for j in range(i+1,n):
                if g[i][j]:
                    v=[Q() for _ in range(n)];v[i]=q(1);v[j]=-g[i][j].conj();return v
        return None
    rest=[i for i in range(n) if i!=pivot];d=g[pivot][pivot]
    s=[[g[i][j]-g[i][pivot]*g[pivot][j]/d for j in rest] for i in rest]
    w=negative_vector(s)
    if w is None:return None
    v=[Q() for _ in range(n)]
    for i,x in zip(rest,w):v[i]=x
    v[pivot]=-sum((g[pivot][i]*v[i] for i in rest),Q())/d
    return v


def rational_squares(d):
    """d=n/m: binary expansion of nm gives <=2 bit(nm) rational squares."""
    if d<=0:raise ValueError('Positive rational required')
    n,m=d.numerator,d.denominator;v=n*m;answer=[];j=0
    while v:
        if v&1:answer.extend([F(2**(j//2),m)]*(1 if j%2==0 else 2))
        j+=1;v>>=1
    assert sum(x*x for x in answer)==d
    return answer


def rational_factor(k):
    """Rectangular C over Q(i), C* C=K; no factoring integers or radicals."""
    n=len(k);rem=[row[:] for row in k];rows=[]
    while any(flat(rem)):
        j=next((i for i in range(n) if real(rem[i][i])>0),None)
        if j is None:raise ValueError('PSD factorization failed')
        d=real(rem[j][j]);v=[rem[i][j]/d for i in range(n)]
        rows.extend([[q(s)*x.conj() for x in v] for s in rational_squares(d)])
        rem=[[rem[i][h]-d*v[i]*v[h].conj() for h in range(n)] for i in range(n)]
    if mul(adj(rows),rows)!=k:raise AssertionError('Factor identity failed')
    return rows


def compile_realization(objects,coefficients):
    channels=[Channel(x) for x in objects]
    if not channels:raise ValueError('Nonempty family required')
    a=channels[0].a;count=len(channels);c=[real(q(x)) for x in coefficients]
    if len(c)!=count or sum(c)!=1 or any(ch.a!=a for ch in channels):raise ValueError('Common input and real affine coefficients required')
    basis,labels=hermitian_basis(a);queue,moments=family_words(channels,basis);d=len(queue)
    values=[x for _,x in queue]
    gram=[[sum((q(cj)*tr(mul(mul(adj(bi),ch.oinv),bj))/a for cj,ch,bi,bj in zip(c,channels,vi,vj)),Q()) for vj in values] for vi in values]
    cert={'input_dim':a,'coefficients':[str(x) for x in c],
          'word_basis':[list(w) for w,_ in queue],'basis_labels':labels,
          'word_algebra_dimension':d,'effective_rank_square_bound':sum(ch.rank**2 for ch in channels),
          'moment_gram':out(gram),'review_status':'Unreviewed construction; exact implementation verification is not independent mathematical review.'}
    neg=negative_vector(gram)
    if neg is not None:
        cert.update(status='not_realizable_negative_norm',polynomial_coefficients=[x.out() for x in neg],negative_norm=str(quadratic(neg,gram)))
        return cert
    vectors=[sum((flat(b) for b in v),[]) for v in values]
    cg=[[sum((x.conj()*y for x,y in zip(v,w)),Q()) for w in vectors] for v in vectors];ci=inv(cg)
    def coordinates(v):
        w=sum((flat(b) for b in v),[])
        rhs=[[sum((x.conj()*y for x,y in zip(u,w)),Q())] for u in vectors]
        z=[row[0] for row in mul(ci,rhs)]
        assert [sum((z[i]*vectors[i][j] for i in range(d)),Q()) for j in range(len(w))]==w
        return z
    kernel=complex_kernel(gram,d)
    for v in kernel:
        pv=[sum_matrices([scale(v[i],values[i][j]) for i in range(d)]) for j in range(count)]
        for h,letter in enumerate(basis):
            product=[mul(mul(b,ch.oinv),ch.apply(letter)) for b,ch in zip(pv,channels)]
            w=coordinates(product);norm=quadratic(w,gram)
            if norm:
                assert norm>0
                cert.update(status='not_realizable_null_ideal',polynomial_coefficients=[x.out() for x in v],
                            generator_index=h,right_product_coefficients=[x.out() for x in w],
                            zero_norm=str(quadratic(v,gram)),positive_product_norm=str(norm))
                return cert
    # HS projection onto the normalized algebra, entirely in raw coordinates.
    # Here Omega is the UNNORMALIZED direct sum of Omega_j; the input CP map
    # is the unscaled direct sum too. Their common scale cancels in Gamma.
    hs=[[sum((tr(mul(mul(mul(ch.oinv,adj(bi)),ch.oinv),bj)) for ch,bi,bj in zip(channels,vi,vj)),Q()) for vj in values] for vi in values]
    target=[[sum((q(cj)*tr(adj(bi)) for cj,bi in zip(c,vi)),Q())] for vi in values]
    alpha=[row[0] for row in mul(inv(hs),target)]
    raw=[sum_matrices([scale(alpha[i],values[i][j]) for i in range(d)]) for j in range(count)]
    k=blockdiag([mul(mul(ch.oinv,b),ch.oinv) for ch,b in zip(channels,raw)])
    assert psd(k)
    factor=rational_factor(k);b=len(factor);jout=zero(a*b)
    for x in range(a):
        for y in range(a):
            e=zero(a);e[x][y]=q(1)
            v=mul(mul(factor,blockdiag([ch.apply(e) for ch in channels])),adj(factor))
            for r in range(b):
                for s in range(b):jout[x*b+r][y*b+s]=v[r][s]
    output={'input_dim':a,'output_dim':b,'choi':out(jout)}
    Channel(output)
    cert.update(status='realizable',nullity=len(kernel),projection_coefficients=[x.out() for x in alpha],
                filter_gram=out(k),rational_factor=out(factor),channel=output,
                largest_output_entry_bits=max_bits(jout),largest_factor_entry_bits=max_bits(factor),
                uniform_flag_success_probability=str(1/(count*real(tr(k)))))
    return cert


def sum_matrices(ms):
    if not ms:raise ValueError('Nonempty list required')
    z=zero(len(ms[0]),len(ms[0][0]))
    for x in ms:z=add(z,x)
    return z

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output');args=p.parse_args()
    obj=json.loads(Path(args.input).read_text());cert=compile_realization(obj['channels'],obj['coefficients'])
    Path(args.output).write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps({key:cert[key] for key in ['status','word_algebra_dimension']},indent=2))
