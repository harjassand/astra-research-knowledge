"""A paid *digital* source of certified tagged-spin records.

This is not a physical experiment or an efficient unknown-apparatus oracle.
It uses an explicitly supplied small-N Hamiltonian, exact rational Pauli
commutators, a bounded Taylor remainder, and dyadic record rounding.
The reconstruction program receives only its resulting records.
"""
from fractions import Fraction as Q
from itertools import combinations,product
from math import factorial,prod
from polynomial_tools import evaluate


def pauli_terms(N,p):
    result={}
    sites=tuple(range(N))
    for alpha,c in p.items():
        a,b,d=alpha
        count=factorial(N)//(factorial(N-a-b-d)*factorial(a)*factorial(b)*factorial(d))
        for xx in combinations(sites,a):
            rem=[i for i in sites if i not in xx]
            for yy in combinations(rem,b):
                rem2=[i for i in rem if i not in yy]
                for zz in combinations(rem2,d):
                    xm=sum(1<<i for i in xx+yy)
                    zm=sum(1<<i for i in yy+zz)
                    result[(xm,zm)]=result.get((xm,zm),Q(0))+N*c/count
    return result


def heisenberg_commutator(H,O):
    result={}; ops=0
    for (x,z),a in H.items():
        for (v,w),b in O.items():
            ops+=1
            phase=((x&z).bit_count()+(v&w).bit_count()
                   -((x^v)&(z^w)).bit_count()+2*(z&v).bit_count())%4
            if phase%2:
                key=(x^v,z^w)
                result[key]=result.get(key,Q(0))+(-2 if phase==1 else 2)*a*b
    return {k:v for k,v in result.items() if v},ops


def expectation_polynomial(O,tag_axis,N):
    result={}
    for (x,z),c in O.items():
        tagged=(x&1,z&1)
        if tagged!=(0,0) and tagged!=tag_axis: continue
        alpha=[0,0,0]
        for i in range(1,N):
            a=((x>>i)&1,(z>>i)&1)
            if a==(1,0): alpha[0]+=1
            elif a==(1,1): alpha[1]+=1
            elif a==(0,1): alpha[2]+=1
        key=tuple(alpha); result[key]=result.get(key,Q(0))+c
    return {k:v for k,v in result.items() if v}


def round_dyadic(x,bits):
    m=1<<bits
    return Q((2*x.numerator*m+x.denominator)//(2*x.denominator),m)


def make_records(N,p,inverse,sched):
    assert N>=inverse.K
    H=pauli_terms(N,p)
    gamma=sched['record_radius']
    S=0
    # The supplied local-incidence contract gives remainder <= 8^(-S-1).
    while Q(1,8**(S+1))>gamma/4: S+=1
    bits=1
    while Q(1,1<<(bits+1))>gamma/4: bits+=1
    error=Q(1,8**(S+1))+Q(1,1<<(bits+1))
    assert error<=gamma
    # b_x: tag +Y, read Z; b_y: tag +Z, read X; b_z: tag +X, read Y.
    probes=[((1,1),(0,1)),((0,1),(1,0)),((1,0),(1,1))]
    moments=[]; pair_ops=0; support_counts=[]
    for tag,measurement in probes:
        O={measurement:Q(1)}; seq=[]; counts=[]
        for n in range(S+1):
            seq.append(expectation_polynomial(O,tag,N))
            counts.append(len(O))
            if n<S:
                O,ops=heisenberg_commutator(H,O); pair_ops+=ops
        moments.append(seq); support_counts.append(counts)
    records=[]
    for j,r in inverse.records:
        vals=[evaluate(m,r)/factorial(n) for n,m in enumerate(moments[j])]
        row=[]
        for t in sched['nodes']:
            exact=Q(0)
            for v in reversed(vals): exact=exact*t+v
            rounded=round_dyadic(exact,bits)
            assert abs(rounded)<=1+gamma
            row.append(rounded)
        records.append(row)
    return records,{'kind':'exact-rational digital source; no physical shots',
                    'N':N,'hamiltonian_pauli_terms':len(H),'taylor_degree':S,
                    'pauli_pair_operations':pair_ops,'support_counts':support_counts,
                    'rounding_bits':bits,'source_record_radius':str(error)}


def recover(inverse,sched,records):
    gradients=[sum((w*y for w,y in zip(sched['weights'],row)),Q(0))/2 for row in records]
    return inverse.reconstruct(gradients,sched['gradient_error'])
