"""Independent exact constant-size checks of assigned Luna boundary claims.

No peer code is imported or run. Proof scope remains the displayed fixtures.
"""
from fractions import Fraction as Q
from pathlib import Path
import json

def mm(A,B):
    return [[sum(A[i][a]*B[a][j] for a in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]

def tr(A):return [list(row) for row in zip(*A)]

def diag(v):return [[x if i==j else Q(0) for j,x in enumerate(v)] for i in range(len(v))]

def add(A,B):return [[x+y for x,y in zip(a,b)] for a,b in zip(A,B)]

def fock_permute(occupied,permutation):
    image=[permutation[i] for i in occupied]
    sign=(-1)**sum(image[i]>image[j] for i in range(len(image)) for j in range(i+1,len(image)))
    return tuple(sorted(image)),sign

P=diag([Q(1),Q(0),Q(1),Q(0)])
U=[[Q(1),0,0,0],[0,Q(3,5),Q(-4,5),0],[0,Q(4,5),Q(3,5),0],[0,0,0,Q(1)]]
Qproj=mm(mm(U,P),tr(U))
K=mm(Qproj,P)
effect=mm(tr(K),K)
assert effect==diag([Q(1),0,Q(9,25),0])
E=add(effect,diag([0,Q(1),0,Q(1)]))
assert E==diag([Q(1),Q(1),Q(9,25),Q(1)])
z=sum(E[i][i] for i in range(4))
n1=(E[1][1]+E[3][3])/z
n2=(E[2][2]+E[3][3])/z
n12=E[3][3]/z
assert (n1,n2,n12)==(Q(25,42),Q(17,42),Q(25,84))
assert n12-n1*n2==Q(25,441)
assert z/4==Q(21,25)

pbs=[0,3,2,1]
states=[(0,2),(0,3),(1,2),(1,3)]
branches=[]
for s in states:
    mid,sgn=fock_permute(s,pbs)
    accepted=sum(i<2 for i in mid)==1
    back,sgn2=fock_permute(mid,pbs)
    assert back==s and sgn*sgn2==1
    branches.append(int(accepted))
assert branches==[1,0,0,1]
cnot=[]
for x in (0,1):
    for y in (0,1):
        p1=p2=1
        ancilla=0
        phase=(-1)**((p2+1)*(x+ancilla+p1+1))
        output=(x,(x+y+ancilla+p1+1)%2)
        assert phase==1 and output==(x,(x+y)%2)
        # First Z-parity encoder retains ancilla a=x with amplitude 1/sqrt(2).
        # Second X-parity projector is (I+X_a X_target)/2. Select ancilla zero.
        terms=[(x,y,Q(1,2)),(1-x,1-y,Q(1,2))]
        selected=[(target,amplitude) for a,target,amplitude in terms if a==0]
        assert selected==[((x+y)%2,Q(1,2))]
        probability=selected[0][1]**2/2
        assert probability==Q(1,8)
        cnot.append({'input':[x,y],'output':list(output),'probability':str(probability)})

x=y=Q(1,2)
det_hess=((x*y)**2-1)/(1+x*y)**4
assert det_hess<0
roots=[(Q(1),Q(0)),(Q(0),Q(1)),(Q(-1),Q(0)),(Q(0),Q(-1))]
ys=[(a[0]-b[0])**2+(a[1]-b[1])**2 for a in roots for b in roots]
assert sum(ys)/16==2 and sum(v*v for v in ys)/16==6
result={'status':'PASS_EXACT_RATIONAL_IDENTITIES','adaptive_acceptance':str(z/4),
        'effect_diagonal':[str(E[i][i]) for i in range(4)],'Wick_gap':str(n12-n1*n2),
        'PBS_branch':branches,'selected_CNOT':cnot,'pair_factor_Hessian_determinant':str(det_hess),
        'iid_unit_phase_one_block':{'mean':'2','second_moment':'6','relative_second_moment':'3/2'},
        'scope':'Named constant-size algebra. No arbitrary-input compiler or generic sampler ran.'}
Path(__file__).with_name('review_fixtures.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
