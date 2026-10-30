"""Exact actual-gradient capacity controls on the covariance boundary.

Universal arguments are in the accompanying proof. This receiver checks
all cubic identities, concrete full-covariance rank-one-valued maps,
two-ray product fields, the uniform quartic margin and the local-map
no-go's polynomial algebra. No unrestricted QC conclusion is inferred.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import product,combinations
import importlib.util,json,time,sys
HERE=Path(__file__).resolve().parent;root=next(p for p in HERE.parents if (p/"outputs/hopf_structure/certificate.json").is_file());sp=importlib.util.spec_from_file_location('compat',root/'outputs/gradient_compatibility/receive.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g);d=g.gauge();b,ca,r=g.b,g.ca,g.r;F,C0,T=r.m.acquired();start=time.perf_counter();source=json.loads((root/'outputs/hopf_structure/certificate.json').read_text());kk=list(map(R,source['ray']['K_coefficients']));K=[[kk[0],kk[1],kk[2]],[kk[1],kk[3],kk[4]],[kk[2],kk[4],kk[5]]];b.pd([[v-R(int(i==j),2) for j,v in enumerate(row)] for i,row in enumerate(K)])
allcubics=[{tuple(pw):R(1)} for pw in d['powers']]
def det(A):return A[0]*A[3]-A[1]*A[2]
def avg(P,law):return sum(w*b.evaluate(P,A) for w,A in law)
def rankone_law(law):
 assert all(w>0 and det(A)==0 and any(A) for w,A in law);assert sum(w for w,A in law)==1;assert all(sum(w*A[i] for w,A in law)==0 for i in range(4));S=[[sum(w*A[i]*A[j] for w,A in law) for j in range(4)] for i in range(4)];f=avg(F,law);four=avg(b.mul(T,T),law);cost=sum(w*g.quadratic([[b.evaluate(P,A) for P in row] for row in d['HF']],[v/3 for v in A])/2 for w,A in law);assert cost==2*f/3 and f-cost>=four/6
 for C in allcubics:assert sum(w*sum(b.evaluate(b.diff(C,i),A)*A[i]/3 for i in range(4)) for w,A in law)==avg(C,law)
 return S,f,four,cost
# An actual piecewise affine periodic composition, not a free-law guess:
# psi=f_p(x)+f_q(y), f tent waves from -1 to 1 and back, breakpoints p,q;
# phi=(min(psi,0),max(psi,0)). Values and slope choices are independent.
p,q=R(1,3),R(2,5);sx=[(p,R(2)/p),(1-p,-R(2)/(1-p))];sy=[(q,R(2)/q),(1-q,-R(2)/(1-q))];law=[]
for output,(wx,x),(wy,y) in product((0,1),sx,sy):
 A=[x,y,R(0),R(0)] if output==0 else [R(0),R(0),x,y];law.append((wx*wy/2,A))
S,f,four,cost=rankone_law(law);b.pd(S);rankone_example={'construction':'phi=(min(f_1/3(x)+f_2/5(y),0),max(f_1/3(x)+f_2/5(y),0)); f_p is the periodic tent from -1 to 1 at time p and back to -1 at time 1','weights':[str(w) for w,A in law],'rays':[list(map(str,A)) for w,A in law],'backgrounds':[[str(v/3) for v in A] for w,A in law],'covariance':[list(map(str,row)) for row in S],'quartic_moment':str(f),'radial_fourth_moment':str(four),'explicit_cost':str(cost),'strict_budget':str(f-cost)}
# Check all eight charge directions are detected by actual maps in this class.
detect=[];rotations=[(R(1),R(0)),(R(0),R(1)),(R(3,5),R(4,5)),(R(-4,5),R(3,5))];E=d['charge_representatives'];EP=[{tuple(pw):E[k][j] for k,pw in enumerate(d['powers']) if E[k][j]} for j in range(8)]
for gamma,(x,y) in product((0,1),rotations):
 transformed=[]
 for w,A in law:
  if gamma:A=[A[3],-A[2],A[1],-A[0]]
  A=[x*A[0]-y*A[2],x*A[1]-y*A[3],y*A[0]+x*A[2],y*A[1]+x*A[3]];transformed.append((w,A))
 rankone_law(transformed);H=[[avg(P,transformed) for P in row] for row in d['HF']];v=[avg(b.diff(F,i),transformed) for i in range(4)];hv=r.m.linear_solve(H,v);row=[]
 for C in EP:w=[avg(b.diff(C,i),transformed) for i in range(4)];row.append(avg(C,transformed)-g.dot(hv,w))
 detect.append(row)
charge_rank=b.rank(detect)
# Actual two-direction fields, with skew one-dimensional profiles.
alpha,beta=R(1,2),R(-1,3);base=[([R(1),R(0)],[1,0]),([R(0),R(1)],[0,1])];product_fields=[]
for gamma,(x,y) in product((0,1),rotations):
 modes=[];rays=[]
 for (u,k),aa in zip(base,(alpha,beta)):
  if gamma:u=[u[1],u[0]];k=[k[1],-k[0]]
  u=[x*u[0]-y*u[1],y*u[0]+x*u[1]];Rj=[u[i]*k[j] for i,j in product(range(2),repeat=2)];rays.append(Rj);modes +=[{'frequency':k,'sine':list(map(str,u))},{'frequency':[2*v for v in k],'sine':[str(aa*v/2) for v in u]}]
 G=r.m.gradient(modes);S=[[r.m.average(b.mul(b.var(4,i),b.var(4,j)),G) for j in range(4)] for i in range(4)];assert b.rank(S)==2;mom=[]
 for aa in (alpha,beta):mom.append((R(1,2)*(1+aa*aa),3*aa/4,R(3,8)*(1+aa**4)+3*aa*aa/2))
 weights=[z[0] for z in mom];bases=[[v*z[1]/(3*z[0]) for v in Rj] for Rj,z in zip(rays,mom)];assert S==[[sum(w*Rj[i]*Rj[j] for w,Rj in zip(weights,rays)) for j in range(4)] for i in range(4)]
 for C in allcubics:assert sum(w*sum(b.evaluate(b.diff(C,i),Rj)*A[i] for i in range(4)) for w,Rj,A in zip(weights,rays,bases))==r.m.average(C,G)
 ff=r.m.average(F,G);l4=r.m.average(b.mul(T,T),G);co=sum(w*g.quadratic([[b.evaluate(P,Rj) for P in row] for row in d['HF']],A)/2 for w,Rj,A in zip(weights,rays,bases));assert ff-co>=ff/3>=l4/6;product_fields.append({'modes':modes,'weights':list(map(str,weights)),'rays':[list(map(str,Rj)) for Rj in rays],'backgrounds':[list(map(str,A)) for A in bases],'quartic_moment':str(ff),'radial_fourth_moment':str(l4),'explicit_cost':str(co),'strict_budget':str(ff-co)})

# Universal local positive-covariance completion is impossible. PSD forces
# unique diagonal quadratic forms from their coherent cubic symbols.
pairs=list(combinations(range(4),2));sympairs=[(i,j) for i in range(4) for j in range(i,4)];Mmap=[[R((1 if i==j else 2)*int(i+j==k)) for i,j in sympairs] for k in range(7)];forced=[]
for target,zeros in (([1,0,1,0,0,0,0],[2,3]),([0,0,1,0,1,0,0],[0,3]),([0,0,0,0,1,0,1],[0,1])):
 rows=list(Mmap);rhs=list(map(R,target))
 for z in zeros:
  for j in range(4):ij=(min(z,j),max(z,j));rows.append([R(int(qq==ij)) for qq in sympairs]);rhs.append(R(0))
 sol,rank=ca.solve_range(rows,[[v] for v in rhs]);assert rank==10;mm=[[R(0)]*4 for _ in range(4)]
 for (i,j),v in zip(sympairs,sol):mm[i][j]=mm[j][i]=v[0]
 r.psd(mm);forced.append(mm)
expected=[[[R(int(i==j and i in active)) for j in range(4)] for i in range(4)] for active in ((0,1),(1,2),(2,3))];assert forced==expected;test=[R(0),R(1),R(0),R(0)];vals=[g.quadratic(M,test) for M in forced];assert vals==[1,1,0] and vals[0]*vals[2]-vals[1]**2==-1
coherent=[[R(1),t,t*t,t**3] for t in (R(0),R(1),R(-1),R(2))];assert b.rank(coherent)==4
out={'uniform_quartic_gap':'1/6','rank_one_valued_class':'ALL actual mean-zero periodic L4 gradients with pointwise rank <=1; arbitrary covariance rank','covariance_rank_two_class':'ALL actual mean-zero periodic L4 gradients with covariance rank <=2','leading_coercivity':'F(A)>=|A|^4/2, exact K-I/2 positive definite','full_covariance_rankone_valued_actual_example':rankone_example,'rankone_valued_actual_charge_detection_rank':charge_rank,'two_ray_actual_product_fields':product_fields,'local_positive_quadratic_covariance_completion':'IMPOSSIBLE; exact symbol matching and positivity force a negative principal minor','local_no_go_forced_diagonal_Gram_matrices':[[list(map(str,row)) for row in M] for M in forced],'local_no_go_input_jet':['0','1','0','0'],'local_no_go_principal_minor':'-1','full_unrestricted_capacity':'NOT_RESOLVED','genuine_ROC_QC_separation':False,'seconds':time.perf_counter()-start};(HERE/'certificate.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'rankone_valued_full_covariance_example_exact':True,'actual_rank2_two_ray_controls':len(product_fields),'all_twenty_cubics_matched':True,'uniform_L4_gap':'1/6','nontranslation_detection_rank':charge_rank,'local_no_go_unique_PSD_diagonal_Grams':3,'local_no_go_negative_minor':-1,'full_capacity':'NOT_RESOLVED','seconds':time.perf_counter()-start},indent=2),flush=True)
