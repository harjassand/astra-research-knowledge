from pathlib import Path
from fractions import Fraction as F
import time,json,hashlib,datetime
started=time.perf_counter();cpu=time.process_time()
b=F(63,100);delta=F(1,2000);rr=F(1,2**500);s=F(1,32);alpha=beta=F(1,2)
q=[b,b*rr,1-b-b*rr]
pi=[delta*b*rr**2,delta*b*rr,1-delta*b*(rr+rr**2)]
w=[pi[i]/q[i] for i in range(3)]
G=[[F(0) for j in range(3)] for i in range(3)]
for i in range(3):
 for j in range(3):
  if i!=j:G[i][j]=q[j]*min(F(1),w[j]/w[i])
 G[i][i]=1-sum(G[i])
L=[[1-s,s,F(0)],[rr*s,1-rr*s,F(0)],[F(0),F(0),F(1)]]
C=[[(F(i==j)+alpha*G[i][j]+beta*L[i][j])/2 for j in range(3)] for i in range(3)]
T=[[C[0][0],16*C[0][1]],[C[1][0]/16,C[1][1]]]
margin=F(3279,3200)-F(2,124)-1
checks={
 'probabilities_strictly_positive':all(x>0 for x in q+pi),
 'probabilities_normalized':sum(q)==1 and sum(pi)==1,
 'unsafe_set_exactly_0_1':[i for i in range(3) if w[i]<F(1,1000)]==[0,1],
 'C_stochastic':all(sum(row)==1 and all(x>=0 for x in row) for row in C),
 'C_pi_reversible':all(pi[i]*C[i][j]==pi[j]*C[j][i] for i in range(3) for j in range(3)),
 'G_killed_row_mass_exact_b_plus_q1':all(sum(G[i][:2])==q[0]+q[1] for i in range(2)),
 'qstar_KL_certificate':q[2]>F(36937,100000)>F(24,65),
 'unsafe_KL_terms_negative':w[0]<1 and w[1]<1,
 'eta_ratio_exact':rr==s**100,
 'theta_transform_exact':rr==(F(1,16))**125,
 'T00_matches':T[0][0]==F(2879,3200),
 'T01_matches':T[0][1]==F(1,8)+4*q[1],
 'norm_power_margin_matches':margin==F(849,99200)>0,
 'probe_integer_bound':F(26,25)**20>2,
 'log1000_certificate':F(27,10)**7>1000,
 'exp_1_01_upper_fraction':F(11,4)*F(100,99)==F(25,9),
 'probe_rho_arithmetic':(1+F(1,2)*F(16,25)*F(26,25)+F(1,2)*F(5,4)*F(26,25))/2==F(4957,5000)
}
assert all(checks.values()),checks
out={'scope':'Independent exact rational reconstruction of the single explicit witness and shared-probe arithmetic from locked submission B; no producer code or broad replay.', 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'norm_power_margin':str(margin),'proof_qualification':'KL uses analytic e>65/24 and negative unsafe terms; p-norm violation uses x^p>=x-(p-1), so no transcendental numerical evaluation was used. Local acceptance fractions use exact roots rr=s^100.', 'wall_seconds':time.perf_counter()-started,'cpu_seconds':time.process_time()-cpu}
p=Path('work/continuous_cycle_0001_review_20261022/instrument_pilot/review/B_EXACT_CHECK.json');p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
