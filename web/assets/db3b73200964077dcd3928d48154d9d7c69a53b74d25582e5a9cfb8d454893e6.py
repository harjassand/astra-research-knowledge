#!/usr/bin/env python3
"""Exact KKT/constant/flag/Petz replay. General proofs are in separate texts."""
from fractions import Fraction as F
from pathlib import Path
import json

OUT=Path(__file__).resolve().parent/'EXPOSED_REPLAY_RESULT.json'
cases=[
 {'name':'active_trace_interior','M':F(2),'lam':F(1,64),'c':F(15,16),
  'a':[F(1),F(1)],'z':[F(1),F(1)]},
 {'name':'active_trace_upper_interior_zero','M':F(2),'lam':F(1,64),'c':F(1,2),
  'a':[F(687,256),F(81,256),F(0)],'z':[F(2),F(1),F(0)]},
 {'name':'inactive_trace_upper_zero','M':F(5,2),'lam':F(1,80),'c':F(0),
  'a':[F(3),F(0),F(0)],'z':[F(5,2),F(0),F(0)]},
 {'name':'active_trace_zero_multiplier','M':F(2),'lam':F(1,4),'c':F(0),
  'a':[F(1),F(1)],'z':[F(1),F(1)]}
]
kkt=[]
for v in cases:
 M,lam,c=v['M'],v['lam'],v['c']; a,z=v['a'],v['z']; d=len(a)
 t=sum(z,F(0))/d; delta=sum((max(ai-M,F(0)) for ai in a),F(0))/d
 c0=(1+4*lam*M)**(-2)
 assert sum(a)==d and 0<t<=1 and 0<=c<1
 assert c==0 or t==1
 regimes=[]
 for ai,zi in zip(a,z):
  if ai==0:
   assert zi==0; regimes.append('zero_a_zero_z')
  elif zi==M:
   assert ai>=M*(c+4*lam*M)**2; regimes.append('upper_clipped')
  else:
   assert 0<zi<M and ai==zi*(c+4*lam*zi)**2
   regimes.append('positive_interior')
  assert zi>=c0*min(ai,M)
 assert t>=c0*(1-delta)
 half_error=sum((abs(ai-zi/t) for ai,zi in zip(a,z)),F(0))/(2*d)
 assert half_error<=1-c0*(1-delta)<=delta+(1-c0)
 eps=16*lam*M
 if eps<=F(1,2) and delta<=eps/2:
  assert t>=F(16,27)>F(1,2) and half_error<=eps
 kkt.append({'case':v['name'],'scope':'GENERAL scalar KKT lemma; not required to realize exponential M',
             'M':str(M),'lambda':str(lam),'c_2k':str(c),'trace':str(t),
             'a':[str(ai) for ai in a],'z':[str(zi) for zi in z],
             'regimes':regimes,'delta':str(delta),'c0':str(c0),
             'normalized_half_error':str(half_error),'certificate':'PASS'})

