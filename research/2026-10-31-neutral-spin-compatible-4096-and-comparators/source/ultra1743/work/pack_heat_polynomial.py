"""Reconstruct the exact three-variable Schur lift of a heat proposal.

This writes algebra and float tensors for a cover search. It does NOT
establish positivity or QC until an exact complete cover is received.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import combinations,product
import sys,json,time,pickle,argparse
import numpy as np,scipy.linalg as la
sys.path.insert(0,str(Path(__file__).resolve().parent));import heat_model as h,heat_leading_family as lf
b,r,ca=h.b,h.r,h.ca;root=h.root;start=time.perf_counter()
# Reuse only the exact linear-system construction, stopping before any solve.
ss=(root/'work/graded_heat_lift.py').read_text();ns={'__file__':str(root/'work/graded_heat_lift.py'),'__name__':'heat_root_constraints'};exec(ss[:ss.index('c0=[R(q)')],ns);E,RHS=ns['E'],ns['RHS'];rank=ns['rankE'];qc=ns['qc'];powers=ns['powers']
parser=argparse.ArgumentParser();parser.add_argument('--nu',type=int,default=4096);args=parser.parse_args();proposal=json.loads((root/'work/graded_heat_joint_adaptive_proposal.json').read_text());assert abs(proposal['nu']-2048)<1e-4
z_float=np.array(proposal['all_cross_coefficients']);c0=list(map(R,qc['example_cubic_coefficients']));rhs=[sum(a*c for a,c in zip(row,c0)) for row in RHS]
EN=np.array(E,float);_,_,piv=la.qr(EN,pivoting=True,mode='economic');piv=list(map(int,piv[:rank]));_,_,rpiv=la.qr(EN[:,piv].T,pivoting=True,mode='economic');rows=list(map(int,rpiv[:rank]));free=[j for j in range(80) if j not in piv];z=[R(0)]*80
for j in free:z[j]=R(round(float(z_float[j])*10**15),10**15)
remaining=[rhs[i]-sum(E[i][j]*z[j] for j in free) for i in rows];sol=r.m.linear_solve([[E[i][j] for j in piv] for i in rows],remaining)
for j,v in zip(piv,sol):z[j]=v
assert all(sum(a*v for a,v in zip(row,z))==rr for row,rr in zip(E,rhs))
lead=[R(round(v*10**15),10**15) for v in proposal['leading_primitive_variation']];oq=[R(round(v*10**12),10**12) for v in proposal['quadratic_two_form']];nu=R(args.nu)
print('exact projection max error',max(abs(float(v)-x) for v,x in zip(z,z_float)),flush=True)
# Exact X(A) linear coefficient matrices, with the stipulated symmetric part.
X=[]
for aa in range(4):
 ea=[R(int(i==aa)) for i in range(4)];HC=[[b.evaluate(p,ea) for p in row] for row in h.HC];M=[[R(0) for _ in range(6)] for _ in range(6)]
 for inds in ((0,1,3,4),(1,2,4,5)):
  for i in range(4):
   for j in range(4):M[inds[i]][inds[j]]+=HC[i][j]/2
 for pair,W in enumerate(h.Wedges):
  co=sum(R(float(h.V[pair*4+aa,l]))*z[l] for l in range(20))/2
  for i in range(6):
   for j in range(6):M[i][j]+=co*R(float(W[i,j]))
 for k,(i,j) in enumerate(h.pairs6):M[i][j]+=z[20+15*aa+k];M[j][i]-=z[20+15*aa+k]
 X.append(M)
DQ=[[sum(oq[p]*R(float(h.Wedges[p,i,j])) for p in range(6))+(2*nu*(1 if i%3!=1 else 2) if i==j else 0) for j in range(6)] for i in range(6)];b.pd(DQ);DQinv,_=ca.solve_range(DQ,[[R(int(i==j)) for j in range(6)] for i in range(6)])
Mbase=[[b.literal(p,2) for p in row] for row in h.base['M']];Mlead=[[b.add(Mbase[i][j],*(b.scale(MM[i][j],co) for MM,co in zip(lf.Ms,lead))) for j in range(7)] for i in range(7)]
eta0,zeta0=map(R,h.base['ray']['canonical_zero']);bb=R(h.base['ray']['A0'][1]);perm=h.base['permutation'];L=[[R(int(i==perm[j])) for j in range(6)] for i in range(6)]
for i in range(6):L[i][0]+=bb*R(int(i==perm[3]))
eta,zeta,t=[b.var(3,i) for i in range(3)];one={(0,0,0):R(1)};zero={};Ahat=[one,eta,zero,zeta];T=b.add(one,b.mul(eta,eta),b.mul(zeta,zeta));T2=b.mul(T,T);w=b.add(eta,b.scale(one,-eta0));g=b.add(zeta,b.scale(one,-zeta0));nn=[g,b.scale(w,-1),zero,zero,zero,zero,zero];rho2=b.add(one,b.mul(t,t));rho4=b.mul(rho2,rho2)
GA=[[R(0)]*4 for _ in range(4)]
for i,(j,sgn) in enumerate(zip((3,2,1,0),(1,-1,1,-1))):GA[i][j]=R(sgn)
GH=[[R(0)]*6 for _ in range(6)]
for i,(j,sgn) in enumerate(zip((5,4,3,2,1,0),(1,-1,1,1,-1,1))):GH[i][j]=R(sgn)

def pmul(A,B):
 return [[b.add(*(b.mul(a,bb) for a,bb in zip(row,col))) for col in zip(*B)] for row in A]
def pt(A):return list(map(list,zip(*A)))
def const(A):return [[b.scale(one,v) for v in row] for row in A]

polys=[]
for gamma,chart in product((0,1),repeat=2):
 u=(one,t) if chart==0 else (t,one);x,y=u
 UA=[[x,zero,b.scale(y,-1),zero],[zero,x,zero,b.scale(y,-1)],[y,zero,x,zero],[zero,y,zero,x]];UH=[[zero for _ in range(6)] for _ in range(6)]
 for j in range(3):UH[j][j]=x;UH[j][j+3]=b.scale(y,-1);UH[j+3][j]=y;UH[j+3][j+3]=x
 if gamma:UA=pmul(UA,const(GA));UH=pmul(UH,const(GH))
 A=[r.compose(p,Ahat,3) if False else b.add(*(b.mul(a,bb) for a,bb in zip(row,Ahat))) for row in UA]
 XP=[[b.add(*(b.scale(A[aa],X[aa][i][j]) for aa in range(4))) for j in range(6)] for i in range(6)];Y=pmul(const(ca.transpose(L)),pmul(pt(UH),XP))
 NY=[[{} for _ in range(6)] for _ in range(7)]
 for j in range(6):
  de,dz=b.diff(Y[0][j],0),b.diff(Y[0][j],1);assert Y[0][j]==b.add(b.mul(w,de),b.mul(g,dz));NY[0][j]=de;NY[1][j]=dz
 for i in range(1,6):NY[i+1]=Y[i]
 cost=pmul(NY,pmul(const(DQinv),pt(NY)));G=[]
 for i in range(7):
  row=[]
  for j in range(7):
   ML={(e[0],e[1],0):co for e,co in Mlead[i][j].items()};row.append(b.add(b.mul(rho4,ML),b.scale(b.mul(T2,cost[i][j]),-1)))
  G.append(row)
 assert G==pt(G);assert all(all(e[0]<=6 and e[1]<=6 and e[2]<=4 for e in p) for row in G for p in row)
 polys.append(G);print('Schur chart',gamma,chart,'polynomial entries built',flush=True)
PAD=[[b.mul(rho4,b.mul(a,bb)) for bb in nn] for a in nn]
params={'nu':str(nu),'leading_primitive_variation':list(map(str,lead)),'cross_coefficients':list(map(str,z)),'quadratic_two_form':list(map(str,oq)),'cubic_primitive_closed_linear_two_form':[[str(sum(R(float(h.V[p*4+a,l]))*z[l] for l in range(20))) for a in range(4)] for p in range(6)],'root_constraints_exact':True,'parameter_scope':'EXACT ALGEBRA ONLY. Global polynomial positivity and QC await a complete verified cover.'}
(root/'work/heat_exact_parameters.json').write_text(json.dumps(params,indent=2)+'\n')
with (root/'work/heat_exact_schur.pkl').open('wb') as fp:pickle.dump({'charts':polys,'padding':PAD,'parameters':params},fp)
arr=np.zeros((4,7,7,7,7,5));pa=np.zeros((7,7,7,7,5))
for ch,G in enumerate(polys):
 for i in range(7):
  for j in range(7):
   for e,co in G[i][j].items():arr[(ch,i,j)+e]=float(co)
for i in range(7):
 for j in range(7):
  for e,co in PAD[i][j].items():pa[(i,j)+e]=float(co)
np.savez(root/'work/heat_schur_float.npz',charts=arr,padding=pa)
print('exact Schur construction seconds',time.perf_counter()-start,flush=True)
