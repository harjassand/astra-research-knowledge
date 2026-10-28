"""Exact reconstruction of a gamma-dependent separating functional.
This constructs, rather than numerically infers, a full continuous-parameter
obstruction to the coupled-flow closed-form/bilinear-SOS class.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations,combinations_with_replacement
import numpy as np,sympy as S,json,time
import mixed_flow_pairing as p
ROOT=Path(__file__).resolve().parent
start=time.monotonic()
xp=list(combinations_with_replacement(range(4),2));zp=list(combinations_with_replacement(range(6),2))
J1=[0,1,3,4];J2=[1,2,4,5]

def index(ex,i,j):
    xx=tuple(n for n,k in enumerate(ex) for _ in range(k))
    assert len(xx)==2
    return xp.index(xx)*21+zp.index(tuple(sorted((i,j))))

closed=[]
for component in range(4):
    for triple in combinations_with_replacement(range(4),3):
        ex=[triple.count(i) for i in range(4)];vec=[0]*210
        for i,j in combinations(range(4),2):
            for derivative,sign in [(i,1 if j==component else 0),(j,-1 if i==component else 0)]:
                if sign and ex[derivative]:
                    reduced=ex.copy();reduced[derivative]-=1;coefficient=sign*ex[derivative]
                    vec[index(reduced,J1[i],J2[j])]+=coefficient
                    vec[index(reduced,J1[j],J2[i])]-=coefficient
        closed.append(vec)
Hf=S.hessian(p.F,p.x);Hd=S.hessian(p.q*p.q,p.x)
Ef=p.coefficient_vector((p.B1.T*Hf*p.B1)[0]+(p.B2.T*Hf*p.B2)[0])
Ed=p.coefficient_vector((p.B1.T*Hd*p.B1)[0]+(p.B2.T*Hd*p.B2)[0])
saved=json.loads((ROOT/'PAIRINGS.json').read_text())
Jf=list(map(Q,saved['rows'][0]['mixed_coefficient_vector']))
Jd=list(map(Q,saved['rows'][1]['mixed_coefficient_vector']))
zero=[0]*210
rows=[v+zero for v in closed]+[zero+v for v in closed]
rows += [Jf+zero,[-10*x for x in Jd]+Jf,zero+Jd]
M=S.Matrix(rows);rref,pivots=M.rref();free=[i for i in range(420) if i not in pivots]
# Gaussian compatible-jet interior, checked here against ALL constraints.
cov=[[0]*6 for _ in range(6)]
for off in (0,3):
    for i,row in enumerate([[3,0,1],[0,1,0],[1,0,3]]):
        for j,val in enumerate(row):cov[off+i][off+j]=val
interior=[Q(int(i==j)*cov[k][l]) for i,j in xp for k,l in zp]
assert M*S.Matrix(interior+zero)==S.zeros(M.rows,1)
numeric=np.load(ROOT/'PARAMETER_DUAL_0_10.npz')
target=np.r_[numeric['L0']+1e-7*np.array(interior,float),numeric['L1']]
exact=[Q(0)]*420
for i in free:exact[i]=Q(round(float(target[i])*10**13),10**13)
for row,pivot in reversed(list(enumerate(pivots))):
    exact[pivot]=-sum((Q(rref[row,j])*exact[j] for j in free),Q(0))
assert M*S.Matrix(exact)==S.zeros(M.rows,1)
L0,L1=exact[:210],exact[210:]

def dot(a,b):return sum((x*y for x,y in zip(a,b)),Q(0))
def moment(lam):
    return [[lam[xp.index(tuple(sorted((i//6,j//6))))*21+zp.index(tuple(sorted((i%6,j%6))))] for j in range(24)] for i in range(24)]
def ldl(A):
    n=len(A);L=[[Q(int(i==j)) for j in range(n)] for i in range(n)];D=[]
    for i in range(n):
        di=A[i][i]-sum((L[i][k]**2*D[k] for k in range(i)),Q(0))
        assert di>0,('nonpositive exact pivot',i,di);D.append(di)
        for j in range(i+1,n):L[j][i]=(A[j][i]-sum((L[j][k]*L[i][k]*D[k] for k in range(i)),Q(0)))/di
    assert all(A[i][j]==sum((L[i][k]*D[k]*L[j][k] for k in range(n)),Q(0)) for i in range(n) for j in range(n))
    return D
D0=ldl(moment(L0));Dend=ldl(moment([a+b for a,b in zip(L0,L1)]))
q0=dot(L0,Ef);q1=dot(L1,Ef)-10*dot(L0,Ed);q2=-10*dot(L1,Ed)
bern=[q0,q0+q1/2,q0+q1+q2]
assert all(x<0 for x in bern)
assert dot(L0,Jf)==0 and dot(L1,Jf)-10*dot(L0,Jd)==0 and dot(L1,Jd)==0
out={'status':'EXACT_CONTINUOUS_PARAMETER_SEPARATOR_PASS','gamma_interval':['0','10'],
 'parameterization':'lambda_gamma=L0+(gamma/10)*L1',
 'lambda_L0':[str(x) for x in L0],'lambda_L1':[str(x) for x in L1],
 'all_closed_cubic_oneform_generators':80,'total_constraint_rank':len(pivots),
 'moment_LDL_at_gamma0':[str(x) for x in D0],
 'moment_LDL_at_gamma10':[str(x) for x in Dend],
 'energy_pairing_Bernstein_coefficients':[str(x) for x in bern],
 'mixed_pairing_polynomial_coefficients':['0','0','0'],
 'interior_regularization':'1e-7; first1e-5 trial retained positive LDL but lost the required negative pairing and was rejected',
 'seconds':time.monotonic()-start,
 'scope':'Exact algebraic obstruction for every real mixed-flow b and gamma in[0,10] to closed homogeneous-quadratic corrections and bilinear SOS. Symmetry/parabolic averaging and gamma>10 plane-wave obstruction are separate analytic proof obligations; no QC failure follows.'}
(ROOT/'EXACT_PARAMETER_SEPARATOR.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('lambda_L0','lambda_L1','moment_LDL_at_gamma0','moment_LDL_at_gamma10','energy_pairing_Bernstein_coefficients')},indent=2))
print('Bernstein diagnostic floats:',[float(x) for x in bern])