flags=[]
for n in (1,2,4,8,16):
 p0=F(1,n+1); p=[F(1,j*(j+1)) for j in range(1,n+1)]
 assert p0+sum(p,F(0))==1
 for k in range(0,n+3):
  tail=sum(p[k:],F(0))
  assert tail<=F(1,k+1)
  if k<=n: assert tail==F(1,k+1)-F(1,n+1)
 coeff=sum((j*p[j-1] for j in range(1,n+1)),F(0))
 assert coeff==sum((F(1,j) for j in range(1,n+2)),F(0))-1
 dim=1+sum(2**j for j in range(1,n+1))
 assert dim==2**(n+1)-1
 assert p0!=F(1,dim)  # uniform ambient center is outside this convex hull
 flags.append({'N':n,'dimension':dim,'label_count':str(2**(n*(n+1)//2)),
               'vacuum_mass':str(p0),'capacity_ln2_coefficient':str(coeff),
               'all_discrete_tail_bounds':'PASS','center_nontracial':True})

def matmul(a,b):
 return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]

def outer(v):
 return [[x*y for y in v] for x in v]

def zero(n):
 return [[F(0) for _ in range(n)] for _ in range(n)]

petz=[]
for name,p in [('nonunital_faithful_output',[[F(1),F(1,2)],[F(0),F(1,2)]]),
               ('nonunital_singular_output',[[F(1),F(1)],[F(0),F(0)]])]:
 d=2; sigma=[F(1,2),F(1,2)]
 assert all(sum(p[i][j] for i in range(d))==1 for j in range(d))
 nu=[sum((p[i][j]*sigma[j] for j in range(d)),F(0)) for i in range(d)]
 r=[[sigma[j]*p[i][j]/nu[i] if nu[i]>0 else sigma[j]
     for i in range(d)] for j in range(d)]
 assert all(sum(r[j][i] for j in range(d))==1 for i in range(d))
 assert [sum((r[j][i]*nu[i] for i in range(d)),F(0)) for j in range(d)]==sigma
 s=matmul(r,p)
 assert s==[list(row) for row in zip(*s)]
 assert all(sum(s[i][j] for i in range(d))==1 for j in range(d))
 assert all(sum(s[i][j] for j in range(d))==1 for i in range(d))
 assert all(s[i][i]>=0 for i in range(d)) and s[0][0]*s[1][1]-s[0][1]*s[1][0]>=0
 # Actual corrected joint channel: random same raw output l, then apply
 # the same stochastic R independently to each correlated output register.
 joint=[[[sum((p[l][j]*r[i][l]*r[k][l] for l in range(d)),F(0))
           for k in range(d)] for i in range(d)] for j in range(d)]
 for j in range(d):
  assert all(v>=0 for row in joint[j] for v in row)
  assert sum((sum(row,F(0)) for row in joint[j]),F(0))==1
  for i in range(d):
   assert sum(joint[j][i],F(0))==s[i][j]
   assert sum(joint[j][k][i] for k in range(d))==s[i][j]
 # HS matrix S kills off-diagonal input units. Dephasing D is a common
 # pure canonical comparator, with an exact full-space C4 Gram certificate.
 shs=zero(4)
 for i in range(d):
  for j in range(d): shs[3*i][3*j]=s[i][j]
 dp=zero(4); dp[0][0]=dp[3][3]=F(1)
 gamma=[[3*F(i==j)+dp[i][j]-4*shs[i][j] for j in range(4)] for i in range(4)]
 v=[F(1),F(0),F(0),F(-1)]; vgram=outer(v)
 cert=[[4*(1-s[0][0])*vgram[i][j] for j in range(4)] for i in range(4)]
 cert[1][1]+=3;cert[2][2]+=3
 assert gamma==cert and 1-s[0][0]>=0
 if any(x==0 for x in nu):
  # The uncompleted Petz would have a zero column, hence would not be TP.
  assert all(p[i][j]==0 for i in range(d) if nu[i]==0 for j in range(d))
 petz.append({'case':name,'Phi_diagonal_matrix':[[str(v) for v in row] for row in p],
              'nu':[str(v) for v in nu],'Petz_completed_matrix':[[str(v) for v in row] for row in r],
              'S_matrix':[[str(v) for v in row] for row in s],
              'TP_unital_HSpositive_HSselfadj_actual_joint':'PASS',
              'fixed_canonical_dephasing_C4_Gram_certificate':'PASS',
              'singular_output_completion_used':any(x==0 for x in nu)})

checks={
 'trace_lower_c0':F(8,9)**2*F(3,4)==F(16,27)>F(1,2),
 'sqrt2_upper_10over7':F(10,7)**2>2,
 'sqrt80_upper_9':9**2>80,
 'Xi_coefficient_less_5':F(33,16)*F(10,7)+1<5,
 'beta_bracket187over7_less27':(1+F(10,7))*9+2*F(10,7)+2==F(187,7)<27,
 'Petz_power_coefficient':4+F(3,2)*F(3,2)==F(25,4),
 'EB_sqrt5over2_less6over5':F(5,4)<F(6,5)**2,
 'prefactor_27root_less5over3':27<F(5,3)**8,
 'prefactor_8':F(24,5)*F(5,3)==8,
 'M_exponent':F(9,8)*2==F(9,4),
 'b_exponent':F(1,4)*F(1,8)==F(1,32),
 'epsilon_exponent':F(1,2)*F(1,8)==F(1,16),
 'optimized_tail_exponent':F(9,4)/144-F(1,32)==-F(1,64),
 'ratio_exponent':1+F(1,16)==F(17,16),
 'derivative68_less288':F(17,16)*64==68<288,
 'boundary_exponent':F(288,64)==F(9,2),
 '2power17over16_less3':2**17<3**16,
 'boundary_exp_lower':F(5,2)**4==F(625,16)>24,
 'constant432_less500':3*144==432<500,
 'large_branch_trivial':500>288,
 'flag_tail_mass_factor':2+2*F(1)<=4
}
assert all(checks.values()),checks
result={'status':'EXACT_EXPOSED_REPLAY_PASS',
        'scope':'Specified KKT/Petz/flag constructions and rational scalar reductions; general proofs in audit texts',
        'arithmetic':'Fractions and integers; no numerical optimizer or random scan',
        'scalar_KKT_cases':kkt,'flag_separation_replays':flags,
        'fixed_Psi_Petz_replays':petz,'rate_constant_checks':checks}
OUT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'KKT_cases':len(kkt),
                 'flag_constructions':len(flags),'fixed_Petz_constructions':len(petz),
                 'exact_rate_constant_checks':len(checks),'output':str(OUT)},indent=2))
