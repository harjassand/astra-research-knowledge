"""Exact acoustic kernels and singular-mean controls for original J_r.

The full classification uses actual Fourier compatibility in PROOF.txt.
This receiver rebuilds all-r kernel identities and determinant signs,
and checks actual singular-profile mean minima without inversion.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import product
import importlib.util,json,time
HERE=Path(__file__).resolve().parent;sp=importlib.util.spec_from_file_location('singular_mean_algebra',HERE.parent/'quartic_coupling/receive.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
add,mul,sc,power,var,diff=m.add,m.mul,m.sc,m.powp,m.var,m.diff
def rank(A):
 A=[list(row) for row in A];row=0
 for j in range(len(A[0])):
  k=next((i for i in range(row,len(A)) if A[i][j]),None)
  if k is None:continue
  A[row],A[k]=A[k],A[row];v=A[row][j];A[row]=[x/v for x in A[row]]
  for i in range(len(A)):
   if i!=row:
    v=A[i][j];A[i]=[x-v*y for x,y in zip(A[i],A[row])]
  row+=1
 return row
def all_parameter_kernels():
 rp,a,bb,c,d=[var(5,i) for i in range(5)];one5={(0,)*5:R(1)};rp2=add(rp,sc(one5,2));u=add(power(a,2),power(c,2));v=add(power(bb,2),power(d,2));j=add(mul(a,d),sc(mul(bb,c),-1));conf=add(u,v,sc(j,-2));F=add(sc(mul(rp,power(conf,2)),9),sc(mul(mul(rp,add(rp,sc(one5,-1))),mul(rp2,power(u,2))),4),sc(mul(rp2,power(j,2)),24),sc(mul(mul(rp,rp2),mul(u,j)),24));HH=[[diff(diff(F,i+1),j+1) for j in range(4)] for i in range(4)]
 r,x,y=[var(3,i) for i in range(3)];one={(0,)*3:R(1)};tt=sc(add(sc(r,2),one),R(1,3));K1=[sc(y,-1),mul(tt,x),x,mul(tt,y)];K2=[x,sc(y,-1),y,x];R1=[x,{},y,{}];R2=[{},x,{},y]
 for ray,K in ((R1,K1),(R2,K2)):
  H=[[m.substitute(Q,[r]+ray) for Q in row] for row in HH];assert all(not add(*(mul(H[i][j],K[j]) for j in range(4))) for i in range(4))
 d1=add(mul(K1[0],K1[3]),sc(mul(K1[1],K1[2]),-1));d2=add(mul(K2[0],K2[3]),sc(mul(K2[1],K2[2]),-1));assert d1==sc(mul(tt,add(power(x,2),power(y,2))),-1) and d2==add(power(x,2),power(y,2))
 # Receive the positive complementary block and nonzero rank-one block
 # at both axes. Together they prove rank exactly three for every r>0.
 rr=var(1,0);oo={(0,):R(1)};rplus2=add(rr,sc(oo,2));r21=add(sc(rr,2),oo)
 for side in (1,2):
  ray=[oo,{}, {},{}] if side==1 else [{},oo,{},{}];H=[[m.substitute(Q,[rr]+ray) for Q in row] for row in HH]
  if side==1:
   det=add(mul(H[0][0],H[3][3]),sc(mul(H[0][3],H[3][0]),-1));assert det==sc(mul(mul(rr,rplus2),power(r21,2)),576);assert H[1][1]==sc(rr,36);assert not add(mul(H[1][1],H[2][2]),sc(mul(H[1][2],H[2][1]),-1))
  else:
   det=add(mul(H[1][1],H[2][2]),sc(mul(H[1][2],H[2][1]),-1));assert det==sc(mul(rr,rplus2),5184);assert H[0][0]==sc(rr,36);assert not add(mul(H[0][0],H[3][3]),sc(mul(H[0][3],H[3][0]),-1))
 return True
def controls():
 out=[];m2,m3,m4=R(3),R(6),R(21)
 for rr in (R(1,10),R(3,4),R(2)):
  F=m.J(rr,[var(4,i) for i in range(4)]);tp=(2*rr+1)/3;u=(R(2),R(-1));U=[[u[0],-u[1]],[u[1],u[0]]]
  for side in (1,2):
   ray=[u[0],R(0),u[1],R(0)] if side==1 else [R(0),u[0],R(0),u[1]];baseK=[[R(0),tp],[R(1),R(0)]] if side==1 else [[R(1),R(0)],[R(0),R(1)]];K=[sum(U[i][j]*baseK[j][k] for j in range(2)) for i,k in product(range(2),repeat=2)];HF=[[m.evaluate(diff(diff(F,i),j),ray) for j in range(4)] for i in range(4)];DF=[m.evaluate(diff(F,i),ray) for i in range(4)];JR=m.evaluate(F,ray);H=[[m2*v for v in row] for row in HF];v=[m3*x for x in DF];M=[-m3*x/(3*m2) for x in ray]
   assert rank(H)==3 and JR>0 and all(sum(H[i][j]*M[j] for j in range(4))+v[i]==0 for i in range(4));assert all(sum(H[i][j]*K[j] for j in range(4))==0 for i in range(4));assert sum(v[i]*K[i] for i in range(4))==0
   gap=JR*(m4-R(2,3)*m3*m3/m2);assert gap>=JR*m4/3
   for s in (R(0),R(7),R(-13,2)):
    mean=[M[i]+s*K[i] for i in range(4)];direct=m.evaluate(F,[mean[i]+3*ray[i] for i in range(4)])/4+3*m.evaluate(F,[mean[i]-ray[i] for i in range(4)])/4-m.evaluate(F,mean);assert direct==gap
   out.append({'r':str(rr),'axis':side,'actual_profile':'h=3 on one quarter period, h=-1 on three quarters; potential is its periodic primitive','rank_of_mean_matrix':3,'minimizing_mean':list(map(str,M)),'free_kernel_direction':list(map(str,K)),'exact_minimum_gap':str(gap),'exact_quartic_moment':str(JR*m4),'all_means_lower_bound_fraction':'1/3','unbounded_kernel_mean_changes_gap':False})
 return out
def main():
 start=time.perf_counter();assert all_parameter_kernels();sp=importlib.util.spec_from_file_location('singular_mean_original_admission',HERE.parent/'quartic_coupling/original_roc.py');o=importlib.util.module_from_spec(sp);sp.loader.exec_module(o);assert o.verify()['global_rank_one_convexity'];out={'original_Jr_global_ROC_all_r_received':True,'all_parameter_all_output_acoustic_kernels_exact':True,'opposite_axis_kernel_determinant_signs_exact':True,'acoustic_axis_Hessians_rank_three_all_r':True,'actual_singular_mean_matrix_classification':'only one-variable rank-one profiles on a single acoustic axis, plus zero field','covariance_rank_at_least_two_implies_mean_matrix_positive_definite':True,'singular_mean_minimum_is_attained':True,'singular_profile_minimum_bound':'at least one third of the quartic moment, for every r>0','nearby_ill_conditioned_means_uniformly_controlled':'NOT_ASSERTED','controls':controls(),'r_rank3_complete_search_representation':'G=T Hess psi, T invertible; up to output SO2 and scale T=diag(1,sign) P with P SPD determinant one and two real parameters','QC_separation':'NOT_ACHIEVED','seconds':time.perf_counter()-start};(HERE/'replay.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='controls'},indent=2))
if __name__=='__main__':main()
