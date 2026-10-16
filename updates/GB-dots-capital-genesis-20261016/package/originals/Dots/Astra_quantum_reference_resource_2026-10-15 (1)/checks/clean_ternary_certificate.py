import sympy as s,json
from pathlib import Path
r=s.Rational;Id=s.eye(2)
B=[s.Matrix([[1,2],[2,4]])/9,s.Matrix([[4,2],[2,1]])/9,s.Matrix([[4,-4],[-4,4]])/9]
R=[b+Id/100 for b in B];H=[B[0],-B[1],s.zeros(2)]
assert sum(B,s.zeros(2))==Id and all(b.det()==0 for b in B)
q=r(3,10);C=s.eye(3)/2+s.ones(3)/6
E=q*s.eye(3);E=E.col_join(s.ones(1,3)*(1-q))
delta=r(1,100);N=(1-delta)*s.eye(3)+delta*s.ones(3)/3
EE=E*N;FF=C*N

def outputs(M,blocks):return [sum((M[j,k]*blocks[k] for k in range(3)),s.zeros(2)) for j in range(M.rows)]
def cost(M,RR,HH):return s.factor(sum(s.trace(k*a.inv()*k) for a,k in zip(outputs(M,RR),outputs(M,HH))))
raw=s.factor(cost(E,R,H)-cost(C,R,H));noisy=s.factor(cost(EE,R,H)-cost(FF,R,H));assert raw<0 and noisy<0
assert all(x>0 for x in EE) and all(x>0 for x in FF)
trace=sum(s.trace(a) for a in R);beta=[a/trace for a in R];hh=[h/trace for h in H];gauge=sum(s.trace(h) for h in hh);hh=[h-gauge*a for h,a in zip(hh,beta)]
t=s.Integer(1)
while not all(a[0,0]>0 and a.det()>0 for a in [a+t*h for a,h in zip(beta,hh)]):t/=2
alpha=[a+t*h for a,h in zip(beta,hh)]
assert sum(s.trace(a) for a in alpha)==sum(s.trace(a) for a in beta)==1
assert all(a==a.T.conjugate() and a[0,0]>0 and a.det()>0 for a in alpha+beta)
def Q2(M):return s.factor(sum(s.trace(a*a*b.inv()) for a,b in zip(outputs(M,alpha),outputs(M,beta))))
pair=s.factor(Q2(EE)-Q2(FF));assert pair<0 and pair==t*t*noisy/trace
out={'source_transition_matrix':str(EE),'target_transition_matrix':str(FF),'common_input_noise':str(delta),'source_all_effects_strictly_positive':True,'target_all_effects_strictly_positive':True,'R_blocks':[str(a) for a in R],'H_blocks':[str(a) for a in H],'baseline_trace':str(trace),'tangent_trace':str(sum(s.trace(h) for h in H)),'original_gap':str(raw),'original_gap_decimal':float(raw),'noisy_gap':str(noisy),'noisy_gap_decimal':float(noisy),'step':str(t),'alpha_blocks':[str(a) for a in alpha],'beta_blocks':[str(a) for a in beta],'direct_pair_Q2_gap':str(pair),'pair_gap_decimal':float(pair),'all_checks_exact':True}
assert json.loads(Path(__file__).with_name('clean_ternary_certificate.json').read_text()) == out, 'Exact fixture mismatch';print(json.dumps(out,indent=2))
