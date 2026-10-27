"""Exact opposition models; neither is a negative witness for q_n.

1. A negative transverse coefficient T for the actual two-copy form.
2. A strictly positive PPT lower form whose product with K_3 has a
   negative Schmidt-rank-two vector. The latter is a reconstructed known
   activation mechanism, and is deliberately not L^{tensor m}.
"""
from fractions import Fraction as F
from itertools import product
import json
import sympy as s


def transverse():
    U=[s.Matrix([[0,-1],[-1,0],[-1,1]]),
       s.Matrix([[0,0],[1,0],[-1,1]])]
    V=[s.Matrix([[1,0],[1,0],[-1,0]]),
       s.Matrix([[0,0],[-1,0],[1,-1]])]
    X=s.Matrix([[41,122],[-35,-246],[-49,-115]])/41
    Y=s.Matrix([[83,205],[35,41],[-35,-171]])/41
    def inner(a,b):return s.trace(a.T*b)
    def q(a):return inner(a,a)-s.trace(a)**2/2
    def b(a,c):return inner(a,c)-s.trace(a)*s.trace(c)/2
    slice_values=[inner(U[i],X)+inner(V[i],Y) for i in range(2)]
    if slice_values!=[0,0]:raise AssertionError('slice')
    A=sum((U[i]*V[i].T for i in range(2)),s.zeros(3))
    a=sum(q(U[i]*V[j].T) for i in range(2) for j in range(2))-q(A)/2
    T=sum(q(U[i]*Y.T)+q(X*V[i].T) for i in range(2))-b(A,X*Y.T)
    d=q(X*Y.T)
    if a!=s.Rational(67,4) or T!=-s.Rational(147605,3362):
        raise AssertionError('transverse coefficient')
    if d!=s.Rational(6714658676,2825761):raise AssertionError('quartic')
    discr=2*a*d-T*T
    if not discr>0:raise AssertionError('must not be original negative witness')
    G=s.Matrix([[inner(U[i],U[j])+inner(V[i],V[j]) for j in range(2)]
                for i in range(2)])
    third=(inner(X,X)+inner(Y,Y))/10000
    # G-third I positive definite makes the third eigenline lowest.
    gap=G-third*s.eye(2)
    if not gap[0,0]>0 or not gap.det()>0:raise AssertionError('lowest Gram')
    # Independently evaluate the actual 9-by-9 q_2 of the rational rank-two C.
    Uf=s.Matrix.vstack(U[0],U[1],X/100)
    Vf=s.Matrix.vstack(V[0],V[1],Y/100)
    C=Uf*Vf.T
    if C.rank()!=2:raise AssertionError('rank control')
    trace0=s.zeros(3);trace1=s.zeros(3)
    for i in range(3):
        trace0+=C[3*i:3*i+3,3*i:3*i+3]
    for i,j in product(range(3),repeat=2):
        trace1[i,j]=sum(C[3*i+k,3*j+k] for k in range(3))
    direct=inner(C,C)-(inner(trace0,trace0)+inner(trace1,trace1))/2+s.trace(C)**2/4
    split=a+T/s.Integer(10000)+d/s.Integer(200000000)
    if direct!=split or not direct>0:raise AssertionError('actual q_2 control')
    return {'scope':'global T>=0 is false for actual q_2; q_2 remains positive',
            'slice':[str(x) for x in slice_values],
            'a':str(a),'T':str(T),'d':str(d),
            '2ad_minus_T2':str(discr),'binary_Gram':str(G),
            'scaled_third_Gram':str(third),'actual_q2':str(direct)}


def de(a,b):return int(a==b)


def sigma(a,b,c,d):
    # a,c are (A1,A2); b,d are (B1,B2).
    ident=de(a[0],c[0])*de(b[0],d[0])
    swap=de(a[0],d[0])*de(b[0],c[0])
    A=F(ident-swap,2);S=F(ident+swap,2)
    P=F(de(a[1],b[1])*de(c[1],d[1]),3)
    I=de(a[1],c[1])*de(b[1],d[1])
    return A*P/15+S*(I-P)/60


def W(a,b,c,d):
    P=F(de(a[0],b[0])*de(c[0],d[0]),3)
    I=de(a[0],c[0])*de(b[0],d[0])
    ident=de(a[1],c[1])*de(b[1],d[1])
    swap=de(a[1],d[1])*de(b[1],c[1])
    A=F(ident-swap,2);S=F(ident+swap,2)
    return P*A/15+(I-P)*S/60


