"""An exact actual-field fixture for zero-weight normal relaxation.

Piecewise-polynomial scalar potentials have disjoint base-stress and
normal-curl supports. Their actual Poisson/Hodge corrector is explicit.
Receive a nonzero nonlocal linear interaction, failure of a finite 1/a
normal cost, and a strict finite-a lowering at scale a^(-2/3).
No grid, numeric derivative, free matrix law, or solver is used.
"""
from pathlib import Path
from fractions import Fraction as R
from math import factorial
import importlib.util,json,time
HERE=Path(__file__).resolve().parent;sp=importlib.util.spec_from_file_location('degenerate_normal_algebra',HERE.parent/'quartic_coupling/receive.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
add,mul,sc,power,diff,var=m.add,m.mul,m.sc,m.powp,m.diff,m.var
one={(0,):R(1)};x=var(1,0);zero={}
def integral(P,lo,hi):return sum((c*(hi**(pw[0]+1)-lo**(pw[0]+1))/(pw[0]+1) for pw,c in P.items()),R(0))
def paired_integral(P,fields,xbox,ybox):
 out=R(0)
 for pw,c in P.items():
  px=one;py=one
  for (fx,fy),k in zip(fields,pw):
   if k:px=mul(px,power(fx,k)) if fx else {};py=mul(py,power(fy,k)) if fy else {}
  out+=c*integral(px,*xbox)*integral(py,*ybox)
 return out
def plateau():
 intervals=[(R(-5,2),R(-3,2)),(R(-3,2),R(3,2)),(R(3,2),R(5,2))];pieces=[]
 for i,box in enumerate(intervals):
  if i==1:chi=one
  else:
   s=add(sc(x,-1 if i==0 else 1),sc(one,-R(3,2)));chi=add(one,sc(power(s,3),-10),sc(power(s,4),15),sc(power(s,5),-6))
  pieces.append((box,mul(x,chi)))
 for i,bound in ((0,R(-5,2)),(2,R(5,2))):
  for j in range(3):assert m.evaluate(pieces[i][1] if j==0 else diff(pieces[i][1],0) if j==1 else diff(diff(pieces[i][1],0),0),[bound])==0
 # eta=x*y on the entire plateau, including a neighborhood of the
 # base's support. Receive value, first and second derivative matching.
 for i,bound in ((0,R(-3,2)),(2,R(3,2))):
  pp=pieces[i][1];qq=x
  for _ in range(3):assert m.evaluate(pp,[bound])==m.evaluate(qq,[bound]);pp=diff(pp,0);qq=diff(qq,0)
 return pieces
def main():
 start=time.perf_counter();rr=R(3,4);F,H=m.n901(rr);c=1/(R(201326592)*(1+rr**4));delta=c/16;N4=power(m.raw_norm(),2);H1=add(H,sc(N4,-delta));P,W,constants=m.compile_extension(F,H,H1,delta,c,c/2);aa=R(constants['a']);assert aa.denominator==1 and constants['a_power_of_two']%3==0;roota=R(2)**(constants['a_power_of_two']//3);assert roota**3==aa;s=1/(roota**2)
 sym_coordinates,curl_coordinate=m.coordinates();assert P==add(F,sc(mul(power(curl_coordinate,2),m.substitute(m.raw_norm(),sym_coordinates)),2*delta*aa),sc(power(curl_coordinate,4),delta*aa**2))
 f=power(add(one,sc(power(x,2),-1)),4);fp=diff(f,0);fpp=diff(fp,0)
 for boundary in (R(-1),R(1)):
  ff=f
  for _ in range(4):assert m.evaluate(ff,[boundary])==0;ff=diff(ff,0)
 base=[(fpp,f),(fp,fp),(fp,fp),(f,fpp)];core=(R(-1),R(1));coeff=[];direction=F
 assert integral(fp,*core)==0 and integral(fpp,*core)==0
 assert all(integral(fx,*core)*integral(fy,*core)==0 for fx,fy in base)
 for k in range(4):
  coeff.append(paired_integral(direction,base,core,core)/(36*factorial(k)));direction=add(diff(direction,0),sc(diff(direction,3),-1))
 p,q,w,t=[var(4,i) for i in range(4)];normsym=add(power(p,2),sc(power(sc(add(q,w),R(1,2)),2),2),power(t,2));curl=add(q,sc(w,-1));Bpoly=mul(power(curl,2),normsym);Cpoly=power(curl,4);B=C=A4=R(0);meanE=[R(0)]*4;meanZ=R(0)
 for xbox,kx in plateau():
  for ybox,ky in plateau():
   kxp=diff(kx,0);kxpp=diff(kxp,0);kyp=diff(ky,0);kypp=diff(kyp,0);E=[(kxp,kyp),(kx,kypp),(sc(kxpp,-1),ky),(sc(kxp,-1),kyp)];A4+=paired_integral(F,E,xbox,ybox)/36;B+=paired_integral(Bpoly,E,xbox,ybox)/36;C+=paired_integral(Cpoly,E,xbox,ybox)/36
   for i in range(4):meanE[i]+=integral(E[i][0],*xbox)*integral(E[i][1],*ybox)/36
   meanZ+=paired_integral(curl,E,xbox,ybox)/36
 assert meanE==[R(0)]*4 and meanZ==0 and C>0 and B>=0 and A4>0;coeff.append(A4);assert coeff[0]>0 and coeff[1]!=0 and coeff[2]>=0 and coeff[3]==0
 # Choose the sign of eta to lower the energy, then a rational trial
 # magnitude so the limiting quartic balance is strictly negative.
 sign=R(-1) if coeff[1]>0 else R(1);linear=sign*coeff[1];tau=min(R(1),-linear/(2*delta*C));limit=linear*tau+delta*C*tau**4;assert linear<0 and limit<0
 lowering=s*tau*linear+s*s*tau*tau*coeff[2]+s**4*tau**4*(A4+2*delta*aa*B+delta*aa*aa*C);after=coeff[0]+lowering;assert lowering<0 and after>0
 # At the OLD scale 1/a, the quadratic normal coefficient is exactly
 # zero, while the actual linear coefficient is nonzero. Multiplying
 # this same corrector by any positive integer sends that coefficient
 # to minus infinity.
 trial_old=linear*tau;assert trial_old<0
 result={'r':str(rr),'periodic_cell':'[-3,3]^2, normalized area 36','base_potential':'psi=(1-x^2)^4_+*(1-y^2)^4_+','normal_potential':'eta=x*y*chi(x)*chi(y); chi=1 on [-3/2,3/2], quintic transition to 0 at +/-5/2','base_Hessian_support':'[-1,1]^2','normal_curl_zero_on_base_support':True,'base_and_normal_mean_gradients_exactly_zero':True,'actual_normal_corrector':'E=-J Hess eta; curl(E)=Delta eta; its Hessian Hodge component is zero','exact_base_energy':str(coeff[0]),'exact_linear_nonlocal_interaction':str(linear),'exact_quadratic_source_coefficient':str(coeff[2]),'exact_cubic_source_coefficient':str(coeff[3]),'exact_quartic_source_coefficient':str(A4),'normal_mixed_quartic_moment_B':str(B),'normal_fourth_moment_C':str(C),'regular_1_over_a_coefficient_infimum':'MINUS_INFINITY','critical_scale':'a^(-2/3)','trial_magnitude':str(tau),'exact_negative_critical_limit_cost':str(limit),'admitted_full_quartic_a':str(aa),'a_power_of_two':constants['a_power_of_two'],'critical_scale_exact_rational':str(s),'finite_a_actual_energy_lowering':str(lowering),'finite_a_positive_total_Jensen_gap':str(after),'quasiconvexity_counterexample':False,'source_and_correction_regularity':'piecewise polynomial C3 and C2 potentials; actual W1,infinity gradients; separated supports permit smooth approximation preserving a nonzero interaction','seconds':time.perf_counter()-start};(HERE/'replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'actual_nonlocal_linear_interaction':float(linear),'base_energy':float(coeff[0]),'normal_fourth_moment':float(C),'negative_critical_limit_cost':float(limit),'regular_scale_infimum':'MINUS_INFINITY','critical_scale':'a^(-2/3)','exact_finite_a_lowering_sign':'NEGATIVE','total_Jensen_gap_sign':'POSITIVE','quasiconvexity_counterexample':False,'seconds':result['seconds']},indent=2))
if __name__=='__main__':main()
