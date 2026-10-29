"""Exact all-control quotient checks; no sampled-word inference of equality."""
import sympy as s, itertools, json
from finite_boundary_tests import rowgen, exclusion
u,v,A,B,alpha,beta,kappa=s.symbols('u v A B alpha beta kappa',positive=True)
m=3;n=m+2
edges={(0,1):A,(1,0):B}
for i in range(2,n):
 edges[1,i]=edges[i,1]=1
 edges[i,2+(i-2+1)%m]=u
 edges[i,2+(i-2-1)%m]=v
Q=rowgen(n,edges)
def check_quotient(L,labels):
 unique=list(dict.fromkeys(labels));index={c:i for i,c in enumerate(unique)}
 P=s.zeros(L.rows,len(unique))
 for i,c in enumerate(labels):P[i,index[c]]=1
 LP=L*P;rep=[labels.index(c) for c in unique];bar=LP[rep,:]
 assert (LP-P*bar).applyfunc(s.simplify)==s.zeros(*LP.shape)
 return unique,bar
states,L=exclusion(Q,cap=n,alpha=alpha,beta=beta)
labels=[(int(0 in z),int(1 in z),sum(i>=2 for i in z)) for z in states]
parts,bar=check_quotient(L,labels)
assert bar.diff(u)==bar.diff(v)==s.zeros(*bar.shape)
# Pair of labeled independently moving replicas plus same-site annihilation.
C=s.kronecker_product(Q,s.eye(n))+s.kronecker_product(s.eye(n),Q)
C=s.Matrix(C.row_join(s.zeros(n*n,1)).col_join(s.zeros(1,n*n+1)))
for i in range(n):
 index=i*n+i;C[index,index]-=kappa;C[index,n*n]=kappa
pairlabels=[]
for i in range(n):
 for j in range(n):
  if i<2 and j<2:label=('out',i,j)
  elif i<2:label=('left',i)
  elif j<2:label=('right',j)
  else:label=('both',(j-i)%m)
  pairlabels.append(label)
pairlabels.append(('dead',))
parts2,cbar=check_quotient(C,pairlabels)
assert (cbar.diff(u)-cbar.diff(v)).applyfunc(s.simplify)==s.zeros(*cbar.shape)
# A known product start (0,0) is an accessible boundary pair; if co-location
# at0 is physically undesirable, use different labeled injection times.
# Every possible boundary-only start/stop/input respects the same partition.
qbase=Q.subs({A:1,B:1});assert s.ones(1,n)*qbase==s.zeros(1,n)
assert qbase*s.ones(n,1)==s.zeros(n,1)
# Constant-activity path u=2-eps,v=eps: equilibrium eps=1 and EP diverges eps→0.
# This algebra is the complete proof; code additionally checks two exact models.
qeq=qbase.subs({u:1,v:1});qneq=qbase.subs({u:s.Rational(19,10),v:s.Rational(1,10)})
assert cbar.subs({u:1,v:1})==cbar.subs({u:s.Rational(19,10),v:s.Rational(1,10)})
out={'site_count':n,'module_size':m,'full_exclusion_states':len(states),'exclusion_quotient_states':len(parts),'exclusion_all_u_v_A_B_alpha_beta_symbolic_identity':'PASS','two_replica_states_with_dead':C.rows,'contact_quotient_states':len(parts2),'contact_depends_only_on_u_plus_v':'PASS','stationary_one_particle':'uniform 1/5','one_particle_entropy':'(3/5)*(u-v)*log(u/v)','fixed_activity_path':'u=2-epsilon,v=epsilon,0<epsilon<=1','entropy_at_19_over_10_1_over_10':float(s.Rational(3,5)*s.Rational(18,10)*s.log(19)),'rate_bound':2,'source_controls':'A(t),B(t),alpha(t),beta(t); all nonanticipating boundary feedback inherited from exact controlled lumpability','contact_controls':'A(t), B(t), kappa(t); labeled boundary observations; pair entrance through gateway; same physical site reaction','exclusion_quotient_labels':parts,'contact_quotient_labels':parts2}
print(json.dumps(out,indent=2))
