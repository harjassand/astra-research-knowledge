"""Separate realization-certificate checker; does not import any compiler.

Shared exact.py kernel means this is not an independent formal verification.
NO certificates are checked directly as polynomial squared norms. YES checks
CPTP, the rational factor, and complete ordered moments by finite closure.
"""
import argparse,json
from pathlib import Path
from exact import *


def combine(coeffs,matrices):
    z=zero(len(matrices[0]),len(matrices[0][0]))
    for c,m in zip(coeffs,matrices):z=add(z,scale(c,m))
    return z


def direct_sum(blocks):
    n=sum(len(x) for x in blocks);z=zero(n);offset=0
    for x in blocks:
        for i in range(len(x)):
            for j in range(len(x)):z[offset+i][offset+j]=x[i][j]
        offset+=len(x)
    return z


def word_value(ch,basis,word):
    z=ch.omega
    for h in word:
        if type(h)!=int or not 0<=h<len(basis):raise AssertionError('Invalid word letter')
        z=mul(mul(z,ch.oinv),ch.apply(basis[h]))
    return z


def norm(ch,raw):return tr(mul(mul(adj(raw),ch.oinv),raw))/ch.a


def check(obj,cert):
    channels=[Channel(x) for x in obj['channels']];c=[real(q(x)) for x in obj['coefficients']]
    a=channels[0].a
    assert len(c)==len(channels) and sum(c)==1 and all(ch.a==a for ch in channels)
    assert [str(x) for x in c]==cert['coefficients']
    basis,_=hermitian_basis(a);words=cert['word_basis']
    values=[[word_value(ch,basis,w) for w in words] for ch in channels]
    status=cert['status'];result={'status':status,'accepted':True}
    if status.startswith('not_realizable_'):
        v=[q(x) for x in cert['polynomial_coefficients']];assert len(v)==len(words)
        raws=[combine(v,ms) for ms in values]
        f=real(sum((q(cj)*norm(ch,x) for cj,ch,x in zip(c,channels,raws)),Q()))
        if status=='not_realizable_negative_norm':
            assert f<0 and f==F(cert['negative_norm']);result['negative_norm']=str(f)
        elif status=='not_realizable_null_ideal':
            assert f==0
            h=cert['generator_index'];assert type(h)==int and 0<=h<len(basis)
            products=[mul(mul(x,ch.oinv),ch.apply(basis[h])) for ch,x in zip(channels,raws)]
            g=real(sum((q(cj)*norm(ch,x) for cj,ch,x in zip(c,channels,products)),Q()))
            assert g>0 and g==F(cert['positive_product_norm'])
            w=[q(x) for x in cert['right_product_coefficients']];assert len(w)==len(words)
            assert products==[combine(w,ms) for ms in values]
            result.update(zero_norm='0',positive_product_norm=str(g))
        else:raise AssertionError('Unknown NO status')
        return result
    assert status=='realizable'
    target=Channel(cert['channel']);assert target.a==a
    factor=mat(cert['rational_factor']);k=mat(cert['filter_gram'])
    assert mul(adj(factor),factor)==k and psd(k)
    for x in range(a):
        for y in range(a):
            e=zero(a);e[x][y]=q(1)
            assert target.apply(e)==mul(mul(factor,direct_sum([ch.apply(e) for ch in channels])),adj(factor))
    all_channels=channels+[target];contrast=c+[F(-1)]
    initial=[ch.omega for ch in all_channels];span=Span();span.insert(sum((flat(m) for m in initial),[]))
    queue=[((),initial)];head=0;maxlen=0
    # Closure, not a preselected finite list of moments, certifies all lengths.
    while head<len(queue):
        word,raw=queue[head];head+=1;maxlen=max(maxlen,len(word))
        assert sum((q(ci)*tr(m)/a for ci,m in zip(contrast,raw)),Q())==Q()
        for h in basis:
            nxt=[mul(mul(m,ch.oinv),ch.apply(h)) for ch,m in zip(all_channels,raw)]
            if span.insert(sum((flat(m) for m in nxt),[])):queue.append((word+(1,),nxt))
    probability=F(cert['uniform_flag_success_probability'])
    assert probability>0 and psd(add(eye(len(k)),scale(-probability*len(channels),k)))
    result.update(output_dim=target.b,output_support_rank=target.rank,combined_algebra_dimension=len(queue),
                  maximum_checked_basis_word_length=maxlen,uniform_flag_success_probability=str(probability))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('certificate');p.add_argument('--output');args=p.parse_args()
    answer=check(json.loads(Path(args.input).read_text()),json.loads(Path(args.certificate).read_text()))
    if args.output:Path(args.output).write_text(json.dumps(answer,indent=2)+'\n')
    print(json.dumps(answer,indent=2))