def K(a,b,c,d):
    return F(de(a,c)*de(b,d))-F(de(a,b)*de(c,d),2)


def activator():
    local=list(product(range(3),repeat=2))
    for a,b,c,d in product(local,repeat=4):
        if W(a,b,c,d)!=sigma(a,d,c,b):raise AssertionError('PPT identity')
    trace_sigma=sum(sigma(a,b,a,b) for a,b in product(local,repeat=2))
    if trace_sigma!=1:raise AssertionError('normalization')
    vec=[]
    for i,j in product(range(3),repeat=2):
        for a2,b2,z in [(0,1,1),(1,0,-1)]:
            vec.append(((i,i,a2),(j,j,b2),z))
    raw=F(0);white=F(0)
    for a,b,z in vec:
        for c,d,w in vec:
            kk=K(a[0],b[0],c[0],d[0])
            raw+=z*w*kk*W(a[1:],b[1:],c[1:],d[1:])
            white+=z*w*kk*de(a[1:],c[1:])*de(b[1:],d[1:])
    if raw!=F(-1,15) or white!=15:raise AssertionError('activation contraction')
    epsilon=F(1,450);strict=raw+epsilon*white
    if strict!=F(-1,30):raise AssertionError('strict activation')
    # Rank uses the two disjoint output basis factors on each party.
    C=s.zeros(27)
    for a,b,z in vec:
        r=9*a[0]+3*a[1]+a[2];c=9*b[0]+3*b[1]+b[2]
        C[r,c]=z
    if C.rank()!=2:raise AssertionError('Schmidt rank')
    return {'scope':'generic positive PPT lower form; NOT the Werner tensor power',
            'PPT_entry_checks':len(local)**4,'trace_sigma':str(trace_sigma),
            'Schmidt_rank':2,'norm_squared':18,'unperturbed_expectation':str(raw),
            'identity_expectation':str(white),'epsilon':str(epsilon),
            'strict_expectation':str(strict),
            'normalized_operator_bound':'1 after scaling by 450/31',
            'normalized_crossed_lower_bound':'1/31, greater than 2^(-5)',
            'normalized_negative_expectation':str(strict*F(450,31))}


def negative_plane():
    # Opposes the additional trial hypothesis that a Gram-sliced T has
    # at most one negative complex direction. This is already false at m=1.
    P=[s.Matrix(z) for z in [[[0,0],[-1,1],[-1,1]],
                            [[0,1],[1,0],[0,-1]],
                            [[-1,1],[0,-1],[1,0]],
                            [[0,-1],[0,0],[0,1]]]]
    def row(A):return s.Matrix([list(A)])
    R=s.Matrix.vstack(row(P[0]).row_join(row(P[2])),
                      row(P[1]).row_join(row(P[3])))
    K=s.Matrix.hstack(*R.nullspace())
    Z=s.Matrix([[-311,166],[-327,318],[-286,-532],[-250,-159],
                [-561,-56],[-528,84],[-150,577],[39,305],
                [-175,-178],[-65,-307]])
    W=K*Z
    def q(A):return s.trace(A.T*A)-s.trace(A)**2/2
    def b(A,B):return s.trace(A.T*B)-s.trace(A)*s.trace(B)/2
    A=P[0]*P[2].T+P[1]*P[3].T
    def t(w):
        X=s.Matrix(3,2,list(w[:6]));Y=s.Matrix(3,2,list(w[6:]))
        return sum(q(P[i]*Y.T)+q(X*P[i+2].T) for i in range(2))-b(A,X*Y.T)
    if R*W!=s.zeros(2,2):raise AssertionError('negative-plane slice')
    g00=t(W[:,0]);g11=t(W[:,1]);g01=(t(W[:,0]+W[:,1])-g00-g11)/2
    G=s.Matrix([[g00,g01],[g01,g11]])
    if G!=s.Matrix([[-138093,91],[91,-6465]]) or not G.det()>0:
        raise AssertionError('negative-plane exact certificate')
    return {'scope':'T may have more than one negative direction even for m=1',
            'factor_blocks':[[[int(v) for v in row] for row in z.tolist()] for z in P],
            'T_on_two_dimensional_Gram_slice':str(G),
            'determinant':str(G.det()),'negative_definite':True,
            'full_certificate':'K=canonical RREF nullspace in this script, W=K Z'}


if __name__=='__main__':
    print(json.dumps({'transverse_opposition':transverse(),
                      'negative_plane_opposition':negative_plane(),
                      'black_box_induction_opposition':activator()},indent=2))
