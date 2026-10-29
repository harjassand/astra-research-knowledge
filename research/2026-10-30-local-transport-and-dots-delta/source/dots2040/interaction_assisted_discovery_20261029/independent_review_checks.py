"""Independent reviewer tests of control scope, moments, and exterior-power distinction."""
import sympy as s, itertools, json
from finite_boundary_tests import rowgen, exclusion, q_r
r=s.symbols('r')
states,L=exclusion(q_r(r),k=2);_,R=exclusion(q_r(1-r),k=2)
a=s.zeros(1,len(states));a[0,states.index((0,1))]=1;b=s.Matrix([int(0 in z) for z in states])
p=a;q=a;mom=[]
for j in range(6):
 mom.append(str(s.factor(((p-q)*b)[0])));p=p*L;q=q*R
assert mom[:5]==['0']*5
assert s.factor(s.sympify(mom[5])-23*(2*r-1))==0

# Separate boundary controls for each labeled particle. Internal module rates remain
# the SAME on both particles; no free independent bulk rate modulation.
u,v,A1,B1,A2,B2,k=s.symbols('u v A1 B1 A2 B2 kappa',positive=True)
n=5;m=3
def Q(A,B):
 edges={(0,1):A,(1,0):B}
 for i in range(2,n):
  edges[1,i]=edges[i,1]=1
  edges[i,2+(i-2+1)%m]=u
  edges[i,2+(i-2-1)%m]=v
 return rowgen(n,edges)
C=s.Matrix(s.kronecker_product(Q(A1,B1),s.eye(n))+s.kronecker_product(s.eye(n),Q(A2,B2)))
C=C.row_join(s.zeros(n*n,1)).col_join(s.zeros(1,n*n+1))
for i in range(n):C[i*n+i,i*n+i]-=k;C[i*n+i,n*n]=k
labels=[]
for i,j in itertools.product(range(n),repeat=2):
 if i<2 and j<2:label=('out',i,j)
 elif i<2:label=('left',i)
 elif j<2:label=('right',j)
 else:label=('both',(j-i)%m)
 labels.append(label)
labels.append(('dead',))
classes=list(dict.fromkeys(labels));P=s.zeros(C.rows,len(classes))
for i,c in enumerate(labels):P[i,classes.index(c)]=1
CP=C*P;bar=CP[[labels.index(c) for c in classes],:]
assert (CP-P*bar).applyfunc(s.simplify)==s.zeros(*CP.shape)
assert (bar.diff(u)-bar.diff(v)).applyfunc(s.simplify)==s.zeros(*bar.shape)
assert (C*s.ones(C.rows,1))==s.zeros(C.rows,1)
# Observations: each particle at boundary 0, plus reaction/dead indicator, factor
# through the partition. Including connector occupancy would also factor through it.
obs=[(int(i==0),int(j==0),0) for i,j in itertools.product(range(n),repeat=2)]+[(0,0,1)]
for c in classes:assert len({obs[j] for j,x in enumerate(labels) if x==c})==1

# Exclusion generator has blocked-hop compensated diagonal, unlike exterior
# two-particle generator, whose diagonal is always Q_ii+Q_jj.
Q0=q_r(0);_,E=exclusion(Q0,k=2)
block_correction=[s.factor(E[a,a]-(Q0[i,i]+Q0[j,j])) for a,(i,j) in enumerate(states)]
assert block_correction==[Q0[i,j]+Q0[j,i] for i,j in states]
# Check a signed exterior offdiagonal differs in graph with non-neighbor ordering:
# moving occupied1->3 within state(1,2) produces sign - on sorted(2,3).
def wedge_generator(Q):
 W=s.zeros(len(states))
 for a,z in enumerate(states):
  W[a,a]=sum(Q[i,i] for i in z)
  for p,i in enumerate(z):
   for j in range(Q.rows):
    if j in z:continue
    raw=list(z);raw[p]=j;w=tuple(sorted(raw));sign=(-1)**sum(raw[k]>raw[l] for k in range(2) for l in range(k+1,2))
    W[a,states.index(w)]+=sign*Q[i,j]
 return W
W=wedge_generator(Q0)
assert W!=E
assert W[states.index((1,2)),states.index((2,3))]==-Q0[1,3]
assert E[states.index((1,2)),states.index((2,3))]==Q0[1,3]
out={'r_vs_1_minus_r_derivative_differences_orders_0_to_5':mom,'contact_separate_A1_B1_A2_B2_controls':'PASS','contact_full_record_observation_partition':'PASS','contact_quotient_depends_only_u_plus_v':'PASS','contact_quotient_dim':len(classes),'exclusion_minus_exterior_diagonal':list(map(str,block_correction)),'exclusion_is_not_exterior_power':'PASS'}
print(json.dumps(out,indent=2))

# Stronger operational contact check: each labeled particle may be absent,
# injected at0, or removed at0. Reaction removes both and may be separately
# counted. This tests full boundary interventions without assuming instantaneous
# preparation of an interior pair or observation of an interior contact.
a1,b1,a2,b2=s.symbols('alpha1 beta1 alpha2 beta2',positive=True)
pos=list(range(-1,n));joint=list(itertools.product(pos,repeat=2));idx={z:i for i,z in enumerate(joint)}
Lx=s.zeros(len(joint));Rx=s.zeros(len(joint));qs=[Q(A1,B1),Q(A2,B2)]
for znum,z in enumerate(joint):
 for p in range(2):
  i=z[p]
  if i==-1:
   w=list(z);w[p]=0;Lx[znum,idx[tuple(w)]] += [a1,a2][p]
  else:
   for j in range(n):
    if j==i:continue
    w=list(z);w[p]=j;Lx[znum,idx[tuple(w)]] += qs[p][i,j]
   if i==0:
    w=list(z);w[p]=-1;Lx[znum,idx[tuple(w)]] += [b1,b2][p]
 if z[0]==z[1] and z[0]>=0:Rx[znum,idx[(-1,-1)]]=k;Rx[znum,znum]=-k
 Lx[znum,znum]=-sum(Lx.row(znum))
lab=[]
for i,j in joint:
 if i<2 and j<2:l=('outside',i,j)
 elif i<2:l=('left',i)
 elif j<2:l=('right',j)
 else:l=('both',(j-i)%m)
 lab.append(l)
cl=list(dict.fromkeys(lab));PX=s.zeros(len(joint),len(cl))
for i,c in enumerate(lab):PX[i,cl.index(c)]=1
rep=[lab.index(c) for c in cl]
for name,M in [('boundary_motion_injection_removal',Lx),('reaction',Rx)]:
 MP=M*PX;MB=MP[rep,:]
 assert (MP-PX*MB).applyfunc(s.simplify)==s.zeros(*MP.shape)
 assert (MB.diff(u)-MB.diff(v)).applyfunc(s.simplify)==s.zeros(*MB.shape)
print(json.dumps({'extended_contact_states':len(joint),'extended_contact_quotient_states':len(cl),'separate_boundary_injection_removal_and_counted_reactions':'PASS'},indent=2))
