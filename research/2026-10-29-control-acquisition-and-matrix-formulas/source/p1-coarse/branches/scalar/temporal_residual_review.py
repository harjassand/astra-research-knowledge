"""Independent exact checks of temporal signed-correction identity.

This file does not import the root temporal compiler. It uses rational matrix
arithmetic from the separately written scalar-branch helper. All examples
are synthetic mathematical witnesses, not physical source acquisitions.
"""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import json
from jet_closure_checks import mm, transpose, eye, add

def neg(A):return [[-x for x in r] for r in A]
def sub(A,B):return add(A,neg(B))
def scale(a,A):return [[a*x for x in row] for row in A]
def dot(a,b):return mm(transpose(a),b)[0][0]
def mul_word(As,word,v):
    out=v
    for i in word:out=mm(As[i],out)
    return out

def rational_sqrt_upper(q,bits=40):
    assert q>=0
    den=1<<bits
    # Ceiling sqrt(q)*den, exactly.
    a=isqrt((q.numerator*den*den)//q.denominator)
    if a*a*q.denominator<q.numerator*den*den:a+=1
    out=F(a,den)
    assert out*out>=q
    return out

def verify_identity(As,b,words,Ls,word):
    cols=[mul_word(As,w,b) for w in words]
    V=[[col[i][0] for col in cols] for i in range(len(b))]
    G=mm(transpose(V),V)
    M=[mm(mm(transpose(V),A),V) for A in As]
    N=[mm(mm(transpose(V),mm(A,A)),V) for A in As]
    E=[sub(mm(A,V),mm(V,L)) for A,L in zip(As,Ls)]
    D=[sub(m,mm(G,L)) for m,L in zip(M,Ls)]
    R=[add(sub(sub(n,mm(m,L)),mm(transpose(L),m)),mm(mm(transpose(L),G),L))
       for m,n,L in zip(M,N,Ls)]
    for e,d,r in zip(E,D,R):
        assert mm(transpose(V),e)==d
        assert mm(transpose(e),e)==r
    q=len(words);c0=[[F(i==0)] for i in range(q)]
    assert mm(V,c0)==b
    H=len(word)
    alpha=[c0]
    for i in word:alpha.append(mm(Ls[i],alpha[-1]))
    beta=[None]*H
    z=c0
    for t in reversed(range(H)):
        beta[t]=z
        z=mm(Ls[word[t]],z)
    raw=mm(mm(transpose(c0),G),alpha[-1])[0][0]
    correction=sum(mm(mm(transpose(beta[t]),D[word[t]]),alpha[t])[0][0] for t in range(H))
    actual=dot(b,mul_word(As,word,b))
    pairs=[];rema=F(0);upper=F(0)
    for t in range(H):
        et=mm(E[word[t]],alpha[t])
        qt=dot(et,et)
        assert qt==mm(mm(transpose(alpha[t]),R[word[t]]),alpha[t])[0][0]
        for s in range(t+1,H):
            es=mm(E[word[s]],beta[s]);qs=dot(es,es)
            middle=mul_word(As,word[t+1:s],et)
            term=dot(es,middle)
            assert term*term<=qt*qs
            rema+=term
            upper+=rational_sqrt_upper(qt*qs)
            pairs.append(str(term))
    assert actual-(raw+correction)==rema
    assert abs(actual-(raw+correction))<=upper
    return {'dictionary_words':[list(w) for w in words],'word':list(word),
            'dictionary_columns':q,'hidden_dimension':len(b),
            'raw_prediction':str(raw),'signed_correction':str(correction),
            'corrected_prediction':str(raw+correction),'actual':str(actual),
            'exact_remainder':str(rema),'exact_pair_terms':pairs,
            'rational_outward_remainder_bound':str(upper)}

def matpow(A,n):
    R=eye(len(A))
    while n:
        if n&1:R=mm(A,R)
        A=mm(A,A);n//=2
    return R

def main():
    # Symmetric rational contractions, certified by maximum absolute row sum.
    As=[[[F(1,2),F(1,8),F(0)],[F(1,8),F(1,3),F(1,10)],[F(0),F(1,10),F(1,4)]],
        [[F(1,3),F(-1,6),F(1,7)],[F(-1,6),F(1,4),F(0)],[F(1,7),F(0),F(1,5)]]]
    for A in As:
        assert A==transpose(A)
        assert max(sum(abs(a) for a in row) for row in A)<=1
    b=[[F(1)],[F(0)],[F(0)]]
    words=[(),(0,),(1,),(0,1)] # 4 columns in R3: G is necessarily singular.
    # Deliberately arbitrary, non-selfadjoint coefficient maps. The identity
    # must not require a Galerkin solve, invertible G or metric-selfadjoint L.
    Ls=[[[F(1,5),0,F(1,10),0],[1,F(1,4),0,F(1,9)],[0,F(-1,7),F(1,3),0],[0,0,F(1,8),F(1,2)]],
        [[F(1,6),F(1,9),0,0],[0,F(1,4),0,0],[1,0,F(1,3),F(1,7)],[0,1,F(-1,10),F(1,5)]]]
    checks=[verify_identity(As,b,words,Ls,w) for w in [(0,),(1,0),(0,1,1,0,1),(1,0,1,0,0,1)]]
    precision=[]
    for N,k in [(8,6),(32,26),(128,100),(512,402)]:
        t=F(1,N);c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
        A=[[c,s],[s,-c]];Bp=eye(2);Bm=[[F(1),F(0)],[F(0),F(-1)]]
        assert mm(A,A)==eye(2)
        V=[[F(1),c],[F(0),s]]
        G=mm(transpose(V),V)
        Map=mm(mm(transpose(V),A),V)
        Mplus=G;Mminus=mm(mm(transpose(V),Bm),V)
        assert sub(Mplus,Mminus)==[[0,0],[0,2*s*s]]
        for B in [Bp,Bm]:assert mm(mm(transpose(V),mm(B,B)),V)==G
        # Actual sequence is B then A, repeated k times.
        vp=matpow(mm(A,Bp),k)[0][0]
        vm=matpow(mm(A,Bm),k)[0][0]
        assert k%2==0 and vp==1 and abs(vm)<F(1,10)
        midpoint=(Mplus[1][1]+Mminus[1][1])/2
        assert abs(Mplus[1][1]-midpoint)==s*s
        assert abs(Mminus[1][1]-midpoint)==s*s
        precision.append({'N':N,'repetitions':k,'horizon':2*k,
                          'gram_min_eigenvalue':str(1-c),
                          'sole_moment_gap':str(2*s*s),'compatible_error_eta':str(s*s),
                          'long_amplitude_plus':str(vp),'long_amplitude_minus_float':float(vm),
                          'long_gap_float':float(vp-vm),'exact_gap_exceeds_9_over_10':vp-vm>F(9,10),
                          'exact_numerator_bits':vm.numerator.bit_length(),
                          'exact_denominator_bits':vm.denominator.bit_length()})
    result={'scope':'Independent finite exact review of signed identity and fixed short-moment precision witness. No whole-pipeline or physical audit.',
            'singular_gram_arbitrary_map_identity_checks':checks,
            'precision_witnesses':precision}
    Path(__file__).with_name('TEMPORAL_RESIDUAL_REVIEW_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
