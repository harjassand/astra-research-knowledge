"""Independent exact algebra and rigorous real-ball Bernstein reception.

No numerical optimizer or producer polynomial cache is imported. Literal
F, C, primitive and cross data reconstruct all four Schur polynomials.
FLINT/Arb encloses the exact Bernstein coefficients. Positive signs of
det(xI+A)'s coefficients certify PD because A is exactly symmetric.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import combinations,product
from math import comb
import json,time,sys,importlib.util,argparse
from flint import arb,arb_mat,fmpq,ctx
HERE=Path(__file__).resolve().parent
root=next(p for p in HERE.parents if (p/'outputs/hopf_structure/certificate.json').is_file())
sp=importlib.util.spec_from_file_location('literal_poly',root/'outputs/hopf_structure/receive.py');b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
def tr(A):return list(map(list,zip(*A)))
def mm(A,B):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def pm(A,B):return [[b.add(*(b.mul(x,y) for x,y in zip(row,col))) for col in zip(*B)] for row in A]
def inverse(A):
 n=len(A);V=[list(row)+[R(int(i==j)) for j in range(n)] for i,row in enumerate(A)]
 for j in range(n):
  k=next(k for k in range(j,n) if V[k][j]);V[j],V[k]=V[k],V[j];q=V[j][j];V[j]=[x/q for x in V[j]]
  for i in range(n):
   if i!=j:q=V[i][j];V[i]=[x-q*y for x,y in zip(V[i],V[j])]
 return [row[n:] for row in V]
def const(A,n):return [[({(0,)*n:x} if x else {}) for x in row] for row in A]
def wedge(O):
 C=[[{} for _ in range(6)] for _ in range(6)];p1=(0,1,3,4);p2=(1,2,4,5)
 for i in range(4):
  for j in range(4):q=b.scale(O[i][j],R(1,2));C[p1[i]][p2[j]]=b.add(C[p1[i]][p2[j]],q);C[p2[j]][p1[i]]=b.add(C[p2[j]][p1[i]],q)
 return C
def heat(H):
 C=[[{} for _ in range(6)] for _ in range(6)]
 for ids in ((0,1,3,4),(1,2,4,5)):
  for i in range(4):
   for j in range(4):C[ids[i]][ids[j]]=b.add(C[ids[i]][ids[j]],H[i][j])
 return C
def reconstruct(cert):
 source=json.loads((root/'outputs/hopf_structure/certificate.json').read_text());qc=json.loads((root/'outputs/quadratic_boundary/certificate.json').read_text());graded=json.loads((root/'outputs/graded_stabilization/certificate.json').read_text());K=list(map(R,source['ray']['K_coefficients']));A=[b.var(4,i) for i in range(4)];T=b.add(*(b.mul(x,x) for x in A));T2=b.mul(T,T)
 X=b.add(b.mul(A[0],A[0]),b.mul(A[2],A[2]),b.scale(b.mul(A[1],A[1]),-1),b.scale(b.mul(A[3],A[3]),-1));Y=b.scale(b.add(b.mul(A[0],A[1]),b.mul(A[2],A[3])),2);Z=b.scale(b.add(b.mul(A[0],A[3]),b.scale(b.mul(A[1],A[2]),-1)),2);forms=(b.mul(X,X),b.scale(b.mul(X,Y),2),b.scale(b.mul(X,Z),2),b.mul(Y,Y),b.scale(b.mul(Y,Z),2),b.mul(Z,Z));F=b.add(*(b.scale(q,k) for q,k in zip(forms,K)))
 C0={tuple(pw):R(v) for pw,v in zip(graded['cubic_powers'],qc['example_cubic_coefficients']) if R(v)};assert sum(map(abs,C0.values()))==1
 HF=[[b.diff(b.diff(F,i),j) for j in range(4)] for i in range(4)];HC=[[b.diff(b.diff(C0,i),j) for j in range(4)] for i in range(4)];P=[b.literal(q,4) for q in cert['leading_primitive']];assert all(sum(e)==5 for q in P for e in q)
 JA=[b.scale(A[2],-1),b.scale(A[3],-1),A[0],A[1]];jt=[P[2],P[3],b.scale(P[0],-1),b.scale(P[1],-1)];perm=(3,2,1,0);sgn=(1,-1,1,-1)
 for i in range(4):
  assert not b.add(*(b.mul(b.diff(P[i],j),JA[j]) for j in range(4)),jt[i]);assert not b.add(b.transform(P[i],perm,sgn),b.scale(P[perm[i]],-sgn[i]))
 assert b.transform(F,perm,sgn)==F
 O=[[{} for _ in range(4)] for _ in range(4)]
 for i,j in combinations(range(4),2):O[i][j]=b.add(b.mul(T,b.add(b.diff(P[j],i),b.scale(b.diff(P[i],j),-1))),b.scale(b.add(b.mul(A[i],P[j]),b.scale(b.mul(A[j],P[i]),-1)),-2));O[j][i]=b.scale(O[i][j],-1)
 Cf=heat([[b.mul(T2,q) for q in row] for row in HF]);OW=wedge(O);Cf=[[b.add(x,y) for x,y in zip(row,rr)] for row,rr in zip(Cf,OW)]
 Mp=[[b.literal(q,2) for q in row] for row in cert['leading_lift']];assert Mp==tr(Mp);bb=R(source['ray']['A0'][1]);L=[[R(int(i==source['permutation'][j])) for j in range(6)] for i in range(6)]
 for i in range(6):L[i][0]+=bb*R(int(i==source['permutation'][3]))
 eta0,zeta0=map(R,source['ray']['canonical_zero']);w=b.add(b.var(2,0),{(0,0):-eta0});g=b.add(b.var(2,1),{(0,0):-zeta0});DD=[[{} for _ in range(6)] for _ in range(7)];DD[0][0]=w;DD[1][0]=g
 for j in range(1,6):DD[j+1][j]={(0,0):R(1)}
 CP=pm(const(tr(L),2),pm([[b.contract(q) for q in row] for row in Cf],const(L,2)));assert CP==pm(tr(DD),pm(Mp,DD))
 OC=[[{} for _ in range(4)] for _ in range(4)];OQ=[[{} for _ in range(4)] for _ in range(4)];pairs=list(combinations(range(4),2));co=list(map(lambda row:list(map(R,row)),cert['cubic_closed_form']));qo=list(map(R,cert['quadratic_closed_form']));XX=[[[R(v) for v in row] for row in V] for V in cert['linear_cross_coefficients']]
 for k,(i,j) in enumerate(pairs):OC[i][j]=b.add(*(b.scale(a,v) for a,v in zip(A,co[k])));OC[j][i]=b.scale(OC[i][j],-1);OQ[i][j]={(0,0,0,0):qo[k]} if qo[k] else {};OQ[j][i]=b.scale(OQ[i][j],-1)
 for i,j,k in combinations(range(4),3):assert not b.add(b.diff(OC[j][k],i),b.scale(b.diff(OC[i][k],j),-1),b.diff(OC[i][j],k))
 BC=heat(HC);CW=wedge(OC);BC=[[b.add(x,y) for x,y in zip(row,rr)] for row,rr in zip(BC,CW)]
 for a in range(4):
  pt=[R(int(a==i)) for i in range(4)]
  for i in range(6):
   for j in range(6):assert XX[a][i][j]+XX[a][j][i]==b.evaluate(BC[i][j],pt)
 nu=R(cert['nu']);QW=wedge(OQ);DQ=[[b.evaluate(QW[i][j],[R(0)]*4)+(2*nu*(2 if i%3==1 else 1) if i==j else 0) for j in range(6)] for i in range(6)];b.pd(DQ);DI=inverse(DQ)
 e,f,t=[b.var(3,i) for i in range(3)];one={(0,0,0):R(1)};zero={};Ah=[one,e,zero,f];Ts=b.add(one,b.mul(e,e),b.mul(f,f));Ts2=b.mul(Ts,Ts);w=b.add(e,b.scale(one,-eta0));g=b.add(f,b.scale(one,-zeta0));DD=[[{} for _ in range(6)] for _ in range(7)];DD[0][0]=w;DD[1][0]=g
 for j in range(1,6):DD[j+1][j]=one
 GA=[[R(0)]*4 for _ in range(4)];GH=[[R(0)]*6 for _ in range(6)]
 for i,(j,s) in enumerate(zip((3,2,1,0),(1,-1,1,-1))):GA[i][j]=R(s)
 for i,(j,s) in enumerate(zip((5,4,3,2,1,0),(1,-1,1,1,-1,1))):GH[i][j]=R(s)
 rho2=b.add(one,b.mul(t,t));rho4=b.mul(rho2,rho2);charts=[];physical=[]
 for ga,oc in product((0,1),repeat=2):
  x,y=(one,t) if oc==0 else (t,one);UA=[[x,zero,b.scale(y,-1),zero],[zero,x,zero,b.scale(y,-1)],[y,zero,x,zero],[zero,y,zero,x]];UH=[[zero for _ in range(6)] for _ in range(6)]
  for j in range(3):UH[j][j]=x;UH[j][j+3]=b.scale(y,-1);UH[j+3][j]=y;UH[j+3][j+3]=x
  if ga:UA=pm(UA,const(GA,3));UH=pm(UH,const(GH,3))
  Av=[b.add(*(b.mul(a,c) for a,c in zip(row,Ah))) for row in UA];XP=[[b.add(*(b.scale(Av[a],XX[a][i][j]) for a in range(4))) for j in range(6)] for i in range(6)];YY=pm(const(tr(L),3),pm(tr(UH),XP));N=[[{} for _ in range(6)] for _ in range(7)]
  for j in range(6):N[0][j]=b.diff(YY[0][j],0);N[1][j]=b.diff(YY[0][j],1);assert YY[0][j]==b.add(b.mul(w,N[0][j]),b.mul(g,N[1][j]))
  for i in range(1,6):N[i+1]=YY[i]
  cost=pm(N,pm(const(DI,3),tr(N)));G=[[b.add(b.mul(rho4,{(a,c,0):v for (a,c),v in Mp[i][j].items()}),b.scale(b.mul(Ts2,cost[i][j]),-1)) for j in range(7)] for i in range(7)];assert G==tr(G);charts.append(G);physical.append(pm(tr(DD),pm(G,DD)))
 print('Exact reconstruction passed: primitive, symmetries, closed forms, cross identity, four Schur identities.',flush=True)
 return charts,physical

def ball(q):return arb(fmpq(q.numerator,q.denominator))
class Tensor:
 def __init__(self,dims,vals):self.dims=dims;self.vals=vals
 def ix(self,x):return (x[0]*self.dims[1]+x[1])*self.dims[2]+x[2]
 def line_indices(self,k):
  axes=[j for j in range(3) if j!=k]
  for other in product(*(range(self.dims[j]) for j in axes)):
   x=[0,0,0]
   for j,v in zip(axes,other):x[j]=v
   line=[]
   for v in range(self.dims[k]):x[k]=v;line.append(self.ix(x))
   yield line
 def split(self,k,q):
  left=[None]*len(self.vals);right=[None]*len(self.vals);half=q==R(1,2);aq=ball(q);ap=ball(1-q);n=self.dims[k]-1
  for line in self.line_indices(k):
   V=[self.vals[i] for i in line];left[line[0]]=V[0];right[line[n]]=V[n]
   for stage in range(1,n+1):
    V=[(a+c)*arb((1,-1)) if half else a*ap+c*aq for a,c in zip(V,V[1:])];left[line[stage]]=V[0];right[line[n-stage]]=V[-1]
  return Tensor(self.dims,left),Tensor(self.dims,right)

def bernstein_global(M,ds):
 n=len(M);dims=tuple(d+1 for d in ds);vals=[arb_mat([[ball(M[i][j].get(ex,R(0))) for j in range(n)] for i in range(n)]) for ex in product(*(range(s) for s in dims))];T=Tensor(dims,vals)
 for axis,deg in enumerate(ds):
  W=[[ball(sum((R(comb(k,j)*(-1)**(k-j)*2**j*comb(i,j),comb(deg,j)) for j in range(min(i,k)+1)),R(0))) for k in range(deg+1)] for i in range(deg+1)];out=[None]*len(vals)
  for line in T.line_indices(axis):
   for i,ii in enumerate(line):
    value=arb_mat(n,n)
    for k,kk in enumerate(line):
     if W[i][k]!=0:value=value+T.vals[kk]*W[i][k]
    out[ii]=value
  T=Tensor(dims,out)
 return T

def cover_tree(leaves):
 edges=[R(s) for leaf in leaves for s in leaf['box']];den=max(q.denominator for q in edges);assert den&(den-1)==0;boxes=[]
 for leaf in leaves:
  raw=tuple(R(s) for s in leaf['box']);assert all((q*den).denominator==1 for q in raw);box=tuple(int(q*den) for q in raw);assert all(-den<=box[2*k]<box[2*k+1]<=den for k in range(3));assert leaf['dimension'] in (6,7);boxes.append(box)
 def build(ids,region):
  if len(ids)==1:
   i=ids[0];assert boxes[i]==region;return {'leaf':i,'seven':leaves[i]['dimension']==7,'six':leaves[i]['dimension']==6}
  choices=[]
  for k in range(3):
   order=sorted(ids,key=lambda i:boxes[i][2*k]);hi=boxes[order[0]][2*k+1]
   for j in range(1,len(order)):
    lo=boxes[order[j]][2*k]
    if hi==lo:choices.append((abs(2*j-len(order)),k,hi,order[:j],order[j:]))
    hi=max(hi,boxes[order[j]][2*k+1])
  assert choices,'cover has an overlap, gap, or non-guillotine partition'
  _,k,c,left,right=min(choices,key=lambda q:q[:3]);rl=list(region);rr=list(region);rl[2*k+1]=c;rr[2*k]=c;L=build(left,tuple(rl));Rr=build(right,tuple(rr));return {'axis':k,'cut':R(c,den),'left':L,'right':Rr,'seven':L['seven'] or Rr['seven'],'six':L['six'] or Rr['six']}
 return build(list(range(len(leaves))),(-den,den,-den,den,-den,den))

def receive(cert,charts,physical):
 start=time.perf_counter();last=start;count=0;boxes=0;bychart=[];six=0;seven=0
 for chart in range(4):
  leaves=[q for q in cert['cover'] if q['chart']==chart];tree=cover_tree(leaves);print('Complete partition reconstructed for chart',chart,'boxes',len(leaves),flush=True);B6=bernstein_global(physical[chart],(8,8,4));B7=bernstein_global(charts[chart],(6,6,4));localcount=0
  def walk(node,region,T6,T7):
   nonlocal count,boxes,last,six,seven,localcount
   if 'leaf' in node:
    leaf=leaves[node['leaf']];assert tuple(map(R,leaf['box']))==region;dim=leaf['dimension'];B=T6 if dim==6 else T7;assert B is not None
    for index,A in enumerate(B.vals):
     poly=A.charpoly()
     for k in range(dim):
      if not poly[k]*((-1)**(dim-k))>0:raise ArithmeticError(('uncertified coefficient',chart,leaf,index,k,str(poly[k])))
    count+=len(B.vals);boxes+=1;localcount+=len(B.vals);six+=int(dim==6);seven+=int(dim==7)
    if time.perf_counter()-last>15:print(json.dumps({'checked_boxes':boxes,'checked_positive_matrices':count,'chart':chart,'seconds':time.perf_counter()-start}),flush=True);last=time.perf_counter()
    return
   axis=node['axis'];cut=node['cut'];q=(cut-region[2*axis])/(region[2*axis+1]-region[2*axis]);assert 0<q<1
   A6,C6=T6.split(axis,q) if node['six'] else (None,None);A7,C7=T7.split(axis,q) if node['seven'] else (None,None);rleft=list(region);rright=list(region);rleft[2*axis+1]=cut;rright[2*axis]=cut
   walk(node['left'],tuple(rleft),A6 if node['left']['six'] else None,A7 if node['left']['seven'] else None);walk(node['right'],tuple(rright),C6 if node['right']['six'] else None,C7 if node['right']['seven'] else None)
  walk(tree,(R(-1),R(1),R(-1),R(1),R(-1),R(1)),B6,B7);bychart.append(localcount)
 return {'nu':cert['nu'],'exact_reconstruction':True,'whole_cube_covered_in_each_of_four_charts':True,'positive_Bernstein_matrices':count,'six_dimensional_boxes':six,'seven_dimensional_boxes':seven,'matrices_by_chart':bychart,'rigorous_ball_precision_bits':ctx.prec,'rigorous_sign_criterion':'all coefficients of det(xI+A) strictly positive; exact A is symmetric','seconds':time.perf_counter()-start,'universal_heat_Gram_verified':True,'QC_at_1859':'UNKNOWN','full_face_QC':'NOT_RESOLVED'}

def main():
 if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
 parser=argparse.ArgumentParser();parser.add_argument('--certificate',default=str(HERE/'certificate.json') if (HERE/'certificate.json').is_file() else str(root/'work/heat_global_certificate.json'));parser.add_argument('--bits',type=int,default=384);args=parser.parse_args();ctx.prec=args.bits;cert=json.loads(Path(args.certificate).read_text());charts,physical=reconstruct(cert);result=receive(cert,charts,physical);Path(args.certificate).with_name('replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
