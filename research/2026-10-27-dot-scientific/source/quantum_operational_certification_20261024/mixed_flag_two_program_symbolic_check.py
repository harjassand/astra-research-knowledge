exec(open('quantum_operational_certification_20261024/mixed_flag_two_program_moment.py').read().split('for r in [2,3,5,10,30,100]:')[0])
import sympy as sp
r=sp.symbols('r',positive=True);d=3*r
G=sp.zeros(6)
for i,p in enumerate(perms):
 inv=np.argsort(p)
 for j,q in enumerate(perms):G[i,j]=d**cyc(tuple(inv[q[k]] for k in range(3)))
Gi=G.inv();xs=[sp.Matrix(base[0][i]-base[1][i]).applyfunc(lambda x:sp.Rational(str(round(float(x)*9))))/9*r**(cyc(p)-3) for i,p in enumerate(perms)]
cs=[sum((Gi[j,i]*xs[i] for i in range(6)),sp.zeros(9)).applyfunc(sp.factor) for j in range(6)]
Bs=sp.Matrix([[1/sp.sqrt(2),1/sp.sqrt(6)],[-1/sp.sqrt(2),1/sp.sqrt(6)],[0,-2/sp.sqrt(6)]])
rs=[[sp.ones(1) for p in perms],[sp.Matrix([[round(np.linalg.det(R))]]) for R in R3],[Bs.T*sp.Matrix(R)*Bs for R in R3]]
ms=[d*(d+1)*(d+2)/6,d*(d-1)*(d-2)/6,d*(d*d-1)/3]
for rep,mul in zip(rs,ms):
 block=sum((sp.kronecker_product(cs[i],rep[i]) for i in range(6)),sp.zeros(9*rep[0].rows))*mul*r
 block=block.applyfunc(lambda x:sp.factor(sp.nsimplify(x)))
 
 seen=set();x=sp.symbols("x"); factors=[]
 for start in range(block.rows):
  if start in seen:continue
  comp={start};stack=[start];seen.add(start)
  while stack:
   k=stack.pop()
   for j in range(block.rows):
    if j not in seen and (block[k,j]!=0 or block[j,k]!=0):seen.add(j);comp.add(j);stack.append(j)
  inds=sorted(comp);sub=block.extract(inds,inds);factors.append(sp.factor((x*sp.eye(len(inds))-sub).det()))
 print(factors,flush=True)
