"""Self-contained exact checker: stdlib only, no optimizer or candidate source.

An actual representing positive measure cannot violate the valid lower cut.
What is checked here is a realizable finite positive *truncated functional*.
"""
from pathlib import Path
from fractions import Fraction as F
import itertools, json, hashlib, time
ROOT=Path(__file__).resolve().parent
start=time.monotonic()
raw=(ROOT/'EXACT_COUNTEREXAMPLE.json').read_bytes()
d=json.loads(raw)
m={(r['k'],r['l']):F(r['value']) for r in d['moments']}
def L(k,l): return m[tuple(sorted((k,l)))]
def mons(n,degree):
    return [a for t in range(degree+1) for a in itertools.product(range(t+1),repeat=n) if sum(a)==t]
def eval_exponent(a):
    if len(a)==8:
        # The coordinate ordering is x,y,u,v, Im(x),Im(y),Im(u),Im(v).
        if any(a[4:]): return F(0)
        a=a[:4]
    return L(a[0]-a[2],a[1]-a[3])
def plus(a,b): return tuple(x+y for x,y in zip(a,b))
def matrix(bs,terms={(0,0):F(1)}):
    return [[sum(c*L(a[0]+b[0]+t[0],a[1]+b[1]+t[1]) for t,c in terms.items()) for b in bs] for a in bs]
def ldlt(A):
    n=len(A); D=[]; T=[[F(0)]*n for _ in range(n)]
    for i in range(n):
        T[i][i]=F(1)
        D.append(A[i][i]-sum(T[i][k]**2*D[k] for k in range(i)))
        assert D[-1]>0,(i,D[-1])
        for j in range(i+1,n):
            T[j][i]=(A[j][i]-sum(T[j][k]*T[i][k]*D[k] for k in range(i)))/D[i]
    assert all(A[i][j]==sum(T[i][k]*D[k]*T[j][k] for k in range(n)) for i in range(n) for j in range(n))
    return D
lin=[(0,0),(1,0),(0,1),(-1,0),(0,-1)]
quad=lin+[(2,0),(1,1),(1,-1),(0,2),(-1,1),(-2,0),(-1,-1),(0,-2)]
reduced=matrix(quad)
pivots={'quotient_moment_order2':ldlt(reduced)}
assert L(0,0)==1
# Check all entries of the FULL complex-as-real 45x45 moment matrix as an
# explicit congruence of the positive 13x13 quotient matrix.
bs8=mons(8,2)
mapped=[]
for a in bs8:
    mapped.append(None if any(a[4:]) else quad.index((a[0]-a[2],a[1]-a[3])))
for i,a in enumerate(bs8):
    for j,b in enumerate(bs8):
        predicted=F(0) if mapped[i] is None or mapped[j] is None else reduced[mapped[i]][mapped[j]]
        assert eval_exponent(plus(a,b))==predicted
for label,t in [('x',(2,0)),('y',(0,2)),('u',(-2,0)),('v',(0,-2))]:
    lo,hi=map(F,d['bounds'][label])
    for kind,terms in [('lower',{t:F(1),(0,0):-lo}),('upper',{t:F(-1),(0,0):hi})]:
        A=matrix(lin,terms)
        pivots[label+'_'+kind+'_localizer']=ldlt(A)
        # The original 9x9 localizer duplicates this 5x5 block with four zero
        # imaginary rows/columns. This follows directly from eval_exponent.
for a in mons(8,2):
    for ix,iu in [(0,2),(1,3)]:
        t=[0]*8;t[ix]=1;t[iu]=1
        assert eval_exponent(plus(a,t))-eval_exponent(a)==0
        # Imaginary parts of bar(x)*u and bar(y)*v vanish because every term
        # carries an imaginary coordinate. Check them explicitly.
        t=[0]*8;t[ix]=1;t[iu+4]=1
        s=[0]*8;s[ix+4]=1;s[iu]=1
        assert eval_exponent(plus(a,t))-eval_exponent(plus(a,s))==0
lower=2*(L(2,0)-L(1,1)-L(-2,0)+L(-1,-1))
assert lower==F(d['lower_cut_value']) and lower<0
current_vq=2*L(2,0)-2*L(1,1)-1-L(2,-2)+2*L(1,-1)
current_uz=2*L(-2,0)-2*L(-1,-1)-L(-4,0)-L(-2,-2)+2*L(-3,-1)
assert current_vq<0 or current_uz<0
for key,D in pivots.items():
    assert list(map(str,D))==d['exact_ldlt_pivots'][key]
receipt={'status':'PASS','arithmetic':'Python Fraction exact rational; comparisons use numerator signs','counterexample_sha256':hashlib.sha256(raw).hexdigest(),'degree4_moment_entries_checked':len(bs8)**2,'full_complex_real_moment_dimension':len(bs8),'strictly_positive_reduced_moment_dimension':len(quad),'original_localizers':8,'each_full_localizer_dimension':9,'each_reduced_localizer_dimension':5,'complex_equality_monomial_multipliers_checked':len(mons(8,2)),'lower_cut_value':str(lower),'scalar_current_bound_1_minus_L_u2':str(1-L(-2,0)),'localized_current_bound_at_q_y_minus_x':str(current_vq),'localized_current_bound_at_z_u_minus_v':str(current_uz),'wall_seconds':time.monotonic()-start,'independent_of_solver_output':True,'requires_third_party_packages':False}
(ROOT/'EXACT_CHECK_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
