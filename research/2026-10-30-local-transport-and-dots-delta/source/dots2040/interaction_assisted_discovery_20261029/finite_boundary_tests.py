import sympy as s, itertools, json
from scipy.linalg import expm
import numpy as np

def rowgen(n,edges):
 Q=s.zeros(n)
 for (i,j),v in edges.items():Q[i,j]=v
 for i in range(n):Q[i,i]=-sum(Q.row(i))
 return Q

def exclusion(Q,k=None,cap=None,alpha=0,beta=0):
 n=Q.rows
 states=list(itertools.combinations(range(n),k)) if k is not None else [z for k1 in range(cap+1) for z in itertools.combinations(range(n),k1)]
 idx={z:i for i,z in enumerate(states)};L=s.zeros(len(states))
 for a,z in enumerate(states):
  for i in z:
   for j in range(n):
    if j in z:continue
    w=tuple(sorted(set(z)-{i}|{j}));L[a,idx[w]]+=Q[i,j]
  if k is None:
   if 0 not in z and len(z)<cap:L[a,idx[tuple(sorted((0,)+z))]]+=alpha
   if 0 in z:L[a,idx[tuple(x for x in z if x!=0)]]+=beta
  L[a,a]=-sum(L.row(a))
 return states,L

def q_r(r):
 K=s.Matrix([[-3,1,2],[1,-4,3],[2,3,-5]])
 S=s.Matrix([[1,0,0],[0,1+r,-r],[0,0,1]])
 kr=S.inv()*K*S
 Q=s.zeros(4);Q[0,1]=Q[1,0]=1;Q[0,0]=-1;Q[1:4,1:4]=kr-s.diag(1,0,0)
 return Q

def first_diff(L,R,a,b,maxorder=30):
 v=a;w=a
 for j in range(maxorder+1):
  d=s.factor(((v-w)*b)[0])
  if d:return j,str(d)
  v=v*L;w=w*R
 return None

if __name__=='__main__':
 r=s.Rational(1,10);states,L=exclusion(q_r(r),cap=2,alpha=1)
 _,R=exclusion(q_r(0),cap=2,alpha=1)
 a=s.zeros(1,len(states));a[0,0]=1;b=s.Matrix([int(0 in z) for z in states])
 out={'states':states,'reservoir_first_difference':first_diff(L,R,a,b)}
 times=[.5,1,2,4,8]
 out['finite_boundary_occupancy']=[{'t':t,'equilibrium':float((np.array(a,float)@expm(t*np.array(R,float))@np.array(b,float))[0,0]),'r_01':float((np.array(a,float)@expm(t*np.array(L,float))@np.array(b,float))[0,0])} for t in times]
 _,L2=exclusion(q_r(s.Rational(1,5)),k=2);_,R2=exclusion(q_r(s.Rational(4,5)),k=2)
 a2=s.zeros(1,6);a2[0,0]=1;b2=s.Matrix([int(0 in z) for z in itertools.combinations(range(4),2)])
 out['r_vs_one_minus_r_first_difference']=first_diff(L2,R2,a2,b2)
 _,L3=exclusion(q_r(s.Rational(1,5)),cap=2,alpha=1);_,R3=exclusion(q_r(s.Rational(4,5)),cap=2,alpha=1)
 out['r_vs_one_minus_r_reservoir_first_difference']=first_diff(L3,R3,a,b)
 # Analytic moment Jacobian at integer positive interior point. No parameter fitting.
 rates=s.symbols('a b c d e f');edges={(0,1):1,(1,0):1,**dict(zip([(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)],rates))};Q=rowgen(4,edges)
 point=dict(zip(rates,[1,2,1,3,2,3]))
 for cap in [1,2]:
  st,G=exclusion(Q,cap=cap,alpha=1);g=G.subs(point);dg=[G.diff(p) for p in rates];v=s.zeros(1,len(st));v[0,0]=1;dv=[s.zeros(1,len(st)) for p in rates];b=s.Matrix([int(0 in z) for z in st]);rows=[];selected=[];rank=0
  for j in range(1,25):
   dv=[dv[i]*g+v*dg[i] for i in range(6)];v=v*g;row=s.Matrix([[ (dd*b)[0] for dd in dv]])
   trial=s.Matrix.vstack(*rows,row) if rows else row
   if trial.rank()>rank:
    rows.append(row);selected.append(j);rank+=1
   if rank==6:break
  out[f'cap_{cap}_moment_jacobian']={'rank':rank,'selected_orders':selected,'matrix':[[str(x) for x in rr] for rr in s.Matrix.vstack(*rows).tolist()]}
  if rank==6:out[f'cap_{cap}_moment_jacobian']['determinant']=str(s.Matrix.vstack(*rows).det())
 print(json.dumps(out,indent=2))
