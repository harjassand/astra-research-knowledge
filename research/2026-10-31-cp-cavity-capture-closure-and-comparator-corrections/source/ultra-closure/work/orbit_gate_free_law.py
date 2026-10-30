"""A free-law probe of the gap between the acquired QC cone and ROC.

Every moment is an atomic matrix-law moment. No compatibility or
gradient realization is inferred. Full continuum QC-orbit gates are
received by exact binary-sextic Sturm signs at the selected law.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import product
import json,sys,importlib.util,time
import numpy as np
from scipy.optimize import minimize_scalar
root=Path(__file__).resolve().parents[1];sp=importlib.util.spec_from_file_location('compat',root/'outputs/gradient_compatibility/receive.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g);d=g.gauge();b,ca,r=g.b,g.ca,g.r;start=time.perf_counter();old=json.loads((root/'outputs/gradient_compatibility/free_law.json').read_text());oldtheta=R(old['mixing_parameter']);atoms=[list(map(R,A)) for A in old['atoms']];safe=[(R(1,8),A) for A in atoms[:8]];bad=[(R(w)/oldtheta,A) for w,A in zip(old['atom_weights'][8:],atoms[8:])];F,C0,T=r.m.acquired();HF=d['HF'];DF=[b.diff(F,i) for i in range(4)];A=[b.var(4,i) for i in range(4)];GA=[[R(0)]*4 for _ in range(4)]
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
for i,(j,s) in enumerate(zip((3,2,1,0),(1,-1,1,-1))):GA[i][j]=R(s)
nodes=[(R(1),R(0)),(R(0),R(1)),(R(1),R(1)),(R(1),R(-1))];interp=[[x**3,x*x*y,x*y*y,y**3] for x,y in nodes];I,_=ca.solve_range(interp,[[R(int(i==j)) for j in range(4)] for i in range(4)]);CP=[]
for gamma,(x,y) in product((0,1),nodes):
 UA=[[x,0,-y,0],[0,x,0,-y],[y,0,x,0],[0,y,0,x]]
 if gamma:UA=ca.mm(UA,GA)
 images=[b.add(*(b.scale(p,c) for p,c in zip(A,row))) for row in UA];CP.append(r.compose(C0,images,4))
def avg(P,law):return sum(w*b.evaluate(P,A) for w,A in law)
def moments(law):return {'H':[[avg(P,law) for P in row] for row in HF],'v':[avg(P,law) for P in DF],'B':[[avg(b.diff(P,i),law) for P in CP] for i in range(4)],'c':[avg(P,law) for P in CP],'f':avg(F,law),'s':avg(T,law)}
sa,ba=moments(safe),moments(bad)
def mix(theta,key):
 a,c=sa[key],ba[key]
 if isinstance(a,list):
  if isinstance(a[0],list):return [[(1-theta)*x+theta*y for x,y in zip(row,rr)] for row,rr in zip(a,c)]
  return [(1-theta)*x+theta*y for x,y in zip(a,c)]
 return (1-theta)*a+theta*c
def stats(theta):
 H=mix(theta,'H');B=mix(theta,'B');v=mix(theta,'v');HB,_=ca.solve_range(H,B);hv=r.m.linear_solve(H,v);a=2*mix(theta,'f')-g.dot(v,hv);rr=[c-g.dot(row,hv) for c,row in zip(mix(theta,'c'),ca.transpose(B))];dd=ca.mm(ca.transpose(B),HB);s=mix(theta,'s');return H,B,v,HB,hv,a,rr,dd,s
angle=np.linspace(0,np.pi,1025);U=np.vstack((np.cos(angle),np.sin(angle)));mono=np.stack((U[0]**3,U[0]**2*U[1],U[0]*U[1]**2,U[1]**3),axis=1);Lag=mono@np.array(I,float);Lag=Lag.T
def required(st,refine=False):
 H,B,v,HB,hv,a,rr,dd,s=st
 if a<=0:return (float('inf'),0,0.)
 vals=[]
 for gamma in (0,1):
  r4=np.array(rr[4*gamma:4*gamma+4],float);D4=np.array([row[4*gamma:4*gamma+4] for row in dd[4*gamma:4*gamma+4]],float);values=(np.einsum('ik,ij,jk->k',Lag,D4,Lag)+(r4@Lag)**2/float(a))/(2*float(s));ix=int(np.argmax(values));th=float(angle[ix]);val=float(values[ix])
  if refine:
   def score(th):
    x,y=np.cos(th),np.sin(th);l=np.array([x**3,x*x*y,x*y*y,y**3])@np.array(I,float);return float((l@D4@l+(l@r4)**2/float(a))/(2*float(s)))
   opt=minimize_scalar(lambda x:-score(x),bounds=(th-np.pi/512,th+np.pi/512),method='bounded',options={'xatol':1e-14});th=float(opt.x);val=score(th)
  vals.append((val,gamma,th))
 return max(vals)
left=R(0);right=oldtheta
for iteration in range(240):
 theta=(left+right)/2;st=stats(theta);req=required(st)
 if req[0]<3000:left=theta
 else:right=theta
 if 2900<req[0]<3100:break
else:raise AssertionError('no intermediate orbit-gate law found')
theta=left;st=stats(theta);H,B,v,HB,hv,a,rr,dd,s=st;req=required(st,True);law=[((1-theta)*w,A) for w,A in safe]+[(theta*w,A) for w,A in bad];assert all(w>0 for w,A in law);S=[[sum(w*A[i]*A[j] for w,A in law) for j in range(4)] for i in range(4)];b.pd(S);b.pd(H);assert a>0
u0,u1=b.var(2,0),b.var(2,1);norm3=b.mul(b.mul(b.add(b.mul(u0,u0),b.mul(u1,u1)),b.add(b.mul(u0,u0),b.mul(u1,u1))),b.add(b.mul(u0,u0),b.mul(u1,u1)));lagpolys=[]
for j in range(4):lagpolys.append({(3-k,k):I[k][j] for k in range(4) if I[k][j]})
gates=[]
for gamma in (0,1):
 rz=b.add(*(b.scale(P,rr[4*gamma+j]) for j,P in enumerate(lagpolys)));quad=b.add(*(b.scale(b.mul(P,Q),dd[4*gamma+i][4*gamma+j]) for i,P in enumerate(lagpolys) for j,Q in enumerate(lagpolys)));gate=b.add(b.scale(norm3,2*4096*s*a),b.scale(quad,-a),b.scale(b.mul(rz,rz),-1));univ={(e[1],):co for e,co in gate.items()};assert len(univ)==len(gate);assert univ.get((0,),0)>0 and univ.get((6,),0)>0 and b.root_count(univ)==0;gates.append(gate)
# Choose a rational unnormalized output vector near the worst orbit.
_,gamma,th=req
if abs(np.cos(th))>=abs(np.sin(th)):u=(R(1),R(round(np.tan(th)*10**8),10**8))
else:u=(R(round(1/np.tan(th)*10**8),10**8),R(1))
ll=[sum(co*x**pw[0]*y**pw[1] for pw,co in P.items()) for P in lagpolys for x,y in [u]];C=b.add(*(b.scale(CP[4*gamma+j],co) for j,co in enumerate(ll)));w=[sum(B[i][4*gamma+j]*ll[j] for j in range(4)) for i in range(4)];hw=r.m.linear_solve(H,w);c=avg(C,law);res=c-g.dot(v,hw);nu=R(1859)*(u[0]*u[0]+u[1]*u[1])**3;bb=2*nu*s-g.dot(w,hw);assert bb>0 and a*bb-res*res<0;rho=-res/a;M=[-rho*x-y for x,y in zip(hv,hw)];p=b.add(F,C,b.scale(T,nu));neg=sum(ww*b.evaluate(p,[x+rho*y for x,y in zip(M,A)]) for ww,A in law)-b.evaluate(p,M);assert neg==rho*rho*(bb-res*res/a)/2<0
# Probe other retained QC quartics; this cannot exhaust known QC tests.
det=b.add(b.mul(A[0],A[3]),b.scale(b.mul(A[1],A[2]),-1));T2=b.mul(T,T);D2=b.mul(det,det);TD=b.mul(T,det);rotational=[]
for ss in (R(-9,10),R(-1,2),R(0),R(1,2),R(9,10)):
 P=b.add(T2,b.scale(TD,-4*ss),b.scale(D2,6*ss*ss-2));HH=[[avg(b.diff(b.diff(P,i),j),law) for j in range(4)] for i in range(4)];vv=[avg(b.diff(P,i),law) for i in range(4)];hh=r.m.linear_solve(HH,vv);aa=2*avg(P,law)-g.dot(vv,hh);rotational.append({'s':str(ss),'Schur_excess':str(aa),'passes_all_means':aa>=0})
out={'object_type':'POSITIVE_ATOMIC_FREE_MATRIX_LAW_NOT_A_GRADIENT','mixing_parameter':str(theta),'atom_weights':[str(w) for w,A in law],'atoms':[list(map(str,A)) for w,A in law],'mean_zero':True,'determinant_moment_zero':True,'full_covariance':True,'strict_leading_F_excess':str(a),'all_4096_seed_symmetry_translation_scaling_QC_tests_pass_strictly':True,'QC_orbit_sextic_gates':[[list(e)+[co.numerator,co.denominator] for e,co in sorted(P.items())] for P in gates],'sextic_real_root_counts':[0,0],'negative_global_ROC_orbit_output':list(map(str,u)),'negative_global_ROC_orbit_Gamma':gamma,'negative_global_ROC_orbit_cubic':[list(e)+[co.numerator,co.denominator] for e,co in sorted(C.items())],'negative_global_ROC_quadratic_coefficient':str(nu),'negative_free_energy_mean':list(map(str,M)),'negative_free_energy_amplitude':str(rho),'negative_free_energy':str(neg),'normalized_negative_free_energy':str(neg/rho**4),'rotational_QC_probes':rotational,'actual_gradient_realization':'UNKNOWN; this is only a free law and may be ruled out by other QC inequalities','genuine_ROC_QC_separation':False,'largest_required_seed_coefficient_numerical':req[0],'bisection_iterations':iteration+1,'seconds':time.perf_counter()-start};(root/'work/orbit_gate_free_law.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'free_atoms':len(law),'largest_required_coefficient_numerical':req[0],'strict_full_orbit_QC_gates_verified':True,'negative_free_ROC_energy':float(neg/rho**4),'rotational_probe_passes':[q['passes_all_means'] for q in rotational],'actual_gradient_realization':out['actual_gradient_realization'],'seconds':time.perf_counter()-start},indent=2),flush=True)
