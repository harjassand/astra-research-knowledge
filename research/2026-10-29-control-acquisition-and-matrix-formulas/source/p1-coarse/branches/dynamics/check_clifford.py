"""Exact frozen-versus-switched passive counterexample.

All reported word values and matrix checks use integer/Fraction arithmetic.
The continuous-generator identity is proved in CLIFFORD.md.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
from collections import Counter
import numpy as np

ROOT=Path(__file__).resolve().parent


def realify(a):
    return np.block([[a.real, -a.imag], [a.imag, a.real]]).astype(np.int64)


def word_num(mats, word):
    out=np.eye(8,dtype=np.int64)
    for j in word:
        out=mats[j] @ out
    return out


def word_value(mats, word):
    return F(int(np.trace(word_num(mats,word))),8*8**len(word))


def inv_fraction(a):
    n=len(a)
    v=[list(row)+[F(int(i==j)) for j in range(n)] for i,row in enumerate(a)]
    for k in range(n):
        p=next(i for i in range(k,n) if v[i][k])
        v[k],v[p]=v[p],v[k]
        div=v[k][k]
        v[k]=[x/div for x in v[k]]
        for i in range(n):
            if i!=k and v[i][k]:
                mul=v[i][k]
                v[i]=[x-mul*y for x,y in zip(v[i],v[k])]
    return [row[n:] for row in v]


def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def gram_shift(mats, words, shift):
    W=[word_num(mats,w) for w in words]
    C=word_num(mats,shift)
    return [[F(int(np.trace(W[i].T @ C @ W[j])),
               8*8**(len(words[i])+len(words[j])+len(shift)))
             for j in range(len(words))] for i in range(len(words))]


class ScalarWordSource:
    """The learner gets only query(word); private matrices are source fixture."""
    def __init__(self, matrices):
        self._matrices=matrices
        self.readings={}

    def query(self, word):
        # Reversal equality follows from real self-adjoint actuators.
        word=tuple(word)
        key=min(word,word[::-1])
        if key not in self.readings:
            self.readings[key]=word_value(self._matrices,key)
        return self.readings[key]


def acquired_gram(query,words,shift):
    return [[query(words[j]+shift+words[i][::-1]) for j in range(len(words))]
            for i in range(len(words))]


def predict(G,Ts,word):
    x=[[F(int(i==0))] for i in range(len(G))]
    for i in word:
        x=mm(Ts[i],x)
    return mm([G[0]],x)[0][0]


def main():
    I=np.eye(2,dtype=complex)
    X=np.array([[0,1],[1,0]],dtype=complex)
    Y=np.array([[0,-1j],[1j,0]],dtype=complex)
    Z=np.diag([1,-1]).astype(complex)
    gammas=[realify(np.kron(X,I)),realify(np.kron(Y,I)),
            realify(np.kron(Z,X)),realify(np.kron(Z,Y)),realify(np.kron(Z,Z))]
    E=np.eye(8,dtype=np.int64)
    for i,g in enumerate(gammas):
        assert np.array_equal(g,g.T)
        assert np.array_equal(g@g,E)
        assert np.trace(g)==0
        for j in range(i):
            assert not np.any(g@gammas[j]+gammas[j]@g)
    chirality=word_num(gammas,range(5))
    chirality_sign=int(chirality[0,0])
    assert np.array_equal(chirality,chirality_sign*E)
    plus=[4*E+3*g for g in gammas]  # Divide by 8.
    minus=plus[:-1]+[4*E-3*gammas[-1]]

    # Every proper Clifford monomial has zero trace; the full one is +/-I.
    proper_trace_checks=0
    for mask in range(1,31):
        w=[j for j in range(5) if mask>>j & 1]
        assert np.trace(word_num(gammas,w))==0
        proper_trace_checks+=1
    early_words=0
    for length in range(5):
        for w in product(range(5), repeat=length):
            assert word_value(plus,w)==word_value(minus,w)
            early_words+=1
    w=(0,1,2,3,4)
    first=word_value(plus,w)
    second=word_value(minus,w)
    assert abs(first-second)==F(243,16384)

    # Purely exact finite controls of frozen mixtures, in addition to the
    # all-mixture proof. Integer coefficient vector avoids float eigenchecks.
    frozen_checks=0
    for u in [[1,0,0,0,0],[1,2,3,4,5],[1,-2,4,-3,2],[3,1,1,2,7]]:
        p=sum((x*a for x,a in zip(u,plus)),np.zeros((8,8),dtype=np.int64))
        q=sum((x*a for x,a in zip(u,minus)),np.zeros((8,8),dtype=np.int64))
        for k in range(1,7):
            # Python object integers avoid overflow at sixth powers.
            assert np.trace(np.linalg.matrix_power(p.astype(object),k))==np.trace(np.linalg.matrix_power(q.astype(object),k))
            frozen_checks+=1

    # The actual word dictionary has 16 columns. It is reachable and invariant
    # in both sources, despite the 64-coordinate vec(I) realization.
    words=[()]+[(i,) for i in range(5)]+[(i,j) for i in range(5) for j in range(i+1,5)]
    sources=[ScalarWordSource(plus),ScalarWordSource(minus)]
    Gp=acquired_gram(sources[0].query,words,())
    Gm=acquired_gram(sources[1].query,words,())
    assert Gp==Gm
    Ginv=inv_fraction(Gp)  # Exact non-singularity check.
    closure_checks=0
    shifts_differ=0
    reduced=[[],[]]
    for i in range(5):
        Mp=acquired_gram(sources[0].query,words,(i,))
        Mm=acquired_gram(sources[1].query,words,(i,))
        shifts_differ+=sum(x!=y for a,b in zip(Mp,Mm) for x,y in zip(a,b))
        for source_id,M in enumerate([Mp,Mm]):
            N=acquired_gram(sources[source_id].query,words,(i,i))
            prediction=mm(M,mm(Ginv,M))
            assert N==prediction
            closure_checks+=1
            reduced[source_id].append(mm(Ginv,M))
    query_costs=[]
    for source in sources:
        query_costs.append({'scalar_readings':len(source.readings),
                            'prepared_reset_histories':len(source.readings),
                            'actuator_applications':sum(map(len,source.readings)),
                            'word_lengths':dict(sorted(Counter(map(len,source.readings)).items()))})
    later_predictions=[]
    later_checks=0
    for length in range(5,18):
        testword=tuple(range(5))+tuple((3*j+j*j+length)%5 for j in range(length-5))
        for source_id,mats in enumerate([plus,minus]):
            actual=word_value(mats,testword) # checker-only call, not learner data
            predicted=predict(Gp,reduced[source_id],testword)
            assert actual==predicted
            later_checks+=1
            later_predictions.append({'source':source_id+1,'word':[i+1 for i in testword],
                                       'exact_prediction':str(predicted)})

    result={
        'all_arithmetic':'integer and Fraction for checks; all-mixture equality proved separately',
        'real_generator_matrix_dimension':8,
        'real_hidden_state_dimension_for_scalar_trace_port':64,
        'gamma_matrices': [g.tolist() for g in gammas],
        'actuator_numerator_matrices_source_one':[a.tolist() for a in plus],
        'actuator_common_denominator':8,
        'source_two_change':'replace actuator 5 numerator 4I+3Gamma5 by 4I-3Gamma5',
        'actuator_spectrum':[str(F(1,8)),str(F(7,8))],
        'source_one_chirality_sign':chirality_sign,
        'proper_clifford_trace_checks':proper_trace_checks,
        'identical_words_length_at_most_four':early_words,
        'distinct_word':[i+1 for i in w],
        'word_response_source_one':str(first),
        'word_response_source_two':str(second),
        'exact_separation':str(abs(first-second)),
        'exact_frozen_mixture_moment_checks':frozen_checks,
        'word_dictionary':[list(x+1 for x in word) for word in words],
        'dictionary_size':len(words),
        'dictionary_gram_equal_between_sources':True,
        'gram_nonsingular_exact':True,
        'shifted_gram_entries_differing_across_all_five_actions':shifts_differ,
        'zero_leakage_exact_checks':closure_checks,
        'charged_acquisition_costs_by_source':query_costs,
        'later_exact_predictions_checked':later_checks,
        'later_queries_supplied_to_learner':0,
        'later_predictions':later_predictions,
        'scope':'finite exact construction; frozen-law equivalence holds for every constant mixture by Clifford identity, not merely the checked examples'
    }
    transcript=[{'source':i+1,'readings':[{'word':[x+1 for x in word],'value':str(value)}
                                        for word,value in sorted(source.readings.items())]}
                for i,source in enumerate(sources)]
    (ROOT/'CLIFFORD_TRANSCRIPTS.json').write_text(json.dumps(transcript,indent=2)+'\n')
    (ROOT/'CLIFFORD_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if 'matrices' not in k and k!='later_predictions'},indent=2))


if __name__=='__main__':
    main()
