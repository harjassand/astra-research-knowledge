"""Independent exact reconstruction; imports no worker implementation."""
import json
from pathlib import Path
import sympy as s
f=s.Rational
K=s.Matrix([[f(2,15),f(49,120),f(49,120)],
            [f(13,30),f(71,240),f(71,240)],
            [f(13,30),f(71,240),f(71,240)]])
L=(s.eye(3)+s.ones(3)/3)/2
V=s.Matrix([[0,f(2,5),f(2,5)],[f(21,40),f(1,4),f(1,4)],
            [f(2,5),f(11,40),f(11,40)]])
residual=K-V*L
q=f(3,40)
assert all(v>=0 for v in V) and all(v>=0 for v in residual)
assert all(sum(V[:,z])==1-q for z in range(3))
assert all(sum(residual[:,x])==q for x in range(3))
signed=K*L.inv(); assert signed[0,0]==-f(1,20)

# A one-line dual lower certificate for EVERY admissible nonquery kernel.
alpha=s.Matrix([[f(5,2),0,0],[0,f(1,2),f(1,2)],[0,f(1,2),f(1,2)]])
pi=s.Matrix([[0,f(1,2),f(1,2)]])
dual_slack=alpha*L.T-s.ones(3,1)*(pi*L.T)
assert all(v>=0 for v in dual_slack)
cost=sum(alpha[y,x]*K[y,x] for y in range(3) for x in range(3))
assert cost==1-q

def utility(C):
    joint=[(-6*C[y,0]+C[y,1]+C[y,2])/3 for y in range(3)]
    return joint,sum(max(0,v) for v in joint)
jK,uK=utility(K); jL,uL=utility(L)
assert uK==f(1,180) and uL==0

# Reconstruct the accepted N1038 sufficient matrix-covariance certificate,
# including singular K; no comparison coefficient is optimized numerically.
P=s.Matrix([[1,0,0],[0,1,0]])
B=s.Matrix([[1,0],[0,1],[-1,-1]])
R=P*L.inv(); D=P*K*B; center=s.Matrix([f(1,3),f(1,3)])
c=f(3,4); blocks=[]
for i in range(3):
    ei=P[:,i]; xi=P*K[:,i]
    M=sum((L[y,i]*R[:,y]*R[:,y].T for y in range(3)),s.zeros(2))
    HL=M-ei*ei.T
    T=s.diag(*xi)-xi*xi.T
    S=D*HL*D.T
    block=c*T-S-(1-c)*(center-xi)*(center-xi).T
    assert block[0,0]>0 and block[1,1]>0 and block.det()>0
    blocks.append({'matrix':[[str(v) for v in block.row(j)] for j in range(2)],
                   'determinant':str(block.det())})

out={'status':'EXACT_INDEPENDENT_RECONSTRUCTION',
     'K':[[str(v) for v in K.row(i)] for i in range(3)],
     'L':[[str(v) for v in L.row(i)] for i in range(3)],
     'unique_signed_garbling':[[str(v) for v in signed.row(i)] for i in range(3)],
     'q_minimax_locally_exact':str(q),
     'dual_slack':[[str(v) for v in dual_slack.row(i)] for i in range(3)],
     'uniform_prior_joint_act_rewards_K':[str(v) for v in jK],
     'uniform_prior_joint_act_rewards_L':[str(v) for v in jL],
     'optimal_reward_K':str(uK),'optimal_reward_L':str(uL),
     'conditional_entropy_upper_from_accepted_N1038_criterion':str(c),
     'N1038_blocks':blocks,
     'claim':'all-finite-quantum-reference Umegaki order does not imply Blackwell/decision order; not a new general theorem or practical advantage'}
Path(__file__).with_name('RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
